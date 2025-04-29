import os
from openai import OpenAI
from ...translator.base import TranslatorProvider, TranslatorFactory


class GPTTranslator(TranslatorProvider):
    """GPT-based translator provider implementation."""
    
    def __init__(self, api_key=None, model="gpt-3.5-turbo", **kwargs):
        """
        Initialize the GPT translator.
        
        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY environment variable)
            model: The GPT model to use
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
        
        self.model = model
        self.client = OpenAI(api_key=self.api_key)
    
    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        Translate text using GPT.
        
        Args:
            text: The text to translate
            source_lang: The source language code
            target_lang: The target language code
            
        Returns:
            The translated text
        """
        try:
            prompt = f"Translate the following text from {source_lang} to {target_lang}:\n\n{text}"
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional translator."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Translation error: {str(e)}"


# Register the provider with the factory
TranslatorFactory.register_provider("gpt", GPTTranslator)