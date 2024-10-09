import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Kafka const
KAFKA_SERVER = 'kafka:29092'
EMOTIONAL_DATA_CLIENT = 'emotional_data_client'

CREDIT_LIMIT_UPDATE_TOPIC = 'credit_limit_topic'
EMOTIONAL_DATA_TOPIC = 'emotional_data_topic'
