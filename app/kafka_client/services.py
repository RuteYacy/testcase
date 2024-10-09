import json
from fastapi import HTTPException, status
from app.config import logger, EMOTIONAL_DATA_TOPIC

from app.kafka_client.producer import KafkaProducerWrapper
from app.kafka_client.schemas import EmotionalDataMessageSchema


def produce_emotional_data_message(
    data_id,
    user_id,
    primary_emotion,
    intensity,
    context,
):
    try:
        message = EmotionalDataMessageSchema(
            data_id=data_id,
            user_id=user_id,
            primary_emotion=primary_emotion,
            intensity=intensity,
            context=context,
        )

        serialized_message = message.model_dump_json()

        KafkaProducerWrapper.produce(
            topic=EMOTIONAL_DATA_TOPIC,
            value=serialized_message,
        )
        logger.info(
            f"Message sent to topic {EMOTIONAL_DATA_TOPIC}: {serialized_message}",
        )

    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid data provided: {ve}"
        )
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error in serializing message to JSON"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while producing the message"
        )
