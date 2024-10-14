import json
from kafka import KafkaConsumer
from config import logger, KAFKA_SERVER, EMOTIONAL_DATA_CLIENT, CREDIT_LIMIT_UPDATE_TOPIC

from store.user_store import update_credit_limit
from store.credit_limit_store import update_data_score
from store.transaction_store import get_recent_transactions

from ml_engine.predict_risk_score import predict_risk_score
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
    def consume(cls, topic, ml_model):
        cls.initialize(topic)

        try:
            logger.info("Kafka consumer waiting for messages...")
            for message in cls._consumer:
                try:
                    decoded_message = json.loads(message.value)
                except json.JSONDecodeError as json_err:
                    logger.error(f"JSON decode error: {json_err}")
                    continue

                id = decoded_message.get("id")
                user_id = decoded_message.get("user_id")
                primary_emotion = decoded_message.get("primary_emotion")
                intensity = decoded_message.get("intensity")

                risk_score, final_credit_limit = predict_risk_score(
                    primary_emotion,
                    intensity,
                    get_recent_transactions(user_id),
                    ml_model
                )

                update_credit_limit(user_id, final_credit_limit)
                update_data_score(id, risk_score, final_credit_limit)

                serialized_message = json.dumps({
                    "user_id": user_id,
                    "message": "Worker is done processing",
                    "risk_score": risk_score
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
