# Gemini Image Generation Prompting Guide

A comprehensive guide to writing effective prompts for Google Gemini image generation models.

## Table of Contents

- [Model Overview](#model-overview)
- [Official Documentation](#official-documentation)
- [Prompting Best Practices](#prompting-best-practices)
- [Text in Images](#text-in-images)
- [Reference Images](#reference-images)
- [Pricing Information](#pricing-information)
- [Advanced Techniques](#advanced-techniques)
- [Common Issues](#common-issues)
- [Example Prompts](#example-prompts)

## Model Overview

### Gemini 2.5 Flash Image (Nano Banana)

- **Model ID**: `gemini-2.5-flash-image`
- **Speed**: Fast generation (seconds)
- **Reference Images**: Up to 3 images
- **Quality**: Good
- **Cost**: Lower ($0.001-$0.01 per image approx.)
- **Best For**: Quick iterations, prototyping, cost-effective production

### Gemini 3 Pro Image Preview (Nano Banana 2)

- **Model ID**: `gemini-3-pro-image-preview`
- **Speed**: Slower (better quality)
- **Reference Images**: Up to 6 images
- **Quality**: Excellent
- **Cost**: Higher ($0.01-$0.10 per image approx.)
- **Best For**: High-quality outputs, complex compositions, professional work

### Key Differences

| Feature | Flash (2.5) | Pro (3.0) |
|---------|-------------|-----------|
| Speed | Fast | Slower |
| Quality | Good | Excellent |
| Reference Images | 3 max | 6 max |
| Cost | Lower | Higher |
| Text Rendering | Good | Better |
| Complex Scenes | Good | Excellent |

## Official Documentation

1. **Image Generation Guide**: https://ai.google.dev/gemini-api/docs/image-generation
2. **Prompting Guide**: https://ai.google.dev/gemini-api/docs/prompting-guide
3. **API Reference**: https://ai.google.dev/api
4. **Pricing**: https://ai.google.dev/pricing
5. **Google AI Studio**: https://aistudio.google.com/

## Prompting Best Practices

### General Guidelines

**1. Be Specific and Descriptive**

- Include detailed descriptions of subjects, settings, and style
- Specify lighting, mood, atmosphere, and composition
- Mention colors, textures, and materials

**Bad**: `a cat`
**Good**: `a fluffy orange tabby cat with green eyes, sitting on a windowsill, soft natural lighting, photorealistic`

**2. Structure Your Prompts**

Use this formula:
```
[Subject] + [Action/Pose] + [Setting/Background] + [Style] + [Lighting/Mood] + [Technical Details]
```

**Example**:
```
A vintage red bicycle [subject]
leaning against a wall [action/pose]
on a cobblestone street in Paris [setting]
watercolor painting style [style]
warm afternoon light [lighting]
soft focus, artistic [technical details]
```

**3. Use Clear, Concrete Language**

- Avoid ambiguous terms
- Use concrete nouns and active verbs
- Specify quantities and positions
- Include camera angles and perspectives

**Vague**: `nice looking food`
**Clear**: `a gourmet burger with melted cheese, fresh lettuce, and tomato on a wooden board, top-down view, restaurant food photography`

**4. Style and Artistic Direction**

Mention specific styles:
- **Art styles**: photorealistic, oil painting, digital art, watercolor, pencil sketch
- **Movements**: impressionist, art nouveau, minimalist, surrealist
- **Photography**: portrait, landscape, macro, aerial, long exposure
- **Era/Culture**: Victorian, Art Deco, Japanese, Nordic minimalist

## Text in Images

### Challenge

AI models often struggle with accurate text rendering. Text may appear garbled, misspelled, or illegible.

### Best Practices for Text

1. **Be Explicit**: State exactly what the text should say
   ```
   A sign that says "OPEN 24/7" in bold red letters
   ```

2. **Specify Font Style**
   ```
   handwritten text, modern sans-serif font, elegant script, bold block letters
   ```

3. **Specify Placement**
   ```
   text centered at the top, sign on the wall reading, label at the bottom
   ```

4. **Keep It Short**
   - Shorter text (1-5 words) renders more accurately
   - Avoid complex sentences or paragraphs

5. **Use Quotes**
   - Always put exact text in quotes: `"HELLO"`

6. **Iterative Approach**
   - Generate, review, refine prompt
   - Consider using Pro model for better text accuracy

### Example Text Prompts

**Coffee Shop Sign**:
```
A coffee shop storefront with a sign that says "BREW HAVEN" in vintage gold lettering, warm lighting, photorealistic
```

**Motivational Poster**:
```
A motivational poster with bold text reading "DREAM BIG" at the top, inspirational mountain landscape background, modern design
```

**Birthday Cake**:
```
A chocolate birthday cake with "Happy Birthday Sarah" written in elegant white cursive frosting on top, professional food photography
```

**Book Cover**:
```
A book cover design with the title "The Last Journey" in bold serif font at the top, author name "John Smith" at the bottom, fantasy landscape background, professional book design
```

## Reference Images

Reference images guide the style, composition, or subject matter of generated images.

### Flash Model (3 Images Max)

Use for:
- **Style Transfer**: Show desired artistic style
- **Composition Guide**: Demonstrate layout/arrangement
- **Subject Reference**: Show specific objects/characters

### Pro Model (6 Images Max)

All Flash uses plus:
- **Multiple Style Influences**: Combine different artistic styles
- **Complex Scene References**: Multiple scene elements
- **Detailed Element References**: Specific textures, patterns, details

### Tips for Reference Images

1. **Use High-Quality Images**: Clear, well-lit, high-resolution
2. **Ensure Alignment**: References should support (not contradict) text prompt
3. **Order Matters**: First image often has strongest influence
4. **Strategic Combination**: Mix style + composition + subject references

### Example Usage

```bash
# Single style reference
gemini-nano-banana-tool generate \
  "A mountain landscape" \
  -o output.png \
  -i style_reference.jpg

# Multiple references (style + composition)
gemini-nano-banana-tool generate \
  "A fantasy castle at sunset" \
  -o output.png \
  -i art_style.jpg \
  -i composition_ref.jpg \
  -i color_palette.jpg
```

## Pricing Information

### Free Tier

- **Rate Limits**: ~15 requests per minute
- **Daily Limits**: Check https://ai.google.dev/pricing for current limits
- **Best For**: Development, testing, small projects

### Paid Tier

**Gemini 2.5 Flash Image**:
- Cost: ~$0.001-$0.01 per image (approximate)
- Fast generation
- Good quality
- Lower cost for high volume

**Gemini 3 Pro Image**:
- Cost: ~$0.01-$0.10 per image (approximate)
- Excellent quality
- Better text rendering
- Supports more reference images

**Note**: Pricing subject to change. Verify at https://ai.google.dev/pricing

## Advanced Techniques

### 1. Compositional Prompting

Break down the scene into layers:

```
Foreground: a wooden fence with wildflowers
Midground: a red barn with white trim
Background: rolling green hills and blue sky
Overall mood: peaceful summer afternoon, golden hour lighting
```

### 2. Style Stacking

Combine multiple style descriptors:

```
Primary style: photorealistic portrait
Secondary influence: cinematic lighting like a movie poster
Color grading: warm golden hour tones with deep shadows
Technical: shallow depth of field, 85mm lens, f/1.8
```

### 3. Negative Prompting

Specify what to avoid (if supported by model):

```
A serene forest landscape (avoid: people, buildings, vehicles, modern elements)
```

### 4. Iterative Refinement

**Process**:
1. Start with basic prompt
2. Generate and review result
3. Identify what needs adjustment
4. Add specific details to address issues
5. Re-generate with refined prompt

**Example Progression**:
```
v1: "a robot"
v2: "a friendly robot with round features, cartoon style"
v3: "a friendly robot with round features and big expressive eyes, cartoon style like Pixar, bright colors"
v4: "a friendly robot with round features and big expressive eyes, cartoon style like Pixar, bright blue and white colors, standing in a futuristic lab, soft lighting"
```

## Common Issues

### Issue: Blurry or Low Quality

**Solution**: Add quality modifiers
```
high resolution, detailed, sharp focus, 8k quality, crisp, professional photography
```

### Issue: Wrong Colors

**Solution**: Be very specific with color names
```
Bad:  "red car"
Good: "bright cherry red car" or "deep burgundy red car"
```

### Issue: Poor Composition

**Solution**: Specify camera angle and framing
```
medium shot, wide angle, aerial view, close-up portrait, bird's eye view, low angle
```

### Issue: Text Rendering Fails

**Solution**:
- Simplify the text (fewer words)
- Make text more prominent in prompt
- Specify font style clearly
- Use reference images with text examples
- Switch to Pro model for better accuracy

### Issue: Unexpected Elements

**Solution**:
- Be more explicit about what should/shouldn't appear
- Use structured prompting format
- Add context to eliminate ambiguity
- Specify "only" or "nothing else but" for minimal scenes

### Issue: Inconsistent Style

**Solution**:
- Use reference images to anchor style
- Be specific about art medium
- Add era/movement descriptors
- Use "in the style of [artist/movement]"

## Example Prompts

### Product Photography

```
A premium smartwatch on a marble surface, studio lighting, commercial photography style, clean white background, sharp focus, product shot, 8k resolution
```

### Character Art

```
A young warrior woman with braided red hair, wearing silver armor with intricate engravings, confident expression, fantasy art style, dramatic lighting from the left, detailed background of a medieval castle, digital painting, detailed
```

### Landscape

```
A serene mountain lake at sunset, snow-capped peaks reflecting in still water, vibrant orange and pink sky, lone pine tree in foreground, photorealistic, wide angle landscape photography, golden hour lighting, sharp focus
```

### Interior Design

```
A modern minimalist living room with floor-to-ceiling windows, Scandinavian design, light wood floors, white walls, gray sofa, indoor plants, natural daylight, architectural photography, clean and bright
```

### Food Photography

```
A rustic Italian pizza with fresh basil, mozzarella, and tomatoes, wood-fired crust, served on a wooden board, restaurant lighting, food photography, overhead shot, shallow depth of field, appetizing
```

### Text-Heavy Design

```
A vintage travel poster with text "VISIT TOKYO" in bold art deco lettering at the top, Mount Fuji in background, cherry blossoms in foreground, 1950s poster art style, limited color palette of red, blue, and cream
```

### Abstract Art

```
Flowing liquid gold and deep blue swirls mixing together, abstract expressionism, dynamic movement, high contrast, macro photography style, dramatic lighting, textured surface, 8k resolution
```

### Portrait Photography

```
Professional headshot of a smiling businesswoman in her 30s, wearing a navy blue blazer, neutral gray background, studio lighting with soft box, sharp focus on eyes, corporate photography style, confident expression
```

## Model Selection Guide

### Choose Flash (2.5) When:

- Speed is priority
- Cost-effectiveness matters
- Iterating quickly on multiple ideas
- Simple to moderate complexity scenes
- Up to 3 reference images sufficient
- Prototyping or testing concepts

### Choose Pro (3.0) When:

- Quality is paramount
- Complex scenes with many elements
- Text accuracy is critical
- Need 4-6 reference images
- Professional/commercial projects
- Complex lighting or special effects required
- Photorealistic detail needed

## CLI Integration

### Basic Usage

```bash
# Simple generation
gemini-nano-banana-tool generate "a sunset over mountains" -o sunset.png

# With aspect ratio
gemini-nano-banana-tool generate "portrait of a cat" -o cat.png -a 9:16

# With reference images
gemini-nano-banana-tool generate "landscape painting" -o art.png \
  -i style_ref.jpg -i composition_ref.jpg

# Using Pro model
gemini-nano-banana-tool generate "complex scene with text" -o output.png \
  -m gemini-3-pro-image-preview
```

### From File

```bash
# Read prompt from file
gemini-nano-banana-tool generate -f prompt.txt -o output.png

# From stdin
echo "a beautiful garden" | gemini-nano-banana-tool generate -s -o garden.png
```

## Resources

1. **Official Docs**: https://ai.google.dev/gemini-api/docs
2. **AI Studio** (Interactive testing): https://aistudio.google.com/
3. **API Reference**: https://ai.google.dev/api
4. **Pricing**: https://ai.google.dev/pricing
5. **Community**: https://discuss.ai.google.dev/
6. **GitHub**: https://github.com/google-gemini/

## Key Takeaways

1. **Specificity Wins**: More detailed prompts produce better results
2. **Text is Challenging**: Requires extra attention and possibly Pro model
3. **Reference Images Help**: Especially for style and composition consistency
4. **Iterate**: First result is rarely perfect, refine your prompt
5. **Model Choice Matters**: Flash for speed/cost, Pro for quality/complexity
6. **Structure Helps**: Organized prompts produce consistent results
7. **Read Official Docs**: Google's documentation is comprehensive and regularly updated

---

**Last Updated**: 2025-11-20
**Sources**: Google AI Developer Documentation, Google AI Studio
**Tool**: gemini-nano-banana-tool

Note: Pricing and model specifications are subject to change. Always verify current details at official Google AI documentation (https://ai.google.dev).
