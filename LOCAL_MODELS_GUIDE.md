# Local Models Integration Guide 🚀

## Overview

VoxVibe now supports **fully local AI models** for complete privacy and zero API costs! This guide will help you set up and use:

- **LM Studio** - Local LLM for chat responses
- **faster-whisper** - Local speech-to-text transcription

## Benefits ✨

- 🔒 **Complete Privacy** - All processing happens on your device
- 💰 **Zero API Costs** - No usage fees or API key required
- ⚡ **Low Latency** - Fast responses without internet roundtrips
- 🌐 **Offline Capable** - Works without internet connection
- 🎯 **Full Control** - Choose your own models

---

## Part 1: LM Studio Setup (LLM)

### What is LM Studio?

LM Studio allows you to run powerful language models locally on your Mac.

### Installation Steps

1. **Download LM Studio**
   - Visit: [https://lmstudio.ai](https://lmstudio.ai)
   - Download the macOS version
   - Install the app

2. **Download a Model**
   - Open LM Studio
   - Go to **"Search"** tab (🔍)
   - **Recommended models** (choose ONE):
     - `Qwen/Qwen2.5-7B-Instruct-GGUF` (7B, balanced)
     - `microsoft/Phi-3-mini-4k-instruct-gguf` (3.8B, fast) ✅
     - `meta-llama/Llama-3.2-3B-Instruct-GGUF` (3B, efficient)
   - Click **Download**
   - Wait for download to complete (~2-4GB)

3. **Load the Model**
   - Go to **"Chat"** tab
   - Select your downloaded model from dropdown
   - Wait for model to load

4. **Start Local Server**
   - Go to **"Developer"** tab
   - Click **"Start Server"**
   - Confirm it shows: `Running on port 1234`
   - ✅ Keep LM Studio running while using VoxVibe

### Testing LM Studio

```bash
# From VoxVibe directory
python test_local_models.py
```

You should see: `✅ LM Studio integration: SUCCESS!`

---

## Part 2: faster-whisper Setup (Transcription)

### What is faster-whisper?

faster-whisper is an optimized implementation of OpenAI's Whisper for local speech recognition.

### Installation

Already done! It was installed with VoxVibe dependencies:

```bash
pip install faster-whisper
```

### Model Selection

faster-whisper supports multiple model sizes:

| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| `tiny` | 75MB | ⚡⚡⚡ | ⭐⭐ | Testing |
| `base` | 145MB | ⚡⚡ | ⭐⭐⭐ | General use ✅ |
| `small` | 466MB | ⚡ | ⭐⭐⭐⭐ | Better accuracy |
| `medium` | 1.5GB | 🐢 | ⭐⭐⭐⭐⭐ | High quality |
| `large-v3` | 3GB | 🐌 | ⭐⭐⭐⭐⭐ | Best quality |

**Recommendation**: Start with `base` (default) - good balance of speed and accuracy.

### First Run Note

On first use, faster-whisper will automatically download the selected model:
- `base` model: ~145MB download
- Takes 1-2 minutes on first run
- Models are cached for future use

### Testing faster-whisper

```bash
# From VoxVibe directory
python test_local_models.py
```

You should see: `✅ faster-whisper integration: SUCCESS!`

---

## Part 3: VoxVibe Configuration

### Using the GUI

1. **Launch VoxVibe**
   ```bash
   python run_gui.py
   ```

2. **Open Settings**
   - Press `Cmd + ,` (or click menu bar → Preferences)

3. **Configure Local Models**

   **Response Model Section:**
   - Set **Response Model** to: `lmstudio`

   **Transcription Model Section:**
   - Set **Transcription Model** to: `faster-whisper`

   **Local Models Configuration Section:**
   - **LM Studio URL**: `http://localhost:1234` (default)
   - **Whisper Model**: `base` (or choose another size)

4. **Save Settings**
   - Click **"Save Settings"**
   - Settings are persisted to `.verbi_config.json`

### Manual Configuration (Optional)

Edit `.verbi_config.json`:

```json
{
    "response_model": "lmstudio",
    "transcription_model": "faster-whisper",
    "tts_model": "openai",
    "lmstudio_base_url": "http://localhost:1234",
    "faster_whisper_model": "base"
}
```

---

## Part 4: Usage Guide

### Starting a Conversation

1. **Ensure LM Studio server is running**
   - Open LM Studio
   - Go to Developer tab
   - Confirm: "Running on port 1234"

2. **Launch VoxVibe**
   ```bash
   python run_gui.py
   ```

3. **Start Recording**
   - Click the record button or press `Space`
   - Speak your message
   - Click again to stop

4. **Processing Flow**
   ```
   Your Voice → faster-whisper (local) → LM Studio (local) → TTS → Audio
   ```

### What's Still Using APIs?

By default, **Text-to-Speech (TTS)** still uses cloud APIs. You have options:

**Option 1: Keep Cloud TTS** (Recommended)
- High quality voices
- Low bandwidth usage
- Configure in Settings: OpenAI, Deepgram, ElevenLabs, or Cartesia

**Option 2: Use Local TTS**
- Already available: `melotts` or `piper`
- Set **TTS Model** to: `melotts` or `piper`
- May require additional setup (see original README)

---

## Performance Tips ⚡

### For LM Studio:

1. **Choose appropriate model size**
   - 3-4B models: Fast on any Mac
   - 7B models: Good on M1/M2/M3 Macs with 16GB+ RAM
   - 13B+ models: Requires M2/M3 Max with 32GB+ RAM

2. **Model format**
   - Use GGUF format (Quant 4-bit or 5-bit)
   - Q4_K_M is a good balance

3. **Keep LM Studio server running**
   - Don't close LM Studio during conversations
   - Model stays loaded in memory

### For faster-whisper:

1. **Model size vs speed**
   - Use `tiny` for real-time transcription
   - Use `base` for general use (recommended)
   - Use `small`/`medium` if accuracy is critical

2. **First run is slower**
   - Models download on first use
   - Subsequent runs are much faster

---

## Troubleshooting 🔧

### LM Studio Issues

**❌ "Failed to connect to LM Studio"**
- ✅ Is LM Studio running?
- ✅ Is the server started? (Developer tab → Start Server)
- ✅ Is a model loaded?
- ✅ Check port is 1234 (default)

**❌ "Model not found"**
- ✅ Load a model in LM Studio Chat tab first
- ✅ Wait for "Model loaded" message

**❌ Slow responses**
- ✅ Try a smaller model (Phi-3-mini, Llama-3.2-3B)
- ✅ Close other apps to free RAM
- ✅ Use quantized models (Q4_K_M)

### faster-whisper Issues

**❌ "Model download failed"**
- ✅ Check internet connection (for first download)
- ✅ Ensure enough disk space (~200MB - 3GB depending on model)
- ✅ Check firewall isn't blocking Hugging Face

**❌ "Transcription is slow"**
- ✅ Use smaller model (`tiny` or `base`)
- ✅ CPU-intensive on Intel Macs (consider cloud STT)
- ✅ M1/M2/M3 Macs perform much better

**❌ "Poor transcription quality"**
- ✅ Use larger model (`small` or `medium`)
- ✅ Speak clearly near microphone
- ✅ Reduce background noise

---

## Testing Everything

Run the comprehensive test:

```bash
python test_local_models.py
```

Expected output:
```
============================================================
TEST SUMMARY
============================================================
lmstudio            : ✅ PASS
faster_whisper      : ✅ PASS

🎉 All tests passed! Local models integration is ready.
```

---

## Comparison: Local vs Cloud

### Local Models (LM Studio + faster-whisper)

**Pros:**
- ✅ Complete privacy
- ✅ No API costs
- ✅ Works offline
- ✅ Low latency (after model loads)
- ✅ No rate limits

**Cons:**
- ⚠️ Requires powerful Mac (M1/M2/M3 recommended)
- ⚠️ Uses RAM (4-8GB per model)
- ⚠️ Initial model download required
- ⚠️ Slightly lower quality than GPT-4/Claude

### Cloud APIs (OpenAI, Groq, Deepgram)

**Pros:**
- ✅ Works on any device
- ✅ State-of-the-art quality
- ✅ No local resources used
- ✅ Regular model updates

**Cons:**
- ⚠️ Costs money per request
- ⚠️ Requires internet
- ⚠️ Data sent to servers
- ⚠️ Possible rate limits

---

## Hybrid Setup (Recommended) 🎯

**Best of both worlds:**

1. **Transcription**: `faster-whisper` (free, fast, local)
2. **LLM**: `lmstudio` (free, private, local)
3. **TTS**: `openai` (cheap ~$0.015/1K chars, high quality)

This setup:
- Keeps voice input private (local STT)
- Keeps conversations private (local LLM)
- Uses minimal API costs (only TTS)
- Delivers great performance

---

## System Requirements

### Minimum:
- macOS 10.13+
- 8GB RAM
- 5GB free disk space
- Intel or Apple Silicon

### Recommended:
- macOS 13+
- 16GB+ RAM
- Apple Silicon (M1/M2/M3)
- 10GB free disk space

---

## Cost Comparison 💰

### Example: 1 hour of conversation (~100 exchanges)

**Cloud (OpenAI + Deepgram + OpenAI TTS):**
- STT: ~$0.36 (1 hour audio)
- LLM: ~$0.50 (GPT-4o)
- TTS: ~$0.15
- **Total: ~$1.01/hour**

**Local (LM Studio + faster-whisper + OpenAI TTS):**
- STT: $0 (local)
- LLM: $0 (local)
- TTS: ~$0.15
- **Total: ~$0.15/hour**

**Fully Local (all local models):**
- **Total: $0/hour**

---

## Next Steps

1. ✅ Complete this setup guide
2. ✅ Run `python test_local_models.py`
3. ✅ Configure VoxVibe settings
4. ✅ Start a test conversation
5. 🎉 Enjoy private, cost-free AI conversations!

---

## Support & Feedback

Having issues? Check:
- LM Studio docs: https://lmstudio.ai/docs
- faster-whisper repo: https://github.com/SYSTRAN/faster-whisper
- VoxVibe issues: https://github.com/ratandeepbansal/VoxVibe/issues

Happy chatting! 🎙️✨
