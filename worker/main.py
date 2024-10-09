from database import init_db
from kafka_client.client import start_kafka


def main():
    init_db()
    start_kafka()


if __name__ == "__main__":
    main()
