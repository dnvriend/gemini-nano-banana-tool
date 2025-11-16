"""Gemini client management for image generation operations.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import logging
import os

from google import genai

logger = logging.getLogger(__name__)


class GeminiClientError(Exception):
    """Base exception for Gemini client errors."""

    pass


class AuthenticationError(GeminiClientError):
    """Raised when authentication fails."""

    pass


def create_client(
    api_key: str | None = None,
    use_vertex: bool = False,
    project: str | None = None,
    location: str | None = None,
) -> genai.Client:
    """Create and configure a Gemini client for image generation operations.

    Supports both Gemini Developer API and Vertex AI authentication.

    Args:
        api_key: API key for Gemini Developer API (optional, reads from env)
        use_vertex: Whether to use Vertex AI instead of Developer API
        project: Google Cloud project ID (required for Vertex AI)
        location: Google Cloud location (required for Vertex AI)

    Returns:
        Configured Gemini client

    Raises:
        AuthenticationError: If authentication configuration is invalid

    Example:
        >>> # Gemini Developer API
        >>> client = create_client()  # Uses GEMINI_API_KEY from environment
        >>> client = create_client(api_key="your-api-key")
        >>>
        >>> # Vertex AI
        >>> client = create_client(
        ...     use_vertex=True,
        ...     project="my-project",
        ...     location="us-central1"
        ... )
    """
    # Vertex AI configuration
    # Check if Vertex AI is enabled via environment or parameter
    logger.debug("Checking authentication method...")
    use_vertex_env = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "").lower() in (
        "true",
        "1",
        "yes",
    )
    if use_vertex or use_vertex_env:
        logger.debug("Using Vertex AI authentication")
        # Read from parameters or environment
        if not project:
            project = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not location:
            location = os.getenv("GOOGLE_CLOUD_LOCATION")

        logger.debug(f"Vertex AI config: project={project}, location={location}")

        if not project:
            logger.error("GOOGLE_CLOUD_PROJECT not set for Vertex AI")
            raise AuthenticationError(
                "GOOGLE_CLOUD_PROJECT environment variable or --project is required for Vertex AI. "
                "Set it with: export GOOGLE_CLOUD_PROJECT='your-project-id'"
            )
        if not location:
            logger.error("GOOGLE_CLOUD_LOCATION not set for Vertex AI")
            raise AuthenticationError(
                "GOOGLE_CLOUD_LOCATION environment variable or --location is required "
                "for Vertex AI. Set it with: export GOOGLE_CLOUD_LOCATION='us-central1'"
            )
        try:
            logger.info(f"Creating Vertex AI client for project={project}, location={location}")
            client = genai.Client(vertexai=True, project=project, location=location)
            logger.debug("Vertex AI client created successfully")
            return client
        except Exception as e:
            logger.error(f"Failed to create Vertex AI client: {e}")
            logger.debug("Vertex AI client creation error details:", exc_info=True)
            raise AuthenticationError(
                f"Failed to create Vertex AI client: {e}. "
                "Ensure you've authenticated with 'gcloud auth application-default login'"
            ) from e

    # Gemini Developer API configuration
    # Priority: 1. Explicit api_key param, 2. GOOGLE_API_KEY, 3. GEMINI_API_KEY
    logger.debug("Using Gemini Developer API authentication")
    if not api_key:
        api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        logger.debug(f"API key from environment: {'set' if api_key else 'not set'}")

    if not api_key:
        logger.error("API key not found in environment or parameters")
        raise AuthenticationError(
            "API key is required. Set GEMINI_API_KEY or GOOGLE_API_KEY environment variable, "
            "or use --api-key option. "
            "Get your API key from https://aistudio.google.com/app/apikey"
        )

    try:
        logger.info("Creating Gemini Developer API client")
        logger.debug(f"API key length: {len(api_key)} characters")
        client = genai.Client(api_key=api_key)
        logger.debug("Gemini client created successfully")
        return client
    except Exception as e:
        logger.error(f"Failed to create Gemini client: {e}")
        logger.debug("Gemini client creation error details:", exc_info=True)
        raise AuthenticationError(f"Failed to create Gemini client: {e}") from e


def validate_client(client: genai.Client) -> None:
    """Validate that the client is properly configured.

    Args:
        client: Gemini client to validate

    Raises:
        GeminiClientError: If client validation fails
    """
    if not isinstance(client, genai.Client):
        raise GeminiClientError(f"Invalid client type: {type(client)}")
