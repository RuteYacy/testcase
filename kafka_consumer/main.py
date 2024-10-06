import asyncio
import logging

from kafka_consumer.consumer import KafkaConsumer

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

kafka_consumer = KafkaConsumer()


async def main():
    await kafka_consumer.start()
    asyncio.create_task(kafka_consumer.consume())

if __name__ == "__main__":
    asyncio.run(main())
