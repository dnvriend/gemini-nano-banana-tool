"""Generate command for image generation.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import json
import sys

import click

from gemini_nano_banana_tool.core.client import AuthenticationError, create_client
from gemini_nano_banana_tool.core.generator import GenerationError, generate_image
from gemini_nano_banana_tool.core.models import DEFAULT_MODEL
from gemini_nano_banana_tool.logging_config import get_logger, setup_logging
from gemini_nano_banana_tool.utils import (
    ValidationError,
    format_resolution,
    load_prompt,
    validate_aspect_ratio,
    validate_model,
    validate_reference_images,
)

logger = get_logger(__name__)


@click.command()
@click.argument("prompt", required=False)
@click.option(
    "-o",
    "--output",
    required=True,
    type=click.Path(),
    help="Output image file path (required)",
)
@click.option(
    "-f",
    "--prompt-file",
    type=click.Path(exists=True),
    help="Read prompt from file (mutually exclusive with prompt argument and --stdin)",
)
@click.option(
    "-s",
    "--stdin",
    is_flag=True,
    help="Read prompt from stdin (mutually exclusive with prompt argument and --prompt-file)",
)
@click.option(
    "-i",
    "--image",
    "images",
    multiple=True,
    type=click.Path(exists=True),
    help="Reference image (can be used up to 3 times)",
)
@click.option(
    "-a",
    "--aspect-ratio",
    default="1:1",
    help="Aspect ratio (default: 1:1). Use 'list-aspect-ratios' to see all options.",
)
@click.option(
    "-m",
    "--model",
    default=DEFAULT_MODEL,
    help=f"Gemini model (default: {DEFAULT_MODEL}). Use 'list-models' to see all options.",
)
@click.option(
    "--api-key",
    type=str,
    help="Override API key from environment",
)
@click.option(
    "--use-vertex",
    is_flag=True,
    help="Use Vertex AI instead of Developer API",
)
@click.option(
    "--project",
    type=str,
    help="Google Cloud project (for Vertex AI)",
)
@click.option(
    "--location",
    type=str,
    help="Google Cloud location (for Vertex AI, default: us-central1)",
)
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Enable verbose output (use -v for INFO, -vv for DEBUG, -vvv for TRACE)",
)
def generate(
    prompt: str | None,
    output: str,
    prompt_file: str | None,
    stdin: bool,
    images: tuple[str, ...],
    aspect_ratio: str,
    model: str,
    api_key: str | None,
    use_vertex: bool,
    project: str | None,
    location: str | None,
    verbose: int,
) -> None:
    """Generate images from text prompts with optional reference images.

    This command creates high-quality images using Google's Gemini AI models.
    You can provide text prompts as a positional argument, from a file, or via stdin.
    Optionally include up to 3 reference images for image editing and composition.

    \b
    Examples:
      # Basic text-to-image with positional argument
      gemini-nano-banana-tool generate "A cat wearing a wizard hat" -o cat.png

      # With aspect ratio
      gemini-nano-banana-tool generate "Panoramic landscape" -o wide.png -a 16:9

      # From file
      gemini-nano-banana-tool generate -o output.png --prompt-file prompt.txt

      # From stdin
      echo "A sunset" | gemini-nano-banana-tool generate -o sunset.png --stdin

      # With reference image
      gemini-nano-banana-tool generate "Add a birthday hat" -o edited.png -i photo.jpg

      # Multiple reference images
      gemini-nano-banana-tool generate "Combine these images" -o result.png \\
        -i image1.jpg -i image2.jpg

      # Verbose mode (INFO level)
      gemini-nano-banana-tool generate "test prompt" -o output.png -v

      # Debug mode (DEBUG level)
      gemini-nano-banana-tool generate "test prompt" -o output.png -vv

      # Trace mode (DEBUG + library internals)
      gemini-nano-banana-tool generate "test prompt" -o output.png -vvv

    \b
    Output Format:
      Returns JSON to stdout with structure:
      {
        "output_path": "image.png",
        "model": "gemini-2.5-flash-image",
        "aspect_ratio": "1:1",
        "resolution": "1024x1024",
        "reference_image_count": 0,
        "token_count": 1310,
        "metadata": {"finish_reason": "STOP", "safety_ratings": null}
      }

    \b
    Supported Aspect Ratios:
      1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3, 21:9, 4:5, 5:4
      Use 'list-aspect-ratios' command for details.

    \b
    Supported Models:
      gemini-2.5-flash-image (default), gemini-2.0-flash-exp,
      gemini-1.5-pro, gemini-1.5-flash
      Use 'list-models' command for details.

    \b
    Authentication:
      Set GEMINI_API_KEY or GOOGLE_API_KEY environment variable.
      Get your API key from: https://aistudio.google.com/app/apikey

      For Vertex AI, set GOOGLE_GENAI_USE_VERTEXAI=true,
      GOOGLE_CLOUD_PROJECT, and GOOGLE_CLOUD_LOCATION.
    """
    # Setup logging based on verbosity
    setup_logging(verbose)
    logger.info("Starting image generation command")

    try:
        # Log command configuration
        logger.info(f"Output file: {output}")
        logger.debug(f"Aspect ratio: {aspect_ratio}")
        logger.debug(f"Model: {model}")
        if images:
            logger.info(f"Reference images: {len(images)}")

        # Load and validate prompt
        try:
            prompt_text = load_prompt(prompt, prompt_file, stdin)
            logger.info(f"Prompt loaded ({len(prompt_text)} characters)")
            logger.debug(f"Prompt preview: {prompt_text[:100]}...")
        except ValidationError as e:
            logger.error(f"Prompt validation failed: {e}")
            sys.exit(1)

        # Validate inputs
        try:
            logger.debug("Validating inputs...")
            if images:
                validate_reference_images(list(images))
                logger.debug(f"Reference images validated: {list(images)}")
            validate_aspect_ratio(aspect_ratio)
            logger.debug(f"Aspect ratio validated: {aspect_ratio}")
            validate_model(model)
            logger.debug(f"Model validated: {model}")
        except ValidationError as e:
            logger.error(f"Validation failed: {e}")
            sys.exit(1)

        # Create client
        try:
            auth_method = "Vertex AI" if use_vertex else "Gemini Developer API"
            logger.info(f"Authenticating with {auth_method}...")
            logger.debug(
                f"Auth details: use_vertex={use_vertex}, project={project}, location={location}"
            )

            client = create_client(
                api_key=api_key,
                use_vertex=use_vertex,
                project=project,
                location=location,
            )
            logger.debug("Client created successfully")
        except AuthenticationError as e:
            logger.error(f"Authentication failed: {e}")
            logger.debug("Authentication error details:", exc_info=True)
            sys.exit(1)

        # Generate image
        try:
            logger.info("Starting image generation...")
            logger.debug(
                f"Generation parameters: prompt_length={len(prompt_text)}, "
                f"aspect_ratio={aspect_ratio}, model={model}, "
                f"reference_images={len(images) if images else 0}"
            )

            result = generate_image(
                client=client,
                prompt=prompt_text,
                output_path=output,
                reference_images=list(images) if images else None,
                aspect_ratio=aspect_ratio,
                model=model,
            )

            # Output JSON result to stdout
            click.echo(json.dumps(result, indent=2))

            # Log success details
            resolution = format_resolution(aspect_ratio)
            logger.info(f"Success! Image saved to: {output}")
            logger.info(f"Resolution: {resolution}")
            logger.info(f"Tokens used: {result.get('token_count', 0)}")
            logger.debug(f"Full result: {result}")

        except GenerationError as e:
            logger.error(f"Image generation failed: {e}")
            logger.debug("Generation error details:", exc_info=True)
            sys.exit(1)

    except KeyboardInterrupt:
        logger.warning("Operation interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Unexpected error: {type(e).__name__}: {e}")
        logger.debug("Full traceback:", exc_info=True)
        sys.exit(1)
