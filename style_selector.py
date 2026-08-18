# style_selector.py
# نود انتخاب سبک بصری و ملیت

class StyleSelector:
    """نود انتخاب سبک هنری، بصری و ملیت برای تصویر"""

    STYLES = [
        ("📷 Realistic", "photorealistic style"),
        ("🎨 Painterly", "painterly art style"),
        ("🧙 Fantasy", "fantasy art style"),
        ("🌸 Anime", "anime style"),
        ("🌀 Surreal", "surreal dreamlike style"),
        ("🌑 Dark", "dark and gritty style"),
        ("🎈 Fun", "colorful playful style"),
        ("🕹️ Pixel Art", "pixel art style"),
        ("🧩 3D Render", "3D rendered style"),
        ("🖌️ Sketch", "sketchy pencil drawing style"),
        ("💧 Watercolor", "watercolor painting style"),
        ("🖍️ Cartoon", "cartoon style"),
        ("📚 Comic Book", "comic book illustration style"),
        ("🖼️ Oil Painting", "oil painting style"),
        ("✏️ Line Art", "clean line art style"),
        ("🧊 Low Poly", "low poly 3D style"),
        ("🌌 Cyberpunk", "cyberpunk neon style"),
        ("🏰 Steampunk", "steampunk style"),
        ("🌿 Ghibli", "Studio Ghibli-inspired style"),
        ("🌅 Vaporwave", "vaporwave aesthetic"),
    ]

    MEDIUMS = [
        ("Digital", "digital art"),
        ("Traditional", "traditional art"),
        ("Photography", "photography"),
        ("Mixed Media", "mixed media"),
        ("3D", "3D render"),
    ]

    COLOR_TONES = [
        ("-", ""),
        ("Warm", "warm color palette"),
        ("Cool", "cool color palette"),
        ("Monochrome", "black and white monochrome"),
        ("Pastel", "soft pastel colors"),
        ("Vibrant", "vibrant saturated colors"),
        ("Muted", "muted desaturated colors"),
        ("Golden", "golden tones"),
        ("Neon", "neon bright colors"),
    ]

    DETAILS = [
        ("-", ""),
        ("Highly Detailed", "highly detailed"),
        ("Minimalist", "minimalist"),
        ("Ornate", "ornate and intricate"),
        ("Texture Rich", "texture-rich"),
    ]

    NATIONALITIES = [
        ("-", ""),
        ("East Asian", "East Asian"),
        ("American", "American"),
        ("European", "European"),
        ("Russian", "Russian"),
        ("Persian (Iran)", "Persian Iranian"),
        ("Arab", "Arab"),
        ("African", "African"),
        ("Native American", "Native American"),
        ("Indian", "Indian"),
        ("Latin American", "Latin American"),
    ]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "style": ([d for d, _ in cls.STYLES],),
                "medium": ([d for d, _ in cls.MEDIUMS],),
                "color_tone": ([d for d, _ in cls.COLOR_TONES], {"default": "-"}),
                "detail": ([d for d, _ in cls.DETAILS], {"default": "-"}),
                "nationality": ([d for d, _ in cls.NATIONALITIES], {"default": "-"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_prompt",)
    FUNCTION = "generate_prompt"
    CATEGORY = "Saeed"

    def generate_prompt(self, style, medium, color_tone, detail, nationality):
        def get_desc(display, source_list):
            for d, desc in source_list:
                if d == display:
                    return desc
            return ""

        prompt = f"Style: {get_desc(style, self.STYLES)}, Medium: {get_desc(medium, self.MEDIUMS)}"

        if color_tone != "-":
            prompt += f", Color: {get_desc(color_tone, self.COLOR_TONES)}"
        if detail != "-":
            prompt += f", Detail: {get_desc(detail, self.DETAILS)}"
        if nationality != "-":
            prompt += f", Nationality: {get_desc(nationality, self.NATIONALITIES)}"

        return (prompt,)