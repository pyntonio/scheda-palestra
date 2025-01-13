from fastapi import FastAPI, HTTPException, APIRouter, Query, BackgroundTasks, Depends
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
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from auth.auth import decode_token, create_confirmation_token  # Usa la funzione corretta
from fastapi.security import OAuth2PasswordBearer
import secrets


Base.metadata.create_all(bind=engine)

app = FastAPI()

# Middleware per CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Sostituisci con il dominio del frontend in produzione
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurazione per la gestione delle password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Definisci il sistema di autorizzazione con OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Funzione per hash delle password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

@app.post("/register/")  # Endpoint per la registrazione
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    current_time = datetime.now()
    
    user_data = {
        "username": user.username,
        "email": user.email,
        "password_hash": hashed_password,
        "created_at": current_time,
        "updated_at": current_time
    }
    
    # Crea l'utente nel database
    new_user = create_user(db=db, user=user_data)

    # Invia l'email di conferma
    send_confirmation_email(user.email, new_user.id)

    return {"message": "User registered successfully", "user": new_user}

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

@app.get("/confirm-email")
def confirm_email(token: str = Query(...), db: Session = Depends(get_db)):
    try:
        # Decodifica il token per ottenere l'ID dell'utente
        decoded_token = decode_token(token)
        user_id = decoded_token["user_id"]
        
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.is_verified = True
            db.commit()
            return {"message": "Email confermata con successo!"}
        else:
            raise HTTPException(status_code=404, detail="Utente non trovato")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Token non valido o scaduto")

# Funzione per inviare l'email di conferma
def send_confirmation_email(to_email: str, user_id: int):
    from_email = os.getenv("MAIL_USERNAME")  # Usa variabili di ambiente
    password = os.getenv("MAIL_PASSWORD")  # Usa variabili di ambiente

    if not from_email or not password:
        raise HTTPException(status_code=500, detail="Email configuration is missing")

    subject = "Conferma la tua registrazione"
    
    # Crea un token di conferma per l'utente
    token = create_confirmation_token(user_id)  # Usa la funzione corretta da auth.py

    body = f"""
    Ciao! Grazie per esserti registrato. Per favore, clicca sul link sottostante per confermare la tua registrazione:

    http://localhost:8000/confirm-email?token={token}
    """

    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore nell'invio dell'email: {e}")

# Endpoint per proteggere l'accesso con il token JWT
@app.get("/protected")
def protected_route(token: str = Depends(oauth2_scheme)):  # Usa oauth2_scheme per gestire il token
    try:
        decoded_data = decode_token(token)  # Decodifica il token
        return {"message": "Access granted", "user": decoded_data}
    except HTTPException as e:
        raise e

# Endpoint per ottenere dati protetti
@app.get("/secure-data")
def get_secure_data(token: str = Depends(oauth2_scheme)):
    decoded_token = decode_token(token)
    if decoded_token:
        return {"data": "This is secured data!"}
    else:
        raise HTTPException(status_code=403, detail="Unauthorized")
