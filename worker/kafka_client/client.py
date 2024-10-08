import asyncio
from kafka_client.producer import KafkaProducer
from kafka_client.consumer import KafkaConsumer
from config import EMOTIONAL_DATA_TOPIC


async def start_kafka():
    await KafkaProducer.initialize()
    await KafkaConsumer.initialize(EMOTIONAL_DATA_TOPIC)

    asyncio.create_task(KafkaConsumer.consume(EMOTIONAL_DATA_TOPIC))


async def close_kafka():
    await KafkaProducer.close()
    await KafkaConsumer.close()
