from fastapi import FastAPI, HTTPException, APIRouter, Query, BackgroundTasks, Depends, status
from fastapi.responses import FileResponse, JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from email.message import EmailMessage
from oroscope.oroscope import genera_oroscopo
import os
from models import OroscopoRequest, MonthlyHoroscope, User  # Importa il modello che hai creato
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
from datetime import datetime, timedelta, time
from auth.auth import decode_token, create_confirmation_token  
from fastapi.security import OAuth2PasswordBearer
import secrets
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import HTMLResponse
from oroscope.mensile import genera_oroscopo_mensile
from oroscope.generico import  genera_oroscopo_generico
from auth.auth_utils import verify_password, create_access_token
from auth.dependencies import get_current_user
from pydantic import BaseModel
from oroscope.natale_card import calcola_carta_natale
import models
import stripe

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

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
templates = Jinja2Templates(directory="templates")
# Funzione per hash delle password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

@app.post("/register/")  # Endpoint per la registrazione
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        # Hash della password
        hashed_password = hash_password(user.password)
        current_time = datetime.now()
        
        user_data = {
            "username": user.username,
            "email": user.email,
            "password_hash": hashed_password,
            "is_verified": False,
            "created_at": current_time,
            "updated_at": current_time
        }

        # Crea l'utente nel database
        new_user = create_user(db=db, user=user_data)

        # Se la creazione è riuscita, invia l'email di conferma
        send_confirmation_email(user.email, new_user.id)

        return {"message": "User registered successfully", "user": new_user}
    
    except Exception as e:
        # Se c'è un errore durante la registrazione, restituisci un errore HTTP
        raise HTTPException(status_code=400, detail=f"Error occurred during registration: {str(e)}")

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Cerca l'utente tramite l'email
    user = db.query(User).filter(User.email == form_data.username).first()
    
    # Verifica se l'utente esiste, se la password è corretta, e se l'utente è verificato
    if not user or not verify_password(form_data.password, user.password_hash):  # Cambia 'hashed_password' con 'password_hash'
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verifica se l'utente è verificato
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not verified",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Crea il token di accesso
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


# Definizione del modello per la richiesta
class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str
# Endpoint che utilizza ChangePasswordRequest
@app.post("/change-password")
def change_password(
    change_request: ChangePasswordRequest,  # Modello della richiesta
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == current_user).first()

    # Verifica la password usando 'password_hash'
    if not user or not verify_password(change_request.current_password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect current password",
        )

    user.password_hash = hash_password(change_request.new_password)
    db.commit()
    return {"message": "Password updated successfully"}

@app.get("/secure-data")
def read_secure_data(
    current_user: str = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """
    Endpoint protetto accessibile solo agli utenti autenticati.
    Restituisce informazioni dettagliate sull'utente, inclusa la carta natale.
    """
    # Recupera l'utente e la carta natale associata usando una join
    user_with_card = (
        db.query(models.User, models.NataleCard)
        .join(models.NataleCard, models.NataleCard.user_id == models.User.id, isouter=True)
        .filter(models.User.email == current_user)
        .first()
    )

    if not user_with_card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User or natal chart not found",
        )
    
    user, natal_card = user_with_card

    # Formattazione born_hour se presente
    born_hour_formatted = None
    if user.born_hour is not None:
        total_seconds = user.born_hour.total_seconds()  # Ottieni i secondi totali da timedelta
        born_hour_formatted = time(
            int(total_seconds // 3600), 
            int((total_seconds % 3600) // 60)
        ).strftime("%H:%M:%S")

    # Costruisci la risposta
    response = {
        "message": f"Hello, {user.username}! This is your secure data.",
        "username": user.username,
        "name": user.name,
        "surname": user.surname,
        "email": user.email,
        "born_date": user.born_date,
        "born_hour": born_hour_formatted,  # Ora formattata
        "born_place": user.born_place,
        "created_at": user.created_at,
        "updated_at": user.updated_at,
        "is_verified": bool(user.is_verified),
    }

    # Aggiungi i dati della carta natale se disponibili
    if natal_card:
        response.update({
            "sun_sign": natal_card.sun_sign,
            "ascendant": natal_card.ascendant,
        })

    return response

# Definisci il Pydantic model per l'aggiornamento delle informazioni utente
class UserUpdate(BaseModel):
    name: str
    surname: str
    born_date: str  # Assuming a string format, you can adjust according to your DB schema
    born_hour: str  # If you want to store this as string (or use datetime.time)
    born_place: str


# Endpoint per aggiornare i dati utente
@app.put("/update-user/")
def update_user_info(
    user_update: UserUpdate,
    current_user: str = Depends(get_current_user),  # Assicura che l'utente sia autenticato
    db: Session = Depends(get_db)
):
    # Recupera l'utente dal database basandosi sull'email nel token
    user = db.query(models.User).filter(models.User.email == current_user).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Converti la data in formato 'dd-mm-yyyy' a 'yyyy-mm-dd' prima di salvarla
    try:
        # Converti la data nel formato 'dd-mm-yyyy' in 'yyyy-mm-dd'
        user_update.born_date = datetime.strptime(user_update.born_date, "%d-%m-%Y").strftime("%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Please use dd-mm-yyyy")

    # Aggiorna le informazioni dell'utente con i nuovi dati
    user.name = user_update.name
    user.surname = user_update.surname
    user.born_date = datetime.strptime(user_update.born_date, "%Y-%m-%d")  # Assicurati che il formato sia 'YYYY-MM-DD'
    user.born_hour = user_update.born_hour  # Adjust based on your schema if it's stored as datetime.time
    user.born_place = user_update.born_place
    user.updated_at = datetime.now()  # Update the timestamp
    
    # Commit delle modifiche nel database
    db.commit()

    # Ora calcoliamo la carta natale
    try:
        # Chiamata alla funzione per calcolare la carta natale
        carta_natale = calcola_carta_natale(
            user_update.born_date,
            user_update.born_hour,
            user_update.born_place
        )

        # Controlliamo se l'utente ha già una carta natale
        existing_card = db.query(models.NataleCard).filter(models.NataleCard.user_id == user.id).first()
        
        if existing_card:
            # Se la carta natale esiste già, aggiorniamo i dati
            existing_card.sun_sign = carta_natale["segno_solare"]["segno"]
            existing_card.sun_sign_description = carta_natale["segno_solare"]["descrizione"]
            existing_card.ascendant = carta_natale["ascendente"]["segno"]
            existing_card.ascendant_description = carta_natale["ascendente"]["descrizione"]
            existing_card.planets = carta_natale["pianeti"]
            existing_card.birth_date = user_update.born_date
            existing_card.birth_time = user_update.born_hour
            existing_card.birth_place = user_update.born_place
            existing_card.updated_at = datetime.now()  # Update the timestamp
            db.commit()
        else:
            # Se non esiste, creiamo una nuova carta natale per l'utente
            new_card = models.NataleCard(
                user_id=user.id,
                birth_date=user_update.born_date,
                birth_time=user_update.born_hour,
                birth_place=user_update.born_place,
                sun_sign=carta_natale["segno_solare"]["segno"],
                sun_sign_description=carta_natale["segno_solare"]["descrizione"],
                ascendant=carta_natale["ascendente"]["segno"],
                ascendant_description=carta_natale["ascendente"]["descrizione"],
                planets=carta_natale["pianeti"]
            )
            db.add(new_card)
            db.commit()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while calculating natal chart: {str(e)}")
    
    # Ritorna i dati aggiornati dell'utente insieme alla carta natale
    return {
        "message": "User data and natal chart updated successfully",
        "user": {
            "name": user.name,
            "surname": user.surname,
            "born_date": user.born_date.strftime("%Y-%m-%d"),
            "born_hour": user.born_hour,
            "born_place": user.born_place,
            "updated_at": user.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        },
        "natal_chart": carta_natale
    }


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

@app.get("/confirm-email", response_class=HTMLResponse)
def confirm_email(request: Request, token: str = Query(...), db: Session = Depends(get_db)):
    try:
        # Decodifica il token per ottenere l'ID dell'utente
        decoded_token = decode_token(token)
        user_id = decoded_token["user_id"]
        
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.is_verified = True 
            db.commit()
            return templates.TemplateResponse("confirm_success.html", {"request": request, "message": "Email confermata con successo!"})
        else:
            return templates.TemplateResponse("confirm_error.html", {"request": request, "message": "Utente non trovato"})
    except Exception as e:
        return templates.TemplateResponse("confirm_error.html", {"request": request, "message": "Token non valido o scaduto"})

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




@app.post("/genera_oroscopo_mensile/")
async def genera_oroscopo_mensile_api(data: dict, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    try:
        # Passiamo i dati ricevuti dall'utente alla funzione genera_oroscopo_mensile
        result = await genera_oroscopo_mensile(data, db)  # Genera l'oroscopo mensile
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        # Estrai il testo dell'oroscopo mensile (contenuto in markdown)
        oroscopo_text = result.get("generated_text", "")  # Prendi il testo generato

        # Estrai il nome del PDF dal percorso restituito (se presente)
        pdf_filename = result.get("pdf_filename", "").split("/")[-1]  # Estrai il nome del PDF dal path
        
        # Restituisci il risultato
        return {
            "message": "Oroscopo mensile generato con successo!",
            "oroscopo_text": oroscopo_text,  # Restituisci anche il testo dell'oroscopo
            "pdf_filename": pdf_filename
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/genera_oroscopo_generico/")
async def genera_oroscopo_generico_api(data: dict, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    try:
        # Passiamo i dati ricevuti dall'utente alla funzione genera_oroscopo_generico
        result = await genera_oroscopo_generico(data, db)  # Genera l'oroscopo

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        # Restituisci il risultato
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/get_monthly_horoscopes/")
def get_monthly_horoscopes(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    try:
        # Recuperiamo l'utente tramite l'email estratta dal token
        user = db.query(User).filter(User.email == current_user).first()

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        # Usando l'ID dell'utente per fare la query sugli oroscopi
        horoscopes = db.query(MonthlyHoroscope).filter(MonthlyHoroscope.user_id == user.id).all()

        if not horoscopes:
            raise HTTPException(status_code=404, detail="No horoscopes found for this user")

        return {"horoscopes": horoscopes}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




# Stripe payments https://chatgpt.com/share/674f4d56-94a8-8011-bccf-ab9d0195fe63
# TO-DO
# 1. gestire webhook per ritorno dati su DB (necessaria macchina esposta a internet o ngrok)
# 2. Creare pagine success o denied su react app dummy
# 3. logica di automatismo per generazione mensile degli oroscopi tramite script cronjobs?
#

# Modello per ricevere i dettagli del piano
class PaymentRequest(BaseModel):
    plan: str  # "monthly" o "yearly"

@app.post("/create-checkout-session")
async def create_checkout_session(request: PaymentRequest):
    try:
        # ID dei prodotti/piani creati su Stripe
        prices = {
            "monthly": "price_1QU52sEb1r0toAUQ4jlWSmBy",  # Sostituisci con l'ID del piano mensile (id di prezzo non di prodotto)
            "yearly": "price_1Qc8GuEb1r0toAUQbnNzRN27",  # Sostituisci con l'ID del piano annuale
        }
        if request.plan not in prices:
            raise HTTPException(status_code=400, detail="Piano non valido")

        # Creazione della sessione di pagamento
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="subscription",  # Modalità abbonamento
            line_items=[{"price": prices[request.plan], "quantity": 1}],
            success_url="http://localhost:3000/success",  # Modifica con il tuo URL
            cancel_url="http://localhost:3000/cancel",
        )
        return {"sessionId": session.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Weeb hook di ritorno da skype per fare in modo di inserire su DB il nuovo prodotto venduto e così gestire gli user e abbonamenti mensili in automatico
# Necessario avere un dominio esposto (forse ngrok può aiutare in test senza avere una macchina esposta https://ngrok.com) a internet per comunicare con il weebhook di stripe https://dashboard.stripe.com/test/workbench/webhooks nuovo weebhook-->Checkout-->checkout.session.async_payment_succeeded
@app.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    endpoint_secret = "whsec_XXXXXXXXXXXXXXXXXX"  # Segreto del webhook da Stripe

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)

        # Gestisci l'evento (es. pagamento riuscito)
        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            customer_email = session["customer_details"]["email"]
            subscription_id = session["subscription"]

            # Salva nel database
            # Es: salva_email_subscription(customer_email, subscription_id)

        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))