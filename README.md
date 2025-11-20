# gemini-nano-banana-tool 🍌

<div align="center">
  <img src=".github/assets/logo.png" alt="gemini-nano-banana-tool" width="200" />
  <br>
  <em>Logo generated with Gemini Pro model (~$0.22 USD)</em>
  <br>
  <br>

[![Python Version](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](https://github.com/python/mypy)
[![AI Generated](https://img.shields.io/badge/AI-Generated-blueviolet.svg)](https://www.anthropic.com/claude)
[![Claude Sonnet 4.5](https://img.shields.io/badge/Model-Claude_Sonnet_4.5-blue)](https://www.anthropic.com/claude)
[![Built with Claude Code](https://img.shields.io/badge/Built_with-Claude_Code-5A67D8.svg)](https://www.anthropic.com/claude/code)

**Gemini Nano Banana Tool** - Professional CLI for generating, editing, and manipulating images using Google's Gemini image generation models (Nano Banana & Nano Banana 2)

</div>

## Table of Contents

- [About](#about)
  - [What is Nano Banana?](#what-is-nano-banana)
  - [Why This CLI?](#why-this-cli)
- [Use Cases](#use-cases)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Promptgen Command](#promptgen-command)
  - [Generate Command](#generate-command)
  - [Generate Conversation Command](#generate-conversation-command)
  - [List Commands](#list-commands)
- [Library Usage](#library-usage)
- [Resources](#resources)
- [Development](#development)
- [License](#license)

## About

### What is Nano Banana?

Google's Gemini image generation models come in two flavors:

**Nano Banana (gemini-2.5-flash-image)** - Fast image generation with fixed ~1024p resolution (up to 3 reference images)
**Nano Banana 2 (gemini-3-pro-image-preview)** - Advanced pro model with 1K/2K/4K resolution support (up to 14 reference images)

Both models provide:

- 🎨 High-quality text-to-image generation
- 🖼️ Image editing with natural language prompts
- 🔄 Multi-image composition (3 images for Flash, 14 images for Pro)
- 📐 Multiple aspect ratios (1:1, 16:9, 9:16, and more)
- 🎯 Variable resolution (Pro model: 1K/2K/4K quality levels)
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

- ✅ **AI Prompt Generation** - Transform simple descriptions into detailed prompts using Gemini 2.0 Flash
- ✅ **Prompt Templates** - 6 specialized templates (photography, character, scene, food, abstract, logo)
- ✅ **Text-to-Image Generation** - Create images from detailed text prompts
- ✅ **Multi-turn Conversations** - Progressive image refinement through conversational turns
- ✅ **Image Editing** - Edit existing images (3 ref images for Flash, 14 for Pro)
- ✅ **Multiple Aspect Ratios** - Support for 10 different aspect ratios
- ✅ **Variable Resolution** - Pro model supports 1K/2K/4K quality levels
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

### Shell Completion (Optional)

Enable shell completion for faster command-line usage:

```bash
# For Bash (add to ~/.bashrc):
eval "$(gemini-nano-banana-tool completion bash)"

# For Zsh (add to ~/.zshrc):
eval "$(gemini-nano-banana-tool completion zsh)"

# For Fish (save to completions directory):
gemini-nano-banana-tool completion fish > ~/.config/fish/completions/gemini-nano-banana-tool.fish
```

For help with shell completion:
```bash
gemini-nano-banana-tool completion --help
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

### Promptgen Command

The `promptgen` command transforms simple descriptions into detailed, best-practice prompts using AI.

#### Why Use Promptgen?

Creating effective image generation prompts requires specific knowledge about:
- Photography and composition terminology
- Lighting and technical details
- Artistic styles and techniques
- Color theory and palettes

The `promptgen` command uses Gemini 2.0 Flash to automatically generate detailed, optimized prompts from simple descriptions.

#### Basic Usage

```bash
# Simple description → detailed prompt
gemini-nano-banana-tool promptgen "wizard cat"

# Output:
# A majestic, fluffy Persian cat wearing an ornate, pointed wizard hat
# adorned with celestial symbols, perched upon a stack of ancient,
# leather-bound spellbooks in a dimly lit, gothic library...
```

#### With Templates

Templates apply best practices for specific categories:

```bash
# Character design template
gemini-nano-banana-tool promptgen "wizard cat" --template character

# Food photography template
gemini-nano-banana-tool promptgen "pasta dish" --template food

# Scene composition template
gemini-nano-banana-tool promptgen "cyberpunk city" --template scene
```

Available templates:
- `photography` - Professional photography with technical details
- `character` - Character design with pose and attire
- `scene` - Scene composition with foreground/midground/background
- `food` - Food photography with plating and lighting
- `abstract` - Abstract art with shapes and colors
- `logo` - Logo design with typography

#### Output Formats

```bash
# Plain text (default) - perfect for piping
gemini-nano-banana-tool promptgen "sunset"

# JSON output - for automation and scripts
gemini-nano-banana-tool promptgen "sunset" --json

# Verbose output - educational, shows analysis
gemini-nano-banana-tool promptgen "sunset" --verbose

# Save to file for reuse
gemini-nano-banana-tool promptgen "sunset" -o prompt.txt
```

#### Complete Workflow: Generate Prompt → Create Image

```bash
# Single pipeline: description → prompt → image
gemini-nano-banana-tool promptgen "wizard cat in magical library" | \
  gemini-nano-banana-tool generate --stdin -o wizard-cat.png -a 16:9

# Or save prompt for reuse
gemini-nano-banana-tool promptgen "cyberpunk city at night" \
  --template scene -o city-prompt.txt

gemini-nano-banana-tool generate -f city-prompt.txt -o city1.png -a 16:9
gemini-nano-banana-tool generate -f city-prompt.txt -o city2.png -a 1:1
```

#### List Available Templates

```bash
gemini-nano-banana-tool promptgen --list-templates
```

### Generate Command

The `generate` command creates images from text prompts with optional reference images.

#### Basic Text-to-Image

```bash
# Simple generation with positional argument
gemini-nano-banana-tool generate "A photorealistic cat wearing a wizard hat" -o cat.png

# With specific aspect ratio
gemini-nano-banana-tool generate "Panoramic mountain landscape" -o wide.png --aspect-ratio 16:9
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
gemini-nano-banana-tool generate "Add a birthday hat to the person" -o edited.png \
  --image original.jpg

# Multiple reference images (up to 3)
gemini-nano-banana-tool generate "Put the dress on the model in a garden setting" -o fashion.png \
  --image dress.jpg \
  --image model.jpg
```

#### Different Aspect Ratios

```bash
# Square (Instagram post)
gemini-nano-banana-tool generate "Modern minimalist design" -o square.png --aspect-ratio 1:1

# Landscape (YouTube thumbnail)
gemini-nano-banana-tool generate "Epic cinematic scene" -o landscape.png --aspect-ratio 16:9

# Portrait (Instagram story)
gemini-nano-banana-tool generate "Vertical portrait" -o portrait.png --aspect-ratio 9:16

# Cinematic (ultra-wide)
gemini-nano-banana-tool generate "Sci-fi panorama" -o cinema.png --aspect-ratio 21:9
```

#### Verbosity Levels

```bash
# Normal mode (warnings only)
gemini-nano-banana-tool generate "test" -o output.png

# Verbose mode (INFO level) - show high-level operations
gemini-nano-banana-tool generate "test" -o output.png -v

# Debug mode (DEBUG level) - show detailed validation and API calls
gemini-nano-banana-tool generate "test" -o output.png -vv

# Trace mode (DEBUG + library internals) - show full HTTP requests and library logs
gemini-nano-banana-tool generate "test" -o output.png -vvv
```

#### Model Selection

```bash
# Use default model (fast, high-quality, fixed ~1024p)
gemini-nano-banana-tool generate "Your prompt" -o output.png

# Use advanced model (higher quality, variable resolution, more features)
gemini-nano-banana-tool generate "Your prompt" -o output.png \
  --model gemini-3-pro-image-preview

# Default model is gemini-2.5-flash-image
```

#### Resolution Quality (Pro Model Only)

The Pro model (`gemini-3-pro-image-preview`) supports variable resolution quality:

```bash
# Default 1K resolution (~1024p)
gemini-nano-banana-tool generate "Your prompt" -o output.png \
  --model gemini-3-pro-image-preview

# 2K resolution (2x scale, higher quality)
gemini-nano-banana-tool generate "Your prompt" -o output.png \
  --model gemini-3-pro-image-preview \
  --resolution 2K

# 4K resolution (4x scale, maximum quality)
gemini-nano-banana-tool generate "Your prompt" -o output.png \
  --model gemini-3-pro-image-preview \
  --resolution 4K

# Note: Flash model ignores --resolution (fixed ~1024p)
```

**Resolution Scale Guide:**
- **1K** (default) - Standard quality, ~1024p base resolution
- **2K** - 2x scale, approximately 2048p (higher quality, more tokens)
- **4K** - 4x scale, approximately 4096p (maximum quality, most tokens)

#### Complete Options

```bash
gemini-nano-banana-tool generate [PROMPT] [OPTIONS]

Arguments:
  PROMPT                         Text prompt (mutually exclusive with --prompt-file and --stdin)

Options:
  -o, --output PATH              Output image file path [required]
  -f, --prompt-file PATH         Read prompt from file
  -s, --stdin                    Read prompt from stdin
  -i, --image PATH               Reference image (max 3 for Flash, 14 for Pro)
  -a, --aspect-ratio TEXT        Aspect ratio (default: 1:1)
  -m, --model TEXT               Gemini model (default: gemini-2.5-flash-image)
  -r, --resolution TEXT          Resolution quality (Pro only: 1K/2K/4K)
  --api-key TEXT                 Override API key from environment
  --use-vertex                   Use Vertex AI instead of Developer API
  --project TEXT                 Google Cloud project (for Vertex AI)
  --location TEXT                Google Cloud location (for Vertex AI)
  -v, --verbose                  Multi-level verbosity (-v INFO, -vv DEBUG, -vvv TRACE)
  --help                         Show this message and exit
```

### Generate Conversation Command

The `generate-conversation` command enables multi-turn image generation through conversational refinement. Each turn builds on previous context, allowing progressive improvements without starting over.

#### Why Use Conversation Mode?

Multi-turn conversation provides several advantages over single-shot generation:

- **Progressive Refinement** - Iteratively improve images without losing context
- **Experiment Safely** - Try variations while maintaining consistency
- **Context Awareness** - Each turn references previous outputs automatically
- **Evolution Tracking** - Complete history of prompts and changes
- **Resume Anytime** - Continue conversations across sessions

#### How It Works

1. **First Turn** - Create initial image from prompt, save conversation state
2. **Subsequent Turns** - Previous output becomes automatic reference image
3. **Persistence** - All turns, prompts, and metadata saved to JSON file
4. **Resume** - Load conversation file to continue refinement

#### Basic Usage

```bash
# Start new conversation
gemini-nano-banana-tool generate-conversation "A sunset over mountains" \
  -o sunset1.png --file conversation.json

# Continue with refinements (loads conversation automatically)
gemini-nano-banana-tool generate-conversation "Make the sky more orange" \
  -o sunset2.png --file conversation.json

# Further refinement
gemini-nano-banana-tool generate-conversation "Add a lake in the foreground" \
  -o sunset3.png --file conversation.json
```

#### Complete Workflow Example

```bash
# Turn 1: Initial generation
gemini-nano-banana-tool generate-conversation \
  "A modern minimalist living room with large windows" \
  -o room-v1.png \
  --file interior-design.json \
  --aspect-ratio 16:9

# Turn 2: Add furniture
gemini-nano-banana-tool generate-conversation \
  "Add a gray sofa and wooden coffee table" \
  -o room-v2.png \
  --file interior-design.json

# Turn 3: Adjust lighting
gemini-nano-banana-tool generate-conversation \
  "Make the lighting warmer and add floor lamp" \
  -o room-v3.png \
  --file interior-design.json

# Turn 4: Final touches
gemini-nano-banana-tool generate-conversation \
  "Add plants and artwork on the walls" \
  -o room-final.png \
  --file interior-design.json
```

#### Conversation File Format

The conversation file is JSON with complete history:

```json
{
  "conversation_id": "20251120_181305",
  "model": "gemini-2.5-flash-image",
  "aspect_ratio": "16:9",
  "turns": [
    {
      "prompt": "A sunset over mountains",
      "output_path": "/path/to/sunset1.png",
      "reference_images": [],
      "metadata": {
        "token_count": 1295,
        "resolution": "1344x768",
        "finish_reason": "STOP"
      },
      "timestamp": "2025-11-20T18:13:11.428020"
    },
    {
      "prompt": "Make the sky more orange",
      "output_path": "/path/to/sunset2.png",
      "reference_images": ["/path/to/sunset1.png"],
      "metadata": {
        "token_count": 1554,
        "resolution": "1344x768",
        "finish_reason": "STOP"
      },
      "timestamp": "2025-11-20T18:13:27.318416"
    }
  ],
  "created_at": "2025-11-20T18:13:05.751502",
  "updated_at": "2025-11-20T18:13:27.318430"
}
```

#### Conversation Options

```bash
gemini-nano-banana-tool generate-conversation [PROMPT] [OPTIONS]

Arguments:
  PROMPT                         Text prompt for this turn [required]

Options:
  -o, --output PATH              Output image file path [required]
  -f, --file PATH                Conversation file (creates new if doesn't exist)
  -a, --aspect-ratio TEXT        Aspect ratio (default: 1:1, only for new conversations)
  -m, --model TEXT               Gemini model (default: gemini-2.5-flash-image, only for new)
  --api-key TEXT                 Override API key from environment
  --use-vertex                   Use Vertex AI instead of Developer API
  --project TEXT                 Google Cloud project (for Vertex AI)
  --location TEXT                Google Cloud location (for Vertex AI)
  -v, --verbose                  Multi-level verbosity (-v INFO, -vv DEBUG, -vvv TRACE)
  --help                         Show this message and exit
```

#### Important Notes

- **Model & Aspect Ratio**: Only set when creating new conversation (locked for subsequent turns)
- **Reference Images**: Previous output automatically used as reference (no manual `-i` needed)
- **Resume Anytime**: Load conversation file to continue from any turn
- **No File Flag**: Can use without `--file` but conversation won't be saved

#### Use Cases

- **Product Photography** - Iteratively adjust lighting, angles, and styling
- **Character Design** - Refine poses, clothing, and expressions progressively
- **Interior Design** - Build rooms by adding furniture and decor step by step
- **Marketing Materials** - Test variations while maintaining brand consistency
- **Concept Art** - Explore different iterations of a design concept
- **Fashion E-commerce** - Try different products on models or in settings

### List Commands

#### List Available Models

```bash
gemini-nano-banana-tool list-models
```

Output:
```
Available Gemini Image Generation Models:
  • gemini-2.5-flash-image (default) - Fast, high-quality image generation
  • gemini-3-pro-image-preview - Advanced model with higher quality and more features
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

### Prompt Generation

```python
from gemini_nano_banana_tool import create_client, generate_prompt

# Create client
client = create_client()  # Uses GEMINI_API_KEY from environment

# Generate detailed prompt from simple description
result = generate_prompt(
    client=client,
    description="wizard cat",
    template="character",  # Optional: use template
    style="photorealistic",  # Optional: style hint
)

print(f"Original: {result['original']}")
print(f"Generated Prompt: {result['prompt']}")
print(f"Tokens used: {result['tokens_used']}")

# Use the generated prompt for image generation
detailed_prompt = result['prompt']
```

### Image Generation

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
print(f"Estimated cost: ${result['estimated_cost_usd']:.4f}")

# Generate with reference images
result = generate_image(
    client=client,
    prompt="Add a hat to the person",
    output_path="edited.png",
    reference_images=["original.jpg"],
    aspect_ratio=AspectRatio.RATIO_1_1
)

# Generate with Pro model and 4K resolution
result = generate_image(
    client=client,
    prompt="Professional product photography",
    output_path="product-4k.png",
    aspect_ratio=AspectRatio.RATIO_16_9,
    model="gemini-3-pro-image-preview",
    resolution="4K"
)
```

### Complete Workflow

```python
from gemini_nano_banana_tool import create_client, generate_prompt, generate_image

# Create client (reuse for multiple operations)
client = create_client()

# Step 1: Generate optimized prompt
prompt_result = generate_prompt(
    client=client,
    description="cyberpunk city at night",
    template="scene"
)

# Step 2: Generate image with optimized prompt
image_result = generate_image(
    client=client,
    prompt=prompt_result['prompt'],
    output_path="cyberpunk-city.png",
    aspect_ratio="16:9"
)

print(f"Image saved: {image_result['output_path']}")
```

### Vertex AI

```python
# Vertex AI client
vertex_client = create_client(
    use_vertex=True,
    project="my-project",
    location="us-central1"
)
```

## Pricing & Cost Tracking

All image generation responses automatically include **estimated cost** in USD based on actual token usage.

### Pricing Structure

**Flash Model (gemini-2.5-flash-image)**:
- $30 per 1M output tokens = **$0.00003 per token**
- Typical: ~1,290 tokens/image = **~$0.039 per image**
- Resolution: Fixed ~1024p

**Pro Model (gemini-3-pro-image-preview)**:
- $120 per 1M output tokens = **$0.00012 per token**
- **1K/2K**: ~1,120 tokens/image = **~$0.134 per image**
- **4K**: ~2,000 tokens/image = **~$0.24 per image**
- Resolution: Variable 1K/2K/4K

### Cost in JSON Output

Every generation includes `estimated_cost_usd` calculated from actual token usage:

```json
{
  "output_path": "image.png",
  "model": "gemini-2.5-flash-image",
  "token_count": 1295,
  "estimated_cost_usd": 0.0389,
  ...
}
```

### Cost Examples

| Volume | Flash Cost | Pro 1K/2K Cost | Pro 4K Cost |
|--------|------------|----------------|-------------|
| 10 images | $0.39 | $1.34 | $2.40 |
| 100 images | $3.90 | $13.40 | $24.00 |
| 1,000 images | $39.00 | $134.00 | $240.00 |

For detailed pricing information, see [references/api-setup-pricing.md](references/api-setup-pricing.md).

## Resources

- **Official Documentation**: [Gemini Image Generation Guide](https://ai.google.dev/gemini-api/docs/image-generation)
- **Official Pricing**: [Google AI Pricing](https://ai.google.dev/pricing)
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
