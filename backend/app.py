from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os

DATABASE_URL = f"mysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    is_admin = Column(Boolean, default=False)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/users')
def create_user(email: str, password: str, db: Session = Depends(get_db)):
    user = User(email=email, password=password)
    db.add(user)
    db.commit()
    return {'id': user.id, 'email': user.email}

@app.get('/users')
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [{'id': u.id, 'email': u.email} for u in users]

@app.delete('/users/{user_id}')
def delete_user(user_id: int, db: Session = Depends(get_db), admin: bool = True):
    # Add real auth check for admin
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    db.delete(user)
    db.commit()
    return {'status': 'deleted'}