from fastapi import WebSocket

class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: list[str,WebSocket]= {}
        print("Creating a list to hold active connections",self.active_connections)

    async def connect(self, room_id: str, websocket: WebSocket):
        await websocket.accept()
        if not self.active_connections.get(room_id):
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)
        print("New Active connections are ",self.active_connections)

    async def disconnect(self, room_id: str, websocket: WebSocket):
        self.active_connections[room_id].remove(websocket)
        print("After disconnect active connections are: ",self.active_connections)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
        # print("Sent a personal msg to , ",websocket)

    async def broadcast(self, message: str, room_id: str, websocket: WebSocket):
        for connection in self.active_connections[room_id]:
            if connection != websocket:
                await connection.send_text(message)
                # print("In broadcast: sent msg to ",connection)

manager = ConnectionManager()
