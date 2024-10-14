import json
import asyncio
import threading

from kafka import KafkaConsumer
from app.config import logger, KAFKA_SERVER, CREDIT_LIMIT_UPDATE_TOPIC

from app.ws.client import WebSocketClient


class KafkaConsumerWrapper:
    _consumer = None

    @classmethod
    def initialize(cls, topic):
        if cls._consumer is None:
            cls._consumer = KafkaConsumer(
                topic,
                bootstrap_servers=KAFKA_SERVER,
                group_id="credit_notification_service",
                auto_offset_reset="earliest",
                enable_auto_commit=True,
                value_deserializer=lambda x: json.loads(x.decode('utf-8'))
            )
            logger.info(f"Kafka consumer started for topic: {topic}")

    @classmethod
    async def consume(cls, topic):
        cls.initialize(topic)

        try:
            logger.info("Kafka consumer waiting for messages...")
            for message in cls._consumer:
                print(message)
                decoded_message = message.value
                await WebSocketClient.broadcast_message(decoded_message)
        except Exception as e:
            logger.error(f"Exception in consumer loop: {e}")
        finally:
            cls.close()

    @classmethod
    async def close(cls):
        if cls._consumer:
            cls._consumer.close()
            cls._consumer = None


def start_consumer_thread():
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        logger.info("Kafka consumer thread started")
        loop.run_until_complete(KafkaConsumerWrapper.consume(CREDIT_LIMIT_UPDATE_TOPIC))
    except Exception as e:
        logger.error(f"Error in Kafka consumer thread: {e}")
    finally:
        logger.info("Kafka consumer thread finished")


def run_kafka_in_background():
    consumer_thread = threading.Thread(
        target=start_consumer_thread, daemon=True,
    )
    consumer_thread.start()
