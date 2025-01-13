from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from pdf_generator.pdf_creator import genera_pdf_da_markdown
from lang.prompts import get_prompts
from oroscope.natale_card import calcola_carta_natale
from db_config.db_config import get_db
from models import Horoscope, AstrologicalDetails, HoroscopeGeneration, GenericHoroscope
import openai
import os
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# Carica la chiave API di OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Verifica che la chiave API sia stata caricata correttamente
if openai.api_key is None:
    raise ValueError("La chiave API non è stata trovata. Assicurati che il file .env contenga OPENAI_API_KEY.")

async def genera_oroscopo(data: dict, db: Session = Depends(get_db)):  # Assicurati che db sia una sessione
    try:
        # Estrai i dati dal dizionario
        user_id = data.get("user_id")  # ID dell'utente che richiede l'oroscopo
        nome = data["nome"]
        data_nascita = data["data_nascita"]
        ora_nascita = data["ora_nascita"]
        luogo_nascita = data["luogo_nascita"]
        lingua = data.get("lingua", "it")
        tipi = data.get("tipi", "generico")  # Tipo singolo, non lista

        # Calcola la carta natale
        carta_natale = calcola_carta_natale(data_nascita, ora_nascita, luogo_nascita)

        # Ottieni i prompt per i tipi di oroscopo richiesti
        prompts = get_prompts(nome, data_nascita, ora_nascita, luogo_nascita, carta_natale, lingua=lingua, tipi=tipi)

        # Creazione della risposta
        oroscopi = {}

        for tipo, lista_prompt in prompts.items():
            oroscopi[tipo] = []

            # Esegui la chiamata API per ciascun prompt separatamente
            for prompt in lista_prompt:
                response = openai.ChatCompletion.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=2000,
                    temperature=0.7
                )

                # Aggiungi la risposta per il tipo di oroscopo
                oroscopi[tipo].append(response.choices[0].message['content'].strip())

        # Genera il PDF con il contenuto dell'oroscopo
        markdown_content = "\n".join(oroscopi.get('generico', []))  # Combina tutte le risposte generiche
        pdf_filename = f"oroscopo_{nome}_{data_nascita}.pdf"
        pdf_path = await genera_pdf_da_markdown(markdown_content, pdf_filename)

        # Salva l'oroscopo nel database
        new_horoscope = GenericHoroscope(
            user_id=user_id,
            name=nome,
            birth_date=data_nascita,
            birth_place=luogo_nascita,
            horoscope_text=markdown_content,
            pdf_filename=pdf_filename
        )
        db.add(new_horoscope)
        db.commit()
        db.refresh(new_horoscope)

        # Salva i dettagli astrologici (opzionale)
        new_astrological_details = AstrologicalDetails(
            horoscope_id=new_horoscope.id,
            mercury=carta_natale.get("mercury"),
            venus=carta_natale.get("venus"),
            mars=carta_natale.get("mars"),
            jupiter=carta_natale.get("jupiter"),
            saturn=carta_natale.get("saturn"),
            neptune=carta_natale.get("neptune"),
            uranus=carta_natale.get("uranus")
        )
        db.add(new_astrological_details)
        db.commit()

        # Registra l'evento di generazione
        horoscope_generation = HoroscopeGeneration(
            user_id=user_id,
            horoscope_type=tipi
        )
        db.add(horoscope_generation)
        db.commit()

        # Restituisci il risultato
        return {
            "oroscopi": oroscopi,
            "pdf_path": pdf_path,
            "testo": markdown_content,
            "horoscope_id": new_horoscope.id
        }

    except Exception as e:
        db.rollback()  # Questo ora è valido
        return {"error": str(e)}
