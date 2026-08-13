# negative_prompt_generator.py
# یک نود برای تولید سریع پرامپت منفی دسته‌بندی‌شده

class NegativePromptGenerator:
    """نود تولید پرامپت منفی – فعال‌سازی گروه‌های کلمات با یک کلیک"""

    # هر دسته شامل یک لیست از کلمات منفی است
    NOISE_WORDS = "low quality, blurry, noisy, grainy, compression artifacts, pixelation, jpeg artifacts, overexposed, underexposed, chromatic aberration, moiré, ringing, aliasing, banding, posterization, haze"

    HUMAN_ANATOMY_WORDS = "extra fingers, missing fingers, fused fingers, deformed hands, extra limbs, missing limbs, bad anatomy, bad proportions, disfigured face, broken wrist, twisted body, mutated, deformed, asymmetrical, cross-eyed, lazy eye"

    REMOVE_HUMANS_WORDS = "no humans, nobody, no people, no person, no man, no woman, no child, empty scene, no pedestrians, no crowd, no silhouettes, no hands, no faces"

    QUALITY_ARTIFACTS_WORDS = "watermark, signature, text, logo, username, frame, border, cropped, out of frame, duplicate, multiple views, split screen, collage, grid, repeated pattern, cluttered, busy background, messy"

    STYLE_NEGATIVES_WORDS = "black and white, monochrome, cartoon, anime, 3d render, painting, illustration, sketch, low poly, lowres, pixel art, plastic, doll, wax, oversaturated"

    LIGHTING_ISSUES_WORDS = "harsh shadows, flat lighting, underexposed, overexposed, lens flare, glare, reflections, uneven lighting, unnatural light"

    COMPOSITION_ISSUES_WORDS = "bad composition, tilted horizon, cramped, negative space, awkward framing, distorted perspective, weird clouds, unnatural colors"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                # دسته‌های قابل انتخاب
                "🔊 Noise / Artifacts": ("BOOLEAN", {"default": False}),
                "🧍 Human Anatomy Issues": ("BOOLEAN", {"default": False}),
                "🚫 Remove Humans": ("BOOLEAN", {"default": False}),
                "🖼️ Quality / Text / Watermark": ("BOOLEAN", {"default": False}),
                "🌑 Style Negatives (cartoon/painting/3D)": ("BOOLEAN", {"default": False}),
                "💡 Lighting Issues": ("BOOLEAN", {"default": False}),
                "📐 Composition / Framing": ("BOOLEAN", {"default": False}),
                # متن دلخواه برای افزودن کلمات منفی اضافی
                "✏️ Custom Negative Words": ("STRING", {"default": "", "multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("negative_prompt",)
    FUNCTION = "generate_prompt"
    CATEGORY = "Saeed"

    def generate_prompt(self, **kwargs):
        negative_parts = []

        # اگر تیک هر دسته فعال باشد، کلمات همان دسته اضافه می‌شود
        if kwargs.get("🔊 Noise / Artifacts", False):
            negative_parts.append(self.NOISE_WORDS)

        if kwargs.get("🧍 Human Anatomy Issues", False):
            negative_parts.append(self.HUMAN_ANATOMY_WORDS)

        if kwargs.get("🚫 Remove Humans", False):
            negative_parts.append(self.REMOVE_HUMANS_WORDS)

        if kwargs.get("🖼️ Quality / Text / Watermark", False):
            negative_parts.append(self.QUALITY_ARTIFACTS_WORDS)

        if kwargs.get("🌑 Style Negatives (cartoon/painting/3D)", False):
            negative_parts.append(self.STYLE_NEGATIVES_WORDS)

        if kwargs.get("💡 Lighting Issues", False):
            negative_parts.append(self.LIGHTING_ISSUES_WORDS)

        if kwargs.get("📐 Composition / Framing", False):
            negative_parts.append(self.COMPOSITION_ISSUES_WORDS)

        # اضافه کردن کلمات سفارشی کاربر
        custom_words = kwargs.get("✏️ Custom Negative Words", "").strip()
        if custom_words:
            negative_parts.append(custom_words)

        # ترکیب همه با ویرگول
        final_negative = ", ".join(negative_parts)

        return (final_negative,)