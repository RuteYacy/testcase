from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from database import Base


class TransactionHistory(Base):
    __tablename__ = "transaction_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    transaction_date = Column(DateTime, index=True)
    transaction_type = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    balance_after_transaction = Column(Float, nullable=True)
    category = Column(String, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "transaction_date": self.transaction_date.isoformat()
            if self.transaction_date else None,
            "transaction_type": self.transaction_type,
            "amount": self.amount,
            "balance_after_transaction": self.balance_after_transaction,
            "category": self.category,
        }
