import asyncio
import json
import websockets
from typing import Dict, Any, Optional
from datetime import datetime
import logging

class VisionWebSocketClient:
    def __init__(self, uri: str = "ws://localhost:8765"):
        self.uri = uri
        self.config: Dict[str, Any] = {}
        self.connected = False
        self.logger = self._setup_logger()
        
    def _setup_logger(self):
        logger = logging.getLogger('VisionPlus')
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    async def send_message(self, ws, message_type: str, payload: Dict[str, Any]):
        message = {
            "type": message_type,
            "payload": payload,
            "timestamp": datetime.now().isoformat()
        }
        await ws.send(json.dumps(message))
        
    async def handle_message(self, message: str) -> None:
        try:
            data = json.loads(message)
            if data.get("type") == "config":
                await self.handle_config(data.get("payload", {}))
            elif data.get("type") == "inference":
                await self.process_inference(data.get("payload", {}))
            elif data.get("type") == "status":
                await self.handle_status(data.get("payload", {}))
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON message: {e}")
            
    async def handle_config(self, config: Dict[str, Any]) -> None:
        self.config.update(config)
        self.logger.info("Configuration updated")
        
    async def handle_status(self, status: Dict[str, Any]) -> None:
        self.logger.info(f"Status update: {status}")
            
    async def process_inference(self, data: Dict[str, Any]) -> None:
        model_type = data.get("model")
        if model_type in self.config.get("models", {}):
            self.logger.info(f"Processing {model_type} inference request")
            try:
                result = await self.run_inference(data)
                self.logger.info(f"Inference completed: {result}")
            except Exception as e:
                self.logger.error(f"Inference failed: {e}")
            
    async def run_inference(self, data: Dict[str, Any]) -> Dict[str, Any]:
        model_config = self.config["models"]["segmentation"]["config"]
        return {
            "status": "success",
            "model": data.get("model"),
            "device": model_config["device"][0],
            "timestamp": datetime.now().isoformat()
        }
            
    async def connect(self):
        while True:
            try:
                async with websockets.connect(self.uri) as ws:
                    self.connected = True
                    self.logger.info(f"Connected to Vision Plus server at {self.uri}")
                    
                    # Send initial configuration request
                    await self.send_message(ws, "config_request", {})
                    
                    while True:
                        message = await ws.recv()
                        await self.handle_message(message)
                        
            except websockets.exceptions.ConnectionClosedError as e:
                self.connected = False
                self.logger.warning(f"Connection closed: {e}")
            except Exception as e:
                self.connected = False
                self.logger.error(f"Unexpected error: {e}")
            
            self.logger.info("Attempting to reconnect in 5 seconds...")
            await asyncio.sleep(5)

if __name__ == "__main__":
    client = VisionWebSocketClient()
    asyncio.run(client.connect())