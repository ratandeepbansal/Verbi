# gui/animations.py

import customtkinter as ctk
import math
from typing import Literal


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

        # Create canvas for custom drawing
        self.canvas = ctk.CTkCanvas(
            self,
            width=size,
            height=size,
            bg=self._apply_appearance_mode(ctk.ThemeManager.theme["CTkFrame"]["fg_color"]),
            highlightthickness=0
        )
        self.canvas.pack()

        # Create pulsing circle
        self.circle = self.canvas.create_oval(
            size // 4, size // 4,
            3 * size // 4, 3 * size // 4,
            fill="#3B8ED0",
            outline=""
        )

    def start(self):
        """Start the pulsing animation."""
        self.is_animating = True
        self._animate()

    def stop(self):
        """Stop the pulsing animation."""
        self.is_animating = False

    def _animate(self):
        """Perform one frame of the pulsing animation."""
        if not self.is_animating:
            return

        # Calculate pulse scale
        self.animation_step = (self.animation_step + 1) % 60
        scale = 0.5 + 0.3 * math.sin(self.animation_step * math.pi / 30)

        # Update circle size
        center = self.size // 2
        radius = (self.size // 2) * scale

        self.canvas.coords(
            self.circle,
            center - radius, center - radius,
            center + radius, center + radius
        )

        # Schedule next frame
        self.after(50, self._animate)


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

        # Create label with spinning character
        self.label = ctk.CTkLabel(
            self,
            text="⟳",
            font=ctk.CTkFont(size=size),
            text_color=["#3B8ED0", "#1F6AA5"]
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
        """Perform one frame of the spinning animation."""
        if not self.is_animating:
            return

        # Rotate through different spinner characters
        spinners = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.angle = (self.angle + 1) % len(spinners)
        self.label.configure(text=spinners[self.angle])

        # Schedule next frame
        self.after(100, self._animate)


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

        # Create 5 bars
        self.bars = []
        for i in range(5):
            bar = ctk.CTkProgressBar(
                self.bars_frame,
                width=10,
                height=height,
                orientation="vertical"
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
        """Perform one frame of the wave animation."""
        if not self.is_animating:
            return

        self.animation_step = (self.animation_step + 1) % 40

        # Update each bar height with a wave pattern
        for i, bar in enumerate(self.bars):
            offset = i * math.pi / 5
            height = 0.3 + 0.5 * abs(math.sin(self.animation_step * math.pi / 20 + offset))
            bar.set(height)

        # Schedule next frame
        self.after(80, self._animate)


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
