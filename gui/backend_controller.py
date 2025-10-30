# gui/backend_controller.py

import logging
import threading
from typing import Callable, Optional, List, Dict
from datetime import datetime

# Import voice assistant modules
from voice_assistant.audio import record_audio, play_audio
from voice_assistant.transcription import transcribe_audio
from voice_assistant.response_generation import generate_response
from voice_assistant.text_to_speech import text_to_speech
from voice_assistant.config import Config
from voice_assistant.api_key_manager import (
    get_transcription_api_key,
    get_response_api_key,
    get_tts_api_key
)

logger = logging.getLogger(__name__)


class BackendController:
    """
    Controller that manages the voice assistant backend operations.
    Handles threading and coordinates between GUI and backend services.
    """

    def __init__(self):
        """Initialize the backend controller."""
        self.is_recording = False
        self.is_processing = False
        self.chat_history: List[Dict[str, str]] = [
            {
                "role": "system",
                "content": """You are a helpful Assistant called Verbi.
                You are friendly and fun and you will help the users with their requests.
                Your answers are short and concise."""
            }
        ]

        # Callbacks for UI updates
        self.on_status_update: Optional[Callable[[str], None]] = None
        self.on_animation_update: Optional[Callable[[str], None]] = None
        self.on_message_add: Optional[Callable[[str, str], None]] = None
        self.on_error: Optional[Callable[[str], None]] = None

        # Validate configuration
        try:
            Config.validate_config()
            logger.info("Configuration validated successfully")
        except Exception as e:
            logger.error(f"Configuration validation failed: {e}")

    def set_callbacks(
        self,
        on_status_update: Callable[[str], None],
        on_animation_update: Callable[[str], None],
        on_message_add: Callable[[str, str], None],
        on_error: Callable[[str], None]
    ):
        """
        Set callback functions for UI updates.

        Args:
            on_status_update: Callback for status text updates
            on_animation_update: Callback for animation state changes
            on_message_add: Callback for adding messages to chat
            on_error: Callback for error handling
        """
        self.on_status_update = on_status_update
        self.on_animation_update = on_animation_update
        self.on_message_add = on_message_add
        self.on_error = on_error

    def start_conversation(self):
        """Start a new voice conversation cycle."""
        if self.is_processing:
            logger.warning("Already processing a conversation")
            return

        # Run in background thread to avoid blocking UI
        thread = threading.Thread(target=self._conversation_thread, daemon=True)
        thread.start()

    def _conversation_thread(self):
        """Background thread that handles the full conversation flow."""
        try:
            self.is_processing = True

            # Step 1: Record audio
            if not self._record_audio():
                return

            # Step 2: Transcribe
            user_text = self._transcribe_audio()
            if not user_text:
                return

            # Step 3: Generate response
            response_text = self._generate_response(user_text)
            if not response_text:
                return

            # Step 4: Text-to-speech
            self._text_to_speech(response_text)

        except Exception as e:
            logger.error(f"Error in conversation thread: {e}", exc_info=True)
            if self.on_error:
                self.on_error(f"Conversation error: {str(e)}")
        finally:
            self.is_processing = False
            if self.on_status_update:
                self.on_status_update("Ready")
            if self.on_animation_update:
                self.on_animation_update("idle")

    def _record_audio(self) -> bool:
        """
        Record audio from microphone.

        Returns:
            bool: True if recording successful, False otherwise
        """
        try:
            if self.on_status_update:
                self.on_status_update("Listening...")
            if self.on_animation_update:
                self.on_animation_update("listening")

            logger.info("Starting audio recording...")
            record_audio(Config.INPUT_AUDIO)
            logger.info("Audio recording complete")
            return True

        except Exception as e:
            logger.error(f"Recording failed: {e}", exc_info=True)
            if self.on_error:
                self.on_error(f"Recording failed: {str(e)}")
            return False

    def _transcribe_audio(self) -> Optional[str]:
        """
        Transcribe recorded audio to text.

        Returns:
            str: Transcribed text, or None if failed
        """
        try:
            if self.on_status_update:
                self.on_status_update("Transcribing...")
            if self.on_animation_update:
                self.on_animation_update("thinking")

            logger.info("Transcribing audio...")
            transcription_api_key = get_transcription_api_key()
            user_text = transcribe_audio(
                Config.TRANSCRIPTION_MODEL,
                transcription_api_key,
                Config.INPUT_AUDIO,
                Config.LOCAL_MODEL_PATH
            )

            if not user_text:
                logger.warning("Empty transcription received")
                if self.on_status_update:
                    self.on_status_update("No speech detected")
                return None

            logger.info(f"Transcription: {user_text}")

            # Add user message to chat
            if self.on_message_add:
                self.on_message_add(user_text, "user")

            # Add to chat history
            self.chat_history.append({"role": "user", "content": user_text})

            return user_text

        except Exception as e:
            logger.error(f"Transcription failed: {e}", exc_info=True)
            if self.on_error:
                self.on_error(f"Transcription failed: {str(e)}")
            return None

    def _generate_response(self, user_text: str) -> Optional[str]:
        """
        Generate LLM response to user input.

        Args:
            user_text: The user's transcribed text

        Returns:
            str: LLM response text, or None if failed
        """
        try:
            if self.on_status_update:
                self.on_status_update("Thinking...")
            if self.on_animation_update:
                self.on_animation_update("thinking")

            logger.info("Generating response...")
            response_api_key = get_response_api_key()
            response_text = generate_response(
                Config.RESPONSE_MODEL,
                response_api_key,
                self.chat_history,
                Config.LOCAL_MODEL_PATH
            )

            logger.info(f"Response: {response_text}")

            # Add assistant message to chat
            if self.on_message_add:
                self.on_message_add(response_text, "assistant")

            # Add to chat history
            self.chat_history.append({"role": "assistant", "content": response_text})

            return response_text

        except Exception as e:
            logger.error(f"Response generation failed: {e}", exc_info=True)
            if self.on_error:
                self.on_error(f"Response generation failed: {str(e)}")
            return None

    def _text_to_speech(self, text: str) -> bool:
        """
        Convert text to speech and play it.

        Args:
            text: The text to convert to speech

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if self.on_status_update:
                self.on_status_update("Speaking...")
            if self.on_animation_update:
                self.on_animation_update("speaking")

            # Determine output file format
            if Config.TTS_MODEL in ['openai', 'elevenlabs', 'melotts', 'cartesia']:
                output_file = 'output.mp3'
            else:
                output_file = 'output.wav'

            logger.info("Generating speech...")
            tts_api_key = get_tts_api_key()
            text_to_speech(
                Config.TTS_MODEL,
                tts_api_key,
                text,
                output_file,
                Config.LOCAL_MODEL_PATH
            )

            # Play audio (skip for cartesia as it streams)
            if Config.TTS_MODEL != "cartesia":
                logger.info("Playing audio...")
                play_audio(output_file)

            logger.info("Speech playback complete")
            return True

        except Exception as e:
            logger.error(f"Text-to-speech failed: {e}", exc_info=True)
            if self.on_error:
                self.on_error(f"Text-to-speech failed: {str(e)}")
            return False

    def clear_history(self):
        """Clear the conversation history."""
        self.chat_history = [
            {
                "role": "system",
                "content": """You are a helpful Assistant called Verbi.
                You are friendly and fun and you will help the users with their requests.
                Your answers are short and concise."""
            }
        ]
        logger.info("Chat history cleared")

    def stop(self):
        """Stop any ongoing operations."""
        self.is_processing = False
        logger.info("Backend controller stopped")
