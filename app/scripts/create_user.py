from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from passlib.context import CryptContext
from datetime import datetime

from app.users.models import User

DATABASE_URL = "postgresql://cwtestcaseuser:cwtestcasepwd@db:5432/cwtestcase"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def create_user(email, password):
    """
    Create a new user with the provided email and password, and store it in the database.
    """
    try:
        hashed_password = get_password_hash(password)
        new_user = User(
            email=email,
            password=hashed_password,
            approved_date=datetime.now(),
            credit_limit=5000,
            interest_rate=3.5,
            loan_term=36
        )

        session.add(new_user)
        session.commit()

        print(f"User {email} created successfully with ID: {new_user.id}")
    except SQLAlchemyError as e:
        print(f"Error occurred while creating user: {str(e)}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    email = "newuser@example.com"
    password = "password123"

    create_user(email, password)
