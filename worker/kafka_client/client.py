from config import EMOTIONAL_DATA_TOPIC
from kafka_client.producer import KafkaProducerWrapper
from kafka_client.consumer import KafkaConsumerWrapper


def start_kafka(ml_model):
    KafkaProducerWrapper.initialize()
    KafkaConsumerWrapper.initialize(EMOTIONAL_DATA_TOPIC)
    KafkaConsumerWrapper.consume(EMOTIONAL_DATA_TOPIC, ml_model)


def close_kafka():
    KafkaProducerWrapper.close()
    KafkaConsumerWrapper.close()
