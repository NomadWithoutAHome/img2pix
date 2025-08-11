# Img2Pix - Image to Pixel Art Converter

A modern Python application with Material UI design that converts any image into stunning pixel art. Built with separation of concerns, following PEP standards, and implementing DRY principles.

## Features

- 🎨 **Modern Material UI Interface** - Clean, intuitive design with dark theme
- 🖼️ **Real-time Preview** - See original and converted images side by side
- ⚡ **Live Processing** - Auto-process option for real-time parameter adjustments
- 🎛️ **Comprehensive Controls** - Fine-tune pixel size, colors, contrast, and saturation
- 💾 **Multiple Formats** - Support for PNG, JPEG, BMP, GIF, and TIFF
- 🧵 **Non-blocking Processing** - Threaded processing keeps UI responsive
- 📊 **Progress Tracking** - Visual progress indicators for all operations
- 🔍 **Advanced Transparency Support** - Full RGBA and alpha channel preservation
- 🎮 **Game Asset Ready** - Perfect for sprites, icons, and UI elements
- 🌈 **Smart Background Handling** - Configurable background compositing

## Screenshot

The application features a three-panel layout:
- **Left Panel**: Parameter controls with sliders for pixel size, color count, contrast, and saturation
- **Center Panel**: Original image preview
- **Right Panel**: Pixel art result preview

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Setup

1. **Clone or download the project**:
   ```bash
   cd E:\img2pix
   ```

2. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

## Usage

### Basic Workflow

1. **Open an Image**: Click "📁 Open Image" to select your source image
2. **Adjust Parameters**: Use the sliders to fine-tune the pixel art effect:
   - **Pixel Size** (2-50): Controls the size of individual pixel blocks
   - **Number of Colors** (2-256): Reduces color palette for retro effect
   - **Contrast** (0.5-2.0): Adjusts image contrast
   - **Saturation** (0.0-2.0): Controls color intensity
3. **Process**: Click "🎨 Convert to Pixel Art" or enable auto-processing
4. **Save**: Click "💾 Save Result" to export your pixel art

### Tips for Best Results

- **Portrait/Character Images**: Use smaller pixel sizes (4-12) with more colors (64-128)
- **Landscape/Scene Images**: Try larger pixel sizes (8-20) with fewer colors (16-64)
- **Retro Game Style**: Use 8-16 pixel size with 8-32 colors
- **High Contrast**: Increase contrast to 1.3-1.5 for more defined edges
- **Vibrant Colors**: Boost saturation to 1.2-1.5 for more vivid pixel art
- **Transparent Images**: PNG format preserves transparency perfectly
- **Game Sprites**: Perfect for character sprites and UI elements
- **Icons & Logos**: Maintains crisp transparent edges

## Project Structure

The application follows clean architecture principles with separation of concerns:

```
img2pix/
├── main.py              # Main application entry point and UI coordination
├── utility/             # Utility package containing core functionality
│   ├── __init__.py      # Package initialization with clean imports
│   ├── image_processor.py   # Core image processing logic
│   └── ui_components.py     # Reusable UI components and widgets
├── requirements.txt     # Project dependencies
├── .gitignore          # Git ignore patterns (includes __pycache__)
├── .gitattributes      # Git file handling and line ending rules
└── README.md           # Project documentation
```

### Architecture

- **`main.py`**: Application entry point, coordinates UI and processing, handles events
- **`utility/` Package**: Organized utility modules with clean imports
  - **`ImageProcessor`**: Handles all image operations (loading, processing, saving)
  - **UI Components**: Modular, reusable widgets following Material Design principles
- **Package Design**: Proper Python package structure with `__init__.py` for clean imports
- **Threading**: Non-blocking image processing for smooth user experience
- **Git Configuration**: Comprehensive ignore rules and file attribute handling

## Advanced Features

### 🔍 Transparency Support

Img2Pix provides comprehensive transparency handling for professional pixel art creation:

#### **Supported Transparency Types**
- **RGBA Images** - Full 32-bit transparency (PNG)
- **Palette Transparency** - GIF-style transparency
- **Alpha Channels** - Variable transparency levels
- **Binary Transparency** - Fully transparent or opaque pixels

#### **Smart Processing**
- **Automatic Detection** - Identifies transparent images automatically
- **Channel Separation** - Processes RGB and alpha channels independently
- **Edge Preservation** - Maintains crisp transparent edges during pixelation
- **Color Quantization** - Reduces colors while preserving transparency
- **Background Compositing** - Optional background color application

#### **Perfect For**
- 🎮 **Game Sprites** - Character animations and game assets
- 🏷️ **Icons & Logos** - UI elements with transparent backgrounds
- 🖼️ **Interface Graphics** - Buttons, panels, and HUD elements
- 🎨 **Digital Art** - Layered artwork with transparency

#### **Technical Implementation**
- Uses RGBA mode for transparent images
- Nearest-neighbor resampling preserves alpha edges
- Separate color quantization for RGB and alpha channels
- Optional background compositing with configurable colors
- Maintains transparency throughout the entire processing pipeline

### 🎯 Use Cases

#### **Game Development**
- Character sprites with transparent backgrounds
- UI elements and interface graphics
- Tile sets and environmental assets
- Animation frames with alpha channels

#### **Digital Art & Design**
- Logo pixelization with transparency
- Icon creation for applications
- Retro-style graphics with modern transparency
- Layered artwork preparation

#### **Web & Mobile**
- Pixelated icons for retro-themed websites
- Mobile app graphics with transparency
- Social media profile images
- Custom emoji and stickers

## Supported Formats

### Input Formats
- **PNG** - Full RGBA transparency support
- **GIF** - Palette-based transparency
- **JPEG, JPG** - Opaque images only
- **BMP** - Basic bitmap support
- **TIFF** - Advanced format support
- Most common image formats with automatic format detection

### Output Formats
- **PNG** - Recommended for transparency and pixel art quality
- **JPEG** - Opaque images with quality settings (1-100)
- **BMP** - Uncompressed bitmap format
- Automatic format detection based on file extension

## Technical Details

### Key Libraries
- **CustomTkinter**: Modern UI framework with Material Design
- **Pillow (PIL)**: Comprehensive image processing
- **NumPy**: Efficient numerical operations
- **Threading**: Responsive UI during processing

### Processing Pipeline
1. **Image Loading**: Convert to RGB, validate format
2. **Enhancement**: Apply contrast and saturation adjustments
3. **Pixelation**: Resize down using nearest-neighbor sampling
4. **Color Quantization**: Reduce color palette using median cut algorithm
5. **Upscaling**: Resize back up to create pixel blocks
6. **Output**: Save in desired format with optimization

### Performance Features
- **Threaded Processing**: UI remains responsive during conversion
- **Memory Efficient**: Optimized image handling for large files
- **Progressive Updates**: Real-time progress feedback
- **Error Handling**: Graceful handling of invalid files/formats

## Customization

### Adding New Parameters
To add new image processing parameters:

1. Add slider in `main.py` `_setup_parameters()`:
   ```python
   self.control_panel.add_slider(
       name="new_param",
       label="New Parameter",
       from_=0.0,
       to=2.0,
       initial_value=1.0,
       command=self._on_parameter_change
   )
   ```

2. Update `image_processor.py` `apply_pixelation()` to use the parameter
3. Pass the parameter in `main.py` `_process_image_thread()`

### Custom UI Themes
Modify color schemes in `ui_components.py` `MaterialButton` color_schemes dictionary.

## Troubleshooting

### Common Issues

**"Failed to load image"**
- Ensure the image file is not corrupted
- Check that the file format is supported
- Verify file permissions

**"Processing error"**
- Try reducing image size if very large (>10MB)
- Check available memory
- Restart application if needed

**Slow processing**
- Large images take more time to process
- Reduce pixel size for faster processing
- Close other memory-intensive applications

### Performance Tips
- For large images, start with larger pixel sizes
- Use PNG for output to preserve pixel art quality
- Enable auto-processing only for small to medium images

## License

This project is open source. Feel free to modify and distribute according to your needs.

