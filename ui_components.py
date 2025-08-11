"""
UI components module containing reusable custom tkinter widgets.
Implements Material Design principles for consistent modern UI.
"""

import customtkinter as ctk
from typing import Callable, Optional, Any
from PIL import Image, ImageTk


class MaterialSlider(ctk.CTkSlider):
    """Custom slider with Material Design styling and value display."""
    
    def __init__(self, master, from_: float, to: float, 
                 label: str, initial_value: Optional[float] = None,
                 command: Optional[Callable] = None, **kwargs):
        super().__init__(master, from_=from_, to=to, command=self._on_value_change, **kwargs)
        
        self.label_text = label
        self.external_command = command
        
        # Create label
        self.label = ctk.CTkLabel(master, text=f"{label}: {initial_value or from_:.1f}")
        
        # Set initial value
        if initial_value is not None:
            self.set(initial_value)
        
        self._update_label(initial_value or from_)
    
    def _on_value_change(self, value: float):
        """Handle value change and update label."""
        self._update_label(value)
        if self.external_command:
            self.external_command(value)
    
    def _update_label(self, value: float):
        """Update the label with current value."""
        if isinstance(value, float):
            if value.is_integer():
                self.label.configure(text=f"{self.label_text}: {int(value)}")
            else:
                self.label.configure(text=f"{self.label_text}: {value:.1f}")
        else:
            self.label.configure(text=f"{self.label_text}: {value}")
    
    def pack_with_label(self, **kwargs):
        """Pack both label and slider."""
        self.label.pack(pady=(10, 5), **kwargs)
        self.pack(pady=(0, 10), **kwargs)
    
    def grid_with_label(self, row: int, column: int, **kwargs):
        """Grid both label and slider."""
        self.label.grid(row=row, column=column, pady=(10, 5), **kwargs)
        self.grid(row=row + 1, column=column, pady=(0, 10), **kwargs)


class ImagePreviewFrame(ctk.CTkFrame):
    """Frame for displaying image previews with scaling."""
    
    def __init__(self, master, title: str, max_size: tuple = (300, 300), **kwargs):
        super().__init__(master, **kwargs)
        
        self.max_size = max_size
        
        # Title
        self.title_label = ctk.CTkLabel(self, text=title, font=ctk.CTkFont(size=16, weight="bold"))
        self.title_label.pack(pady=(10, 5))
        
        # Image label
        self.image_label = ctk.CTkLabel(self, text="No image", width=max_size[0], height=max_size[1])
        self.image_label.pack(pady=10, padx=10)
        
        self.current_image: Optional[ImageTk.PhotoImage] = None
    
    def display_image(self, pil_image: Image.Image):
        """Display PIL image in the frame."""
        if pil_image is None:
            self.image_label.configure(image="", text="No image")
            return
        
        # Calculate size while maintaining aspect ratio
        img_copy = pil_image.copy()
        img_copy.thumbnail(self.max_size, Image.Resampling.LANCZOS)
        
        # Convert to PhotoImage
        self.current_image = ImageTk.PhotoImage(img_copy)
        
        # Update label
        self.image_label.configure(image=self.current_image, text="")
    
    def clear_image(self):
        """Clear the displayed image."""
        self.current_image = None
        self.image_label.configure(image="", text="No image")


class MaterialButton(ctk.CTkButton):
    """Custom button with Material Design styling."""
    
    def __init__(self, master, text: str, command: Optional[Callable] = None,
                 button_type: str = "primary", **kwargs):
        
        # Define color schemes
        color_schemes = {
            "primary": {
                "fg_color": "#1976D2",
                "hover_color": "#1565C0",
                "text_color": "white"
            },
            "secondary": {
                "fg_color": "#424242",
                "hover_color": "#303030",
                "text_color": "white"
            },
            "success": {
                "fg_color": "#388E3C",
                "hover_color": "#2E7D32",
                "text_color": "white"
            },
            "warning": {
                "fg_color": "#F57C00",
                "hover_color": "#EF6C00",
                "text_color": "white"
            }
        }
        
        colors = color_schemes.get(button_type, color_schemes["primary"])
        
        super().__init__(
            master,
            text=text,
            command=command,
            fg_color=colors["fg_color"],
            hover_color=colors["hover_color"],
            text_color=colors["text_color"],
            corner_radius=8,
            font=ctk.CTkFont(size=12, weight="bold"),
            **kwargs
        )


class ProgressFrame(ctk.CTkFrame):
    """Frame for showing progress information."""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.progress_label = ctk.CTkLabel(self, text="Ready")
        self.progress_label.pack(pady=10)
        
        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.pack(pady=10, padx=20, fill="x")
        self.progress_bar.set(0)
    
    def set_progress(self, value: float, text: str = ""):
        """Update progress bar and text."""
        self.progress_bar.set(value)
        if text:
            self.progress_label.configure(text=text)
    
    def reset_progress(self):
        """Reset progress to initial state."""
        self.progress_bar.set(0)
        self.progress_label.configure(text="Ready")


class ParameterPanel(ctk.CTkScrollableFrame):
    """Scrollable panel for adjustment parameters."""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.sliders = {}
        
        # Title
        title = ctk.CTkLabel(self, text="Pixel Art Parameters", 
                           font=ctk.CTkFont(size=18, weight="bold"))
        title.pack(pady=(10, 20))
    
    def add_slider(self, name: str, label: str, from_: float, to: float,
                   initial_value: float, command: Optional[Callable] = None) -> MaterialSlider:
        """Add a parameter slider to the panel."""
        slider = MaterialSlider(
            self, 
            from_=from_, 
            to=to, 
            label=label,
            initial_value=initial_value,
            command=command
        )
        slider.pack_with_label(fill="x", padx=20)
        
        self.sliders[name] = slider
        return slider
    
    def get_value(self, name: str) -> float:
        """Get current value of a slider."""
        if name in self.sliders:
            return self.sliders[name].get()
        return 0.0
    
    def get_all_values(self) -> dict:
        """Get all slider values as a dictionary."""
        return {name: slider.get() for name, slider in self.sliders.items()}
