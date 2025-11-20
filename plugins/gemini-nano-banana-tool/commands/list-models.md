# List Models Command

List available Gemini image generation models with descriptions.

## Usage

```bash
gemini-nano-banana-tool list-models
```

## Output

```
Available Gemini Image Generation Models:
  • gemini-2.5-flash-image (default) - Fast, high-quality image generation
  • gemini-3-pro-image-preview - Advanced model with higher quality and more features
```

## Model Details

### Flash Model (gemini-2.5-flash-image)

**Default Model**

- **Speed**: Fast (seconds per image)
- **Quality**: High quality
- **Resolution**: Fixed ~1024p
- **Cost**: $0.00003 per token (~$0.039 per image)
- **Reference Images**: Up to 3
- **Best For**: Quick iterations, cost-effective production, high-volume generation

### Pro Model (gemini-3-pro-image-preview)

**Advanced Model**

- **Speed**: Slower (better quality)
- **Quality**: Maximum quality
- **Resolution**: Variable (1K/2K/4K)
- **Cost**: $0.00012 per token (~$0.134-0.24 per image)
- **Reference Images**: Up to 14
- **Best For**: Professional assets, high-quality requirements, complex scenes

## Usage with Generate Command

```bash
# Default Flash model
gemini-nano-banana-tool generate "Your prompt" -o output.png

# Pro model
gemini-nano-banana-tool generate "Your prompt" -o output.png \
  -m gemini-3-pro-image-preview

# Pro model with 4K resolution
gemini-nano-banana-tool generate "Your prompt" -o output.png \
  -m gemini-3-pro-image-preview -r 4K
```

## Cost Comparison

| Model | Typical Cost | Speed | Quality | Resolution |
|-------|-------------|-------|---------|------------|
| Flash | $0.039 | Fast | High | Fixed ~1024p |
| Pro 1K/2K | $0.134 | Medium | Higher | 1K-2K |
| Pro 4K | $0.24 | Slower | Maximum | Up to 4K |

## Choosing a Model

**Use Flash when:**
- Prototyping and testing
- High-volume generation
- Cost is a concern
- Speed matters

**Use Pro when:**
- Final production images
- Complex scenes with fine details
- Higher resolution needed
- Professional/commercial work
