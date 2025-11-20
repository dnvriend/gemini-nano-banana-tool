"""Utility functions for Gemini Nano Banana CLI.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import logging
import os
import sys
from pathlib import Path

from gemini_nano_banana_tool.core.models import (
    ASPECT_RATIO_RESOLUTIONS,
    SUPPORTED_MODELS,
)

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Raised when input validation fails."""

    pass


def load_prompt(
    prompt: str | None,
    prompt_file: str | None,
    use_stdin: bool,
) -> str:
    """Load prompt from positional argument, file, or stdin (mutually exclusive).

    Args:
        prompt: Direct prompt text from positional argument
        prompt_file: Path to file containing prompt
        use_stdin: Whether to read from stdin

    Returns:
        The loaded prompt text

    Raises:
        ValidationError: If multiple sources provided, none provided, or loading fails

    Example:
        >>> # From positional argument
        >>> prompt = load_prompt("Hello world", None, False)
        >>>
        >>> # From file
        >>> prompt = load_prompt(None, "prompt.txt", False)
        >>>
        >>> # From stdin
        >>> prompt = load_prompt(None, None, True)
    """
    # Check mutually exclusive
    logger.debug("Loading prompt from source...")
    provided = [prompt is not None, prompt_file is not None, use_stdin]
    if sum(provided) == 0:
        logger.error("No prompt source provided")
        raise ValidationError(
            "No prompt provided. Use one of: PROMPT (positional), --prompt-file FILE, or --stdin"
        )
    if sum(provided) > 1:
        logger.error(f"Multiple prompt sources provided: {provided}")
        raise ValidationError(
            "Multiple prompt sources provided. "
            "Use only one of: PROMPT (positional), --prompt-file, or --stdin"
        )

    # Load from appropriate source
    if prompt:
        logger.debug("Loading prompt from argument")
        return prompt.strip()

    if prompt_file:
        logger.debug(f"Loading prompt from file: {prompt_file}")
        try:
            with open(prompt_file, encoding="utf-8") as f:
                content = f.read().strip()
            if not content:
                logger.error(f"Prompt file is empty: {prompt_file}")
                raise ValidationError(f"Prompt file is empty: {prompt_file}")
            logger.debug(f"Prompt loaded from file: {len(content)} characters")
            return content
        except FileNotFoundError:
            logger.error(f"Prompt file not found: {prompt_file}")
            raise ValidationError(
                f"Prompt file not found: {prompt_file}. "
                f"Ensure the file exists and the path is correct."
            )
        except PermissionError:
            logger.error(f"Permission denied reading prompt file: {prompt_file}")
            raise ValidationError(f"Permission denied reading prompt file: {prompt_file}")
        except Exception as e:
            logger.error(f"Failed to read prompt file {prompt_file}: {e}")
            logger.debug("Prompt file read error details:", exc_info=True)
            raise ValidationError(f"Failed to read prompt file {prompt_file}: {e}")

    if use_stdin:
        logger.debug("Loading prompt from stdin")
        try:
            content = sys.stdin.read().strip()
            if not content:
                logger.error("No input received from stdin")
                raise ValidationError(
                    "No input received from stdin. "
                    "Pipe content or use --prompt or --prompt-file instead."
                )
            logger.debug(f"Prompt loaded from stdin: {len(content)} characters")
            return content
        except Exception as e:
            logger.error(f"Failed to read from stdin: {e}")
            logger.debug("Stdin read error details:", exc_info=True)
            raise ValidationError(f"Failed to read from stdin: {e}")

    # Should never reach here
    raise ValidationError("Internal error: no prompt source handled")


def validate_reference_images(image_paths: list[str], model: str | None = None) -> None:
    """Validate reference images based on model limits (all must exist).

    Args:
        image_paths: List of image file paths
        model: Gemini model name (determines max images: flash=3, pro=6)

    Raises:
        ValidationError: If validation fails

    Example:
        >>> validate_reference_images(["img1.jpg", "img2.jpg"], "gemini-2.5-flash-image")
        >>> # Raises ValidationError if too many images or any don't exist
    """
    from gemini_nano_banana_tool.core.models import (
        DEFAULT_MODEL,
        MAX_REFERENCE_IMAGES_PER_MODEL,
    )

    # Determine max images for the model
    model_to_use = model or DEFAULT_MODEL
    max_images = MAX_REFERENCE_IMAGES_PER_MODEL.get(model_to_use, 3)

    logger.debug(
        f"Validating {len(image_paths)} reference images "
        f"for model {model_to_use} (max={max_images})"
    )

    if len(image_paths) > max_images:
        logger.error(f"Too many reference images: {len(image_paths)} > {max_images}")
        raise ValidationError(
            f"Too many reference images: {len(image_paths)}. "
            f"Maximum allowed for {model_to_use} is {max_images}. "
            f"Provided: {', '.join(image_paths)}"
        )

    for img_path in image_paths:
        logger.debug(f"Validating reference image: {img_path}")
        if not os.path.exists(img_path):
            logger.error(f"Reference image not found: {img_path}")
            raise ValidationError(
                f"Reference image not found: {img_path}. "
                f"Ensure the file exists and the path is correct."
            )
        if not os.path.isfile(img_path):
            logger.error(f"Reference image path is not a file: {img_path}")
            raise ValidationError(f"Reference image path is not a file: {img_path}")
    logger.debug("All reference images validated successfully")


def validate_aspect_ratio(aspect_ratio: str) -> None:
    """Validate aspect ratio is supported.

    Args:
        aspect_ratio: Aspect ratio string (e.g., "16:9")

    Raises:
        ValidationError: If aspect ratio is not supported

    Example:
        >>> validate_aspect_ratio("16:9")
        >>> # Raises ValidationError if not in supported list
    """
    if aspect_ratio not in ASPECT_RATIO_RESOLUTIONS:
        supported = ", ".join(ASPECT_RATIO_RESOLUTIONS.keys())
        raise ValidationError(
            f"Unsupported aspect ratio: {aspect_ratio}. "
            f"Supported ratios: {supported}. "
            f"Use 'gemini-nano-banana-tool list-aspect-ratios' to see all options."
        )


def validate_model(model: str) -> None:
    """Validate model is supported.

    Args:
        model: Model name

    Raises:
        ValidationError: If model is not supported

    Example:
        >>> validate_model("gemini-2.5-flash-image")
        >>> # Raises ValidationError if not in supported list
    """
    if model not in SUPPORTED_MODELS:
        supported = ", ".join(SUPPORTED_MODELS)
        raise ValidationError(
            f"Unsupported model: {model}. "
            f"Supported models: {supported}. "
            f"Use 'gemini-nano-banana-tool list-models' to see all options."
        )


def save_image(image_data: bytes, output_path: str) -> None:
    """Save image bytes to file.

    Args:
        image_data: Image data as bytes
        output_path: Output file path

    Raises:
        ValidationError: If save fails

    Example:
        >>> save_image(b"\\x89PNG...", "output.png")
    """
    try:
        logger.debug(f"Saving image to: {output_path}")
        # Ensure parent directory exists
        output_file = Path(output_path)
        if not output_file.parent.exists():
            logger.debug(f"Creating parent directory: {output_file.parent}")
            output_file.parent.mkdir(parents=True, exist_ok=True)

        # Write image data
        logger.debug(f"Writing {len(image_data)} bytes to file")
        with open(output_path, "wb") as f:
            f.write(image_data)
        logger.debug(f"Image saved successfully to: {output_path}")
    except PermissionError:
        logger.error(f"Permission denied writing to: {output_path}")
        raise ValidationError(
            f"Permission denied writing to: {output_path}. "
            f"Check directory permissions or choose a different location."
        )
    except OSError as e:
        logger.error(f"Failed to save image to {output_path}: {e}")
        logger.debug("Image save error details:", exc_info=True)
        raise ValidationError(f"Failed to save image to {output_path}: {e}")


def format_resolution(aspect_ratio: str) -> str:
    """Format resolution string from aspect ratio.

    Args:
        aspect_ratio: Aspect ratio string (e.g., "16:9")

    Returns:
        Formatted resolution string (e.g., "1344x768")

    Example:
        >>> format_resolution("16:9")
        '1344x768'
    """
    if aspect_ratio in ASPECT_RATIO_RESOLUTIONS:
        width, height = ASPECT_RATIO_RESOLUTIONS[aspect_ratio]
        return f"{width}x{height}"
    return "unknown"
