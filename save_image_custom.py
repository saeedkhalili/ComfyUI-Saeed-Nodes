# save_image_custom.py
# نود ذخیره‌ی تصویر با نام‌گذاری سفارشی

import os
import datetime as dt

import numpy as np
from PIL import Image
from PIL.PngImagePlugin import PngInfo

import folder_paths

# ----------------------------------------------------------------------
# توابع تبدیل تاریخ میلادی به هجری شمسی (الگوریتم استاندارد jalaali-js)
def _div(a, b):
    if a >= 0:
        return a // b
    return -((-a) // b)

def _mod(a, b):
    return a - b * _div(a, b)

_BREAKS = [-61, 9, 38, 199, 426, 686, 756, 818, 1111, 1181, 1210,
           1635, 2060, 2097, 2192, 2262, 2324, 2394, 2456, 3178]

def _jal_cal(jy, without_leap=False):
    bl = len(_BREAKS)
    gy = jy + 621
    leap_j = -14
    jp = _BREAKS[0]
    jump = 0
    for i in range(1, bl):
        jm = _BREAKS[i]
        jump = jm - jp
        if jy < jm:
            break
        leap_j = leap_j + _div(jump, 33) * 8 + _div(_mod(jump, 33), 4)
        jp = jm
    n = jy - jp
    leap_j = leap_j + _div(n, 33) * 8 + _div(_mod(n, 33) + 3, 4)
    if jump > 0 and n > 0 and (jump - n) < 33:
        leap_j += 1
    leap_g = _div(gy, 4) - _div((_div(gy, 100) + 1) * 3, 4) - 150
    march = 20 + leap_j - leap_g
    if not without_leap:
        if (jump - n) < 33:
            if march < 21:
                leap_j += 1
        else:
            if march < 20:
                leap_j += 1
    return leap_j, gy, march

def _g2d(gy, gm, gd):
    d = _div((gy + _div(gm - 8, 6) + 100100) * 1461, 4) + \
        _div(153 * _mod(gm + 9, 12) + 2, 5) + gd - 34840408
    d = d - _div(_div(gy + 100100 + _div(gm - 8, 6), 100) * 3, 4) + 752
    return d

def _d2g(jdn):
    j = 4 * jdn + 139361631
    j = j + _div(_div(4 * jdn + 183187720, 146097) * 3, 4) * 4 - 3908
    i = _div(_mod(j, 1461), 4) * 5 + 308
    gd = _div(_mod(i, 153), 5) + 1
    gm = _mod(_div(i, 153), 12) + 1
    gy = _div(j, 1461) - 100100 + _div(8 - gm, 6)
    return gy, gm, gd

def _d2j(jdn):
    gy, _, _ = _d2g(jdn)
    jy = gy - 621
    _, _, march = _jal_cal(jy, False)
    jdn1f = _g2d(gy, 3, march)
    k = jdn - jdn1f
    if k >= 0:
        if k <= 185:
            jm = 1 + _div(k, 31)
            jd = _mod(k, 31) + 1
            return jy, jm, jd
        else:
            k -= 186
    else:
        jy -= 1
        k += 179
        leap_j, _, _ = _jal_cal(jy, False)
        if leap_j == 1:
            k += 1
    jm = 7 + _div(k, 30)
    jd = _mod(k, 30) + 1
    return jy, jm, jd

def gregorian_to_jalali(g_date):
    jdn = _g2d(g_date.year, g_date.month, g_date.day)
    return _d2j(jdn)


class SaveImageCustom:
    """ذخیره‌ی تصویر با نام‌گذاری دلخواه و پیش‌نمایش"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "use_size": ("BOOLEAN", {"default": True}),
                "use_date": ("BOOLEAN", {"default": True}),
                "calendar": (["Gregorian", "Jalali"], {"default": "Gregorian"}),
                "use_seed": ("BOOLEAN", {"default": True}),
                "separator": ("STRING", {"default": "_", "multiline": False}),
            },
            "optional": {
                "folder": ("STRING", {"default": ""}),
                "project_name": ("STRING", {"default": ""}),
                "suffix": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("images", "filename")
    FUNCTION = "save_image"
    CATEGORY = "Saeed"
    OUTPUT_NODE = True

    def save_image(self, images, use_size, use_date, calendar, use_seed,
                   separator, folder="", project_name="", suffix=""):

        # تلاش برای خواندن seed از تنسور تصویر (اگر نود تولیدکننده آن را ست کرده باشد)
        seed = getattr(images, "seed", None)

        parts = []
        if project_name.strip():
            parts.append(project_name.strip())

        if use_size:
            w = images.shape[2]
            h = images.shape[1]
            parts.append(f"{w}x{h}")

        if use_date:
            now = dt.date.today()
            if calendar == "Gregorian":
                date_str = f"{now.year:04d}{now.month:02d}{now.day:02d}"
            else:
                jy, jm, jd = gregorian_to_jalali(now)
                date_str = f"{jy:04d}{jm:02d}{jd:02d}"
            parts.append(date_str)

        if use_seed and seed is not None:
            parts.append(str(seed))

        if not parts:
            parts.append("image")

        base_name = separator.join(parts)

        output_root = folder_paths.get_output_directory()
        if folder.strip():
            save_dir = os.path.join(output_root, folder.strip())
        else:
            save_dir = output_root
        os.makedirs(save_dir, exist_ok=True)

        saved_files = []
        batch = images.shape[0]
        for i in range(batch):
            counter = 1
            while True:
                # بعد از شمارنده "_" و سپس عبارت انتهایی
                if suffix.strip():
                    candidate = f"{base_name}_{counter:05d}_{suffix.strip()}.png"
                else:
                    candidate = f"{base_name}_{counter:05d}.png"
                full_path = os.path.join(save_dir, candidate)
                if not os.path.exists(full_path):
                    break
                counter += 1

            img_np = (images[i].cpu().numpy() * 255.0).astype(np.uint8)
            pil_img = Image.fromarray(img_np, "RGB")

            pnginfo = PngInfo()
            meta_dict = getattr(images, "metadata", None)
            if meta_dict:
                for k, v in meta_dict.items():
                    if isinstance(v, str):
                        pnginfo.add_text(k, v)

            pil_img.save(full_path, pnginfo=(pnginfo if pnginfo else None))
            saved_files.append({
                "filename": candidate,
                "subfolder": folder.strip() if folder.strip() else "",
                "type": "output"
            })

        ui = {"images": saved_files}
        return {"ui": ui, "result": (images, saved_files[-1]["filename"] if saved_files else "")}