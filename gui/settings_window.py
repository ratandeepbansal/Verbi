# gui/settings_window.py

import customtkinter as ctk
import os
import json
import threading
from typing import Callable, Optional
import logging
from gui.theme import NeonTheme, LayoutConfig

logger = logging.getLogger(__name__)


class SettingsWindow(ctk.CTkToplevel):
    """Settings window for configuring Verbi voice assistant."""

    def __init__(self, parent, on_settings_saved: Optional[Callable] = None):
        """
        Initialize the settings window.

        Args:
            parent: Parent window
            on_settings_saved: Callback function when settings are saved
        """
        super().__init__(parent)

        self.on_settings_saved = on_settings_saved
        self.config_file = ".verbi_config.json"

        # Window configuration with neon theme
        self.title("VoxVibe Settings")
        self.geometry("700x900")
        self.resizable(False, False)
        self.configure(fg_color=NeonTheme.BG_BLACK)

        # Make window modal
        self.transient(parent)
        self.grab_set()

        # Center window on parent
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (700 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (900 // 2)
        self.geometry(f"+{x}+{y}")

        # Create UI
        self._create_widgets()
        self._load_settings()

    def _create_widgets(self):
        """Create all UI widgets."""
        # Main container with scrollable frame
        self.main_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # Title with neon green
        title = ctk.CTkLabel(
            self.main_container,
            text="Settings",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=NeonTheme.PRIMARY
        )
        title.pack(pady=(0, 20))

        # Model Selection Section
        self._create_model_section()

        # LLM Model Details Section
        self._create_llm_details_section()

        # Local Models Configuration Section
        self._create_local_models_section()

        # API Keys Section
        self._create_api_keys_section()

        # API Status Section
        self._create_api_status_section()

        # Buttons
        self._create_buttons()

    def _create_model_section(self):
        """Create model selection section."""
        # Section header with neon green
        header = ctk.CTkLabel(
            self.main_container,
            text="Model Selection",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=NeonTheme.PRIMARY
        )
        header.pack(anchor="w", pady=(10, 10))

        # Transcription Model
        transcription_frame = ctk.CTkFrame(
            self.main_container,
            fg_color=NeonTheme.BG_ELEVATED,
            border_color=NeonTheme.BORDER_DEFAULT,
            border_width=1
        )
        transcription_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(
            transcription_frame,
            text="Transcription Model:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=10, pady=10)

        self.transcription_var = ctk.StringVar(value="deepgram")
        self.transcription_menu = ctk.CTkOptionMenu(
            transcription_frame,
            variable=self.transcription_var,
            values=["openai", "groq", "deepgram", "fastwhisperapi", "faster-whisper", "local"],
            width=200
        )
        self.transcription_menu.pack(side="right", padx=10, pady=10)

        # Response Model
        response_frame = ctk.CTkFrame(
            self.main_container,
            fg_color=NeonTheme.BG_ELEVATED,
            border_color=NeonTheme.BORDER_DEFAULT,
            border_width=1
        )
        response_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(
            response_frame,
            text="Response Model:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=10, pady=10)

        self.response_var = ctk.StringVar(value="openai")
        self.response_menu = ctk.CTkOptionMenu(
            response_frame,
            variable=self.response_var,
            values=["openai", "groq", "ollama", "lmstudio", "local"],
            width=200
        )
        self.response_menu.pack(side="right", padx=10, pady=10)

        # TTS Model
        tts_frame = ctk.CTkFrame(
            self.main_container,
            fg_color=NeonTheme.BG_ELEVATED,
            border_color=NeonTheme.BORDER_DEFAULT,
            border_width=1
        )
        tts_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(
            tts_frame,
            text="Text-to-Speech Model:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=10, pady=10)

        self.tts_var = ctk.StringVar(value="openai")
        self.tts_menu = ctk.CTkOptionMenu(
            tts_frame,
            variable=self.tts_var,
            values=["openai", "deepgram", "elevenlabs", "melotts", "cartesia", "piper", "local"],
            width=200
        )
        self.tts_menu.pack(side="right", padx=10, pady=10)

    def _create_llm_details_section(self):
        """Create LLM model details section."""
        # Section header with neon green
        header = ctk.CTkLabel(
            self.main_container,
            text="LLM Model Details",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=NeonTheme.PRIMARY
        )
        header.pack(anchor="w", pady=(20, 10))

        # OpenAI LLM
        openai_llm_frame = ctk.CTkFrame(
            self.main_container,
            fg_color=NeonTheme.BG_ELEVATED,
            border_color=NeonTheme.BORDER_DEFAULT,
            border_width=1
        )
        openai_llm_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(
            openai_llm_frame,
            text="OpenAI Model:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=10, pady=10)

        self.openai_llm_var = ctk.StringVar(value="gpt-4o")
        self.openai_llm_entry = ctk.CTkEntry(
            openai_llm_frame,
            textvariable=self.openai_llm_var,
            width=200
        )
        self.openai_llm_entry.pack(side="right", padx=10, pady=10)

        # Groq LLM
        groq_llm_frame = ctk.CTkFrame(
            self.main_container,
            fg_color=NeonTheme.BG_ELEVATED,
            border_color=NeonTheme.BORDER_DEFAULT,
            border_width=1
        )
        groq_llm_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(
            groq_llm_frame,
            text="Groq Model:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=10, pady=10)

        self.groq_llm_var = ctk.StringVar(value="llama3-8b-8192")
        self.groq_llm_entry = ctk.CTkEntry(
            groq_llm_frame,
            textvariable=self.groq_llm_var,
            width=200
        )
        self.groq_llm_entry.pack(side="right", padx=10, pady=10)

        # Ollama LLM
        ollama_llm_frame = ctk.CTkFrame(
            self.main_container,
            fg_color=NeonTheme.BG_ELEVATED,
            border_color=NeonTheme.BORDER_DEFAULT,
            border_width=1
        )
        ollama_llm_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(
            ollama_llm_frame,
            text="Ollama Model:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=10, pady=10)

        self.ollama_llm_var = ctk.StringVar(value="llama3:8b")
        self.ollama_llm_entry = ctk.CTkEntry(
            ollama_llm_frame,
            textvariable=self.ollama_llm_var,
            width=200
        )
        self.ollama_llm_entry.pack(side="right", padx=10, pady=10)

    def _create_local_models_section(self):
        """Create local models configuration section."""
        # Section header with neon green
        header = ctk.CTkLabel(
            self.main_container,
            text="Local Models Configuration",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=NeonTheme.PRIMARY
        )
        header.pack(anchor="w", pady=(20, 10))

        # LM Studio Base URL
        lmstudio_frame = ctk.CTkFrame(
            self.main_container,
            fg_color=NeonTheme.BG_ELEVATED,
            border_color=NeonTheme.BORDER_DEFAULT,
            border_width=1
        )
        lmstudio_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(
            lmstudio_frame,
            text="LM Studio URL:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=10, pady=10)

        self.lmstudio_url_var = ctk.StringVar(value="http://localhost:1234")
        self.lmstudio_url_entry = ctk.CTkEntry(
            lmstudio_frame,
            textvariable=self.lmstudio_url_var,
            width=200
        )
        self.lmstudio_url_entry.pack(side="right", padx=10, pady=10)

        # faster-whisper Model Size
        whisper_frame = ctk.CTkFrame(
            self.main_container,
            fg_color=NeonTheme.BG_ELEVATED,
            border_color=NeonTheme.BORDER_DEFAULT,
            border_width=1
        )
        whisper_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(
            whisper_frame,
            text="Whisper Model:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=10, pady=10)

        self.whisper_model_var = ctk.StringVar(value="base")
        self.whisper_model_menu = ctk.CTkOptionMenu(
            whisper_frame,
            variable=self.whisper_model_var,
            values=["tiny", "base", "small", "medium", "large-v3"],
            width=200
        )
        self.whisper_model_menu.pack(side="right", padx=10, pady=10)

    def _create_api_keys_section(self):
        """Create API keys section."""
        # Section header with neon green
        header = ctk.CTkLabel(
            self.main_container,
            text="API Keys",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=NeonTheme.PRIMARY
        )
        header.pack(anchor="w", pady=(20, 10))

        # Info label with muted color
        info = ctk.CTkLabel(
            self.main_container,
            text="Enter your API keys below. They will be saved securely.",
            font=ctk.CTkFont(size=12),
            text_color=NeonTheme.TEXT_MUTED
        )
        info.pack(anchor="w", pady=(0, 10))

        # OpenAI API Key
        self._create_api_key_field("OpenAI API Key:", "openai_key")

        # Groq API Key
        self._create_api_key_field("Groq API Key:", "groq_key")

        # Deepgram API Key
        self._create_api_key_field("Deepgram API Key:", "deepgram_key")

        # ElevenLabs API Key
        self._create_api_key_field("ElevenLabs API Key:", "elevenlabs_key")

        # Cartesia API Key
        self._create_api_key_field("Cartesia API Key:", "cartesia_key")

    def _create_api_key_field(self, label_text: str, field_name: str):
        """
        Create an API key input field.

        Args:
            label_text: Label for the field
            field_name: Internal field name
        """
        frame = ctk.CTkFrame(
            self.main_container,
            fg_color=NeonTheme.BG_ELEVATED,
            border_color=NeonTheme.BORDER_DEFAULT,
            border_width=1
        )
        frame.pack(fill="x", pady=5)

        ctk.CTkLabel(
            frame,
            text=label_text,
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=10, pady=10)

        var = ctk.StringVar()
        entry = ctk.CTkEntry(
            frame,
            textvariable=var,
            show="*",
            width=300
        )
        entry.pack(side="right", padx=10, pady=10)

        # Store reference
        setattr(self, f"{field_name}_var", var)
        setattr(self, f"{field_name}_entry", entry)

    def _create_api_status_section(self):
        """Create API status testing section."""
        # Section header with neon green
        header = ctk.CTkLabel(
            self.main_container,
            text="API Status",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=NeonTheme.PRIMARY
        )
        header.pack(anchor="w", pady=(20, 10))

        # Info label with muted color
        info = ctk.CTkLabel(
            self.main_container,
            text="Test your API connections to verify they are working correctly.",
            font=ctk.CTkFont(size=12),
            text_color=NeonTheme.TEXT_MUTED
        )
        info.pack(anchor="w", pady=(0, 10))

        # Status container with neon theme
        status_container = ctk.CTkFrame(
            self.main_container,
            fg_color=NeonTheme.BG_SURFACE,
            border_color=NeonTheme.BORDER_DEFAULT,
            border_width=1
        )
        status_container.pack(fill="x", pady=10)

        # Dictionary to store status labels
        self.api_status_labels = {}

        # Create status row for each provider
        providers = ["OpenAI", "Groq", "Deepgram", "ElevenLabs", "Cartesia"]
        for provider in providers:
            self._create_api_status_row(status_container, provider)

        # Test button with neon purple theme
        test_button_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        test_button_frame.pack(fill="x", pady=(10, 0))

        self.test_apis_btn = ctk.CTkButton(
            test_button_frame,
            text="Test All APIs",
            command=self._test_all_apis,
            width=150,
            height=35,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=NeonTheme.SECONDARY_PURPLE,
            hover_color="#7A00CC",  # Darker purple for hover
            border_color=NeonTheme.SECONDARY_PURPLE,
            border_width=1
        )
        self.test_apis_btn.pack(side="left")

        # Status message with muted color
        self.test_status_label = ctk.CTkLabel(
            test_button_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=NeonTheme.TEXT_MUTED
        )
        self.test_status_label.pack(side="left", padx=20)

    def _create_api_status_row(self, parent, provider_name: str):
        """
        Create a status row for an API provider.

        Args:
            parent: Parent widget
            provider_name: Name of the provider
        """
        row = ctk.CTkFrame(
            parent,
            fg_color=NeonTheme.BG_ELEVATED,
            border_color=NeonTheme.BORDER_DEFAULT,
            border_width=1
        )
        row.pack(fill="x", pady=3, padx=10)

        # Provider name
        name_label = ctk.CTkLabel(
            row,
            text=f"{provider_name}:",
            font=ctk.CTkFont(size=14),
            width=120,
            anchor="w"
        )
        name_label.pack(side="left", padx=10, pady=8)

        # Status icon
        status_label = ctk.CTkLabel(
            row,
            text="●",
            font=ctk.CTkFont(size=20),
            text_color=NeonTheme.TEXT_MUTED,
            width=30
        )
        status_label.pack(side="left", padx=5)

        # Status message
        message_label = ctk.CTkLabel(
            row,
            text="Not tested",
            font=ctk.CTkFont(size=12),
            text_color=NeonTheme.TEXT_MUTED,
            anchor="w"
        )
        message_label.pack(side="left", padx=10)

        # Store references
        self.api_status_labels[provider_name] = {
            "icon": status_label,
            "message": message_label
        }

    def _test_all_apis(self):
        """Test all API providers in background thread."""
        # Disable button during testing
        self.test_apis_btn.configure(state="disabled", text="Testing...")
        self.test_status_label.configure(text="Testing APIs...", text_color=NeonTheme.SECONDARY_PURPLE)

        # Reset all statuses with neon purple (testing state)
        for provider in self.api_status_labels:
            self.api_status_labels[provider]["icon"].configure(text="●", text_color=NeonTheme.SECONDARY_PURPLE)
            self.api_status_labels[provider]["message"].configure(text="Testing...", text_color=NeonTheme.SECONDARY_PURPLE)

        # Run tests in background thread
        thread = threading.Thread(target=self._run_api_tests, daemon=True)
        thread.start()

    def _run_api_tests(self):
        """Run API tests in background thread."""
        from voice_assistant.api_tester import test_all_apis

        # Get API keys from form
        results = test_all_apis(
            openai_key=self.openai_key_var.get(),
            groq_key=self.groq_key_var.get(),
            deepgram_key=self.deepgram_key_var.get(),
            elevenlabs_key=self.elevenlabs_key_var.get(),
            cartesia_key=self.cartesia_key_var.get()
        )

        # Update UI in main thread
        self.after(0, lambda: self._update_api_status(results))

    def _update_api_status(self, results: dict):
        """
        Update UI with API test results.

        Args:
            results: Dictionary of test results
        """
        for provider, (success, message) in results.items():
            if provider in self.api_status_labels:
                icon_label = self.api_status_labels[provider]["icon"]
                msg_label = self.api_status_labels[provider]["message"]

                if success:
                    # Neon green for success
                    icon_label.configure(text="✓", text_color=NeonTheme.PRIMARY)
                    msg_label.configure(text=message, text_color=NeonTheme.PRIMARY)
                else:
                    # Neon pink for errors
                    icon_label.configure(text="✗", text_color=NeonTheme.SECONDARY_PINK)
                    msg_label.configure(text=message, text_color=NeonTheme.SECONDARY_PINK)

        # Re-enable button
        self.test_apis_btn.configure(state="normal", text="Test All APIs")
        self.test_status_label.configure(text="Testing complete", text_color=NeonTheme.PRIMARY)

        logger.info(f"API test results: {results}")

    def _create_buttons(self):
        """Create action buttons with neon theme."""
        button_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        button_frame.pack(fill="x", pady=(20, 0))

        # Save button - neon green (primary action)
        save_btn = ctk.CTkButton(
            button_frame,
            text="Save Settings",
            command=self._save_settings,
            width=150,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=NeonTheme.BUTTON_PRIMARY,
            hover_color=NeonTheme.BUTTON_PRIMARY_HOVER,
            border_color=NeonTheme.PRIMARY,
            border_width=1
        )
        save_btn.pack(side="left", padx=5)

        # Cancel button - gray/muted
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.destroy,
            width=150,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color=NeonTheme.BUTTON_SECONDARY,
            hover_color=NeonTheme.BUTTON_SECONDARY_HOVER,
            border_color=NeonTheme.BORDER_DEFAULT,
            border_width=1
        )
        cancel_btn.pack(side="left", padx=5)

        # Reset to defaults button - neon pink (warning action)
        reset_btn = ctk.CTkButton(
            button_frame,
            text="Reset to Defaults",
            command=self._reset_to_defaults,
            width=150,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color=NeonTheme.BUTTON_DANGER,
            hover_color=NeonTheme.BUTTON_DANGER_HOVER,
            border_color=NeonTheme.SECONDARY_PINK,
            border_width=1
        )
        reset_btn.pack(side="right", padx=5)

    def _load_settings(self):
        """Load settings from config file or environment variables."""
        try:
            # Try to load from config file first
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    settings = json.load(f)

                # Model selection
                self.transcription_var.set(settings.get("transcription_model", "deepgram"))
                self.response_var.set(settings.get("response_model", "openai"))
                self.tts_var.set(settings.get("tts_model", "openai"))

                # LLM models
                self.openai_llm_var.set(settings.get("openai_llm", "gpt-4o"))
                self.groq_llm_var.set(settings.get("groq_llm", "llama3-8b-8192"))
                self.ollama_llm_var.set(settings.get("ollama_llm", "llama3:8b"))

                # Local models configuration
                self.lmstudio_url_var.set(settings.get("lmstudio_base_url", "http://localhost:1234"))
                self.whisper_model_var.set(settings.get("faster_whisper_model", "base"))

                # API keys (if saved)
                self.openai_key_var.set(settings.get("openai_api_key", ""))
                self.groq_key_var.set(settings.get("groq_api_key", ""))
                self.deepgram_key_var.set(settings.get("deepgram_api_key", ""))
                self.elevenlabs_key_var.set(settings.get("elevenlabs_api_key", ""))
                self.cartesia_key_var.set(settings.get("cartesia_api_key", ""))

                logger.info("Settings loaded from config file")
            else:
                # Load from environment variables
                self._load_from_env()
                logger.info("Settings loaded from environment variables")

        except Exception as e:
            logger.error(f"Error loading settings: {e}")
            self._load_from_env()

    def _load_from_env(self):
        """Load settings from environment variables."""
        from voice_assistant.config import Config

        # Model selection
        self.transcription_var.set(Config.TRANSCRIPTION_MODEL)
        self.response_var.set(Config.RESPONSE_MODEL)
        self.tts_var.set(Config.TTS_MODEL)

        # LLM models
        self.openai_llm_var.set(Config.OPENAI_LLM)
        self.groq_llm_var.set(Config.GROQ_LLM)
        self.ollama_llm_var.set(Config.OLLAMA_LLM)

        # Local models configuration
        self.lmstudio_url_var.set(Config.LMSTUDIO_BASE_URL)
        self.whisper_model_var.set(Config.FASTER_WHISPER_MODEL)

        # API keys
        self.openai_key_var.set(Config.OPENAI_API_KEY or "")
        self.groq_key_var.set(Config.GROQ_API_KEY or "")
        self.deepgram_key_var.set(Config.DEEPGRAM_API_KEY or "")
        self.elevenlabs_key_var.set(Config.ELEVENLABS_API_KEY or "")
        self.cartesia_key_var.set(Config.CARTESIA_API_KEY or "")

    def _save_settings(self):
        """Save settings to config file and update Config class."""
        try:
            settings = {
                "transcription_model": self.transcription_var.get(),
                "response_model": self.response_var.get(),
                "tts_model": self.tts_var.get(),
                "openai_llm": self.openai_llm_var.get(),
                "groq_llm": self.groq_llm_var.get(),
                "ollama_llm": self.ollama_llm_var.get(),
                "lmstudio_base_url": self.lmstudio_url_var.get(),
                "faster_whisper_model": self.whisper_model_var.get(),
                "openai_api_key": self.openai_key_var.get(),
                "groq_api_key": self.groq_key_var.get(),
                "deepgram_api_key": self.deepgram_key_var.get(),
                "elevenlabs_api_key": self.elevenlabs_key_var.get(),
                "cartesia_api_key": self.cartesia_key_var.get(),
            }

            # Save to file
            with open(self.config_file, 'w') as f:
                json.dump(settings, f, indent=4)

            # Update Config class
            from voice_assistant.config import Config
            Config.TRANSCRIPTION_MODEL = settings["transcription_model"]
            Config.RESPONSE_MODEL = settings["response_model"]
            Config.TTS_MODEL = settings["tts_model"]
            Config.OPENAI_LLM = settings["openai_llm"]
            Config.GROQ_LLM = settings["groq_llm"]
            Config.OLLAMA_LLM = settings["ollama_llm"]
            Config.LMSTUDIO_BASE_URL = settings["lmstudio_base_url"]
            Config.FASTER_WHISPER_MODEL = settings["faster_whisper_model"]

            # Update API keys if provided
            if settings["openai_api_key"]:
                Config.OPENAI_API_KEY = settings["openai_api_key"]
                os.environ["OPENAI_API_KEY"] = settings["openai_api_key"]
            if settings["groq_api_key"]:
                Config.GROQ_API_KEY = settings["groq_api_key"]
                os.environ["GROQ_API_KEY"] = settings["groq_api_key"]
            if settings["deepgram_api_key"]:
                Config.DEEPGRAM_API_KEY = settings["deepgram_api_key"]
                os.environ["DEEPGRAM_API_KEY"] = settings["deepgram_api_key"]
            if settings["elevenlabs_api_key"]:
                Config.ELEVENLABS_API_KEY = settings["elevenlabs_api_key"]
                os.environ["ELEVENLABS_API_KEY"] = settings["elevenlabs_api_key"]
            if settings["cartesia_api_key"]:
                Config.CARTESIA_API_KEY = settings["cartesia_api_key"]
                os.environ["CARTESIA_API_KEY"] = settings["cartesia_api_key"]

            # Validate config
            try:
                Config.validate_config()
                logger.info("Settings saved and validated successfully")

                # Show success message
                self._show_message("Success", "Settings saved successfully!")

                # Call callback if provided
                if self.on_settings_saved:
                    self.on_settings_saved()

                # Close window
                self.destroy()

            except ValueError as e:
                logger.error(f"Configuration validation failed: {e}")
                self._show_error("Validation Error", str(e))

        except Exception as e:
            logger.error(f"Error saving settings: {e}")
            self._show_error("Save Error", f"Failed to save settings: {str(e)}")

    def _reset_to_defaults(self):
        """Reset all settings to default values."""
        self.transcription_var.set("deepgram")
        self.response_var.set("openai")
        self.tts_var.set("openai")
        self.openai_llm_var.set("gpt-4o")
        self.groq_llm_var.set("llama3-8b-8192")
        self.ollama_llm_var.set("llama3:8b")

        # Don't clear API keys, just show a message
        self._show_message("Reset", "Model settings reset to defaults.\nAPI keys were not cleared.")

    def _show_message(self, title: str, message: str):
        """Show info message dialog with neon theme."""
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("400x150")
        dialog.transient(self)
        dialog.grab_set()
        dialog.configure(fg_color=NeonTheme.BG_BLACK)

        # Center on parent
        dialog.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - 200
        y = self.winfo_y() + (self.winfo_height() // 2) - 75
        dialog.geometry(f"+{x}+{y}")

        ctk.CTkLabel(
            dialog,
            text=message,
            font=ctk.CTkFont(size=14),
            wraplength=350
        ).pack(pady=30)

        ctk.CTkButton(
            dialog,
            text="OK",
            command=dialog.destroy,
            width=100,
            fg_color=NeonTheme.BUTTON_PRIMARY,
            hover_color=NeonTheme.BUTTON_PRIMARY_HOVER
        ).pack(pady=10)

    def _show_error(self, title: str, message: str):
        """Show error message dialog with neon theme."""
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("400x150")
        dialog.transient(self)
        dialog.grab_set()
        dialog.configure(fg_color=NeonTheme.BG_BLACK)

        # Center on parent
        dialog.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - 200
        y = self.winfo_y() + (self.winfo_height() // 2) - 75
        dialog.geometry(f"+{x}+{y}")

        ctk.CTkLabel(
            dialog,
            text=message,
            font=ctk.CTkFont(size=14),
            wraplength=350,
            text_color=NeonTheme.SECONDARY_PINK
        ).pack(pady=30)

        ctk.CTkButton(
            dialog,
            text="OK",
            command=dialog.destroy,
            width=100,
            fg_color=NeonTheme.BUTTON_DANGER,
            hover_color=NeonTheme.BUTTON_DANGER_HOVER
        ).pack(pady=10)
