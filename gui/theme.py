"""
VoxVibe Neon Theme Configuration
A cyberpunk-inspired dark theme with neon green accents
"""

class NeonTheme:
    """Neon color scheme for VoxVibe"""

    # ===== PRIMARY COLORS =====
    PRIMARY = "#00FF41"          # Neon Green (Matrix-style)
    PRIMARY_HOVER = "#00CC34"    # Darker green for hover
    PRIMARY_GLOW = "#00FF4166"   # Semi-transparent for glow effects

    # ===== SECONDARY COLORS =====
    SECONDARY_CYAN = "#00FFFF"   # Neon Cyan for accents
    SECONDARY_PINK = "#FF006E"   # Neon Pink for warnings/errors
    SECONDARY_PURPLE = "#9D00FF" # Neon Purple for info
    SECONDARY_BLUE = "#0080FF"   # Neon Blue for links

    # ===== BACKGROUND COLORS =====
    BG_BLACK = "#000000"         # Pure black
    BG_SURFACE = "#0A0A0A"       # Very dark gray for surfaces
    BG_ELEVATED = "#141414"      # Slightly lighter for elevated elements
    BG_CHAT = "#050505"          # Chat area background

    # ===== TEXT COLORS =====
    TEXT_PRIMARY = "#FFFFFF"     # Pure white
    TEXT_SECONDARY = "#AAAAAA"   # Light gray
    TEXT_MUTED = "#666666"       # Muted gray
    TEXT_NEON = "#00FF41"        # Neon green text

    # ===== MESSAGE BUBBLE COLORS =====
    USER_BUBBLE = "#0D1F0D"      # Dark green for user messages
    USER_BORDER = "#00FF41"      # Neon green border
    ASSISTANT_BUBBLE = "#0A0A0A" # Very dark gray for assistant
    ASSISTANT_BORDER = "#00FFFF" # Cyan border

    # ===== STATUS INDICATOR COLORS =====
    STATUS_LISTENING = "#00FF41"  # Neon green (pulsing)
    STATUS_THINKING = "#9D00FF"   # Neon purple (spinning)
    STATUS_SPEAKING = "#00FFFF"   # Neon cyan (wave)
    STATUS_IDLE = "#333333"       # Dark gray

    # ===== BUTTON COLORS =====
    BUTTON_PRIMARY = "#00FF41"
    BUTTON_PRIMARY_HOVER = "#00CC34"
    BUTTON_SECONDARY = "#1A1A1A"
    BUTTON_SECONDARY_HOVER = "#2A2A2A"
    BUTTON_DANGER = "#FF006E"
    BUTTON_DANGER_HOVER = "#CC0058"

    # ===== BORDER & EFFECTS =====
    BORDER_DEFAULT = "#222222"
    BORDER_HOVER = "#00FF41"
    BORDER_FOCUS = "#00FFFF"
    SHADOW_COLOR = "#00FF4133"   # Neon green shadow
    GLOW_COLOR = "#00FF4166"     # Glow effect

    # ===== GRADIENT COLORS =====
    GRADIENT_START = "#000000"
    GRADIENT_MID = "#001a0d"     # Very dark green tint
    GRADIENT_END = "#000a14"     # Very dark cyan tint

    # ===== TRANSPARENCY VALUES =====
    BLUR_OPACITY = 0.6           # For glassmorphism
    OVERLAY_OPACITY = 0.3        # For overlays

    @classmethod
    def get_gradient_bg(cls):
        """Returns gradient background for chat area"""
        return f"linear-gradient(135deg, {cls.GRADIENT_START} 0%, {cls.GRADIENT_MID} 50%, {cls.GRADIENT_END} 100%)"

    @classmethod
    def get_glow_shadow(cls, color=None):
        """Returns box shadow for glow effect"""
        glow_color = color or cls.PRIMARY
        return f"0 0 10px {glow_color}, 0 0 20px {glow_color}66, 0 0 30px {glow_color}33"

    @classmethod
    def get_message_gradient(cls, is_user=True):
        """Returns gradient for message bubbles"""
        if is_user:
            return f"linear-gradient(135deg, {cls.USER_BUBBLE} 0%, #0a1a0a 100%)"
        else:
            return f"linear-gradient(135deg, {cls.ASSISTANT_BUBBLE} 0%, #0f0f0f 100%)"


class AnimationConfig:
    """Animation timing and easing configurations"""

    # ===== TIMING =====
    FAST = 150          # 150ms for quick transitions
    NORMAL = 300        # 300ms for standard transitions
    SLOW = 500          # 500ms for emphasis

    # ===== EASING FUNCTIONS =====
    EASE_IN_OUT = "ease-in-out"
    EASE_OUT = "ease-out"
    EASE_IN = "ease-in"
    ELASTIC = "cubic-bezier(0.68, -0.55, 0.265, 1.55)"
    SMOOTH = "cubic-bezier(0.4, 0.0, 0.2, 1)"

    # ===== STATUS ANIMATIONS =====
    PULSE_DURATION = 2000    # 2s for pulse animation
    SPIN_DURATION = 1500     # 1.5s for spin animation
    WAVE_DURATION = 1800     # 1.8s for wave animation

    # ===== GLOW ANIMATIONS =====
    GLOW_DURATION = 2500     # 2.5s for glow pulse
    GLOW_INTENSITY_MIN = 0.5
    GLOW_INTENSITY_MAX = 1.0


class LayoutConfig:
    """Layout and spacing configurations"""

    # ===== SPACING =====
    SPACE_XS = 4
    SPACE_SM = 8
    SPACE_MD = 16
    SPACE_LG = 24
    SPACE_XL = 32

    # ===== BORDER RADIUS =====
    RADIUS_SM = 4
    RADIUS_MD = 8
    RADIUS_LG = 12
    RADIUS_XL = 16
    RADIUS_PILL = 9999

    # ===== BLUR =====
    BLUR_SM = 5
    BLUR_MD = 10
    BLUR_LG = 20
