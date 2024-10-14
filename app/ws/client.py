from fastapi import WebSocket, WebSocketDisconnect
import json

# List to store all connected WebSocket clients
connected_clients = []


class WebSocketClient:
    @staticmethod
    async def connect(websocket: WebSocket):
        await websocket.accept()
        connected_clients.append(websocket)

    @staticmethod
    async def disconnect(websocket: WebSocket):
        if websocket in connected_clients:
            connected_clients.remove(websocket)

    @staticmethod
    async def broadcast_message(message):
        print('Received ws message: ', message)
        # Broadcast Kafka message to all WebSocket clients
        for client in connected_clients:
            try:
                await client.send_text(json.dumps(message))
            except Exception as e:
                print(f"Error sending message to WebSocket client: {e}")
                await WebSocketClient.disconnect(client)


# WebSocket endpoint for FastAPI
async def websocket_endpoint(websocket: WebSocket):
    await WebSocketClient.connect(websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await WebSocketClient.disconnect(websocket)
