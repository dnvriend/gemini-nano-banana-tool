"""List commands for discovering models and aspect ratios.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import click

from gemini_nano_banana_tool.core.models import (
    ASPECT_RATIO_DESCRIPTIONS,
    ASPECT_RATIO_RESOLUTIONS,
    COST_PER_IMAGE,
    COST_PER_TOKEN,
    DEFAULT_MODEL,
    MODEL_DESCRIPTIONS,
    SUPPORTED_MODELS,
    is_imagen_model,
)


@click.command(name="list-models")
def list_models() -> None:
    """List available image generation models.

    Displays all supported Gemini and Imagen models with descriptions and pricing.

    Example:
        $ gemini-nano-banana-tool list-models
    """
    # Separate models by type
    gemini_models = [m for m in SUPPORTED_MODELS if not is_imagen_model(m)]
    imagen_models = [m for m in SUPPORTED_MODELS if is_imagen_model(m)]

    # Display Gemini models
    if gemini_models:
        click.echo("Gemini Image Generation Models:")
        for model in gemini_models:
            description = MODEL_DESCRIPTIONS.get(model, "")
            is_default = " (default)" if model == DEFAULT_MODEL else ""
            cost_per_token = COST_PER_TOKEN.get(model, 0.0)
            pricing = f"~${cost_per_token * 1_000_000:.0f}/1M tokens"
            click.echo(f"  • {model}{is_default}")
            click.echo(f"    {description}")
            click.echo(f"    Pricing: {pricing}")

    # Display Imagen models
    if imagen_models:
        click.echo("\nImagen 4 Models:")
        for model in imagen_models:
            description = MODEL_DESCRIPTIONS.get(model, "")
            cost_per_image = COST_PER_IMAGE.get(model, 0.0)
            pricing = f"${cost_per_image:.2f}/image"
            click.echo(f"  • {model}")
            click.echo(f"    {description}")
            click.echo(f"    Pricing: {pricing}")


@click.command(name="list-aspect-ratios")
def list_aspect_ratios() -> None:
    """List available aspect ratios for image generation.

    Displays all supported aspect ratios with resolutions and use cases.

    Example:
        $ gemini-nano-banana-tool list-aspect-ratios
    """
    click.echo("Available Aspect Ratios:")
    for ratio in ASPECT_RATIO_RESOLUTIONS:
        width, height = ASPECT_RATIO_RESOLUTIONS[ratio]
        description = ASPECT_RATIO_DESCRIPTIONS.get(ratio, "")
        click.echo(f"  {ratio:6} ({width}x{height:4}) - {description}")
