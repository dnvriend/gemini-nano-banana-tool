# Generate Command

Generate images from text prompts with optional reference images using Google Gemini models.

## Usage

```bash
gemini-nano-banana-tool generate [PROMPT] -o OUTPUT [OPTIONS]
```

## Arguments

- `PROMPT` - Text prompt (positional, mutually exclusive with `-f` and `-s`)

## Required Options

- `-o, --output PATH` - Output image file path (required)

## Prompt Input Options (mutually exclusive)

- `PROMPT` - Positional argument (default)
- `-f, --prompt-file PATH` - Read prompt from file
- `-s, --stdin` - Read prompt from stdin (for piping)

## Image Options

- `-i, --image PATH` - Reference image (can be used up to 3 times for Flash, 14 for Pro)
- `-a, --aspect-ratio TEXT` - Aspect ratio (default: 1:1)
- `-m, --model TEXT` - Gemini model (default: gemini-2.5-flash-image)
- `-r, --resolution TEXT` - Resolution quality for Pro model (1K/2K/4K)

## Authentication Options

- `--api-key TEXT` - Override API key from environment
- `--use-vertex` - Use Vertex AI instead of Developer API
- `--project TEXT` - Google Cloud project (for Vertex AI)
- `--location TEXT` - Google Cloud location (for Vertex AI)

## Other Options

- `-v, --verbose` - Multi-level verbosity (-v INFO, -vv DEBUG, -vvv TRACE)

## Examples

### Basic Text-to-Image

```bash
# Simple generation
gemini-nano-banana-tool generate "A cat wearing a wizard hat" -o cat.png

# With aspect ratio
gemini-nano-banana-tool generate "Mountain landscape" -o landscape.png -a 16:9
```

### Prompt from File or Stdin

```bash
# From file
gemini-nano-banana-tool generate -f prompt.txt -o output.png

# From stdin (piping)
echo "Beautiful sunset" | gemini-nano-banana-tool generate -o sunset.png -s

# With promptgen
gemini-nano-banana-tool promptgen "wizard cat" | \
  gemini-nano-banana-tool generate -o cat.png -s -a 16:9
```

### Image Editing with Reference Images

```bash
# Single reference image
gemini-nano-banana-tool generate "Add a birthday hat" -o edited.png \
  -i original.jpg

# Multiple reference images
gemini-nano-banana-tool generate "Put the dress on the model in garden" \
  -o fashion.png -i dress.jpg -i model.jpg

# Up to 3 references (Flash) or 14 (Pro)
gemini-nano-banana-tool generate "Combine these styles" -o result.png \
  -i ref1.jpg -i ref2.jpg -i ref3.jpg
```

### Different Aspect Ratios

```bash
# Square (Instagram post)
gemini-nano-banana-tool generate "Modern design" -o square.png -a 1:1

# Widescreen (YouTube thumbnail)
gemini-nano-banana-tool generate "Epic scene" -o wide.png -a 16:9

# Vertical (Instagram story)
gemini-nano-banana-tool generate "Portrait" -o vertical.png -a 9:16

# Cinematic (ultra-wide)
gemini-nano-banana-tool generate "Sci-fi panorama" -o cinema.png -a 21:9
```

### Model Selection and Resolution

```bash
# Default Flash model (fast, cost-effective)
gemini-nano-banana-tool generate "Your prompt" -o output.png

# Pro model (higher quality)
gemini-nano-banana-tool generate "Your prompt" -o output.png \
  -m gemini-3-pro-image-preview

# Pro with 4K resolution (maximum quality)
gemini-nano-banana-tool generate "Your prompt" -o output.png \
  -m gemini-3-pro-image-preview -r 4K
```

### Verbosity Levels

```bash
# Normal (warnings only)
gemini-nano-banana-tool generate "test" -o output.png

# Verbose (show operations)
gemini-nano-banana-tool generate "test" -o output.png -v

# Debug (detailed info)
gemini-nano-banana-tool generate "test" -o output.png -vv

# Trace (full HTTP logs)
gemini-nano-banana-tool generate "test" -o output.png -vvv
```

## Output Format

Returns JSON with generation details:

```json
{
  "output_path": "output.png",
  "model": "gemini-2.5-flash-image",
  "aspect_ratio": "16:9",
  "resolution": "1344x768",
  "resolution_quality": "1K",
  "reference_image_count": 0,
  "token_count": 1295,
  "estimated_cost_usd": 0.0389,
  "metadata": {
    "finish_reason": "STOP",
    "safety_ratings": null
  }
}
```

## Cost Information

Automatic cost tracking based on token usage:

- **Flash Model**: ~$0.039 per image (1,290 tokens × $0.00003)
- **Pro Model 1K/2K**: ~$0.134 per image (1,120 tokens × $0.00012)
- **Pro Model 4K**: ~$0.24 per image (2,000 tokens × $0.00012)

Cost is always included in output JSON as `estimated_cost_usd`.

## Supported Aspect Ratios

- `1:1` - Square (1024×1024)
- `16:9` - Widescreen (1344×768)
- `9:16` - Vertical (768×1344)
- `4:3` - Traditional (1184×864)
- `3:4` - Portrait (864×1184)
- `3:2` - DSLR (1248×832)
- `2:3` - Portrait photo (832×1248)
- `21:9` - Cinematic (1536×672)
- `4:5` - Instagram portrait (896×1152)
- `5:4` - Medium format (1152×896)

## Authentication

Set environment variable:
```bash
export GEMINI_API_KEY='your-api-key'
```

Get API key: https://aistudio.google.com/app/apikey

For Vertex AI:
```bash
export GOOGLE_GENAI_USE_VERTEXAI=true
export GOOGLE_CLOUD_PROJECT='your-project-id'
export GOOGLE_CLOUD_LOCATION='us-central1'
```
