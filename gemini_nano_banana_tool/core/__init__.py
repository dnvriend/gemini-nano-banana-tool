"""Core library modules for Gemini Nano Banana image generation.

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
    MODEL_DESCRIPTIONS,
    SUPPORTED_MODELS,
    AspectRatio,
)
from gemini_nano_banana_tool.core.prompt_templates import (
    TEMPLATE_DESCRIPTIONS,
    detect_category,
    get_template,
    list_templates,
)
from gemini_nano_banana_tool.core.promptgen import (
    PromptGenerationError,
    format_verbose_output,
    generate_prompt,
)

__all__ = [
    # Client
    "create_client",
    "validate_client",
    "GeminiClientError",
    "AuthenticationError",
    # Generator
    "generate_image",
    "GenerationError",
    # Promptgen
    "generate_prompt",
    "PromptGenerationError",
    "format_verbose_output",
    # Templates
    "get_template",
    "detect_category",
    "list_templates",
    "TEMPLATE_DESCRIPTIONS",
    # Models
    "AspectRatio",
    "ASPECT_RATIO_RESOLUTIONS",
    "ASPECT_RATIO_DESCRIPTIONS",
    "SUPPORTED_MODELS",
    "MODEL_DESCRIPTIONS",
    "DEFAULT_MODEL",
]
