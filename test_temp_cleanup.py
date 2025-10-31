#!/usr/bin/env python3
"""
Test script for temporary file cleanup functionality.
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from voice_assistant.temp_file_manager import temp_file_manager


def test_temp_file_manager():
    """Test the temp file manager functionality."""
    print("=" * 60)
    print("TEMP FILE MANAGER TEST")
    print("=" * 60)

    # Test 1: Register some temp files
    print("\nTest 1: Registering temp files...")
    file1 = temp_file_manager.get_output_file('mp3')
    file2 = temp_file_manager.get_output_file('wav')
    file3 = temp_file_manager.get_input_file('mp3')

    print(f"✓ Registered: {file1}")
    print(f"✓ Registered: {file2}")
    print(f"✓ Registered: {file3}")

    # Create actual files
    print("\nTest 2: Creating temporary files...")
    for file_path in [file1, file2, file3]:
        with open(file_path, 'w') as f:
            f.write("test data")
        print(f"✓ Created: {file_path}")

    # Check registered files
    print(f"\nTest 3: Checking registered files...")
    registered = temp_file_manager.get_temp_files()
    print(f"✓ Total registered files: {len(registered)}")
    for f in registered:
        exists = "✓ EXISTS" if os.path.exists(f) else "✗ MISSING"
        print(f"  {f} - {exists}")

    # Test cleanup
    print(f"\nTest 4: Testing cleanup...")
    removed = temp_file_manager.cleanup_all()
    print(f"✓ Cleaned up {removed} files")

    # Verify cleanup
    print(f"\nTest 5: Verifying cleanup...")
    for file_path in [file1, file2, file3]:
        if os.path.exists(file_path):
            print(f"✗ File still exists: {file_path}")
        else:
            print(f"✓ File removed: {file_path}")

    registered_after = temp_file_manager.get_temp_files()
    print(f"\n✓ Registered files after cleanup: {len(registered_after)}")

    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    test_temp_file_manager()
