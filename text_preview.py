class TextPreview:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"source": ("*",)}}

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "preview"
    CATEGORY = "Saeed"
    OUTPUT_NODE = True

    def preview(self, source):
        text = str(source)
        return {"ui": {"text": [text]}, "result": (text,)}