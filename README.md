# VoxVibe 🎙️✨

**A Native macOS Desktop App for AI Voice Conversations**
*Vibe-coded with Claude AI*

> Built on top of the excellent [Verbi](https://github.com/PromtEngineer/Verbi) voice assistant by [@PromtEngineer](https://github.com/PromtEngineer)

![macOS](https://img.shields.io/badge/macOS-10.13+-blue)
![Python](https://img.shields.io/badge/python-3.10+-green)
![AI-Coded](https://img.shields.io/badge/AI--Coded-Claude-purple)
![License](https://img.shields.io/badge/license-MIT-blue)

<p align="center">
  <img src="assets/images/screenshot.jpg" alt="VoxVibe Neon Theme" width="800">
  <br>
  <em>VoxVibe with the new cyberpunk neon theme</em>
</p>

## About This Project 📖

**VoxVibe** is a macOS GUI fork of Verbi that transforms the powerful CLI voice assistant into a beautiful, native desktop application. This entire GUI implementation was vibe-coded with Claude AI, bringing modern design and user experience to voice-based AI interactions.

While Verbi provides the excellent backend foundation with its modular AI provider architecture, VoxVibe adds:

- 🖥️ **Native macOS Application** - Built with CustomTkinter for a modern, polished interface
- 🎨 **Visual Feedback** - Animated status indicators (pulsing, spinning, wave effects)
- ⚙️ **Settings Panel** - Easy API configuration with one-click connectivity testing
- 💾 **Conversation Management** - Save, load, and export your conversations
- ⌨️ **Keyboard Shortcuts** - Efficient navigation and control
- 📦 **Standalone .app Bundle** - No Python installation required for end users

## Original Verbi Project 🙏

This project would not exist without the amazing work of **[@PromtEngineer](https://github.com/PromtEngineer)** on the original **[Verbi](https://github.com/PromtEngineer/Verbi)** voice assistant.

**Original Verbi:**
- **Repository**: https://github.com/PromtEngineer/Verbi
- **Creator**: [@PromtEngineer](https://github.com/PromtEngineer)
- **What it does**: Modular voice assistant with CLI interface supporting multiple AI providers

<p align="center">
<a href="https://trendshift.io/repositories/11584" target="_blank"><img src="https://trendshift.io/api/badge/repositories/11584" alt="PromtEngineer%2FVerbi | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>
</p>

**All credit for the core voice assistant functionality, modular architecture, and AI provider integrations goes to the original Verbi project.**

## What VoxVibe Adds 🆕

This fork focuses specifically on creating a native macOS desktop experience, entirely vibe-coded with AI:

### GUI Implementation (Phases 1-3)
- **Phase 1**: Basic GUI foundation with CustomTkinter
  - Modern dark-themed interface
  - Record button with visual feedback
  - Chat display area for conversations

- **Phase 2**: Core UI components with animations
  - Message bubbles (user/assistant styling)
  - Animated status indicators (listening/thinking/speaking)
  - Auto-scroll and timestamps

- **Phase 3**: Backend integration
  - Connected GUI to Verbi's audio, transcription, LLM, and TTS modules
  - Threaded processing for non-blocking UI
  - Real-time status updates

### Enhanced Features (Phases 4-5)
- **Phase 4**: Settings & Configuration
  - Visual settings panel for API keys and model selection
  - API connectivity testing for all 5 providers
  - Persistent configuration storage

- **Phase 5**: Enhanced UX
  - Menu bar (File, Edit, View, Help)
  - Keyboard shortcuts (Space, Cmd+K, Cmd+,, Esc)
  - Conversation save/load/export (JSON, text, markdown)
  - Confirmation dialogs and About screen
  - Window geometry persistence

### Packaging (Phase 6)
- **Phase 6**: macOS App Bundle
  - PyInstaller configuration for standalone .app
  - ~133MB bundle with all dependencies included
  - Info.plist with proper permissions and metadata
  - No Python installation required to run

### Neon Theme (Latest Update) ✨
- **Cyberpunk Aesthetic**: Complete UI redesign with neon colors
  - Pure black (#000000) background for maximum contrast
  - Neon green (#00FF41) as primary color (Matrix-style)
  - Secondary neon colors: Cyan, Purple, Pink for accents
- **Enhanced Animations**: Smooth 30fps animations with elegant easing
  - Pulsing indicator (listening): Neon green with sine wave motion
  - Spinner indicator (thinking): Neon purple with optimized timing
  - Wave indicator (speaking): Neon cyan with fluid motion
- **Consistent Styling**: Professional design across all windows
  - Message bubbles with neon accent borders
  - Settings panel with themed buttons and status indicators
  - Dialog boxes with cohesive neon styling
- **Visual Hierarchy**: Thoughtful use of color for better UX
  - Success states: Neon green
  - Error states: Neon pink
  - Processing states: Neon purple

## Quick Start 🚀

### Prerequisites
- macOS 10.13 (High Sierra) or higher
- Python 3.10+ (for development)
- API keys from at least one provider (OpenAI, Groq, Deepgram, ElevenLabs, or Cartesia)

### Installation

1. **Clone this repository**:
```bash
git clone https://github.com/ratandeepbansal/VoxVibe.git
cd VoxVibe
```

2. **Set up virtual environment**:
```bash
python -m venv venv
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Configure API keys**:
Create a `.env` file:
```bash
OPENAI_API_KEY=your_key_here
GROQ_API_KEY=your_key_here
DEEPGRAM_API_KEY=your_key_here
ELEVENLABS_API_KEY=your_key_here
CARTESIA_API_KEY=your_key_here
```

5. **Run VoxVibe**:
```bash
python run_gui.py
```

## Building macOS App 📦

Build VoxVibe as a standalone macOS application:

```bash
# Ensure dependencies are installed
pip install -r requirements.txt

# Build the app
pyinstaller verbi.spec --clean --noconfirm

# Your app is ready!
# Location: dist/Verbi.app
```

The resulting `Verbi.app` can be:
- Double-clicked to run
- Moved to Applications folder
- Distributed to other Macs (no Python required)

**App size**: ~133MB (includes all dependencies)

### Custom App Icon

To add a custom icon:
1. Create/obtain a `.icns` file
2. Place it as `assets/icon.icns`
3. Rebuild with PyInstaller

See `assets/ICON_README.md` for creating `.icns` files.

## Features 🎯

### Core Features (from Verbi)
- **Modular AI Providers**: Switch between OpenAI, Groq, Deepgram, ElevenLabs, Cartesia
- **Voice Recording**: High-quality audio capture with noise calibration
- **Transcription**: Multiple STT options (Whisper, Groq, Deepgram)
- **LLM Response**: OpenAI GPT-4, Groq LLaMA, or local models via Ollama
- **Text-to-Speech**: Natural voices from OpenAI, Deepgram, ElevenLabs, Cartesia

### GUI Features (VoxVibe)
- **Visual Status** (Neon Theme):
  - 🎧 Pulsing neon green when listening
  - 🔄 Spinning neon purple when thinking
  - 🌊 Waving neon cyan when speaking

- **Settings Panel**:
  - API key configuration with neon styling
  - Model selection per provider
  - One-click API testing with color-coded results

- **Conversation Management**:
  - Save as JSON for later loading
  - Export as plain text
  - Export as markdown

- **Keyboard Shortcuts**:
  - `Space` - Start/stop recording
  - `Cmd/Ctrl + K` - Clear conversation
  - `Cmd/Ctrl + ,` - Open settings
  - `Escape` - Stop current action

## Project Structure 📂

```
VoxVibe/
├── gui/                          # GUI implementation (VoxVibe)
│   ├── main_window.py           # Main application window
│   ├── settings_window.py       # Settings panel
│   ├── chat_area.py             # Chat display
│   ├── animations.py            # Status indicators
│   ├── theme.py                 # Neon theme configuration
│   ├── dialogs.py               # Reusable dialogs
│   └── backend_controller.py    # GUI-backend bridge
├── voice_assistant/              # Core voice functionality (from Verbi)
│   ├── audio.py                 # Recording and playback
│   ├── transcription.py         # STT integration
│   ├── response_generation.py   # LLM integration
│   ├── text_to_speech.py        # TTS integration
│   ├── config.py                # Configuration
│   └── api_tester.py            # API connectivity testing
├── assets/                       # App resources
│   └── ICON_README.md           # Icon instructions
├── run_gui.py                    # GUI entry point
├── run_voice_assistant.py        # CLI entry point (original)
├── verbi.spec                    # PyInstaller config
└── requirements.txt              # Dependencies
```

## Supported AI Providers ⚙️

| Provider | Transcription | LLM | Text-to-Speech |
|----------|--------------|-----|----------------|
| **OpenAI** | ✅ Whisper | ✅ GPT-4 | ✅ TTS |
| **Groq** | ✅ Whisper-large-v3 | ✅ LLaMA | ❌ |
| **Deepgram** | ✅ Nova-2 | ❌ | ✅ Aura |
| **ElevenLabs** | ❌ | ❌ | ✅ Premium voices |
| **Cartesia** | ❌ | ❌ | ✅ Sonic |
| **Ollama** | ❌ | ✅ Local models | ❌ |

## Troubleshooting 🔧

### App won't launch
- **Microphone permission**: System Preferences > Security & Privacy > Privacy > Microphone
- **API keys**: Configure in Settings panel or `.env` file

### API errors
- Verify keys in Settings > API Keys
- Click "Test All APIs" to check connectivity
- Ensure internet connection is active

### Audio issues
- Check microphone permission
- System Preferences > Sound > Input
- Ensure mic isn't used by another app

## Development 🛠️

### Running from source
```bash
source venv/bin/activate
python run_gui.py
```

### Running CLI version (original Verbi)
```bash
source venv/bin/activate
python run_voice_assistant.py
```

## Roadmap & Future Enhancements 🚀

### ✅ Completed Enhancements
- **Neon Theme** 🌈 (Latest Update)
  - ✅ Dark theme with vibrant neon colors (cyberpunk aesthetic)
  - ✅ Dynamic and responsive animations at 30fps
  - ✅ Smooth transitions between states with elegant easing
  - ✅ Consistent color scheme across all windows
  - ⏳ Glassmorphism effects (Future)
  - ⏳ Customizable color schemes (Future)
  - ⏳ Particle effects during voice interaction (Future)

### Potential Future Improvements
Features being considered for VoxVibe:

### Web Application Version 🌐
- **Browser-Based VoxVibe**
  - Port to web using Streamlit, Flask, or FastAPI + React
  - Access from any device with a browser
  - Real-time WebSocket communication for voice streaming
  - Responsive design for mobile and tablet
  - Cloud deployment options (Vercel, Railway, Render)
  - Multi-user support with authentication
  - Shareable conversation links

### Local Models Integration ⚡
- **LM Studio SDK Integration**
  - Use local models via LM Studio for ultra-low latency
  - Local transcription (Whisper models)
  - Local LLM inference (Llama, Mistral, etc.)
  - Local text-to-speech (Piper, Coqui TTS)
  - Eliminate API costs and dependencies
  - Privacy-focused - all processing on-device
  - Offline capability
  - Fine-tuned models for specific use cases

### Additional Features Under Consideration
- Real-time voice activity detection (VAD) for automatic recording
- Multi-language support
- Voice profile customization
- Conversation analytics and insights
- Plugin/extension system
- Windows and Linux GUI versions
- iOS/Android mobile apps

**Want to contribute?** These are great starting points for PRs!

## Contributing 🤝

This is a fork focused on macOS GUI implementation. For contributions:

- **GUI/macOS features**: Submit PRs to this repository
- **Core voice assistant features**: Consider contributing to the [original Verbi project](https://github.com/PromtEngineer/Verbi)

## License 📄

This project maintains the same license as the original Verbi project.

## Acknowledgments 🙏

- **[@PromtEngineer](https://github.com/PromtEngineer)** - Creator of [Verbi](https://github.com/PromtEngineer/Verbi), the foundation of this project
- **CustomTkinter** - For the modern GUI framework
- **PyInstaller** - For macOS app bundling
- All the AI providers (OpenAI, Groq, Deepgram, ElevenLabs, Cartesia) for their excellent APIs

---

**VoxVibe** = [Verbi](https://github.com/PromtEngineer/Verbi)'s voice assistant + macOS native GUI ❤️
