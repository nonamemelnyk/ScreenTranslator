import asyncio

from googletrans import Translator
from ...translator.base import TranslatorProvider, TranslatorFactory


class GoogleTranslator(TranslatorProvider):
    """Google Translate provider implementation."""
    
    def __init__(self, **kwargs):
        """Initialize the Google translator."""
        self.translator = Translator()
    
    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        Translate text using Google Translate.
        
        Args:
            text: The text to translate
            source_lang: The source language code
            target_lang: The target language code
            
        Returns:
            The translated text
        """
        try:
            result = asyncio.run(self.translator.translate(text, src=source_lang, dest=target_lang))
            return result.text
        except Exception as e:
            return f"Translation error: {str(e)}"


# Register the provider with the factory
TranslatorFactory.register_provider("google", GoogleTranslator)