from fastapi import HTTPException
from lang.prompts import get_prompts
from oroscope.natale_card import calcola_carta_natale
import openai
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from models import Horoscope  # Importa il modello della tabella Horoscopes

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# Carica la chiave API di OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Verifica che la chiave API sia stata caricata correttamente
if openai.api_key is None:
    raise ValueError("La chiave API non è stata trovata. Assicurati che il file .env contenga OPENAI_API_KEY.")

async def genera_oroscopo_generico(data: dict, db: Session):
    try:
        # Estrai i dati dal dizionario
        nome = data["nome"]
        data_nascita = data["data_nascita"]
        ora_nascita = data["ora_nascita"]
        luogo_nascita = data["luogo_nascita"]
        lingua = data.get("lingua", "it")
        
        # Calcola la carta natale
        carta_natale = calcola_carta_natale(data_nascita, ora_nascita, luogo_nascita)

        # Ottieni i prompt per l'oroscopo generico
        prompts = get_prompts(nome, data_nascita, ora_nascita, luogo_nascita, carta_natale, lingua=lingua, tipi="generico")

        oroscopi = {}
        
        # Esegui la chiamata API per ciascun prompt separatamente
        for tipo, lista_prompt in prompts.items():
            oroscopi[tipo] = []
            for prompt in lista_prompt:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=2000,
                    temperature=0.7
                )
                oroscopi[tipo].append(response.choices[0].message['content'].strip())

        # Estrai i segni zodiacali
        sun_sign = carta_natale['sun_sign']  # Supponiamo che la funzione calcola_carta_natale restituisca questi dati
        ascendant_sign = carta_natale['ascendant_sign']
        moon_sign = carta_natale['moon_sign']

        # Salva nel database
        new_oroscopo = Horoscope(
            user_id=data['user_id'],  # Assumiamo che l'utente venga passato come parte di 'data'
            birthdate=data_nascita,
            birthplace=luogo_nascita,
            sun_sign=sun_sign,
            ascendant_sign=ascendant_sign,
            moon_sign=moon_sign,
            generated_text="\n".join(oroscopi.get('generico', [])),  # Salviamo il testo generato
        )
        
        db.add(new_oroscopo)
        db.commit()
        db.refresh(new_oroscopo)

        return {"message": "Oroscopo generico generato con successo!"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
