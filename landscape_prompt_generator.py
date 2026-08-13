# landscape_prompt_generator.py
# یک نود برای تولید پرامپت منظره پس‌زمینه

class LandscapePromptGenerator:
    """نود تولید پرامپت منظره پس‌زمینه – انتخابی، سریع و سینمایی"""

    LANDSCAPES = [
        ("🏜️ Desert", "vast desert with golden sand dunes"),
        ("🌲 Forest", "dense forest with tall trees"),
        ("🌴 Jungle", "lush tropical jungle"),
        ("❄️ Arctic", "frozen arctic landscape with ice and snow"),
        ("🌊 Underwater", "underwater scene with coral reefs and marine life"),
        ("🏔️ Mountains", "majestic mountain range with snowy peaks"),
        ("🌾 Grassland", "open grassland plains under wide sky"),
        ("🏞️ Canyon", "deep canyon with layered rock formations"),
        ("🌋 Volcano", "active volcano with lava flows"),
        ("🪐 Space", "deep space with stars and nebulae"),
        ("👽 Alien Planet", "alien planet surface with strange rock formations"),
        ("🏙️ Urban City", "modern city skyline with tall buildings"),
        ("🏚️ Dystopian Ruins", "dystopian ruined city with decaying structures"),
        ("🧙 Fantasy Realm", "fantasy realm with magical elements"),
        ("🏖️ Coastal Beach", "sandy beach with ocean waves"),
        ("🕳️ Cave", "dark cave interior with stalactites"),
        ("🐊 Swamp", "murky swamp with twisted trees and water"),
        ("🌸 Meadow", "colorful flower meadow under open sky"),
    ]

    WEATHERS = [
        ("-", ""),
        ("☀️ Clear", "clear sky"),
        ("☁️ Cloudy", "partly cloudy sky"),
        ("🌧️ Rain", "rain falling"),
        ("❄️ Snow", "snow falling"),
        ("⛈️ Storm", "thunderstorm with lightning"),
        ("🌫️ Fog", "dense fog"),
        ("🌪️ Sandstorm", "sandstorm with blowing sand"),
        ("🌋 Ashfall", "volcanic ash falling"),
        ("☄️ Meteor Shower", "meteor shower in the sky"),
        ("🌌 Aurora", "aurora borealis in the sky"),
    ]

    LIGHTINGS = [
        ("-", ""),
        ("🌇 Golden Hour", "warm golden hour light"),
        ("🌃 Blue Hour", "cool blue hour light"),
        ("☀️ Midday", "bright midday sun"),
        ("🌙 Moonlight", "soft moonlight"),
        ("✨ Bioluminescence", "glowing bioluminescent light"),
        ("💡 Neon", "neon lighting"),
        ("🌟 Volumetric Rays", "volumetric light rays"),
        ("🌥️ Overcast", "soft overcast light"),
        ("🔥 Firelight", "warm flickering firelight"),
        ("🪐 Cosmic Glow", "mysterious cosmic glow"),
    ]

    MOODS = [
        ("-", ""),
        ("😌 Peaceful", "peaceful and serene atmosphere"),
        ("🔮 Mysterious", "mysterious and mystical mood"),
        ("🏆 Epic", "epic and grand atmosphere"),
        ("🖤 Dark", "dark and moody atmosphere"),
        ("🎉 Joyful", "joyful and vibrant mood"),
        ("😢 Melancholy", "melancholic and nostalgic mood"),
        ("❤️ Romantic", "romantic and dreamy mood"),
        ("🌑 Lonely", "lonely and isolated atmosphere"),
    ]

    VEGETATIONS = [
        ("-", ""),
        ("🌵 Sparse", "sparse desert vegetation"),
        ("🌿 Lush", "lush green vegetation"),
        ("🍂 Autumnal", "autumnal trees with falling leaves"),
        ("🌸 Blooming", "blooming flowers and blossoms"),
        ("👾 Alien Flora", "strange alien plants"),
        ("💎 Crystal Flora", "crystal formations and glowing plants"),
        ("🍄 Mushrooms", "giant mushrooms and fungi"),
    ]

    SKY_ELEMENTS = [
        ("-", ""),
        ("🌙 Single Moon", "a single large moon in the sky"),
        ("🌕🌖 Twin Moons", "two moons in the sky"),
        ("✨ Stars", "a sky full of stars"),
        ("🌌 Galaxy", "a visible galaxy band"),
        ("🪐 Planet", "a large planet looming in the sky"),
        ("💫 Ringed Planet", "a ringed planet in the sky"),
        ("🌈 Nebula", "colorful nebula clouds"),
        ("☄️ Comet", "a passing comet"),
        ("🌌 Aurora", "aurora in the sky"),
        ("☀️☀️ Multiple Suns", "multiple suns in the sky"),
    ]

    STYLES = [
        ("📷 Realistic", "photorealistic style"),
        ("🧙 Fantasy", "fantasy art style"),
        ("🌀 Surreal", "surreal dreamlike style"),
        ("🌑 Dark", "dark and gritty style"),
        ("🎈 Fun", "colorful playful style"),
        ("🌸 Anime", "anime style"),
        ("🎨 Painterly", "painterly art style"),
    ]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "landscape_type": ([d for d, _ in cls.LANDSCAPES],),
                "weather": ([d for d, _ in cls.WEATHERS], {"default": "-"}),
                "lighting": ([d for d, _ in cls.LIGHTINGS], {"default": "-"}),
                "mood": ([d for d, _ in cls.MOODS], {"default": "-"}),
                "vegetation": ([d for d, _ in cls.VEGETATIONS], {"default": "-"}),
                "sky_element": ([d for d, _ in cls.SKY_ELEMENTS], {"default": "-"}),
                "style": ([d for d, _ in cls.STYLES], {"default": "📷 Realistic"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("landscape_prompt",)
    FUNCTION = "generate_prompt"
    CATEGORY = "Saeed"

    def generate_prompt(self, landscape_type, weather, lighting, mood,
                        vegetation, sky_element, style):
        def get_desc(display, source_list):
            for d, desc in source_list:
                if d == display:
                    return desc
            return ""

        landscape_desc = get_desc(landscape_type, self.LANDSCAPES)
        prompt = f"Background landscape: {landscape_desc}"

        if weather != "-":
            prompt += f", {get_desc(weather, self.WEATHERS)}"
        if lighting != "-":
            prompt += f", {get_desc(lighting, self.LIGHTINGS)}"
        if mood != "-":
            prompt += f", {get_desc(mood, self.MOODS)}"
        if vegetation != "-":
            prompt += f", {get_desc(vegetation, self.VEGETATIONS)}"
        if sky_element != "-":
            prompt += f", {get_desc(sky_element, self.SKY_ELEMENTS)}"

        style_desc = get_desc(style, self.STYLES)
        prompt += f", {style_desc}"

        prompt += ", highly detailed, cinematic composition"

        return (prompt,)