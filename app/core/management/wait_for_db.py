import time
import os
import psycopg2
from psycopg2 import OperationalError

DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", 5432)
DB_USER = os.getenv("DB_USER", "cwtestcaseuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "cwtestcasepwd")
DB_NAME = os.getenv("DB_NAME", "cwtestcase")


def wait_for_db():
    """
    Wait until PostgreSQL is available to start app.
    """
    connected = False
    while not connected:
        try:
            conn = psycopg2.connect(
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT
            )
            connected = True
            conn.close()
            print("PostgreSQL is ready!")
        except OperationalError:
            print("Waiting for PostgreSQL...")
            time.sleep(2)


if __name__ == "__main__":
    wait_for_db()
