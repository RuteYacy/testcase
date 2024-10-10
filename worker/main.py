from database import init_db
from kafka_client.client import start_kafka
from ml_engine.train_risk_model import train_model

ml_model = None


def main():
    init_db()

    ml_model = train_model()
    start_kafka(ml_model)


if __name__ == "__main__":
    main()
