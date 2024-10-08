import json
from aiokafka import AIOKafkaProducer
from config import logger, KAFKA_SERVER


class KafkaProducer:
    _producer = None

    @classmethod
    async def initialize(cls):
        if cls._producer is None:
            cls._producer = AIOKafkaProducer(
                bootstrap_servers=KAFKA_SERVER,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            await cls._producer.start()
            logger.info("Async Kafka producer started")

    @classmethod
    async def produce(cls, topic, value):
        if cls._producer is None:
            await cls.initialize()
        try:
            await cls._producer.send_and_wait(topic, value=value)
            logger.info(f"Message sent to Kafka topic: {topic}")
        except Exception as err:
            logger.error(f"Kafka producer error: {err}")

    @classmethod
    async def close(cls):
        if cls._producer:
            await cls._producer.stop()
            cls._producer = None
