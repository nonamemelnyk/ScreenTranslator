# ScreenTranslator

A modular tool for capturing screenshots, recognizing text, translating it, and inserting the translated text back into the screenshot.

## Features

- **Modular Architecture**: Separate modules for screenshot capture, text recognition, translation, and text insertion
- **Multiple Providers**: Support for different providers in each module
- **Easy Configuration**: Simple configuration through environment variables
- **Extensible**: Easy to add new providers for any module

## Modules and Providers

### Screenshot Module
Captures screenshots from your screen.

Providers:
- **PyAutoGUI**: Cross-platform screenshot capture using PyAutoGUI
- **PIL**: Screenshot capture using PIL (Pillow)

### Text Recognition Module
Extracts text from images.

Providers:
- **Tesseract**: Text recognition using Tesseract OCR
- **Mock**: A mock provider for testing purposes

### Translator Module
Translates text between languages.

Providers:
- **Google**: Translation using Google Translate
- **GPT**: Translation using OpenAI's GPT models
- **DeepL**: Translation using DeepL API

### Text Insertion Module
Inserts translated text into screenshots.

Providers:
- **PIL**: Text insertion using PIL (Pillow)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ScreenTranslator.git
   cd ScreenTranslator
   ```

2. Install dependencies using Poetry:
   ```
   poetry install
   ```

3. Create a `.env` file based on the `.env_example` file:
   ```
   cp .env_example .env
   ```

4. Edit the `.env` file to configure your API keys and preferences.

**Note:** The `.env` file is included in `.gitignore` to prevent sensitive information like API keys from being committed to the repository.

## Configuration

ScreenTranslator uses environment variables for configuration. The following variables can be set in your `.env` file:

### Translation Settings
- `TRANSLATION_SERVICE`: The translation provider to use (google, gpt, deepl)
- `DEFAULT_SOURCE_LANGUAGE`: The default source language code
- `DEFAULT_TARGET_LANGUAGE`: The default target language code
- `OPENAI_API_KEY`: Your OpenAI API key (required for GPT provider)
- `DEEPL_AUTH_KEY`: Your DeepL authentication key (required for DeepL provider)

### Screenshot Settings
- `SCREENSHOT_PROVIDER`: The screenshot provider to use (pyautogui, pil)

### Text Recognition Settings
- `TEXT_RECOGNITION_PROVIDER`: The text recognition provider to use (tesseract, mock)
- `TESSERACT_CMD`: Path to the Tesseract executable (required for Tesseract on Windows)

### Text Insertion Settings
- `TEXT_INSERTION_PROVIDER`: The text insertion provider to use (pil)
- `INSERT_TRANSLATED_TEXT`: Whether to insert translated text into screenshots (True/False)

### Debug Settings
- `DEBUG_MODE`: Enable debug mode (True/False)
- `LOG_LEVEL`: Logging level (INFO, DEBUG, etc.)

## Usage

### Basic Usage

Run the application using Poetry:

```
poetry run python main.py
```

This will:
1. Capture a screenshot of your entire screen
2. Recognize text from the screenshot
3. Translate the text to your target language
4. Optionally insert the translated text into the screenshot (if `INSERT_TRANSLATED_TEXT` is enabled)
5. Display the results

### Programmatic Usage

```python
from screentranslator.translator.base import TranslatorFactory
from screentranslator.screenshot.base import ScreenshotFactory
from screentranslator.text_recognition.base import TextRecognitionFactory
from screentranslator.text_insertion.base import TextInsertionFactory

# Import providers to register them
from screentranslator.translator.providers import google, gpt, deepl
from screentranslator.screenshot.providers import pyautogui_provider, pil_provider
from screentranslator.text_recognition.providers import tesseract_provider, mock_provider
from screentranslator.text_insertion.providers import pil_provider as text_insertion_pil

# Create providers
screenshot = ScreenshotFactory.get_provider("pyautogui")
text_recognition = TextRecognitionFactory.get_provider("tesseract")
translator = TranslatorFactory.get_provider("google")
text_insertion = TextInsertionFactory.get_provider("pil")

# Use them sequentially
screenshot_data = screenshot.capture()
recognized_text = text_recognition.recognize(screenshot_data)
translated_text = translator.translate(recognized_text, "en", "es")

# Optionally insert translated text into the screenshot
screenshot_data.seek(0)  # Reset position to beginning of file
screenshot_with_text = text_insertion.insert_text(
    screenshot_data, 
    translated_text,
    {'position': 'bottom'}  # Position at the bottom of the image
)

print(f"Original: {recognized_text}")
print(f"Translated: {translated_text}")

# Save the screenshot with translated text
from PIL import Image
Image.open(screenshot_with_text).save("translated_screenshot.png")
print("Screenshot with translated text saved as 'translated_screenshot.png'")
```

## Development

### Environment Setup

1. Make sure you have Poetry installed:
   ```
   pip install poetry
   ```

2. Install dependencies:
   ```
   poetry install
   ```

3. Create and configure your `.env` file as described in the Configuration section.

### Adding Dependencies

To add a new dependency:

```
poetry add package-name
```

### Adding New Providers

To add a new provider for any module:

1. Create a new file in the appropriate providers directory
2. Implement the provider class that inherits from the base provider class
3. Register the provider with the factory
4. Import the provider in the main application

Example for a new translator provider:

```python
from ...translator.base import TranslatorProvider, TranslatorFactory

class MyTranslator(TranslatorProvider):
    def translate(self, text, source_lang, target_lang):
        # Implementation here
        return translated_text

# Register the provider
TranslatorFactory.register_provider("my_translator", MyTranslator)
```

### Running Tests

Run the tests to verify the functionality:

```
python -m unittest discover tests
```

## License

MIT
