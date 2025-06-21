# backend/app.py

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os

# --- Configuration de la DB

DATABASE_URL = (
    f"mysql://{os.getenv('DB_USER')}"
    f":{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}"
    f"/{os.getenv('DB_NAME')}"
)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# --- Modèle SQLAlchemy

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    is_admin = Column(Boolean, default=False)

# --- Modèle Pydantic pour la création

class UserCreate(BaseModel):
    email: str
    password: str

# --- Application

app = FastAPI()

# --- Dépendance pour la session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Endpoints

@app.post('/users')
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Vérification d’existence optionnelle
    if db.query(User).filter_by(email=user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {'id': new_user.id, 'email': new_user.email}

@app.get('/users')
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [{'id': u.id, 'email': u.email} for u in users]

@app.delete('/users/{user_id}')
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    db.delete(user)
    db.commit()
    return {'status': 'deleted'}
