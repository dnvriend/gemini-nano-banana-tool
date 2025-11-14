"""Utility functions for Gemini Nano Banana CLI.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import os
import sys
from pathlib import Path

from gemini_nano_banana_tool.core.models import (
    ASPECT_RATIO_RESOLUTIONS,
    MAX_REFERENCE_IMAGES,
    SUPPORTED_MODELS,
)


class ValidationError(Exception):
    """Raised when input validation fails."""

    pass


def load_prompt(
    prompt: str | None,
    prompt_file: str | None,
    use_stdin: bool,
) -> str:
    """Load prompt from argument, file, or stdin (mutually exclusive).

    Args:
        prompt: Direct prompt text
        prompt_file: Path to file containing prompt
        use_stdin: Whether to read from stdin

    Returns:
        The loaded prompt text

    Raises:
        ValidationError: If multiple sources provided, none provided, or loading fails

    Example:
        >>> # From argument
        >>> prompt = load_prompt("Hello world", None, False)
        >>>
        >>> # From file
        >>> prompt = load_prompt(None, "prompt.txt", False)
        >>>
        >>> # From stdin
        >>> prompt = load_prompt(None, None, True)
    """
    # Check mutually exclusive
    provided = [prompt is not None, prompt_file is not None, use_stdin]
    if sum(provided) == 0:
        raise ValidationError(
            "No prompt provided. Use one of: --prompt TEXT, --prompt-file FILE, or --stdin"
        )
    if sum(provided) > 1:
        raise ValidationError(
            "Multiple prompt sources provided. Use only one of: --prompt, --prompt-file, or --stdin"
        )

    # Load from appropriate source
    if prompt:
        return prompt.strip()

    if prompt_file:
        try:
            with open(prompt_file, encoding="utf-8") as f:
                content = f.read().strip()
            if not content:
                raise ValidationError(f"Prompt file is empty: {prompt_file}")
            return content
        except FileNotFoundError:
            raise ValidationError(
                f"Prompt file not found: {prompt_file}. "
                f"Ensure the file exists and the path is correct."
            )
        except PermissionError:
            raise ValidationError(f"Permission denied reading prompt file: {prompt_file}")
        except Exception as e:
            raise ValidationError(f"Failed to read prompt file {prompt_file}: {e}")

    if use_stdin:
        try:
            content = sys.stdin.read().strip()
            if not content:
                raise ValidationError(
                    "No input received from stdin. "
                    "Pipe content or use --prompt or --prompt-file instead."
                )
            return content
        except Exception as e:
            raise ValidationError(f"Failed to read from stdin: {e}")

    # Should never reach here
    raise ValidationError("Internal error: no prompt source handled")


def validate_reference_images(image_paths: list[str]) -> None:
    """Validate reference images (max 3, all exist).

    Args:
        image_paths: List of image file paths

    Raises:
        ValidationError: If validation fails

    Example:
        >>> validate_reference_images(["img1.jpg", "img2.jpg"])
        >>> # Raises ValidationError if more than 3 images or any don't exist
    """
    if len(image_paths) > MAX_REFERENCE_IMAGES:
        raise ValidationError(
            f"Too many reference images: {len(image_paths)}. "
            f"Maximum allowed is {MAX_REFERENCE_IMAGES}. "
            f"Provided: {', '.join(image_paths)}"
        )

    for img_path in image_paths:
        if not os.path.exists(img_path):
            raise ValidationError(
                f"Reference image not found: {img_path}. "
                f"Ensure the file exists and the path is correct."
            )
        if not os.path.isfile(img_path):
            raise ValidationError(f"Reference image path is not a file: {img_path}")


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
        # Ensure parent directory exists
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Write image data
        with open(output_path, "wb") as f:
            f.write(image_data)
    except PermissionError:
        raise ValidationError(
            f"Permission denied writing to: {output_path}. "
            f"Check directory permissions or choose a different location."
        )
    except OSError as e:
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
