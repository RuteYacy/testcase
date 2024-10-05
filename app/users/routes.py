from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.users.models import User
from app.users.schemas import User
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/users", response_model=List[User])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users
