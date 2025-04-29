"""
Command-line interface for ScreenTranslator.
Handles parsing arguments and running the application from the command line.
"""

import argparse
import sys
from typing import List, Optional

from screentranslator.app import run_application


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """
    Parse command-line arguments.

    Args:
        args: Optional list of command-line arguments. If None, sys.argv is used.

    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="ScreenTranslator - A tool for translating text from screen captures."
    )

    # Translation settings
    translation_group = parser.add_argument_group("Translation Settings")
    translation_group.add_argument(
        "--translation-service", 
        choices=["google", "gpt", "deepl"],
        help="Translation service to use (default: from env or 'google')"
    )
    translation_group.add_argument(
        "--source-language", 
        help="Source language code (default: from env or 'en')"
    )
    translation_group.add_argument(
        "--target-language", 
        help="Target language code (default: from env or 'es')"
    )
    
    # Screenshot settings
    screenshot_group = parser.add_argument_group("Screenshot Settings")
    screenshot_group.add_argument(
        "--screenshot-provider", 
        choices=["pyautogui", "pil"],
        help="Screenshot provider to use (default: from env or 'pyautogui')"
    )
    
    # Text recognition settings
    recognition_group = parser.add_argument_group("Text Recognition Settings")
    recognition_group.add_argument(
        "--text-recognition-provider", 
        choices=["tesseract", "mock"],
        help="Text recognition provider to use (default: from env or 'tesseract')"
    )
    
    # Text insertion settings
    insertion_group = parser.add_argument_group("Text Insertion Settings")
    insertion_group.add_argument(
        "--text-insertion-provider", 
        choices=["pil"],
        help="Text insertion provider to use (default: from env or 'pil')"
    )
    insertion_group.add_argument(
        "--insert-translated-text", 
        action="store_true",
        help="Insert translated text into screenshot (default: from env or True)"
    )
    insertion_group.add_argument(
        "--no-insert-translated-text", 
        dest="insert_translated_text",
        action="store_false",
        help="Do not insert translated text into screenshot"
    )
    
    # Debug settings
    debug_group = parser.add_argument_group("Debug Settings")
    debug_group.add_argument(
        "--debug", 
        action="store_true",
        help="Enable debug mode (default: from env or False)"
    )
    debug_group.add_argument(
        "--log-level", 
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level (default: from env or 'INFO')"
    )
    
    return parser.parse_args(args)


def main(args: Optional[List[str]] = None) -> int:
    """
    Main entry point for the command-line interface.

    Args:
        args: Optional list of command-line arguments. If None, sys.argv[1:] is used.

    Returns:
        Exit code (0 for success, non-zero for error)
    """
    parsed_args = parse_args(args)
    
    # Convert argparse.Namespace to list of arguments in the format expected by Config
    config_args = []
    for key, value in vars(parsed_args).items():
        if value is not None:
            if isinstance(value, bool):
                if value:
                    config_args.append(f"--{key.replace('_', '-')}")
            else:
                config_args.append(f"--{key.replace('_', '-')}={value}")
    
    return run_application(config_args)


if __name__ == "__main__":
    sys.exit(main())