# gui/dialogs.py

"""
Reusable dialog components for the Verbi GUI.
"""

import customtkinter as ctk
from typing import Optional, Callable
import webbrowser


def create_centered_dialog(parent, title: str, width: int, height: int) -> ctk.CTkToplevel:
    """
    Create a centered dialog window.

    Args:
        parent: Parent window
        title: Dialog title
        width: Dialog width
        height: Dialog height

    Returns:
        Configured CTkToplevel dialog
    """
    dialog = ctk.CTkToplevel(parent)
    dialog.title(title)
    dialog.geometry(f"{width}x{height}")
    dialog.transient(parent)
    dialog.grab_set()

    # Center dialog on parent
    dialog.update_idletasks()
    x = parent.winfo_x() + (parent.winfo_width() // 2) - (width // 2)
    y = parent.winfo_y() + (parent.winfo_height() // 2) - (height // 2)
    dialog.geometry(f"+{x}+{y}")

    return dialog


class ErrorDialog:
    """Error dialog with customizable message."""

    def __init__(self, parent, message: str, title: str = "Error"):
        """
        Create and display an error dialog.

        Args:
            parent: Parent window
            message: Error message to display
            title: Dialog title (default: "Error")
        """
        self.dialog = create_centered_dialog(parent, title, 400, 200)

        # Error message
        error_label = ctk.CTkLabel(
            self.dialog,
            text=f"⚠️ {title}\n\n{message}",
            font=ctk.CTkFont(size=14),
            wraplength=350
        )
        error_label.pack(pady=20, padx=20)

        # OK button
        ok_btn = ctk.CTkButton(
            self.dialog,
            text="OK",
            command=self.dialog.destroy,
            width=100
        )
        ok_btn.pack(pady=10)


class ConfirmationDialog:
    """Confirmation dialog with Yes/No buttons."""

    def __init__(self, parent, message: str, on_confirm: Callable, title: str = "Confirm"):
        """
        Create and display a confirmation dialog.

        Args:
            parent: Parent window
            message: Confirmation message
            on_confirm: Callback function to execute on confirmation
            title: Dialog title (default: "Confirm")
        """
        self.dialog = create_centered_dialog(parent, title, 400, 200)

        # Message
        message_label = ctk.CTkLabel(
            self.dialog,
            text=message,
            font=ctk.CTkFont(size=14),
            wraplength=350
        )
        message_label.pack(pady=30, padx=20)

        # Button frame
        button_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        button_frame.pack(pady=10)

        # Yes button
        yes_btn = ctk.CTkButton(
            button_frame,
            text="Yes",
            command=lambda: [self.dialog.destroy(), on_confirm()],
            width=100,
            fg_color="red",
            hover_color="darkred"
        )
        yes_btn.pack(side="left", padx=10)

        # No button
        no_btn = ctk.CTkButton(
            button_frame,
            text="No",
            command=self.dialog.destroy,
            width=100,
            fg_color="gray",
            hover_color="darkgray"
        )
        no_btn.pack(side="left", padx=10)


class AboutDialog:
    """About dialog with app information."""

    def __init__(self, parent, version: str = "1.0.0"):
        """
        Create and display an About dialog.

        Args:
            parent: Parent window
            version: App version string (default: "1.0.0")
        """
        self.dialog = create_centered_dialog(parent, "About Verbi", 400, 350)

        # Title
        title_label = ctk.CTkLabel(
            self.dialog,
            text="Verbi",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title_label.pack(pady=(30, 5))

        # Version
        version_label = ctk.CTkLabel(
            self.dialog,
            text=f"Version {version}",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        version_label.pack(pady=5)

        # Description
        desc_label = ctk.CTkLabel(
            self.dialog,
            text="AI-Powered Voice Assistant\n\nBuilt with CustomTkinter\nSupports multiple AI providers",
            font=ctk.CTkFont(size=12),
            justify="center"
        )
        desc_label.pack(pady=20)

        # Credits
        credits_label = ctk.CTkLabel(
            self.dialog,
            text="© 2025 Verbi\nAll rights reserved",
            font=ctk.CTkFont(size=10),
            text_color="gray",
            justify="center"
        )
        credits_label.pack(pady=10)

        # Button frame
        button_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        button_frame.pack(pady=20)

        # Documentation button
        docs_btn = ctk.CTkButton(
            button_frame,
            text="Documentation",
            command=self._open_docs,
            width=120,
            fg_color="blue",
            hover_color="darkblue"
        )
        docs_btn.pack(side="left", padx=5)

        # Close button
        close_btn = ctk.CTkButton(
            button_frame,
            text="Close",
            command=self.dialog.destroy,
            width=100
        )
        close_btn.pack(side="left", padx=5)

    def _open_docs(self):
        """Open documentation in web browser."""
        webbrowser.open("https://github.com/ratandeepbansal/Verbi")


class InfoDialog:
    """Simple information dialog."""

    def __init__(self, parent, message: str, title: str = "Information"):
        """
        Create and display an information dialog.

        Args:
            parent: Parent window
            message: Information message to display
            title: Dialog title (default: "Information")
        """
        self.dialog = create_centered_dialog(parent, title, 400, 150)

        # Message
        message_label = ctk.CTkLabel(
            self.dialog,
            text=message,
            font=ctk.CTkFont(size=14),
            wraplength=350
        )
        message_label.pack(pady=30, padx=20)

        # OK button
        ok_btn = ctk.CTkButton(
            self.dialog,
            text="OK",
            command=self.dialog.destroy,
            width=100
        )
        ok_btn.pack(pady=10)
