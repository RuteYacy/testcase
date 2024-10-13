from datetime import datetime
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String

from app.core.database import Base


class CreditLimit(Base):
    __tablename__ = "credit_limit"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now, index=True)

    risk_score = Column(Float, nullable=False)
    credit_limit = Column(Float, nullable=False)

    emotional_data_id = Column(Integer, ForeignKey("emotional_data.id"), nullable=False)
    primary_emotion = Column(String, nullable=False)
