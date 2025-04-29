import io
from ...text_recognition.base import TextRecognitionProvider, TextRecognitionFactory


class MockTextRecognition(TextRecognitionProvider):
    """Mock text recognition provider for testing purposes."""
    
    def __init__(self, predefined_text=None, **kwargs):
        """
        Initialize the mock text recognition provider.
        
        Args:
            predefined_text: Optional text to return instead of analyzing the image
        """
        self.predefined_text = predefined_text
    
    def recognize(self, image_data: io.BytesIO) -> str:
        """
        Simulate text recognition from an image.
        
        Args:
            image_data: BytesIO object containing the image data
            
        Returns:
            The simulated recognized text
        """
        if self.predefined_text is not None:
            return self.predefined_text
            
        # If no predefined text, return a sample text
        return "This is a simulated text recognition result.\nIt does not actually analyze the image content."


# Register the provider with the factory
TextRecognitionFactory.register_provider("mock", MockTextRecognition)