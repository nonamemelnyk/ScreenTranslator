from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import io


class TextInsertionProvider(ABC):
    """Base abstract class for all text insertion providers."""

    @abstractmethod
    def insert_text(self, image_data: io.BytesIO, text: str, position: Optional[Dict[str, Any]] = None) -> io.BytesIO:
        """
        Insert text into an image.
        
        Args:
            image_data: BytesIO object containing the image data
            text: The text to insert into the image
            position: Optional dictionary with positioning parameters (may vary by provider)
                    If None, the provider will use default positioning
            
        Returns:
            BytesIO object containing the modified image data with inserted text
        """
        pass


class TextInsertionFactory:
    """Factory class for creating text insertion providers."""
    
    _providers = {}
    
    @classmethod
    def register_provider(cls, name: str, provider_class):
        """Register a text insertion provider."""
        cls._providers[name] = provider_class
        
    @classmethod
    def get_provider(cls, name: str, **kwargs) -> Optional[TextInsertionProvider]:
        """
        Get a text insertion provider by name.
        
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