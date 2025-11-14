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
from gemini_nano_banana_tool.utils import (
    ValidationError,
    format_resolution,
    load_prompt,
    validate_aspect_ratio,
    validate_model,
    validate_reference_images,
)


@click.command()
@click.option(
    "-o",
    "--output",
    required=True,
    type=click.Path(),
    help="Output image file path (required)",
)
@click.option(
    "-p",
    "--prompt",
    type=str,
    help="Prompt text (mutually exclusive with --prompt-file and --stdin)",
)
@click.option(
    "-f",
    "--prompt-file",
    type=click.Path(exists=True),
    help="Read prompt from file (mutually exclusive with --prompt and --stdin)",
)
@click.option(
    "-s",
    "--stdin",
    is_flag=True,
    help="Read prompt from stdin (mutually exclusive with --prompt and --prompt-file)",
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
    is_flag=True,
    help="Enable verbose output",
)
def generate(
    output: str,
    prompt: str | None,
    prompt_file: str | None,
    stdin: bool,
    images: tuple[str, ...],
    aspect_ratio: str,
    model: str,
    api_key: str | None,
    use_vertex: bool,
    project: str | None,
    location: str | None,
    verbose: bool,
) -> None:
    """Generate images from text prompts with optional reference images.

    This command creates high-quality images using Google's Gemini AI models.
    You can provide text prompts directly, from a file, or via stdin.
    Optionally include up to 3 reference images for image editing and composition.

    \b
    Examples:
      # Basic text-to-image
      gemini-nano-banana-tool generate -o cat.png --prompt "A cat wearing a wizard hat"

      # With aspect ratio
      gemini-nano-banana-tool generate -o wide.png -a 16:9 --prompt "Panoramic landscape"

      # From file
      gemini-nano-banana-tool generate -o output.png --prompt-file prompt.txt

      # From stdin
      echo "A sunset" | gemini-nano-banana-tool generate -o sunset.png --stdin

      # With reference image
      gemini-nano-banana-tool generate -o edited.png -i photo.jpg \\
        --prompt "Add a birthday hat"

      # Multiple reference images
      gemini-nano-banana-tool generate -o result.png \\
        -i image1.jpg -i image2.jpg \\
        --prompt "Combine these images"

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
    try:
        # Verbose output
        if verbose:
            click.echo(f"Output file: {output}", err=True)
            click.echo(f"Aspect ratio: {aspect_ratio}", err=True)
            click.echo(f"Model: {model}", err=True)
            if images:
                click.echo(f"Reference images: {len(images)}", err=True)

        # Load and validate prompt
        try:
            prompt_text = load_prompt(prompt, prompt_file, stdin)
            if verbose:
                click.echo(f"Prompt loaded ({len(prompt_text)} characters)", err=True)
        except ValidationError as e:
            click.echo(f"Error: {e}", err=True)
            sys.exit(1)

        # Validate inputs
        try:
            if images:
                validate_reference_images(list(images))
            validate_aspect_ratio(aspect_ratio)
            validate_model(model)
        except ValidationError as e:
            click.echo(f"Error: {e}", err=True)
            sys.exit(1)

        # Create client
        try:
            if verbose:
                auth_method = "Vertex AI" if use_vertex else "Gemini Developer API"
                click.echo(f"Authenticating with {auth_method}...", err=True)

            client = create_client(
                api_key=api_key,
                use_vertex=use_vertex,
                project=project,
                location=location,
            )
        except AuthenticationError as e:
            click.echo(f"Authentication Error: {e}", err=True)
            sys.exit(1)

        # Generate image
        try:
            if verbose:
                click.echo("Generating image...", err=True)

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

            if verbose:
                resolution = format_resolution(aspect_ratio)
                click.echo(f"\nSuccess! Image saved to: {output}", err=True)
                click.echo(f"Resolution: {resolution}", err=True)
                click.echo(f"Tokens used: {result.get('token_count', 0)}", err=True)

        except GenerationError as e:
            click.echo(f"Generation Error: {e}", err=True)
            sys.exit(1)

    except KeyboardInterrupt:
        click.echo("\nOperation interrupted by user.", err=True)
        sys.exit(130)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        if verbose:
            import traceback

            click.echo(traceback.format_exc(), err=True)
        sys.exit(1)
