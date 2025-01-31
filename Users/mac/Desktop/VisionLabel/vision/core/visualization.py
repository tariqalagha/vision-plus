import numpy as np
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
import vtk
from vtk.util import numpy_support

class VisualizationManager:
    def __init__(self):
        self.logger = self._setup_logger()
        self.renderers: Dict[str, Any] = {}
        self.current_scene = None
        self.quality_level = "high"

    def _setup_logger(self):
        logger = logging.getLogger('VisionVisualization')
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def setup_renderer(self, scene_name: str, quality: str = "high") -> bool:
        try:
            renderer = vtk.vtkRenderer()
            render_window = vtk.vtkRenderWindow()
            render_window.AddRenderer(renderer)
            
            # Configure rendering quality
            render_window.SetMultiSamples(4 if quality == "high" else 0)
            renderer.SetUseFXAA(True if quality == "high" else False)
            
            self.renderers[scene_name] = {
                "renderer": renderer,
                "window": render_window,
                "actors": [],
                "created_at": datetime.now().isoformat()
            }
            return True
        except Exception as e:
            self.logger.error(f"Failed to setup renderer: {e}")
            return False

    def add_volume(self, scene_name: str, volume_data: np.ndarray) -> bool:
        try:
            if scene_name not in self.renderers:
                self.setup_renderer(scene_name)

            vtk_data = numpy_support.numpy_to_vtk(volume_data.ravel())
            image_data = vtk.vtkImageData()
            image_data.SetDimensions(volume_data.shape)
            image_data.GetPointData().SetScalars(vtk_data)

            volume_mapper = vtk.vtkSmartVolumeMapper()
            volume_mapper.SetInputData(image_data)
            
            volume_property = vtk.vtkVolumeProperty()
            volume_property.ShadeOn()
            volume_property.SetInterpolationTypeToLinear()
            
            volume = vtk.vtkVolume()
            volume.SetMapper(volume_mapper)
            volume.SetProperty(volume_property)
            
            self.renderers[scene_name]["actors"].append(volume)
            self.renderers[scene_name]["renderer"].AddVolume(volume)
            return True
        except Exception as e:
            self.logger.error(f"Failed to add volume: {e}")
            return False

    def update_scene(self, scene_name: str, data: Dict[str, Any]) -> bool:
        try:
            if scene_name not in self.renderers:
                return False
                
            render_window = self.renderers[scene_name]["window"]
            render_window.Render()
            return True
        except Exception as e:
            self.logger.error(f"Failed to update scene: {e}")
            return False

    def get_scene_info(self, scene_name: str) -> Dict[str, Any]:
        if scene_name not in self.renderers:
            return {"status": "not_found"}
            
        return {
            "status": "active",
            "actors_count": len(self.renderers[scene_name]["actors"]),
            "quality": self.quality_level,
            "timestamp": datetime.now().isoformat()
        }

    def list_scenes(self) -> List[str]:
        return list(self.renderers.keys())