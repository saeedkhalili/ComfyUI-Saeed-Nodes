# image_renamer.py
# نود تغییر نام خودکار تصاویر بر اساس توضیح VLM
# بدون تبدیل مجدد تصویر – حفظ پسوند اصلی و metadata

import os
import shutil
import numpy as np
from PIL import Image
import torch
import folder_paths
import comfy.sd
import nodes as core_nodes

TextGenerate = core_nodes.NODE_CLASS_MAPPINGS.get("TextGenerate")
CLIPLoader = core_nodes.NODE_CLASS_MAPPINGS.get("CLIPLoader")

if TextGenerate is None or CLIPLoader is None:
    raise RuntimeError("Required core nodes 'CLIPLoader' and 'TextGenerate' are not available.")


class ImageRenamer:
    """نام‌گذاری و دسته‌بندی تصاویر با هوش مصنوعی – سریع و بدون افت کیفیت"""

    CATEGORIES = [
        "indoor location",
        "outdoor location",
        "character",
        "creature",
        "graphic",
        "object",
        "vehicle",
    ]

    CLASSIFY_PROMPT = (
        "Classify this image into exactly one of these categories: "
        "indoor location, outdoor location, character, creature, graphic, object, vehicle. "
        "Output only the category name, nothing else."
    )

    @classmethod
    def INPUT_TYPES(cls):
        clip_models = folder_paths.get_filename_list("text_encoders")
        try:
            clip_types = [e.name.lower() for e in comfy.sd.CLIPType]
        except Exception:
            clip_types = ["stable_diffusion", "qwen_image"]

        return {
            "required": {
                "source_folder": ("STRING", {
                    "default": "",
                    "multiline": False
                }),
                "clip_name": (clip_models, {"default": "Qwen\\qwen3.5_4b_bf16.safetensors"}),
                "clip_type": (clip_types, {"default": "qwen_image"}),
                "prompt": ("STRING", {
                    "multiline": True,
                    "default": "Output exactly five lowercase words describing the image, joined by underscores. Do NOT add any other text, punctuation, line breaks, or explanation. Only the five words."
                }),
                "max_length": ("INT", {"default": 64, "min": 1, "max": 1024}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "output_prefix": ("STRING", {"default": "Rename"}),
                "operation": (["copy", "move"], {"default": "copy"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("summary",)
    FUNCTION = "rename_images"
    CATEGORY = "Saeed"

    # ---------- helpers ----------
    def _resolve_source_folder(self, folder_arg):
        """تعیین مسیر پوشهٔ مبدأ"""
        if folder_arg and str(folder_arg).strip():
            folder = str(folder_arg).strip()
            folder = os.path.expanduser(folder)
            if not os.path.isabs(folder):
                folder = os.path.abspath(folder)
            return folder
        else:
            return folder_paths.get_input_directory()

    def _load_image_tensor(self, path):
        """بارگذاری تصویر به‌صورت tensor برای پردازش VLM"""
        with Image.open(path) as img:
            rgb = img.convert("RGB")
            arr = np.array(rgb).astype(np.float32) / 255.0
        return torch.from_numpy(arr).unsqueeze(0)

    def _clean_caption(self, text):
        if text is None:
            return ""
        text = str(text)
        text = text.replace("</think>", "")
        text = text.replace("\n", "")
        text = text.strip()
        return text

    def _unique_path(self, directory, base_name, ext):
        """ساخت مسیر یکتا با پسوند اصلی"""
        os.makedirs(directory, exist_ok=True)
        candidate = f"{base_name}{ext}"
        counter = 1
        while os.path.exists(os.path.join(directory, candidate)):
            candidate = f"{base_name}_{counter}{ext}"
            counter += 1
        return os.path.join(directory, candidate)

    def _text_generate(self, tg, clip, image_tensor, prompt, max_length, sampling_mode):
        return tg.execute(
            clip=clip,
            image=image_tensor,
            prompt=prompt,
            max_length=max_length,
            sampling_mode=sampling_mode,
        )[0]

    def _classify_image(self, tg, clip, image_tensor, sampling_mode):
        raw = self._text_generate(
            tg, clip, image_tensor, self.CLASSIFY_PROMPT,
            16, sampling_mode
        )
        raw = self._clean_caption(raw).lower()

        # تطبیق دقیق با دسته‌ها (اولویت با دو کلمه‌ای‌ها)
        for cat in self.CATEGORIES:
            if cat in raw:
                return cat
        return "object"   # دستهٔ پیش‌فرض

    def rename_images(self, source_folder, clip_name, clip_type, prompt,
                      max_length, seed, output_prefix, operation):
        root = self._resolve_source_folder(source_folder)

        if not os.path.isdir(root):
            raise FileNotFoundError(f"Folder '{root}' does not exist.")

        # بارگذاری CLIP
        clip_loader = CLIPLoader()
        clip = clip_loader.load_clip(clip_name, clip_type, "default")[0]

        valid_exts = (".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff")
        files = []
        # جمع‌آوری فایل‌ها از پوشهٔ اصلی و زیرپوشه‌ها (به‌جز پوشهٔ خروجی)
        out_base = os.path.join(root, output_prefix)
        for dirpath, dirnames, filenames in os.walk(root):
            if os.path.abspath(dirpath).startswith(os.path.abspath(out_base)):
                continue
            for f in filenames:
                if f.lower().endswith(valid_exts):
                    files.append(os.path.join(dirpath, f))

        files.sort()

        if not files:
            return ("No image files found.",)

        tg = TextGenerate()

        sampling_mode = {
            "sampling_mode": "on",
            "temperature": 0.7,
            "top_k": 64,
            "top_p": 0.95,
            "min_p": 0.05,
            "repetition_penalty": 1.05,
            "seed": seed,
        }

        processed = 0
        skipped = 0
        summary_lines = []

        for src_path in files:
            ext = os.path.splitext(src_path)[1].lower()
            if not ext:
                ext = ".jpg"

            try:
                image_tensor = self._load_image_tensor(src_path)
            except Exception:
                skipped += 1
                continue

            # ۱) تولید نام
            caption = self._text_generate(
                tg, clip, image_tensor, prompt, max_length, sampling_mode
            )
            clean_name = self._clean_caption(caption)
            if not clean_name or len(clean_name) >= 128:
                clean_name = "ERROR_Renaming"

            # ۲) دسته‌بندی
            category = self._classify_image(tg, clip, image_tensor, sampling_mode)

            # ۳) مسیر مقصد
            dest_dir = os.path.join(out_base, category)
            dest_path = self._unique_path(dest_dir, clean_name, ext)

            # ۴) کپی یا جابه‌جایی
            try:
                if operation == "move":
                    shutil.move(src_path, dest_path)
                else:
                    shutil.copy2(src_path, dest_path)
                processed += 1
            except Exception:
                skipped += 1

        summary_lines.append(f"Processed: {processed} files")
        summary_lines.append(f"Skipped: {skipped}")
        return (", ".join(summary_lines),)