"""
Application module for ScreenTranslator.
Handles the core functionality of capturing screenshots and translating text.
"""

import io
from PIL import Image

from screentranslator.config import Config
from screentranslator.providers import ProviderManager


class ScreenTranslatorApp:
    """Main application class for handling screen translation functionality."""

    def __init__(self, args=None):
        """
        Initialize the application with configuration and providers.

        Args:
            args: Optional list of command-line arguments to pass to Config
        """
        self.config = Config(args)
        self.providers = ProviderManager(self.config)

    def display_config(self):
        """Display the current configuration."""
        self.config.display()

    def capture_and_translate(self, region=None):
        """
        Capture a screenshot, recognize text, translate it, and optionally insert the translated text.

        Args:
            region: Optional tuple (x, y, width, height) defining the region to capture

        Returns:
            A dictionary with the original screenshot, recognized text, translated text,
            and optionally the screenshot with inserted translated text
        """
        # Step 1: Capture screenshot
        print("Capturing screenshot...")
        screenshot_data = self.providers.screenshot.capture(region)

        # Save original screenshot for reference
        original_screenshot = io.BytesIO(screenshot_data.getvalue())
        original_screenshot.seek(0)

        # Step 2: Recognize text
        print("Recognizing text...")
        recognized_text = self.providers.text_recognition.recognize(screenshot_data)

        # Step 3: Translate text
        print(f"Translating from {self.config.source_language} to {self.config.target_language}...")
        translated_text = self.providers.translator.translate(
            recognized_text, 
            self.config.source_language, 
            self.config.target_language
        )

        # Step 4: Insert translated text into screenshot if enabled
        screenshot_with_text = None
        if self.config.insert_translated_text:
            print("Inserting translated text into screenshot...")
            # Reset the screenshot data position to the beginning
            screenshot_data.seek(0)
            screenshot_with_text = self.providers.text_insertion.insert_text(
                screenshot_data,
                translated_text,
                {'position': 'bottom'}  # Default position at the bottom of the image
            )

        # Return all results
        result = {
            "screenshot": original_screenshot,
            "recognized_text": recognized_text,
            "translated_text": translated_text
        }

        if screenshot_with_text:
            result["screenshot_with_text"] = screenshot_with_text

        return result


def run_application(args=None):
    """
    Run the ScreenTranslator application.

    Args:
        args: Optional list of command-line arguments to pass to Config
    """
    try:
        app = ScreenTranslatorApp(args)
        app.display_config()

        print("\nPerforming screen translation...")
        result = app.capture_and_translate()

        print("\nResults:")
        print("Recognized Text:")
        print(result["recognized_text"])
        print("\nTranslated Text:")
        print(result["translated_text"])

        # Optionally save the screenshots for reference
        if app.config.debug_mode == False:
            # Save original screenshot
            screenshot = Image.open(result["screenshot"])
            screenshot.save("last_screenshot.png")
            print("\nOriginal screenshot saved as 'last_screenshot.png'")

            # Save screenshot with translated text if available
            if "screenshot_with_text" in result:
                screenshot_with_text = Image.open(result["screenshot_with_text"])
                screenshot_with_text.save("last_screenshot_with_text.png")
                print("Screenshot with translated text saved as 'last_screenshot_with_text.png'")

    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    return 0
