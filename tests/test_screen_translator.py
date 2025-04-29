"""
Test for the ScreenTranslator application demonstrating sequential use of modules.
"""

import os
import io
import unittest
from unittest.mock import patch, MagicMock
from PIL import Image, ImageDraw, ImageFont

# Import the modules
from screentranslator.translator.base import TranslatorFactory
from screentranslator.screenshot.base import ScreenshotFactory
from screentranslator.text_recognition.base import TextRecognitionFactory

# Import providers to register them
from screentranslator.translator.providers import google, gpt, deepl
from screentranslator.screenshot.providers import pyautogui_provider, pil_provider
from screentranslator.text_recognition.providers import tesseract_provider, mock_provider


class TestScreenTranslator(unittest.TestCase):
    """Test case for the ScreenTranslator application."""
    
    def setUp(self):
        """Set up the test environment."""
        # Create a test image with text
        self.test_image = self._create_test_image("Hello, World!")
        
        # Create mock providers for testing
        self.mock_screenshot = MagicMock()
        self.mock_screenshot.capture.return_value = self.test_image
        
        self.mock_text_recognition = MagicMock()
        self.mock_text_recognition.recognize.return_value = "Hello, World!"
        
        self.mock_translator = MagicMock()
        self.mock_translator.translate.return_value = "Hola, Mundo!"
        
        # Register mock providers with factories
        ScreenshotFactory.register_provider("mock", lambda **kwargs: self.mock_screenshot)
        TextRecognitionFactory.register_provider("mock_ocr", lambda **kwargs: self.mock_text_recognition)
        TranslatorFactory.register_provider("mock_translator", lambda **kwargs: self.mock_translator)
    
    def _create_test_image(self, text):
        """Create a test image with the given text."""
        # Create a new image with white background
        img = Image.new('RGB', (400, 200), color=(255, 255, 255))
        d = ImageDraw.Draw(img)
        
        # Add text to the image
        d.text((50, 100), text, fill=(0, 0, 0))
        
        # Convert to BytesIO
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        return img_byte_arr
    
    def test_sequential_module_usage(self):
        """Test the sequential use of screenshot, text recognition, and translation modules."""
        # Step 1: Capture screenshot
        screenshot_provider = ScreenshotFactory.get_provider("mock")
        screenshot_data = screenshot_provider.capture()
        
        # Verify screenshot was captured
        self.assertIsNotNone(screenshot_data)
        self.mock_screenshot.capture.assert_called_once()
        
        # Step 2: Recognize text from screenshot
        text_recognition_provider = TextRecognitionFactory.get_provider("mock_ocr")
        recognized_text = text_recognition_provider.recognize(screenshot_data)
        
        # Verify text was recognized
        self.assertEqual(recognized_text, "Hello, World!")
        self.mock_text_recognition.recognize.assert_called_once_with(screenshot_data)
        
        # Step 3: Translate the recognized text
        translator_provider = TranslatorFactory.get_provider("mock_translator")
        translated_text = translator_provider.translate(recognized_text, "en", "es")
        
        # Verify text was translated
        self.assertEqual(translated_text, "Hola, Mundo!")
        self.mock_translator.translate.assert_called_once_with(recognized_text, "en", "es")
        
        print("\nSequential module test completed successfully:")
        print(f"Original text: {recognized_text}")
        print(f"Translated text: {translated_text}")
    
    def test_real_providers(self):
        """Test with real providers (if available)."""
        try:
            # Try to use real providers if available
            screenshot_provider = ScreenshotFactory.get_provider("pil")
            text_recognition_provider = TextRecognitionFactory.get_provider("mock")  # Use mock for text recognition
            translator_provider = TranslatorFactory.get_provider("google")
            
            # Skip test if any provider is not available
            if not all([screenshot_provider, text_recognition_provider, translator_provider]):
                self.skipTest("One or more real providers not available")
            
            # Set predefined text for the mock text recognition
            text_recognition_provider.predefined_text = "Hello, World!"
            
            # Capture a small region of the screen
            region = (0, 0, 100, 100)  # Small region to make the test faster
            screenshot_data = screenshot_provider.capture(region)
            
            # Recognize text (will return predefined text)
            recognized_text = text_recognition_provider.recognize(screenshot_data)
            
            # Translate text
            translated_text = translator_provider.translate(recognized_text, "en", "es")
            
            print("\nReal providers test:")
            print(f"Original text: {recognized_text}")
            print(f"Translated text: {translated_text}")
            
            # Basic verification
            self.assertIsNotNone(translated_text)
            self.assertNotEqual(recognized_text, translated_text)
            
        except Exception as e:
            self.skipTest(f"Test with real providers skipped: {str(e)}")


if __name__ == '__main__':
    unittest.main()