from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.database import init_db
from app.kafka.producer import KafkaProducer

from app.users.routes import router as user_router
from app.emotional_data.routes import router as emotional_data_router


app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    try:
        await KafkaProducer.initialize()
        yield
    except Exception as e:
        print("Exception during startup")
        raise e
    finally:
        await KafkaProducer.close()


app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(emotional_data_router)


@app.get("/")
def read_root():
    return {"message": "Go to http://localhost:8000/docs"}
