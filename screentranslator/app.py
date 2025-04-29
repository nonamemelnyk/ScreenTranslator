"""
Application module for ScreenTranslator.
Handles the core functionality of capturing screenshots and translating text.
"""

import io
import logging
import os
import pathlib
import sys
import tempfile
import time
from datetime import datetime
from typing import Dict, Optional, Tuple, Union

import pyautogui
from PIL import Image
from pynput import keyboard

from screentranslator.config import Config
from screentranslator.providers import ProviderManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


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
        self.keyboard_listener = None
        self.shortcut_detected = False
        self.region = None

    def display_config(self):
        """Display the current configuration."""
        self.config.display()

    def select_region(self) -> Optional[Tuple[int, int, int, int]]:
        """
        Allow the user to select a region of the screen.

        Returns:
            A tuple (x, y, width, height) representing the selected region, or None if cancelled
        """
        logger.info("Select a region by clicking and dragging. Press Esc to cancel.")
        try:
            # Get the starting position
            logger.info("Click and drag to select a region...")

            # Wait for user to click
            logger.info("Click to start selection...")
            start_pos = pyautogui.position()
            button_pressed = False

            while not button_pressed:
                time.sleep(0.1)
                # Check if Esc was pressed to cancel
                if keyboard.Key.esc in self.pressed_keys:
                    logger.info("Region selection cancelled.")
                    return None

                # Check if mouse position changed (indicating a click and drag)
                current_pos = pyautogui.position()
                if current_pos != start_pos:
                    button_pressed = True
                    start_x, start_y = start_pos
                    start_pos = current_pos

            # Wait for mouse button release (when position stops changing)
            logger.info("Drag to select region...")
            last_pos = start_pos
            same_pos_count = 0

            while same_pos_count < 5:  # Consider released after 5 consecutive same positions
                time.sleep(0.1)
                current_pos = pyautogui.position()

                if current_pos == last_pos:
                    same_pos_count += 1
                else:
                    same_pos_count = 0
                    last_pos = current_pos

            # Get the ending position
            end_x, end_y = last_pos

            # Calculate the region
            x = min(start_x, end_x)
            y = min(start_y, end_y)
            width = abs(end_x - start_x)
            height = abs(end_y - start_y)

            # Ensure minimum size
            if width < 10 or height < 10:
                logger.warning("Selected region is too small. Please try again.")
                return None

            logger.info(f"Selected region: x={x}, y={y}, width={width}, height={height}")
            return (x, y, width, height)
        except Exception as e:
            logger.error(f"Error during region selection: {str(e)}")
            return None

    def on_key_press(self, key):
        """
        Handle key press events.

        Args:
            key: The key that was pressed
        """
        try:
            # Add key to pressed keys
            self.pressed_keys.add(key)

            # Check if cmd key is pressed (either left or right)
            cmd_pressed = keyboard.Key.cmd_l in self.pressed_keys or keyboard.Key.cmd_r in self.pressed_keys
            # Check if shift key is pressed (either left or right)
            shift_pressed = keyboard.Key.shift_l in self.pressed_keys or keyboard.Key.shift_r in self.pressed_keys

            # Check for Cmd+Shift+7 (full screen)
            if hasattr(key, 'char') and key.char == '7' and cmd_pressed and shift_pressed:
                logger.info("Detected Cmd+Shift+7: Capturing full screen")
                self.shortcut_detected = True
                self.region = None
                return False  # Stop listener

            # Check for Cmd+Shift+8 (select region)
            elif hasattr(key, 'char') and key.char == '8' and cmd_pressed and shift_pressed:
                logger.info("Detected Cmd+Shift+8: Select region")
                self.shortcut_detected = True
                self.region = self.select_region()
                return False  # Stop listener

        except Exception as e:
            logger.error(f"Error in key press handler: {str(e)}")

    def on_key_release(self, key):
        """
        Handle key release events.

        Args:
            key: The key that was released
        """
        try:
            # Remove key from pressed keys
            if key in self.pressed_keys:
                self.pressed_keys.remove(key)
        except Exception as e:
            logger.error(f"Error in key release handler: {str(e)}")

    def wait_for_shortcut(self):
        """
        Wait for the user to press either Cmd+Shift+7 or Cmd+Shift+8.

        Returns:
            A tuple (shortcut_detected, region) where shortcut_detected is a boolean
            indicating if a shortcut was detected, and region is the selected region
            (None for full screen)
        """
        logger.info("Waiting for keyboard shortcut...")
        logger.info("Press Cmd+Shift+7 for full screen capture")
        logger.info("Press Cmd+Shift+8 to select a region")

        self.shortcut_detected = False
        self.region = None
        self.pressed_keys = set()

        # Start keyboard listener
        with keyboard.Listener(
            on_press=self.on_key_press,
            on_release=self.on_key_release
        ) as listener:
            self.keyboard_listener = listener
            listener.join()

        return self.shortcut_detected, self.region

    def capture_and_translate(self, region: Optional[Tuple[int, int, int, int]] = None) -> Dict[str, Union[io.BytesIO, str]]:
        """
        Capture a screenshot, recognize text, translate it, and optionally insert the translated text.

        Args:
            region: Optional tuple (x, y, width, height) defining the region to capture

        Returns:
            A dictionary with the original screenshot, recognized text, translated text,
            and optionally the screenshot with inserted translated text
        """
        try:
            # Step 1: Capture screenshot
            logger.info("Capturing screenshot...")
            screenshot_data = self.providers.screenshot.capture(region)

            # Save original screenshot for reference
            original_screenshot = io.BytesIO(screenshot_data.getvalue())
            original_screenshot.seek(0)

            # Step 2: Recognize text
            logger.info("Recognizing text...")
            recognized_text = self.providers.text_recognition.recognize(screenshot_data)

            if not recognized_text.strip():
                logger.warning("No text was recognized in the screenshot.")

            # Step 3: Translate text
            logger.info(f"Translating from {self.config.source_language} to {self.config.target_language}...")
            translated_text = self.providers.translator.translate(
                recognized_text, 
                self.config.source_language, 
                self.config.target_language
            )

            # Step 4: Insert translated text into screenshot if enabled
            screenshot_with_text = None
            if self.config.insert_translated_text and translated_text.strip():
                logger.info("Inserting translated text into screenshot...")
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

        except Exception as e:
            logger.error(f"Error during capture and translate: {str(e)}", exc_info=self.config.debug_mode)
            raise


def get_output_directory() -> pathlib.Path:
    """
    Get the output directory for saving screenshots and other files.

    Returns:
        Path to the output directory
    """
    # Use user's home directory or current directory as base
    base_dir = pathlib.Path.home() / ".screentranslator"

    # Create the directory if it doesn't exist
    base_dir.mkdir(exist_ok=True, parents=True)

    # Create a subdirectory for the current date
    date_dir = base_dir / datetime.now().strftime("%Y-%m-%d")
    date_dir.mkdir(exist_ok=True)

    return date_dir


def run_application(args=None) -> int:
    """
    Run the ScreenTranslator application.

    Args:
        args: Optional list of command-line arguments to pass to Config

    Returns:
        Exit code (0 for success, non-zero for error)
    """
    try:
        # Initialize the application
        app = ScreenTranslatorApp(args)

        # Set log level based on configuration
        log_level = getattr(logging, app.config.log_level.upper(), logging.INFO)
        logger.setLevel(log_level)

        # Display configuration
        app.display_config()

        # Wait for keyboard shortcut
        logger.info("Waiting for keyboard shortcut...")
        shortcut_detected, region = app.wait_for_shortcut()

        if not shortcut_detected:
            logger.info("No shortcut detected. Exiting...")
            return 0

        logger.info("Performing screen translation...")
        result = app.capture_and_translate(region)

        logger.info("\nResults:")
        logger.info("Recognized Text:")
        logger.info(result["recognized_text"])
        logger.info("\nTranslated Text:")
        logger.info(result["translated_text"])

        # Save the screenshots for reference
        if not app.config.debug_mode:
            # Get output directory
            output_dir = get_output_directory()
            timestamp = datetime.now().strftime("%H%M%S")

            # Save original screenshot
            screenshot = Image.open(result["screenshot"])
            screenshot_path = output_dir / f"screenshot_{timestamp}.png"
            screenshot.save(screenshot_path)
            logger.info(f"Original screenshot saved as '{screenshot_path}'")

            # Save screenshot with translated text if available
            if "screenshot_with_text" in result:
                screenshot_with_text = Image.open(result["screenshot_with_text"])
                screenshot_with_text_path = output_dir / f"screenshot_translated_{timestamp}.png"
                screenshot_with_text.save(screenshot_with_text_path)
                logger.info(f"Screenshot with translated text saved as '{screenshot_with_text_path}'")

    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        return 130  # Standard exit code for SIGINT
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=app.config.debug_mode)
        return 1

    return 0
