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
from gemini_nano_banana_tool.logging_config import get_logger, setup_logging

logger = get_logger(__name__)


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
    "--show-analysis",
    is_flag=True,
    help="Show detailed analysis with prompt breakdown (alternative to --json)",
)
@click.option(
    "--list-templates",
    is_flag=True,
    help="List available templates and exit",
)
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Enable verbose logging (use -v for INFO, -vv for DEBUG, -vvv for TRACE)",
)
@click.option(
    "-m",
    "--model",
    default="gemini-2.5-flash",
    help="LLM model for generation (default: gemini-2.5-flash)",
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
    show_analysis: bool,
    list_templates: bool,
    verbose: int,
    model: str,
    api_key: str | None,
    use_vertex: bool,
    project: str | None,
    location: str | None,
) -> None:
    """Generate detailed image prompts from simple descriptions.

    Transform basic descriptions into detailed, effective prompts using
    Gemini 2.5 Flash for enhanced prompt engineering.

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
      # Show detailed analysis
      gemini-nano-banana-tool promptgen "abstract shapes" --show-analysis

    \b
      # Save to file for reuse
      gemini-nano-banana-tool promptgen "fantasy castle" -o castle-prompt.txt

    \b
      # From stdin
      echo "magical forest" | gemini-nano-banana-tool promptgen --stdin

    \b
      # Enable debug logging
      gemini-nano-banana-tool promptgen "sunset" -vv

    \b
    Output Format:
      Default: Plain text prompt to stdout (pipeable)
      --json: JSON with metadata (prompt, category, tokens, cost, etc.)
      --show-analysis: Human-readable analysis with prompt breakdown and cost
      -v/-vv/-vvv: Control logging verbosity (INFO/DEBUG/TRACE)

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
    # Setup logging based on verbosity
    setup_logging(verbose)
    logger.info("Starting prompt generation command")

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
                logger.error("Cannot use both --stdin and description argument")
                click.echo(
                    "Error: Cannot use both --stdin and description argument",
                    err=True,
                )
                sys.exit(1)
            logger.debug("Reading description from stdin")
            desc = sys.stdin.read().strip()
        elif desc_input:
            desc = desc_input
            logger.debug(f"Description length: {len(desc)} characters")
        else:
            logger.error("No description provided")
            click.echo(
                "Error: No description provided. "
                "Use description argument, --description, or --stdin",
                err=True,
            )
            sys.exit(1)

        # Validate description
        if not desc or len(desc.strip()) == 0:
            logger.error("Description is empty")
            click.echo("Error: Description cannot be empty", err=True)
            sys.exit(1)

        logger.info(f"Description: {desc[:50]}{'...' if len(desc) > 50 else ''}")

        # Create client
        logger.debug(f"Creating client (use_vertex={use_vertex})")
        client = create_client(
            api_key=api_key,
            use_vertex=use_vertex,
            project=project,
            location=location,
        )
        logger.info("Client created successfully")

        # Log generation parameters
        logger.info(f"Model: {model}")
        if template:
            logger.info(f"Template: {template}")
        if category:
            logger.debug(f"Category: {category}")
        if style:
            logger.debug(f"Style: {style}")

        # Generate prompt
        logger.info("Generating detailed prompt...")
        result = generate_prompt(
            client=client,
            description=desc,
            template=template,
            category=category,
            style=style,
            model=model,
        )
        logger.info(f"Prompt generated successfully (tokens: {result['tokens_used']})")
        logger.debug(f"Estimated cost: ${result['estimated_cost_usd']:.4f}")

        # Format output based on flags
        if output_json:
            logger.debug("Formatting output as JSON")
            output_text = json.dumps(result, indent=2)
        elif show_analysis:
            logger.debug("Formatting output as verbose analysis")
            output_text = format_verbose_output(result)
        else:
            logger.debug("Formatting output as plain text")
            # Plain text (default)
            output_text = result["prompt"]

        # Write to file or stdout
        if output:
            logger.debug(f"Writing output to file: {output}")
            with open(output, "w", encoding="utf-8") as f:
                f.write(output_text)
                if not output_text.endswith("\n"):
                    f.write("\n")
            logger.info(f"Prompt saved to: {output}")
            click.echo(f"Prompt saved to: {output}", err=True)
        else:
            logger.debug("Writing output to stdout")
            click.echo(output_text)

        logger.info("Prompt generation completed successfully")

    except AuthenticationError as e:
        logger.error(f"Authentication error: {e}")
        click.echo(f"Authentication Error: {e}", err=True)
        click.echo(
            "Set GEMINI_API_KEY environment variable or use --api-key option",
            err=True,
        )
        sys.exit(1)
    except PromptGenerationError as e:
        logger.error(f"Generation error: {e}", exc_info=verbose >= 2)
        click.echo(f"Generation Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        click.echo(f"Unexpected Error: {e}", err=True)
        sys.exit(1)
