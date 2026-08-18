# scene_element_generator.py
# تولید المان صحنه برای چهار موقعیت مختلف

class SceneElementGenerator:
    """نود تولید المان صحنه در چهار لایهٔ فورگراند، میدگراند، خیلی نزدیک و سراسری"""

    ELEMENTS = [
        ("-", ""),
        ("🌳 Tree", "a large tree"),
        ("🪨 Rock", "a large rock"),
        ("🔥 Fire", "fire"),
        ("💧 Water", "water"),
        ("🌫️ Fog", "fog"),
        ("🌺 Flowers", "flowers"),
        ("🍄 Mushrooms", "mushrooms"),
        ("🏮 Lantern", "lantern"),
        ("🪑 Furniture", "furniture"),
        ("🗿 Statue", "statue"),
        ("🪞 Mirror", "mirror"),
        ("🪜 Ladder", "ladder"),
        ("🧱 Wall", "wall"),
        ("🪟 Window", "window"),
        ("🚪 Door", "door"),
        ("💎 Crystal", "glowing crystal formations"),
        ("🌀 Portal", "mystical swirling portal"),
        ("🚗 Vehicle", "a vehicle"),
    ]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "foreground_element": ([d for d, _ in cls.ELEMENTS],),
                "midground_element": ([d for d, _ in cls.ELEMENTS],),
                "very_close_element": ([d for d, _ in cls.ELEMENTS],),
                "across_frame_element": ([d for d, _ in cls.ELEMENTS],),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("scene_element_prompt",)
    FUNCTION = "generate_prompt"
    CATEGORY = "Saeed"

    def generate_prompt(self, foreground_element, midground_element,
                        very_close_element, across_frame_element):
        def get_desc(display, source_list):
            for d, desc in source_list:
                if d == display:
                    return desc
            return ""

        parts = []

        if foreground_element != "-":
            parts.append(f"Foreground element: {get_desc(foreground_element, self.ELEMENTS)}")
        if midground_element != "-":
            parts.append(f"Midground element: {get_desc(midground_element, self.ELEMENTS)}")
        if very_close_element != "-":
            parts.append(f"Very close element: {get_desc(very_close_element, self.ELEMENTS)}")
        if across_frame_element != "-":
            parts.append(f"Across frame element: {get_desc(across_frame_element, self.ELEMENTS)}")

        if not parts:
            return ("",)

        return (" | ".join(parts),)