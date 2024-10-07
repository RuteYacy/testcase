from pydantic import BaseModel


class EmotionalDataInput(BaseModel):
    primary_emotion: str = None
    intensity: float = None
    situation: str = None
