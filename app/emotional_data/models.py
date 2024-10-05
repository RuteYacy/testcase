from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Float, DateTime, String, ForeignKey

from app.core.database import Base


class EmotionalData(Base):
    __tablename__ = "emotional_data"

    data_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc), index=True)

    happiness = Column(Float, nullable=False)
    stress = Column(Float, nullable=False)
    confidence = Column(Float, nullable=True)
    anxiety = Column(Float, nullable=True)
    sadness = Column(Float, nullable=True)
    anger = Column(Float, nullable=True)
    excitement = Column(Float, nullable=True)
    fear = Column(Float, nullable=True)

    thought_data = Column(String, nullable=True)
    risk_score = Column(Float, nullable=True)
    credit_limit_calculated = Column(Integer, nullable=True)
