# gui/main_window.py

import customtkinter as ctk
from typing import Optional
import sys
import os

# Set appearance mode and default color theme
ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"


class VerbiMainWindow(ctk.CTk):
    """
    Main window for Verbi voice assistant GUI.
    """

    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Verbi - Voice Assistant")
        self.geometry("900x700")
        self.minsize(700, 500)

        # Center window on screen
        self.center_window()

        # Configure grid layout (3 rows: header, chat, controls)
        self.grid_rowconfigure(1, weight=1)  # Chat area expands
        self.grid_columnconfigure(0, weight=1)

        # Create UI sections
        self.create_header()
        self.create_chat_area()
        self.create_controls()

        # Bind close event
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def center_window(self):
        """Center the window on the screen."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def create_header(self):
        """Create the header section with title and settings."""
        header_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        header_frame.grid_columnconfigure(1, weight=1)

        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="Verbi",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title_label.grid(row=0, column=0, sticky="w")

        # Status indicator
        self.status_label = ctk.CTkLabel(
            header_frame,
            text="Ready",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        self.status_label.grid(row=0, column=1, sticky="e", padx=(0, 10))

        # Settings button (placeholder for now)
        settings_btn = ctk.CTkButton(
            header_frame,
            text="⚙",
            font=ctk.CTkFont(size=20),
            width=40,
            height=40,
            command=self.open_settings
        )
        settings_btn.grid(row=0, column=2, sticky="e")

    def create_chat_area(self):
        """Create the main chat display area."""
        # Chat container
        chat_container = ctk.CTkFrame(self, corner_radius=10)
        chat_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        chat_container.grid_rowconfigure(0, weight=1)
        chat_container.grid_columnconfigure(0, weight=1)

        # Scrollable frame for messages
        self.chat_scroll = ctk.CTkScrollableFrame(
            chat_container,
            corner_radius=10,
            fg_color="transparent"
        )
        self.chat_scroll.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.chat_scroll.grid_columnconfigure(0, weight=1)

        # Welcome message
        self.add_welcome_message()

    def add_welcome_message(self):
        """Add a welcome message to the chat."""
        welcome_frame = ctk.CTkFrame(self.chat_scroll, fg_color="transparent")
        welcome_frame.grid(row=0, column=0, pady=20, sticky="ew")

        welcome_text = ctk.CTkLabel(
            welcome_frame,
            text="👋 Welcome to Verbi!\n\nClick the microphone button below to start talking.",
            font=ctk.CTkFont(size=16),
            text_color="gray",
            justify="center"
        )
        welcome_text.pack(expand=True)

    def create_controls(self):
        """Create the control buttons section."""
        controls_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        controls_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(10, 20))
        controls_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Clear conversation button
        clear_btn = ctk.CTkButton(
            controls_frame,
            text="Clear",
            font=ctk.CTkFont(size=14),
            width=100,
            height=40,
            fg_color="gray30",
            hover_color="gray20",
            command=self.clear_conversation
        )
        clear_btn.grid(row=0, column=0, padx=5)

        # Main microphone button (large, centered)
        self.mic_button = ctk.CTkButton(
            controls_frame,
            text="🎤",
            font=ctk.CTkFont(size=48),
            width=120,
            height=120,
            corner_radius=60,
            fg_color=["#3B8ED0", "#1F6AA5"],
            hover_color=["#36719F", "#144870"],
            command=self.toggle_recording
        )
        self.mic_button.grid(row=0, column=1, padx=5, pady=10)

        # Stop button
        self.stop_btn = ctk.CTkButton(
            controls_frame,
            text="Stop",
            font=ctk.CTkFont(size=14),
            width=100,
            height=40,
            fg_color="gray30",
            hover_color="gray20",
            command=self.stop_action,
            state="disabled"
        )
        self.stop_btn.grid(row=0, column=2, padx=5)

    def toggle_recording(self):
        """Toggle audio recording (placeholder)."""
        current_state = self.mic_button.cget("text")
        if current_state == "🎤":
            # Start recording
            self.mic_button.configure(text="⏸", fg_color="red")
            self.stop_btn.configure(state="normal")
            self.update_status("Listening...")
            print("Recording started...")  # Placeholder
        else:
            # Stop recording
            self.mic_button.configure(text="🎤", fg_color=["#3B8ED0", "#1F6AA5"])
            self.stop_btn.configure(state="disabled")
            self.update_status("Processing...")
            print("Recording stopped...")  # Placeholder

    def stop_action(self):
        """Stop current action (recording/playback)."""
        self.mic_button.configure(text="🎤", fg_color=["#3B8ED0", "#1F6AA5"])
        self.stop_btn.configure(state="disabled")
        self.update_status("Ready")
        print("Action stopped")  # Placeholder

    def clear_conversation(self):
        """Clear the conversation history."""
        # Remove all widgets from chat scroll
        for widget in self.chat_scroll.winfo_children():
            widget.destroy()

        # Add welcome message back
        self.add_welcome_message()
        self.update_status("Conversation cleared")
        print("Conversation cleared")  # Placeholder

    def open_settings(self):
        """Open settings dialog (placeholder)."""
        print("Settings clicked")  # Placeholder
        # TODO: Open settings window in Phase 4

    def update_status(self, message: str):
        """Update the status label."""
        self.status_label.configure(text=message)

    def on_closing(self):
        """Handle window close event."""
        print("Closing application...")
        self.quit()
        self.destroy()


def main():
    """Main entry point for the GUI application."""
    app = VerbiMainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
