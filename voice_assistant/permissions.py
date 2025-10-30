# voice_assistant/permissions.py

import logging
import platform
import sys

logger = logging.getLogger(__name__)


def check_microphone_permission():
    """
    Check if the application has microphone permission.

    Returns:
        bool: True if permission is granted, False otherwise
    """
    if platform.system() != 'Darwin':  # Not macOS
        return True

    try:
        # Try to import PyObjC modules for AVFoundation
        import AVFoundation

        # Check current authorization status
        auth_status = AVFoundation.AVCaptureDevice.authorizationStatusForMediaType_(
            AVFoundation.AVMediaTypeAudio
        )

        # Status values:
        # 0 = AVAuthorizationStatusNotDetermined
        # 1 = AVAuthorizationStatusRestricted
        # 2 = AVAuthorizationStatusDenied
        # 3 = AVAuthorizationStatusAuthorized

        if auth_status == 3:  # Authorized
            logger.info("Microphone permission: Granted")
            return True
        elif auth_status == 0:  # Not determined
            logger.warning("Microphone permission: Not determined (will prompt on first use)")
            return True  # Will prompt automatically
        else:
            logger.error(f"Microphone permission: Denied (status={auth_status})")
            return False

    except ImportError:
        logger.warning("PyObjC not available, cannot check microphone permission")
        # If PyObjC is not installed, assume permission is OK
        # The system will prompt automatically when accessing microphone
        return True
    except Exception as e:
        logger.error(f"Error checking microphone permission: {e}")
        return True  # Assume OK and let the system handle it


def request_microphone_permission():
    """
    Request microphone permission from the user.
    This will trigger the system permission dialog on first access.

    Returns:
        bool: True if permission granted or will be prompted, False if denied
    """
    if platform.system() != 'Darwin':  # Not macOS
        return True

    try:
        import AVFoundation
        import AppKit
        from PyObjCTools import AppHelper

        # Check current status
        auth_status = AVFoundation.AVCaptureDevice.authorizationStatusForMediaType_(
            AVFoundation.AVMediaTypeAudio
        )

        if auth_status == 3:  # Already authorized
            logger.info("Microphone permission already granted")
            return True
        elif auth_status in [1, 2]:  # Restricted or Denied
            logger.error("Microphone permission denied. Please enable it in System Settings.")
            return False

        # Request permission (auth_status == 0, not determined)
        logger.info("Requesting microphone permission...")

        # This will trigger the permission dialog
        def completion_handler(granted):
            if granted:
                logger.info("Microphone permission granted by user")
            else:
                logger.error("Microphone permission denied by user")

        AVFoundation.AVCaptureDevice.requestAccessForMediaType_completionHandler_(
            AVFoundation.AVMediaTypeAudio,
            completion_handler
        )

        return True

    except ImportError:
        logger.warning("PyObjC not available for permission request")
        return True  # System will handle permission prompt automatically
    except Exception as e:
        logger.error(f"Error requesting microphone permission: {e}")
        return True


def open_system_preferences_microphone():
    """
    Open System Settings to the Microphone privacy page.
    """
    if platform.system() != 'Darwin':
        return

    try:
        import subprocess
        # Open System Settings to Privacy & Security > Microphone
        subprocess.run([
            'open',
            'x-apple.systempreferences:com.apple.preference.security?Privacy_Microphone'
        ])
        logger.info("Opened System Settings for microphone permissions")
    except Exception as e:
        logger.error(f"Failed to open System Settings: {e}")


def get_permission_instructions():
    """
    Get user-friendly instructions for granting microphone permission.

    Returns:
        str: Instructions text
    """
    if platform.system() != 'Darwin':
        return "Please ensure your microphone is connected and working."

    return """To grant microphone permission:

1. Open System Settings
2. Go to Privacy & Security
3. Select Microphone
4. Enable permission for Python or Terminal

Then restart the application."""
