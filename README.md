# gemini-nano-banana-tool 🍌

[![Python Version](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](https://github.com/python/mypy)
[![AI Generated](https://img.shields.io/badge/AI-Generated-blueviolet.svg)](https://www.anthropic.com/claude)
[![Claude Sonnet 4.5](https://img.shields.io/badge/Model-Claude_Sonnet_4.5-blue)](https://www.anthropic.com/claude)
[![Built with Claude Code](https://img.shields.io/badge/Built_with-Claude_Code-5A67D8.svg)](https://www.anthropic.com/claude/code)

A professional CLI for generating, editing, and manipulating images using Google's Gemini 2.5 Flash Image model (codename "Nano Banana").

## Table of Contents

- [About](#about)
  - [What is Nano Banana?](#what-is-nano-banana)
  - [Why This CLI?](#why-this-cli)
- [Use Cases](#use-cases)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Generate Command](#generate-command)
  - [List Commands](#list-commands)
- [Library Usage](#library-usage)
- [Resources](#resources)
- [Development](#development)
- [License](#license)

## About

### What is Nano Banana?

**Gemini 2.5 Flash Image** (codename "Nano Banana") is Google's latest AI image generation model that provides:

- 🎨 High-quality text-to-image generation
- 🖼️ Image editing with natural language prompts
- 🔄 Multi-image composition (up to 3 reference images)
- 📐 Multiple aspect ratios (1:1, 16:9, 9:16, and more)
- 🎭 Style transfer and artistic rendering
- ✨ Built-in SynthID watermarking for authenticity

Learn more: [Google Gemini Image Generation Documentation](https://ai.google.dev/gemini-api/docs/image-generation)

### Why This CLI?

This tool provides a **professional, agent-friendly CLI** for Gemini image generation with:

- **🤖 Agent-Friendly Design**: Structured commands and error messages enable AI agents (like Claude Code) to reason and act effectively in ReAct loops
- **🔧 Composable Architecture**: JSON output to stdout, logs to stderr—perfect for pipes and automation
- **📦 Reusable Building Blocks**: Commands serve as building blocks for skills, MCP servers, shell scripts, and workflows
- **🛡️ Type-Safe & Reliable**: Comprehensive type hints and mypy strict mode ensure predictable behavior in automated systems
- **📚 Rich Documentation**: Extensive help messages and error handling guide both humans and agents
- **🎯 Dual-Mode Operation**: Use as CLI tool or import as Python library

## Use Cases

- 🎨 **Creative Content Generation** - Generate marketing visuals, social media content, concept art
- 🖼️ **Image Editing & Enhancement** - Remove objects, change backgrounds, apply style transfers
- 🔄 **Multi-Image Composition** - Combine multiple images for fashion e-commerce, product visualization
- 📐 **Multi-Format Output** - Generate images for various platforms (Instagram, YouTube, TikTok, etc.)
- 🤖 **AI Agent Integration** - Build autonomous image generation workflows with Claude Code
- 🔁 **Batch Processing** - Script generation pipelines with shell loops and automation
- 🧪 **Rapid Prototyping** - Quick visual mockups and design iterations

## Features

- ✅ **Text-to-Image Generation** - Create images from detailed text prompts
- ✅ **Image Editing** - Edit existing images with up to 3 reference images
- ✅ **Multiple Aspect Ratios** - Support for 10 different aspect ratios
- ✅ **Flexible Prompt Input** - From argument, file, or stdin
- ✅ **Model Selection** - Choose from multiple Gemini models
- ✅ **Dual Authentication** - Supports both Gemini API key and Vertex AI
- ✅ **Discovery Commands** - List available models and aspect ratios
- ✅ **Type-Safe** - Full type hints with mypy strict mode
- ✅ **Library Mode** - Import and use programmatically
- ✅ **Agent-Ready** - Structured output for AI automation

## Installation

### Prerequisites

- **Python 3.14 or higher**
- **uv** package manager ([installation guide](https://github.com/astral-sh/uv))

### Install from Source

```bash
# Clone the repository
git clone https://github.com/dnvriend/gemini-nano-banana-tool.git
cd gemini-nano-banana-tool

# Install globally with uv
uv tool install .
```

### Install with mise (Recommended for Development)

```bash
cd gemini-nano-banana-tool
mise trust
mise install
uv sync
uv tool install .
```

### Verify Installation

```bash
gemini-nano-banana-tool --version
gemini-nano-banana-tool --help
```

## Configuration

### Gemini Developer API (Recommended)

Set `GEMINI_API_KEY` or `GOOGLE_API_KEY`. The client automatically picks up these variables. If both are set, `GOOGLE_API_KEY` takes precedence.

```bash
export GEMINI_API_KEY='your-api-key'
```

**Get your API key:**

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create or select a project
3. Generate an API key
4. Set the environment variable

### Gemini API on Vertex AI

For Vertex AI, set the following environment variables:

```bash
export GOOGLE_GENAI_USE_VERTEXAI=true
export GOOGLE_CLOUD_PROJECT='your-project-id'
export GOOGLE_CLOUD_LOCATION='us-central1'
```

**Prerequisites:**

- Google Cloud project with Vertex AI API enabled
- Proper IAM permissions for Vertex AI
- Authenticated with `gcloud auth application-default login`

## Usage

### Generate Command

The `generate` command creates images from text prompts with optional reference images.

#### Basic Text-to-Image

```bash
# Simple generation
gemini-nano-banana-tool generate -o cat.png --prompt "A photorealistic cat wearing a wizard hat"

# With specific aspect ratio
gemini-nano-banana-tool generate -o wide.png --aspect-ratio 16:9 \
  --prompt "A panoramic mountain landscape at golden hour"
```

#### Prompt from File

```bash
# Read prompt from file
gemini-nano-banana-tool generate -o output.png --prompt-file prompt.txt

# Read from stdin
echo "A beautiful sunset" | gemini-nano-banana-tool generate -o sunset.png --stdin
```

#### Image Editing (Reference Images)

```bash
# Edit with single reference image
gemini-nano-banana-tool generate -o edited.png \
  --image original.jpg \
  --prompt "Add a birthday hat to the person"

# Multiple reference images (up to 3)
gemini-nano-banana-tool generate -o fashion.png \
  --image dress.jpg \
  --image model.jpg \
  --prompt "Put the dress on the model in a garden setting"
```

#### Different Aspect Ratios

```bash
# Square (Instagram post)
gemini-nano-banana-tool generate -o square.png --aspect-ratio 1:1 --prompt "..."

# Landscape (YouTube thumbnail)
gemini-nano-banana-tool generate -o landscape.png --aspect-ratio 16:9 --prompt "..."

# Portrait (Instagram story)
gemini-nano-banana-tool generate -o portrait.png --aspect-ratio 9:16 --prompt "..."

# Cinematic (ultra-wide)
gemini-nano-banana-tool generate -o cinema.png --aspect-ratio 21:9 --prompt "..."
```

#### Model Selection

```bash
# Use specific model
gemini-nano-banana-tool generate -o output.png \
  --model gemini-2.0-flash-exp \
  --prompt "Your prompt"

# Default model is gemini-2.5-flash-image
```

#### Complete Options

```bash
gemini-nano-banana-tool generate [OPTIONS]

Options:
  -o, --output PATH              Output image file path [required]
  -p, --prompt TEXT              Prompt text (mutually exclusive with --prompt-file and --stdin)
  -f, --prompt-file PATH         Read prompt from file (mutually exclusive with --prompt and --stdin)
  -s, --stdin                    Read prompt from stdin (mutually exclusive with --prompt and --prompt-file)
  -i, --image PATH               Reference image (can be used up to 3 times)
  -a, --aspect-ratio TEXT        Aspect ratio (default: 1:1)
  -m, --model TEXT               Gemini model (default: gemini-2.5-flash-image)
  --api-key TEXT                 Override API key from environment
  --use-vertex                   Use Vertex AI instead of Developer API
  --project TEXT                 Google Cloud project (for Vertex AI)
  --location TEXT                Google Cloud location (for Vertex AI)
  -v, --verbose                  Enable verbose output
  --help                         Show this message and exit
```

### List Commands

#### List Available Models

```bash
gemini-nano-banana-tool list-models
```

Output:
```
Available Gemini Image Generation Models:
  • gemini-2.5-flash-image (default) - Fast, high-quality image generation
  • gemini-2.0-flash-exp - Experimental features
  • gemini-1.5-pro - Higher quality, slower generation
  • gemini-1.5-flash - Fast generation
```

#### List Aspect Ratios

```bash
gemini-nano-banana-tool list-aspect-ratios
```

Output:
```
Available Aspect Ratios:
  1:1    (1024x1024)  - Square (Instagram post, social media)
  16:9   (1344x768)   - Widescreen (YouTube thumbnail, desktop)
  9:16   (768x1344)   - Vertical (Instagram story, TikTok, mobile)
  4:3    (1184x864)   - Traditional (classic photography)
  3:4    (864x1184)   - Portrait orientation
  3:2    (1248x832)   - DSLR photography
  2:3    (832x1248)   - Portrait photography
  21:9   (1536x672)   - Cinematic (ultra-wide)
  4:5    (896x1152)   - Instagram portrait
  5:4    (1152x896)   - Medium format photography
```

## Library Usage

Import and use programmatically in your Python code:

```python
from gemini_nano_banana_tool import create_client, generate_image, AspectRatio

# Create client
client = create_client()  # Uses GEMINI_API_KEY from environment

# Generate image from text
result = generate_image(
    client=client,
    prompt="A beautiful sunset over mountains",
    output_path="sunset.png",
    aspect_ratio=AspectRatio.RATIO_16_9,
    model="gemini-2.5-flash-image"
)

print(f"Generated: {result['output_path']}")
print(f"Resolution: {result['resolution']}")
print(f"Tokens used: {result['token_count']}")

# Generate with reference images
result = generate_image(
    client=client,
    prompt="Add a hat to the person",
    output_path="edited.png",
    reference_images=["original.jpg"],
    aspect_ratio=AspectRatio.RATIO_1_1
)

# Vertex AI client
vertex_client = create_client(
    use_vertex=True,
    project="my-project",
    location="us-central1"
)
```

## Resources

- **Official Documentation**: [Gemini Image Generation Guide](https://ai.google.dev/gemini-api/docs/image-generation)
- **Google AI Studio**: [Get API Key](https://aistudio.google.com/app/apikey)
- **Python SDK**: [google-genai](https://pypi.org/project/google-genai/)
- **Vertex AI**: [Setup Guide](https://cloud.google.com/vertex-ai/docs/start/introduction-unified-platform)

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/dnvriend/gemini-nano-banana-tool.git
cd gemini-nano-banana-tool

# Install dependencies
make install

# Show available commands
make help
```

### Available Make Commands

```bash
make install          # Install dependencies
make format           # Format code with ruff
make lint             # Run linting with ruff
make typecheck        # Run type checking with mypy
make test             # Run tests with pytest
make check            # Run all checks (lint, typecheck, test)
make pipeline         # Run full pipeline (format, check, build, install-global)
make build            # Build package
make clean            # Remove build artifacts
```

### Project Structure

```
gemini-nano-banana-tool/
├── gemini_nano_banana_tool/
│   ├── __init__.py              # Public API exports
│   ├── cli.py                   # CLI entry point
│   ├── core/                    # Core library
│   │   ├── __init__.py
│   │   ├── client.py           # Gemini client management
│   │   ├── generator.py        # Image generation logic
│   │   └── models.py           # Data models and constants
│   ├── commands/                # CLI commands
│   │   ├── __init__.py
│   │   ├── generate_command.py
│   │   └── list_commands.py
│   └── utils.py                 # Utilities
├── tests/                       # Test suite
├── pyproject.toml               # Project configuration
├── Makefile                     # Development commands
├── README.md                    # This file
└── CLAUDE.md                    # Developer guide
```

### Code Standards

- Python 3.14+ with modern syntax (`dict`/`list` over `Dict`/`List`)
- Type hints required for all functions
- Docstrings with Args, Returns, Raises sections
- Line length: 100 characters
- Format with `ruff`, type check with `mypy --strict`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Dennis Vriend**

- GitHub: [@dnvriend](https://github.com/dnvriend)

## Acknowledgments

- Built with [Click](https://click.palletsprojects.com/) for CLI framework
- Powered by [google-genai](https://pypi.org/project/google-genai/) SDK
- Developed with [uv](https://github.com/astral-sh/uv) for fast Python tooling
- Inspired by [gemini-tts-tool](https://github.com/dnvriend/gemini-tts-tool)

---

**Generated with AI**

This project was created using [Claude Code](https://www.anthropic.com/claude/code), an AI-powered development tool. The CLI-first design philosophy ensures reliable integration with AI agents, automation pipelines, and provides reusable building blocks for image generation workflows.

Made with ❤️ using Python 3.14
