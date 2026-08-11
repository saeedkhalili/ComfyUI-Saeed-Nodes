import os
import folder_paths
import comfy.sd
import comfy.utils
from nodes import LoraLoader

# CLIP type list from ComfyUI enum
try:
    _clip_type_enum = comfy.sd.CLIPType
    CLIP_TYPES = [e.name.lower() for e in _clip_type_enum]
    if "stable_diffusion" not in CLIP_TYPES:
        CLIP_TYPES.insert(0, "stable_diffusion")
except Exception:
    CLIP_TYPES = ["stable_diffusion", "stable_cascade", "sd3", "stable_audio",
                  "mochi", "ltxv", "pixart", "cosmos", "lumina2", "wan",
                  "hidream", "chroma", "ace", "omnigen2", "qwen_image",
                  "hunyuan_image", "flux2", "ovis", "longcat_image",
                  "cogvideox", "lens", "pixeldit", "ideogram4"]


class ModelLoaderWithLora:
    """
    Loads Diffusion Model, CLIP (with type), VAE, and up to 5 LoRAs with strength and trigger words.
    Outputs: MODEL, CLIP, VAE, trigger_words (comma-separated).
    """
    @classmethod
    def INPUT_TYPES(cls):
        diffusion_models = folder_paths.get_filename_list("diffusion_models")
        clip_models = folder_paths.get_filename_list("text_encoders")
        vae_models = folder_paths.get_filename_list("vae")
        lora_models = ["none"] + folder_paths.get_filename_list("loras")

        inputs = {
            "required": {
                "diffusion_model": (diffusion_models, {"default": "Qwen\\qwen_image_2512_fp8_e4m3fn.safetensors"}),
                "clip_model": (clip_models, {"default": "Qwen\\qwen_2.5_vl_7b_fp8_scaled.safetensors"}),
                "clip_type": (CLIP_TYPES, {"default": "qwen_image"}),
                "vae_model": (vae_models, {"default": "qwen_image_vae.safetensors"}),
            }
        }

        # LoRA slots 1-5
        inputs["required"].update({
            "lora_1_model": (lora_models, {"default": "Qwen\\Qwen-Image-2512-Lightning-8steps-V1.0-fp32.safetensors"}),
            "lora_1_strength": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
            "lora_1_trigger_word": ("STRING", {"default": "", "multiline": False}),
        })
        inputs["required"].update({
            "lora_2_model": (lora_models, {"default": "Qwen\\aldniki_qwen_reality_transform_v01.safetensors"}),
            "lora_2_strength": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
            "lora_2_trigger_word": ("STRING", {"default": "transform into realistic photography", "multiline": False}),
        })
        for i in range(3, 6):
            inputs["required"].update({
                f"lora_{i}_model": (lora_models, {"default": "none"}),
                f"lora_{i}_strength": ("FLOAT", {"default": 0.0 if i < 5 else 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                f"lora_{i}_trigger_word": ("STRING", {"default": "", "multiline": False}),
            })

        return inputs

    RETURN_TYPES = ("MODEL", "CLIP", "VAE", "STRING")
    RETURN_NAMES = ("MODEL", "CLIP", "VAE", "trigger_words")
    FUNCTION = "load_models"
    CATEGORY = "Saeed"

    def load_models(self, diffusion_model, clip_model, clip_type, vae_model, **lora_kwargs):
        # 1. Load Diffusion Model
        if not diffusion_model:
            raise ValueError("Diffusion model not selected.")
        unet_path = folder_paths.get_full_path("diffusion_models", diffusion_model)
        model = comfy.sd.load_diffusion_model(unet_path)

        # 2. Load CLIP
        clip_path = folder_paths.get_full_path("text_encoders", clip_model)
        clip = comfy.sd.load_clip(
            ckpt_paths=[clip_path],
            embedding_directory=folder_paths.get_folder_paths("embeddings"),
            clip_type=clip_type
        )

        # 3. Load VAE
        vae_path = folder_paths.get_full_path("vae", vae_model)
        vae_sd = comfy.utils.load_torch_file(vae_path)
        vae = comfy.sd.VAE(sd=vae_sd)

        # 4. Apply LoRAs using standard LoraLoader
        trigger_words = []
        lora_loader = LoraLoader()
        for i in range(1, 6):
            lora_name = lora_kwargs.get(f"lora_{i}_model", "none")
            if lora_name == "none":
                continue
            strength = lora_kwargs.get(f"lora_{i}_strength", 1.0)
            trigger_word = lora_kwargs.get(f"lora_{i}_trigger_word", "").strip()

            model, clip = lora_loader.load_lora(model, clip, lora_name, strength, strength)

            if trigger_word:
                trigger_words.append(trigger_word)

        # 5. Build trigger words string
        final_trigger = ", ".join(trigger_words)
        return (model, clip, vae, final_trigger)