import logging
from aiokafka import AIOKafkaConsumer

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

EMOTIONAL_DATA_TOPIC = 'emotional_data_topic'
KAFKA_SERVER = 'kafka:29092'


async def consume():
    consumer = AIOKafkaConsumer(
        EMOTIONAL_DATA_TOPIC,
        bootstrap_servers=KAFKA_SERVER,
        group_id="emotional-data",
        enable_auto_commit=False,
        auto_offset_reset="earliest",
    )
    await consumer.start()
    try:
        async for msg in consumer:
            decoded_message = msg.value.decode("utf-8")
            print(f"Received message: {decoded_message}")
    except Exception as e:
        logging.error(f"Exception in consumer loop: {e}")
    finally:
        await consumer.stop()
        print('Kafka consumer stopped')
