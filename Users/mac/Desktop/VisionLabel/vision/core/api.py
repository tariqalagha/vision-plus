from fastapi import FastAPI, HTTPException
from typing import Dict, Any, List
import logging
from datetime import datetime
import uvicorn
from pydantic import BaseModel

class WorkflowRequest(BaseModel):
    name: str
    steps: List[Dict[str, Any]]

class InferenceRequest(BaseModel):
    model_name: str
    data: Dict[str, Any]

class VisionAPI:
    def __init__(self, model_manager, visualization_manager, automation_manager):
        self.app = FastAPI(title="Vision Plus API")
        self.logger = self._setup_logger()
        self.model_manager = model_manager
        self.vis_manager = visualization_manager
        self.auto_manager = automation_manager
        self._setup_routes()

    def _setup_logger(self):
        logger = logging.getLogger('VisionAPI')
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def _setup_routes(self):
        @self.app.post("/workflow/create")
        async def create_workflow(request: WorkflowRequest):
            try:
                workflow_id = await self.auto_manager.create_workflow(
                    request.name, request.steps
                )
                return {"workflow_id": workflow_id, "status": "created"}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/inference/{model_name}")
        async def run_inference(model_name: str, request: InferenceRequest):
            try:
                result = await self.model_manager.run_inference(
                    model_name, request.data
                )
                if result is None:
                    raise HTTPException(status_code=404, detail="Model not found")
                return result
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/visualization/scenes")
        async def list_scenes():
            return {"scenes": self.vis_manager.list_scenes()}

        @self.app.get("/models/status")
        async def get_models_status():
            return self.model_manager.list_models()

        @self.app.get("/workflow/{workflow_id}/status")
        async def get_workflow_status(workflow_id: str):
            status = self.auto_manager.get_workflow_status(workflow_id)
            if status["status"] == "not_found":
                raise HTTPException(status_code=404, detail="Workflow not found")
            return status

    async def start(self, host: str = "0.0.0.0", port: int = 8000):
        self.logger.info(f"Starting Vision Plus API on {host}:{port}")
        config = uvicorn.Config(self.app, host=host, port=port)
        server = uvicorn.Server(config)
        await server.serve()

def create_api(model_manager, visualization_manager, automation_manager):
    return VisionAPI(model_manager, visualization_manager, automation_manager)