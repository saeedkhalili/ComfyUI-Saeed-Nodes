import torch

class CinematicAspectRatioSelector:
    """
    A self-contained node that selects cinematic aspect ratios,
    scales resolution by a quality factor (K), rounds to multiples of 8,
    and outputs an empty latent along with name, width, height.
    No other custom nodes required.
    """

    ASPECTS = {
        "Ultra Panavision Landscape":(4096, 1484),
        "Anamorphic Landscape":      (4096, 1743),
        "HD Landscape":              (4096, 2304),
        "NTSC Landscape":            (4096, 2731),
        "Square Size":               (4096, 4096),
        "NTSC Portrait":             (2731, 4096),
        "HD Portrait":               (2304, 4096),
        "Anamorphic Portrait":       (1743, 4096),
    }
    RATIO_NAMES = list(ASPECTS.keys())
    ROUND_TO = 8

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "aspect_ratio": (cls.RATIO_NAMES,),
                "quality_k":    ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 10.0,
                    "step": 0.1,
                    "display": "Quality (K)"
                }),
            }
        }

    RETURN_TYPES = ("STRING", "INT", "INT", "LATENT")
    RETURN_NAMES = ("name", "width", "height", "latent")
    FUNCTION = "select"
    CATEGORY = "Saeed"          # <-- دسته‌ی اختصاصی شما

    def select(self, aspect_ratio, quality_k):
        base_w, base_h = self.ASPECTS[aspect_ratio]

        def calc_dim(base, k):
            scaled = (base / 4.0) * k
            return int((- (scaled // -self.ROUND_TO)) * self.ROUND_TO)

        w = calc_dim(base_w, quality_k)
        h = calc_dim(base_h, quality_k)

        latent = torch.zeros([1, 4, h // 8, w // 8])
        return (aspect_ratio, w, h, {"samples": latent})