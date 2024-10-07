import sys
import asyncio

from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaError

BOOTSTRAP_SERVERS = 'kafka:29092'


async def wait_for_kafka():
    producer = AIOKafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)
    max_attempts = 10
    attempt = 0
    while attempt < max_attempts:
        try:
            await producer.start()
            await producer.stop()
            print("Kafka is ready")
            return
        except KafkaError:
            attempt += 1
            print("Kafka not ready, retrying ...")
            await asyncio.sleep(5)
    print("Kafka did not become ready in time")
    sys.exit(1)

if __name__ == "__main__":
    asyncio.run(wait_for_kafka())
