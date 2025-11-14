"""List commands for discovering models and aspect ratios.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import click

from gemini_nano_banana_tool.core.models import (
    ASPECT_RATIO_DESCRIPTIONS,
    ASPECT_RATIO_RESOLUTIONS,
    DEFAULT_MODEL,
    MODEL_DESCRIPTIONS,
    SUPPORTED_MODELS,
)


@click.command(name="list-models")
def list_models() -> None:
    """List available Gemini models for image generation.

    Displays all supported Gemini models with descriptions.

    Example:
        $ gemini-nano-banana-tool list-models
    """
    click.echo("Available Gemini Image Generation Models:")
    for model in SUPPORTED_MODELS:
        description = MODEL_DESCRIPTIONS.get(model, "")
        is_default = " (default)" if model == DEFAULT_MODEL else ""
        click.echo(f"  • {model}{is_default} - {description}")


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
