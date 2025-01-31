from pydantic import BaseSettings
from typing import Dict, Any

class VisionConfig(BaseSettings):
    db_url: str = "sqlite:///vision_plus.db"
    api_port: int = 8000
    websocket_port: int = 8765
    log_level: str = "INFO"
    model_cache_dir: str = "./model_cache"
    
    class Config:
        env_file = ".env"