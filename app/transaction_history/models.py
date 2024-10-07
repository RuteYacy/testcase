from datetime import datetime
from sqlalchemy import Column, Integer, Float, DateTime, String, ForeignKey

from app.core.database import Base


class TransactionHistory(Base):
    __tablename__ = "transaction_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    transaction_date = Column(DateTime, default=datetime.now, index=True)
    transaction_type = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    balance_after_transaction = Column(Float, nullable=True)
    category = Column(String, nullable=True)
