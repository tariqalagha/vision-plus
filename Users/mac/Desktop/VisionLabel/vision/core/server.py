import asyncio
import json
import websockets
import logging
from datetime import datetime
from typing import Dict, Set, Any

class VisionWebSocketServer:
    def __init__(self, host: str = "localhost", port: int = 8765):
        self.host = host
        self.port = port
        self.clients: Set[websockets.WebSocketServerProtocol] = set()
        self.config = self._load_default_config()
        self.logger = self._setup_logger()

    def _setup_logger(self):
        logger = logging.getLogger('VisionServer')
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def _load_default_config(self) -> Dict[str, Any]:
        return {
            "models": {
                "segmentation": {
                    "enabled": True,
                    "config": {
                        "device": ["cuda", "cpu", "mps"],
                        "models": {}
                    }
                }
            }
        }

    async def register(self, websocket: websockets.WebSocketServerProtocol):
        self.clients.add(websocket)
        self.logger.info(f"Client connected. Total clients: {len(self.clients)}")

    async def unregister(self, websocket: websockets.WebSocketServerProtocol):
        self.clients.remove(websocket)
        self.logger.info(f"Client disconnected. Total clients: {len(self.clients)}")

    async def send_message(self, websocket: websockets.WebSocketServerProtocol, message_type: str, payload: Dict[str, Any]):
        message = {
            "type": message_type,
            "payload": payload,
            "timestamp": datetime.now().isoformat()
        }
        await websocket.send(json.dumps(message))

    async def handle_message(self, websocket: websockets.WebSocketServerProtocol, message: str):
        try:
            data = json.loads(message)
            if data.get("type") == "config_request":
                await self.send_message(websocket, "config", self.config)
            elif data.get("type") == "inference":
                await self.handle_inference(websocket, data.get("payload", {}))
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON message: {e}")

    async def handle_inference(self, websocket: websockets.WebSocketServerProtocol, data: Dict[str, Any]):
        response = {
            "status": "received",
            "model": data.get("model"),
            "timestamp": datetime.now().isoformat()
        }
        await self.send_message(websocket, "inference_response", response)

    async def handler(self, websocket: websockets.WebSocketServerProtocol, path: str):
        await self.register(websocket)
        try:
            async for message in websocket:
                await self.handle_message(websocket, message)
        finally:
            await self.unregister(websocket)

    async def start(self):
        self.logger.info(f"Starting Vision Plus server on {self.host}:{self.port}")
        async with websockets.serve(self.handler, self.host, self.port):
            await asyncio.Future()  # run forever

def main():
    server = VisionWebSocketServer()
    asyncio.run(server.start())

if __name__ == "__main__":
    main()