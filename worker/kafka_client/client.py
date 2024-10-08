from config import EMOTIONAL_DATA_TOPIC
from kafka_client.producer import KafkaProducerWrapper
from kafka_client.consumer import KafkaConsumerWrapper


def start_kafka():
    KafkaProducerWrapper.initialize()
    KafkaConsumerWrapper.initialize(EMOTIONAL_DATA_TOPIC)
    KafkaConsumerWrapper.consume(EMOTIONAL_DATA_TOPIC)


def close_kafka():
    KafkaProducerWrapper.close()
    KafkaConsumerWrapper.close()
