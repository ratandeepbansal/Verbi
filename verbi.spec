# -*- mode: python ; coding: utf-8 -*-

"""
PyInstaller spec file for Verbi Voice Assistant
"""

import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Check if icon exists
icon_path = 'assets/icon.icns' if os.path.exists('assets/icon.icns') else None

# Collect all data files from packages
datas = []
datas += collect_data_files('customtkinter')
datas += collect_data_files('pygame')

# Hidden imports for various dependencies
hiddenimports = [
    'pygame',
    'pygame.mixer',
    'speech_recognition',
    'pydub',
    'numpy',
    'sounddevice',
    'soundfile',
    'customtkinter',
    'tkinter',
    'tkinter.filedialog',
    'openai',
    'groq',
    'deepgram',
    'elevenlabs',
    'cartesia',
    'ollama',
    'requests',
    'json',
    'logging',
    'threading',
    'queue',
    'wave',
    'io',
    'os',
    'sys',
    'colorama',
    'dotenv',
    'AVFoundation',
    'Cocoa',
    'objc',
    'jaraco',
    'jaraco.text',
    'jaraco.functools',
    'jaraco.context',
    'more_itertools',
    'packaging',
    'pkg_resources',
    'platformdirs',
]

# Add submodules
hiddenimports += collect_submodules('pygame')
hiddenimports += collect_submodules('customtkinter')
hiddenimports += collect_submodules('speech_recognition')
hiddenimports += collect_submodules('deepgram')
hiddenimports += collect_submodules('pyobjc')
hiddenimports += collect_submodules('jaraco')
hiddenimports += collect_submodules('pkg_resources')

# Add local package modules explicitly
hiddenimports += [
    'gui',
    'gui.main_window',
    'gui.dialogs',
    'gui.settings_window',
    'gui.chat_area',
    'gui.animations',
    'gui.backend_controller',
    'voice_assistant',
    'voice_assistant.audio',
    'voice_assistant.transcription',
    'voice_assistant.response_generation',
    'voice_assistant.text_to_speech',
    'voice_assistant.config',
    'voice_assistant.api_tester',
    'voice_assistant.api_key_manager',
    'voice_assistant.local_tts_api',
    'voice_assistant.local_tts_generation',
    'voice_assistant.permissions',
    'voice_assistant.utils',
]

a = Analysis(
    ['run_gui.py'],
    pathex=['.'],  # Add current directory to search path
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'scipy',
        'pandas',
        'PIL',
        'IPython',
        'jupyter',
        'notebook',
        'setuptools',
        'wheel',
        'pip',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Verbi',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=True,  # Important for macOS
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Verbi',
)

app = BUNDLE(
    coll,
    name='Verbi.app',
    icon=icon_path,
    bundle_identifier='com.verbi.voiceassistant',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSHighResolutionCapable': 'True',
        'NSMicrophoneUsageDescription': 'Verbi needs access to your microphone to record voice commands.',
        'LSMinimumSystemVersion': '10.13.0',
        'CFBundleName': 'Verbi',
        'CFBundleDisplayName': 'Verbi Voice Assistant',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
        'NSRequiresAquaSystemAppearance': False,
    },
)
