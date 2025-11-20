"""Promptgen command for generating detailed prompts from simple descriptions.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import json
import sys

import click

from gemini_nano_banana_tool.core.client import AuthenticationError, create_client
from gemini_nano_banana_tool.core.prompt_templates import TEMPLATE_DESCRIPTIONS
from gemini_nano_banana_tool.core.promptgen import (
    PromptGenerationError,
    format_verbose_output,
    generate_prompt,
)


@click.command()
@click.argument("description", required=False, type=str)
@click.option(
    "-d",
    "--description",
    "description_opt",
    type=str,
    help="Simple description of desired image (alternative to positional arg)",
)
@click.option(
    "-t",
    "--template",
    type=click.Choice(
        ["photography", "character", "scene", "food", "abstract", "logo"],
        case_sensitive=False,
    ),
    help="Use prompt template for specific category",
)
@click.option(
    "-c",
    "--category",
    type=str,
    help="Category hint (overrides template detection)",
)
@click.option(
    "-s",
    "--style",
    type=str,
    help="Style hint (e.g., photorealistic, watercolor, anime, digital-art)",
)
@click.option(
    "--stdin",
    is_flag=True,
    help="Read description from stdin",
)
@click.option(
    "-o",
    "--output",
    type=click.Path(),
    help="Save prompt to file (default: stdout)",
)
@click.option(
    "--json",
    "output_json",
    is_flag=True,
    help="Output as JSON with metadata",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Verbose output with analysis breakdown",
)
@click.option(
    "--list-templates",
    is_flag=True,
    help="List available templates and exit",
)
@click.option(
    "-m",
    "--model",
    default="gemini-3-pro",
    help="LLM model for generation (default: gemini-3-pro)",
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
def promptgen(
    description: str | None,
    description_opt: str | None,
    template: str | None,
    category: str | None,
    style: str | None,
    stdin: bool,
    output: str | None,
    output_json: bool,
    verbose: bool,
    list_templates: bool,
    model: str,
    api_key: str | None,
    use_vertex: bool,
    project: str | None,
    location: str | None,
) -> None:
    """Generate detailed image prompts from simple descriptions.

    Transform basic descriptions into detailed, effective prompts using
    Gemini 3 Pro for enhanced prompt engineering.

    \b
    Examples:

    \b
      # Basic usage
      gemini-nano-banana-tool promptgen "wizard cat"

    \b
      # With template
      gemini-nano-banana-tool promptgen "wizard cat" --template character

    \b
      # With style hint
      gemini-nano-banana-tool promptgen "sunset" --style watercolor

    \b
      # Pipe to generate command
      gemini-nano-banana-tool promptgen "cyberpunk city" --template scene | \\
        gemini-nano-banana-tool generate -o city.png --stdin -a 16:9

    \b
      # JSON output for automation
      gemini-nano-banana-tool promptgen "food dish" --template food --json

    \b
      # Verbose output (educational)
      gemini-nano-banana-tool promptgen "abstract shapes" --verbose

    \b
      # Save to file for reuse
      gemini-nano-banana-tool promptgen "fantasy castle" -o castle-prompt.txt

    \b
      # From stdin
      echo "magical forest" | gemini-nano-banana-tool promptgen --stdin

    \b
    Output Format:
      Default: Plain text prompt to stdout (pipeable)
      --json: JSON with metadata (prompt, category, tokens, cost, etc.)
      --verbose: Human-readable analysis with prompt breakdown and cost

    \b
    Available Templates:
      photography - Professional photography with technical details
      character   - Character design with pose and attire
      scene       - Scene composition with layers
      food        - Food photography with plating
      abstract    - Abstract art with shapes and colors
      logo        - Logo design with typography

    Use --list-templates to see all templates with descriptions.
    """
    try:
        # Handle --list-templates
        if list_templates:
            click.echo("Available Prompt Templates:\n")
            for name, description_text in TEMPLATE_DESCRIPTIONS.items():
                click.echo(f"  {name:12} - {description_text}")
            return

        # Get description from argument, option, or stdin
        desc: str
        desc_input = description or description_opt
        if stdin:
            if desc_input:
                click.echo(
                    "Error: Cannot use both --stdin and description argument",
                    err=True,
                )
                sys.exit(1)
            desc = sys.stdin.read().strip()
        elif desc_input:
            desc = desc_input
        else:
            click.echo(
                "Error: No description provided. "
                "Use description argument, --description, or --stdin",
                err=True,
            )
            sys.exit(1)

        # Validate description
        if not desc or len(desc.strip()) == 0:
            click.echo("Error: Description cannot be empty", err=True)
            sys.exit(1)

        # Create client
        client = create_client(
            api_key=api_key,
            use_vertex=use_vertex,
            project=project,
            location=location,
        )

        # Generate prompt
        result = generate_prompt(
            client=client,
            description=desc,
            template=template,
            category=category,
            style=style,
            model=model,
        )

        # Format output based on flags
        if output_json:
            output_text = json.dumps(result, indent=2)
        elif verbose:
            output_text = format_verbose_output(result)
        else:
            # Plain text (default)
            output_text = result["prompt"]

        # Write to file or stdout
        if output:
            with open(output, "w", encoding="utf-8") as f:
                f.write(output_text)
                if not output_text.endswith("\n"):
                    f.write("\n")
            click.echo(f"Prompt saved to: {output}", err=True)
        else:
            click.echo(output_text)

    except AuthenticationError as e:
        click.echo(f"Authentication Error: {e}", err=True)
        click.echo(
            "Set GEMINI_API_KEY environment variable or use --api-key option",
            err=True,
        )
        sys.exit(1)
    except PromptGenerationError as e:
        click.echo(f"Generation Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected Error: {e}", err=True)
        sys.exit(1)
