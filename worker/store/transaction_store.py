from sqlalchemy import desc
from database import get_db

from models.transaction_history import TransactionHistory


def get_recent_transactions(user_id):
    db = next(get_db())
    try:
        # Query the transaction history table for the user,
        # sorted by most 30 recent transactions
        transactions = db.query(TransactionHistory).filter(
            TransactionHistory.user_id == user_id
        ).order_by(
            desc(TransactionHistory.created_at)
        ).limit(30).all()

        # Convert each transaction record to a dictionary with relevant details
        transaction_dicts = [
            {
                "created_at": transaction["created_at"],
                "type": transaction["type"],
                "amount": transaction["amount"],
                "balance_after_transaction": transaction["balance_after_transaction"],
                "category": transaction["category"],
            }
            for transaction in (trans.to_dict() for trans in transactions)
        ]

        return transaction_dicts
    finally:
        db.close()
