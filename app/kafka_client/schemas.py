from pydantic import BaseModel
from typing import Optional
from app.emotional_data.schemas import PrimaryEmotionEnum


class EmotionalDataMessageSchema(BaseModel):
    data_id: int
    user_id: int
    primary_emotion: PrimaryEmotionEnum
    intensity: float
    context: Optional[str] = None
