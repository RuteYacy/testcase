import json
from kafka import KafkaConsumer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.emotional_data.models import EmotionalData
from app.kafka.constants import EMOTIONAL_DATA_TOPIC, KAFKA_SERVER


consumer = KafkaConsumer(
    EMOTIONAL_DATA_TOPIC,
    bootstrap_servers=KAFKA_SERVER,
    auto_offset_reset='earliest',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)


def save_emotional_data(db: Session, data: dict):
    emotional_record = EmotionalData(
        user_id=data["user_id"],
        happiness=data["happiness"],
        stress=data["stress"],
        confidence=data.get("confidence"),
        anxiety=data.get("anxiety"),
        sadness=data.get("sadness"),
        anger=data.get("anger"),
        excitement=data.get("excitement"),
        fear=data.get("fear"),
        thought_data=data.get("thought_data"),
        timestamp=data["timestamp"]
    )

    db.add(emotional_record)
    db.commit()


def consume_emotion_data():
    for message in consumer:
        message_data = message.value

        db = next(get_db())

        save_emotional_data(db, message_data)

        print(f"Stored emotional data for user {message_data['user_id']}.")


if __name__ == "__main__":
    consume_emotion_data()
