from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.database import init_db
from app.kafka_producer.producer import KafkaProducerWrapper

from app.users.routes import router as user_router
from app.emotional_data.routes import router as emotional_data_router
from app.transaction_history.routes import router as transaction_history_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    KafkaProducerWrapper.initialize()
    try:
        yield
    finally:
        KafkaProducerWrapper.close()


app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(emotional_data_router)
app.include_router(transaction_history_router)


@app.get("/")
def read_root():
    return {"message": "Go to http://localhost:8000/docs"}
