from app.config import logger

from fastapi import APIRouter, Depends

from app.users.models import User
from app.core.dependencies import get_auth_user

from app.kafka_producer.schemas import EmotionalDataRequest
from app.kafka_producer.services import produce_emotional_data_message


router = APIRouter(
    prefix="/kafka-producer",
    tags=["kafka-producer"],
)


@router.post("/send-emotiontal-data", response_model=dict)
async def send_emotional_data(
    data: EmotionalDataRequest,
    current_user: User = Depends(get_auth_user),
):
    """
    Receives emotional data as JSON and sends it to Kafka to be processed.
    """
    try:
        produce_emotional_data_message(
            data_id=data.data_id,
            user_id=current_user.id,
            primary_emotion=data.primary_emotion,
            intensity=data.intensity,
            context=data.context,
        )
    except Exception as e:
        logger.error(f"Failed to process emotional data message: {e}")
        return {"message": "Failed to process the data", "error": str(e)}

    return {"message": "Emotional data sent to Kafka successfully"}
