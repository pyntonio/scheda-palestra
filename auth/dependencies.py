from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from auth.auth_utils import decode_access_token  # Importa la funzione dal file auth_utils.py

# Configura il sistema di autenticazione OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Dipendenza per verificare il token JWT e restituire l'email dell'utente autenticato.
    """
    email = decode_access_token(token)
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return email
