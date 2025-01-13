from skyfield.api import load
from astropy.coordinates import EarthLocation
import astropy.units as u
from astropy.time import Time

def calcola_carta_natale(data_nascita: str, ora_nascita: str, luogo_nascita: str):
    # Convertire la data e l'ora di nascita in un formato compatibile con Astropy
    birthdate = f"{data_nascita} {ora_nascita}:00"
    birth_time = Time(birthdate, format='iso')

    # Latitudine e longitudine del luogo di nascita
    lat, lon = map(float, luogo_nascita.split(","))
    location = EarthLocation(lat=lat * u.deg, lon=lon * u.deg)

    # Carica i dati planetari con Skyfield (DE421 ephemeris)
    planets = load('de421.bsp')
    earth = planets['earth']
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
        "Sole": sun_pos.radec()[0]._degrees,  # Usa _degrees per ottenere in gradi
        "Luna": moon_pos.radec()[0]._degrees,  # Usa _degrees per ottenere in gradi
        "Mercurio": mercury_pos.radec()[0]._degrees,  # Usa _degrees per ottenere in gradi
        "Venere": venus_pos.radec()[0]._degrees,  # Usa _degrees per ottenere in gradi
        "Marte": mars_pos.radec()[0]._degrees,  # Usa _degrees per ottenere in gradi
        "Giove": jupiter_pos.radec()[0]._degrees,  # Usa _degrees per ottenere in gradi
        "Saturno": saturn_pos.radec()[0]._degrees,  # Usa _degrees per ottenere in gradi
        "Urano": uranus_pos.radec()[0]._degrees,  # Usa _degrees per ottenere in gradi
        "Nettuno": neptune_pos.radec()[0]._degrees  # Usa _degrees per ottenere in gradi
    }

    # Calcolare l'ascendente (approssimazione basata sul Sole)
    # RA del Sole è ottenuto dalla radec() e convertito in gradi
    ascendente = (sun_pos.radec()[0]._degrees + 180) % 360  # Usa _degrees per ottenere in gradi

    print(f"Debug - Posizioni planetarie per {ascendente}:")
    for pianeta, posizione in pianeti.items():
        print(f"{pianeta}: {posizione:.2f}°")

    return {"pianeti": pianeti, "ascendente": ascendente}
