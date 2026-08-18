# prompt_randomizer.py
# نود کنترل‌کننده برای رندوم کردن چند پرامپت‌جنریتور با یک کلیک

class PromptRandomizer:
    """انتخاب و رندوم‌سازی گروهی پرامپت‌جنریتورها"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "camera": ("BOOLEAN", {"default": False}),
                "camera_movement": ("BOOLEAN", {"default": False}),
                "light": ("BOOLEAN", {"default": False}),
                "landscape": ("BOOLEAN", {"default": False}),
                "character": ("BOOLEAN", {"default": False}),
                "action": ("BOOLEAN", {"default": False}),
                "scene_element": ("BOOLEAN", {"default": False}),
                "style": ("BOOLEAN", {"default": False}),
                "framing": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "randomize"
    CATEGORY = "Saeed"
    OUTPUT_NODE = True

    def randomize(self, **kwargs):
        # عملیات رندوم توسط افزونهٔ JavaScript انجام می‌شود
        return ()