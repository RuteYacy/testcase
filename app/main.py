from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import init_db
from app.users.routes import router as user_router

app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(user_router)


@app.get("/")
def read_root():
    return {"message": "Go to http://localhost:8000/docs"}
