# camera_movement_selector.py
# انتخاب حرکت دوربین برای ویدئو

class CameraMovementSelector:
    """نود انتخاب حرکت دوربین – مخصوص ویدئو"""

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
                "movement": ([d for d, _ in cls.MOVEMENT_TYPES], {"default": "-"}),
                "camera_turn": (cls.CAMERA_TURNS, {"default": "-"}),
                "camera_shake": (cls.CAMERA_SHAKES, {"default": "-"}),
                "speed": (cls.SPEEDS, {"default": "-"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("camera_movement_prompt",)
    FUNCTION = "generate_prompt"
    CATEGORY = "Saeed"

    def generate_prompt(self, movement, camera_turn, camera_shake, speed):
        def get_desc(display, source_list):
            for d, desc in source_list:
                if d == display:
                    return desc
            return ""

        if movement == "-":
            return ("Static shot, no camera movement",)

        prompt = f"Camera movement: {get_desc(movement, self.MOVEMENT_TYPES)}"
        if camera_turn != "-":
            prompt += f", Turn: {camera_turn}"
        if camera_shake != "-":
            prompt += f", Shake: {camera_shake}"
        if speed != "-":
            prompt += f", Speed: {speed}"

        return (prompt,)