import os
import deepl
from ...translator.base import TranslatorProvider, TranslatorFactory


class DeepLTranslator(TranslatorProvider):
    """DeepL translator provider implementation."""
    
    def __init__(self, auth_key=None, **kwargs):
        """
        Initialize the DeepL translator.
        
        Args:
            auth_key: DeepL authentication key (defaults to DEEPL_AUTH_KEY environment variable)
        """
        self.auth_key = auth_key or os.getenv("DEEPL_AUTH_KEY")
        if not self.auth_key:
            raise ValueError("DeepL authentication key is required. Set DEEPL_AUTH_KEY environment variable or pass auth_key parameter.")
        
        self.translator = deepl.Translator(self.auth_key)
    
    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        Translate text using DeepL.
        
        Args:
            text: The text to translate
            source_lang: The source language code
            target_lang: The target language code
            
        Returns:
            The translated text
        """
        try:
            # DeepL uses different language code format, convert if needed
            source_lang = self._normalize_lang_code(source_lang)
            target_lang = self._normalize_lang_code(target_lang)
            
            result = self.translator.translate_text(
                text,
                source_lang=source_lang if source_lang != "auto" else None,
                target_lang=target_lang
            )
            return result.text
        except Exception as e:
            return f"Translation error: {str(e)}"
    
    def _normalize_lang_code(self, lang_code: str) -> str:
        """
        Convert standard language codes to DeepL format.
        
        Args:
            lang_code: The language code to normalize
            
        Returns:
            The normalized language code for DeepL
        """
        # DeepL uses uppercase language codes for most languages
        if lang_code.lower() == "en":
            return "EN-US"  # or EN-GB depending on preference
        elif lang_code.lower() == "pt":
            return "PT-PT"  # or PT-BR depending on preference
        
        # For most other languages, just uppercase
        return lang_code.upper()


# Register the provider with the factory
TranslatorFactory.register_provider("deepl", DeepLTranslator)