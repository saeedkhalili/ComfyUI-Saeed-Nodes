# cinematic_camera_selector.py
# انتخاب دوربین برای تصویر – بدون حرکت

class CameraSelector:
    """
    نود انتخاب دوربین برای تصویرسازی
    شامل زاویه، اندازه شات، موقعیت و لنز
    """
    ANGLES = [
        ("🎥 Straight-on angle", "camera directly facing the subject"),
        ("👁️ Eye-level", "camera at the subject's eye level"),
        ("🔽 High angle", "looking down from above the subject"),
        ("🔼 Low angle", "looking up from below the subject"),
        ("🦅 Bird's-eye view", "directly overhead, like a bird looking down"),
        ("⬇️ Top-down shot", "flat overhead view, like a map"),
        ("🪱 Worm's-eye view", "extreme low angle looking straight up"),
        ("📐 Dutch angle", "canted/tilted angle for a dynamic or uneasy feeling"),
        ("👤 Profile shot", "side view of the subject"),
        ("🔄 Three-quarter view", "subject at a 45-degree angle to camera"),
        ("🔙 Rear view", "from behind the subject"),
        ("👥 Over-the-shoulder (OTS)", "over the shoulder of a foreground character"),
        ("👀 Point of View (POV)", "as if seen through the character's eyes"),
        ("🚁 Overhead shot", "high aerial view, looking down from a distance"),
    ]
    SHOTS = [
        ("🌌 Extreme Wide Shot (EWS)", "subject very small in frame, vast environment visible"),
        ("🏞️ Wide Shot (WS)", "full subject and surroundings"),
        ("🧍 Full Shot (FS)", "entire subject from head to toe"),
        ("🧍‍♂️ Medium Full Shot (MFS)", "subject from knees up"),
        ("👤 Medium Shot (MS)", "subject from waist up"),
        ("🧑 Medium Close-Up (MCU)", "chest and head"),
        ("😃 Close-Up (CU)", "face or detail fills the frame"),
        ("🔍 Extreme Close-Up (ECU)", "only a specific part, e.g. eyes or lips"),
    ]
    POSITIONS = [
        ("⬆️ Front view", "subject facing the camera"),
        ("⬅️ Left side view", "showing the subject's left side"),
        ("➡️ Right side view", "showing the subject's right side"),
        ("⬇️ Back view", "subject seen from behind"),
        ("🔼 Top view", "looking straight down"),
        ("🔽 Bottom view", "looking straight up"),
        ("↗️ Three-quarter front view", "45-degree angle from the front"),
        ("↙️ Three-quarter rear view", "45-degree angle from the rear"),
    ]
    LENSES = [
        ("10mm", "10mm ultra‑wide lens"),
        ("14mm", "14mm ultra‑wide lens"),
        ("18mm", "18mm ultra‑wide lens"),
        ("24mm", "24mm wide lens"),
        ("28mm", "28mm wide lens"),
        ("35mm", "35mm wide lens"),
        ("50mm", "50mm standard lens"),
        ("65mm", "65mm standard lens"),
        ("85mm", "85mm short telephoto lens"),
        ("100mm", "100mm short telephoto lens"),
        ("135mm", "135mm telephoto lens"),
        ("200mm", "200mm telephoto lens"),
    ]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "camera_angle": ([d for d, _ in cls.ANGLES],),
                "shot_size": ([d for d, _ in cls.SHOTS],),
                "position": ([d for d, _ in cls.POSITIONS],),
                "lens": ([d for d, _ in cls.LENSES], {"default": "50mm"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("camera_prompt",)
    FUNCTION = "generate_prompt"
    CATEGORY = "Saeed"

    def generate_prompt(self, camera_angle, shot_size, position, lens):
        def get_desc(display, source_list):
            for d, desc in source_list:
                if d == display:
                    return desc
            return ""

        prompt = (
            f"Camera angle: {get_desc(camera_angle, self.ANGLES)}, "
            f"Shot: {get_desc(shot_size, self.SHOTS)}, "
            f"Position: {get_desc(position, self.POSITIONS)}, "
            f"Lens: {get_desc(lens, self.LENSES)}"
        )
        return (prompt,)