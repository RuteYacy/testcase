import json
from aiokafka import AIOKafkaConsumer
from app.config import logger, KAFKA_SERVER


class KafkaConsumer:
    _consumer = None

    @classmethod
    async def initialize(cls, topic):
        if cls._consumer is None:
            cls._consumer = AIOKafkaConsumer(
                topic,
                bootstrap_servers=KAFKA_SERVER,
                group_id="credit_notification_service",
                auto_offset_reset="earliest",
                value_deserializer=lambda x: json.loads(x.decode('utf-8'))
            )
            await cls._consumer.start()
            logger.info(f"Async Kafka consumer started for topic: {topic}")

    @classmethod
    async def consume(cls, topic):
        await cls.initialize(topic)

        try:
            logger.info("Kafka consumer waiting for messages...")
            async for message in cls._consumer:
                decoded_message = message.value
                print(decoded_message)
        except Exception as e:
            logger.error(f"Exception in consumer loop: {e}")
        finally:
            await cls.close()

    @classmethod
    async def close(cls):
        if cls._consumer:
            await cls._consumer.stop()
            cls._consumer = None
