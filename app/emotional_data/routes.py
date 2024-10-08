from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.emotional_data.models import EmotionalData
from app.emotional_data.schemas import EmotionalDataInput

from app.kafka_producer.producer import KafkaProducerWrapper, EMOTIONAL_DATA_TOPIC

from app.dependencies import get_auth_user
from app.core.database import get_db
from app.users.models import User

router = APIRouter(
    prefix="/emotional-data",
    tags=["emotional-data"],
)


@router.post("/send-data", response_model=dict)
async def send_emotional_data(
    emotion_data: EmotionalDataInput,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_auth_user),
):
    """
    Submit user's emotional data to be processed and stored.

    Returns:
    - A dictionary confirming data storage.
    """
    new_emotional_data = EmotionalData(
        user_id=current_user.id,
        timestamp=datetime.now(),
        primary_emotion=emotion_data.primary_emotion,
        intensity=emotion_data.intensity,
        context=emotion_data.context,
    )

    db.add(new_emotional_data)
    db.commit()

    data = {
        "user_id": current_user.id,
        "timestamp": new_emotional_data.timestamp.isoformat(),
        "primary_emotion": emotion_data.primary_emotion,
        "intensity": emotion_data.intensity,
        "context": emotion_data.context,
    }

    try:
        KafkaProducerWrapper.produce(topic=EMOTIONAL_DATA_TOPIC, value={"data": data})
    except Exception as e:
        print(f"Failed to send message to Kafka: {e}")

    return {
        "message": "Emotional data successfully stored and sent to Kafka",
        "user_id": current_user.id
    }
