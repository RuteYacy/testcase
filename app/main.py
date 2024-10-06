import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.database import init_db
from app.kafka.consumer import KafkaConsumerHandler

from app.users.routes import router as user_router
from app.emotional_data.routes import router as emotional_data_router

loop = asyncio.get_event_loop()
kafka_consumer = None

app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    consume_kafka()
    yield


def consume_kafka():
    global kafka_consumer
    kafka_consumer = KafkaConsumerHandler(loop)
    asyncio.create_task(kafka_consumer.consume())


app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(emotional_data_router)


@app.get("/")
def read_root():
    return {"message": "Go to http://localhost:8000/docs"}
