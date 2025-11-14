# Prompt Engineering Guide for Nano Banana

This guide provides strategies and best practices for crafting effective prompts with Gemini 2.5 Flash Image (Nano Banana).

**Reference Guide**: [Prompt Engineering for Gemini 2.5 Flash Image (AI SuperHub)](https://aisuperhub.io/blog/prompt-engineering-for-gemini-25-flash-image-nano-banana-50plus-image-prompts-included)

## Core Prompting Principles

### 1. Be Specific and Descriptive

**Good:**
```
"Create a photorealistic image of a nano banana dish served on a white porcelain plate, 
with elegant garnishes and soft restaurant lighting, in a modern minimalist style"
```

**Less Effective:**
```
"Make a food picture"
```

### 2. Include Style and Mood

Specify the desired artistic style, mood, and atmosphere:

- **Artistic Styles**: watercolor, oil painting, digital art, sketch, anime, photorealistic
- **Moods**: serene, dramatic, energetic, mysterious, warm, cool
- **Lighting**: golden hour, soft lighting, dramatic shadows, neon lights

**Example:**
```
"A cyberpunk cityscape at night with neon lights reflecting in puddles, 
in a futuristic digital art style with vibrant colors and dramatic contrast"
```

### 3. Describe Composition and Perspective

Guide the composition of your image:

- **Camera angles**: bird's eye view, close-up, wide angle, side view
- **Composition**: centered, rule of thirds, symmetrical, dynamic
- **Depth**: foreground, midground, background elements

**Example:**
```
"Wide-angle shot of a nano banana dish in the foreground, 
with a blurred restaurant interior in the background, 
using shallow depth of field"
```

### 4. Specify Colors and Palette

Be explicit about color choices:

```
"A nano banana dish with warm earth tones - golden yellows, 
soft browns, and cream whites, with a complementary blue accent"
```

### 5. Include Technical Details

For high-quality results, include technical specifications:

- Resolution preferences (handled via aspect ratio in config)
- Detail level: "highly detailed", "intricate", "minimalist"
- Texture: "smooth", "textured", "glossy", "matte"

## Prompt Categories and Examples

### Photography and Realism

```
"Professional food photography of a nano banana dish, 
shot with a macro lens, soft natural lighting from a window, 
shallow depth of field, high detail, restaurant setting"
```

```
"Photorealistic portrait of a character in cyberpunk attire, 
neon-lit urban background, bokeh effect, cinematic lighting, 
8k quality"
```

### Artistic Styles

```
"Watercolor painting of a nano banana dish, soft pastel colors, 
loose brushstrokes, artistic impressionist style, on textured paper"
```

```
"Digital art illustration in anime style, vibrant colors, 
clean line art, cell shading, character design with nano banana theme"
```

### Abstract and Conceptual

```
"Abstract composition featuring nano banana motifs, 
geometric shapes, bold colors, minimalist design, 
modern art style"
```

```
"Conceptual art piece representing the fusion of nature and technology, 
with nano banana elements as a central theme, surrealist style"
```

### Character Design

```
"Character design for a cyberpunk chef specializing in nano banana cuisine, 
wearing futuristic kitchen attire, detailed accessories, 
consistent character style, front view"
```

### Scene Composition

```
"A bustling futuristic restaurant kitchen, with nano banana dishes being prepared, 
multiple chefs in action, steam and warm lighting, 
wide-angle perspective, detailed environment"
```

### Logo and Typography

```
"Logo design featuring 'Nano Banana' text, modern typography, 
geometric shapes, clean minimalist style, suitable for restaurant branding, 
high contrast for visibility"
```

## Advanced Prompting Techniques

### 1. Multi-Element Descriptions

Break down complex scenes into components:

```
"Scene composition: 
- Foreground: A beautifully plated nano banana dish on a dark wood table
- Midground: Soft candlelight and elegant table settings
- Background: Blurred view of a sophisticated restaurant interior
- Lighting: Warm, intimate, golden hour atmosphere
- Style: Fine dining photography, professional quality"
```

### 2. Iterative Prompt Refinement

Start broad, then refine:

**First prompt:**
```
"A nano banana dish"
```

**Refined:**
```
"A gourmet nano banana dish served in a fine dining restaurant, 
with artistic plating, garnishes, and professional photography lighting"
```

**Further refined:**
```
"Photorealistic image of a gourmet nano banana dish on white porcelain, 
with microgreens and edible flowers as garnish, soft directional lighting 
creating subtle shadows, shallow depth of field, restaurant ambiance in background, 
fine dining photography style"
```

### 3. Negative Prompts (What to Avoid)

While Nano Banana doesn't explicitly support negative prompts like some models, you can guide away from unwanted elements:

```
"Create a nano banana dish, but avoid heavy shadows or cluttered backgrounds, 
focus on clean presentation"
```

### 4. Reference-Based Prompting

When using reference images, complement them with descriptive text:

```
"Using the style from the reference image, create a new nano banana dish 
with similar artistic approach, color palette, and composition style"
```

### 5. Consistency Prompts

For character consistency across multiple images:

```
"Generate this same character in a new scene. Maintain exact facial features, 
clothing design, and color scheme from the reference"
```

## Prompt Templates

### Food Photography Template

```
"[Style] photography of [dish description], [plating style], 
[lighting description], [background/mood], [technical details]"
```

### Character Design Template

```
"[Style] character design: [description], [clothing/attire], 
[pose/viewpoint], [setting/mood], [technical details]"
```

### Scene Composition Template

```
"[Style] scene: [main subject], [foreground elements], 
[midground elements], [background elements], [lighting/atmosphere], 
[perspective/composition], [technical details]"
```

## Common Prompt Patterns (50+ Examples)

### Food & Culinary
1. "Gourmet nano banana dessert plated on black slate, minimalist presentation"
2. "Macro photography of nano banana texture, detailed surface, soft lighting"
3. "Restaurant menu photo of nano banana dish, professional food styling"
4. "Aerial view of nano banana platter, overhead lighting, vibrant colors"
5. "Fine dining presentation of nano banana, elegant garnishes, white background"

### Characters & Portraits
6. "Cyberpunk character portrait, neon city background, detailed facial features"
7. "Fantasy character design, medieval style, detailed costume, full body view"
8. "Anime-style character, vibrant colors, expressive eyes, standing pose"
9. "Realistic portrait photography, natural lighting, professional headshot style"
10. "Character concept art, three-quarter view, detailed clothing design"

### Environments & Scenes
11. "Futuristic cityscape at sunset, neon signs, rain-slicked streets"
12. "Interior design: modern minimalist restaurant, warm lighting, nano banana theme"
13. "Nature scene: tropical forest, dappled sunlight, vibrant flora"
14. "Urban street scene, bustling atmosphere, golden hour lighting"
15. "Abstract space environment, cosmic colors, ethereal atmosphere"

### Abstract & Artistic
16. "Abstract geometric composition, bold primary colors, minimalist style"
17. "Surrealist artwork, dreamlike atmosphere, impossible perspectives"
18. "Impressionist painting style, soft brushstrokes, natural color palette"
19. "Digital art illustration, vibrant gradients, modern aesthetic"
20. "Minimalist line art, monochrome, elegant simplicity"

### Technical & Detailed
21. "Technical diagram, labeled components, clean line art style"
22. "Infographic design, data visualization, modern flat design"
23. "Blueprint style, technical drawings, architectural precision"
24. "Scientific illustration, detailed cross-section, educational style"
25. "Product design sketch, multiple views, professional presentation"

And many more variations based on combining these elements...

## Prompt Engineering Workflow

### Step 1: Initial Prompt
Start with a basic description of what you want.

### Step 2: Add Style
Specify the artistic style or photographic approach.

### Step 3: Refine Details
Add specific details about composition, lighting, colors.

### Step 4: Iterate Based on Results
Review the generated image and refine the prompt for better results.

### Step 5: Use References
If needed, add reference images to guide style or consistency.

## Best Practices Summary

1. ✅ **Be specific** - Include details about style, mood, composition
2. ✅ **Use descriptive language** - Paint a clear picture with words
3. ✅ **Specify technical aspects** - Lighting, perspective, quality level
4. ✅ **Iterate and refine** - Build on initial results
5. ✅ **Combine text and images** - Use reference images when helpful
6. ✅ **Test variations** - Try different phrasings and styles
7. ✅ **Consider the use case** - Tailor prompts to intended purpose

## What to Avoid

1. ❌ **Overly vague prompts** - "Make something cool"
2. ❌ **Contradictory instructions** - Mixing incompatible styles
3. ❌ **Assuming context** - The model needs explicit guidance
4. ❌ **Single-word prompts** - Insufficient detail for good results
5. ❌ **Ignoring iterations** - Not refining based on initial results

## References

- [AI SuperHub - Prompt Engineering Guide](https://aisuperhub.io/blog/prompt-engineering-for-gemini-25-flash-image-nano-banana-50plus-image-prompts-included)
- [Gemini API Documentation](https://ai.google.dev/gemini-api/docs/image-generation#go)
- [Google Developers Blog - Gemini 2.5 Flash Image](https://developers.googleblog.com/en/introducing-gemini-2-5-flash-image/)

