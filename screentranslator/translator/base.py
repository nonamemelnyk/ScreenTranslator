from abc import ABC, abstractmethod
from typing import Optional


class TranslatorProvider(ABC):
    """Base abstract class for all translator providers."""

    @abstractmethod
    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        Translate text from source language to target language.
        
        Args:
            text: The text to translate
            source_lang: The source language code
            target_lang: The target language code
            
        Returns:
            The translated text
        """
        pass


class TranslatorFactory:
    """Factory class for creating translator providers."""
    
    _providers = {}
    
    @classmethod
    def register_provider(cls, name: str, provider_class):
        """Register a translator provider."""
        cls._providers[name] = provider_class
        
    @classmethod
    def get_provider(cls, name: str, **kwargs) -> Optional[TranslatorProvider]:
        """
        Get a translator provider by name.
        
        Args:
            name: The name of the provider
            **kwargs: Additional arguments to pass to the provider constructor
            
        Returns:
            An instance of the requested provider or None if not found
        """
        provider_class = cls._providers.get(name)
        if provider_class:
            return provider_class(**kwargs)
        return None
        
    @classmethod
    def list_providers(cls) -> list:
        """List all registered providers."""
        return list(cls._providers.keys())