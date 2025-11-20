# Generate Conversation Command

Multi-turn image generation with progressive refinement. Each turn builds on previous context, allowing iterative improvements without starting over.

## Usage

```bash
gemini-nano-banana-tool generate-conversation PROMPT -o OUTPUT [OPTIONS]
```

## Arguments

- `PROMPT` - Text prompt for this turn (required)

## Required Options

- `-o, --output PATH` - Output image file path (required)

## Conversation Options

- `-f, --file PATH` - Conversation file (creates new if doesn't exist)
- `-a, --aspect-ratio TEXT` - Aspect ratio (default: 1:1, only for new conversations)
- `-m, --model TEXT` - Gemini model (default: gemini-2.5-flash-image, only for new)

## Authentication Options

- `--api-key TEXT` - Override API key from environment
- `--use-vertex` - Use Vertex AI instead of Developer API
- `--project TEXT` - Google Cloud project (for Vertex AI)
- `--location TEXT` - Google Cloud location (for Vertex AI)

## Other Options

- `-v, --verbose` - Multi-level verbosity (-v INFO, -vv DEBUG, -vvv TRACE)

## How It Works

1. **First Turn**: Create initial image from prompt, save conversation state
2. **Subsequent Turns**: Previous output automatically becomes reference image
3. **Persistence**: All turns, prompts, and metadata saved to JSON file
4. **Resume**: Load conversation file to continue refinement

## Examples

### Basic Multi-Turn Workflow

```bash
# Turn 1: Initial generation
gemini-nano-banana-tool generate-conversation "A sunset over mountains" \
  -o sunset1.png --file conversation.json

# Turn 2: Refinement (loads conversation automatically)
gemini-nano-banana-tool generate-conversation "Make the sky more orange" \
  -o sunset2.png --file conversation.json

# Turn 3: Further refinement
gemini-nano-banana-tool generate-conversation "Add a lake in the foreground" \
  -o sunset3.png --file conversation.json
```

### Interior Design Example

```bash
# Turn 1: Initial room
gemini-nano-banana-tool generate-conversation \
  "A modern minimalist living room with large windows" \
  -o room-v1.png --file interior.json -a 16:9

# Turn 2: Add furniture
gemini-nano-banana-tool generate-conversation \
  "Add a gray sofa and wooden coffee table" \
  -o room-v2.png --file interior.json

# Turn 3: Adjust lighting
gemini-nano-banana-tool generate-conversation \
  "Make the lighting warmer and add floor lamp" \
  -o room-v3.png --file interior.json

# Turn 4: Final touches
gemini-nano-banana-tool generate-conversation \
  "Add plants and artwork on the walls" \
  -o room-final.png --file interior.json
```

### Product Photography Example

```bash
# Turn 1: Initial product shot
gemini-nano-banana-tool generate-conversation \
  "Professional product photo of wireless headphones" \
  -o headphones-v1.png --file product.json -a 1:1

# Turn 2: Adjust angle
gemini-nano-banana-tool generate-conversation \
  "Rotate to show the left side" \
  -o headphones-v2.png --file product.json

# Turn 3: Change background
gemini-nano-banana-tool generate-conversation \
  "Change background to dark gradient" \
  -o headphones-v3.png --file product.json
```

## Conversation File Format

The conversation file stores complete history in JSON:

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

## Use Cases

- **Product Photography**: Iteratively adjust lighting, angles, styling
- **Character Design**: Refine poses, clothing, expressions progressively
- **Interior Design**: Build rooms by adding furniture and decor step by step
- **Marketing Materials**: Test variations while maintaining consistency
- **Concept Art**: Explore different iterations of a design
- **Fashion E-commerce**: Try products on models or in different settings

## Important Notes

- **Model & Aspect Ratio**: Only set when creating new conversation (locked for subsequent turns)
- **Reference Images**: Previous output automatically used (no manual `-i` needed)
- **Resume Anytime**: Load conversation file to continue from any turn
- **No File Flag**: Can use without `--file` but conversation won't be saved

## Why Use Conversation Mode?

- **Progressive Refinement**: Iteratively improve without losing context
- **Experiment Safely**: Try variations while maintaining consistency
- **Context Awareness**: Each turn references previous outputs automatically
- **Evolution Tracking**: Complete history of prompts and changes
- **Resume Anytime**: Continue conversations across sessions

## Cost Information

Each turn costs the same as a single generation:
- **Flash Model**: ~$0.039 per turn
- **Pro Model 1K/2K**: ~$0.134 per turn
- **Pro Model 4K**: ~$0.24 per turn

Cost is tracked per turn in conversation file metadata.

## Authentication

Set environment variable:
```bash
export GEMINI_API_KEY='your-api-key'
```

Get API key: https://aistudio.google.com/app/apikey
