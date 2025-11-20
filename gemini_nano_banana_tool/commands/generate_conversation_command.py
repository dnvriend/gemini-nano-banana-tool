"""Generate conversation command for multi-turn image generation.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import json
import sys
from pathlib import Path

import click

from gemini_nano_banana_tool.core.client import AuthenticationError, create_client
from gemini_nano_banana_tool.core.conversation import Conversation, ConversationTurn
from gemini_nano_banana_tool.core.generator import GenerationError, generate_image
from gemini_nano_banana_tool.core.models import DEFAULT_MODEL
from gemini_nano_banana_tool.logging_config import get_logger, setup_logging
from gemini_nano_banana_tool.utils import (
    ValidationError,
    validate_aspect_ratio,
    validate_model,
)

logger = get_logger(__name__)


@click.command(name="generate-conversation")
@click.argument("prompt")
@click.option(
    "-o",
    "--output",
    required=True,
    type=click.Path(),
    help="Output image file path (required)",
)
@click.option(
    "-f",
    "--file",
    "conversation_file",
    type=click.Path(),
    help="Conversation file to continue (creates new if doesn't exist)",
)
@click.option(
    "-a",
    "--aspect-ratio",
    default="1:1",
    help="Aspect ratio (default: 1:1). Only used for new conversations.",
)
@click.option(
    "-m",
    "--model",
    default=DEFAULT_MODEL,
    help=f"Gemini model (default: {DEFAULT_MODEL}). Only used for new conversations.",
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
    help="Google Cloud location (for Vertex AI)",
)
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Multi-level verbosity (-v INFO, -vv DEBUG, -vvv TRACE)",
)
def generate_conversation(
    prompt: str,
    output: str,
    conversation_file: str | None,
    aspect_ratio: str,
    model: str,
    api_key: str | None,
    use_vertex: bool,
    project: str | None,
    location: str | None,
    verbose: int,
) -> None:
    """Generate images with multi-turn conversation refinement.

    This command enables progressive image refinement through conversational editing.
    Each turn builds on previous context, allowing iterative improvements.

    The conversation state is saved to a file and can be continued in future sessions.

    \b
    Examples:
      # Start new conversation
      gemini-nano-banana-tool generate-conversation "A sunset over mountains" \\
        -o sunset1.png --file conversation.json

      # Continue conversation with refinements
      gemini-nano-banana-tool generate-conversation "Make the sky more orange" \\
        -o sunset2.png --file conversation.json

      # Further refinement
      gemini-nano-banana-tool generate-conversation "Add a lake in the foreground" \\
        -o sunset3.png --file conversation.json

    \b
    Conversation File:
      - JSON file storing conversation history
      - Contains all prompts and generated images
      - Can be resumed at any time
      - Auto-created if doesn't exist

    \b
    Multi-turn Benefits:
      - Progressive refinement without starting over
      - Context-aware edits based on conversation history
      - Experiment with variations while maintaining consistency
      - Track evolution of your image generation process
    """
    # Setup logging
    setup_logging(verbose)
    logger.info("Starting multi-turn conversation generation")

    try:
        # Load or create conversation
        if conversation_file and Path(conversation_file).exists():
            logger.info(f"Loading existing conversation: {conversation_file}")
            try:
                conversation = Conversation.load(conversation_file)
                logger.info(f"Loaded conversation with {len(conversation.turns)} previous turn(s)")
                # Use conversation's model and aspect ratio
                model = conversation.model
                aspect_ratio = conversation.aspect_ratio
                logger.debug(
                    f"Using conversation settings: model={model}, aspect_ratio={aspect_ratio}"
                )
            except (FileNotFoundError, ValueError) as e:
                logger.error(f"Failed to load conversation: {e}")
                sys.exit(1)
        else:
            # Create new conversation
            if conversation_file:
                logger.info(f"Creating new conversation: {conversation_file}")
            else:
                logger.warning("No conversation file specified - conversation won't be saved")

            # Validate new conversation settings
            try:
                validate_aspect_ratio(aspect_ratio)
                validate_model(model)
            except ValidationError as e:
                logger.error(f"Validation failed: {e}")
                sys.exit(1)

            conversation = Conversation(
                model=model,
                aspect_ratio=aspect_ratio,
            )
            logger.debug(f"Created new conversation: {conversation.conversation_id}")

        # Log prompt info
        logger.info(f"Turn {len(conversation.turns) + 1}: {prompt[:50]}...")
        logger.debug(f"Full prompt: {prompt}")

        # Build reference images from conversation history
        reference_images: list[str] = []
        if conversation.turns:
            # Use last generated image as reference
            last_turn = conversation.turns[-1]
            if last_turn.output_path and Path(last_turn.output_path).exists():
                reference_images.append(last_turn.output_path)
                logger.debug(f"Using previous output as reference: {last_turn.output_path}")

        # Create client
        try:
            auth_method = "Vertex AI" if use_vertex else "Gemini Developer API"
            logger.info(f"Authenticating with {auth_method}...")
            client = create_client(
                api_key=api_key,
                use_vertex=use_vertex,
                project=project,
                location=location,
            )
            logger.debug("Client created successfully")
        except AuthenticationError as e:
            logger.error(f"Authentication failed: {e}")
            sys.exit(1)

        # Generate image
        try:
            logger.info(f"Generating image with model: {model}")
            result = generate_image(
                client=client,
                prompt=prompt,
                output_path=output,
                reference_images=reference_images if reference_images else None,
                aspect_ratio=aspect_ratio,
                model=model,
            )

            # Add turn to conversation
            turn = ConversationTurn(
                prompt=prompt,
                output_path=output,
                reference_images=reference_images,
                metadata={
                    "token_count": result.get("token_count", 0),
                    "resolution": result.get("resolution"),
                    "finish_reason": result.get("metadata", {}).get("finish_reason"),
                },
            )
            conversation.add_turn(turn)

            # Save conversation if file specified
            if conversation_file:
                try:
                    conversation.save(conversation_file)
                    logger.info(f"Conversation saved to: {conversation_file}")
                except Exception as e:
                    logger.error(f"Failed to save conversation: {e}")
                    logger.debug("Save error details:", exc_info=True)

            # Output result as JSON
            output_data = {
                **result,
                "conversation_id": conversation.conversation_id,
                "turn_number": len(conversation.turns),
                "conversation_file": conversation_file,
            }
            click.echo(json.dumps(output_data, indent=2))

            logger.info(f"Turn {len(conversation.turns)} completed successfully")
            logger.info(f"Image saved to: {output}")

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
