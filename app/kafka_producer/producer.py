import json
import logging
from kafka import KafkaProducer

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

EMOTIONAL_DATA_TOPIC = 'emotional_data_topic'
EMOTIONAL_DATA_CLIENT = 'emotional_data_client'
KAFKA_SERVER = 'kafka:29092'


class KafkaProducerWrapper:
    _producer = None  # Class-level variable to hold the Kafka producer instance

    @classmethod
    def initialize(cls):
        if cls._producer is None:
            cls._producer = KafkaProducer(
                bootstrap_servers=KAFKA_SERVER,
                # Serialize data to JSON format
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            logging.info("Kafka producer started")

    @classmethod
    def produce(cls, topic, value):
        if cls._producer is None:
            cls.initialize()
        try:
            # Send the message to the specified Kafka topic and flush the producer buffer
            cls._producer.send(topic, value=value)
            cls._producer.flush()
            logging.info("Message sent to Kafka")
        except Exception as err:
            logging.error(f"Kafka producer error: {err}")

    @classmethod
    def close(cls):
        if cls._producer:
            cls._producer.close()
            cls._producer = None
