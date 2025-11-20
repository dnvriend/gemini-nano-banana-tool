# Promptgen Command

Transform simple descriptions into detailed, optimized image generation prompts using Gemini 2.0 Flash AI.

## Usage

```bash
gemini-nano-banana-tool promptgen DESCRIPTION [OPTIONS]
```

## Arguments

- `DESCRIPTION` - Simple description to enhance (e.g., "wizard cat", "cyberpunk city")

## Options

- `-t, --template TEXT` - Apply specialized template (photography, character, scene, food, abstract, logo)
- `-s, --style TEXT` - Style hint (photorealistic, artistic, minimalist, etc.)
- `-o, --output PATH` - Save prompt to file instead of stdout
- `--json` - Output in JSON format
- `-v, --verbose` - Show analysis and reasoning
- `--list-templates` - Show all available templates

## Examples

### Basic Usage

```bash
# Generate detailed prompt from simple description
gemini-nano-banana-tool promptgen "wizard cat"

# With template for better results
gemini-nano-banana-tool promptgen "wizard cat" --template character

# Save to file for reuse
gemini-nano-banana-tool promptgen "sunset landscape" -o prompt.txt
```

### Pipeline: Generate Prompt → Create Image

```bash
# Single pipeline: description → optimized prompt → image
gemini-nano-banana-tool promptgen "wizard cat in magical library" | \
  gemini-nano-banana-tool generate --stdin -o wizard-cat.png -a 16:9
```

### With Templates

```bash
# Photography template - technical camera details
gemini-nano-banana-tool promptgen "mountain landscape" --template photography

# Food template - plating and lighting
gemini-nano-banana-tool promptgen "pasta dish" --template food

# Scene template - foreground/midground/background
gemini-nano-banana-tool promptgen "cyberpunk city" --template scene
```

### JSON Output (for automation)

```bash
# Get structured output
gemini-nano-banana-tool promptgen "sunset" --json

# Output format:
# {
#   "original": "sunset",
#   "prompt": "A breathtaking golden hour sunset...",
#   "template": null,
#   "style": null,
#   "tokens_used": 156
# }
```

## Available Templates

- `photography` - Professional photography with technical details (aperture, focal length, lighting)
- `character` - Character design with pose, attire, expression
- `scene` - Scene composition with foreground/midground/background layers
- `food` - Food photography with plating, garnish, lighting
- `abstract` - Abstract art with shapes, colors, patterns
- `logo` - Logo design with typography, symbolism, brand identity

## Why Use Promptgen?

Creating effective image generation prompts requires knowledge of:
- Photography and composition terminology
- Lighting and technical details
- Artistic styles and techniques
- Color theory and palettes

Promptgen automates this expertise using AI, transforming simple ideas into detailed, effective prompts.

## Output Modes

- **Plain text** (default) - Ready for piping to generate command
- **JSON** (`--json`) - Structured output for scripts and automation
- **Verbose** (`-v`) - Shows AI analysis and reasoning process

## Cost

Promptgen uses Gemini 2.0 Flash for prompt generation:
- Cost: ~$0.001-0.003 per prompt optimization
- Much cheaper than trial-and-error generation

## Authentication

Requires `GEMINI_API_KEY` or `GOOGLE_API_KEY` environment variable.

Get your API key: https://aistudio.google.com/app/apikey
