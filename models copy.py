from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Enum, Text, DECIMAL, TIMESTAMP, DateTime, Boolean
from sqlalchemy.orm import relationship
from db_config.db_config import Base
from sqlalchemy.sql import func

class OroscopoRequest(BaseModel):
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
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.current_timestamp(), nullable=False)
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp(), nullable=False)
    is_verified = Column(Boolean, default=False)  # Aggiungi il campo is_verified
    horoscopes = relationship("Horoscope", back_populates="user")


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

    user = relationship("User", back_populates="horoscopes")
    astrological_details = relationship("AstrologicalDetail", back_populates="horoscope")


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

    # Relazione con l'utente
    user = relationship("User", back_populates="horoscopes")
    # Relazione con i dettagli astrologici
    astrological_details = relationship("AstrologicalDetails", back_populates="horoscope")

# Modello per i dettagli astrologici
class AstrologicalDetails(Base):
    __tablename__ = 'astrological_details'

    id = Column(Integer, primary_key=True, index=True)
    horoscope_id = Column(Integer, ForeignKey("generic_horoscopes.id"))
    mercury = Column(String)
    venus = Column(String)
    mars = Column(String)
    jupiter = Column(String)
    saturn = Column(String)
    neptune = Column(String)
    uranus = Column(String)

    # Relazione con l'oroscopo
    horoscope = relationship("GenericHoroscope", back_populates="astrological_details")

# Modello per la generazione dell'oroscopo
class HoroscopeGeneration(Base):
    __tablename__ = 'horoscope_generations'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    horoscope_type = Column(String)

    # Relazione con l'utente
    user = relationship("User")

# Modello per l'oroscopo mensile
class MonthlyHoroscope(Base):
    __tablename__ = 'monthly_horoscopes'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    birth_date = Column(Date)
    birth_place = Column(String)
    horoscope_text = Column(Text)
    pdf_filename = Column(String)
    month = Column(Integer)  # Mese in cui è stato generato l'oroscopo
    year = Column(Integer)   # Anno in cui è stato generato l'oroscopo

    # Relazione con l'utente
    user = relationship("User", back_populates="monthly_horoscopes")
    # Relazione con i dettagli astrologici
    astrological_details = relationship("AstrologicalDetails", back_populates="monthly_horoscope")

# Aggiungere la relazione nel modello User
User.monthly_horoscopes = relationship("MonthlyHoroscope", back_populates="user")
