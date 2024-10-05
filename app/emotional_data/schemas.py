from pydantic import BaseModel


class EmotionalDataInput(BaseModel):
    happiness: float
    stress: float
    confidence: float = None
    anxiety: float = None
    sadness: float = None
    anger: float = None
    excitement: float = None
    fear: float = None
    thought_data: str = None
