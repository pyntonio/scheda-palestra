from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, TIMESTAMP, DateTime, Boolean, JSON
from sqlalchemy.orm import relationship
from db_config.db_config import Base
from sqlalchemy.sql import func
import datetime

class OroscopoRequest(BaseModel):
    user_id: int  # Aggiungi il campo user_id per l'utente
    nome: str
    data_nascita: str  # Ad esempio, '1990-01-01'
    ora_nascita: str   # Ad esempio, '15:30'
    luogo_nascita: str # Ad esempio, '45.07, 7.68' (latitudine e longitudine)
    lingua: Optional[str] = "it"  # Linguaggio opzionale, di default "it"
    tipi: Optional[str] = "generico"  # Tipo di oroscopo, di default "generico"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=True)  # Nuovo campo
    surname = Column(String(255), nullable=True)  # Nuovo campo
    email = Column(String(255), unique=True, nullable=False)
    born_date = Column(Date, nullable=True)  # Nuovo campo
    born_hour = Column(String(8), nullable=True)  # Nuovo campo (formato HH:MM:SS)
    born_place = Column(String(255), nullable=True)  # Nuovo campo
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.current_timestamp(), nullable=False)
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp(), nullable=False)
    is_verified = Column(Boolean, default=False)
    # Relazione con la carta natale
    natal_cards = relationship("NataleCard", back_populates="user")

class Horoscope(Base):
    __tablename__ = "horoscopes"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    birthdate = Column(Date, nullable=False)
    birthplace = Column(String(255), nullable=False)
    sun_sign = Column(String(50))
    ascendant_sign = Column(String(50))
    moon_sign = Column(String(50))
    generated_text = Column(Text, nullable=False)
    pdf_filename = Column(String(255))
    created_at = Column(TIMESTAMP, default='CURRENT_TIMESTAMP')


# Modello per l'oroscopo generico
class GenericHoroscope(Base):
    __tablename__ = 'generic_horoscopes'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    birth_date = Column(Date)
    birth_place = Column(String)
    horoscope_text = Column(Text)
    pdf_filename = Column(String)



# Modello per la generazione dell'oroscopo
class HoroscopeGeneration(Base):
    __tablename__ = 'horoscope_generations'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    horoscope_type = Column(String)


class MonthlyHoroscope(Base):
    __tablename__ = "monthly_horoscopes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    pdf_filename = Column(String(255), nullable=True)
    generated_at = Column(DateTime, default=datetime.datetime.utcnow)
    birthdate = Column(Date, nullable=False)
    birthplace = Column(String(255), nullable=False)
    sun_sign = Column(String(50), nullable=True)
    ascendant_sign = Column(String(50), nullable=True)
    moon_sign = Column(String(50), nullable=True)
    generated_text = Column(Text, nullable=False)


# Modello per la carta natale
class NataleCard(Base):
    __tablename__ = "natale_card"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    birth_date = Column(Date, nullable=False)
    birth_time = Column(String(8), nullable=False)  # Formato HH:MM
    birth_place = Column(String(255), nullable=False)
    sun_sign = Column(String(50), nullable=True)
    sun_sign_description = Column(Text, nullable=True)
    ascendant = Column(String(50), nullable=True)
    ascendant_description = Column(Text, nullable=True)
    planets = Column(JSON, nullable=True)  # Planet positions stored as JSON
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    user = relationship("User", back_populates="natal_cards")  # Relazione con l'utente