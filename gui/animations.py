# gui/animations.py

import customtkinter as ctk
import math
from typing import Literal
from gui.theme import NeonTheme, AnimationConfig


class PulsingIndicator(ctk.CTkFrame):
    """
    A pulsing circular indicator for the 'listening' state.
    """

    def __init__(self, master, size: int = 80, **kwargs):
        """
        Initialize the pulsing indicator.

        Args:
            master: Parent widget
            size: Size of the indicator in pixels
        """
        super().__init__(master, **kwargs)

        self.size = size
        self.is_animating = False
        self.animation_step = 0
        self.configure(fg_color="transparent")

        # Create canvas for custom drawing with black background
        self.canvas = ctk.CTkCanvas(
            self,
            width=size,
            height=size,
            bg=NeonTheme.BG_BLACK,
            highlightthickness=0
        )
        self.canvas.pack()

        # Create pulsing circle with neon green
        self.circle = self.canvas.create_oval(
            size // 4, size // 4,
            3 * size // 4, 3 * size // 4,
            fill=NeonTheme.STATUS_LISTENING,
            outline=NeonTheme.PRIMARY,
            width=2
        )

    def start(self):
        """Start the pulsing animation."""
        self.is_animating = True
        self._animate()

    def stop(self):
        """Stop the pulsing animation."""
        self.is_animating = False

    def _animate(self):
        """Perform one frame of the pulsing animation with smooth easing."""
        if not self.is_animating:
            return

        # Calculate smooth pulse scale with easing
        self.animation_step = (self.animation_step + 1) % 100
        # Use smoother sine wave for more elegant pulsing
        scale = 0.6 + 0.25 * math.sin(self.animation_step * 2 * math.pi / 100)

        # Update circle size
        center = self.size // 2
        radius = (self.size // 2) * scale

        self.canvas.coords(
            self.circle,
            center - radius, center - radius,
            center + radius, center + radius
        )

        # Schedule next frame with smoother timing (33ms ≈ 30fps)
        self.after(33, self._animate)


class SpinnerIndicator(ctk.CTkFrame):
    """
    A spinning loader indicator for the 'thinking' state.
    """

    def __init__(self, master, size: int = 40, **kwargs):
        """
        Initialize the spinner indicator.

        Args:
            master: Parent widget
            size: Size of the spinner in pixels
        """
        super().__init__(master, **kwargs)

        self.size = size
        self.is_animating = False
        self.angle = 0
        self.configure(fg_color="transparent")

        # Create label with spinning character in neon purple
        self.label = ctk.CTkLabel(
            self,
            text="⟳",
            font=ctk.CTkFont(size=size),
            text_color=NeonTheme.STATUS_THINKING
        )
        self.label.pack()

    def start(self):
        """Start the spinning animation."""
        self.is_animating = True
        self._animate()

    def stop(self):
        """Stop the spinning animation."""
        self.is_animating = False

    def _animate(self):
        """Perform one frame of the spinning animation with smooth timing."""
        if not self.is_animating:
            return

        # Rotate through different spinner characters
        spinners = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.angle = (self.angle + 1) % len(spinners)
        self.label.configure(text=spinners[self.angle])

        # Schedule next frame with smoother timing (80ms for readable character cycling)
        self.after(80, self._animate)


class WaveIndicator(ctk.CTkFrame):
    """
    An animated wave indicator for the 'speaking' state.
    """

    def __init__(self, master, width: int = 100, height: int = 40, **kwargs):
        """
        Initialize the wave indicator.

        Args:
            master: Parent widget
            width: Width of the wave in pixels
            height: Height of the wave in pixels
        """
        super().__init__(master, **kwargs)

        self.width = width
        self.height = height
        self.is_animating = False
        self.animation_step = 0
        self.configure(fg_color="transparent")

        # Create container for wave bars
        self.bars_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.bars_frame.pack()

        # Create 5 bars with neon cyan theme
        self.bars = []
        for i in range(5):
            bar = ctk.CTkProgressBar(
                self.bars_frame,
                width=10,
                height=height,
                orientation="vertical",
                progress_color=NeonTheme.STATUS_SPEAKING,  # Neon cyan
                fg_color=NeonTheme.BG_SURFACE  # Dark gray background
            )
            bar.grid(row=0, column=i, padx=3)
            bar.set(0.3)
            self.bars.append(bar)

    def start(self):
        """Start the wave animation."""
        self.is_animating = True
        self._animate()

    def stop(self):
        """Stop the wave animation."""
        self.is_animating = False
        # Reset all bars to default height
        for bar in self.bars:
            bar.set(0.3)

    def _animate(self):
        """Perform one frame of the wave animation with smooth, elegant motion."""
        if not self.is_animating:
            return

        self.animation_step = (self.animation_step + 1) % 60

        # Update each bar height with a smooth wave pattern
        for i, bar in enumerate(self.bars):
            # Create phase offset for wave effect across bars
            offset = i * math.pi / 4
            # Smooth sine wave with elegant easing
            height = 0.25 + 0.6 * abs(math.sin(self.animation_step * math.pi / 30 + offset))
            bar.set(height)

        # Schedule next frame with smoother timing (50ms ≈ 20fps for fluid wave motion)
        self.after(50, self._animate)


class StatusIndicator(ctk.CTkFrame):
    """
    A compound status indicator that shows different animations based on state.
    """

    def __init__(self, master, **kwargs):
        """Initialize the status indicator."""
        super().__init__(master, **kwargs)

        self.configure(fg_color="transparent")
        self.current_state: Literal["idle", "listening", "thinking", "speaking"] = "idle"

        # Create all indicators (only one will be visible at a time)
        self.pulsing = PulsingIndicator(self, size=60)
        self.spinner = SpinnerIndicator(self, size=40)
        self.wave = WaveIndicator(self, width=100, height=40)

        # Hide all initially
        self.pulsing.pack_forget()
        self.spinner.pack_forget()
        self.wave.pack_forget()

    def set_state(self, state: Literal["idle", "listening", "thinking", "speaking"]):
        """
        Set the current state and update the animation.

        Args:
            state: The state to display ("idle", "listening", "thinking", "speaking")
        """
        # Stop all animations
        self.pulsing.stop()
        self.spinner.stop()
        self.wave.stop()

        # Hide all indicators
        self.pulsing.pack_forget()
        self.spinner.pack_forget()
        self.wave.pack_forget()

        self.current_state = state

        # Show and start appropriate indicator
        if state == "listening":
            self.pulsing.pack(pady=10)
            self.pulsing.start()
        elif state == "thinking":
            self.spinner.pack(pady=10)
            self.spinner.start()
        elif state == "speaking":
            self.wave.pack(pady=10)
            self.wave.start()
        # For "idle", nothing is shown
