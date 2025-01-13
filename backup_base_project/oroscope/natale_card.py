from skyfield.api import load
from astropy.coordinates import EarthLocation
import astropy.units as u
from astropy.time import Time
from datetime import datetime

# Funzioni di validazione per data e ora
def valida_data(data: str) -> str:
    try:
        # Converte e restituisce la data in formato YYYY-MM-DD
        return datetime.strptime(data, "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        raise ValueError("Formato data non valido. Usa il formato 'YYYY-MM-DD'.")

def valida_ora(ora: str) -> str:
    try:
        # Converte e restituisce l'ora in formato HH:MM
        return datetime.strptime(ora, "%H:%M").strftime("%H:%M")
    except ValueError:
        raise ValueError("Formato ora non valido. Usa il formato 'HH:MM'.")

# Funzione per determinare il segno zodiacale solare
def determina_segno_zodiacale(gradi_solare):
    segni = [
        ("Ariete", 0, 30),
        ("Toro", 30, 60),
        ("Gemelli", 60, 90),
        ("Cancro", 90, 120),
        ("Leone", 120, 150),
        ("Vergine", 150, 180),
        ("Bilancia", 180, 210),
        ("Scorpione", 210, 240),
        ("Sagittario", 240, 270),
        ("Capricorno", 270, 300),
        ("Acquario", 300, 330),
        ("Pesci", 330, 360),
    ]
    for segno, inizio, fine in segni:
        if inizio <= gradi_solare < fine:
            return segno
    return "Errore"

# Funzione per generare una descrizione astrologica
def genera_descrizione(segno, tipo):
    descrizioni = {
        "Ariete": f"L'{tipo} in Ariete indica energia, determinazione e voglia di agire.",
        "Toro": f"L'{tipo} in Toro rappresenta stabilità, amore per la bellezza e praticità.",
        "Gemelli": f"L'{tipo} in Gemelli suggerisce curiosità, comunicazione e versatilità.",
        "Cancro": f"L'{tipo} in Cancro mostra emotività, protezione e connessione familiare.",
        "Leone": f"L'{tipo} in Leone riflette leadership, creatività e passione.",
        "Vergine": f"L'{tipo} in Vergine simboleggia precisione, intelligenza e attenzione al dettaglio.",
        "Bilancia": f"L'{tipo} in Bilancia parla di equilibrio, armonia e relazioni.",
        "Scorpione": f"L'{tipo} in Scorpione esprime intensità, trasformazione e mistero.",
        "Sagittario": f"L'{tipo} in Sagittario indica ottimismo, espansione e ricerca di verità.",
        "Capricorno": f"L'{tipo} in Capricorno rappresenta ambizione, disciplina e responsabilità.",
        "Acquario": f"L'{tipo} in Acquario suggerisce innovazione, indipendenza e pensiero originale.",
        "Pesci": f"L'{tipo} in Pesci mostra sensibilità, immaginazione e spiritualità."
    }
    return descrizioni.get(segno, f"Descrizione non disponibile per {segno}.")

# Funzione per calcolare l'ascendente
def calcola_ascendente(sun_pos, location, birth_time):
    ts = load.timescale()
    t = ts.from_astropy(birth_time)
    
    # Calcola l'ora siderale locale
    gmst = t.gmst  # Greenwich Mean Sidereal Time in ore
    long = location.lon.deg  # Longitudine in gradi
    lst = (gmst + long / 15) % 24  # Local Sidereal Time in ore
    
    # Converti l'ora siderale in gradi
    lst_degrees = lst * 15  # 360° = 24h, quindi 15° per ogni ora
    
    # L'ascendente è calcolato come il grado sull'orizzonte orientale
    ascendente = (lst_degrees + sun_pos.radec()[0]._degrees) % 360
    return ascendente

def calcola_carta_natale(data_nascita: str, ora_nascita: str, luogo_nascita: str):
    try:
        # Validazione della data e dell'ora
        data_nascita = valida_data(data_nascita)
        ora_nascita = valida_ora(ora_nascita)
        
        # Convertire la data e l'ora di nascita in un formato compatibile con Astropy
        birthdate = f"{data_nascita} {ora_nascita}:00"
        birth_time = Time(birthdate, format='iso')

        # Latitudine e longitudine del luogo di nascita
        lat, lon = map(float, luogo_nascita.split(","))
        location = EarthLocation(lat=lat * u.deg, lon=lon * u.deg)

        # Carica i dati planetari con Skyfield (DE421 ephemeris)
        planets = load('de421.bsp')
        sun = planets['sun']
        moon = planets['moon']
        mars = planets['mars']
        venus = planets['venus']
        mercury = planets['mercury']
        jupiter = planets['jupiter barycenter']
        saturn = planets['saturn barycenter']
        uranus = planets['uranus barycenter']
        neptune = planets['neptune barycenter']
        
        # Calcolare la posizione dei pianeti
        ts = load.timescale()
        t = ts.utc(birth_time.datetime.year, birth_time.datetime.month,
                   birth_time.datetime.day, birth_time.datetime.hour,
                   birth_time.datetime.minute, birth_time.datetime.second)
        
        sun_pos = sun.at(t)
        moon_pos = moon.at(t)
        mars_pos = mars.at(t)
        venus_pos = venus.at(t)
        mercury_pos = mercury.at(t)
        jupiter_pos = jupiter.at(t)
        saturn_pos = saturn.at(t)
        uranus_pos = uranus.at(t)
        neptune_pos = neptune.at(t)
        
        # Posizioni planetarie (astronomical unit - AU)
        pianeti = {
            "Sole": sun_pos.radec()[0]._degrees,
            "Luna": moon_pos.radec()[0]._degrees,
            "Mercurio": mercury_pos.radec()[0]._degrees,
            "Venere": venus_pos.radec()[0]._degrees,
            "Marte": mars_pos.radec()[0]._degrees,
            "Giove": jupiter_pos.radec()[0]._degrees,
            "Saturno": saturn_pos.radec()[0]._degrees,
            "Urano": uranus_pos.radec()[0]._degrees,
            "Nettuno": neptune_pos.radec()[0]._degrees
        }

        # Calcolare il segno zodiacale solare
        segno_solare = determina_segno_zodiacale(pianeti["Sole"])

        # Calcolare l'ascendente
        ascendente_gradi = calcola_ascendente(sun_pos, location, birth_time)
        ascendente_segno = determina_segno_zodiacale(ascendente_gradi)

        # Creare l'output finale
        output = {
            "pianeti": pianeti,
            "segno_solare": {
                "segno": segno_solare,
                "descrizione": genera_descrizione(segno_solare, "Sole")
            },
            "ascendente": {
                "gradi": ascendente_gradi,
                "segno": ascendente_segno,
                "descrizione": genera_descrizione(ascendente_segno, "Ascendente")
            }
        }

        # Debug: Stampa l'output per verifica
        print("Debug - Output calcola_carta_natale:", output)

        return output
    
    except Exception as e:
        raise ValueError(f"Errore nel calcolo della carta natale: {e}")
