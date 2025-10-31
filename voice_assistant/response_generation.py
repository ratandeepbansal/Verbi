# voice_assistant/response_generation.py

import logging

from openai import OpenAI
from groq import Groq
import ollama
import lmstudio as lms

from voice_assistant.config import Config


def generate_response(model:str, api_key:str, chat_history:list, local_model_path:str=None):
    """
    Generate a response using the specified model.
    
    Args:
    model (str): The model to use for response generation ('openai', 'groq', 'local').
    api_key (str): The API key for the response generation service.
    chat_history (list): The chat history as a list of messages.
    local_model_path (str): The path to the local model (if applicable).

    Returns:
    str: The generated response text.
    """
    try:
        if model == 'openai':
            return _generate_openai_response(api_key, chat_history)
        elif model == 'groq':
            return _generate_groq_response(api_key, chat_history)
        elif model == 'ollama':
            return _generate_ollama_response(chat_history)
        elif model == 'lmstudio':
            return _generate_lmstudio_response(chat_history)
        elif model == 'local':
            # Placeholder for local LLM response generation
            return "Generated response from local model"
        else:
            raise ValueError("Unsupported response generation model")
    except Exception as e:
        logging.error(f"Failed to generate response: {e}")
        return "Error in generating response"

def _generate_openai_response(api_key, chat_history):
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=Config.OPENAI_LLM,
        messages=chat_history
    )
    return response.choices[0].message.content


def _generate_groq_response(api_key, chat_history):
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model=Config.GROQ_LLM,
        messages=chat_history
    )
    return response.choices[0].message.content


def _generate_ollama_response(chat_history):
    response = ollama.chat(
        model=Config.OLLAMA_LLM,
        messages=chat_history,
    )
    return response['message']['content']


def _generate_lmstudio_response(chat_history):
    """
    Generate response using LM Studio local server.

    Args:
        chat_history (list): The chat history as a list of messages.

    Returns:
        str: The generated response text.
    """
    try:
        from openai import OpenAI
        from voice_assistant.config import Config

        # Use OpenAI-compatible API which properly handles message history
        client = OpenAI(
            base_url=Config.LMSTUDIO_BASE_URL + "/v1",
            api_key="lm-studio"  # LM Studio doesn't require a real API key
        )

        # Make completion request with full chat history
        completion = client.chat.completions.create(
            model="local-model",  # LM Studio uses whatever model is loaded
            messages=chat_history,
            temperature=0.7,
            max_tokens=500
        )

        response_text = completion.choices[0].message.content
        logging.info(f"Response: {response_text}")

        return response_text

    except Exception as e:
        logging.error(f"LM Studio generation error: {e}")
        raise Exception(f"Failed to generate response with LM Studio: {e}")