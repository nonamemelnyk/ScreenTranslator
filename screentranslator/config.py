"""
Configuration module for ScreenTranslator.
Handles loading environment variables, command-line arguments, and providing configuration settings.
"""

import argparse
import os
import sys
from typing import Dict, List, Optional, Union

from dotenv import load_dotenv


class Config:
    """Configuration class for ScreenTranslator."""

    def __init__(self, args: Optional[List[str]] = None):
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
        self.translation_service = self._get_config_value(
            cmd_args, "translation_service", "TRANSLATION_SERVICE", "google"
        )
        self.source_language = self._get_config_value(
            cmd_args, "source_language", "DEFAULT_SOURCE_LANGUAGE", "en"
        )
        self.target_language = self._get_config_value(
            cmd_args, "target_language", "DEFAULT_TARGET_LANGUAGE", "es"
        )

        # Screenshot settings
        self.screenshot_provider = self._get_config_value(
            cmd_args, "screenshot_provider", "SCREENSHOT_PROVIDER", "pyautogui"
        )

        # Text recognition settings
        self.text_recognition_provider = self._get_config_value(
            cmd_args, "text_recognition_provider", "TEXT_RECOGNITION_PROVIDER", "tesseract"
        )

        # Text insertion settings
        self.text_insertion_provider = self._get_config_value(
            cmd_args, "text_insertion_provider", "TEXT_INSERTION_PROVIDER", "pil"
        )
        insert_text_value = self._get_config_value(
            cmd_args, "insert_translated_text", "INSERT_TRANSLATED_TEXT", "True"
        )
        self.insert_translated_text = insert_text_value.lower() == "true"

        # Debug settings
        debug_mode_value = self._get_config_value(
            cmd_args, "debug", "DEBUG_MODE", "False"
        )
        self.debug_mode = debug_mode_value.lower() == "true"
        self.log_level = self._get_config_value(
            cmd_args, "log_level", "LOG_LEVEL", "INFO"
        )

    def _get_config_value(
        self, 
        args: Dict[str, str], 
        arg_name: str, 
        env_name: str, 
        default: str
    ) -> str:
        """
        Get configuration value from command-line arguments or environment variables.

        Args:
            args: Dictionary of command-line arguments
            arg_name: Name of the command-line argument
            env_name: Name of the environment variable
            default: Default value if not found in args or env

        Returns:
            The configuration value
        """
        return args.get(arg_name) or os.getenv(env_name, default)

    def _parse_args(self, args: List[str]) -> Dict[str, str]:
        """
        Parse command-line arguments using argparse.

        Args:
            args: List of command-line arguments

        Returns:
            Dictionary of parsed arguments
        """
        parser = argparse.ArgumentParser(
            description="ScreenTranslator - A tool for translating text from screen captures."
        )

        # Translation settings
        parser.add_argument(
            "--translation-service", 
            choices=["google", "gpt", "deepl"],
            help="Translation service to use (default: from env or 'google')"
        )
        parser.add_argument(
            "--source-language", 
            help="Source language code (default: from env or 'en')"
        )
        parser.add_argument(
            "--target-language", 
            help="Target language code (default: from env or 'es')"
        )

        # Screenshot settings
        parser.add_argument(
            "--screenshot-provider", 
            choices=["pyautogui", "pil"],
            help="Screenshot provider to use (default: from env or 'pyautogui')"
        )

        # Text recognition settings
        parser.add_argument(
            "--text-recognition-provider", 
            choices=["tesseract", "mock"],
            help="Text recognition provider to use (default: from env or 'tesseract')"
        )

        # Text insertion settings
        parser.add_argument(
            "--text-insertion-provider", 
            choices=["pil"],
            help="Text insertion provider to use (default: from env or 'pil')"
        )
        parser.add_argument(
            "--insert-translated-text", 
            action="store_true",
            help="Insert translated text into screenshot (default: from env or True)"
        )
        parser.add_argument(
            "--no-insert-translated-text", 
            dest="insert_translated_text",
            action="store_false",
            help="Do not insert translated text into screenshot"
        )

        # Debug settings
        parser.add_argument(
            "--debug", 
            action="store_true",
            help="Enable debug mode (default: from env or False)"
        )
        parser.add_argument(
            "--log-level", 
            choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
            help="Logging level (default: from env or 'INFO')"
        )

        # Parse arguments
        parsed_args = parser.parse_args(args)

        # Convert to dictionary, filtering out None values
        return {k: v for k, v in vars(parsed_args).items() if v is not None}

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
