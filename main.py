"""
Main application module for Img2Pix - Image to Pixel Art Converter.
Provides a modern Material UI interface for converting images to pixel art.
"""

import os
import threading
from tkinter import filedialog, messagebox
from typing import Optional

import customtkinter as ctk

from utility import (
    ImageProcessor, MaterialButton, ImagePreviewFrame, 
    ParameterPanel, ProgressFrame, MaterialSlider
)


class Img2PixApp:
    """Main application class for the Image to Pixel Art converter."""
    
    def __init__(self):
        self.processor = ImageProcessor()
        self.current_file_path: Optional[str] = None
        self.processing_thread: Optional[threading.Thread] = None
        
        self._setup_ui()
        self._setup_parameters()
        self._bind_events()
    
    def _setup_ui(self):
        """Initialize the main UI components."""
        # Configure theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Main window
        self.root = ctk.CTk()
        self.root.title("Img2Pix - Image to Pixel Art Converter")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Configure grid weights
        self.root.grid_columnconfigure(1, weight=2)
        self.root.grid_columnconfigure(2, weight=2)
        self.root.grid_rowconfigure(0, weight=1)
        
        self._create_control_panel()
        self._create_image_previews()
        self._create_menu_bar()
    
    def _create_menu_bar(self):
        """Create the top menu bar with file operations."""
        menu_frame = ctk.CTkFrame(self.root, height=60)
        menu_frame.grid(row=0, column=0, columnspan=3, sticky="ew", padx=10, pady=(10, 0))
        menu_frame.grid_columnconfigure(4, weight=1)  # Expand space after buttons
        
        # Title
        title_label = ctk.CTkLabel(
            menu_frame, 
            text="Img2Pix", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=15)
        
        # File operation buttons
        MaterialButton(
            menu_frame, 
            text="📁 Open Image",
            command=self._open_image,
            width=120
        ).grid(row=0, column=1, padx=10, pady=15)
        
        MaterialButton(
            menu_frame, 
            text="💾 Save Result",
            command=self._save_image,
            button_type="success",
            width=120
        ).grid(row=0, column=2, padx=10, pady=15)
        
        MaterialButton(
            menu_frame, 
            text="🔄 Reset",
            command=self._reset_all,
            button_type="secondary",
            width=100
        ).grid(row=0, column=3, padx=10, pady=15)
    
    def _create_control_panel(self):
        """Create the left control panel with parameters."""
        self.control_panel = ParameterPanel(self.root, width=300)
        self.control_panel.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=10)
        
        # Process button
        self.process_button = MaterialButton(
            self.control_panel,
            text="🎨 Convert to Pixel Art",
            command=self._process_image,
            button_type="primary",
            height=40
        )
        self.process_button.pack(pady=20, padx=20, fill="x")
        
        # Progress frame
        self.progress_frame = ProgressFrame(self.control_panel)
        self.progress_frame.pack(pady=10, padx=20, fill="x")
        
        # Auto-process checkbox
        self.auto_process_var = ctk.BooleanVar(value=False)
        self.auto_process_cb = ctk.CTkCheckBox(
            self.control_panel,
            text="Auto-process on parameter change",
            variable=self.auto_process_var
        )
        self.auto_process_cb.pack(pady=10, padx=20)
    
    def _create_image_previews(self):
        """Create image preview frames."""
        # Original image preview
        self.original_preview = ImagePreviewFrame(
            self.root, 
            title="Original Image",
            max_size=(400, 400)
        )
        self.original_preview.grid(row=1, column=1, sticky="nsew", padx=5, pady=10)
        
        # Result image preview
        self.result_preview = ImagePreviewFrame(
            self.root, 
            title="Pixel Art Result",
            max_size=(400, 400)
        )
        self.result_preview.grid(row=1, column=2, sticky="nsew", padx=(5, 10), pady=10)
    
    def _setup_parameters(self):
        """Setup parameter sliders."""
        # Pixel size slider
        self.control_panel.add_slider(
            name="pixel_size",
            label="Pixel Size",
            from_=2,
            to=50,
            initial_value=8,
            command=self._on_parameter_change
        )
        
        # Number of colors slider
        self.control_panel.add_slider(
            name="colors",
            label="Number of Colors",
            from_=2,
            to=256,
            initial_value=32,
            command=self._on_parameter_change
        )
        
        # Contrast slider
        self.control_panel.add_slider(
            name="contrast",
            label="Contrast",
            from_=0.5,
            to=2.0,
            initial_value=1.0,
            command=self._on_parameter_change
        )
        
        # Saturation slider
        self.control_panel.add_slider(
            name="saturation",
            label="Saturation",
            from_=0.0,
            to=2.0,
            initial_value=1.2,
            command=self._on_parameter_change
        )
    
    def _bind_events(self):
        """Bind window events."""
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _on_parameter_change(self, value):
        """Handle parameter change."""
        if self.auto_process_var.get() and self.processor.get_original_image():
            self._process_image()
    
    def _open_image(self):
        """Open and load an image file."""
        file_types = [
            ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff"),
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpg *.jpeg"),
            ("All files", "*.*")
        ]
        
        file_path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=file_types
        )
        
        if file_path:
            self._load_image(file_path)
    
    def _load_image(self, file_path: str):
        """Load image from file path."""
        try:
            self.progress_frame.set_progress(0.3, "Loading image...")
            
            if self.processor.load_image(file_path):
                self.current_file_path = file_path
                
                # Display original image
                original_img = self.processor.get_original_image()
                self.original_preview.display_image(original_img)
                
                # Clear result preview
                self.result_preview.clear_image()
                
                self.progress_frame.set_progress(1.0, f"Loaded: {os.path.basename(file_path)}")
                
                # Auto-process if enabled
                if self.auto_process_var.get():
                    self.root.after(100, self._process_image)
                else:
                    self.progress_frame.reset_progress()
                
            else:
                messagebox.showerror("Error", "Failed to load image. Please check the file format.")
                self.progress_frame.reset_progress()
                
        except Exception as e:
            messagebox.showerror("Error", f"Error loading image: {str(e)}")
            self.progress_frame.reset_progress()
    
    def _process_image(self):
        """Process the loaded image with current parameters."""
        if not self.processor.get_original_image():
            messagebox.showwarning("Warning", "Please load an image first.")
            return
        
        # Disable process button during processing
        self.process_button.configure(state="disabled")
        
        # Start processing in separate thread
        self.processing_thread = threading.Thread(target=self._process_image_thread)
        self.processing_thread.daemon = True
        self.processing_thread.start()
    
    def _process_image_thread(self):
        """Process image in separate thread."""
        try:
            self.root.after(0, lambda: self.progress_frame.set_progress(0.2, "Processing image..."))
            
            # Get current parameter values
            params = self.control_panel.get_all_values()
            
            self.root.after(0, lambda: self.progress_frame.set_progress(0.5, "Applying pixelation..."))
            
            # Apply pixelation
            success = self.processor.apply_pixelation(
                pixel_size=int(params["pixel_size"]),
                num_colors=int(params["colors"]),
                contrast=params["contrast"],
                saturation=params["saturation"]
            )
            
            if success:
                self.root.after(0, lambda: self.progress_frame.set_progress(0.8, "Updating preview..."))
                
                # Update result preview
                result_img = self.processor.get_processed_image()
                self.root.after(0, lambda: self.result_preview.display_image(result_img))
                
                self.root.after(0, lambda: self.progress_frame.set_progress(1.0, "Processing complete!"))
                
                # Reset progress after delay
                self.root.after(2000, lambda: self.progress_frame.reset_progress())
            else:
                self.root.after(0, lambda: messagebox.showerror("Error", "Failed to process image."))
                self.root.after(0, lambda: self.progress_frame.reset_progress())
        
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Processing error: {str(e)}"))
            self.root.after(0, lambda: self.progress_frame.reset_progress())
        
        finally:
            # Re-enable process button
            self.root.after(0, lambda: self.process_button.configure(state="normal"))
    
    def _save_image(self):
        """Save the processed image."""
        if not self.processor.get_processed_image():
            messagebox.showwarning("Warning", "No processed image to save. Please process an image first.")
            return
        
        file_types = [
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpg"),
            ("BMP files", "*.bmp"),
            ("All files", "*.*")
        ]
        
        # Suggest filename based on original
        suggested_name = "pixel_art.png"
        if self.current_file_path:
            base_name = os.path.splitext(os.path.basename(self.current_file_path))[0]
            suggested_name = f"{base_name}_pixel_art.png"
        
        file_path = filedialog.asksaveasfilename(
            title="Save pixel art image",
            filetypes=file_types,
            defaultextension=".png",
            initialfile=suggested_name
        )
        
        if file_path:
            try:
                self.progress_frame.set_progress(0.5, "Saving image...")
                
                if self.processor.save_image(file_path):
                    self.progress_frame.set_progress(1.0, f"Saved: {os.path.basename(file_path)}")
                    messagebox.showinfo("Success", f"Image saved successfully!\n{file_path}")
                    
                    # Reset progress after delay
                    self.root.after(2000, lambda: self.progress_frame.reset_progress())
                else:
                    messagebox.showerror("Error", "Failed to save image.")
                    self.progress_frame.reset_progress()
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error saving image: {str(e)}")
                self.progress_frame.reset_progress()
    
    def _reset_all(self):
        """Reset the application to initial state."""
        # Clear processor
        self.processor = ImageProcessor()
        self.current_file_path = None
        
        # Clear previews
        self.original_preview.clear_image()
        self.result_preview.clear_image()
        
        # Reset progress
        self.progress_frame.reset_progress()
        
        # Reset parameters to default values
        self.control_panel.sliders["pixel_size"].set(8)
        self.control_panel.sliders["colors"].set(32)
        self.control_panel.sliders["contrast"].set(1.0)
        self.control_panel.sliders["saturation"].set(1.2)
    
    def _on_closing(self):
        """Handle application closing."""
        # Wait for processing thread to finish if running
        if self.processing_thread and self.processing_thread.is_alive():
            self.processing_thread.join(timeout=1.0)
        
        self.root.destroy()
    
    def run(self):
        """Start the application."""
        self.root.mainloop()


def main():
    """Main entry point."""
    try:
        app = Img2PixApp()
        app.run()
    except Exception as e:
        messagebox.showerror("Critical Error", f"Application failed to start: {str(e)}")


if __name__ == "__main__":
    main()
