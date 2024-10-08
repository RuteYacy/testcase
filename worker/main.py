import asyncio
from kafka_client.client import start_kafka, close_kafka
from database import init_db


async def main():
    init_db()

    try:
        await start_kafka()
        while True:
            await asyncio.sleep(1)
    except Exception as e:
        print(f"Error in main: {e}")
    finally:
        await close_kafka()


if __name__ == "__main__":
    asyncio.run(main())
