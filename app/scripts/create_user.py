import random
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from passlib.context import CryptContext

from app.users.models import User
from app.transaction_history.models import TransactionHistory
from app.emotional_data.models import EmotionalData
from app.credit_limit.models import CreditLimit

DATABASE_URL = "postgresql://cwtestcaseuser:cwtestcasepwd@db:5432/cwtestcase"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def create_user(email, password):
    """
    Create a new user and store it in the database.
    """
    try:
        hashed_password = get_password_hash(password)
        new_user = User(
            name='John Doe',
            email=email,
            password=hashed_password,
            approved_date=datetime.now(),
        )

        session.add(new_user)
        session.commit()

        print(f"User {email} created successfully with ID: {new_user.id}")
        return new_user.id
    except SQLAlchemyError as e:
        print(f"Error occurred while creating user: {str(e)}")
        session.rollback()


def create_transactions(user_id):
    """
    Create random transactions for a user and return them.
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
        return transactions
    except SQLAlchemyError as e:
        print(f"Error occurred while creating transactions: {str(e)}")
        session.rollback()


def create_emotional_data(user_id):
    """
    Create random emotional data for a user and return them.
    """
    emotions = ['anger', 'anxiety', 'stress', 'happiness', 'calm',
                'neutral', 'sadness', 'fear', 'surprise']

    emotional_data = []

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

            emotional_data.append(new_emotional_data)
            session.add(new_emotional_data)

        session.commit()
        print(f"Emotional data created successfully for user {user_id}.")
        return emotional_data
    except SQLAlchemyError as e:
        print(f"Error occurred while creating emotional data: {str(e)}")
        session.rollback()


def create_credit_limit(user_id, transactions, emotional_data):
    """
    Create rows for the credit_limit table using calculated risk_score and credit_limit.
    """
    try:
        latest_credit_limit = None

        for emotional_record in emotional_data:
            primary_emotion = emotional_record.primary_emotion
            intensity = emotional_record.intensity

            risk_score, final_credit_limit = predict_risk_score(
                primary_emotion,
                intensity,
                transactions
            )

            new_credit_limit = CreditLimit(
                user_id=user_id,
                created_at=datetime.now(),
                risk_score=risk_score,
                credit_limit=final_credit_limit,
                emotional_data_id=emotional_record.id,
                primary_emotion=primary_emotion
            )

            session.add(new_credit_limit)
            latest_credit_limit = final_credit_limit

        session.commit()
        print(f"Credit limits created successfully for user {user_id}.")

        # Update the user's credit limit and balance
        user = session.query(User).filter(User.id == user_id).first()

        if latest_credit_limit is not None:
            user.credit_limit = latest_credit_limit

            # Calculate the user's balance based on the latest transactions
            latest_transaction = transactions[-1]
            user.balance = latest_transaction.balance_after_transaction

            # Set approved_date or denied_date based on the credit limit value
            if latest_credit_limit > 0:
                user.approved_date = datetime.now()
                user.denied_date = None
            else:
                user.denied_date = datetime.now()
                user.approved_date = None

            session.commit()
            print(f"User {user_id} updated with credit limit and balance.")
        else:
            print(f"No valid credit limit calculated for user {user_id}.")

    except SQLAlchemyError as e:
        print(f"Error occurred while creating credit limits: {str(e)}")
        session.rollback()


def predict_risk_score(primary_emotion, intensity, transactions):
    """
    Calculate a mock risk score and credit limit based on basic transaction and emotional data.
    """
    total_income = sum([trans.amount for trans in transactions if trans.amount > 0])
    total_spending = sum([abs(trans.amount) for trans in transactions if trans.amount < 0])

    emotion_map = {
        "anger": 0.7, "anxiety": 0.6, "stress": 0.5,
        "happiness": 0.2, "calm": 0.1, "neutral": 0.3,
        "sadness": 0.6, "fear": 0.7, "surprise": 0.4
    }
    emotion_risk_modifier = emotion_map.get(primary_emotion, 0.3)

    risk_score = intensity * emotion_risk_modifier
    risk_score = max(0, min(risk_score, 1))
    risk_score = round(risk_score, 2)

    base_credit_limit = calculate_base_credit_limit(
        total_income,
        total_spending,
        transactions
    )

    final_credit_limit = base_credit_limit * (1 - risk_score)
    final_credit_limit = round(final_credit_limit, 2)

    return risk_score, final_credit_limit


def calculate_base_credit_limit(total_income, total_spending, transactions):
    base_credit_limit = (total_income / max(len(transactions), 1)) * 3 - (total_spending / max(len(transactions), 1))

    return max(base_credit_limit, 0)


if __name__ == "__main__":
    email = "newuser@example.com"
    password = "password123"

    user_id = create_user(email, password)

    if user_id:
        transactions = create_transactions(user_id)
        emotional_data = create_emotional_data(user_id)
        create_credit_limit(user_id, transactions, emotional_data)
