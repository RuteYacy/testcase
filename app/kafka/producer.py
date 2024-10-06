import json
from kafka import KafkaProducer

from app.kafka.constants import EMOTIONAL_DATA_TOPIC, KAFKA_SERVER


producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


def submit_emotional_data_to_kafka(user_data):
    producer.send(EMOTIONAL_DATA_TOPIC, value=user_data)
    producer.flush()
