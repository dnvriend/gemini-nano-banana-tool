# Gemini Nano Banana Tool - Reference Documentation

Comprehensive guides and references for Google Gemini image generation.

## Quick Start

**New to Gemini image generation?** Start here:
1. [Quick Reference](quick-reference.md) - One-page cheat sheet
2. [API Setup & Pricing](api-setup-pricing.md) - Get your API key and understand costs
3. [Prompting Guide](prompting-guide.md) - Learn to write effective prompts

## Documentation Index

### 1. Quick Reference (quick-reference.md)

**One-page cheat sheet for quick lookups**

Contents:
- Model comparison table (Flash vs Pro)
- Prompt formula
- Essential modifiers (quality, style, lighting)
- Text rendering tips
- Common issues and solutions
- CLI command examples
- Pricing summary

**Use this when**: You need a quick reminder or reference while working

### 2. API Setup & Pricing (api-setup-pricing.md)

**Complete guide to API setup and cost management**

Contents:
- Getting API keys (Developer API vs Vertex AI)
- Authentication methods
- Detailed pricing breakdown
- Rate limits and quotas
- Cost optimization strategies
- Billing setup
- Cost examples and scenarios

**Use this when**:
- Setting up for the first time
- Planning project budgets
- Understanding costs
- Troubleshooting authentication

### 3. Prompting Guide (prompting-guide.md)

**Comprehensive guide to writing effective prompts**

Contents:
- Model overview and differences
- Prompting best practices
- Text rendering techniques
- Reference image strategies
- Advanced prompting techniques
- Common issues and solutions
- Example prompts by use case
- Model selection guide

**Use this when**:
- Learning prompt engineering
- Improving image quality
- Troubleshooting generation issues
- Finding inspiration for prompts

## Model Comparison

| Feature | Flash (2.5) | Pro (3.0) |
|---------|-------------|-----------|
| **Model ID** | `gemini-2.5-flash-image` | `gemini-3-pro-image-preview` |
| **Speed** | Fast | Slower |
| **Quality** | Good | Excellent |
| **Reference Images** | 3 max | 6 max |
| **Cost** | $0.001-$0.01 | $0.01-$0.10 |
| **Best For** | Quick iterations | Professional work |

## Essential Links

### Official Google Resources
- **Main Docs**: https://ai.google.dev/gemini-api/docs/image-generation
- **AI Studio**: https://aistudio.google.com/ (Interactive testing)
- **Pricing**: https://ai.google.dev/pricing
- **API Reference**: https://ai.google.dev/api
- **Community**: https://discuss.ai.google.dev/

### Tool Resources
- **GitHub**: https://github.com/dnvriend/gemini-nano-banana-tool
- **PyPI**: https://pypi.org/project/gemini-nano-banana-tool/
- **CLI Help**: `gemini-nano-banana-tool --help`

## Quick CLI Examples

### Basic Generation
```bash
# Simple text-to-image
gemini-nano-banana-tool generate "a sunset over mountains" -o sunset.png

# With aspect ratio
gemini-nano-banana-tool generate "portrait of a cat" -o cat.png -a 9:16

# With reference images (up to 3 for Flash)
gemini-nano-banana-tool generate "landscape painting" -o art.png \
  -i style.jpg -i composition.jpg
```

### Advanced Usage
```bash
# From file
gemini-nano-banana-tool generate -f prompt.txt -o output.png

# From stdin
echo "beautiful garden" | gemini-nano-banana-tool generate -s -o garden.png

# Using Pro model
gemini-nano-banana-tool generate "complex scene" -o output.png \
  -m gemini-3-pro-image-preview

# With Vertex AI
gemini-nano-banana-tool generate "prompt" -o output.png \
  --use-vertex --project my-project --location us-central1
```

## Prompting Tips Summary

### Essential Formula
```
[Subject] + [Action] + [Setting] + [Style] + [Lighting] + [Technical]
```

### For Better Quality
```
Add: high resolution, detailed, sharp focus, 8k quality, professional
```

### For Text in Images
```
Format: [object] with text that says "[EXACT TEXT]" in [font style]
Example: A sign that says "OPEN" in bold red letters
```

### Common Fixes

| Problem | Solution |
|---------|----------|
| Blurry images | Add: `high resolution, sharp focus, detailed` |
| Wrong colors | Be specific: `bright cherry red` not `red` |
| Poor framing | Add: `wide angle, medium shot, aerial view` |
| Bad text | Keep short, use Pro model, specify font |
| Unexpected elements | Be explicit, use structured prompts |

## API Key Setup (Quick)

### Developer API (Recommended for Start)
```bash
# Get key from: https://aistudio.google.com/app/apikey
export GEMINI_API_KEY="your-api-key-here"

# Test
gemini-nano-banana-tool generate "test" -o test.png
```

### Vertex AI (Enterprise)
```bash
# Authenticate
gcloud auth application-default login

# Set variables
export GOOGLE_GENAI_USE_VERTEXAI=true
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_CLOUD_LOCATION="us-central1"

# Test
gemini-nano-banana-tool generate "test" -o test.png --use-vertex
```

## Pricing Quick Reference

### Free Tier
- ~15 requests per minute
- Suitable for development and testing
- No credit card required

### Paid Tier
| Usage | Flash Cost | Pro Cost |
|-------|------------|----------|
| 10 images | $0.01-$0.10 | $0.10-$1.00 |
| 100 images | $0.10-$1.00 | $1.00-$10.00 |
| 1,000 images | $1.00-$10.00 | $10.00-$100.00 |

**Note**: Approximate costs, verify at https://ai.google.dev/pricing

## Model Selection Guide

### Choose Flash (2.5) When:
- Speed is priority
- Cost-effectiveness matters
- Iterating on ideas quickly
- Simple to moderate complexity
- 3 or fewer reference images

### Choose Pro (3.0) When:
- Quality is paramount
- Complex scenes required
- Text accuracy is critical
- Need 4-6 reference images
- Professional/commercial projects

## Common Use Cases

### Product Photography
```bash
gemini-nano-banana-tool generate \
  "premium smartwatch on marble, studio lighting, white background, sharp focus, 8k" \
  -o product.png -a 1:1
```

### Social Media Content
```bash
gemini-nano-banana-tool generate \
  "motivational quote poster with text 'Dream Big' in bold font, inspirational background" \
  -o social.png -a 9:16
```

### Professional Headshots
```bash
gemini-nano-banana-tool generate \
  "professional headshot, 30s businesswoman, navy blazer, gray background, studio lighting" \
  -o headshot.png -a 4:5 -m gemini-3-pro-image-preview
```

### Artistic Creations
```bash
gemini-nano-banana-tool generate \
  "abstract art, flowing gold and blue swirls, high contrast, detailed" \
  -o art.png -a 16:9 -i style_reference.jpg
```

## Troubleshooting

### Authentication Errors
1. Check API key is set: `echo $GEMINI_API_KEY`
2. Verify key is valid in [AI Studio](https://aistudio.google.com/)
3. Check for typos in environment variable name

### Rate Limit Errors
1. Wait before retrying (15 RPM limit on free tier)
2. Upgrade to paid tier for higher limits
3. Implement retry logic with backoff

### Poor Image Quality
1. Add quality modifiers to prompt
2. Use Pro model for complex scenes
3. Test prompt in AI Studio first
4. Use reference images for style guidance

### Text Not Rendering
1. Keep text short (1-5 words)
2. Put exact text in quotes
3. Specify font style clearly
4. Consider Pro model for better accuracy

## Next Steps

1. **Get Started**: Follow [API Setup & Pricing](api-setup-pricing.md) to get your API key
2. **Learn Prompting**: Read [Prompting Guide](prompting-guide.md) for effective techniques
3. **Practice**: Test prompts in [Google AI Studio](https://aistudio.google.com/)
4. **Use the CLI**: Run `gemini-nano-banana-tool --help` for command reference
5. **Iterate**: Refine your prompts based on results

## Contributing

Found an issue or have improvements? Contributions welcome!

1. Check existing documentation
2. Test changes with real examples
3. Update relevant guides
4. Submit pull request

## Updates

This documentation is updated regularly as Google releases new features and models. Always verify:
- Current pricing at: https://ai.google.dev/pricing
- Latest models at: https://ai.google.dev/models
- API changes at: https://ai.google.dev/gemini-api/docs

---

**Last Updated**: 2025-11-20
**Tool Version**: gemini-nano-banana-tool v1.0.0+
**Google AI SDK**: google-genai

For the most up-to-date information, always refer to official Google AI documentation at https://ai.google.dev
