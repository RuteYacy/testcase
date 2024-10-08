from app.config import EMOTIONAL_DATA_TOPIC

from app.kafka_producer.producer import KafkaProducerWrapper
from app.kafka_producer.schemas import EmotionalDataMessageSchema


def produce_emotional_data_message(
    data_id,
    user_id,
    primary_emotion,
    intensity,
    context,
):
    message = EmotionalDataMessageSchema(
        data_id=data_id,
        user_id=user_id,
        primary_emotion=primary_emotion,
        intensity=intensity,
        context=context,
    )

    # Validate and serialize the message
    serialized_message = message.model_dump_json()

    KafkaProducerWrapper.produce(
        topic=EMOTIONAL_DATA_TOPIC,
        value=serialized_message,
    )
