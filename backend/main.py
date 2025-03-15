from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

app = FastAPI()

class StudyRoomManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

study_room_manager = StudyRoomManager()

@app.websocket("/study-room/{room_id}")
async def study_room_endpoint(websocket: WebSocket, room_id: str):
    await study_room_manager.connect(websocket)
    try:
        while True:
            message = await websocket.receive_text()
            await study_room_manager.broadcast(f"[Room {room_id}] {message}")
    except WebSocketDisconnect:
        study_room_manager.disconnect(websocket)
