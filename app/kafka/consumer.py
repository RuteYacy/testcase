import logging

from aiokafka import AIOKafkaConsumer

from app.kafka.constants import KAFKA_SERVER, EMOTIONAL_DATA_TOPIC

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class KafkaConsumer:
    def __init__(self):
        self.consumer = AIOKafkaConsumer(
            EMOTIONAL_DATA_TOPIC,
            bootstrap_servers=KAFKA_SERVER,
            group_id="emotional-data",
            auto_offset_reset="earliest",
        )

    async def start(self):
        try:
            await self.consumer.start()
            print('Kafka consumer started')
        except Exception as e:
            logging.error(f"Error starting consumer: {e}")
            raise e

    async def consume(self):
        print('Starting consumer loop')
        try:
            async for msg in self.consumer:
                decoded_message = msg.value.decode("utf-8")
                print(f"Received message: {decoded_message}")
        except Exception as e:
            logging.error(f"Exception in consumer loop: {e}")
        finally:
            pass

    async def stop(self):
        await self.consumer.stop()
        print('Kafka consumer stopped')
