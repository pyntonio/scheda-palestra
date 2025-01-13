from pydantic import BaseModel, EmailStr
from typing import Optional

# User Schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(BaseModel):
    username: str
    email: str
    password: str  # Accept plain text password for input

class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True

# Horoscope Schemas
class HoroscopeBase(BaseModel):
    birthdate: str
    birthplace: str
    sun_sign: Optional[str]
    ascendant_sign: Optional[str]
    moon_sign: Optional[str]
    generated_text: str
    pdf_filename: Optional[str]

class HoroscopeCreate(HoroscopeBase):
    pass

class HoroscopeOut(HoroscopeBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
        
# Crea un modello Pydantic per la richiesta del cambio password
class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str