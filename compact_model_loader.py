import os
import folder_paths
import comfy.sd
import comfy.utils
from nodes import LoraLoader, CLIPLoader

try:
    # دریافت لیست نوع‌های CLIP دقیقاً از نود استاندارد Load CLIP
    _clip_types_info = CLIPLoader.INPUT_TYPES()["required"]["type"]
    if isinstance(_clip_types_info, tuple):
        CLIP_TYPES = _clip_types_info[0]
    else:
        CLIP_TYPES = _clip_types_info
except Exception:
    CLIP_TYPES = ["stable_diffusion", "qwen_image", "krea2"]  # fallback


class ModelLoaderWithLora:
    """
    لودر مدل جامع: Diffusion Model، CLIP (با لیست نوع استاندارد)، VAE
    و ۵ اسلات لورا با قدرت و کلمهٔ تریگر.
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

        # اسلات‌های لورا
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
        # ۱. بارگذاری Diffusion Model
        if not diffusion_model:
            raise ValueError("Diffusion model not selected.")
        unet_path = folder_paths.get_full_path("diffusion_models", diffusion_model)
        model = comfy.sd.load_diffusion_model(unet_path)

        # ۲. بارگذاری CLIP با استفاده از نود استاندارد CLIPLoader
        # این روش تضمین می‌کند که تمام clip_type ها (مثل krea2) بدون ایراد کار کنند.
        clip_loader = CLIPLoader()
        clip = clip_loader.load_clip(clip_model, clip_type)[0]

        # ۳. بارگذاری VAE
        vae_path = folder_paths.get_full_path("vae", vae_model)
        vae_sd = comfy.utils.load_torch_file(vae_path)
        vae = comfy.sd.VAE(sd=vae_sd)

        # ۴. اعمال LoRAها
        trigger_words = []
        lora_loader = LoraLoader()
        for i in range(1, 6):
            lora_name = lora_kwargs.get(f"lora_{i}_model", "none")
            if lora_name == "none":
                continue
            strength = lora_kwargs.get(f"lora_{i}_strength", 1.0)
            trigger_word = lora_kwargs.get(f"lora_{i}_trigger_word", "").strip()

            lora_path = folder_paths.get_full_path("loras", lora_name)
            model, clip = lora_loader.load_lora(model, clip, lora_name, strength, strength)

            if trigger_word:
                trigger_words.append(trigger_word)

        # ۵. ترکیب کلمات تریگر
        final_trigger = ", ".join(trigger_words)
        return (model, clip, vae, final_trigger)