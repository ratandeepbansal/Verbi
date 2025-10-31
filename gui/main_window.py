# gui/main_window.py

import customtkinter as ctk
from typing import Optional
import sys
import os
import logging
import tkinter as tk
from tkinter import filedialog
import json
from datetime import datetime

from gui.chat_area import ChatArea
from gui.animations import StatusIndicator
from gui.backend_controller import BackendController
from gui.settings_window import SettingsWindow
from gui.dialogs import ErrorDialog, ConfirmationDialog, AboutDialog
from gui.theme import NeonTheme, AnimationConfig

# Set appearance mode to dark for neon theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")  # Will be overridden by neon theme

logger = logging.getLogger(__name__)


class VerbiMainWindow(ctk.CTk):
    """
    Main window for Verbi voice assistant GUI.
    """

    def __init__(self):
        super().__init__()

        # Configure window with neon theme
        self.title("VoxVibe - AI Voice Assistant")
        self.geometry("900x700")
        self.minsize(700, 500)

        # Apply neon theme - pure black background
        self.configure(fg_color=NeonTheme.BG_BLACK)

        # Load and apply saved window geometry
        self.window_config_file = ".verbi_window.json"
        self.load_window_geometry()

        # Configure grid layout (4 rows: header, status_indicator, chat, controls)
        self.grid_rowconfigure(2, weight=1)  # Chat area expands
        self.grid_columnconfigure(0, weight=1)

        # Initialize backend controller
        self.backend = BackendController()
        self.backend.set_callbacks(
            on_status_update=self.handle_status_update,
            on_animation_update=self.handle_animation_update,
            on_message_add=self.handle_message_add,
            on_error=self.handle_error
        )

        # Create menu bar
        self.create_menu_bar()

        # Create UI sections
        self.create_header()
        self.create_status_indicator()
        self.create_chat_area()
        self.create_controls()

        # Setup keyboard shortcuts
        self.setup_keyboard_shortcuts()

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

    def load_window_geometry(self):
        """Load and apply saved window geometry."""
        try:
            if os.path.exists(self.window_config_file):
                with open(self.window_config_file, 'r') as f:
                    config = json.load(f)

                # Apply saved geometry
                width = config.get("width", 900)
                height = config.get("height", 700)
                x = config.get("x")
                y = config.get("y")

                if x is not None and y is not None:
                    self.geometry(f"{width}x{height}+{x}+{y}")
                else:
                    self.geometry(f"{width}x{height}")
                    self.center_window()

                logger.info(f"Window geometry loaded: {width}x{height}+{x}+{y}")
            else:
                # No saved geometry, center window
                self.center_window()
        except Exception as e:
            logger.error(f"Error loading window geometry: {e}")
            self.center_window()

    def save_window_geometry(self):
        """Save current window geometry."""
        try:
            # Get current geometry
            geometry = self.geometry()  # Returns "widthxheight+x+y"
            parts = geometry.replace('+', ' ').replace('x', ' ').split()

            config = {
                "width": int(parts[0]),
                "height": int(parts[1]),
                "x": int(parts[2]),
                "y": int(parts[3])
            }

            with open(self.window_config_file, 'w') as f:
                json.dump(config, f, indent=2)

            logger.info(f"Window geometry saved: {geometry}")
        except Exception as e:
            logger.error(f"Error saving window geometry: {e}")

    def create_menu_bar(self):
        """Create the application menu bar."""
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save Conversation...", command=self.save_conversation, accelerator="Cmd+S")
        file_menu.add_command(label="Load Conversation...", command=self.load_conversation, accelerator="Cmd+O")
        file_menu.add_command(label="Export as Text...", command=self.export_conversation_text)
        file_menu.add_command(label="Export as Markdown...", command=self.export_conversation_markdown)
        file_menu.add_separator()
        file_menu.add_command(label="Settings", command=self.open_settings, accelerator="Cmd+,")
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=self.on_closing, accelerator="Cmd+Q")

        # Edit Menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Clear Conversation", command=self.clear_conversation, accelerator="Cmd+K")

        # View Menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Zoom In", command=lambda: self._adjust_scale(0.1))
        view_menu.add_command(label="Zoom Out", command=lambda: self._adjust_scale(-0.1))
        view_menu.add_command(label="Reset Zoom", command=lambda: self._reset_scale())

        # Help Menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About Verbi", command=self.show_about_dialog)
        help_menu.add_command(label="View Documentation", command=self.open_documentation)

        # Add keyboard accelerators
        self.bind("<Command-s>", lambda e: self.save_conversation())
        self.bind("<Control-s>", lambda e: self.save_conversation())
        self.bind("<Command-o>", lambda e: self.load_conversation())
        self.bind("<Control-o>", lambda e: self.load_conversation())
        self.bind("<Command-q>", lambda e: self.on_closing())
        self.bind("<Control-q>", lambda e: self.on_closing())

        logger.info("Menu bar created")

    def _adjust_scale(self, delta: float):
        """Adjust the UI scaling."""
        current_scale = ctk.ScalingTracker.get_window_dpi_scaling(self)
        new_scale = max(0.8, min(1.5, current_scale + delta))
        ctk.set_widget_scaling(new_scale)
        logger.info(f"UI scale adjusted to {new_scale}")

    def _reset_scale(self):
        """Reset UI scaling to default."""
        ctk.set_widget_scaling(1.0)
        logger.info("UI scale reset to default")

    def setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts for the application."""
        # Space bar - Push to talk
        self.bind("<space>", lambda e: self.toggle_recording())

        # Cmd+K (Mac) or Ctrl+K (Windows/Linux) - Clear conversation
        self.bind("<Command-k>", lambda e: self.clear_conversation())
        self.bind("<Control-k>", lambda e: self.clear_conversation())

        # Cmd+, (Mac) or Ctrl+, (Windows/Linux) - Open settings
        self.bind("<Command-comma>", lambda e: self.open_settings())
        self.bind("<Control-comma>", lambda e: self.open_settings())

        # Escape - Stop action
        self.bind("<Escape>", lambda e: self.stop_action())

        logger.info("Keyboard shortcuts configured")

    def create_header(self):
        """Create the header section with title and settings."""
        header_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        header_frame.grid_columnconfigure(1, weight=1)

        # Title with neon green color
        title_label = ctk.CTkLabel(
            header_frame,
            text="VoxVibe",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=NeonTheme.PRIMARY
        )
        title_label.grid(row=0, column=0, sticky="w")

        # Status indicator with themed text
        self.status_label = ctk.CTkLabel(
            header_frame,
            text="Ready",
            font=ctk.CTkFont(size=14),
            text_color=NeonTheme.TEXT_SECONDARY
        )
        self.status_label.grid(row=0, column=1, sticky="e", padx=(0, 10))

        # Settings button with neon theme
        settings_btn = ctk.CTkButton(
            header_frame,
            text="⚙",
            font=ctk.CTkFont(size=20),
            width=40,
            height=40,
            fg_color=NeonTheme.BG_ELEVATED,
            hover_color=NeonTheme.BG_SURFACE,
            border_color=NeonTheme.PRIMARY,
            border_width=1,
            command=self.open_settings
        )
        settings_btn.grid(row=0, column=2, sticky="e")

    def create_status_indicator(self):
        """Create the status indicator animation area."""
        indicator_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent", height=80)
        indicator_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 5))
        indicator_frame.grid_propagate(False)
        indicator_frame.grid_columnconfigure(0, weight=1)

        # Create status indicator
        self.status_indicator = StatusIndicator(indicator_frame)
        self.status_indicator.grid(row=0, column=0)

    def create_chat_area(self):
        """Create the main chat display area with neon theme."""
        # Chat container with dark background
        chat_container = ctk.CTkFrame(
            self,
            corner_radius=10,
            fg_color=NeonTheme.BG_CHAT,
            border_color=NeonTheme.PRIMARY,
            border_width=1
        )
        chat_container.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        chat_container.grid_rowconfigure(0, weight=1)
        chat_container.grid_columnconfigure(0, weight=1)

        # Use new ChatArea widget
        self.chat_area = ChatArea(
            chat_container,
            corner_radius=10,
            fg_color="transparent"
        )
        self.chat_area.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Welcome message
        self.add_welcome_message()

    def add_welcome_message(self):
        """Add a welcome message to the chat."""
        self.chat_area.add_system_message(
            "👋 Welcome to VoxVibe!\n\nClick the microphone button below to start talking."
        )

    def create_controls(self):
        """Create the control buttons section."""
        controls_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        controls_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=(10, 20))
        controls_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Clear conversation button with neon theme
        clear_btn = ctk.CTkButton(
            controls_frame,
            text="Clear",
            font=ctk.CTkFont(size=14),
            width=100,
            height=40,
            fg_color=NeonTheme.BUTTON_SECONDARY,
            hover_color=NeonTheme.BUTTON_SECONDARY_HOVER,
            border_color=NeonTheme.BORDER_DEFAULT,
            border_width=1,
            command=self.clear_conversation
        )
        clear_btn.grid(row=0, column=0, padx=5)

        # Main microphone button (large, centered) with neon green
        self.mic_button = ctk.CTkButton(
            controls_frame,
            text="🎤",
            font=ctk.CTkFont(size=48),
            width=120,
            height=120,
            corner_radius=60,
            fg_color=NeonTheme.BUTTON_PRIMARY,
            hover_color=NeonTheme.BUTTON_PRIMARY_HOVER,
            border_color=NeonTheme.PRIMARY,
            border_width=2,
            command=self.toggle_recording
        )
        self.mic_button.grid(row=0, column=1, padx=5, pady=10)

        # Stop button with danger color
        self.stop_btn = ctk.CTkButton(
            controls_frame,
            text="Stop",
            font=ctk.CTkFont(size=14),
            width=100,
            height=40,
            fg_color=NeonTheme.BUTTON_DANGER,
            hover_color=NeonTheme.BUTTON_DANGER_HOVER,
            border_color=NeonTheme.SECONDARY_PINK,
            border_width=1,
            command=self.stop_action,
            state="disabled"
        )
        self.stop_btn.grid(row=0, column=2, padx=5)

        # Demo button with cyan accent
        demo_btn = ctk.CTkButton(
            controls_frame,
            text="Demo",
            font=ctk.CTkFont(size=14),
            width=100,
            height=40,
            fg_color=NeonTheme.BUTTON_SECONDARY,
            hover_color=NeonTheme.BUTTON_SECONDARY_HOVER,
            border_color=NeonTheme.SECONDARY_CYAN,
            border_width=1,
            text_color=NeonTheme.SECONDARY_CYAN,
            command=self.demo_conversation
        )
        demo_btn.grid(row=0, column=3, padx=5)

    def toggle_recording(self):
        """Start voice conversation with backend."""
        if self.backend.is_processing:
            logger.warning("Already processing a conversation")
            return

        # Disable mic button while processing
        self.mic_button.configure(state="disabled")
        self.stop_btn.configure(state="normal")

        # Start conversation in background
        self.backend.start_conversation()

        logger.info("Voice conversation started")

    def stop_action(self):
        """Stop current action (recording/playback)."""
        self.backend.stop()
        self.mic_button.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.update_status("Ready")
        self.status_indicator.set_state("idle")
        logger.info("Action stopped")

    def clear_conversation(self):
        """Clear the conversation history with confirmation."""
        # Show confirmation dialog
        self._show_confirmation_dialog(
            title="Clear Conversation",
            message="Are you sure you want to clear the conversation history?\n\nThis action cannot be undone.",
            on_confirm=self._do_clear_conversation
        )

    def _do_clear_conversation(self):
        """Actually clear the conversation after confirmation."""
        # Clear backend history
        self.backend.clear_history()

        # Clear all messages from UI
        self.chat_area.clear_messages()

        # Add welcome message back
        self.add_welcome_message()
        self.update_status("Conversation cleared")
        self.status_indicator.set_state("idle")
        logger.info("Conversation cleared")

    def demo_conversation(self):
        """Demo the chat UI with sample messages and animations."""
        # Clear first
        self.chat_area.clear_messages()

        # Simulate a conversation
        self.update_status("Demo mode")

        # User message
        self.chat_area.add_message("Hello Verbi! How are you today?", sender="user")

        # Simulate thinking
        self.after(800, lambda: self.status_indicator.set_state("thinking"))
        self.after(800, lambda: self.update_status("Thinking..."))

        # Assistant response
        self.after(2000, lambda: self.chat_area.add_message(
            "Hello! I'm doing great, thank you for asking! I'm here to help you with anything you need.",
            sender="assistant"
        ))

        # Simulate speaking
        self.after(2000, lambda: self.status_indicator.set_state("speaking"))
        self.after(2000, lambda: self.update_status("Speaking..."))

        # User follows up
        self.after(4000, lambda: self.chat_area.add_message(
            "Can you tell me about the weather?",
            sender="user"
        ))

        # Thinking again
        self.after(4800, lambda: self.status_indicator.set_state("thinking"))
        self.after(4800, lambda: self.update_status("Thinking..."))

        # Final response
        self.after(6000, lambda: self.chat_area.add_message(
            "I'd be happy to help with the weather! However, I need access to weather services to provide accurate information. Would you like me to set that up?",
            sender="assistant"
        ))

        # Back to ready
        self.after(6500, lambda: self.status_indicator.set_state("idle"))
        self.after(6500, lambda: self.update_status("Ready"))

    def open_settings(self):
        """Open settings dialog."""
        logger.info("Opening settings window")
        settings_window = SettingsWindow(self, on_settings_saved=self.on_settings_saved)

    def on_settings_saved(self):
        """Handle settings saved callback."""
        logger.info("Settings saved, updating UI")
        self.update_status("Settings updated")

    def update_status(self, message: str):
        """Update the status label."""
        self.status_label.configure(text=message)

    # Backend callback handlers
    def handle_status_update(self, status: str):
        """Handle status updates from backend (thread-safe)."""
        self.after(0, lambda: self.update_status(status))

    def handle_animation_update(self, state: str):
        """Handle animation state updates from backend (thread-safe)."""
        self.after(0, lambda: self.status_indicator.set_state(state))
        # Re-enable mic button when back to idle
        if state == "idle":
            self.after(0, lambda: self.mic_button.configure(state="normal"))
            self.after(0, lambda: self.stop_btn.configure(state="disabled"))

    def handle_message_add(self, message: str, sender: str):
        """Handle adding messages from backend (thread-safe)."""
        self.after(0, lambda: self.chat_area.add_message(message, sender))

    def handle_error(self, error_message: str):
        """Handle errors from backend (thread-safe)."""
        self.after(0, lambda: self._show_error_dialog(error_message))
        self.after(0, lambda: self.mic_button.configure(state="normal"))
        self.after(0, lambda: self.stop_btn.configure(state="disabled"))

    def _show_error_dialog(self, error_message: str):
        """Show error dialog to user."""
        logger.error(f"Showing error dialog: {error_message}")
        ErrorDialog(self, error_message)

    def _show_confirmation_dialog(self, title: str, message: str, on_confirm):
        """Show confirmation dialog with Yes/No buttons."""
        ConfirmationDialog(self, message, on_confirm, title)

    def save_conversation(self):
        """Save conversation history to JSON file."""
        if not self.backend.chat_history or len(self.backend.chat_history) <= 1:
            self._show_error_dialog("No conversation to save!")
            return

        # Ask for file location
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile=f"verbi_conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )

        if filename:
            try:
                with open(filename, 'w') as f:
                    json.dump({
                        "timestamp": datetime.now().isoformat(),
                        "messages": self.backend.chat_history
                    }, f, indent=2)
                self.update_status(f"Conversation saved")
                logger.info(f"Conversation saved to {filename}")
            except Exception as e:
                logger.error(f"Error saving conversation: {e}")
                self._show_error_dialog(f"Failed to save conversation: {str(e)}")

    def load_conversation(self):
        """Load conversation history from JSON file."""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if filename:
            try:
                with open(filename, 'r') as f:
                    data = json.load(f)

                # Clear current conversation
                self.backend.chat_history = data.get("messages", [])
                self.chat_area.clear_messages()

                # Display loaded messages
                for msg in self.backend.chat_history:
                    if msg["role"] == "user":
                        self.chat_area.add_message(msg["content"], "user")
                    elif msg["role"] == "assistant":
                        self.chat_area.add_message(msg["content"], "assistant")

                self.update_status("Conversation loaded")
                logger.info(f"Conversation loaded from {filename}")
            except Exception as e:
                logger.error(f"Error loading conversation: {e}")
                self._show_error_dialog(f"Failed to load conversation: {str(e)}")

    def export_conversation_text(self):
        """Export conversation as plain text file."""
        if not self.backend.chat_history or len(self.backend.chat_history) <= 1:
            self._show_error_dialog("No conversation to export!")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"verbi_conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )

        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(f"Verbi Conversation Export\n")
                    f.write(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("=" * 60 + "\n\n")

                    for msg in self.backend.chat_history:
                        if msg["role"] == "user":
                            f.write(f"USER:\n{msg['content']}\n\n")
                        elif msg["role"] == "assistant":
                            f.write(f"ASSISTANT:\n{msg['content']}\n\n")
                        f.write("-" * 60 + "\n\n")

                self.update_status("Conversation exported as text")
                logger.info(f"Conversation exported to {filename}")
            except Exception as e:
                logger.error(f"Error exporting conversation: {e}")
                self._show_error_dialog(f"Failed to export conversation: {str(e)}")

    def export_conversation_markdown(self):
        """Export conversation as markdown file."""
        if not self.backend.chat_history or len(self.backend.chat_history) <= 1:
            self._show_error_dialog("No conversation to export!")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".md",
            filetypes=[("Markdown files", "*.md"), ("All files", "*.*")],
            initialfile=f"verbi_conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        )

        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(f"# Verbi Conversation\n\n")
                    f.write(f"**Exported:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    f.write("---\n\n")

                    for msg in self.backend.chat_history:
                        if msg["role"] == "user":
                            f.write(f"### 👤 User\n\n{msg['content']}\n\n")
                        elif msg["role"] == "assistant":
                            f.write(f"### 🤖 Assistant\n\n{msg['content']}\n\n")

                self.update_status("Conversation exported as markdown")
                logger.info(f"Conversation exported to {filename}")
            except Exception as e:
                logger.error(f"Error exporting conversation: {e}")
                self._show_error_dialog(f"Failed to export conversation: {str(e)}")

    def show_about_dialog(self):
        """Show About dialog with version info."""
        AboutDialog(self, version="1.0.0")

    def open_documentation(self):
        """Open documentation in web browser."""
        import webbrowser
        webbrowser.open("https://github.com/ratandeepbansal/Verbi")
        logger.info("Opening documentation")

    def on_closing(self):
        """Handle window close event."""
        logger.info("Closing application...")

        # Save window geometry
        self.save_window_geometry()

        # Stop backend
        self.backend.stop()

        # Close application
        self.quit()
        self.destroy()


def main():
    """Main entry point for the GUI application."""
    app = VerbiMainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
