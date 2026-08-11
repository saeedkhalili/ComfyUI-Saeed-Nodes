class CameraSelector:
    """
    A node that generates a cinematic camera prompt.
    Selection lists include emojis for visual guidance (not in prompt output).
    Lens is a combo box with exact focal lengths.
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

    # Lens options (combo box for exact values)
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

    MOVEMENT_TYPES = [
        ("-", ""),
        ("➡️ Dolly In (push-in)", "Dolly In: camera moves closer to subject"),
        ("⬅️ Dolly Out (push-out)", "Dolly Out: camera moves away from subject"),
        ("🔄 Orbit Left (circles around)", "Orbit Left: camera circles around subject counter‑clockwise"),
        ("🔄 Orbit Right (circles around)", "Orbit Right: camera circles around subject clockwise"),
        ("⬆️ Pitch (overhead view)", "Pitch: camera tilts to an overhead view"),
        ("🤚 Handheld (handheld movement)", "Handheld: realistic shaky human‑held motion"),
        ("🚶 Tracking Shot (camera follows, tracks)", "Tracking Shot: camera follows the subject laterally"),
        ("⬆️ Crane Up (camera goes up)", "Crane Up: camera elevates"),
        ("⬇️ Crane Down (camera goes down)", "Crane Down: camera descends"),
        ("🚁 Drone View (overhead view, god's-eye)", "Drone View: aerial overhead perspective"),
        ("👥 Over-the-shoulder", "Over-the-shoulder: from behind a foreground character"),
    ]

    CAMERA_TURNS = ["-", "🌌 Expansive / Epic", "🔒 Intimate / Claustrophobic", "😐 Medium"]
    CAMERA_SHAKES = ["-", "🌊 smooth", "〰️ wiggly", "📳 shaky", "👾 glitchy", "💥 crash"]
    SPEEDS = [
        "-",
        "⏸️ freeze time (Freeze-frame — dramatic pause)",
        "🐌 Slow motion — dramatic emphasis (elements move slowly)",
        "🔄 Continuous shot — realism, unbroken take",
        "⚡ Fast motion (elements move fast)",
        "⏳ Time-lapse — passage of time",
    ]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "camera_angle": ([d for d, _ in cls.ANGLES],),
                "shot_size": ([d for d, _ in cls.SHOTS],),
                "position": ([d for d, _ in cls.POSITIONS],),
                "lens": ([d for d, _ in cls.LENSES], {"default": "50mm"}),
                "movement": ([d for d, _ in cls.MOVEMENT_TYPES], {"default": "-"}),
                "camera_turn": (cls.CAMERA_TURNS, {"default": "-"}),
                "camera_shake": (cls.CAMERA_SHAKES, {"default": "-"}),
                "speed": (cls.SPEEDS, {"default": "-"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("camera_prompt",)
    FUNCTION = "generate_prompt"
    CATEGORY = "Saeed"

    def generate_prompt(self, camera_angle, shot_size, position, lens,
                        movement, camera_turn, camera_shake, speed):
        def get_desc(display, source_list):
            for d, desc in source_list:
                if d == display:
                    return desc
            return ""

        # Static part
        angle_desc = get_desc(camera_angle, self.ANGLES)
        shot_desc = get_desc(shot_size, self.SHOTS)
        pos_desc = get_desc(position, self.POSITIONS)
        lens_desc = get_desc(lens, self.LENSES)   # already a description string

        prompt = (f"Camera angle: {angle_desc}, "
                  f"Shot: {shot_desc}, "
                  f"Position: {pos_desc}, "
                  f"Lens: {lens_desc}")

        # Dynamic part
        if movement != "-":
            move_desc = get_desc(movement, self.MOVEMENT_TYPES)
            prompt += f", Movement: {move_desc}"
            if camera_turn != "-":
                prompt += f", Turn: {camera_turn}"
            if camera_shake != "-":
                prompt += f", Shake: {camera_shake}"
            if speed != "-":
                prompt += f", Speed: {speed}"

        return (prompt,)