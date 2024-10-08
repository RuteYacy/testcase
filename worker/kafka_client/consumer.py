import json
from kafka import KafkaConsumer
from config import logger, KAFKA_SERVER, EMOTIONAL_DATA_CLIENT


class KafkaConsumerWrapper:
    _consumer = None

    @classmethod
    def initialize(cls, topic):
        if cls._consumer is None:
            cls._consumer = KafkaConsumer(
                topic,
                bootstrap_servers=[KAFKA_SERVER],
                group_id=EMOTIONAL_DATA_CLIENT,
                auto_offset_reset="earliest",
                value_deserializer=lambda x: json.loads(x.decode('utf-8'))
            )
            logger.info(f"Kafka consumer started for topic: {topic}")

    @classmethod
    def consume(cls, topic):
        cls.initialize(topic)

        try:
            logger.info("Kafka consumer waiting for messages...")
            for message in cls._consumer:
                decoded_message = message.value
                print(decoded_message)
        except Exception as e:
            logger.error(f"Exception in consumer loop: {e}")
        finally:
            cls.close()

    @classmethod
    def close(cls):
        if cls._consumer:
            cls._consumer.close()
            cls._consumer = None
