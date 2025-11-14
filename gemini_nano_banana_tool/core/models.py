"""Data models and constants for Gemini image generation.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from enum import Enum

# Supported aspect ratios and their resolutions
ASPECT_RATIO_RESOLUTIONS: dict[str, tuple[int, int]] = {
    "1:1": (1024, 1024),
    "16:9": (1344, 768),
    "9:16": (768, 1344),
    "4:3": (1184, 864),
    "3:4": (864, 1184),
    "3:2": (1248, 832),
    "2:3": (832, 1248),
    "21:9": (1536, 672),
    "4:5": (896, 1152),
    "5:4": (1152, 896),
}

# Aspect ratio descriptions for help text
ASPECT_RATIO_DESCRIPTIONS: dict[str, str] = {
    "1:1": "Square (Instagram post, social media)",
    "16:9": "Widescreen (YouTube thumbnail, desktop)",
    "9:16": "Vertical (Instagram story, TikTok, mobile)",
    "4:3": "Traditional (classic photography)",
    "3:4": "Portrait orientation",
    "3:2": "DSLR photography",
    "2:3": "Portrait photography",
    "21:9": "Cinematic (ultra-wide)",
    "4:5": "Instagram portrait",
    "5:4": "Medium format photography",
}


class AspectRatio(str, Enum):
    """Supported aspect ratios for image generation."""

    RATIO_1_1 = "1:1"
    RATIO_16_9 = "16:9"
    RATIO_9_16 = "9:16"
    RATIO_4_3 = "4:3"
    RATIO_3_4 = "3:4"
    RATIO_3_2 = "3:2"
    RATIO_2_3 = "2:3"
    RATIO_21_9 = "21:9"
    RATIO_4_5 = "4:5"
    RATIO_5_4 = "5:4"


# Supported Gemini models for image generation
SUPPORTED_MODELS: list[str] = [
    "gemini-2.5-flash-image",
    "gemini-2.0-flash-exp",
    "gemini-1.5-pro",
    "gemini-1.5-flash",
]

# Model descriptions for help text
MODEL_DESCRIPTIONS: dict[str, str] = {
    "gemini-2.5-flash-image": "Fast, high-quality image generation (default)",
    "gemini-2.0-flash-exp": "Experimental features",
    "gemini-1.5-pro": "Higher quality, slower generation",
    "gemini-1.5-flash": "Fast generation",
}

# Default model
DEFAULT_MODEL = "gemini-2.5-flash-image"

# Maximum number of reference images
MAX_REFERENCE_IMAGES = 3
