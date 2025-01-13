import jwt
from fastapi import HTTPException
from datetime import datetime, timedelta

SECRET_KEY = "your_secret_key"  # Cambia con una chiave segreta più sicura
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Tempo di scadenza per i token di conferma email

# Funzione per decodificare il token
def decode_token(token: str):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Funzione per creare un token
def create_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Funzione per creare un token di accesso (es. per conferma email)
def create_confirmation_token(user_id: int, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    data = {"user_id": user_id}
    return create_token(data, expires_delta)

