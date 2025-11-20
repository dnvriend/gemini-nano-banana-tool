# Gemini Image Generation - Quick Reference

A one-page reference for Google Gemini image generation.

## Models at a Glance

| Model | Speed | Quality | Ref Images | Cost | Use For |
|-------|-------|---------|------------|------|---------|
| **Flash 2.5** | Fast | Good | 3 max | $ | Quick iterations, prototyping |
| **Pro 3.0** | Slow | Excellent | 6 max | $$$ | Professional, complex scenes |

## Prompt Formula

```
[Subject] + [Action] + [Setting] + [Style] + [Lighting] + [Technical]
```

**Example**:
```
vintage bicycle + leaning against wall + Paris street + watercolor + warm afternoon + soft focus
```

## Essential Modifiers

### Quality
```
high resolution, detailed, sharp focus, 8k quality, professional
```

### Photography
```
portrait, landscape, macro, aerial, studio lighting, golden hour
```

### Art Styles
```
photorealistic, oil painting, watercolor, digital art, pencil sketch
```

### Mood/Lighting
```
dramatic, soft, warm, moody, cinematic, natural daylight
```

## Text in Images

**Format**: `[object] with text that says "[EXACT TEXT]" in [font style]`

**Examples**:
```
A sign that says "OPEN" in bold red letters
A book cover with title "The Journey" in elegant serif font
A cake with "Happy Birthday" in cursive frosting
```

**Tips**:
- Keep text short (1-5 words)
- Use quotes around exact text
- Specify font style
- Use Pro model for better accuracy

## Reference Images

**Flash (3 max)**: Style + Composition + Subject
**Pro (6 max)**: Multiple styles + Complex scenes

```bash
# With references
-i style.jpg -i composition.jpg -i subject.jpg
```

## Common Issues & Fixes

| Problem | Solution |
|---------|----------|
| Blurry | Add: `high resolution, sharp focus, detailed` |
| Wrong colors | Be specific: `bright cherry red` not just `red` |
| Bad composition | Add: `wide angle, medium shot, aerial view` |
| Failed text | Simplify text, use Pro model, add font style |
| Unexpected elements | Be explicit, use structured prompting |

## CLI Commands

```bash
# Basic
gemini-nano-banana-tool generate "prompt" -o output.png

# With aspect ratio
-a 16:9

# With references (max 3 for Flash, 6 for Pro)
-i ref1.jpg -i ref2.jpg -i ref3.jpg

# Use Pro model
-m gemini-3-pro-image-preview

# From file
-f prompt.txt

# From stdin
echo "prompt" | gemini-nano-banana-tool generate -s -o out.png
```

## Pricing (Approximate)

| Tier | Flash 2.5 | Pro 3.0 |
|------|-----------|---------|
| **Free** | ~15/min | ~15/min |
| **Paid** | $0.001-$0.01 | $0.01-$0.10 |

Verify at: https://ai.google.dev/pricing

## Aspect Ratios

```
1:1    (1024×1024)  Square, social media
16:9   (1344×768)   Widescreen, desktop
9:16   (768×1344)   Mobile, portrait
4:3    (1024×768)   Traditional photo
3:4    (768×1024)   Portrait photo
```

## Example Prompts

**Product**:
```
Premium smartwatch on marble, studio lighting, white background, sharp focus, 8k
```

**Portrait**:
```
Professional headshot, 30s businesswoman, navy blazer, gray background, studio lighting
```

**Landscape**:
```
Mountain lake at sunset, snow-capped peaks, orange sky, pine tree foreground, photorealistic
```

**Text Design**:
```
Vintage poster with "VISIT TOKYO" in art deco font, Mount Fuji background, 1950s style
```

## When to Use Each Model

**Flash 2.5**:
- Speed matters
- Lower cost needed
- Simple/moderate scenes
- Quick prototyping

**Pro 3.0**:
- Quality critical
- Complex scenes
- Accurate text needed
- Professional work

## Resources

- **Docs**: https://ai.google.dev/gemini-api/docs/image-generation
- **Studio**: https://aistudio.google.com/
- **Pricing**: https://ai.google.dev/pricing
- **API**: https://ai.google.dev/api

## Pro Tips

1. **Specificity > Length**: Detailed beats long
2. **Iterate**: Refine prompts based on results
3. **References Help**: Especially for style consistency
4. **Structure**: Use the formula above
5. **Test in Studio**: Try prompts interactively first

---

**Tool**: gemini-nano-banana-tool
**Updated**: 2025-11-20
