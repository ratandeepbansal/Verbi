# voice_assistant/transcription.py

import json
import logging
import requests
import time

from colorama import Fore, init
from openai import OpenAI
from groq import Groq
from deepgram import DeepgramClient
from faster_whisper import WhisperModel

fast_url = "http://localhost:8000"
checked_fastwhisperapi = False

# Cache for faster-whisper model to avoid reloading
_faster_whisper_model_cache = {}

def check_fastwhisperapi():
    """Check if the FastWhisper API is running."""
    global checked_fastwhisperapi, fast_url
    if not checked_fastwhisperapi:
        infopoint = f"{fast_url}/info"
        try:
            response = requests.get(infopoint)
            if response.status_code != 200:
                raise Exception("FastWhisperAPI is not running")
        except Exception:
            raise Exception("FastWhisperAPI is not running")
        checked_fastwhisperapi = True

def transcribe_audio(model, api_key, audio_file_path, local_model_path=None):
    """
    Transcribe an audio file using the specified model.
    
    Args:
        model (str): The model to use for transcription ('openai', 'groq', 'deepgram', 'fastwhisper', 'local').
        api_key (str): The API key for the transcription service.
        audio_file_path (str): The path to the audio file to transcribe.
        local_model_path (str): The path to the local model (if applicable).

    Returns:
        str: The transcribed text.
    """
    try:
        if model == 'openai':
            return _transcribe_with_openai(api_key, audio_file_path)
        elif model == 'groq':
            return _transcribe_with_groq(api_key, audio_file_path)
        elif model == 'deepgram':
            return _transcribe_with_deepgram(api_key, audio_file_path)
        elif model == 'fastwhisperapi':
            return _transcribe_with_fastwhisperapi(audio_file_path)
        elif model == 'faster-whisper':
            return _transcribe_with_faster_whisper(audio_file_path, local_model_path)
        elif model == 'local':
            # Placeholder for local STT model transcription
            return "Transcribed text from local model"
        else:
            raise ValueError("Unsupported transcription model")
    except Exception as e:
        logging.error(f"{Fore.RED}Failed to transcribe audio: {e}{Fore.RESET}")
        raise Exception("Error in transcribing audio")

def _transcribe_with_openai(api_key, audio_file_path):
    client = OpenAI(api_key=api_key)
    with open(audio_file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language='en'
        )
    return transcription.text


def _transcribe_with_groq(api_key, audio_file_path):
    client = Groq(api_key=api_key)
    with open(audio_file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-large-v3",
            file=audio_file,
            language='en'
        )
    return transcription.text


def _transcribe_with_deepgram(api_key, audio_file_path):
    try:
        from deepgram import DeepgramClient

        # Initialize client with API key
        client = DeepgramClient(api_key=api_key)

        # Read and transcribe audio file
        with open(audio_file_path, "rb") as audio_file:
            response = client.listen.v1.media.transcribe_file(
                request=audio_file.read(),
                model="nova-2",
                smart_format=True
            )

        # Extract transcript from response
        transcript = response.results.channels[0].alternatives[0].transcript
        return transcript

    except Exception as e:
        logging.error(f"{Fore.RED}Deepgram transcription error: {e}{Fore.RESET}")
        raise


def _transcribe_with_fastwhisperapi(audio_file_path):
    check_fastwhisperapi()
    endpoint = f"{fast_url}/v1/transcriptions"

    files = {'file': (audio_file_path, open(audio_file_path, 'rb'))}
    data = {
        'model': "base",
        'language': "en",
        'initial_prompt': None,
        'vad_filter': True,
    }
    headers = {'Authorization': 'Bearer dummy_api_key'}

    response = requests.post(endpoint, files=files, data=data, headers=headers)
    response_json = response.json()
    return response_json.get('text', 'No text found in the response.')


def _transcribe_with_faster_whisper(audio_file_path, model_size=None):
    """
    Transcribe audio using faster-whisper (local Whisper model).

    Args:
        audio_file_path (str): Path to the audio file
        model_size (str): Model size ('tiny', 'base', 'small', 'medium', 'large-v3')
                         If None, uses Config.FASTER_WHISPER_MODEL

    Returns:
        str: The transcribed text
    """
    try:
        from voice_assistant.config import Config

        # Use provided model size or default from config
        # Ignore if model_size looks like a file path (contains '/')
        if model_size is None or '/' in str(model_size) or model_size == '':
            model_size = Config.FASTER_WHISPER_MODEL

        # Check if model is already cached
        global _faster_whisper_model_cache
        if model_size not in _faster_whisper_model_cache:
            logging.info(f"Loading faster-whisper model: {model_size}")
            # Load model with optimal settings for Mac
            # compute_type="int8" for CPU, "float16" for GPU
            model = WhisperModel(
                model_size,
                device="cpu",
                compute_type="int8",
                download_root=None  # Uses default cache directory
            )
            _faster_whisper_model_cache[model_size] = model
            logging.info(f"Model {model_size} loaded successfully")
        else:
            model = _faster_whisper_model_cache[model_size]

        # Transcribe audio
        segments, info = model.transcribe(
            audio_file_path,
            beam_size=5,
            language="en",
            vad_filter=True,  # Voice activity detection
            vad_parameters=dict(min_silence_duration_ms=500)
        )

        # Combine all segments into a single transcript
        transcript = " ".join([segment.text for segment in segments])

        logging.info(f"Detected language '{info.language}' with probability {info.language_probability}")

        return transcript.strip()

    except Exception as e:
        logging.error(f"{Fore.RED}faster-whisper transcription error: {e}{Fore.RESET}")
        raise