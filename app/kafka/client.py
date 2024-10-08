import asyncio
from app.config import CREDIT_LIMIT_UPDATE_TOPIC

from app.kafka.producer import KafkaProducer
from app.kafka.consumer import KafkaConsumer


async def start_kafka():
    await KafkaProducer.initialize()
    await KafkaConsumer.initialize(CREDIT_LIMIT_UPDATE_TOPIC)

    asyncio.create_task(KafkaConsumer.consume(CREDIT_LIMIT_UPDATE_TOPIC))


async def close_kafka():
    await KafkaProducer.close()
    await KafkaConsumer.close()
