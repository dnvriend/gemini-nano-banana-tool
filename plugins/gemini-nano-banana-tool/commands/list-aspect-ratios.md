# List Aspect Ratios Command

List supported aspect ratios with resolutions and use cases.

## Usage

```bash
gemini-nano-banana-tool list-aspect-ratios
```

## Output

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

## Usage with Generate Command

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

## Common Platform Aspect Ratios

### Social Media

- **Instagram Post**: 1:1 (square)
- **Instagram Story**: 9:16 (vertical)
- **Instagram Portrait**: 4:5
- **Twitter Post**: 16:9 or 1:1
- **Facebook Post**: 1:1 or 16:9
- **LinkedIn Post**: 1:1 or 16:9

### Video Platforms

- **YouTube Thumbnail**: 16:9
- **YouTube Banner**: 16:9 (wide)
- **TikTok**: 9:16 (vertical)
- **YouTube Shorts**: 9:16 (vertical)

### Photography

- **DSLR Standard**: 3:2
- **Medium Format**: 5:4
- **Classic Film**: 4:3
- **Portrait**: 2:3 or 3:4

### Displays

- **Desktop/Laptop**: 16:9
- **Ultrawide Monitor**: 21:9
- **Mobile Portrait**: 9:16
- **Tablet**: 4:3

## Choosing an Aspect Ratio

**For social media content:**
- Use 1:1 for maximum compatibility
- Use 9:16 for stories and vertical video
- Use 4:5 for Instagram portrait posts

**For professional photography:**
- Use 3:2 for DSLR standard
- Use 5:4 for medium format look
- Use 2:3 for traditional portrait

**For video/cinema:**
- Use 16:9 for standard widescreen
- Use 21:9 for cinematic ultra-wide
- Use 9:16 for vertical mobile video

**For presentations/displays:**
- Use 16:9 for modern displays
- Use 4:3 for traditional presentations
