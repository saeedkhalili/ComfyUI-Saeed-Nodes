# landscape_prompt_generator.py
# تولید پرامپت منظره – بدون سبک

class LandscapePromptGenerator:
    """نود تولید پرامپت منظره پس‌زمینه"""

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
        ("🏙️ City", "modern city skyline with tall buildings"),
        ("🏘️ Village", "picturesque village with rustic houses and narrow streets"),
        ("🏚️ Dystopian Ruins", "dystopian ruined city with decaying structures"),
        ("🧙 Fantasy Realm", "fantasy realm with magical elements"),
        ("🏖️ Coastal Beach", "sandy beach with ocean waves"),
        ("🕳️ Cave", "dark cave interior with stalactites"),
        ("🐊 Swamp", "murky swamp with twisted trees and water"),
        ("🌸 Meadow", "colorful flower meadow under open sky"),
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

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "landscape_type": ([d for d, _ in cls.LANDSCAPES],),
                "mood": ([d for d, _ in cls.MOODS], {"default": "-"}),
                "vegetation": ([d for d, _ in cls.VEGETATIONS], {"default": "-"}),
                "sky_element": ([d for d, _ in cls.SKY_ELEMENTS], {"default": "-"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("landscape_prompt",)
    FUNCTION = "generate_prompt"
    CATEGORY = "Saeed"

    def generate_prompt(self, landscape_type, mood, vegetation, sky_element):
        def get_desc(display, source_list):
            for d, desc in source_list:
                if d == display:
                    return desc
            return ""

        prompt = f"Background landscape: {get_desc(landscape_type, self.LANDSCAPES)}"

        if mood != "-":
            prompt += f", {get_desc(mood, self.MOODS)}"
        if vegetation != "-":
            prompt += f", {get_desc(vegetation, self.VEGETATIONS)}"
        if sky_element != "-":
            prompt += f", {get_desc(sky_element, self.SKY_ELEMENTS)}"

        prompt += ", highly detailed, cinematic composition"

        return (prompt,)