"""Image generation logic for Gemini Nano Banana.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import base64
from typing import Any

from google import genai
from google.genai import types

from gemini_nano_banana_tool.core.models import (
    ASPECT_RATIO_RESOLUTIONS,
    DEFAULT_MODEL,
)
from gemini_nano_banana_tool.utils import save_image


class GenerationError(Exception):
    """Raised when image generation fails."""

    pass


def generate_image(
    client: genai.Client,
    prompt: str,
    output_path: str,
    reference_images: list[str] | None = None,
    aspect_ratio: str = "1:1",
    model: str = DEFAULT_MODEL,
) -> dict[str, Any]:
    """Generate image from prompt and optional reference images.

    Args:
        client: Configured Gemini client
        prompt: Text prompt for image generation
        output_path: Path to save generated image
        reference_images: Optional list of reference image paths (max 3)
        aspect_ratio: Aspect ratio (e.g., "16:9")
        model: Gemini model to use

    Returns:
        dict with keys:
            - output_path: Path where image was saved
            - model: Model used
            - aspect_ratio: Aspect ratio used
            - resolution: Resolution string (e.g., "1344x768")
            - reference_image_count: Number of reference images provided
            - token_count: Total tokens used
            - metadata: Additional generation metadata

    Raises:
        GenerationError: If image generation fails
        FileNotFoundError: If reference images don't exist

    Example:
        >>> from gemini_nano_banana_tool import create_client, generate_image
        >>> client = create_client()
        >>> result = generate_image(
        ...     client=client,
        ...     prompt="A beautiful sunset",
        ...     output_path="sunset.png",
        ...     aspect_ratio="16:9"
        ... )
        >>> print(f"Generated: {result['output_path']}")
    """
    try:
        # Build contents for the generation request
        contents: list[types.Part] = []

        # Add reference images if provided
        if reference_images:
            for img_path in reference_images:
                try:
                    with open(img_path, "rb") as f:
                        image_data = f.read()
                    # Create Part with inline data
                    contents.append(
                        types.Part(
                            inline_data=types.Blob(
                                mime_type=_get_mime_type(img_path),
                                data=image_data,
                            )
                        )
                    )
                except FileNotFoundError:
                    raise GenerationError(
                        f"Reference image not found: {img_path}. "
                        f"Ensure the file exists and the path is correct."
                    )
                except PermissionError:
                    raise GenerationError(f"Permission denied reading reference image: {img_path}")
                except Exception as e:
                    raise GenerationError(f"Failed to load reference image {img_path}: {e}")

        # Add text prompt
        contents.append(types.Part(text=prompt))

        # Configure generation with aspect ratio
        config = types.GenerateContentConfig(
            response_modalities=["IMAGE"],
            image_config=types.ImageConfig(
                aspect_ratio=aspect_ratio,
            ),
        )

        # Generate content
        response = client.models.generate_content(
            model=model,
            contents=contents,  # type: ignore[arg-type]
            config=config,
        )

        # Extract image from response
        if not response.candidates:
            raise GenerationError("No candidates returned from API. Request may have been blocked.")

        candidate = response.candidates[0]

        # Check for content filtering
        if not candidate.content or not candidate.content.parts:
            finish_reason = getattr(candidate, "finish_reason", "UNKNOWN")
            raise GenerationError(
                f"No content generated. Finish reason: {finish_reason}. "
                f"The prompt may have been blocked by safety filters."
            )

        # Find the image part
        image_part = None
        for part in candidate.content.parts:
            if hasattr(part, "inline_data") and part.inline_data:
                image_part = part
                break

        if not image_part:
            raise GenerationError(
                "No image data found in response. The model may have returned text only."
            )

        # Decode and save image
        try:
            # Handle both bytes and base64-encoded string
            if image_part.inline_data and image_part.inline_data.data:
                image_bytes = (
                    base64.b64decode(image_part.inline_data.data)
                    if isinstance(image_part.inline_data.data, str)
                    else image_part.inline_data.data
                )
                save_image(image_bytes, output_path)
            else:
                raise GenerationError("No image data available in response")
        except Exception as e:
            raise GenerationError(f"Failed to save generated image: {e}")

        # Extract token usage
        token_count = 0
        if hasattr(response, "usage_metadata") and response.usage_metadata:
            token_count = getattr(response.usage_metadata, "total_token_count", 0)

        # Format resolution
        width, height = ASPECT_RATIO_RESOLUTIONS.get(aspect_ratio, (0, 0))
        resolution = f"{width}x{height}"

        # Build result
        return {
            "output_path": output_path,
            "model": model,
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
            "reference_image_count": len(reference_images) if reference_images else 0,
            "token_count": token_count,
            "metadata": {
                "finish_reason": getattr(candidate, "finish_reason", "UNKNOWN"),
                "safety_ratings": getattr(candidate, "safety_ratings", None),
            },
        }

    except GenerationError:
        raise
    except Exception as e:
        raise GenerationError(
            f"Image generation failed: {e}. "
            f"Check your API key, network connection, and input parameters."
        )


def _get_mime_type(file_path: str) -> str:
    """Determine MIME type from file extension.

    Args:
        file_path: Path to image file

    Returns:
        MIME type string (e.g., "image/png")
    """
    ext = file_path.lower().split(".")[-1]
    mime_types = {
        "png": "image/png",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "webp": "image/webp",
        "gif": "image/gif",
    }
    return mime_types.get(ext, "image/jpeg")
