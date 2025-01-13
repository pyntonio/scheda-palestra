def get_prompt(nome, data_nascita, ora_nascita, luogo_nascita, carta_natale, lingua="it"):
    pianeti = ", ".join([f"{pianeta}: {gradi:.2f}°" for pianeta, gradi in carta_natale["pianeti"].items()])
    ascendente = carta_natale["ascendente"]

    if lingua == "it":
        return f"""
        Genera un oroscopo personalizzato per {nome}, nato il {data_nascita} alle {ora_nascita} a {luogo_nascita}.
        Il suo ascendente è {ascendente} e i pianeti nella carta natale sono: {pianeti}.
        """
    elif lingua == "en":
        return f"""
        Create a personalized horoscope for {nome}, born on {data_nascita} at {ora_nascita} in {luogo_nascita}.
        Their ascendant is {ascendente} and the planets in the natal chart are: {pianeti}.
        """
    else:
        raise ValueError("Lingua non supportata")
