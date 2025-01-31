import asyncio
import logging
from vision.core.server import VisionWebSocketServer
from vision.core.models import ModelManager
from vision.core.visualization import VisualizationManager
from vision.core.automation import AutomationManager
from vision.core.api import create_api
from vision.core.preprocessing import PreprocessingManager
from vision.core.monitoring import MonitoringManager
from vision.config import VisionConfig
from vision.database import Database

class VisionPlus:
    def __init__(self, config_path: str = None):
        self.config = VisionConfig(_env_file=config_path if config_path else None)
        self.logger = self._setup_logger()
        self.db = Database(self.config.db_url)
        
        # Initialize monitoring
        self.monitor = MonitoringManager()
        
        # Initialize managers with monitoring
        self.model_manager = ModelManager()
        self.vis_manager = VisualizationManager()
        self.auto_manager = AutomationManager()
        self.preprocess_manager = PreprocessingManager()
        
        # Initialize servers
        self.websocket_server = VisionWebSocketServer(port=self.config.websocket_port)
        self.api = create_api(
            self.model_manager,
            self.vis_manager,
            self.auto_manager,
            self.preprocess_manager
        )

    def _setup_logger(self):
        logger = logging.getLogger('VisionPlus')
        logger.setLevel(self.config.log_level)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    async def start(self):
        self.logger.info(f"Starting Vision Plus system with config: {self.config}")
        
        # Start monitoring
        monitor_task = asyncio.create_task(self.monitor.monitor_system_resources())
        
        # Start all services with performance logging
        start_time = asyncio.get_event_loop().time()
        await asyncio.gather(
            self.websocket_server.start(),
            self.api.start(port=self.config.api_port)
        )
        
        duration = asyncio.get_event_loop().time() - start_time
        await self.monitor.log_performance("System startup", duration)
        
        # Keep monitoring running
        await monitor_task

def run_app(config_path: str = None):
    app = VisionPlus(config_path)
    asyncio.run(app.start())

if __name__ == "__main__":
    run_app()