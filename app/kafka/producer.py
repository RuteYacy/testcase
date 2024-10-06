import json
import logging
from aiokafka import AIOKafkaProducer


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

EMOTIONAL_DATA_TOPIC = 'emotional_data_topic'
KAFKA_SERVER = 'kafka:29092'


class KafkaProducer:
    _producer = None

    @classmethod
    async def initialize(cls):
        if cls._producer is None:
            cls._producer = AIOKafkaProducer(bootstrap_servers=KAFKA_SERVER)
            await cls._producer.start()

    @classmethod
    async def produce(cls, topic, value):
        if cls._producer is None:
            await cls.initialize()
        try:
            await cls._producer.send(topic, json.dumps(value).encode())
        except Exception as err:
            logging.error(f"Kafka producer error: {err}")

    @classmethod
    async def close(cls):
        if cls._producer:
            await cls._producer.stop()
            cls._producer = None
