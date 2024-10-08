from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Float, DateTime, String, ForeignKey

from app.core.database import Base


class EmotionalData(Base):
    __tablename__ = "emotional_data"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc), index=True)

    primary_emotion = Column(String, nullable=True)
    intensity = Column(Float, nullable=True)
    context = Column(String, nullable=True)

    processed_score = Column(Float, nullable=True)
