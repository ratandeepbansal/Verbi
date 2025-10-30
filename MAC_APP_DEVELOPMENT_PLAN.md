# Verbi macOS App Development Plan

## Overview

This document outlines the plan to package Verbi into a native macOS application with a Siri-like graphical interface.

## Recommended Tech Stack

### GUI Framework: **CustomTkinter**
- Modern, macOS-native appearance
- Easy to learn and implement
- Perfect for Siri-like interface design
- Built-in dark/light mode support
- No licensing issues (LGPL)

### Packaging Tool: **PyInstaller**
- Better dependency handling for audio libraries
- Mature and well-documented
- Creates native macOS .app bundles
- Cross-platform (future-proof)

---

## Step-by-Step Development Plan

### Phase 1: Setup & Basic GUI Foundation

#### Step 1.1: Environment Setup
- Install CustomTkinter: `pip install customtkinter`
- Install PyInstaller: `pip install pyinstaller`
- Create new `gui/` directory for UI components

#### Step 1.2: Basic Window & Layout
- Create main window with CustomTkinter
- Design basic layout (header, chat area, controls)
- Add app icon and branding
- Test window opens and closes properly

**Deliverable:** Empty GUI window that launches

---

### Phase 2: Core UI Components

#### Step 2.1: Chat Display Area
- Create scrollable text area for conversation history
- Design message bubbles (user vs assistant)
- Add timestamps to messages
- Implement auto-scroll to latest message

#### Step 2.2: Visual Feedback Indicators
- Add "listening" animation (pulsing circle/wave)
- Add "thinking" spinner/loading indicator
- Add "speaking" animation
- Status label showing current state

#### Step 2.3: Control Buttons
- Push-to-talk button (press to record)
- Stop/cancel button
- Clear conversation button
- Settings button

**Deliverable:** Full UI mockup with visual states

---

### Phase 3: Backend Integration

#### Step 3.1: Connect Audio Recording
- Integrate existing `audio.py` functions
- Trigger recording on button press
- Show visual feedback during recording
- Handle recording errors gracefully

#### Step 3.2: Connect Transcription
- Display transcribed text in chat area
- Show loading state during transcription
- Handle empty/failed transcriptions
- Display user message bubble

#### Step 3.3: Connect LLM Response
- Show "thinking" indicator while generating
- Display assistant response in chat bubble
- Handle API errors with user-friendly messages
- Add retry logic

#### Step 3.4: Connect Text-to-Speech
- Play audio response automatically
- Show "speaking" animation during playback
- Add option to stop playback mid-speech
- Handle TTS errors

**Deliverable:** Fully functional voice assistant with GUI

---

### Phase 4: Settings & Configuration

#### Step 4.1: Settings Panel
- Create settings window/sidebar
- Add dropdown for transcription model selection
- Add dropdown for LLM model selection
- Add dropdown for TTS model selection

#### Step 4.2: API Key Management
- Add secure text fields for API keys
- Save settings to local config file
- Load settings on app start
- Validate API keys before saving

#### Step 4.3: Audio Settings
- Microphone selection dropdown
- Audio output device selection
- Volume controls
- Test audio button

**Deliverable:** Configurable settings without editing code

---

### Phase 5: Enhanced Features

#### Step 5.1: Keyboard Shortcuts
- Space bar to talk (push-to-talk)
- Cmd+K to clear conversation
- Cmd+, to open settings
- Esc to cancel/stop

#### Step 5.2: Conversation Management
- Save conversation history to file
- Load previous conversations
- Export conversation as text/markdown
- Clear history confirmation dialog

#### Step 5.3: Polish & UX Improvements
- Add app menu bar (File, Edit, View, Help)
- Add "About" dialog with version info
- Add sound effects (beep on recording start/stop)
- Add system notifications for responses
- Remember window size/position

**Deliverable:** Polished user experience

---

### Phase 6: Packaging & Distribution

#### Step 6.1: PyInstaller Configuration
- Create `verbi.spec` file
- Configure app icon (.icns file)
- Include all data files and dependencies
- Test basic bundle creation

#### Step 6.2: Fix Packaging Issues
- Debug missing dependencies
- Add hidden imports for audio libraries
- Configure file permissions
- Test on clean macOS installation

#### Step 6.3: Code Signing & Notarization (Optional)
- Get Apple Developer account
- Create signing certificate
- Sign the application
- Notarize with Apple
- Create DMG installer

#### Step 6.4: Documentation
- Create user guide
- Document system requirements
- Create installation instructions
- Add troubleshooting section

**Deliverable:** Distributable macOS .app bundle

---

## Proposed Project Structure

```
Verbi/
├── voice_assistant/        # Existing backend
│   ├── audio.py
│   ├── transcription.py
│   ├── response_generation.py
│   └── ...
├── gui/                    # New GUI components
│   ├── __init__.py
│   ├── main_window.py     # Main GUI window
│   ├── chat_area.py       # Chat display widget
│   ├── controls.py        # Buttons and controls
│   ├── settings_window.py # Settings dialog
│   ├── animations.py      # Visual feedback animations
│   └── themes.py          # Color schemes and styling
├── assets/                 # New assets folder
│   ├── icons/             # App icons
│   ├── sounds/            # Sound effects
│   └── images/            # UI images
├── run_gui.py             # New GUI entry point
├── verbi.spec             # PyInstaller spec file
└── requirements-gui.txt   # GUI-specific dependencies
```

---

## Estimated Timeline

- **Phase 1:** 2-3 hours
- **Phase 2:** 4-6 hours
- **Phase 3:** 6-8 hours
- **Phase 4:** 4-5 hours
- **Phase 5:** 4-6 hours
- **Phase 6:** 3-5 hours

**Total:** ~23-33 hours of development

---

## Development Approach

Build this **incrementally**, testing each phase before moving to the next. Start with Phase 1 to get a basic window running, then gradually add features based on feedback.

---

## Technical Considerations

### Dependencies
- CustomTkinter for modern UI
- PyInstaller for packaging
- Existing voice_assistant modules (audio, transcription, LLM, TTS)
- PyAudio, pygame for audio I/O
- Threading for non-blocking UI during processing

### Challenges to Address
- Audio library compatibility with PyInstaller
- Thread-safe UI updates from background tasks
- Proper resource cleanup (audio devices, API connections)
- Cross-version Python compatibility
- macOS permissions (microphone access)

### User Experience Goals
- Responsive UI (never freeze during processing)
- Clear visual feedback for all states
- Graceful error handling with helpful messages
- Intuitive controls requiring minimal learning
- Native macOS look and feel

---

## Next Steps

1. Install required dependencies
2. Create `gui/` directory structure
3. Implement Phase 1: Basic window
4. Test and iterate on each phase
5. Gather user feedback between phases
6. Package and distribute

---

*Last Updated: 2025-10-31*
