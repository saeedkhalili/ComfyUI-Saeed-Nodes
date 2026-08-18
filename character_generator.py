# character_generator.py
# تولید پرامپت شخصیت

class CharacterGenerator:
    """نود تولید مشخصات کاراکتر"""

    GENDERS = [
        ("👨 Male", "male"),
        ("👩 Female", "female"),
        ("🧑 Non-binary", "non-binary"),
        ("🤖 Robot", "robot"),
        ("👽 Alien", "alien"),
    ]
    AGES = [
        ("👶 Baby", "baby"),
        ("🧒 Child", "child"),
        ("🧑 Teenager", "teenager"),
        ("👨 Adult", "adult"),
        ("🧓 Elder", "elder"),
    ]
    CLOTHING = [
        ("👕 Casual", "casual clothing"),
        ("👔 Formal", "formal attire"),
        ("🧥 Winter coat", "winter coat"),
        ("👗 Dress", "dress"),
        ("🥻 Traditional", "traditional clothing"),
        ("🦸 Superhero", "superhero suit"),
        ("🥋 Martial arts", "martial arts uniform"),
        ("👘 Kimono", "kimono"),
        ("🎭 Masked", "wearing a mask"),
        ("🧕 Hijab", "wearing hijab"),
    ]
    DECADES = [
        ("1900s", "1900s style"),
        ("1920s", "1920s style"),
        ("1950s", "1950s style"),
        ("1980s", "1980s style"),
        ("2000s", "2000s style"),
        ("2020s", "modern 2020s style"),
        ("Future", "futuristic style"),
    ]
    CLOTHING_COLOR_TEXTURE = [
        ("-", ""),
        ("Colorful", "colorful clothing"),
        ("White", "white clothing"),
        ("Black", "black clothing"),
        ("Denim", "denim fabric"),
        ("Shiny / Glossy", "shiny glossy clothing"),
        ("Matte", "matte fabric clothing"),
        ("Patterned", "patterned clothing"),
        ("Pastel", "pastel clothing"),
        ("Earth tones", "earth-toned clothing"),
        ("Metallic", "metallic clothing"),
        ("Translucent", "translucent clothing"),
    ]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "gender": ([d for d, _ in cls.GENDERS],),
                "age": ([d for d, _ in cls.AGES],),
                "clothing": ([d for d, _ in cls.CLOTHING],),
                "clothing_color_texture": ([d for d, _ in cls.CLOTHING_COLOR_TEXTURE], {"default": "-"}),
                "decade": ([d for d, _ in cls.DECADES],),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("character_prompt",)
    FUNCTION = "generate_prompt"
    CATEGORY = "Saeed"

    def generate_prompt(self, gender, age, clothing, clothing_color_texture, decade):
        def get_desc(display, source_list):
            for d, desc in source_list:
                if d == display:
                    return desc
            return ""

        prompt = (
            f"Character: {get_desc(gender, self.GENDERS)}, "
            f"{get_desc(age, self.AGES)}, "
            f"wearing {get_desc(clothing, self.CLOTHING)}"
        )

        if clothing_color_texture != "-":
            prompt += f", clothing color/texture: {get_desc(clothing_color_texture, self.CLOTHING_COLOR_TEXTURE)}"

        prompt += f", {get_desc(decade, self.DECADES)}"

        return (prompt,)