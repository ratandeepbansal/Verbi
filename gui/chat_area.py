# gui/chat_area.py

import customtkinter as ctk
from datetime import datetime
from typing import Literal


class MessageBubble(ctk.CTkFrame):
    """
    A message bubble widget for displaying user or assistant messages.
    """

    def __init__(
        self,
        master,
        message: str,
        sender: Literal["user", "assistant"],
        timestamp: str = None,
        **kwargs
    ):
        """
        Initialize a message bubble.

        Args:
            master: Parent widget
            message: The message text to display
            sender: Either "user" or "assistant"
            timestamp: Optional timestamp string. If None, current time is used
        """
        super().__init__(master, **kwargs)

        self.message = message
        self.sender = sender
        self.timestamp = timestamp or datetime.now().strftime("%I:%M %p")

        # Configure colors based on sender
        if sender == "user":
            self.fg_color = ["#3B8ED0", "#1F6AA5"]  # Blue for user
            self.text_color = "white"
            self.anchor = "e"  # Align to right
        else:  # assistant
            self.fg_color = ["gray75", "gray30"]  # Gray for assistant
            self.text_color = ["gray10", "white"]
            self.anchor = "w"  # Align to left

        self.configure(fg_color=self.fg_color, corner_radius=15)
        self.grid_columnconfigure(0, weight=1)

        self._create_widgets()

    def _create_widgets(self):
        """Create the internal widgets for the message bubble."""
        # Message text
        message_label = ctk.CTkLabel(
            self,
            text=self.message,
            font=ctk.CTkFont(size=14),
            text_color=self.text_color,
            wraplength=400,
            justify="left",
            anchor="w"
        )
        message_label.grid(row=0, column=0, sticky="w", padx=15, pady=(12, 5))

        # Timestamp
        timestamp_label = ctk.CTkLabel(
            self,
            text=self.timestamp,
            font=ctk.CTkFont(size=10),
            text_color=self.text_color if self.sender == "user" else "gray50",
        )
        timestamp_label.grid(row=1, column=0, sticky="e", padx=15, pady=(0, 8))


class ChatArea(ctk.CTkScrollableFrame):
    """
    A scrollable chat area that manages message bubbles.
    """

    def __init__(self, master, **kwargs):
        """Initialize the chat area."""
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.message_count = 0

    def add_message(
        self,
        message: str,
        sender: Literal["user", "assistant"],
        timestamp: str = None
    ):
        """
        Add a message bubble to the chat area.

        Args:
            message: The message text
            sender: Either "user" or "assistant"
            timestamp: Optional timestamp string
        """
        # Create container frame for alignment
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.grid(row=self.message_count, column=0, sticky="ew", pady=5, padx=10)
        container.grid_columnconfigure(0, weight=1)

        # Create message bubble
        bubble = MessageBubble(
            container,
            message=message,
            sender=sender,
            timestamp=timestamp
        )

        # Align bubble based on sender
        if sender == "user":
            bubble.grid(row=0, column=0, sticky="e", padx=(100, 0))
        else:  # assistant
            bubble.grid(row=0, column=0, sticky="w", padx=(0, 100))

        self.message_count += 1

        # Auto-scroll to bottom
        self.after(100, self._scroll_to_bottom)

    def _scroll_to_bottom(self):
        """Scroll to the bottom of the chat area."""
        self._parent_canvas.yview_moveto(1.0)

    def clear_messages(self):
        """Remove all messages from the chat area."""
        for widget in self.winfo_children():
            widget.destroy()
        self.message_count = 0

    def add_system_message(self, message: str):
        """
        Add a centered system message (e.g., welcome message, status updates).

        Args:
            message: The system message text
        """
        system_frame = ctk.CTkFrame(self, fg_color="transparent")
        system_frame.grid(row=self.message_count, column=0, pady=15, sticky="ew")
        system_frame.grid_columnconfigure(0, weight=1)

        system_label = ctk.CTkLabel(
            system_frame,
            text=message,
            font=ctk.CTkFont(size=14),
            text_color="gray",
            justify="center"
        )
        system_label.grid(row=0, column=0)

        self.message_count += 1
        self.after(100, self._scroll_to_bottom)
