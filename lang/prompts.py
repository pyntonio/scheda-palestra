def get_prompts(nome, data_nascita, ora_nascita, luogo_nascita, carta_natale, lingua="it", tipi=None):
    """
    Genera più prompt per ciascun tipo di oroscopo richiesto.

    Args:
        nome (str): Nome della persona.
        data_nascita (str): Data di nascita (formato YYYY-MM-DD).
        ora_nascita (str): Ora di nascita (formato HH:MM).
        luogo_nascita (str): Luogo di nascita (formato lat,lon).
        carta_natale (dict): Dati della carta natale.
        lingua (str): Lingua del prompt ('it' o 'en').
        tipi (list): Tipi di oroscopo richiesti (es. ["generico", "mensile"]).

    Returns:
        dict: Un dizionario con i tipi di oroscopo come chiavi e le liste di prompt come valori.
    """
    if tipi is None:
        tipi = "generico"  # Tipo predefinito

    # Se 'tipi' è una stringa, trasformiamolo in una lista con un solo elemento
    if isinstance(tipi, str):
        tipi = [tipi]

    pianeti = ", ".join([f"{pianeta}: {gradi:.2f}°" for pianeta, gradi in carta_natale["pianeti"].items()])
    ascendente = carta_natale["ascendente"]["segno"]
    segno_solare = carta_natale["segno_solare"]["segno"]

    # Dati base del prompt
    prompts = {}
    for tipo in tipi:
        if lingua == "it":
            if tipo == "generico":
                prompts["generico"] = [
                    f"""
                    Genera un oroscopo personalizzato per {nome}, nato il {data_nascita} alle {ora_nascita} a {luogo_nascita}.
                    Il suo segno zodiacale è {segno_solare}, il suo ascendente è {ascendente} e i pianeti nella carta natale sono: {pianeti}.
                    """,
                    f"""
                    Oroscopo per {nome}, nato il {data_nascita} alle {ora_nascita} a {luogo_nascita}.
                    Considerando il suo segno {segno_solare} e l'ascendente {ascendente}, quali sono le tendenze astrologiche generali di questo periodo?
                    """,
                    f"""
                    Per {nome}, nato il {data_nascita} alle {ora_nascita}, con il segno {segno_solare} e l'ascendente {ascendente},
                    genera un oroscopo che esplori le influenze planetarie sulla sua vita, tenendo conto della sua carta natale.
                    """
                ]
            elif tipo == "mensile":
                prompts["mensile"] = [
                    f"""
                    Crea un oroscopo mensile per {nome}, nato il {data_nascita} alle {ora_nascita} a {luogo_nascita}.
                    Il suo segno zodiacale è {segno_solare} e il suo ascendente è {ascendente}.
                    Considera i transiti planetari per il mese corrente e fornisci previsioni su amore, carriera e benessere.
                    """,
                    f"""
                    Per {nome}, nato il {data_nascita}, crea un oroscopo mensile con attenzione ai transiti astrologici.
                    Quali influenze planetarie possono emergere per il segno {segno_solare} e l'ascendente {ascendente}?
                    """,
                    f"""
                    Genera un oroscopo mensile dettagliato per {nome}, considerando la sua carta natale e i transiti planetari. Pianeti: {pianeti}
                    Prevedi come le posizioni planetarie influenzeranno vari aspetti della sua vita durante il mese, come relazioni, lavoro e salute.
                    """
                ]
            else:
                raise ValueError(f"Tipo di oroscopo '{tipo}' non supportato in lingua italiana.")
        
        elif lingua == "en":
            if tipo == "generico":
                prompts["generico"] = [
                    f"""
                    Create a personalized horoscope for {nome}, born on {data_nascita} at {ora_nascita} in {luogo_nascita}.
                    Their zodiac sign is {segno_solare}, their ascendant is {ascendente}, and the planets in the natal chart are: {pianeti}.
                    """,
                    f"""
                    Horoscope for {nome}, born on {data_nascita} at {ora_nascita} in {luogo_nascita}.
                    Considering their {segno_solare} zodiac sign and {ascendente} ascendant, what are the general astrological trends for this period?
                    """,
                    f"""
                    For {nome}, born on {data_nascita} at {ora_nascita}, with the zodiac sign {segno_solare} and ascendant {ascendente},
                    generate a horoscope exploring the planetary influences on their life, considering their natal chart.
                    """
                ]
            elif tipo == "mensile":
                prompts["mensile"] = [
                    f"""
                    Create a monthly horoscope for {nome}, born on {data_nascita} at {ora_nascita} in {luogo_nascita}.
                    Their zodiac sign is {segno_solare} and their ascendant is {ascendente}.
                    Consider the current planetary transits and provide predictions about love, career, and wellness.
                    """,
                    f"""
                    For {nome}, born on {data_nascita}, create a monthly horoscope with attention to astrological transits.
                    What planetary influences might emerge for the {segno_solare} zodiac sign and {ascendente} ascendant?
                    """,
                    f"""
                    Generate a detailed monthly horoscope for {nome}, considering their natal chart and planetary transits. Planets: {pianeti}
                    Predict how the planetary positions will affect various aspects of their life during the month, such as relationships, work, and health.
                    """
                ]
            else:
                raise ValueError(f"Horoscope type '{tipo}' not supported in English.")
        
        else:
            raise ValueError("Lingua non supportata")

    return prompts
