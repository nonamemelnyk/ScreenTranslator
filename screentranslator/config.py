"""
Configuration module for ScreenTranslator.
Handles loading environment variables, command-line arguments, and providing configuration settings.
"""

import os
import sys
from dotenv import load_dotenv


class Config:
    """Configuration class for ScreenTranslator."""

    def __init__(self, args=None):
        """
        Initialize configuration from environment variables and command-line arguments.

        Args:
            args: Optional list of command-line arguments. If None, sys.argv is used.
        """
        # Load environment variables
        load_dotenv()

        # Parse command-line arguments
        cmd_args = self._parse_args(args if args is not None else sys.argv[1:])

        # Translation settings
        self.translation_service = cmd_args.get('TRANSLATION_SERVICE') or os.getenv('TRANSLATION_SERVICE', 'google')
        self.source_language = cmd_args.get('DEFAULT_SOURCE_LANGUAGE') or os.getenv('DEFAULT_SOURCE_LANGUAGE', 'en')
        self.target_language = cmd_args.get('DEFAULT_TARGET_LANGUAGE') or os.getenv('DEFAULT_TARGET_LANGUAGE', 'es')

        # Screenshot settings
        self.screenshot_provider = cmd_args.get('SCREENSHOT_PROVIDER') or os.getenv('SCREENSHOT_PROVIDER', 'pyautogui')

        # Text recognition settings
        self.text_recognition_provider = cmd_args.get('TEXT_RECOGNITION_PROVIDER') or os.getenv('TEXT_RECOGNITION_PROVIDER', 'tesseract')

        # Text insertion settings
        self.text_insertion_provider = cmd_args.get('TEXT_INSERTION_PROVIDER') or os.getenv('TEXT_INSERTION_PROVIDER', 'pil')
        insert_text_value = cmd_args.get('INSERT_TRANSLATED_TEXT') or os.getenv('INSERT_TRANSLATED_TEXT', 'True')
        self.insert_translated_text = insert_text_value.lower() == 'true'

        # Debug settings
        debug_mode_value = cmd_args.get('DEBUG_MODE') or os.getenv('DEBUG_MODE', 'False')
        self.debug_mode = debug_mode_value.lower() == 'true'
        self.log_level = cmd_args.get('LOG_LEVEL') or os.getenv('LOG_LEVEL', 'INFO')

    def _parse_args(self, args):
        """
        Parse command-line arguments in the format --KEY=VALUE.

        Args:
            args: List of command-line arguments

        Returns:
            Dictionary of parsed arguments
        """
        result = {}
        for arg in args:
            if arg.startswith('--'):
                try:
                    key, value = arg[2:].split('=', 1)
                    result[key] = value
                except ValueError:
                    # If there's no value, treat it as a flag
                    result[arg[2:]] = 'True'
        return result

    def display(self):
        """Display the current configuration."""
        print("ScreenTranslator Configuration:")
        print(f"Translation Service: {self.translation_service}")
        print(f"Source Language: {self.source_language}")
        print(f"Target Language: {self.target_language}")
        print(f"Screenshot Provider: {self.screenshot_provider}")
        print(f"Text Recognition Provider: {self.text_recognition_provider}")
        print(f"Text Insertion Provider: {self.text_insertion_provider}")
        print(f"Insert Translated Text: {self.insert_translated_text}")
        print(f"Debug Mode: {self.debug_mode}")
        print(f"Log Level: {self.log_level}")
