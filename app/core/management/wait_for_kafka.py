import sys
import time

from kafka import KafkaAdminClient
from kafka.errors import KafkaError

BOOTSTRAP_SERVERS = 'kafka:29092'


def wait_for_kafka():
    """
    Wait until Kafka is available to start app.
    """
    max_attempts = 10
    attempt = 0
    while attempt < max_attempts:
        try:
            admin_client = KafkaAdminClient(bootstrap_servers=BOOTSTRAP_SERVERS)
            admin_client.list_topics()
            admin_client.close()
            print("Kafka is ready")
            return
        except KafkaError:
            attempt += 1
            print("Kafka not ready, retrying...")
            time.sleep(5)
    print("Kafka did not become ready in time")
    sys.exit(1)


if __name__ == "__main__":
    wait_for_kafka()
