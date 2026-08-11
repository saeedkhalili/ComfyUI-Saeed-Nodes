from .cinematic_aspect_ratio import CinematicAspectRatioSelector
from .compact_model_loader import ModelLoaderWithLora
from .cinematic_camera_selector import CameraSelector
from .cinematic_light_selector import LightSelector
from .image_generator import ImageGenerator          # ← تغییر نام ماژول و کلاس

NODE_CLASS_MAPPINGS = {
    "CinematicAspectRatioSelector": CinematicAspectRatioSelector,
    "ModelLoaderWithLora": ModelLoaderWithLora,
    "CameraSelector": CameraSelector,
    "LightSelector": LightSelector,
    "ImageGenerator": ImageGenerator                  # ← نام کلاس جدید
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CinematicAspectRatioSelector": "Cinematic Aspect Ratio Selector",
    "ModelLoaderWithLora": "Model Loader (Diffusion, CLIP, VAE, LoRA)",
    "CameraSelector": "Camera Selector",
    "LightSelector": "Light Selector",
    "ImageGenerator": "Image Generator"               # ← نام نمایشی
}