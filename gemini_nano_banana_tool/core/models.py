"""Data models and constants for Gemini image generation.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from enum import Enum

# Supported aspect ratios and their resolutions (Flash model / 1K quality)
# These are baseline 1K resolutions used by Flash model and Pro model at 1K quality
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

# Resolution quality levels (Pro model only)
# Flash model only supports 1K (baseline resolutions above)
SUPPORTED_RESOLUTIONS: list[str] = ["1K", "2K", "4K"]

# Resolution scale multipliers for Pro model
# 1K = baseline (same as ASPECT_RATIO_RESOLUTIONS)
# 2K = ~2x scale, 4K = ~4x scale
RESOLUTION_MULTIPLIERS: dict[str, float] = {
    "1K": 1.0,  # 1024x1024 for 1:1
    "2K": 2.0,  # ~2048x2048 for 1:1
    "4K": 4.0,  # ~4096x4096 for 1:1
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


# Supported models for image generation (Gemini + Imagen)
SUPPORTED_MODELS: list[str] = [
    # Gemini models (Nano Banana)
    "gemini-2.5-flash-image",
    "gemini-3-pro-image-preview",
    # Imagen 4 models
    "imagen-4.0-generate-001",
    "imagen-4.0-ultra-generate-001",
    "imagen-4.0-fast-generate-001",
]

# Model descriptions for help text
MODEL_DESCRIPTIONS: dict[str, str] = {
    "gemini-2.5-flash-image": "Fast generation, fixed ~1024p resolution, 3 ref images",
    "gemini-3-pro-image-preview": (
        "Advanced quality, 1K/2K/4K resolution, 14 ref images, Google Search grounding"
    ),
    "imagen-4.0-generate-001": "Balanced quality and speed, photorealistic generation",
    "imagen-4.0-ultra-generate-001": "Highest quality, photorealism focus, slower generation",
    "imagen-4.0-fast-generate-001": "Fastest generation, good quality, cost-effective",
}

# Default model
DEFAULT_MODEL = "gemini-2.5-flash-image"

# Maximum number of reference images per model
# Pro model: 6 high-fidelity + 8 style/composition = 14 total
MAX_REFERENCE_IMAGES_PER_MODEL: dict[str, int] = {
    "gemini-2.5-flash-image": 3,
    "gemini-3-pro-image-preview": 14,
}

# Legacy constant for backward compatibility (uses flash model limit)
MAX_REFERENCE_IMAGES = 3

# Models that support variable resolution (1K/2K/4K)
MODELS_WITH_RESOLUTION_SUPPORT: list[str] = [
    "gemini-3-pro-image-preview",
]

# Default resolution for Pro model
DEFAULT_RESOLUTION = "1K"

# Pricing per output token (USD) - Gemini models
# Source: https://ai.google.dev/pricing
# Flash Image: $30/1M tokens = $0.00003 per token
# Pro Image: $120/1M tokens = $0.00012 per token
# Flash Text: $0.30/1M tokens = $0.0000003 per token
# Pro Text: $12/1M tokens = $0.000012 per token
# Experimental models: Free during preview (using Flash pricing as reference)
COST_PER_TOKEN: dict[str, float] = {
    "gemini-2.5-flash-image": 0.00003,  # $30 per 1M tokens (image generation)
    "gemini-3-pro-image-preview": 0.00012,  # $120 per 1M tokens (image generation)
    "gemini-2.5-flash": 0.0000003,  # $0.30 per 1M tokens (text generation)
    "gemini-2.0-flash-exp": 0.0000003,  # Free preview, using Flash pricing as reference
    "gemini-3-pro-preview": 0.000012,  # $12 per 1M tokens (text generation)
}

# Pricing per image (USD) - Imagen 4 models
# Source: https://cloud.google.com/vertex-ai/generative-ai/pricing
COST_PER_IMAGE: dict[str, float] = {
    "imagen-4.0-generate-001": 0.04,  # $0.04 per image
    "imagen-4.0-ultra-generate-001": 0.06,  # $0.06 per image
    "imagen-4.0-fast-generate-001": 0.02,  # $0.02 per image
}

# Example costs per image based on typical token usage:
# Gemini Flash: 1,290 tokens × $0.00003 = ~$0.039 per image
# Gemini Pro 1K/2K: 1,120 tokens × $0.00012 = ~$0.134 per image
# Gemini Pro 4K: 2,000 tokens × $0.00012 = ~$0.24 per image
# Imagen 4 Fast: $0.02 per image (flat rate)
# Imagen 4: $0.04 per image (flat rate)
# Imagen 4 Ultra: $0.06 per image (flat rate)


# Helper function to check if model uses Imagen API
def is_imagen_model(model: str) -> bool:
    """Check if model is an Imagen model (vs Gemini model)."""
    return model.startswith("imagen-")
