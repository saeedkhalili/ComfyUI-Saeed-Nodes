# image_date_organizer.py
# نود مرتب‌سازی تصاویر و ویدئوها بر اساس تاریخ عکاسی/تغییر فایل
# جابجایی/کپی فایل‌ها در پوشه‌های سال/ماه/روز (میلادی یا هجری شمسی)
# پشتیبانی از مسیر دلخواه، جستجوی بازگشتی و حذف پوشه‌های خالی قبلی

import os
import re
import shutil
import datetime as dt
from PIL import Image

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
    """تبدیل date میلادی به tuple سال، ماه، روز هجری شمسی"""
    jdn = _g2d(g_date.year, g_date.month, g_date.day)
    return _d2j(jdn)

# ----------------------------------------------------------------------
# نام ماه‌ها
GREGORIAN_MONTHS = {
    1: "January", 2: "February", 3: "March", 4: "April",
    5: "May", 6: "June", 7: "July", 8: "August",
    9: "September", 10: "October", 11: "November", 12: "December"
}
JALALI_MONTHS = {
    1: "فروردین", 2: "اردیبهشت", 3: "خرداد", 4: "تیر",
    5: "مرداد", 6: "شهریور", 7: "مهر", 8: "آبان",
    9: "آذر", 10: "دی", 11: "بهمن", 12: "اسفند"
}

# ----------------------------------------------------------------------
class ImageDateOrganizer:
    """مرتب‌سازی خودکار تصاویر و ویدئوها بر اساس تاریخ"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "source_folder": ("STRING", {
                    "default": "",
                    "multiline": False
                }),
                "recursive": ("BOOLEAN", {"default": True}),
                "calendar": (["Gregorian", "Jalali (Shamsi)"], {"default": "Gregorian"}),
                "max_files_per_day": ("INT", {"default": 5, "min": 1, "max": 1000}),
                "operation": (["move", "copy"], {"default": "move"}),
                "remove_empty_old_folders": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("summary",)
    FUNCTION = "organize"
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

    def _get_date(self, file_path):
        """استخراج تاریخ عکاسی از EXIF یا تغییر فایل برای ویدئوها"""
        try:
            if file_path.lower().endswith((".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff")):
                img = Image.open(file_path)
                exif = img.getexif()
                for tag in (36867, 36868, 306):
                    val = exif.get(tag)
                    if val:
                        m = re.search(r'(\d{4})[:\-](\d{2})[:\-](\d{2})', str(val))
                        if m:
                            year, month, day = map(int, m.groups())
                            return dt.date(year, month, day)
            return dt.date.fromtimestamp(os.path.getmtime(file_path))
        except Exception:
            return dt.date.fromtimestamp(os.path.getmtime(file_path))

    def _is_already_organized(self, src_path, root):
        """بررسی اینکه فایل قبلاً در ساختار سال/ماه قرار دارد یا نه"""
        rel = os.path.relpath(os.path.dirname(src_path), root)
        parts = rel.split(os.sep)
        if len(parts) >= 2:
            if re.fullmatch(r'\d{4}', parts[0]) and re.match(r'\d{2}_.+', parts[1]):
                return True
        return False

    def _count_existing_for_day(self, directory, day):
        """تعداد فایل‌های موجود در ماه با پیشوند روز + فایل‌های داخل پوشهٔ روز"""
        count = 0
        day_str = f"{day:02d}"
        if os.path.isdir(directory):
            for f in os.listdir(directory):
                if os.path.isfile(os.path.join(directory, f)) and f.startswith(day_str + "_"):
                    count += 1
        day_dir = os.path.join(directory, day_str)
        if os.path.isdir(day_dir):
            count += len([f for f in os.listdir(day_dir)
                          if os.path.isfile(os.path.join(day_dir, f))])
        return count

    def _unique_file_name(self, directory, base_prefix, ext):
        """ساخت نام فایل یکتا با شمارنده"""
        os.makedirs(directory, exist_ok=True)
        counter = 1
        while True:
            if base_prefix:
                candidate = f"{base_prefix}_{counter:03d}{ext}"
            else:
                candidate = f"{counter:03d}{ext}"
            path = os.path.join(directory, candidate)
            if not os.path.exists(path):
                return path
            counter += 1

    def organize(self, source_folder, recursive, calendar, max_files_per_day,
                 operation, remove_empty_old_folders):
        root = self._resolve_source_folder(source_folder)

        if not os.path.isdir(root):
            raise FileNotFoundError(f"Folder '{root}' does not exist.")

        valid_exts = (
            ".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff",
            ".mp4", ".mov", ".mkv", ".avi", ".webm", ".m4v", ".flv",
            ".wmv", ".mpeg", ".mpg", ".3gp"
        )

        # جمع‌آوری همهٔ فایل‌ها (بازگشتی یا فقط پوشهٔ اصلی)
        files = []
        if recursive:
            for dirpath, dirnames, filenames in os.walk(root):
                for f in filenames:
                    if f.lower().endswith(valid_exts):
                        full = os.path.join(dirpath, f)
                        files.append(full)
        else:
            for f in os.listdir(root):
                full = os.path.join(root, f)
                if os.path.isfile(full) and f.lower().endswith(valid_exts):
                    files.append(full)

        files.sort()

        if not files:
            return ("No image or video files found.",)

        moved_count = 0
        skipped_count = 0
        protected_dirs = set()  # پوشه‌های ساخته‌شده که نباید حذف شوند
        run_counters = {}  # key = (year, month, day)

        for src_path in files:
            # اگر فایل قبلاً در ساختار سال/ماه است، رد می‌کنیم
            if self._is_already_organized(src_path, root):
                continue

            ext = os.path.splitext(src_path)[1].lower()
            if not ext:
                ext = ".jpg"

            try:
                file_date = self._get_date(src_path)
            except Exception:
                skipped_count += 1
                continue

            if calendar == "Gregorian":
                year, month, day = file_date.year, file_date.month, file_date.day
                month_name = GREGORIAN_MONTHS.get(month, str(month))
            else:
                year, month, day = gregorian_to_jalali(file_date)
                month_name = JALALI_MONTHS.get(month, str(month))

            year_str = f"{year:04d}"
            month_str = f"{month:02d}_{month_name}"

            month_dir = os.path.join(root, year_str, month_str)
            os.makedirs(month_dir, exist_ok=True)
            protected_dirs.add(month_dir)
            protected_dirs.add(os.path.dirname(month_dir))  # سال

            key = (year, month, day)
            run_count = run_counters.get(key, 0)
            existing = self._count_existing_for_day(month_dir, day)
            total_for_day = existing + run_count

            if total_for_day < max_files_per_day:
                base_prefix = f"{day:02d}"
                dest_dir = month_dir
            else:
                day_str = f"{day:02d}"
                dest_dir = os.path.join(month_dir, day_str)
                base_prefix = ""   # چون پوشه روز خودش مشخص است

            protected_dirs.add(dest_dir)
            dest_path = self._unique_file_name(dest_dir, base_prefix, ext)

            try:
                if operation == "move":
                    shutil.move(src_path, dest_path)
                else:
                    shutil.copy2(src_path, dest_path)
                moved_count += 1
                run_counters[key] = run_count + 1
            except Exception:
                skipped_count += 1

        # حذف پوشه‌های خالی قدیمی (فقط در حالت move و در صورت فعال بودن)
        if operation == "move" and remove_empty_old_folders:
            for dirpath, dirnames, filenames in os.walk(root, topdown=False):
                # پوشه‌های جدید و مسیرهایی که باید حفظ شوند را حذف نمی‌کنیم
                if dirpath == root:
                    continue
                if dirpath in protected_dirs:
                    continue
                # اگر پوشه در داخل یکی از پوشه‌های محافظت‌شده است، حذف نمی‌کنیم
                if any(dirpath.startswith(p + os.sep) for p in protected_dirs):
                    continue
                try:
                    if not os.listdir(dirpath):  # فقط پوشهٔ خالی
                        os.rmdir(dirpath)
                except OSError:
                    pass

        summary_lines = []
        summary_lines.append(f"Processed: {moved_count} files")
        summary_lines.append(f"Skipped: {skipped_count}")
        if operation == "move" and remove_empty_old_folders:
            summary_lines.append("Empty old folders removed: True")
        return (", ".join(summary_lines),)