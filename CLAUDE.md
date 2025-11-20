# gemini-nano-banana-tool - Developer Guide

## Overview

A professional, CLI-first Python tool for Google Gemini image generation (Nano Banana). Built with modern Python tooling (uv, mise, click, Python 3.14+) and designed for both human use and AI agent automation.

**Tech Stack:**
- **Language**: Python 3.14+
- **CLI Framework**: Click
- **SDK**: google-genai
- **Package Manager**: uv
- **Environment Manager**: mise
- **Linting**: ruff
- **Type Checking**: mypy (strict mode)
- **Testing**: pytest

## Architecture

### Project Structure

```
gemini-nano-banana-tool/
├── gemini_nano_banana_tool/
│   ├── __init__.py              # Public API exports for library usage
│   ├── cli.py                   # CLI entry point, command registration
│   ├── core/                    # Core library (importable, CLI-independent)
│   │   ├── __init__.py          # Core API exports
│   │   ├── client.py            # Gemini client creation and authentication
│   │   ├── generator.py         # Image generation logic
│   │   └── models.py            # Data models, constants (AspectRatio, etc.)
│   ├── commands/                # CLI command implementations
│   │   ├── __init__.py
│   │   ├── generate_command.py  # generate command with Click decorators
│   │   └── list_commands.py     # list-models and list-aspect-ratios commands
│   └── utils.py                 # Shared utilities (validation, I/O, prompt loading)
├── tests/                       # Test suite
│   ├── __init__.py
│   ├── test_utils.py
│   ├── test_client.py
│   ├── test_generator.py
│   └── test_commands.py
├── references/                  # Documentation and guides
│   ├── api-setup-pricing.md    # API key setup and pricing info
│   ├── prompting-guide.md      # Prompt engineering best practices
│   └── examples.md             # Usage examples and patterns
├── pyproject.toml               # Project configuration
├── Makefile                     # Development commands
├── README.md                    # User documentation
├── CLAUDE.md                    # This file (developer guide)
├── LICENSE                      # MIT License
└── .mise.toml                   # mise configuration
```

### Key Design Principles

1. **Separation of Concerns**
   - `core/` contains business logic, independent of CLI
   - `commands/` contains CLI wrappers with Click decorators
   - Core functions are importable and reusable

2. **Exception-Based Errors**
   - Core functions raise exceptions (NOT `sys.exit`)
   - CLI boundary catches exceptions and formats errors
   - Enables proper error handling in library mode

3. **Composable Output**
   - JSON data to stdout for piping
   - Logs and errors to stderr
   - Enables shell composition and automation

4. **Type Safety**
   - Full type hints throughout
   - Passes `mypy --strict`
   - Modern Python syntax (`dict`/`list` over `Dict`/`List`)

5. **Agent-Friendly Design**
   - Rich error messages with solutions
   - Help text includes working examples
   - Structured output for parsing

## Core Modules

### core/client.py

Manages Gemini client creation with support for both Gemini Developer API and Vertex AI.

**Key Functions:**
```python
def create_client(
    api_key: str | None = None,
    use_vertex: bool = False,
    project: str | None = None,
    location: str | None = None,
) -> genai.Client:
    """Create Gemini client with API key or Vertex AI authentication."""

class AuthenticationError(Exception):
    """Raised when authentication fails."""
```

**Authentication Priority:**
1. Explicit `api_key` parameter
2. `GOOGLE_API_KEY` environment variable
3. `GEMINI_API_KEY` environment variable
4. Vertex AI (if `use_vertex=True` or `GOOGLE_GENAI_USE_VERTEXAI=true`)

### core/models.py

Data models and constants.

**Key Classes/Enums:**
```python
class AspectRatio(str, Enum):
    """Supported aspect ratios for image generation."""
    RATIO_1_1 = "1:1"     # 1024x1024
    RATIO_16_9 = "16:9"   # 1344x768
    RATIO_9_16 = "9:16"   # 768x1344
    # ... more ratios

ASPECT_RATIO_RESOLUTIONS: dict[str, tuple[int, int]] = {
    "1:1": (1024, 1024),
    "16:9": (1344, 768),
    # ... mappings
}

SUPPORTED_MODELS: list[str] = [
    "gemini-2.5-flash-image",  # default
    "gemini-3-pro-image-preview",
]

DEFAULT_MODEL = "gemini-2.5-flash-image"
```

### core/generator.py

Image generation logic.

**Key Functions:**
```python
def generate_image(
    client: genai.Client,
    prompt: str,
    output_path: str,
    reference_images: list[str] | None = None,
    aspect_ratio: str = "1:1",
    model: str = DEFAULT_MODEL,
) -> dict[str, Any]:
    """Generate image from prompt and optional reference images.

    Returns:
        dict with keys: output_path, model, aspect_ratio, resolution,
        reference_image_count, token_count, metadata

    Raises:
        GenerationError: If image generation fails
        FileNotFoundError: If reference images don't exist
    """

class GenerationError(Exception):
    """Raised when image generation fails."""
```

### utils.py

Shared utilities.

**Key Functions:**
```python
def load_prompt(
    prompt: str | None,
    prompt_file: str | None,
    use_stdin: bool,
) -> str:
    """Load prompt from argument, file, or stdin (mutually exclusive).

    Raises:
        ValueError: If multiple sources provided or none provided
    """

def validate_reference_images(image_paths: list[str]) -> None:
    """Validate reference images (max 3, all exist).

    Raises:
        ValueError: If more than 3 images or any don't exist
    """

def save_image(image_data: bytes, output_path: str) -> None:
    """Save image bytes to file.

    Raises:
        IOError: If save fails
    """
```

## CLI Commands

### generate

Main command for image generation.

**Signature:**
```python
@click.command()
@click.argument("prompt", required=False)
@click.option("-o", "--output", required=True, type=click.Path(),
              help="Output image file path")
@click.option("-f", "--prompt-file", type=click.Path(exists=True),
              help="Read prompt from file")
@click.option("-s", "--stdin", is_flag=True,
              help="Read prompt from stdin")
@click.option("-i", "--image", "images", multiple=True, type=click.Path(exists=True),
              help="Reference image (can be used up to 3 times)")
@click.option("-a", "--aspect-ratio", default="1:1",
              help="Aspect ratio (default: 1:1)")
@click.option("-m", "--model", default=DEFAULT_MODEL,
              help=f"Gemini model (default: {DEFAULT_MODEL})")
@click.option("--api-key", type=str,
              help="Override API key from environment")
@click.option("--use-vertex", is_flag=True,
              help="Use Vertex AI instead of Developer API")
@click.option("--project", type=str,
              help="Google Cloud project (for Vertex AI)")
@click.option("--location", type=str,
              help="Google Cloud location (for Vertex AI)")
@click.option("-v", "--verbose", count=True,
              help="Multi-level verbosity (-v INFO, -vv DEBUG, -vvv TRACE)")
def generate(...) -> None:
    """Generate images from text prompts with optional reference images."""
```

**Validation:**
- Exactly one of `PROMPT` (positional), `--prompt-file`, or `--stdin` must be provided
- Maximum 3 reference images
- Aspect ratio must be valid
- Model must be in supported list

**Verbosity Levels:**
- `0` (no flag): WARNING only - minimal output
- `-v` (1): INFO - high-level operations, authentication, generation status
- `-vv` (2): DEBUG - detailed validation, API call details, file operations
- `-vvv` (3+): TRACE - DEBUG + dependent library logging (HTTP requests, etc.)

**Error Handling:**
Uses structured logging at appropriate levels:
```python
logger.info("Starting image generation...")
logger.debug(f"Generation parameters: prompt_length={len(prompt_text)}, aspect_ratio={aspect_ratio}")
logger.error(f"Image generation failed: {e}")
logger.debug("Generation error details:", exc_info=True)
```

### list-models

List available Gemini models.

**Output Format:**
```
Available Gemini Image Generation Models:
  • gemini-2.5-flash-image (default) - Fast, high-quality image generation
  • gemini-3-pro-image-preview - Advanced model with higher quality and more features
```

### list-aspect-ratios

List supported aspect ratios.

**Output Format:**
```
Available Aspect Ratios:
  1:1    (1024x1024)  - Square (Instagram post, social media)
  16:9   (1344x768)   - Widescreen (YouTube thumbnail, desktop)
  ...
```

## Development Commands

### Quick Start

```bash
# Install dependencies
make install

# Run checks
make check

# Full pipeline
make pipeline
```

### Quality Checks

```bash
# Format code (auto-fix)
make format                    # ruff format

# Lint code
make lint                      # ruff check

# Type check (strict mode)
make typecheck                 # mypy --strict

# Run tests
make test                      # pytest

# All checks
make check                     # lint + typecheck + test
```

### Build & Install

```bash
# Build package
make build                     # uv build

# Install globally
make install-global            # uv tool install dist/*.whl

# Full pipeline
make pipeline                  # format + check + build + install-global
```

### Run Locally

```bash
# Run without installing
make run ARGS="--help"
make run ARGS="generate 'test prompt' -o test.png"

# Or directly
uv run gemini-nano-banana-tool --help
```

## Code Standards

### Python Version & Syntax

- **Python 3.14+** required
- Use modern syntax: `dict` and `list` (not `Dict` and `List` from typing)
- Use `|` for union types (not `Union`)
- Use `str | None` (not `Optional[str]`)

### Type Hints

Required for all functions:

```python
def generate_image(
    client: genai.Client,
    prompt: str,
    output_path: str,
    reference_images: list[str] | None = None,
    aspect_ratio: str = "1:1",
    model: str = DEFAULT_MODEL,
) -> dict[str, Any]:
    """Generate image from prompt."""
```

### Docstrings

Required for all public functions:

```python
def create_client(api_key: str | None = None) -> genai.Client:
    """Create and configure a Gemini client.

    Args:
        api_key: API key for authentication (optional, reads from env)

    Returns:
        Configured Gemini client

    Raises:
        AuthenticationError: If authentication fails
    """
```

### Module Docstrings

Required at the top of every `.py` file:

```python
"""Image generation logic for Gemini Nano Banana.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""
```

### Error Handling

- Core functions raise exceptions (never call `sys.exit()`)
- CLI commands catch exceptions and handle exit codes
- Provide actionable error messages

```python
# Good (in core/)
if not api_key:
    raise AuthenticationError(
        "API key required. Set GEMINI_API_KEY or use --api-key option. "
        "Get API key from https://aistudio.google.com/app/apikey"
    )

# Good (in commands/)
try:
    result = generate_image(...)
except AuthenticationError as e:
    click.echo(f"Error: {e}", err=True)
    sys.exit(1)
```

## Important Notes

### Dependencies

- **google-genai**: Official Google Generative AI Python SDK
  - [PyPI](https://pypi.org/project/google-genai/)
  - [Documentation](https://ai.google.dev/gemini-api/docs)
- **click**: CLI framework for building command-line interfaces
- **Pillow**: Image processing (optional, for validation)

### Authentication

The tool supports two authentication methods:

1. **Gemini Developer API** (recommended for development)
   - Set `GEMINI_API_KEY` or `GOOGLE_API_KEY`
   - Get key from [Google AI Studio](https://aistudio.google.com/app/apikey)

2. **Vertex AI** (for production/enterprise)
   - Set `GOOGLE_GENAI_USE_VERTEXAI=true`
   - Set `GOOGLE_CLOUD_PROJECT` and `GOOGLE_CLOUD_LOCATION`
   - Authenticate with `gcloud auth application-default login`

### Image Generation Details

- **Maximum Reference Images**: 3
- **Supported Formats**: PNG, JPEG, WebP (output automatically determined by extension)
- **SynthID Watermarking**: Automatically applied by Google for authenticity
- **Rate Limits**: Free tier ~15 requests/minute (check current limits in API docs)

### Version Synchronization

Keep version consistent across three locations:
1. `pyproject.toml` → `[project] version = "1.0.0"`
2. `cli.py` → `@click.version_option(version="1.0.0")`
3. `__init__.py` → `__version__ = "1.0.0"`

## Testing

### Run Tests

```bash
# All tests
make test

# Specific test file
uv run pytest tests/test_generator.py

# With coverage
uv run pytest --cov=gemini_nano_banana_tool

# Verbose
uv run pytest -v
```

### Test Structure

```python
def test_generate_image_success():
    """Test successful image generation."""
    # Arrange
    client = Mock(spec=genai.Client)
    prompt = "test prompt"

    # Act
    result = generate_image(client, prompt, "output.png")

    # Assert
    assert result["output_path"] == "output.png"
    assert "resolution" in result
```

## Known Issues & Future Fixes

### Current Implementation

All features are functional based on the `google-genai` SDK.

### Future Enhancements

- **Batch Generation**: Support generating multiple images from a file of prompts
- **Progress Bar**: Add progress indication for long-running generations
- **Image Validation**: Validate output images with Pillow
- **Caching**: Cache API responses for development/testing
- **Config File**: Support `.gemini-nano-banana.yaml` for defaults

## Library Usage

The tool can be imported and used programmatically:

```python
from gemini_nano_banana_tool import create_client, generate_image, AspectRatio

# Create client
client = create_client()

# Generate image
result = generate_image(
    client=client,
    prompt="A beautiful sunset",
    output_path="sunset.png",
    aspect_ratio=AspectRatio.RATIO_16_9,
    model="gemini-2.5-flash-image"
)

print(f"Generated: {result['output_path']}")
print(f"Resolution: {result['resolution']}")
print(f"Tokens: {result['token_count']}")
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes following code standards
4. Run `make pipeline` to ensure all checks pass
5. Commit with descriptive message
6. Submit pull request

## Resources

- **Official Gemini Docs**: https://ai.google.dev/gemini-api/docs/image-generation
- **google-genai SDK**: https://pypi.org/project/google-genai/
- **Google AI Studio**: https://aistudio.google.com/
- **Click Documentation**: https://click.palletsprojects.com/
- **uv Documentation**: https://github.com/astral-sh/uv

---

**Generated with Claude Code**

This developer guide was created to support professional development of the gemini-nano-banana-tool CLI. The architecture emphasizes separation of concerns, type safety, and agent-friendly design patterns for reliable automation and integration.
