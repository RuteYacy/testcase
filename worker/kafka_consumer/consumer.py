import json
from config import logger

from kafka.admin import NewTopic
from kafka import KafkaConsumer, KafkaAdminClient

from store.user_store import update_credit_limit
from store.emotional_data_store import update_data_score

from utils.calculate_credit_limit import get_credit_limit

EMOTIONAL_DATA_TOPIC = 'emotional_data_topic'
EMOTIONAL_DATA_CLIENT = 'emotional_data_client'
KAFKA_SERVER = 'kafka:29092'


def ensure_topic_exists():
    admin_client = KafkaAdminClient(bootstrap_servers=KAFKA_SERVER)
    try:
        existing_topics = admin_client.list_topics()

        # Check if the specific topic exists, if not, create it
        if EMOTIONAL_DATA_TOPIC not in existing_topics:
            logger.info(f"Creating topic: {EMOTIONAL_DATA_TOPIC}")
            topic = NewTopic(
                name=EMOTIONAL_DATA_TOPIC,
                num_partitions=1,
                replication_factor=1
            )
            admin_client.create_topics([topic])
            logger.info(f"Topic '{EMOTIONAL_DATA_TOPIC}' created successfully.")
        else:
            logger.error(f"Topic '{EMOTIONAL_DATA_TOPIC}' already exists.")
    except Exception as e:
        logger.error(f"Error creating topic: {e}")
    finally:
        admin_client.close()


async def consume():
    ensure_topic_exists()

    consumer = KafkaConsumer(
        EMOTIONAL_DATA_TOPIC,
        bootstrap_servers=KAFKA_SERVER,
        group_id=EMOTIONAL_DATA_CLIENT,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    try:
        logger.info("Kafka consumer started and waiting for messages...")
        for message in consumer:
            decoded_message = json.loads(message.value)
            logger.info(f"Received message: {decoded_message}")

            data_id = decoded_message.get("data_id")
            user_id = decoded_message.get("user_id")
            primary_emotion = decoded_message.get("primary_emotion")
            intensity = decoded_message.get("intensity")
            context = decoded_message.get("context")

            # Calculate the risk score and final credit limit based on message data
            risk_score, final_credit_limit = get_credit_limit(
                user_id,
                primary_emotion,
                intensity,
                context,
            )
            # Update the user’s credit limit and the data score in the store
            await update_credit_limit(user_id, final_credit_limit)
            await update_data_score(data_id, risk_score, final_credit_limit)
    except Exception as e:
        logger.error(f"Exception in consumer loop: {e}")
    finally:
        consumer.close()
        logger.info('Kafka consumer stopped')
