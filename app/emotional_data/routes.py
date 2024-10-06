from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.emotional_data.models import EmotionalData
from app.emotional_data.schemas import EmotionalDataInput

from app.dependencies import get_current_user
from app.core.database import get_db
from app.users.models import User

router = APIRouter(
    prefix="/emotional-data",
    tags=["emotional-data"],
)


@router.post("/send-data", response_model=dict)
def send_emotional_data(
    emotion_data: EmotionalDataInput,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Submit user's emotional data to be processed and stored.

    Returns:
    - A dictionary confirming data storage.
    """
    new_emotional_data = EmotionalData(
        user_id=current_user.id,
        happiness=emotion_data.happiness,
        stress=emotion_data.stress,
        confidence=emotion_data.confidence,
        anxiety=emotion_data.anxiety,
        sadness=emotion_data.sadness,
        anger=emotion_data.anger,
        excitement=emotion_data.excitement,
        fear=emotion_data.fear,
        thought_data=emotion_data.thought_data,
        timestamp=datetime.now()
    )

    db.add(new_emotional_data)
    db.commit()

    return {
        "message": "Emotional data successfully stored",
        "user_id": current_user.id
    }
