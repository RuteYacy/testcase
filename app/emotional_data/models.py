from datetime import datetime, timezone
from sqlalchemy import (Column, Integer, Float, DateTime,
                        String, ForeignKey, CheckConstraint)

from app.core.database import Base


class EmotionalData(Base):
    __tablename__ = "emotional_data"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc), index=True)

    primary_emotion = Column(String, nullable=True)
    intensity = Column(Float, nullable=True)
    context = Column(String, nullable=True)

    __table_args__ = (
        CheckConstraint(
            "primary_emotion IN ('anger', 'anxiety', 'stress', 'happiness', " +
            "'calm', 'neutral', 'sadness', 'fear', 'surprise')",
            name="valid_primary_emotion"
        ),
    )
