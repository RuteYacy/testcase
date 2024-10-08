from app.config import logger
from fastapi import HTTPException, status

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.users.models import User
from app.users.schemas import UserSignUp
from app.users.services import get_password_hash


def create_user(db: Session, user: UserSignUp):
    """
    Creates a new user, hashes the password, and adds them to the database.

    Returns:
    - The newly created user object.
    """
    try:
        hashed_password = get_password_hash(user.password)

        db_user = User(
            email=user.email,
            password=hashed_password,
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user

    except SQLAlchemyError as e:
        logger.error(f"Database error occurred while creating a user: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the user in the database."
        )

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the user."
        )
