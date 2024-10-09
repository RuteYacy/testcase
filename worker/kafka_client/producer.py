import json
from kafka import KafkaProducer
from config import logger, KAFKA_SERVER


class KafkaProducerWrapper:
    _producer = None

    @classmethod
    def initialize(cls):
        if cls._producer is None:
            cls._producer = KafkaProducer(
                bootstrap_servers=[KAFKA_SERVER],
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            logger.info("Kafka producer started")

    @classmethod
    def produce(cls, topic, value):
        if cls._producer is None:
            cls.initialize()
        try:
            cls._producer.send(topic, value=value)
            cls._producer.flush()
            logger.info(f"Message sent to Kafka topic: {topic}")
        except Exception as err:
            logger.error(f"Kafka producer error: {err}")

    @classmethod
    def close(cls):
        if cls._producer:
            cls._producer.close()
            cls._producer = None
