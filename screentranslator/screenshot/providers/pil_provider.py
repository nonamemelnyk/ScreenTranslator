import io
import os
from PIL import ImageGrab
from typing import Optional, Tuple
from ...screenshot.base import ScreenshotProvider, ScreenshotFactory


class PILScreenshot(ScreenshotProvider):
    """Screenshot provider implementation using PIL (Pillow)."""
    
    def __init__(self, **kwargs):
        """Initialize the PIL screenshot provider."""
        # Check if we're on macOS, which requires additional permissions for PIL.ImageGrab
        self.is_macos = os.name == 'posix' and os.uname().sysname == 'Darwin'
        if self.is_macos:
            print("Note: On macOS, PIL.ImageGrab requires Quartz display services access.")
    
    def capture(self, region: Optional[Tuple[int, int, int, int]] = None) -> io.BytesIO:
        """
        Capture a screenshot using PIL.
        
        Args:
            region: Optional tuple (x, y, width, height) defining the region to capture.
                   If None, captures the entire screen.
            
        Returns:
            BytesIO object containing the screenshot image data
        """
        try:
            if region:
                x, y, width, height = region
                # PIL uses bbox format (left, top, right, bottom)
                bbox = (x, y, x + width, y + height)
                screenshot = ImageGrab.grab(bbox=bbox)
            else:
                screenshot = ImageGrab.grab()
            
            # Convert the PIL Image to bytes
            img_byte_arr = io.BytesIO()
            screenshot.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            
            return img_byte_arr
        except Exception as e:
            # In case of error, create an error image
            from PIL import Image, ImageDraw
            
            error_img = Image.new('RGB', (400, 100), color=(255, 0, 0))
            draw = ImageDraw.Draw(error_img)
            draw.text((10, 40), f"Screenshot error: {str(e)}", fill=(255, 255, 255))
            
            img_byte_arr = io.BytesIO()
            error_img.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            
            print(f"Screenshot error: {str(e)}")
            return img_byte_arr


# Register the provider with the factory
ScreenshotFactory.register_provider("pil", PILScreenshot)