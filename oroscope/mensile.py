from fastapi import HTTPException
from lang.prompts import get_prompts
from oroscope.natale_card import calcola_carta_natale
import openai
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from models import MonthlyHoroscope  # Importa il modello della tabella MonthlyHoroscope

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# Carica la chiave API di OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Verifica che la chiave API sia stata caricata correttamente
if openai.api_key is None:
    raise ValueError("La chiave API non è stata trovata. Assicurati che il file .env contenga OPENAI_API_KEY.")

async def genera_oroscopo_mensile(data: dict, db: Session):
    try:
        # Estrai i dati dal dizionario
        nome = data["nome"]
        data_nascita = data["data_nascita"]
        ora_nascita = data["ora_nascita"]
        luogo_nascita = data["luogo_nascita"]
        lingua = data.get("lingua", "it")
        
        # Calcola la carta natale
        carta_natale = calcola_carta_natale(data_nascita, ora_nascita, luogo_nascita)
        print("Risultato della carta natale:", carta_natale)  # Verifica il contenuto
        
        # Ottieni i segni zodiacali
        sun_sign = carta_natale['segno_solare']['segno']  # Modifica per usare la chiave corretta
        ascendant_sign = carta_natale['ascendente']['segno']  # Modifica per usare la chiave corretta
        moon_sign = carta_natale['luna']  # Modifica se serve una chiave specifica per la luna

        # Verifica i segni zodiacali
        print("Segno Solare:", sun_sign)
        print("Ascendente:", ascendant_sign)
        print("Luna:", moon_sign)

        # Ottieni i prompt per l'oroscopo mensile
        prompts = get_prompts(nome, data_nascita, ora_nascita, luogo_nascita, carta_natale, lingua=lingua, tipi="mensile")
        print("Prompts generati:", prompts)  # Verifica il contenuto dei prompts

        oroscopi = {}
        
        # Esegui la chiamata API per ciascun prompt separatamente
        for tipo, lista_prompt in prompts.items():
            oroscopi[tipo] = []
            for prompt in lista_prompt:
                response = openai.ChatCompletion.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=2000,
                    temperature=0.7
                )
                oroscopi[tipo].append(response.choices[0].message['content'].strip())

        # Salva nel database
        new_oroscopo = MonthlyHoroscope(
            user_id=data['user_id'],  # ID dell'utente
            birthdate=data_nascita,
            birthplace=luogo_nascita,
            sun_sign=sun_sign,
            ascendant_sign=ascendant_sign,
            moon_sign=moon_sign,
            generated_text="\n".join(oroscopi.get('mensile', [])),  # Testo generato
        )
        
        db.add(new_oroscopo)
        db.commit()
        db.refresh(new_oroscopo)

        # Restituisci i dati necessari per il PDF
        return {
            "message": "Oroscopo mensile generato con successo!",
            "generated_text": "\n".join(oroscopi.get('mensile', [])),
            "pdf_filename": f"{new_oroscopo.id}_mensile.pdf"  # Aggiungi un nome per il PDF
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
