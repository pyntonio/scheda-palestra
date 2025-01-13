from fastapi import FastAPI, HTTPException, APIRouter, BackgroundTasks, Depends
from fastapi.responses import FileResponse, JSONResponse
from email.message import EmailMessage
from oroscope.oroscope import genera_oroscopo
import os
from models import OroscopoRequest, User  # Importa il modello che hai creato
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from db_config.db_config import Base, engine, get_db
from crud.crud import create_user, get_user_by_email
from schemas.schemas import UserCreate, UserOut
from passlib.context import CryptContext
from schemas import schemas
#from mail_config import fm
from datetime import datetime


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Sostituisci con il dominio del frontend in produzione
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


router = APIRouter()

# Endpoint per generare l'oroscopo
@app.post("/genera_oroscopo/") 
async def genera_oroscopo_api(data: dict, background_tasks: BackgroundTasks):
    try:
        # Genera l'oroscopo e il PDF tramite la funzione principale
        result = await genera_oroscopo(data)  # Genera l'oroscopo e il PDF
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        # Estrai il nome del PDF dal percorso restituito
        pdf_filename = result.get("pdf_path").split("/")[-1]  # Estrai il nome del PDF dal path
        
        # Recupera il testo dell'oroscopo (contenuto in markdown)
        oroscopo_text = result.get("testo", "")  # Prendi il testo in markdown

        # Restituisci il risultato
        return {
            "message": "Oroscopo generato e PDF in fase di creazione.",
            "oroscopo_text": oroscopo_text,  # Restituisci anche il testo dell'oroscopo
            "pdf_filename": pdf_filename
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint per scaricare il PDF generato
@app.get("/download_oroscopo/{pdf_filename}")
async def download_oroscopo(pdf_filename: str):
    percorso_pdf = os.path.join("static", "oroscopi", pdf_filename)
    
    # Verifica che il PDF esista
    if not os.path.exists(percorso_pdf):
        raise HTTPException(status_code=404, detail="PDF non trovato")
    
    # Restituisci il PDF come risposta
    return FileResponse(percorso_pdf, media_type="application/pdf", filename=pdf_filename)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

@app.post("/register/")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Hash della password
    hashed_password = hash_password(user.password)
    
    # Ottieni il timestamp corrente
    current_time = datetime.now()
    
    # Creazione del dizionario per il database
    user_data = {
        "username": user.username,
        "email": user.email,
        "password_hash": hashed_password,
        "created_at": current_time,
        "updated_at": current_time
    }
    
    # Creazione dell'utente
    new_user = create_user(db=db, user=user_data)
    
    return {"message": "User registered successfully", "user": new_user}