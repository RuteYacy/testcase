from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class EmotionalDataMessageSchema(BaseModel):
    data_id: int
    user_id: int
    timestamp: datetime
    primary_emotion: str
    intensity: float
    context: Optional[str] = None
