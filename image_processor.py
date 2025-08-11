"""
Image processor module for converting images to pixel art.
Handles image loading, processing, and conversion logic.
"""

from typing import Tuple, Optional
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance


class ImageProcessor:
    """Handles image processing operations for pixel art conversion."""
    
    def __init__(self):
        self.original_image: Optional[Image.Image] = None
        self.processed_image: Optional[Image.Image] = None
    
    def load_image(self, file_path: str) -> bool:
        """
        Load an image from file path.
        
        Args:
            file_path: Path to the image file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.original_image = Image.open(file_path)
            # Convert to RGB if necessary
            if self.original_image.mode != 'RGB':
                self.original_image = self.original_image.convert('RGB')
            return True
        except Exception as e:
            print(f"Error loading image: {e}")
            return False
    
    def resize_image(self, image: Image.Image, target_size: Tuple[int, int], 
                    maintain_aspect: bool = True) -> Image.Image:
        """
        Resize image while optionally maintaining aspect ratio.
        
        Args:
            image: PIL Image object
            target_size: Tuple of (width, height)
            maintain_aspect: Whether to maintain aspect ratio
            
        Returns:
            Resized PIL Image
        """
        if maintain_aspect:
            image.thumbnail(target_size, Image.Resampling.NEAREST)
            return image
        else:
            return image.resize(target_size, Image.Resampling.NEAREST)
    
    def quantize_colors(self, image: Image.Image, num_colors: int) -> Image.Image:
        """
        Reduce the number of colors in the image.
        
        Args:
            image: PIL Image object
            num_colors: Number of colors to reduce to
            
        Returns:
            Color-quantized PIL Image
        """
        # Convert to P mode (palette) with specified number of colors
        quantized = image.quantize(colors=num_colors, method=Image.Quantize.MEDIANCUT)
        # Convert back to RGB
        return quantized.convert('RGB')
    
    def apply_pixelation(self, pixel_size: int, num_colors: int, 
                        contrast: float = 1.0, saturation: float = 1.0) -> bool:
        """
        Apply pixelation effect to the loaded image.
        
        Args:
            pixel_size: Size of each pixel block
            num_colors: Number of colors to use
            contrast: Contrast adjustment (1.0 = no change)
            saturation: Saturation adjustment (1.0 = no change)
            
        Returns:
            bool: True if successful, False otherwise
        """
        if self.original_image is None:
            return False
        
        try:
            # Start with original image
            img = self.original_image.copy()
            
            # Adjust contrast and saturation
            if contrast != 1.0:
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(contrast)
            
            if saturation != 1.0:
                enhancer = ImageEnhance.Color(img)
                img = enhancer.enhance(saturation)
            
            # Get original dimensions
            width, height = img.size
            
            # Calculate new dimensions for pixelation
            new_width = width // pixel_size
            new_height = height // pixel_size
            
            if new_width == 0 or new_height == 0:
                return False
            
            # Resize down with nearest neighbor
            small_img = img.resize((new_width, new_height), Image.Resampling.NEAREST)
            
            # Quantize colors
            small_img = self.quantize_colors(small_img, num_colors)
            
            # Resize back up to create pixel blocks
            self.processed_image = small_img.resize((width, height), Image.Resampling.NEAREST)
            
            return True
            
        except Exception as e:
            print(f"Error applying pixelation: {e}")
            return False
    
    def save_image(self, file_path: str, quality: int = 95) -> bool:
        """
        Save the processed image to file.
        
        Args:
            file_path: Output file path
            quality: JPEG quality (1-100)
            
        Returns:
            bool: True if successful, False otherwise
        """
        if self.processed_image is None:
            return False
        
        try:
            # Determine format from file extension
            file_extension = file_path.lower().split('.')[-1]
            
            if file_extension in ['jpg', 'jpeg']:
                self.processed_image.save(file_path, 'JPEG', quality=quality, optimize=True)
            elif file_extension == 'png':
                self.processed_image.save(file_path, 'PNG', optimize=True)
            elif file_extension == 'bmp':
                self.processed_image.save(file_path, 'BMP')
            else:
                # Default to PNG
                self.processed_image.save(file_path, 'PNG', optimize=True)
            
            return True
            
        except Exception as e:
            print(f"Error saving image: {e}")
            return False
    
    def get_processed_image(self) -> Optional[Image.Image]:
        """Get the processed image."""
        return self.processed_image
    
    def get_original_image(self) -> Optional[Image.Image]:
        """Get the original image."""
        return self.original_image
