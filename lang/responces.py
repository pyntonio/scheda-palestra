def format_response(oroscopo: str, lingua: str = "it"):
    if lingua == "it":
        return {"messaggio": "Ecco il tuo oroscopo personalizzato!", "oroscopo": oroscopo}
    elif lingua == "en":
        return {"message": "Here is your personalized horoscope!", "horoscope": oroscopo}
    else:
        raise ValueError("Lingua non supportata")
