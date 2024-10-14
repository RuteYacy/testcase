from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from database import Base


class TransactionHistory(Base):
    __tablename__ = "transaction_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, index=True)
    type = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    balance_after_transaction = Column(Float, nullable=True)
    category = Column(String, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat()
            if self.created_at else None,
            "type": self.type,
            "amount": self.amount,
            "balance_after_transaction": self.balance_after_transaction,
            "category": self.category,
        }
