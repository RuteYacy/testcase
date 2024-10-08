import asyncio
from kafka_consumer.consumer import consume
from database import init_db


def main():
    init_db()
    asyncio.run(consume())


if __name__ == "__main__":
    main()