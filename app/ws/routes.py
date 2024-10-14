from fastapi import APIRouter
from app.ws.client import websocket_endpoint

router = APIRouter(
    prefix="/ws",
    tags=["ws"],
)


@router.post("/")
async def websocket_endpoint_route(websocket):
    await websocket_endpoint(websocket)
