#!/usr/bin/env python3
"""
Test script for local models integration (LM Studio + faster-whisper)
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_lmstudio():
    """Test LM Studio connection and chat completion"""
    print("\n" + "="*60)
    print("TESTING LM STUDIO INTEGRATION")
    print("="*60)

    try:
        import lmstudio as lms
        from voice_assistant.config import Config

        print(f"✓ LM Studio SDK imported successfully")
        print(f"✓ Connecting to: {Config.LMSTUDIO_BASE_URL}")

        # Test connection and model (LM Studio SDK uses simple API)
        model = lms.llm()

        print(f"✓ Connected to LM Studio server")
        print(f"✓ Model loaded successfully")

        # Test simple chat
        print("\nTesting chat completion...")
        test_chat_history = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say 'Hello! LM Studio integration is working!' in one sentence."}
        ]

        from voice_assistant.response_generation import generate_response
        response = generate_response(
            model='lmstudio',
            api_key=None,  # Not needed for LM Studio
            chat_history=test_chat_history
        )

        print(f"\n✓ LM Studio Response: {response}")
        print("\n✅ LM Studio integration: SUCCESS!")
        return True

    except Exception as e:
        print(f"\n❌ LM Studio integration FAILED: {e}")
        print("\nTroubleshooting:")
        print("1. Is LM Studio running?")
        print("2. Is the server started (Developer tab)?")
        print("3. Is a model loaded in LM Studio?")
        print("4. Is the port correct (default: 1234)?")
        return False


def test_faster_whisper():
    """Test faster-whisper local transcription"""
    print("\n" + "="*60)
    print("TESTING FASTER-WHISPER INTEGRATION")
    print("="*60)

    try:
        from faster_whisper import WhisperModel
        from voice_assistant.config import Config

        print(f"✓ faster-whisper imported successfully")
        print(f"✓ Model size: {Config.FASTER_WHISPER_MODEL}")

        # Test model loading (will download on first run)
        print(f"\nLoading Whisper model '{Config.FASTER_WHISPER_MODEL}'...")
        print("(This may take a few minutes on first run to download the model)")

        model = WhisperModel(
            Config.FASTER_WHISPER_MODEL,
            device="cpu",
            compute_type="int8"
        )

        print(f"✓ Model loaded successfully")
        print("\n✅ faster-whisper integration: SUCCESS!")
        print("\nNote: To test transcription, record audio using the GUI")
        return True

    except Exception as e:
        print(f"\n❌ faster-whisper integration FAILED: {e}")
        print("\nTroubleshooting:")
        print("1. Is faster-whisper installed? (pip install faster-whisper)")
        print("2. Do you have enough disk space for model download?")
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("LOCAL MODELS INTEGRATION TEST")
    print("="*60)

    results = {
        "lmstudio": test_lmstudio(),
        "faster_whisper": test_faster_whisper()
    }

    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    for name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{name:20s}: {status}")

    all_pass = all(results.values())

    if all_pass:
        print("\n🎉 All tests passed! Local models integration is ready.")
        print("\nNext steps:")
        print("1. Open VoxVibe GUI: python run_gui.py")
        print("2. Go to Settings (Cmd+,)")
        print("3. Set Response Model to 'lmstudio'")
        print("4. Set Transcription Model to 'faster-whisper'")
        print("5. Save and start chatting!")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
