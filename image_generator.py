# image_generator.py
# نود جنریتور تصویر – اتصال پرامپت‌ها و اجرای نمونه‌برداری

import torch
import comfy.sd
from nodes import CLIPTextEncode, KSampler, VAEDecode

try:
    from comfy.model_sampling import AuraFlowModelSampling
except ImportError:
    AuraFlowModelSampling = None


class ImageGenerator:
    """جنریتور تصویر – مدل، کلیپ، وی‌ای‌ای، لاتنت و پرامپت‌ها را می‌گیرد"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("MODEL",),
                "clip": ("CLIP",),
                "vae": ("VAE",),
                "latent": ("LATENT",),
                "positive_prompt": ("STRING", {"multiline": True, "default": ""}),
                "negative_prompt": ("STRING", {"multiline": True, "default": ""}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "steps": ("INT", {"default": 8, "min": 1, "max": 100}),
                "cfg": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 20.0, "step": 0.1}),
                "sampler_name": (["euler", "heun", "dpm_2", "dpmpp_2m", "lms"], {"default": "euler"}),
                "scheduler": (["normal", "simple", "beta", "karras"], {"default": "beta"}),
                "denoise": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "aura_flow_shift": ("FLOAT", {"default": 3.0, "min": 0.0, "max": 10.0, "step": 0.01}),
            },
            "optional": {
                "camera_prompt": ("STRING", {"forceInput": True, "default": ""}),
                "camera_movement_prompt": ("STRING", {"forceInput": True, "default": ""}),
                "light_prompt": ("STRING", {"forceInput": True, "default": ""}),
                "landscape_prompt": ("STRING", {"forceInput": True, "default": ""}),
                "character_prompt": ("STRING", {"forceInput": True, "default": ""}),
                "action_prompt": ("STRING", {"forceInput": True, "default": ""}),
                "scene_element_prompt": ("STRING", {"forceInput": True, "default": ""}),
                "style_prompt": ("STRING", {"forceInput": True, "default": ""}),
                "framing_prompt": ("STRING", {"forceInput": True, "default": ""}),
                "trigger_words": ("STRING", {"forceInput": True, "default": ""}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "generate"
    CATEGORY = "Saeed"

    def generate(self, model, clip, vae, latent, positive_prompt, negative_prompt,
                 seed, steps, cfg, sampler_name, scheduler, denoise, aura_flow_shift,
                 camera_prompt="", camera_movement_prompt="", light_prompt="",
                 landscape_prompt="", character_prompt="", action_prompt="",
                 scene_element_prompt="", style_prompt="", framing_prompt="", trigger_words=""):

        # 1. AuraFlow (در صورت وجود)
        if AuraFlowModelSampling is not None:
            try:
                model.model_sampling = AuraFlowModelSampling(model.model_config, s=aura_flow_shift)
            except TypeError:
                model.model_sampling = AuraFlowModelSampling(model.model_config)
        else:
            print("Warning: AuraFlow sampling not available – skipping.")

        # 2. ساخت پرامپت کامل
        final_prompt = positive_prompt.strip()

        prompt_parts = [
            ("camera", camera_prompt.strip()),
            ("camera movement", camera_movement_prompt.strip()),
            ("light", light_prompt.strip()),
            ("landscape", landscape_prompt.strip()),
            ("character", character_prompt.strip()),
            ("action", action_prompt.strip()),
            ("scene element", scene_element_prompt.strip()),
            ("style", style_prompt.strip()),
            ("framing", framing_prompt.strip()),
        ]

        added_prompts = []
        for label, p in prompt_parts:
            if p:
                added_prompts.append(p)

        if trigger_words.strip():
            added_prompts.append(trigger_words.strip())

        if final_prompt and added_prompts:
            final_prompt = final_prompt + " | " + " | ".join(added_prompts)
        elif not final_prompt and added_prompts:
            final_prompt = " | ".join(added_prompts)

        # 3. انکد کردن پرامپت‌ها
        encode_pos = CLIPTextEncode()
        pos_cond = encode_pos.encode(clip, final_prompt)[0]
        encode_neg = CLIPTextEncode()
        neg_cond = encode_neg.encode(clip, negative_prompt)[0]

        # 4. نمونه‌برداری
        sampler = KSampler()
        latent_out = sampler.sample(model, seed, steps, cfg,
                                    sampler_name, scheduler,
                                    pos_cond, neg_cond, latent, denoise)[0]

        # 5. دیکد تصویر
        decoder = VAEDecode()
        image = decoder.decode(vae, latent_out)[0]
        image.seed = seed   # افزودن seed به تصویر برای استفاده در نود ذخیره‌ساز

        return (image,)