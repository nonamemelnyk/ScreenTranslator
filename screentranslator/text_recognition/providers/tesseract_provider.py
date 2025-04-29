import io
import os
import pytesseract
from PIL import Image
from ...text_recognition.base import TextRecognitionProvider, TextRecognitionFactory


class TesseractTextRecognition(TextRecognitionProvider):
    """Text recognition provider implementation using Tesseract OCR."""
    
    def __init__(self, tesseract_cmd=None, lang="eng", **kwargs):
        """
        Initialize the Tesseract OCR provider.
        
        Args:
            tesseract_cmd: Path to the Tesseract executable (defaults to TESSERACT_CMD environment variable)
            lang: Language for OCR (default: eng)
        """
        # Set Tesseract command path if provided or from environment
        self.tesseract_cmd = tesseract_cmd or os.getenv("TESSERACT_CMD")
        if self.tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = self.tesseract_cmd
            
        self.lang = lang
    
    def recognize(self, image_data: io.BytesIO) -> str:
        """
        Recognize text from an image using Tesseract OCR.
        
        Args:
            image_data: BytesIO object containing the image data
            
        Returns:
            The recognized text as a string
        """
        try:
            # Open the image from BytesIO
            image = Image.open(image_data)
            
            # Use Tesseract to extract text
            text = pytesseract.image_to_string(image, lang=self.lang)
            
            # Return the extracted text, removing any trailing whitespace
            return text.strip()
        except Exception as e:
            return f"Text recognition error: {str(e)}"


# Register the provider with the factory
TextRecognitionFactory.register_provider("tesseract", TesseractTextRecognition)