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

    Generate, edit, and manipulate images using Google's Gemini image generation models:
    • Nano Banana (gemini-2.5-flash-image) - Fast, high-quality generation
    • Nano Banana 2 (gemini-3-pro-image-preview) - Advanced pro model with higher quality

    Create high-quality images from text prompts, edit existing images with natural
    language, and compose multiple images together.

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

      # Generate image from text (both commands are equivalent)
      gemini-nano-banana-tool generate -o cat.png --prompt "A cat wearing a wizard hat"
      gemini-nano-banana-tool generate-image -o cat.png --prompt "A cat wearing a wizard hat"

      # Edit image with reference
      gemini-nano-banana-tool generate -o edited.png -i photo.jpg --prompt "Add a hat"

      # List available options
      gemini-nano-banana-tool list-models
      gemini-nano-banana-tool list-aspect-ratios

    \b
    For detailed command help:
      gemini-nano-banana-tool promptgen --help
      gemini-nano-banana-tool generate --help
      gemini-nano-banana-tool generate-image --help
      gemini-nano-banana-tool list-models --help
      gemini-nano-banana-tool list-aspect-ratios --help
    """
    # Initialize context object for passing data between commands
    ctx.ensure_object(dict)


@main.command()
@click.argument("shell", type=click.Choice(["bash", "zsh", "fish"]))
def completion(shell: str) -> None:
    """Generate shell completion script.

    SHELL: The shell type (bash, zsh, fish)

    Install instructions:

    \b
    # Bash (add to ~/.bashrc):
    eval "$(gemini-nano-banana-tool completion bash)"

    \b
    # Zsh (add to ~/.zshrc):
    eval "$(gemini-nano-banana-tool completion zsh)"

    \b
    # Fish (save to ~/.config/fish/completions/gemini-nano-banana-tool.fish):
    gemini-nano-banana-tool completion fish > \\
        ~/.config/fish/completions/gemini-nano-banana-tool.fish
    """
    # Import shell-specific completion classes
    from click.shell_completion import BashComplete, FishComplete, ZshComplete

    # Map shell names to completion classes
    completion_classes = {
        "bash": BashComplete,
        "zsh": ZshComplete,
        "fish": FishComplete,
    }

    completion_class = completion_classes.get(shell)
    if completion_class:
        completer = completion_class(
            cli=main,
            ctx_args={},
            prog_name="gemini-nano-banana-tool",
            complete_var="_GEMINI_NANO_BANANA_TOOL_COMPLETE",
        )
        click.echo(completer.source())
    else:
        raise click.BadParameter(f"Unsupported shell: {shell}")


# Register commands
main.add_command(promptgen)
main.add_command(generate)
main.add_command(generate, name="generate-image")  # Alias for generate
main.add_command(generate_conversation)
main.add_command(list_models)
main.add_command(list_aspect_ratios)


if __name__ == "__main__":
    main()
