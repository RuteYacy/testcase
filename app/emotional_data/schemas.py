from pydantic import BaseModel, Field
from enum import Enum


class PrimaryEmotionEnum(str, Enum):
    anger = "anger"
    anxiety = "anxiety"
    stress = "stress"
    happiness = "happiness"
    calm = "calm"
    neutral = "neutral"
    sadness = "sadness"
    fear = "fear"
    surprise = "surprise"


class EmotionalDataInput(BaseModel):
    primary_emotion: PrimaryEmotionEnum
    intensity: float = Field(..., ge=0, le=1)
    context: str = None
