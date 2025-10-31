#!/usr/bin/env python3
"""
Detailed diagnostic test for local models integration
"""

import sys
import os
import logging

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_faster_whisper_detailed():
    """Detailed test of faster-whisper with actual audio"""
    print("\n" + "="*60)
    print("DETAILED FASTER-WHISPER TEST")
    print("="*60)

    try:
        from voice_assistant.transcription import transcribe_audio, _transcribe_with_faster_whisper
        from voice_assistant.config import Config
        import tempfile
        import wave
        import numpy as np

        print(f"✓ Imports successful")
        print(f"✓ Config.FASTER_WHISPER_MODEL = {Config.FASTER_WHISPER_MODEL}")

        # Create a test audio file (1 second of silence)
        print("\nCreating test audio file...")
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            test_audio_path = f.name

        # Generate 1 second of silent audio at 16kHz
        sample_rate = 16000
        duration = 1.0
        samples = np.zeros(int(sample_rate * duration), dtype=np.int16)

        with wave.open(test_audio_path, 'w') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(samples.tobytes())

        print(f"✓ Test audio created: {test_audio_path}")

        # Test direct function call
        print("\nTesting _transcribe_with_faster_whisper directly...")
        try:
            result = _transcribe_with_faster_whisper(test_audio_path)
            print(f"✓ Direct call successful")
            print(f"  Result: '{result}'")
        except Exception as e:
            print(f"❌ Direct call failed: {e}")
            import traceback
            traceback.print_exc()

        # Test via transcribe_audio function
        print("\nTesting transcribe_audio with 'faster-whisper' model...")
        try:
            result = transcribe_audio(
                model='faster-whisper',
                api_key=None,
                audio_file_path=test_audio_path
            )
            print(f"✓ transcribe_audio successful")
            print(f"  Result: '{result}'")
        except Exception as e:
            print(f"❌ transcribe_audio failed: {e}")
            import traceback
            traceback.print_exc()

        # Cleanup
        os.unlink(test_audio_path)
        print("\n✅ faster-whisper detailed test completed")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


def test_lmstudio_detailed():
    """Detailed test of LM Studio integration"""
    print("\n" + "="*60)
    print("DETAILED LM STUDIO TEST")
    print("="*60)

    try:
        from voice_assistant.response_generation import generate_response, _generate_lmstudio_response
        from voice_assistant.config import Config
        import lmstudio as lms

        print(f"✓ Imports successful")
        print(f"✓ Config.LMSTUDIO_BASE_URL = {Config.LMSTUDIO_BASE_URL}")

        # Test 1: Direct SDK test
        print("\nTest 1: Testing LM Studio SDK directly...")
        try:
            model = lms.llm()
            print(f"✓ LM Studio SDK connection successful")

            # Simple test
            response = model.respond("Say 'Hello' and nothing else.")
            print(f"✓ Direct SDK response: '{response}'")
        except Exception as e:
            print(f"❌ Direct SDK failed: {e}")
            import traceback
            traceback.print_exc()
            return

        # Test 2: Test _generate_lmstudio_response directly
        print("\nTest 2: Testing _generate_lmstudio_response function...")
        try:
            test_history = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'Test successful' in 2 words."}
            ]
            result = _generate_lmstudio_response(test_history)
            print(f"✓ _generate_lmstudio_response successful")
            print(f"  Result: '{result}'")
        except Exception as e:
            print(f"❌ _generate_lmstudio_response failed: {e}")
            import traceback
            traceback.print_exc()

        # Test 3: Test via generate_response function
        print("\nTest 3: Testing generate_response with 'lmstudio' model...")
        try:
            test_history = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Reply with only the word 'SUCCESS'"}
            ]
            result = generate_response(
                model='lmstudio',
                api_key=None,
                chat_history=test_history
            )
            print(f"✓ generate_response successful")
            print(f"  Result: '{result}'")
        except Exception as e:
            print(f"❌ generate_response failed: {e}")
            import traceback
            traceback.print_exc()

        print("\n✅ LM Studio detailed test completed")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


def test_config_loading():
    """Test configuration loading"""
    print("\n" + "="*60)
    print("CONFIGURATION TEST")
    print("="*60)

    try:
        from voice_assistant.config import Config
        import os

        print("\nCurrent Configuration:")
        print(f"  TRANSCRIPTION_MODEL: {Config.TRANSCRIPTION_MODEL}")
        print(f"  RESPONSE_MODEL: {Config.RESPONSE_MODEL}")
        print(f"  TTS_MODEL: {Config.TTS_MODEL}")
        print(f"  LMSTUDIO_BASE_URL: {Config.LMSTUDIO_BASE_URL}")
        print(f"  FASTER_WHISPER_MODEL: {Config.FASTER_WHISPER_MODEL}")

        # Check if config file exists
        config_file = ".verbi_config.json"
        if os.path.exists(config_file):
            print(f"\n✓ Config file exists: {config_file}")
            import json
            with open(config_file, 'r') as f:
                settings = json.load(f)
                print("\nConfig file contents:")
                for key, value in settings.items():
                    if 'key' not in key.lower():  # Don't print API keys
                        print(f"  {key}: {value}")
        else:
            print(f"\n⚠️  No config file found at: {config_file}")

        print("\n✅ Configuration test completed")

    except Exception as e:
        print(f"\n❌ Configuration test failed: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Run all detailed tests"""
    print("\n" + "="*60)
    print("DETAILED INTEGRATION DIAGNOSTIC")
    print("="*60)

    test_config_loading()
    test_lmstudio_detailed()
    test_faster_whisper_detailed()

    print("\n" + "="*60)
    print("DIAGNOSTIC COMPLETE")
    print("="*60)


if __name__ == "__main__":
    main()
