import unittest
import io
from PIL import Image, ImageDraw
from screentranslator.text_insertion.base import TextInsertionFactory
from screentranslator.text_insertion.providers import pil_provider


class TestTextInsertion(unittest.TestCase):
    """Test cases for the text insertion module."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a test image
        self.test_image = Image.new('RGB', (400, 200), color=(100, 100, 100))
        draw = ImageDraw.Draw(self.test_image)
        draw.text((10, 10), "Test Image", fill=(255, 255, 255))
        
        # Convert to BytesIO
        self.image_data = io.BytesIO()
        self.test_image.save(self.image_data, format='PNG')
        self.image_data.seek(0)
        
        # Test text
        self.test_text = "This is translated text"
        
    def test_pil_provider_registration(self):
        """Test that the PIL provider is registered correctly."""
        providers = TextInsertionFactory.list_providers()
        self.assertIn("pil", providers)
        
    def test_pil_provider_creation(self):
        """Test that the PIL provider can be created."""
        provider = TextInsertionFactory.get_provider("pil")
        self.assertIsNotNone(provider)
        
    def test_text_insertion(self):
        """Test that text can be inserted into an image."""
        provider = TextInsertionFactory.get_provider("pil")
        
        # Insert text at the bottom
        self.image_data.seek(0)
        result = provider.insert_text(
            self.image_data,
            self.test_text,
            {'position': 'bottom'}
        )
        
        # Verify result is a BytesIO object
        self.assertIsInstance(result, io.BytesIO)
        
        # Open the result image to verify it's valid
        result_image = Image.open(result)
        self.assertEqual(result_image.size, self.test_image.size)
        
    def test_text_insertion_positions(self):
        """Test text insertion at different positions."""
        provider = TextInsertionFactory.get_provider("pil")
        positions = ['top', 'bottom', 'center', 'top-left', 'top-right', 'bottom-left', 'bottom-right']
        
        for position in positions:
            self.image_data.seek(0)
            result = provider.insert_text(
                self.image_data,
                f"Position: {position}",
                {'position': position}
            )
            
            # Verify result is valid
            result_image = Image.open(result)
            self.assertEqual(result_image.size, self.test_image.size)


if __name__ == '__main__':
    unittest.main()