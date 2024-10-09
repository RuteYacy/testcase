from pydantic import BaseModel
from typing import Optional


class EmotionalDataRequest(BaseModel):
    data_id: int
    user_id: int
    primary_emotion: str
    intensity: float
    context: str


class EmotionalDataMessageSchema(BaseModel):
    data_id: int
    user_id: int
    primary_emotion: str
    intensity: float
    context: Optional[str] = None
