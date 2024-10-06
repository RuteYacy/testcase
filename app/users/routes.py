import os
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List

from app.sessions.crud import create_session

from app.users.models import User
from app.users.schemas import UserSchema, UserSignUp, UserSignIn
from app.users.crud import create_user

from app.core.database import get_db
from app.sessions.service import create_access_token
from app.users.service import verify_password

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/users", response_model=List[UserSchema])
def get_users(db: Session = Depends(get_db)):
    """
    Get a list of all users.

    Returns:
    - A list of users objects.
    """
    users = db.query(User).all()
    return users


@router.post("/signup", response_model=dict)
def signup(user: UserSignUp, request: Request, db: Session = Depends(get_db)):
    """
    Sign up a new user by registering it in the database.

    Returns:
    - A dictionary containing access and refresh tokens, and user details.
    """
    # Check if a user with the given email already exists
    user_in_db = db.query(User).filter(User.email == user.email).first()
    if user_in_db:
        raise HTTPException(status_code=400, detail="User email already registered")

    new_user = create_user(db, user)
    if not new_user:
        raise HTTPException(status_code=500, detail="Failed to create user")

    access_token_expires = timedelta(hours=int(os.getenv('ACCESS_TOKEN_DURATION')))
    access_token = create_access_token(
        data={"sub": new_user.email},
        expires_delta=access_token_expires
    )

    refresh_token_expires = timedelta(hours=int(os.getenv('REFRESH_TOKEN_DURATION')))
    refresh_token = create_access_token(
        data={"sub": new_user.email},
        expires_delta=refresh_token_expires
    )

    create_session(
        db=db,
        user_id=new_user.id,
        refresh_token=refresh_token,
        client_ip=request.client.host,
        refresh_token_expires=refresh_token_expires
    )

    user_response = UserSchema.model_validate(new_user)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": user_response,
    }


@router.post("/signin", response_model=dict)
def signin(user: UserSignIn, request: Request, db: Session = Depends(get_db)):
    """
    Sign in an existing user by verifying their email and password.

    Returns:
    - A dictionary containing access and refresh tokens.
    """
    # Check if a user with the given email exists in the database
    user_in_db = db.query(User).filter(User.email == user.email).first()
    if not user_in_db:
        raise HTTPException(status_code=404, detail="Invalid email or password")

    if not verify_password(user.password, user_in_db.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token_expires = timedelta(hours=int(os.getenv('ACCESS_TOKEN_DURATION')))
    access_token = create_access_token(
        data={"sub": user_in_db.email},
        expires_delta=access_token_expires
    )

    refresh_token_expires = timedelta(hours=int(os.getenv('REFRESH_TOKEN_DURATION')))
    refresh_token = create_access_token(
        data={"sub": user_in_db.email},
        expires_delta=refresh_token_expires
    )

    create_session(
        db=db,
        user_id=user_in_db.id,
        refresh_token=refresh_token,
        client_ip=request.client.host,
        refresh_token_expires=refresh_token_expires
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }
