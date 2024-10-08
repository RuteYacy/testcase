from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import random


DATABASE_URL = "postgresql://cwtestcaseuser:cwtestcasepwd@db:5432/cwtestcase"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

user_id = 1


def create_random_transactions(user_id):
    transaction_types = ['deposit', 'withdrawal', 'transfer', 'payment']
    categories = ['food', 'entertainment', 'groceries', 'rent', 'utilities', 'salary', 'investment', None]

    for _ in range(8):
        transaction_type = random.choice(transaction_types)
        amount = round(random.uniform(10, 1000), 2)
        balance_after_transaction = round(random.uniform(500, 5000), 2)
        category = random.choice(categories)

        transaction_date = datetime.now() - timedelta(days=random.randint(0, 30))

        session.execute(
            text("""
            INSERT INTO transaction_history (user_id, transaction_date, transaction_type, amount, balance_after_transaction, category)
            VALUES (:user_id, :transaction_date, :transaction_type, :amount, :balance_after_transaction, :category)
            """),
            {
                'user_id': user_id,
                'transaction_date': transaction_date,
                'transaction_type': transaction_type,
                'amount': amount,
                'balance_after_transaction': balance_after_transaction,
                'category': category
            }
        )

    session.commit()
    print("Random transactions created successfully.")


if __name__ == "__main__":
    create_random_transactions(user_id)
