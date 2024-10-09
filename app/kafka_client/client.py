import asyncio
from app.config import CREDIT_LIMIT_UPDATE_TOPIC

from app.kafka_client.producer import KafkaProducerWrapper
from app.kafka_client.consumer import KafkaConsumerWrapper


async def start_kafka():
    await KafkaProducerWrapper.initialize()
    await KafkaConsumerWrapper.initialize(CREDIT_LIMIT_UPDATE_TOPIC)

    asyncio.create_task(KafkaConsumerWrapper.consume(CREDIT_LIMIT_UPDATE_TOPIC))


async def close_kafka():
    await KafkaProducerWrapper.close()
    await KafkaConsumerWrapper.close()
