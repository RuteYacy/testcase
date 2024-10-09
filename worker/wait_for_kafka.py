import sys
import asyncio
from aiokafka import AIOKafkaProducer

BOOTSTRAP_SERVERS = 'kafka:29092'


async def wait_for_kafka():
    """
    Wait until Kafka is available to start worker.
    """
    max_attempts = 10
    attempt = 0

    while attempt < max_attempts:
        try:
            producer = AIOKafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)
            await producer.start()
            await producer.send_and_wait("test_topic", b"health_check")
            await producer.stop()
            print("Kafka is ready")
            return
        except Exception as e:
            attempt += 1
            print(f"Kafka not ready, retrying... (attempt {attempt}) - Error: {e}")
            await asyncio.sleep(5)

    print("Kafka did not become ready in time")
    sys.exit(1)


if __name__ == "__main__":
    asyncio.run(wait_for_kafka())
