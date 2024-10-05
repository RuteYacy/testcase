from fastapi import FastAPI
from app.users import routes as users_routes
from app.core.database import init_db

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


app.include_router(users_routes.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI with PostgreSQL"}
