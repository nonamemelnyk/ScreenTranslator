import io
import pyautogui
from PIL import Image
from typing import Optional, Tuple
from ...screenshot.base import ScreenshotProvider, ScreenshotFactory


class PyAutoGUIScreenshot(ScreenshotProvider):
    """Screenshot provider implementation using PyAutoGUI."""
    
    def __init__(self, **kwargs):
        """Initialize the PyAutoGUI screenshot provider."""
        pass
    
    def capture(self, region: Optional[Tuple[int, int, int, int]] = None) -> io.BytesIO:
        """
        Capture a screenshot using PyAutoGUI.
        
        Args:
            region: Optional tuple (x, y, width, height) defining the region to capture.
                   If None, captures the entire screen.
            
        Returns:
            BytesIO object containing the screenshot image data
        """
        try:
            if region:
                x, y, width, height = region
                screenshot = pyautogui.screenshot(region=(x, y, width, height))
            else:
                screenshot = pyautogui.screenshot()
            
            # Convert the PIL Image to bytes
            img_byte_arr = io.BytesIO()
            screenshot.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            
            return img_byte_arr
        except Exception as e:
            # In case of error, return an empty image with error message
            error_img = Image.new('RGB', (400, 100), color=(255, 0, 0))
            img_byte_arr = io.BytesIO()
            error_img.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            
            print(f"Screenshot error: {str(e)}")
            return img_byte_arr


# Register the provider with the factory
ScreenshotFactory.register_provider("pyautogui", PyAutoGUIScreenshot)