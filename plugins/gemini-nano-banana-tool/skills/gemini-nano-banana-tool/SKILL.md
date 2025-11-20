# Gemini Nano Banana Tool Skill

Professional CLI for Google Gemini image generation with AI-powered prompt optimization, cost tracking, and multi-turn conversations.

## Quick Reference

```bash
# AI prompt optimization
gemini-nano-banana-tool promptgen "simple description"

# Generate image
gemini-nano-banana-tool generate "detailed prompt" -o output.png

# Multi-turn refinement
gemini-nano-banana-tool generate-conversation "prompt" -o output.png -f conv.json

# Discovery
gemini-nano-banana-tool list-models
gemini-nano-banana-tool list-aspect-ratios
```

## Core Capabilities

### 1. AI Prompt Generation

Transform simple descriptions into detailed, optimized prompts:

```bash
# Basic usage
gemini-nano-banana-tool promptgen "wizard cat"

# With template for specialized prompts
gemini-nano-banana-tool promptgen "wizard cat" --template character

# Pipeline: optimize then generate
gemini-nano-banana-tool promptgen "cyberpunk city" --template scene | \
  gemini-nano-banana-tool generate -o city.png --stdin -a 16:9
```

**Available Templates**:
- `photography` - Technical camera details, lighting
- `character` - Pose, attire, expression
- `scene` - Foreground/midground/background
- `food` - Plating, garnish, lighting
- `abstract` - Shapes, colors, patterns
- `logo` - Typography, symbolism

### 2. Text-to-Image Generation

Generate images from prompts with flexible input:

```bash
# From positional argument
gemini-nano-banana-tool generate "A cat wearing a wizard hat" -o cat.png

# From file
gemini-nano-banana-tool generate -f prompt.txt -o output.png

# From stdin (piping)
echo "Beautiful sunset" | gemini-nano-banana-tool generate -o sunset.png -s
```

### 3. Image Editing with References

Edit existing images using natural language:

```bash
# Single reference
gemini-nano-banana-tool generate "Add a birthday hat" -o edited.png -i photo.jpg

# Multiple references (up to 3 for Flash, 14 for Pro)
gemini-nano-banana-tool generate "Combine these elements" -o result.png \
  -i ref1.jpg -i ref2.jpg -i ref3.jpg
```

### 4. Multi-Turn Conversations

Progressive image refinement across multiple turns:

```bash
# Turn 1: Initial image
gemini-nano-banana-tool generate-conversation \
  "Modern living room with large windows" \
  -o room-v1.png -f interior.json -a 16:9

# Turn 2: Add furniture (previous image auto-referenced)
gemini-nano-banana-tool generate-conversation \
  "Add gray sofa and wooden coffee table" \
  -o room-v2.png -f interior.json

# Turn 3: Adjust lighting
gemini-nano-banana-tool generate-conversation \
  "Make lighting warmer, add floor lamp" \
  -o room-v3.png -f interior.json
```

### 5. Aspect Ratios

10 supported aspect ratios for different platforms:

```bash
# Square (Instagram post)
gemini-nano-banana-tool generate "Design" -o square.png -a 1:1

# Widescreen (YouTube thumbnail)
gemini-nano-banana-tool generate "Scene" -o wide.png -a 16:9

# Vertical (Instagram story)
gemini-nano-banana-tool generate "Portrait" -o vertical.png -a 9:16

# Cinematic (ultra-wide)
gemini-nano-banana-tool generate "Panorama" -o cinema.png -a 21:9
```

**All Ratios**: 1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3, 21:9, 4:5, 5:4

### 6. Model Selection

Choose between Flash (fast, cost-effective) and Pro (high quality):

```bash
# Flash model (default) - Fast, cost-effective
gemini-nano-banana-tool generate "Prompt" -o output.png

# Pro model - Higher quality
gemini-nano-banana-tool generate "Prompt" -o output.png \
  -m gemini-3-pro-image-preview

# Pro with 4K resolution - Maximum quality
gemini-nano-banana-tool generate "Prompt" -o output.png \
  -m gemini-3-pro-image-preview -r 4K
```

### 7. Cost Tracking

Automatic cost calculation based on actual token usage:

```json
{
  "output_path": "output.png",
  "model": "gemini-2.5-flash-image",
  "token_count": 1295,
  "estimated_cost_usd": 0.0389,
  "resolution": "1344x768"
}
```

**Typical Costs**:
- Flash: ~$0.039 per image
- Pro 1K/2K: ~$0.134 per image
- Pro 4K: ~$0.24 per image

### 8. Verbosity Levels

Multi-level logging for debugging:

```bash
# Normal (warnings only)
gemini-nano-banana-tool generate "test" -o output.png

# Info (-v) - High-level operations
gemini-nano-banana-tool generate "test" -o output.png -v

# Debug (-vv) - Detailed validation
gemini-nano-banana-tool generate "test" -o output.png -vv

# Trace (-vvv) - Full HTTP logs
gemini-nano-banana-tool generate "test" -o output.png -vvv
```

## Authentication

### Gemini Developer API (Recommended)

```bash
export GEMINI_API_KEY='your-api-key'
```

Get API key: https://aistudio.google.com/app/apikey

### Vertex AI (Enterprise)

```bash
export GOOGLE_GENAI_USE_VERTEXAI=true
export GOOGLE_CLOUD_PROJECT='your-project-id'
export GOOGLE_CLOUD_LOCATION='us-central1'

# Authenticate
gcloud auth application-default login
```

## Common Workflows

### Workflow 1: Quick Generation

```bash
# Optimize prompt and generate in one pipeline
gemini-nano-banana-tool promptgen "wizard in magical library" | \
  gemini-nano-banana-tool generate -o wizard.png -s -a 16:9
```

### Workflow 2: Batch Processing

```bash
# Generate multiple variations
for style in "photorealistic" "artistic" "minimalist"; do
  gemini-nano-banana-tool generate \
    "A cat in $style style" \
    -o "cat-$style.png" \
    -a 1:1
done
```

### Workflow 3: Progressive Refinement

```bash
# Generate base image
gemini-nano-banana-tool generate "Product photo of headphones" \
  -o product-v1.png -a 1:1

# Refine with conversation mode
gemini-nano-banana-tool generate-conversation \
  "Rotate to show left side" \
  -o product-v2.png -f product.json

gemini-nano-banana-tool generate-conversation \
  "Change background to dark gradient" \
  -o product-v3.png -f product.json
```

### Workflow 4: Template-Based Generation

```bash
# Generate food photography
gemini-nano-banana-tool promptgen "pasta carbonara" --template food \
  -o pasta-prompt.txt

# Use saved prompt
gemini-nano-banana-tool generate -f pasta-prompt.txt \
  -o pasta.png -a 4:3

# Generate character design
gemini-nano-banana-tool promptgen "space explorer" --template character | \
  gemini-nano-banana-tool generate -o explorer.png -s -a 2:3
```

## Use Cases

### Content Creation

- Social media posts and stories
- Marketing materials and ads
- Blog post illustrations
- YouTube thumbnails

### E-commerce

- Product photography variations
- Lifestyle product shots
- Fashion combinations
- Product on model composites

### Design & Prototyping

- Concept art exploration
- UI/UX mockups
- Logo design iterations
- Brand visual exploration

### Professional Assets

- High-quality 4K renders
- Professional photography
- Print-ready materials
- Commercial content

## Output Format

All commands return structured JSON:

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

## Error Handling

The tool provides actionable error messages:

```bash
# Missing API key
Error: API key required. Set GEMINI_API_KEY or use --api-key option.
Get API key from https://aistudio.google.com/app/apikey

# Too many reference images
Error: Maximum 3 reference images allowed (Flash model).
Use Pro model for up to 14 reference images.

# Invalid aspect ratio
Error: Invalid aspect ratio '16:10'.
Use 'gemini-nano-banana-tool list-aspect-ratios' to see supported ratios.
```

## Shell Completion

Enable tab completion for faster usage:

```bash
# Bash
eval "$(gemini-nano-banana-tool completion bash)"

# Zsh
eval "$(gemini-nano-banana-tool completion zsh)"

# Fish
gemini-nano-banana-tool completion fish > \
  ~/.config/fish/completions/gemini-nano-banana-tool.fish
```

## Cost Optimization

### Choose the Right Model

**Use Flash for**:
- Prototyping and testing
- High-volume generation
- Cost-sensitive projects
- Quick iterations

**Use Pro for**:
- Final production images
- Complex scenes with detail
- Professional/commercial work
- Higher resolution needs

### Optimize Prompts

```bash
# Use promptgen to reduce trial-and-error
gemini-nano-banana-tool promptgen "your idea" --template photography \
  -o prompt.txt

# Reuse successful prompts
gemini-nano-banana-tool generate -f prompt.txt -o v1.png -a 1:1
gemini-nano-banana-tool generate -f prompt.txt -o v2.png -a 16:9
```

### Use Conversation Mode

```bash
# Refine instead of regenerating from scratch
gemini-nano-banana-tool generate-conversation \
  "Initial prompt" -o v1.png -f conv.json

gemini-nano-banana-tool generate-conversation \
  "Small adjustment" -o v2.png -f conv.json
```

## Library Usage

Import and use programmatically:

```python
from gemini_nano_banana_tool import create_client, generate_image, generate_prompt

# Create client (reuse for multiple operations)
client = create_client()

# Generate optimized prompt
prompt_result = generate_prompt(
    client=client,
    description="wizard cat",
    template="character"
)

# Generate image
image_result = generate_image(
    client=client,
    prompt=prompt_result['prompt'],
    output_path="wizard-cat.png",
    aspect_ratio="16:9"
)

print(f"Cost: ${image_result['estimated_cost_usd']:.4f}")
```

## Resources

- **Documentation**: README.md and CLAUDE.md in project root
- **API Setup**: references/api-setup-pricing.md
- **Prompting Guide**: references/prompting-guide.md (if available)
- **Examples**: references/examples.md (if available)
- **Official Gemini Docs**: https://ai.google.dev/gemini-api/docs/image-generation
- **API Key**: https://aistudio.google.com/app/apikey

## Installation

```bash
# Clone repository
git clone https://github.com/dnvriend/gemini-nano-banana-tool.git
cd gemini-nano-banana-tool

# Install with uv
uv tool install .

# Verify
gemini-nano-banana-tool --version
gemini-nano-banana-tool --help
```

## Support

For issues or questions:
- GitHub Issues: https://github.com/dnvriend/gemini-nano-banana-tool/issues
- Documentation: Check README.md and CLAUDE.md
- API Documentation: https://ai.google.dev/gemini-api/docs

---

**Generated with Claude Code**

This skill provides comprehensive access to Google Gemini's image generation capabilities through a professional, agent-friendly CLI with automatic cost tracking, AI prompt optimization, and multi-turn conversation support.
