#!/usr/bin/env python3
"""
Test script for pyttsx3 local TTS
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_pyttsx3_direct():
    """Test pyttsx3 directly"""
    print("\n" + "="*60)
    print("TEST 1: Direct pyttsx3 Test")
    print("="*60)

    try:
        import pyttsx3

        print("✓ pyttsx3 imported successfully")

        # Initialize engine
        engine = pyttsx3.init()
        print("✓ pyttsx3 engine initialized")

        # Get available voices
        voices = engine.getProperty('voices')
        print(f"\n✓ Available voices: {len(voices)}")
        for i, voice in enumerate(voices[:3]):  # Show first 3
            print(f"  {i}: {voice.name} ({voice.id})")

        # Test speech generation
        test_file = "/tmp/test_pyttsx3.mp3"
        test_text = "Hello! This is a test of pyttsx3 text to speech."

        print(f"\nGenerating speech...")
        engine.save_to_file(test_text, test_file)
        engine.runAndWait()

        # Check if file was created
        if os.path.exists(test_file):
            file_size = os.path.getsize(test_file)
            print(f"✓ Audio file created: {test_file}")
            print(f"  File size: {file_size} bytes")
            os.unlink(test_file)  # Clean up
        else:
            print("❌ Audio file was not created")
            return False

        print("\n✅ Direct pyttsx3 test: SUCCESS!")
        return True

    except Exception as e:
        print(f"\n❌ Direct pyttsx3 test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_pyttsx3_via_voice_assistant():
    """Test pyttsx3 through voice_assistant module"""
    print("\n" + "="*60)
    print("TEST 2: pyttsx3 via voice_assistant Module")
    print("="*60)

    try:
        from voice_assistant.text_to_speech import text_to_speech

        print("✓ voice_assistant.text_to_speech imported")

        test_file = "/tmp/test_voice_assistant_pyttsx3.mp3"
        test_text = "Testing pyttsx3 through the voice assistant module."

        print(f"\nGenerating speech via text_to_speech()...")
        text_to_speech(
            model="pyttsx3",
            api_key=None,  # Not needed for pyttsx3
            text=test_text,
            output_file_path=test_file
        )

        # Check if file was created
        if os.path.exists(test_file):
            file_size = os.path.getsize(test_file)
            print(f"✓ Audio file created: {test_file}")
            print(f"  File size: {file_size} bytes")
            os.unlink(test_file)  # Clean up
        else:
            print("❌ Audio file was not created")
            return False

        print("\n✅ Voice assistant module test: SUCCESS!")
        return True

    except Exception as e:
        print(f"\n❌ Voice assistant module test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_full_local_pipeline():
    """Test complete local pipeline"""
    print("\n" + "="*60)
    print("TEST 3: Full Local Pipeline Test")
    print("="*60)

    try:
        from voice_assistant.config import Config

        # Load config
        Config.load_from_file()

        print(f"\n📋 Current Configuration:")
        print(f"  Transcription: {Config.TRANSCRIPTION_MODEL}")
        print(f"  LLM: {Config.RESPONSE_MODEL}")
        print(f"  TTS: {Config.TTS_MODEL}")

        # Check if all are local
        is_local_stt = Config.TRANSCRIPTION_MODEL == 'faster-whisper'
        is_local_llm = Config.RESPONSE_MODEL == 'lmstudio'
        is_local_tts = Config.TTS_MODEL == 'pyttsx3'

        print(f"\n✅ Local STT: {'Yes' if is_local_stt else 'No'} ({Config.TRANSCRIPTION_MODEL})")
        print(f"✅ Local LLM: {'Yes' if is_local_llm else 'No'} ({Config.RESPONSE_MODEL})")
        print(f"✅ Local TTS: {'Yes' if is_local_tts else 'No'} ({Config.TTS_MODEL})")

        if is_local_stt and is_local_llm and is_local_tts:
            print("\n🎉 100% LOCAL PIPELINE CONFIGURED!")
            print("\n✅ Full local pipeline test: SUCCESS!")
            return True
        else:
            print("\n⚠️  Not fully local yet. Update settings to:")
            if not is_local_stt:
                print("  - Set Transcription Model to: faster-whisper")
            if not is_local_llm:
                print("  - Set Response Model to: lmstudio")
            if not is_local_tts:
                print("  - Set TTS Model to: pyttsx3")
            return False

    except Exception as e:
        print(f"\n❌ Full pipeline test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("PYTTSX3 LOCAL TTS TEST SUITE")
    print("="*60)

    results = {
        "direct": test_pyttsx3_direct(),
        "voice_assistant": test_pyttsx3_via_voice_assistant(),
        "full_pipeline": test_full_local_pipeline()
    }

    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    for name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{name:20s}: {status}")

    all_pass = all(results.values())

    if all_pass:
        print("\n🎉 All tests passed! pyttsx3 local TTS is ready!")
        print("\nTo use in VoxVibe:")
        print("1. Open Settings (Cmd+,)")
        print("2. Set TTS Model to: pyttsx3")
        print("3. Save and test!")
        print("\n💡 Complete local pipeline:")
        print("  Voice → faster-whisper → LM Studio → pyttsx3 → Audio")
        print("  100% private, 100% free, 100% offline!")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
