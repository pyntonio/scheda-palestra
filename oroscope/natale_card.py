from skyfield.api import load
from astropy.coordinates import EarthLocation
import astropy.units as u
from datetime import datetime
from astropy.time import Time


# Funzione per convalidare la data
def valida_data(data):
    try:
        # Verifica se la data è nel formato YYYY-MM-DD
        datetime.strptime(data, "%Y-%m-%d")  
        return data
    except ValueError:
        try:
            # Se la data è nel formato dd-mm-yyyy, la converte in yyyy-mm-dd
            return datetime.strptime(data, "%d-%m-%Y").strftime("%Y-%m-%d")
        except ValueError:
            raise ValueError("La data di nascita non è nel formato corretto (YYYY-MM-DD o dd-mm-yyyy).")

def valida_ora(ora):
    try:
        # Verifica se l'ora è un numero (secondi)
        if isinstance(ora, (int, float)):
            ore = int(ora // 3600)  # Ore in formato intero
            minuti = int((ora % 3600) // 60)  # Minuti in formato intero
            
            # Formatta l'ora come stringa nel formato HH:MM
            ora_formattata = f"{ore:02d}:{minuti:02d}"
            
            # Restituisce l'ora nel formato corretto
            return ora_formattata
        else:
            # Se l'ora è già nel formato stringa, la validiamo
            datetime.strptime(ora, "%H:%M")
            return ora
    except ValueError:
        raise ValueError("L'ora di nascita non è nel formato corretto (HH:MM o in secondi).")
    
# Funzione per determinare il segno zodiacale basato sulla data di nascita
def determina_segno_zodiacale(data_nascita):
    segni = [
        ("Ariete", (3, 21), (4, 19)),
        ("Toro", (4, 20), (5, 20)),
        ("Gemelli", (5, 21), (6, 20)),
        ("Cancro", (6, 21), (7, 22)),
        ("Leone", (7, 23), (8, 22)),
        ("Vergine", (8, 23), (9, 22)),
        ("Bilancia", (9, 23), (10, 22)),
        ("Scorpione", (10, 23), (11, 21)),
        ("Sagittario", (11, 22), (12, 21)),
        ("Capricorno", (12, 22), (1, 19)),
        ("Acquario", (1, 20), (2, 18)),
        ("Pesci", (2, 19), (3, 20)),
    ]
    
    try:
        # Convertiamo la data di nascita in datetime
        data = datetime.strptime(data_nascita, "%Y-%m-%d")
        
        # Verifica in quale intervallo di date rientra la data di nascita
        for segno, start, end in segni:
            start_date = datetime(data.year, start[0], start[1])
            end_date = datetime(data.year, end[0], end[1])
            
            # Gestiamo l'anno di Capricorno che va da dicembre a gennaio
            if start_date <= data <= end_date:
                return segno
        
        # Se non trova nessun segno, lancia un errore
        raise ValueError("Non è stato possibile determinare il segno solare.")
    
    except Exception as e:
        raise ValueError(f"Errore nel calcolo del segno solare: {e}")


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
# Funzione per calcolare l'ascendente in base alla posizione del Sole e l'ora di nascita
def calcola_ascendente(sun_pos, location, birth_time):
    ts = load.timescale()
    t = ts.from_astropy(birth_time)
    
    gmst = t.gmst
    long = location.lon.deg
    lst = (gmst + long / 15) % 24
    lst_degrees = lst * 15
    
    ascendente = (lst_degrees + sun_pos.radec()[0]._degrees) % 360
    
    # Mappiamo l'ascendente a un segno zodiacale
    segni = [
        ("Ariete", (0, 30)),
        ("Toro", (30, 60)),
        ("Gemelli", (60, 90)),
        ("Cancro", (90, 120)),
        ("Leone", (120, 150)),
        ("Vergine", (150, 180)),
        ("Bilancia", (180, 210)),
        ("Scorpione", (210, 240)),
        ("Sagittario", (240, 270)),
        ("Capricorno", (270, 300)),
        ("Acquario", (300, 330)),
        ("Pesci", (330, 360)),
    ]
    
    for segno, (start, end) in segni:
        if start <= ascendente < end:
            return segno

    return "Errore"  # Se non trovato, ritorna un errore (non dovrebbe mai accadere)


def calcola_carta_natale(data_nascita: str, ora_nascita: str, luogo_nascita: str):
    try:
        # Validazione della data e dell'ora
        data_nascita = valida_data(data_nascita)
        ora_nascita = valida_ora(ora_nascita)
        
        # Convertire la data e l'ora di nascita in un formato compatibile con Astropy
        birthdate = f"{data_nascita} {ora_nascita}:00"
        birth_time = Time(datetime.strptime(birthdate, "%Y-%m-%d %H:%M:%S"))

        # Latitudine e longitudine del luogo di nascita
        lat, lon = map(float, luogo_nascita.split(","))
        location = EarthLocation(lat=lat * u.deg, lon=lon * u.deg)

        # Carica i dati planetari con Skyfield
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
        
        ts = load.timescale()
        t = ts.utc(birth_time.datetime.year, birth_time.datetime.month,
                   birth_time.datetime.day, birth_time.datetime.hour,
                   birth_time.datetime.minute, birth_time.datetime.second)
        
        # Calcolare la posizione dei pianeti
        sun_pos = sun.at(t)
        moon_pos = moon.at(t)
        mars_pos = mars.at(t)
        venus_pos = venus.at(t)
        mercury_pos = mercury.at(t)
        jupiter_pos = jupiter.at(t)
        saturn_pos = saturn.at(t)
        uranus_pos = uranus.at(t)
        neptune_pos = neptune.at(t)

        # Posizioni planetarie
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
        
        # Calcolare il segno solare
        segno_sol = determina_segno_zodiacale(data_nascita)

        # Verifica il valore di segno_sol prima di utilizzarlo
        if not segno_sol:
            raise ValueError(f"Errore nel calcolo del segno solare: segno_sol è {segno_sol}")
        
        # Generare la descrizione per il segno solare
        descrizione_sol = genera_descrizione(segno_sol, "Sole")

        # Calcolare l'ascendente
        ascendente = calcola_ascendente(sun_pos, location, birth_time)
        
        # Generare la descrizione per l'ascendente
        descrizione_ascendente = genera_descrizione(ascendente, "Ascendente")
        
        # Creare l'output finale
        output = {
            "pianeti": pianeti,
            "segno_solare": {
                "segno": segno_sol,
                "descrizione": descrizione_sol
            },
            "ascendente": {
                "segno": ascendente,
                "descrizione": descrizione_ascendente
            }
        }

        return output
    
    except Exception as e:
        # Aggiungi qui il messaggio di errore per il debug
        return {"error": f"Errore nel calcolo della carta natale: {str(e)}"}
