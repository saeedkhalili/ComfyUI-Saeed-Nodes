# image_generator.py
# یک نود که مدل را گرفته، پرامپت‌ها را ترکیب می‌کند،
# در صورت وجود AuraFlow را اعمال می‌کند، نمونه‌برداری و دیکد را انجام می‌دهد
# و تصویر به‌همراه نام فایل خروجی می‌دهد.

import comfy.sd
from nodes import CLIPTextEncode, KSampler, VAEDecode

try:
    from comfy.model_sampling import AuraFlowModelSampling
except ImportError:
    AuraFlowModelSampling = None


class ImageGenerator:
    """نود جنریتور سینمایی – پرامپت‌ها را ترکیب کرده، نمونه‌برداری و دیکد می‌کند."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("MODEL",),
                "clip": ("CLIP",),
                "vae": ("VAE",),
                "latent": ("LATENT",),
                "project_name": ("STRING", {"default": "ProGen"}),     # ← بعد از latent
                "ratio_name": ("STRING", {"default": ""}),              # ← جایگزین ratio_string
                "positive_prompt": ("STRING", {"multiline": True, "default": ""}),
                "negative_prompt": ("STRING", {"multiline": True, "default": ""}),
                "camera_prompt": ("STRING", {"default": ""}),
                "light_prompt": ("STRING", {"default": ""}),
                "trigger_words": ("STRING", {"default": ""}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "steps": ("INT", {"default": 8, "min": 1, "max": 100}),
                "cfg": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 20.0, "step": 0.1}),
                "sampler_name": (["euler", "heun", "dpm_2", "dpmpp_2m", "lms"], {"default": "euler"}),
                "scheduler": (["normal", "simple", "beta", "karras"], {"default": "beta"}),
                "denoise": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "aura_flow_shift": ("FLOAT", {"default": 3.0, "min": 0.0, "max": 10.0, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("image", "file_name")
    FUNCTION = "generate"
    CATEGORY = "Saeed"

    def generate(self, model, clip, vae, latent, project_name, ratio_name,
                 positive_prompt, negative_prompt, camera_prompt, light_prompt,
                 trigger_words, seed, steps, cfg, sampler_name, scheduler,
                 denoise, aura_flow_shift):

        # 1. AuraFlow (در صورت وجود)
        if AuraFlowModelSampling is not None:
            try:
                model.model_sampling = AuraFlowModelSampling(model.model_config, s=aura_flow_shift)
            except TypeError:
                model.model_sampling = AuraFlowModelSampling(model.model_config)
        else:
            print("Warning: AuraFlow sampling not available – skipping.")

        # 2. ساخت پرامپت کامل
        full_prompt = positive_prompt
        if camera_prompt.strip():
            full_prompt += f" | {camera_prompt.strip()}"
        if light_prompt.strip():
            full_prompt += f" | {light_prompt.strip()}"
        if trigger_words.strip():
            full_prompt += f" {trigger_words.strip()}"

        # 3. انکد کردن پرامپت‌ها
        encode_pos = CLIPTextEncode()
        pos_cond = encode_pos.encode(clip, full_prompt)[0]
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
        image.seed = seed   # افزودن seed به تصویر

        # 6. ساخت نام فایل
        safe_ratio = ratio_name.replace(" ", "_")
        if safe_ratio:
            file_name = f"{project_name}/{safe_ratio}_SEED{seed}"
        else:
            file_name = f"{project_name}/SEED{seed}"

        return (image, file_name)