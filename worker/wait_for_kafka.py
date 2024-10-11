import time
from kafka import KafkaAdminClient
from kafka.errors import NoBrokersAvailable

KAFKA_HOST = 'kafka:29092'


def wait_for_kafka():
    """
    Wait until Kafka is available to start worker.
    """
    connected = False
    while not connected:
        try:
            admin_client = KafkaAdminClient(
                bootstrap_servers=KAFKA_HOST
            )
            connected = True
            admin_client.close()
            print("Kafka is ready!")
        except NoBrokersAvailable:
            print("Waiting for Kafka...")
            time.sleep(2)


if __name__ == "__main__":
    wait_for_kafka()
