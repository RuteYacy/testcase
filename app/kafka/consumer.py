import json
import logging
from kafka import KafkaConsumer
from app.kafka.constants import EMOTIONAL_DATA_TOPIC, KAFKA_SERVER

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class KafkaConsumerHandler:
    def __init__(self, loop):
        self.loop = loop
        self.consumer = KafkaConsumer(
            EMOTIONAL_DATA_TOPIC,
            bootstrap_servers=KAFKA_SERVER,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )

    async def consume(self):
        print("Starting Kafka Consumer...")
        try:
            await self.consumer.start()

        except Exception as e:
            logging.info(str(e))
            return

        try:
            async for msg in self.consumer:
                msg.value.decode("utf-8")
        finally:
            await self.consumer.stop()
