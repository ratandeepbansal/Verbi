# VERBI STUDIO - AI Voice Assistant with Modern GUI 🎙️✨

> **A desktop GUI application built on top of the amazing [Verbi](https://github.com/PromtEngineer/Verbi) project by PromtEngineer**

Verbi Studio is a feature-rich desktop application that brings a beautiful, modern graphical interface to the powerful Verbi voice assistant. Built with CustomTkinter, it offers an intuitive way to interact with multiple AI providers through voice, with real-time animations, visual feedback, and comprehensive settings management.

## What's New in Verbi Studio 🆕

- 🖥️ **Modern Desktop UI**: Clean, dark-themed interface with smooth animations
- 🎨 **Visual Status Indicators**: Animated pulsing, spinning, and wave effects
- ⚙️ **Comprehensive Settings Panel**: Easy API configuration with visual status testing
- 💾 **Conversation Management**: Save, load, and export your conversations
- ⌨️ **Keyboard Shortcuts**: Quick access to all features
- 📦 **Standalone macOS App**: Build as a native .app bundle
- 🎯 **Multiple AI Providers**: Switch between OpenAI, Groq, Deepgram, ElevenLabs, and Cartesia

## Credits & Original Project 🙏

This project is built upon the excellent foundation of **[Verbi](https://github.com/PromtEngineer/Verbi)** created by [PromtEngineer](https://github.com/PromtEngineer). Verbi Studio extends the original CLI-based voice assistant with a complete GUI implementation while maintaining all the modular design and API flexibility that makes Verbi great.

**Original Verbi Project:**
- Repository: https://github.com/PromtEngineer/Verbi
- Creator: [@PromtEngineer](https://github.com/PromtEngineer)

<p align="center">
<a href="https://trendshift.io/repositories/11584" target="_blank"><img src="https://trendshift.io/api/badge/repositories/11584" alt="PromtEngineer%2FVerbi | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>
</p>

## Motivation ✨✨✨

Welcome to the Voice Assistant project! 🎙️ Our goal is to create a modular voice assistant application that allows you to experiment with state-of-the-art (SOTA) models for various components. The modular structure provides flexibility, enabling you to pick and choose between different SOTA models for transcription, response generation, and text-to-speech (TTS). This approach facilitates easy testing and comparison of different models, making it an ideal platform for research and development in voice assistant technologies. Whether you're a developer, researcher, or enthusiast, this project is for you!

## Features 🧰

- **Modular Design**: Easily switch between different models for transcription, response generation, and TTS.
- **Support for Multiple APIs**: Integrates with OpenAI, Groq, and Deepgram APIs, along with placeholders for local models.
- **Audio Recording and Playback**: Record audio from the microphone and play generated speech.
- **Configuration Management**: Centralized configuration in `config.py` for easy setup and management.

## Project Structure 📂

```plaintext
voice_assistant/
├── voice_assistant/
│   ├── __init__.py
│   ├── audio.py
│   ├── api_key_manager.py
│   ├── config.py
│   ├── transcription.py
│   ├── response_generation.py
│   ├── text_to_speech.py
│   ├── utils.py
│   ├── local_tts_api.py
│   ├── local_tts_generation.py
├── .env
├── run_voice_assistant.py
├── piper_server.py
├── setup.py
├── requirements.txt
└── README.md
```

## Setup Instructions  📋

#### Prerequisites ✅

- Python 3.10 or higher
- Virtual environment (recommended)

#### Step-by-Step Instructions 🔢

1. 📥 **Clone the repository**

```shell
   git clone https://github.com/PromtEngineer/Verbi.git
   cd Verbi
```
2. 🐍 **Set up a virtual environment**

  Using `venv`:

```shell
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
  Using `conda`:

```shell
    conda create --name verbi python=3.10
    conda activate verbi
```
3.  📦 **Install the required packages**

```shell
   pip install -r requirements.txt
```
4. 🛠️ **Set up the environment variables**

Create a  `.env` file in the root directory and add your API keys:
```shell
    OPENAI_API_KEY=your_openai_api_key
    GROQ_API_KEY=your_groq_api_key
    DEEPGRAM_API_KEY=your_deepgram_api_key
    LOCAL_MODEL_PATH=path/to/local/model
    PIPER_SERVER_URL=server_url
```
5. 🧩 **Configure the models**

Edit config.py to select the models you want to use:

```shell
    class Config:
        # Model selection
        TRANSCRIPTION_MODEL = 'groq'  # Options: 'openai', 'groq', 'deepgram', 'fastwhisperapi' 'local'
        RESPONSE_MODEL = 'groq'       # Options: 'openai', 'groq', 'ollama', 'local'
        TTS_MODEL = 'deepgram'        # Options: 'openai', 'deepgram', 'elevenlabs', 'local', 'melotts', 'piper'

        # API keys and paths
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
        LOCAL_MODEL_PATH = os.getenv("LOCAL_MODEL_PATH")
```

If you are running LLM locally via [Ollama](https://ollama.com/), make sure the Ollama server is runnig before starting verbi. 

6. 🔊 **Configure ElevenLabs Jarvis' Voice**
- Voice samples [here](https://github.com/PromtEngineer/Verbi/tree/main/voice_samples).
- Follow this [link](https://elevenlabs.io/app/voice-lab/share/de3746fa51a09e771604d74b5d1ff6797b6b96a5958f9de95cef544dde31dad9/WArWzu0z4mbSyy5BfRKM) to add the Jarvis voice to your ElevenLabs account.
- Name the voice 'Paul J.' or, if you prefer a different name, ensure it matches the ELEVENLABS_VOICE_ID variable in the text_to_speech.py file.

7. 🏃 **Run the voice assistant**

```shell
   python run_voice_assistant.py
```
8. 🎤 **Install FastWhisperAPI**

   _Optional step if you need a local transcription model_

   ***Clone the repository***
   ```shell
      cd..
      git clone https://github.com/3choff/FastWhisperAPI.git
      cd FastWhisperAPI
   ```
   ***Install the required packages:***
   ```shell
      pip install -r requirements.txt
   ```
   ***Run the API***
   ```shell
      fastapi run main.py
   ```
   ***Alternative Setup and Run Methods***

   The API can also run directly on a Docker container or in Google Colab.

   ***Docker:***

   ***Build a Docker container:***
   ```shell
      docker build -t fastwhisperapi .
   ```
   ***Run the container***
   ```shell
      docker run -p 8000:8000 fastwhisperapi
   ```
   Refer to the repository documentation for the Google Colab method: https://github.com/3choff/FastWhisperAPI/blob/main/README.md

8. 🎤 **Install Local TTS - MeloTTS**

   _Optional step if you need a local Text to Speech model_

   ***Install MeloTTS from Github***

   Use the following [link](https://github.com/myshell-ai/MeloTTS/blob/main/docs/install.md#linux-and-macos-install) to install MeloTTS for your operating system. 

   Once the package is installed on your local virtual environment, you can start the api server using the following command. 
   ```shell
      python voice_assistant/local_tts_api.py
   ```
   The `local_tts_api.py` file implements as fastapi server that will listen to incoming text and will generate audio using MeloTTS model. 
   In order to use the local TTS model, you will need to update the `config.py` file by setting: 

   ```shell
      TTS_MODEL = 'melotts'        # Options: 'openai', 'deepgram', 'elevenlabs', 'local', 'melotts', 'piper'
   ```

9. 🎤 **Install Local TTS - Piper**

   _A faster and lightweight alternative to MeloTTS_

   ***Download the Piper Binary and the voice from Github***

   Use the following [link](https://github.com/rhasspy/piper) to install Piper Binary for your operating system.

   Use the following [link](https://github.com/rhasspy/piper?tab=readme-ov-file#voices) to download Piper voices.
   Each voice will have two files:
   | `.onnx` | Actual voice model |
   | `.onnx.json` | Model configuration |

   For example:

   ```shell
   models/en_US-lessac-medium/
   ├── en_US-lessac-medium.onnx
   ├── en_US-lessac-medium.onnx.json
   ```

   Once the binary and voice is downloaded on your system, edit the `piper_server.py` and provide the binary and voice paths.
   ```shell
      piper_executable = "./piper/piper"  #example path to the piper binary 
      model_path = "en_US-lessac-medium.onnx" #example path to the .onnx file
   ```

   You can start the api server using the following command. 
   ```shell
      python piper_server.py
   ```

   The `piper_server.py` file implements as fastapi server that will listen to incoming text and will generate audio using Piper model. 
   In order to use the local TTS model, you will need to update the `config.py` file by setting: 

   ```shell
      TTS_MODEL = 'piper'        # Options: 'openai', 'deepgram', 'elevenlabs', 'local', 'melotts','piper'
   ```
   You can run the main file to start using verbi with local models.

## GUI Application - Verbi Studio 🖥️

### Running the GUI

To run the Verbi Studio GUI version:

```shell
python run_gui.py
```

### GUI Features

- **Modern Interface**: Clean, dark-themed UI with smooth animations and visual feedback
- **Visual Status Indicators**:
  - 🎧 Pulsing indicator when listening
  - 🔄 Spinning indicator when thinking
  - 🌊 Wave indicator when speaking
- **Settings Panel**: Easy configuration of API keys and model selection for all providers
- **API Status Testing**: Test all configured APIs with one click to verify connectivity
- **Conversation Management**:
  - Save conversations in JSON format
  - Load previous conversations
  - Export as text or markdown
- **Keyboard Shortcuts**:
  - `Space` - Push to talk
  - `Cmd/Ctrl + K` - Clear conversation
  - `Cmd/Ctrl + ,` - Open settings
  - `Escape` - Stop current action

### Building macOS App Bundle

Build Verbi Studio as a standalone macOS application:

1. **Ensure all dependencies are installed**:
```shell
pip install -r requirements.txt
```

2. **Build the app bundle**:
```shell
pyinstaller verbi.spec --clean --noconfirm
```

3. **Find your app**:
The `Verbi.app` will be created in the `dist/` directory. You can:
- Double-click `Verbi.app` to run it
- Drag it to your Applications folder
- Run from terminal: `./dist/Verbi.app/Contents/MacOS/Verbi`

**Note**: The app bundle is ~133MB and includes all dependencies. No Python installation required to run the bundled app.

### Custom App Icon

To add a custom icon to Verbi Studio:

1. Create or obtain a `.icns` file (macOS app icon format)
2. Place it in the `assets/` directory as `icon.icns`
3. Rebuild with PyInstaller

See `assets/ICON_README.md` for detailed instructions on creating `.icns` files.

### System Requirements

- **macOS**: 10.13 (High Sierra) or higher
- **Python**: 3.10 or higher (for development; not required for bundled app)
- **Microphone**: Required for voice input
- **Internet**: Required for API-based models

### Troubleshooting

**App won't launch:**
- Grant microphone permission: System Preferences > Security & Privacy > Privacy > Microphone
- Ensure API keys are configured in Settings panel or `.env` file

**API errors:**
- Verify API keys in Settings > API Keys section
- Use "Test All APIs" button to check connectivity
- Check internet connection

**Audio issues:**
- Verify microphone permission is granted
- Check System Preferences > Sound > Input
- Ensure microphone is not being used by another application

## Model Options ⚙️

#### Transcription Models  🎤

- **OpenAI**: Uses OpenAI's Whisper model.
- **Groq**: Uses Groq's Whisper-large-v3 model.
- **Deepgram**: Uses Deepgram's transcription model.
- **FastWhisperAPI**: Uses FastWhisperAPI, a local transcription API powered by Faster Whisper.
- **Local**: Placeholder for a local speech-to-text (STT) model.

#### Response Generation Models  💬

- **OpenAI**: Uses OpenAI's GPT-4 model.
- **Groq**: Uses Groq's LLaMA model.
- **Ollama**: Uses any model served via Ollama.
- **Local**: Placeholder for a local language model.

#### Text-to-Speech (TTS) Models  🔊

- **OpenAI**: Uses OpenAI's TTS model with the 'fable' voice.
- **Deepgram**: Uses Deepgram's TTS model with the 'aura-angus-en' voice.
- **ElevenLabs**: Uses ElevenLabs' TTS model with the 'Paul J.' voice.
- **Local**: Placeholder for a local TTS model.

## Detailed Module Descriptions  📘

- **`run_verbi.py`**: Main script to run the voice assistant.
- **`voice_assistant/config.py`**: Manages configuration settings and API keys.
- **`voice_assistant/api_key_manager.py`**: Handles retrieval of API keys based on configured models.
- **`voice_assistant/audio.py`**: Functions for recording and playing audio.
- **`voice_assistant/transcription.py`**: Manages audio transcription using various APIs.
- **`voice_assistant/response_generation.py`**: Handles generating responses using various language models.
- **`voice_assistant/text_to_speech.py`**: Manages converting text responses into speech.
- **`voice_assistant/utils.py`**: Contains utility functions like deleting files.
- **`voice_assistant/local_tts_api.py`**: Contains the api implementation to run the MeloTTS model.
- **`voice_assistant/local_tts_generation.py`**: Contains the code to use the MeloTTS api to generated audio.
- **`voice_assistant/__init__.py`**: Initializes the `voice_assistant` package.

## Roadmap 🛤️🛤️🛤️

Here's what's next for the Voice Assistant project:

1. **Add Support for Streaming**: Enable real-time streaming of audio input and output.
2. **Add Support for ElevenLabs and Enhanced Deepgram for TTS**: Integrate additional TTS options for higher quality and variety.
3. **Add Filler Audios**: Include background or filler audios while waiting for model responses to enhance user experience.
4. **Add Support for Local Models Across the Board**: Expand support for local models in transcription, response generation, and TTS.

## Contributing 🤝

We welcome contributions from the community! If you'd like to help improve this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request detailing your changes.

## Star History ✨✨✨

[![Star History Chart](https://api.star-history.com/svg?repos=PromtEngineer/Verbi&type=Date)](https://star-history.com/#PromtEngineer/Verbi&Date)


