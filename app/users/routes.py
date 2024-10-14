import os
from typing import List

from datetime import timedelta
from sqlalchemy.orm import Session
from email_validator import validate_email, EmailNotValidError
from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.users.models import User
from app.users.crud import create_user
from app.users.services import verify_password
from app.users.schemas import UserSchema, UserSignUp, UserSignIn, UserResponse

from app.sessions.models import Sessions
from app.sessions.crud import create_session
from app.sessions.services import create_access_token

from app.core.database import get_db
from app.core.dependencies import get_auth_user


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


ACCESS_TOKEN_DURATION = os.getenv('ACCESS_TOKEN_DURATION')
REFRESH_TOKEN_DURATION = os.getenv('REFRESH_TOKEN_DURATION')


@router.get("/", response_model=List[UserSchema])
def get_users(db: Session = Depends(get_db)):
    """
    Get a list of all users.

    Returns:
    - A list of users objects.
    """
    try:
        users = db.query(User).all()
        return users
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.post("/signup", response_model=UserResponse)
def signup(user: UserSignUp, request: Request, db: Session = Depends(get_db)):
    """
    Sign up a new user by registering it in the database.

    Returns:
    - A UserResponse object containing access and refresh tokens, and user details.
    """
    try:
        # Validate the email format
        try:
            valid_email = validate_email(user.email)
            user.email = valid_email.email
        except EmailNotValidError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid email address: {str(e)}",
            )

        # Check if a user with the given email already exists
        user_in_db = db.query(User).filter(User.email == user.email).first()
        if user_in_db:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User email already registered",
            )

        new_user = create_user(db, user)
        if not new_user:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user",
            )

        access_token_expires = timedelta(hours=int(ACCESS_TOKEN_DURATION))
        access_token = create_access_token(
            data={"sub": new_user.email},
            expires_delta=access_token_expires
        )

        refresh_token_expires = timedelta(hours=int(REFRESH_TOKEN_DURATION))
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

        return UserResponse(
            user=user_response,
            access_token=access_token,
            refresh_token=refresh_token
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.post("/signin", response_model=UserResponse)
def signin(user: UserSignIn, request: Request, db: Session = Depends(get_db)):
    """
    Sign in an existing user by verifying their email and password.

    Returns:
    - A UserResponse object containing access and refresh tokens, and user details.
    """
    try:
        # Check if a user with the given email exists in the database
        user_in_db = db.query(User).filter(User.email == user.email).first()
        if not user_in_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid email or password",
            )

        if not verify_password(user.password, user_in_db.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        access_token_expires = timedelta(hours=int(ACCESS_TOKEN_DURATION))
        access_token = create_access_token(
            data={"sub": user_in_db.email},
            expires_delta=access_token_expires
        )

        refresh_token_expires = timedelta(hours=int(REFRESH_TOKEN_DURATION))
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

        user_response = UserSchema.model_validate(user_in_db)

        return UserResponse(
            user=user_response,
            access_token=access_token,
            refresh_token=refresh_token
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.post("/signout", status_code=status.HTTP_200_OK)
def signout(
    current_user: User = Depends(get_auth_user),
    db: Session = Depends(get_db)
):
    """
    Sign out the current authenticated user by removing their last session.

    Returns:
    - A success message if the session is successfully removed.
    """
    try:
        # Find the latest session for the authenticated user
        session = db.query(Sessions)\
                    .filter(Sessions.user_id == current_user.id)\
                    .order_by(Sessions.created_at.desc())\
                    .first()

        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found",
            )

        db.delete(session)
        db.commit()

        return {"message": "User successfully signed out"}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/{user_id}", response_model=UserSchema)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """
    Get a user by their ID.

    Returns:
    - A UserSchema object.
    """
    try:
        # Query the database for the user by ID
        user = db.query(User).filter(User.id == user_id).first()

        # If the user is not found, raise a 404 error
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        # Return the user details
        return UserSchema.model_validate(user)

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
