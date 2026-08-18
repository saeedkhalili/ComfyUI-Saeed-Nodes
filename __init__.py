from .cinematic_aspect_ratio import CinematicAspectRatioSelector
from .compact_model_loader import ModelLoaderWithLora
from .cinematic_camera_selector import CameraSelector
from .camera_movement_selector import CameraMovementSelector
from .cinematic_light_selector import LightSelector
from .image_generator import ImageGenerator
from .landscape_prompt_generator import LandscapePromptGenerator
from .negative_prompt_generator import NegativePromptGenerator
from .image_renamer import ImageRenamer
from .image_date_organizer import ImageDateOrganizer
from .text_preview import TextPreview
from .save_image_custom import SaveImageCustom
from .character_generator import CharacterGenerator
from .action_generator import ActionGenerator
from .scene_element_generator import SceneElementGenerator
from .style_selector import StyleSelector
from .framing_selector import FramingSelector
from .prompt_randomizer import PromptRandomizer

NODE_CLASS_MAPPINGS = {
    "CinematicAspectRatioSelector": CinematicAspectRatioSelector,
    "ModelLoaderWithLora": ModelLoaderWithLora,
    "CameraSelector": CameraSelector,
    "CameraMovementSelector": CameraMovementSelector,
    "LightSelector": LightSelector,
    "ImageGenerator": ImageGenerator,
    "LandscapePromptGenerator": LandscapePromptGenerator,
    "NegativePromptGenerator": NegativePromptGenerator,
    "ImageRenamer": ImageRenamer,
    "ImageDateOrganizer": ImageDateOrganizer,
    "TextPreview": TextPreview,
    "SaveImageCustom": SaveImageCustom,
    "CharacterGenerator": CharacterGenerator,
    "ActionGenerator": ActionGenerator,
    "SceneElementGenerator": SceneElementGenerator,
    "StyleSelector": StyleSelector,
    "FramingSelector": FramingSelector,
    "PromptRandomizer": PromptRandomizer,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CinematicAspectRatioSelector": "Cinematic Aspect Ratio Selector",
    "ModelLoaderWithLora": "Model Loader (Diffusion, CLIP, VAE, LoRA)",
    "CameraSelector": "Camera Selector",
    "CameraMovementSelector": "Camera Movement Selector",
    "LightSelector": "Light Selector",
    "ImageGenerator": "Image Generator",
    "LandscapePromptGenerator": "Landscape Prompt Generator",
    "NegativePromptGenerator": "Negative Prompt Generator",
    "ImageRenamer": "Image Renamer",
    "ImageDateOrganizer": "Image Date Organizer",
    "TextPreview": "Text Preview",
    "SaveImageCustom": "Save Image Custom",
    "CharacterGenerator": "Character Generator",
    "ActionGenerator": "Action Generator",
    "SceneElementGenerator": "Scene Element Generator",
    "StyleSelector": "Style Selector",
    "FramingSelector": "Framing Selector",
    "PromptRandomizer": "Prompt Randomizer",
}

WEB_DIRECTORY = "./web"