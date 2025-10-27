# PixelLab API Configuration Template
# Copy this file to pixellab_config.py and add your API key

# Get your API key from: https://pixellab.ai/api
PIXELLAB_API_KEY = "your_api_key_here"

# API Configuration
PIXELLAB_API_URL = "https://api.pixellab.ai/v1"
PIXELLAB_TIMEOUT = 300  # seconds

# Default generation settings
DEFAULT_STYLE = "pixel_art"
DEFAULT_SIZE = 64
DEFAULT_ANIMATIONS = ["idle", "walk", "attack", "death"]
DEFAULT_FRAMES = {
    "idle": 4,
    "walk": 8,
    "attack": 6,
    "death": 8
}
