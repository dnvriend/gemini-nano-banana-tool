"""Gemini Nano Banana Tool - Professional AI image generation CLI and library.

A professional CLI and Python library for generating, editing, and manipulating images
using Google's Gemini 2.5 Flash Image model (codename "Nano Banana").

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from gemini_nano_banana_tool.core.client import (
    AuthenticationError,
    GeminiClientError,
    create_client,
    validate_client,
)
from gemini_nano_banana_tool.core.generator import GenerationError, generate_image
from gemini_nano_banana_tool.core.models import (
    ASPECT_RATIO_DESCRIPTIONS,
    ASPECT_RATIO_RESOLUTIONS,
    DEFAULT_MODEL,
    MAX_REFERENCE_IMAGES,
    MODEL_DESCRIPTIONS,
    SUPPORTED_MODELS,
    AspectRatio,
)
from gemini_nano_banana_tool.utils import (
    ValidationError,
    format_resolution,
    load_prompt,
    save_image,
    validate_aspect_ratio,
    validate_model,
    validate_reference_images,
)

__version__ = "1.0.0"

__all__ = [
    # Version
    "__version__",
    # Client
    "create_client",
    "validate_client",
    "GeminiClientError",
    "AuthenticationError",
    # Generator
    "generate_image",
    "GenerationError",
    # Models
    "AspectRatio",
    "ASPECT_RATIO_RESOLUTIONS",
    "ASPECT_RATIO_DESCRIPTIONS",
    "SUPPORTED_MODELS",
    "MODEL_DESCRIPTIONS",
    "DEFAULT_MODEL",
    "MAX_REFERENCE_IMAGES",
    # Utils
    "load_prompt",
    "validate_reference_images",
    "validate_aspect_ratio",
    "validate_model",
    "save_image",
    "format_resolution",
    "ValidationError",
]
