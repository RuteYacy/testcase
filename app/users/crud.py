from sqlalchemy.orm import Session

from app.users.schemas import UserSignUp
from app.users.models import User

from app.core.password import get_password_hash


def create_user(db: Session, user: UserSignUp):
    """
    Creates a new user, hashes the password, and adds them to the database.

    Returns:
    - The newly created user object.
    """
    hashed_password = get_password_hash(user.password)

    db_user = User(
        user_email=user.user_email,
        password=hashed_password,
    )

    db.add(db_user)
    db.commit()

    db.refresh(db_user)

    return db_user
