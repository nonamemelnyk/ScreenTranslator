"""
ScreenTranslator - A tool for translating text from screen captures.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ScreenTranslator:
    """Main class for handling screen translation functionality."""

    def __init__(self):
        """Initialize the translator with settings from environment variables."""
        self.api_key = os.getenv('API_KEY')
        self.translation_service = os.getenv('TRANSLATION_SERVICE', 'google')
        self.source_language = os.getenv('DEFAULT_SOURCE_LANGUAGE', 'en')
        self.target_language = os.getenv('DEFAULT_TARGET_LANGUAGE', 'es')
        self.debug_mode = os.getenv('DEBUG_MODE', 'False').lower() == 'true'
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')

    def display_config(self):
        """Display the current configuration (without showing the API key)."""
        print("ScreenTranslator Configuration:")
        print(f"Translation Service: {self.translation_service}")
        print(f"Source Language: {self.source_language}")
        print(f"Target Language: {self.target_language}")
        print(f"Debug Mode: {self.debug_mode}")
        print(f"Log Level: {self.log_level}")
        print(f"API Key: {'Configured' if self.api_key else 'Not configured'}")

    def translate_text(self, text):
        """Simulate translating text using the configured service."""
        if not self.api_key:
            return "Error: API key not configured. Please set API_KEY in your .env file."

        # This is just a simulation - in a real app, you would call the translation API
        print(f"Translating from {self.source_language} to {self.target_language} using {self.translation_service}...")
        return f"Translated: {text} (simulated)"


if __name__ == '__main__':
    # Create and use the translator
    translator = ScreenTranslator()
    translator.display_config()

    # Example translation
    sample_text = "Hello, world!"
    result = translator.translate_text(sample_text)
    print(f"\nOriginal: {sample_text}")
    print(result)
