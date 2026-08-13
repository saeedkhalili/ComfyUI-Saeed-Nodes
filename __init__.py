from .cinematic_aspect_ratio import CinematicAspectRatioSelector
from .compact_model_loader import ModelLoaderWithLora
from .cinematic_camera_selector import CameraSelector
from .cinematic_light_selector import LightSelector
from .image_generator import ImageGenerator
from .landscape_prompt_generator import LandscapePromptGenerator
from .negative_prompt_generator import NegativePromptGenerator

NODE_CLASS_MAPPINGS = {
    "CinematicAspectRatioSelector": CinematicAspectRatioSelector,
    "ModelLoaderWithLora": ModelLoaderWithLora,
    "CameraSelector": CameraSelector,
    "LightSelector": LightSelector,
    "ImageGenerator": ImageGenerator,
    "LandscapePromptGenerator": LandscapePromptGenerator,
    "NegativePromptGenerator": NegativePromptGenerator
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CinematicAspectRatioSelector": "Cinematic Aspect Ratio Selector",
    "ModelLoaderWithLora": "Model Loader (Diffusion, CLIP, VAE, LoRA)",
    "CameraSelector": "Camera Selector",
    "LightSelector": "Light Selector",
    "ImageGenerator": "Image Generator",
    "LandscapePromptGenerator": "Landscape Prompt Generator",
    "NegativePromptGenerator": "Negative Prompt Generator"
}