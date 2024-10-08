from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.database import init_db
from app.kafka.client import start_kafka, close_kafka

from app.users.routes import router as user_router
from app.emotional_data.routes import router as emotional_data_router
from app.kafka.routes import router as kafka_router
from app.transaction_history.routes import router as transaction_history_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    await start_kafka()

    try:
        yield
    finally:
        await close_kafka()


app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(emotional_data_router)
app.include_router(kafka_router)
app.include_router(transaction_history_router)


@app.get("/")
def read_root():
    return {"message": "Go to http://localhost:8000/docs"}
