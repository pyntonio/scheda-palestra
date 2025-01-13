from sqlalchemy.orm import Session
from models import User, Horoscope, MonthlyHoroscope
from schemas.schemas import UserCreate, HoroscopeCreate
from fastapi import HTTPException
from schemas import schemas



# User CRUD
def create_user(db: Session, user: dict):
    new_user = User(**user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# Horoscope CRUD
def create_horoscope(db: Session, horoscope: HoroscopeCreate, user_id: int):
    db_horoscope = Horoscope(**horoscope.dict(), user_id=user_id)
    db.add(db_horoscope)
    db.commit()
    db.refresh(db_horoscope)
    return db_horoscope

def get_horoscopes_by_user(db: Session, user_id: int):
    return db.query(Horoscope).filter(Horoscope.user_id == user_id).all()


def get_monthly_horoscopes_for_user(db: Session, user_email: str):
    return db.query(MonthlyHoroscope).join(User).filter(User.email == user_email).all()
