from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List

from app.users.models import User
from app.users.schemas import UserSchema, UserCreate

from app.core.database import SessionLocal
from app.core.token import create_access_token
from app.core.password import get_password_hash

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/users", response_model=List[UserSchema])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router.post("/signup", response_model=dict)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    user_in_db = db.query(User).filter(User.user_email == user.user_email).first()
    if user_in_db:
        raise HTTPException(status_code=400, detail="User email already registered")

    hashed_password = get_password_hash(user.password)

    new_user = User(
        user_email=user.user_email,
        hashed_password=hashed_password,
    )
    db.add(new_user)
    db.commit()

    db.refresh(new_user)

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": new_user.user_email},
        expires_delta=access_token_expires
    )

    user_response = UserSchema.model_validate(new_user)

    return {"access_token": access_token, "token_type": "bearer",
            "user": user_response,
            }
