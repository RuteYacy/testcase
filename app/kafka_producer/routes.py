from app.config import logger
from fastapi import APIRouter, Depends, HTTPException, status

from app.users.models import User
from app.core.dependencies import get_auth_user

from app.kafka_producer.schemas import EmotionalDataRequest
from app.kafka_producer.services import produce_emotional_data_message


router = APIRouter(
    prefix="/kafka-producer",
    tags=["kafka-producer"],
)


@router.post("/send-emotional-data",
             response_model=dict,
             status_code=status.HTTP_202_ACCEPTED)
async def send_emotional_data(
    data: EmotionalDataRequest,
    current_user: User = Depends(get_auth_user),
):
    """
    Receives emotional data as JSON and sends it to Kafka to be processed.
    """
    if data.user_id != current_user.id:
        logger.warning(
            f"User {current_user.id} attempted to send data for user {data.user_id}",
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to send data for this user.",
        )

    try:
        produce_emotional_data_message(
            data_id=data.data_id,
            user_id=current_user.id,
            primary_emotion=data.primary_emotion,
            intensity=data.intensity,
            context=data.context,
        )
    except ValueError as ve:
        logger.error(f"Validation error when processing emotional data: {ve}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid input data. Please check your request.",
        )
    except ConnectionError as ce:
        logger.error(f"Kafka connection error: {ce}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to connect to Kafka. Please try again later.",
        )
    except Exception as e:
        logger.error(f"Failed to process emotional data message: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while processing the data.",
        )

    return {"message": "Emotional data sent to Kafka successfully"}
