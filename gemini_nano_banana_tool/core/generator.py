"""Image generation logic for Gemini Nano Banana.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import base64
import logging
from typing import Any

from google import genai
from google.genai import types

from gemini_nano_banana_tool.core.models import (
    ASPECT_RATIO_RESOLUTIONS,
    COST_PER_TOKEN,
    DEFAULT_MODEL,
    DEFAULT_RESOLUTION,
    MODELS_WITH_RESOLUTION_SUPPORT,
)
from gemini_nano_banana_tool.utils import save_image

logger = logging.getLogger(__name__)


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
    resolution: str | None = None,
) -> dict[str, Any]:
    """Generate image from prompt and optional reference images.

    Args:
        client: Configured Gemini client
        prompt: Text prompt for image generation
        output_path: Path to save generated image
        reference_images: Optional list of reference image paths (max 3 Flash, 14 Pro)
        aspect_ratio: Aspect ratio (e.g., "16:9")
        model: Gemini model to use
        resolution: Resolution quality for Pro model (1K/2K/4K), ignored for Flash

    Returns:
        dict with keys:
            - output_path: Path where image was saved
            - model: Model used
            - aspect_ratio: Aspect ratio used
            - resolution: Resolution string (e.g., "1344x768")
            - resolution_quality: Resolution quality level (1K/2K/4K)
            - reference_image_count: Number of reference images provided
            - token_count: Total tokens used
            - estimated_cost_usd: Estimated cost in USD based on token usage
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
        logger.debug(
            f"Starting image generation: model={model}, aspect_ratio={aspect_ratio}, "
            f"resolution={resolution or 'default'}, "
            f"reference_images={len(reference_images) if reference_images else 0}"
        )
        logger.debug(f"Prompt length: {len(prompt)} characters")

        # Build contents for the generation request
        contents: list[types.Part] = []

        # Add reference images if provided
        if reference_images:
            logger.info(f"Loading {len(reference_images)} reference image(s)")
            for img_path in reference_images:
                try:
                    logger.debug(f"Loading reference image: {img_path}")
                    with open(img_path, "rb") as f:
                        image_data = f.read()
                    mime_type = _get_mime_type(img_path)
                    logger.debug(
                        f"Reference image loaded: {img_path}, "
                        f"size={len(image_data)} bytes, mime_type={mime_type}"
                    )
                    # Create Part with inline data
                    contents.append(
                        types.Part(
                            inline_data=types.Blob(
                                mime_type=mime_type,
                                data=image_data,
                            )
                        )
                    )
                except FileNotFoundError:
                    logger.error(f"Reference image not found: {img_path}")
                    raise GenerationError(
                        f"Reference image not found: {img_path}. "
                        f"Ensure the file exists and the path is correct."
                    )
                except PermissionError:
                    logger.error(f"Permission denied reading reference image: {img_path}")
                    raise GenerationError(f"Permission denied reading reference image: {img_path}")
                except Exception as e:
                    logger.error(f"Failed to load reference image {img_path}: {e}")
                    logger.debug("Reference image load error details:", exc_info=True)
                    raise GenerationError(f"Failed to load reference image {img_path}: {e}")

        # Add text prompt
        logger.debug("Adding text prompt to request")
        contents.append(types.Part(text=prompt))

        # Configure generation with aspect ratio and resolution
        # Determine effective resolution to use
        effective_resolution = None
        if resolution and model in MODELS_WITH_RESOLUTION_SUPPORT:
            effective_resolution = resolution
            logger.debug(
                f"Configuring generation: aspect_ratio={aspect_ratio}, resolution={resolution}"
            )
        else:
            if resolution and model not in MODELS_WITH_RESOLUTION_SUPPORT:
                logger.warning(
                    f"Resolution '{resolution}' ignored for model '{model}' "
                    f"(only Pro model supports variable resolution)"
                )
            logger.debug(
                f"Configuring generation: aspect_ratio={aspect_ratio}, resolution=default (~1024p)"
            )

        # Build image config
        image_config_params: dict[str, Any] = {"aspect_ratio": aspect_ratio}
        if effective_resolution:
            # Pro model: add image_size parameter
            image_config_params["image_size"] = effective_resolution
            logger.debug(f"Using image_size={effective_resolution} for Pro model")

        config = types.GenerateContentConfig(
            response_modalities=["IMAGE"],
            image_config=types.ImageConfig(**image_config_params),
        )

        # Generate content
        logger.info(f"Calling Gemini API: model={model}")
        logger.debug(f"Request config: {config}")
        response = client.models.generate_content(
            model=model,
            contents=contents,  # type: ignore[arg-type]
            config=config,
        )
        logger.debug("API call completed")

        # Extract image from response
        if not response.candidates:
            logger.error("No candidates returned from API")
            raise GenerationError("No candidates returned from API. Request may have been blocked.")

        candidate = response.candidates[0]
        logger.debug(f"Response has {len(response.candidates)} candidate(s)")

        # Check for content filtering
        if not candidate.content or not candidate.content.parts:
            finish_reason = getattr(candidate, "finish_reason", "UNKNOWN")
            logger.error(f"No content generated, finish_reason={finish_reason}")
            raise GenerationError(
                f"No content generated. Finish reason: {finish_reason}. "
                f"The prompt may have been blocked by safety filters."
            )

        # Find the image part
        logger.debug(f"Extracting image from {len(candidate.content.parts)} part(s)")
        image_part = None
        for part in candidate.content.parts:
            if hasattr(part, "inline_data") and part.inline_data:
                image_part = part
                break

        if not image_part:
            logger.error("No image data found in response")
            raise GenerationError(
                "No image data found in response. The model may have returned text only."
            )

        # Decode and save image
        try:
            logger.debug("Decoding and saving image...")
            # Handle both bytes and base64-encoded string
            if image_part.inline_data and image_part.inline_data.data:
                image_bytes = (
                    base64.b64decode(image_part.inline_data.data)
                    if isinstance(image_part.inline_data.data, str)
                    else image_part.inline_data.data
                )
                logger.debug(f"Image size: {len(image_bytes)} bytes")
                save_image(image_bytes, output_path)
                logger.info(f"Image saved successfully to: {output_path}")
            else:
                logger.error("No image data available in response")
                raise GenerationError("No image data available in response")
        except Exception as e:
            logger.error(f"Failed to save generated image: {e}")
            logger.debug("Image save error details:", exc_info=True)
            raise GenerationError(f"Failed to save generated image: {e}")

        # Extract token usage
        token_count = 0
        if hasattr(response, "usage_metadata") and response.usage_metadata:
            token_count = getattr(response.usage_metadata, "total_token_count", 0)
        logger.debug(f"Token usage: {token_count}")

        # Calculate cost based on token usage
        cost_per_token = COST_PER_TOKEN.get(model, 0.0)
        estimated_cost = token_count * cost_per_token if token_count > 0 else 0.0
        logger.debug(
            f"Cost calculation: {token_count} tokens × ${cost_per_token} = ${estimated_cost:.4f}"
        )

        # Format resolution
        width, height = ASPECT_RATIO_RESOLUTIONS.get(aspect_ratio, (0, 0))
        resolution_str = f"{width}x{height}"
        logger.debug(f"Image resolution: {resolution_str}")

        # Build result
        result = {
            "output_path": output_path,
            "model": model,
            "aspect_ratio": aspect_ratio,
            "resolution": resolution_str,
            "resolution_quality": effective_resolution or DEFAULT_RESOLUTION,
            "reference_image_count": len(reference_images) if reference_images else 0,
            "token_count": token_count,
            "estimated_cost_usd": round(estimated_cost, 4),
            "metadata": {
                "finish_reason": getattr(candidate, "finish_reason", "UNKNOWN"),
                "safety_ratings": getattr(candidate, "safety_ratings", None),
            },
        }
        logger.debug(f"Generation completed successfully: {result}")
        return result

    except GenerationError:
        raise
    except Exception as e:
        logger.error(f"Image generation failed: {type(e).__name__}: {e}")
        logger.debug("Generation error details:", exc_info=True)
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
