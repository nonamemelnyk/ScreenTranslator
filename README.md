# ScreenTranslator

A tool for translating text from screen captures.

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

## Configuration

ScreenTranslator uses environment variables for configuration. Create a `.env` file in the project root with the following variables:

```
API_KEY=your_api_key_here
TRANSLATION_SERVICE=google
DEFAULT_SOURCE_LANGUAGE=en
DEFAULT_TARGET_LANGUAGE=es
DEBUG_MODE=False
LOG_LEVEL=INFO
```

**Note:** The `.env` file is included in `.gitignore` to prevent sensitive information like API keys from being committed to the repository.

## Usage

Run the application using Poetry:

```
poetry run python main.py
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

## License

MIT