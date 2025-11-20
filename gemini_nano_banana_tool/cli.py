"""CLI entry point for gemini-nano-banana-tool.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import click

from gemini_nano_banana_tool.commands import (
    generate,
    generate_conversation,
    list_aspect_ratios,
    list_models,
    promptgen,
)


@click.group()
@click.version_option(version="2.0.0")
@click.pass_context
def main(ctx: click.Context) -> None:
    """Gemini Nano Banana Tool - Professional AI image generation CLI.

    Generate, edit, and manipulate images using Google's Gemini 2.5 Flash Image model
    (codename "Nano Banana"). Create high-quality images from text prompts, edit existing
    images with natural language, and compose multiple images together.

    \b
    Key Features:
      • AI-powered prompt generation from simple descriptions
      • Text-to-image generation with detailed prompts
      • Image editing with up to 3 reference images
      • Multiple aspect ratios (1:1, 16:9, 9:16, etc.)
      • Flexible prompt input (argument, file, or stdin)
      • Dual authentication (API key and Vertex AI)

    \b
    Authentication:
      Set GEMINI_API_KEY or GOOGLE_API_KEY environment variable.
      Get your API key from: https://aistudio.google.com/app/apikey

    \b
    For Vertex AI:
      Set GOOGLE_GENAI_USE_VERTEXAI=true
      Set GOOGLE_CLOUD_PROJECT='your-project-id'
      Set GOOGLE_CLOUD_LOCATION='us-central1'

    \b
    Examples:
      # Generate detailed prompt from simple description
      gemini-nano-banana-tool promptgen "wizard cat"

      # Generate prompt and create image in one pipeline
      gemini-nano-banana-tool promptgen "wizard cat" | \\
        gemini-nano-banana-tool generate -o cat.png --stdin

      # Generate image from text
      gemini-nano-banana-tool generate -o cat.png --prompt "A cat wearing a wizard hat"

      # Edit image with reference
      gemini-nano-banana-tool generate -o edited.png -i photo.jpg --prompt "Add a hat"

      # List available options
      gemini-nano-banana-tool list-models
      gemini-nano-banana-tool list-aspect-ratios

    \b
    For detailed command help:
      gemini-nano-banana-tool promptgen --help
      gemini-nano-banana-tool generate --help
      gemini-nano-banana-tool list-models --help
      gemini-nano-banana-tool list-aspect-ratios --help
    """
    # Initialize context object for passing data between commands
    ctx.ensure_object(dict)


# Register commands
main.add_command(promptgen)
main.add_command(generate)
main.add_command(generate_conversation)
main.add_command(list_models)
main.add_command(list_aspect_ratios)


if __name__ == "__main__":
    main()
