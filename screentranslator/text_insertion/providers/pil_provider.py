import io
import os
from PIL import Image, ImageDraw, ImageFont
from typing import Optional, Dict, Any
from ...text_insertion.base import TextInsertionProvider, TextInsertionFactory


class PILTextInsertion(TextInsertionProvider):
    """Text insertion provider implementation using PIL (Pillow)."""
    
    def __init__(self, font_path=None, font_size=24, text_color=(255, 255, 255), 
                 background_color=(0, 0, 0, 128), padding=10, **kwargs):
        """
        Initialize the PIL text insertion provider.
        
        Args:
            font_path: Path to a TrueType font file (optional)
            font_size: Font size to use (default: 24)
            text_color: RGB tuple for text color (default: white)
            background_color: RGBA tuple for text background (default: semi-transparent black)
            padding: Padding around text in pixels (default: 10)
        """
        self.font_size = font_size
        self.text_color = text_color
        self.background_color = background_color
        self.padding = padding
        
        # Try to load the specified font or use default
        self.font = None
        if font_path and os.path.exists(font_path):
            try:
                self.font = ImageFont.truetype(font_path, self.font_size)
            except Exception as e:
                print(f"Error loading font: {str(e)}")
        
        # If no font specified or loading failed, use default
        if not self.font:
            # Use a default font that comes with PIL
            self.font = ImageFont.load_default()
    
    def insert_text(self, image_data: io.BytesIO, text: str, position: Optional[Dict[str, Any]] = None) -> io.BytesIO:
        """
        Insert text into an image using PIL.
        
        Args:
            image_data: BytesIO object containing the image data
            text: The text to insert into the image
            position: Optional dictionary with positioning parameters:
                     - 'x': x-coordinate (default: center)
                     - 'y': y-coordinate (default: bottom)
                     - 'align': text alignment ('left', 'center', 'right') (default: 'center')
                     - 'position': predefined position ('top', 'bottom', 'center', 'top-left', etc.)
            
        Returns:
            BytesIO object containing the modified image data with inserted text
        """
        try:
            # Open the image from BytesIO
            image = Image.open(image_data)
            
            # Create a drawing context
            draw = ImageDraw.Draw(image, 'RGBA')
            
            # Process position parameters
            pos = self._calculate_position(image.size, text, position)
            
            # Calculate text size to create background
            text_width, text_height = draw.textbbox((0, 0), text, font=self.font)[2:]
            
            # Add padding to text dimensions
            text_width += self.padding * 2
            text_height += self.padding * 2
            
            # Draw semi-transparent background for text
            background_x = pos['x'] - self.padding
            background_y = pos['y'] - self.padding
            
            # Adjust background position based on alignment
            if pos['align'] == 'center':
                background_x -= text_width // 2
            elif pos['align'] == 'right':
                background_x -= text_width
            
            # Draw the background rectangle
            draw.rectangle(
                [(background_x, background_y), 
                 (background_x + text_width, background_y + text_height)],
                fill=self.background_color
            )
            
            # Draw the text
            text_x = pos['x']
            text_y = pos['y']
            
            # Adjust text position based on alignment
            if pos['align'] == 'center':
                text_x -= text_width // 2 - self.padding
            elif pos['align'] == 'right':
                text_x -= text_width - self.padding
            else:  # 'left'
                text_x += self.padding
            
            text_y += self.padding
            
            draw.text((text_x, text_y), text, font=self.font, fill=self.text_color)
            
            # Save the modified image to a new BytesIO object
            output = io.BytesIO()
            image.save(output, format='PNG')
            output.seek(0)
            
            return output
        except Exception as e:
            # In case of error, create an error image
            error_img = Image.new('RGB', (400, 100), color=(255, 0, 0))
            draw = ImageDraw.Draw(error_img)
            draw.text((10, 40), f"Text insertion error: {str(e)}", fill=(255, 255, 255))
            
            output = io.BytesIO()
            error_img.save(output, format='PNG')
            output.seek(0)
            
            print(f"Text insertion error: {str(e)}")
            return output
    
    def _calculate_position(self, image_size, text, position_params):
        """Calculate the position for text insertion based on parameters and image size."""
        width, height = image_size
        
        # Default position (bottom center)
        result = {
            'x': width // 2,
            'y': height - 50,
            'align': 'center'
        }
        
        if not position_params:
            return result
        
        # Extract position parameters
        if 'position' in position_params:
            # Predefined positions
            pos = position_params['position'].lower()
            
            if pos == 'top':
                result['y'] = 20
            elif pos == 'center':
                result['y'] = height // 2
            elif pos == 'bottom':
                result['y'] = height - 50
            elif pos == 'top-left':
                result['x'] = 20
                result['y'] = 20
                result['align'] = 'left'
            elif pos == 'top-right':
                result['x'] = width - 20
                result['y'] = 20
                result['align'] = 'right'
            elif pos == 'bottom-left':
                result['x'] = 20
                result['y'] = height - 50
                result['align'] = 'left'
            elif pos == 'bottom-right':
                result['x'] = width - 20
                result['y'] = height - 50
                result['align'] = 'right'
        
        # Override with explicit coordinates if provided
        if 'x' in position_params:
            result['x'] = position_params['x']
        if 'y' in position_params:
            result['y'] = position_params['y']
        if 'align' in position_params:
            result['align'] = position_params['align']
            
        return result


# Register the provider with the factory
TextInsertionFactory.register_provider("pil", PILTextInsertion)