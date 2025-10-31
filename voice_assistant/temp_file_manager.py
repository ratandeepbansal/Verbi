"""
Centralized temporary file manager for VoxVibe.

Handles creation, tracking, and cleanup of temporary audio files.
"""

import os
import logging
from pathlib import Path
from typing import List, Set

logger = logging.getLogger(__name__)


class TempFileManager:
    """Manages temporary files for the application."""

    _instance = None
    _temp_files: Set[str] = set()

    def __new__(cls):
        """Singleton pattern to ensure only one instance."""
        if cls._instance is None:
            cls._instance = super(TempFileManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize the temp file manager."""
        if not hasattr(self, '_initialized'):
            self._temp_files = set()
            self._initialized = True

    def register_temp_file(self, file_path: str) -> str:
        """
        Register a temporary file for tracking.

        Args:
            file_path: Path to the temporary file

        Returns:
            str: The file path
        """
        self._temp_files.add(file_path)
        logger.debug(f"Registered temp file: {file_path}")
        return file_path

    def get_output_file(self, file_format: str) -> str:
        """
        Get a temp file path for output with the specified format.

        Args:
            file_format: File extension (e.g., 'mp3', 'wav', 'aiff')

        Returns:
            str: Path to the temp output file
        """
        file_path = f"output.{file_format}"
        return self.register_temp_file(file_path)

    def get_input_file(self, file_format: str = 'mp3') -> str:
        """
        Get a temp file path for input/recording.

        Args:
            file_format: File extension (default: 'mp3')

        Returns:
            str: Path to the temp input file
        """
        file_path = f"test.{file_format}"
        return self.register_temp_file(file_path)

    def cleanup_file(self, file_path: str) -> bool:
        """
        Remove a specific temporary file.

        Args:
            file_path: Path to the file to remove

        Returns:
            bool: True if file was removed, False otherwise
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Removed temp file: {file_path}")
                if file_path in self._temp_files:
                    self._temp_files.remove(file_path)
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to remove temp file {file_path}: {e}")
            return False

    def cleanup_all(self) -> int:
        """
        Remove all registered temporary files.

        Returns:
            int: Number of files removed
        """
        removed_count = 0
        files_to_remove = list(self._temp_files)

        for file_path in files_to_remove:
            if self.cleanup_file(file_path):
                removed_count += 1

        logger.info(f"Cleaned up {removed_count} temporary files")
        return removed_count

    def get_temp_files(self) -> List[str]:
        """
        Get list of all registered temporary files.

        Returns:
            List[str]: List of temp file paths
        """
        return list(self._temp_files)


# Global instance
temp_file_manager = TempFileManager()
