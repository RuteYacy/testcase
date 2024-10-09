import json
from kafka import KafkaConsumer
from config import logger, KAFKA_SERVER, EMOTIONAL_DATA_CLIENT, CREDIT_LIMIT_UPDATE_TOPIC

from store.user_store import update_credit_limit
from store.emotional_data_store import update_data_score
from ml_engine.credit_analysis import get_credit_limit

from kafka_client.producer import KafkaProducerWrapper


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
                try:
                    decoded_message = json.loads(message.value)
                except json.JSONDecodeError as json_err:
                    logger.error(f"JSON decode error: {json_err}")
                    continue

                data_id = decoded_message.get("data_id")
                user_id = decoded_message.get("user_id")
                primary_emotion = decoded_message.get("primary_emotion")
                intensity = decoded_message.get("intensity")
                context = decoded_message.get("context")

                risk_score, final_credit_limit = get_credit_limit(
                    user_id,
                    primary_emotion,
                    intensity,
                    context,
                )

                update_credit_limit(user_id, final_credit_limit)
                update_data_score(data_id, risk_score, final_credit_limit)

                serialized_message = json.dumps({
                    "message": "Worker is done processing"
                })

                KafkaProducerWrapper.produce(
                    topic=CREDIT_LIMIT_UPDATE_TOPIC,
                    value=serialized_message,
                )
        except Exception as e:
            logger.error(f"Exception in consumer loop: {e}")
        finally:
            cls.close()

    @classmethod
    def close(cls):
        if cls._consumer:
            cls._consumer.close()
            cls._consumer = None
