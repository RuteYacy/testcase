import json
import logging

from kafka.admin import NewTopic
from kafka import KafkaConsumer, KafkaAdminClient

from utils.calculate_credit_limit import get_credit_limit

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

EMOTIONAL_DATA_TOPIC = 'emotional_data_topic'
EMOTIONAL_DATA_CLIENT = 'emotional_data_client'
KAFKA_SERVER = 'kafka:29092'


def ensure_topic_exists():
    admin_client = KafkaAdminClient(bootstrap_servers=KAFKA_SERVER)
    try:
        existing_topics = admin_client.list_topics()

        if EMOTIONAL_DATA_TOPIC not in existing_topics:
            logging.info(f"Creating topic: {EMOTIONAL_DATA_TOPIC}")
            topic = NewTopic(
                name=EMOTIONAL_DATA_TOPIC,
                num_partitions=1,
                replication_factor=1
            )
            admin_client.create_topics([topic])
            logging.info(f"Topic '{EMOTIONAL_DATA_TOPIC}' created successfully.")
        else:
            logging.info(f"Topic '{EMOTIONAL_DATA_TOPIC}' already exists.")
    except Exception as e:
        logging.error(f"Error creating topic: {e}")
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
        logging.info("Kafka consumer started and waiting for messages...")
        for message in consumer:
            decoded_message = message.value
            logging.info(f"Received message: {decoded_message}")

            data = decoded_message.get("data", {})
            user_id = data.get("user_id")
            primary_emotion = data.get("primary_emotion")
            intensity = data.get("intensity")
            context = data.get("context")

            final_credit_limit = get_credit_limit(
                user_id,
                primary_emotion,
                intensity,
                context,
            )
            print(final_credit_limit)
    except Exception as e:
        logging.error(f"Exception in consumer loop: {e}")
    finally:
        consumer.close()
        logging.info('Kafka consumer stopped')
