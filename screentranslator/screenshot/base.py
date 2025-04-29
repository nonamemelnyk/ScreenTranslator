from abc import ABC, abstractmethod
from typing import Optional, Tuple, Union
import io


class ScreenshotProvider(ABC):
    """Base abstract class for all screenshot providers."""

    @abstractmethod
    def capture(self, region: Optional[Tuple[int, int, int, int]] = None) -> io.BytesIO:
        """
        Capture a screenshot.
        
        Args:
            region: Optional tuple (x, y, width, height) defining the region to capture.
                   If None, captures the entire screen.
            
        Returns:
            BytesIO object containing the screenshot image data
        """
        pass


class ScreenshotFactory:
    """Factory class for creating screenshot providers."""
    
    _providers = {}
    
    @classmethod
    def register_provider(cls, name: str, provider_class):
        """Register a screenshot provider."""
        cls._providers[name] = provider_class
        
    @classmethod
    def get_provider(cls, name: str, **kwargs) -> Optional[ScreenshotProvider]:
        """
        Get a screenshot provider by name.
        
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