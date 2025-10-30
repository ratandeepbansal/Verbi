#!/usr/bin/env python3
# run_gui.py

"""
Entry point for Verbi GUI application.

This script launches the graphical user interface for the Verbi voice assistant.
"""

import sys
import os
import logging

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from gui.main_window import VerbiMainWindow

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Main entry point for the GUI application."""
    try:
        logger.info("Starting Verbi GUI application...")
        app = VerbiMainWindow()
        app.mainloop()
        logger.info("Application closed successfully")
    except Exception as e:
        logger.error(f"Error running GUI application: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
