from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from passlib.context import CryptContext
from datetime import datetime, timezone
import random

from app.users.models import User
from app.transaction_history.models import TransactionHistory
from app.emotional_data.models import EmotionalData

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
        return new_user.id
    except SQLAlchemyError as e:
        print(f"Error occurred while creating user: {str(e)}")
        session.rollback()
    finally:
        session.close()


def create_transactions(user_id):
    """
    Create random transactions for a user and store them in the database.
    """
    transaction_types = ['credit', 'debit']
    categories = ['home', 'other', 'transactions', 'food', 'education', 'personal',
                  'communication', 'entertainment', 'health', 'transport', 'tax']

    transactions = []

    try:
        for _ in range(16):
            transaction_type = random.choice(transaction_types)
            category = random.choice(categories)
            amount = round(random.uniform(-500, 500), 2)
            balance_after_transaction = round(random.uniform(0, 5000), 2)

            new_transaction = TransactionHistory(
                user_id=user_id,
                transaction_type=transaction_type,
                amount=amount,
                balance_after_transaction=balance_after_transaction,
                category=category
            )
            transactions.append(new_transaction)
            session.add(new_transaction)

        session.commit()
        print(f"Transactions created successfully for user {user_id}.")
    except SQLAlchemyError as e:
        print(f"Error occurred while creating transactions: {str(e)}")
        session.rollback()
    finally:
        session.close()


def create_emotional_data(user_id):
    """
    Create random emotional data for a user and store it in the database.
    """
    emotions = ['anger', 'anxiety', 'stress', 'happiness', 'calm',
                'neutral', 'sadness', 'fear', 'surprise']

    try:
        for _ in range(16):
            primary_emotion = random.choice(emotions)
            intensity = round(random.uniform(0.1, 1.0), 2)
            context = f"Sample context for emotion {primary_emotion}"

            new_emotional_data = EmotionalData(
                user_id=user_id,
                primary_emotion=primary_emotion,
                intensity=intensity,
                context=context
            )

            session.add(new_emotional_data)

        session.commit()
        print(f"Emotional data created successfully for user {user_id}.")
    except SQLAlchemyError as e:
        print(f"Error occurred while creating emotional data: {str(e)}")
        session.rollback()
    finally:
        session.close()


if __name__ == "__main__":
    email = "newuser@example.com"
    password = "password123"

    user_id = create_user(email, password)

    if user_id:
        create_transactions(user_id)
        create_emotional_data(user_id)
