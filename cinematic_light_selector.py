class LightSelector:
    """
    A node for generating detailed lighting prompts.
    Choose Outdoor or Indoor environment, then select options.
    Each option adds descriptive text to the prompt.
    Emoji icons appear in the combo boxes for visual guidance (not in output prompt).
    """
    ENVIRONMENTS = ["☀️ Outdoor", "🏠 Indoor"]

    # Each tuple: (display_with_emoji, prompt_description)
    TIMES_OF_DAY = [
        ("-", ""),
        ("🌅 Morning", "soft warm morning light"),
        ("☀️ Noon", "harsh midday sun directly overhead"),
        ("🌤️ Afternoon", "warm slanting afternoon light"),
        ("🌇 Sunset", "dramatic golden sunset colors"),
        ("🌙 Night", "moonlight and dark shadows"),
        ("✨ Golden Hour", "magical golden hour glow"),
    ]
    WEATHERS = [
        ("-", ""),
        ("☀️ Sunny", "bright direct sunlight"),
        ("☁️ Cloudy", "soft diffused light through clouds"),
        ("🌥️ Overcast", "flat grey overcast sky"),
        ("🌧️ Rain", "wet surfaces and diffused light"),
        ("🌫️ Fog", "misty atmospheric light"),
    ]
    LIGHT_TYPES = [
        ("-", ""),
        ("🔑 Key Light", "main dominant light source, defining form and shadows"),
        ("⚪ Fill Light", "soft bounce light reducing contrast"),
        ("✨ Rim Light", "edge light separating subject from background"),
        ("🪔 Practical Light", "visible in-scene light source like a lamp or candle"),
        ("🌐 Ambient Light", "non-directional fill, overall base illumination"),
        ("🎬 Motivated Light", "light logically coming from an off-screen source"),
    ]
    COLORS = [
        ("-", ""),
        ("⚪ White", "white light"),
        ("🟡 Yellow", "yellow light"),
        ("🟠 Orange", "orange light"),
        ("🔴 Red", "red light"),
        ("🟣 Purple", "purple light"),
        ("🔵 Blue", "blue light"),
        ("🟢 Green", "green light"),
    ]
    DIRECTIONS = [
        ("-", ""),
        ("⬆️ Front", "from the front"),
        ("⬅️ Left", "from the left"),
        ("➡️ Right", "from the right"),
        ("⬇️ Back", "from behind"),
        ("🔼 Top", "from directly above"),
        ("🔽 Bottom", "from below"),
        ("↗️ Three-quarter front", "from a three-quarter front angle"),
        ("↙️ Three-quarter rear", "from a three-quarter rear angle"),
    ]
    QUALITIES = [
        ("-", ""),
        ("🔴 Hard Light", "hard, undiffused light with sharp, crisp shadows"),
        ("🔵 Soft Light", "soft, heavily diffused light with smooth transitions"),
        ("🌁 Diffused Light", "diffused light through a scrim, evenly spread"),
        ("✨ Specular Light", "specular, mirror-like light creating sharp highlights"),
        ("🔄 Bounce Light", "bounced light reflecting off a board, ultra-soft"),
        ("🌟 Volumetric Light", "volumetric light with visible god-rays and shafts"),
    ]
    CONTRASTS = [
        ("-", ""),
        ("☀️ High-Key Lighting", "high-key lighting, bright with minimal shadows"),
        ("🌑 Low-Key Lighting", "low-key lighting, dramatic contrast with deep shadows"),
        ("🎨 Chiaroscuro", "chiaroscuro, dramatic interplay of light and darkness"),
    ]
    KELVIN_VALUES = [
        ("-", ""),
        ("2000K 🕯️", "color temperature 2000K (very warm candlelight)"),
        ("3000K 💡", "color temperature 3000K (warm incandescent)"),
        ("4000K 🌤️", "color temperature 4000K (neutral white)"),
        ("5000K ☀️", "color temperature 5000K (daylight)"),
        ("6500K ☁️", "color temperature 6500K (overcast daylight)"),
        ("10000K 🟦", "color temperature 10000K (deep blue sky)"),
    ]
    GENRES = [
        ("-", ""),
        ("👻 Horror", "sinister horror lighting, monstrous shadows"),
        ("🦸 Hero Intro", "heroic epic lighting with majestic rim light"),
        ("🦹 Villain Intro", "villainous menacing lighting, hollow eye shadows"),
        ("😨 Tension / Suspense", "suspenseful tight lighting, fractured shadows"),
        ("❤️ Romance", "romantic luminous lighting, soft glowing flare"),
        ("😢 Sadness / Melancholy", "melancholic bleak lighting, dreary overcast"),
        ("👽 Sci-Fi", "futuristic sci-fi lighting with neon contrasts"),
        ("💥 Action", "dynamic explosive action lighting, stark flashes"),
        ("🧚 Dreamy / Fantasy", "ethereal fantasy lighting with magical specular highlights"),
    ]

    @classmethod
    def _extract_displays(cls, items):
        return [display for display, _ in items]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "environment": (cls.ENVIRONMENTS,),
                "time_of_day": (cls._extract_displays(cls.TIMES_OF_DAY), {"default": "-"}),
                "weather": (cls._extract_displays(cls.WEATHERS), {"default": "-"}),
                "light_type": (cls._extract_displays(cls.LIGHT_TYPES), {"default": "-"}),
                "color": (cls._extract_displays(cls.COLORS), {"default": "-"}),
                "direction": (cls._extract_displays(cls.DIRECTIONS), {"default": "-"}),
                "quality": (cls._extract_displays(cls.QUALITIES), {"default": "-"}),
                "contrast": (cls._extract_displays(cls.CONTRASTS), {"default": "-"}),
                "kelvin": (cls._extract_displays(cls.KELVIN_VALUES), {"default": "-"}),
                "genre": (cls._extract_displays(cls.GENRES), {"default": "-"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("lighting_prompt",)
    FUNCTION = "generate_prompt"
    CATEGORY = "Saeed"

    def generate_prompt(self, environment, time_of_day, weather, light_type,
                        color, direction, quality, contrast, kelvin, genre):
        # helper to get description by display string (includes emoji)
        def get_desc(display, source_list):
            for d, desc in source_list:
                if d == display:
                    return desc
            return ""

        parts = []
        if environment.startswith("☀️"):
            parts.append("Outdoor lighting")
            time_desc = get_desc(time_of_day, self.TIMES_OF_DAY)
            if time_desc:
                parts.append(time_desc)
            weather_desc = get_desc(weather, self.WEATHERS)
            if weather_desc:
                parts.append(weather_desc)
        else:  # Indoor
            parts.append("Indoor lighting")
            light_desc = get_desc(light_type, self.LIGHT_TYPES)
            if light_desc:
                parts.append(light_desc)
            color_desc = get_desc(color, self.COLORS)
            if color_desc:
                parts.append(color_desc)
            dir_desc = get_desc(direction, self.DIRECTIONS)
            if dir_desc:
                parts.append(dir_desc)
            quality_desc = get_desc(quality, self.QUALITIES)
            if quality_desc:
                parts.append(quality_desc)
            contrast_desc = get_desc(contrast, self.CONTRASTS)
            if contrast_desc:
                parts.append(contrast_desc)

        kelvin_desc = get_desc(kelvin, self.KELVIN_VALUES)
        if kelvin_desc:
            parts.append(kelvin_desc)
        genre_desc = get_desc(genre, self.GENRES)
        if genre_desc:
            parts.append(genre_desc)

        prompt = ", ".join(parts)
        return (prompt,)