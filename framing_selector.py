# framing_selector.py
# نود انتخاب قاب‌بندی و کمپوزیشن

class FramingSelector:
    """نود انتخاب قاب‌بندی و ترکیب‌بندی تصویر"""

    FRAMING_TYPES = [
        ("Rule of Thirds", "subject placed at a rule-of-thirds intersection"),
        ("Centered", "subject centered in frame"),
        ("Golden Ratio", "composition following golden ratio spiral"),
        ("Symmetrical", "perfectly symmetrical composition"),
        ("Diagonal", "strong diagonal lines across the frame"),
        ("Frame within Frame", "subject framed by foreground elements"),
        ("Leading Lines", "leading lines guiding the eye to the subject"),
        ("Negative Space", "large negative space around subject"),
        ("Wide Angle", "expansive wide-angle composition"),
        ("Close-Up", "intimate close-up framing"),
        ("Over-the-Shoulder", "framed over a foreground character's shoulder"),
    ]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "framing": ([d for d, _ in cls.FRAMING_TYPES],),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("framing_prompt",)
    FUNCTION = "generate_prompt"
    CATEGORY = "Saeed"

    def generate_prompt(self, framing):
        def get_desc(display, source_list):
            for d, desc in source_list:
                if d == display:
                    return desc
            return ""

        prompt = f"Framing: {get_desc(framing, self.FRAMING_TYPES)}"
        return (prompt,)