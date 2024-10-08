from sqlalchemy import desc
from database import get_db

from models.transaction_history import TransactionHistory


def get_recent_transactions(user_id):
    db = next(get_db())
    try:
        transactions = db.query(TransactionHistory).filter(
            TransactionHistory.user_id == user_id
        ).order_by(
            desc(TransactionHistory.transaction_date)
        ).limit(30).all()

        transaction_dicts = [
            {
                "transaction_date": transaction["transaction_date"],
                "transaction_type": transaction["transaction_type"],
                "amount": transaction["amount"],
                "balance_after_transaction": transaction["balance_after_transaction"],
                "category": transaction["category"],
            }
            for transaction in (trans.to_dict() for trans in transactions)
        ]

        return transaction_dicts
    finally:
        db.close()
