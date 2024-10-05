from datetime import datetime, timezone
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey

from app.core.database import Base


class Sessions(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    refresh_token = Column(String, nullable=False)
    client_ip = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
