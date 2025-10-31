# voice_assistant/api_tester.py

"""
API testing module to verify connectivity and credentials for all supported providers.
"""

import logging
from typing import Dict, Tuple

logger = logging.getLogger(__name__)


def test_openai_api(api_key: str) -> Tuple[bool, str]:
    """
    Test OpenAI API connectivity.

    Args:
        api_key: OpenAI API key

    Returns:
        Tuple of (success: bool, message: str)
    """
    if not api_key:
        return False, "API key not provided"

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)
        # Make a minimal test request
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5
        )

        if response.choices:
            return True, "Connected successfully"
        else:
            return False, "Invalid response from API"

    except Exception as e:
        error_msg = str(e)
        if "api_key" in error_msg.lower() or "authentication" in error_msg.lower():
            return False, "Invalid API key"
        elif "quota" in error_msg.lower():
            return False, "Quota exceeded"
        else:
            return False, f"Error: {error_msg[:50]}"


def test_groq_api(api_key: str) -> Tuple[bool, str]:
    """
    Test Groq API connectivity.

    Args:
        api_key: Groq API key

    Returns:
        Tuple of (success: bool, message: str)
    """
    if not api_key:
        return False, "API key not provided"

    try:
        from groq import Groq

        client = Groq(api_key=api_key)
        # Make a minimal test request
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5
        )

        if response.choices:
            return True, "Connected successfully"
        else:
            return False, "Invalid response from API"

    except Exception as e:
        error_msg = str(e)
        if "api_key" in error_msg.lower() or "authentication" in error_msg.lower() or "unauthorized" in error_msg.lower():
            return False, "Invalid API key"
        elif "quota" in error_msg.lower() or "rate" in error_msg.lower():
            return False, "Rate limit exceeded"
        else:
            return False, f"Error: {error_msg[:50]}"


def test_deepgram_api(api_key: str) -> Tuple[bool, str]:
    """
    Test Deepgram API connectivity.

    Args:
        api_key: Deepgram API key

    Returns:
        Tuple of (success: bool, message: str)
    """
    if not api_key:
        return False, "API key not provided"

    try:
        from deepgram import DeepgramClient

        # Initialize client
        client = DeepgramClient(api_key=api_key)

        # Create a minimal test audio file (1 second of silence)
        import io
        import wave

        # Create in-memory WAV file
        buffer = io.BytesIO()
        with wave.open(buffer, 'wb') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(16000)  # 16kHz
            # Write 0.1 seconds of silence
            wav_file.writeframes(b'\x00\x00' * 1600)

        buffer.seek(0)
        audio_data = buffer.read()

        # Test transcription
        response = client.listen.rest.v("1").transcribe_file(
            {"buffer": audio_data},
            {"model": "nova-2", "smart_format": True}
        )

        # Check if response has expected structure
        if hasattr(response, 'results'):
            return True, "Connected successfully"
        else:
            return False, "Invalid response from API"

    except Exception as e:
        error_msg = str(e)
        if "api_key" in error_msg.lower() or "authentication" in error_msg.lower() or "unauthorized" in error_msg.lower():
            return False, "Invalid API key"
        elif "quota" in error_msg.lower() or "insufficient" in error_msg.lower():
            return False, "Quota exceeded"
        else:
            return False, f"Error: {error_msg[:50]}"


def test_elevenlabs_api(api_key: str) -> Tuple[bool, str]:
    """
    Test ElevenLabs API connectivity.

    Args:
        api_key: ElevenLabs API key

    Returns:
        Tuple of (success: bool, message: str)
    """
    if not api_key:
        return False, "API key not provided"

    try:
        import requests

        # Test by getting available voices (lightweight API call)
        url = "https://api.elevenlabs.io/v1/voices"
        headers = {
            "xi-api-key": api_key
        }

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            return True, "Connected successfully"
        elif response.status_code == 401:
            return False, "Invalid API key"
        elif response.status_code == 429:
            return False, "Rate limit exceeded"
        else:
            return False, f"Error: Status {response.status_code}"

    except requests.exceptions.Timeout:
        return False, "Connection timeout"
    except Exception as e:
        error_msg = str(e)
        return False, f"Error: {error_msg[:50]}"


def test_cartesia_api(api_key: str) -> Tuple[bool, str]:
    """
    Test Cartesia API connectivity.

    Args:
        api_key: Cartesia API key

    Returns:
        Tuple of (success: bool, message: str)
    """
    if not api_key:
        return False, "API key not provided"

    try:
        import requests

        # Test by making a minimal TTS request
        url = "https://api.cartesia.ai/tts/bytes"
        headers = {
            "X-API-Key": api_key,
            "Cartesia-Version": "2024-06-10",
            "Content-Type": "application/json"
        }

        data = {
            "model_id": "sonic-english",
            "transcript": "test",
            "voice": {
                "mode": "id",
                "id": "a0e99841-438c-4a64-b679-ae501e7d6091"
            },
            "output_format": {
                "container": "raw",
                "encoding": "pcm_f32le",
                "sample_rate": 22050
            }
        }

        response = requests.post(url, headers=headers, json=data, timeout=10)

        if response.status_code == 200:
            return True, "Connected successfully"
        elif response.status_code == 401 or response.status_code == 403:
            return False, "Invalid API key"
        elif response.status_code == 429:
            return False, "Rate limit exceeded"
        else:
            return False, f"Error: Status {response.status_code}"

    except requests.exceptions.Timeout:
        return False, "Connection timeout"
    except Exception as e:
        error_msg = str(e)
        return False, f"Error: {error_msg[:50]}"


def test_all_apis(openai_key: str = "", groq_key: str = "", deepgram_key: str = "",
                  elevenlabs_key: str = "", cartesia_key: str = "") -> Dict[str, Tuple[bool, str]]:
    """
    Test all API providers.

    Args:
        openai_key: OpenAI API key
        groq_key: Groq API key
        deepgram_key: Deepgram API key
        elevenlabs_key: ElevenLabs API key
        cartesia_key: Cartesia API key

    Returns:
        Dictionary mapping provider name to (success, message) tuple
    """
    results = {}

    logger.info("Testing OpenAI API...")
    results["OpenAI"] = test_openai_api(openai_key)

    logger.info("Testing Groq API...")
    results["Groq"] = test_groq_api(groq_key)

    logger.info("Testing Deepgram API...")
    results["Deepgram"] = test_deepgram_api(deepgram_key)

    logger.info("Testing ElevenLabs API...")
    results["ElevenLabs"] = test_elevenlabs_api(elevenlabs_key)

    logger.info("Testing Cartesia API...")
    results["Cartesia"] = test_cartesia_api(cartesia_key)

    return results
