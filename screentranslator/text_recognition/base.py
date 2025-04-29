from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
import io


class TextRecognitionProvider(ABC):
    """Base abstract class for all text recognition providers."""

    @abstractmethod
    def recognize(self, image_data: io.BytesIO) -> str:
        """
        Recognize text from an image.
        
        Args:
            image_data: BytesIO object containing the image data
            
        Returns:
            The recognized text as a string
        """
        pass


class TextRecognitionFactory:
    """Factory class for creating text recognition providers."""
    
    _providers = {}
    
    @classmethod
    def register_provider(cls, name: str, provider_class):
        """Register a text recognition provider."""
        cls._providers[name] = provider_class
        
    @classmethod
    def get_provider(cls, name: str, **kwargs) -> Optional[TextRecognitionProvider]:
        """
        Get a text recognition provider by name.
        
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