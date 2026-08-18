# action_generator.py
# تولید پرامپت حالت/اکشن کاراکتر

class ActionGenerator:
    """نود تولید اکشن و حالت فیگور"""

    ACTIONS = [
        ("🧍 Standing", "standing"),
        ("🚶 Walking", "walking"),
        ("🏃 Running", "running"),
        ("🤸 Jumping", "jumping"),
        ("🥊 Fighting", "fighting"),
        ("💃 Dancing", "dancing"),
        ("🧘 Meditating", "meditating"),
        ("🛌 Lying", "lying down"),
        ("🙏 Kneeling", "kneeling"),
        ("🕴️ Floating", "floating"),
    ]
    EXPRESSIONS = [
        ("😐 Neutral", "neutral expression"),
        ("😊 Happy", "happy expression"),
        ("😢 Sad", "sad expression"),
        ("😠 Angry", "angry expression"),
        ("😨 Scared", "scared expression"),
        ("😲 Surprised", "surprised expression"),
        ("😏 Smirking", "smirking"),
        ("🤔 Thinking", "thinking expression"),
    ]
    BODY_ORIENTATIONS = [
        ("Front", "facing the camera"),
        ("Back", "facing away"),
        ("Side", "side profile"),
        ("Three-quarter", "three-quarter view"),
    ]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "action": ([d for d, _ in cls.ACTIONS],),
                "expression": ([d for d, _ in cls.EXPRESSIONS],),
                "orientation": ([d for d, _ in cls.BODY_ORIENTATIONS],),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("action_prompt",)
    FUNCTION = "generate_prompt"
    CATEGORY = "Saeed"

    def generate_prompt(self, action, expression, orientation):
        def get_desc(display, source_list):
            for d, desc in source_list:
                if d == display:
                    return desc
            return ""

        prompt = f"Action: {get_desc(action, self.ACTIONS)}, expression: {get_desc(expression, self.EXPRESSIONS)}, body orientation: {get_desc(orientation, self.BODY_ORIENTATIONS)}"
        return (prompt,)