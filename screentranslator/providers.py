"""
Providers module for ScreenTranslator.
Handles initialization of various service providers.
"""

from screentranslator.translator.base import TranslatorFactory
from screentranslator.screenshot.base import ScreenshotFactory
from screentranslator.text_recognition.base import TextRecognitionFactory
from screentranslator.text_insertion.base import TextInsertionFactory

# Import providers to register them with factories
from screentranslator.translator.providers import google, gpt, deepl
from screentranslator.screenshot.providers import pyautogui_provider, pil_provider
from screentranslator.text_recognition.providers import tesseract_provider, mock_provider
from screentranslator.text_insertion.providers import pil_provider as text_insertion_pil


class ProviderManager:
    """Manager class for initializing and managing service providers."""

    def __init__(self, config):
        """
        Initialize providers based on configuration.
        
        Args:
            config: Configuration object containing provider settings
        """
        self.config = config
        self.translator = None
        self.screenshot = None
        self.text_recognition = None
        self.text_insertion = None
        
        self._init_providers()

    def _init_providers(self):
        """Initialize the providers based on configuration."""
        # Initialize translator
        self.translator = TranslatorFactory.get_provider(self.config.translation_service)
        if not self.translator:
            available = TranslatorFactory.list_providers()
            raise ValueError(f"Translator provider '{self.config.translation_service}' not found. Available providers: {available}")

        # Initialize screenshot provider
        self.screenshot = ScreenshotFactory.get_provider(self.config.screenshot_provider)
        if not self.screenshot:
            available = ScreenshotFactory.list_providers()
            raise ValueError(f"Screenshot provider '{self.config.screenshot_provider}' not found. Available providers: {available}")

        # Initialize text recognition provider
        self.text_recognition = TextRecognitionFactory.get_provider(self.config.text_recognition_provider)
        if not self.text_recognition:
            available = TextRecognitionFactory.list_providers()
            raise ValueError(f"Text recognition provider '{self.config.text_recognition_provider}' not found. Available providers: {available}")

        # Initialize text insertion provider
        self.text_insertion = TextInsertionFactory.get_provider(self.config.text_insertion_provider)
        if not self.text_insertion:
            available = TextInsertionFactory.list_providers()
            raise ValueError(f"Text insertion provider '{self.config.text_insertion_provider}' not found. Available providers: {available}")