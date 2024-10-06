import json
import logging

from aiokafka import AIOKafkaProducer

from app.kafka.constants import KAFKA_SERVER

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class kafkaProducer:
    async def produce(topic, value):
        try:
            producer = AIOKafkaProducer(bootstrap_servers=KAFKA_SERVER)
            await producer.start()

            try:
                await producer.send_and_wait(topic, json.dumps(value).encode())
            finally:
                await producer.stop()

        except Exception as err:
            logging.log(f"Some Kafka error: {err}")
