"""Prompt templates for different image generation categories.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from typing import Final

# Template definitions based on prompting guide best practices
TEMPLATES: Final[dict[str, str]] = {
    "photography": """Transform this into a professional photography prompt with:
- Photographic style (portrait, landscape, macro, etc.)
- Camera/lens details (if relevant)
- Lighting description (natural, studio, golden hour, etc.)
- Depth of field and focus details
- Technical quality indicators (sharp, detailed, high resolution)
- Mood and atmosphere
- Background and setting

Example format: "Professional [style] photography of [subject], shot with [lens details],
[lighting description], [depth of field], [mood/atmosphere], [technical quality]"
""",
    "character": """Transform this into a character design prompt with:
- Character description (physical features, expression)
- Clothing and accessories details
- Art style (anime, realistic, cartoon, concept art, etc.)
- Pose and viewpoint (front view, three-quarter, full body, etc.)
- Setting or background context
- Color palette and mood
- Technical details (clean lines, detailed rendering, etc.)

Example format: "[Art style] character design of [description], wearing [clothing],
[pose/viewpoint], [setting], [color palette], [technical details]"
""",
    "scene": """Transform this into a scene composition prompt with:
- Scene overview and main subject
- Foreground elements (what's closest to viewer)
- Midground elements (middle distance)
- Background elements (distant/backdrop)
- Lighting and atmosphere (time of day, weather, mood)
- Perspective and composition (wide angle, aerial view, etc.)
- Style and technical quality

Example format: "[Style] scene composition: [main subject],
Foreground: [elements], Midground: [elements], Background: [elements],
[lighting/atmosphere], [perspective], [technical details]"
""",
    "food": """Transform this into a food photography prompt with:
- Dish description and ingredients
- Plating style (minimalist, elaborate, rustic, etc.)
- Serving presentation (plate type, garnishes, accompaniments)
- Lighting (natural window light, soft studio, dramatic, etc.)
- Camera angle (overhead, 45-degree, close-up, etc.)
- Background and setting (restaurant, kitchen, table setting)
- Mood and atmosphere (elegant, casual, vibrant, etc.)
- Technical quality (sharp focus, shallow depth of field, etc.)

Example format: "Professional food photography of [dish], [plating style],
[camera angle], [lighting], [background/setting], [mood], [technical details]"
""",
    "abstract": """Transform this into an abstract art prompt with:
- Concept or theme
- Geometric shapes or organic forms
- Color palette (bold, pastel, monochrome, etc.)
- Composition style (symmetrical, dynamic, minimalist, etc.)
- Art movement or style (modernist, surrealist, minimalist, etc.)
- Texture and patterns
- Mood and emotional impact

Example format: "Abstract [style] composition featuring [concept],
[shapes/forms], [color palette], [composition style], [texture/patterns],
[mood/atmosphere]"
""",
    "logo": """Transform this into a logo design prompt with:
- Brand name or text (if applicable)
- Logo type (wordmark, symbol, combination, etc.)
- Design style (modern, minimalist, vintage, tech, organic, etc.)
- Geometric elements or shapes
- Color scheme and contrast
- Typography style (if text is included)
- Use case or purpose (app icon, business card, signage, etc.)
- Technical requirements (scalable, high contrast, clean lines)

Example format: "Logo design for [brand/purpose], [logo type], [design style],
featuring [elements], [color scheme], [typography], [technical requirements]"
""",
}

# Template descriptions for CLI help
TEMPLATE_DESCRIPTIONS: Final[dict[str, str]] = {
    "photography": "Professional photography with camera, lighting, and technical details",
    "character": "Character design with pose, attire, and style specifications",
    "scene": "Scene composition with foreground, midground, background layers",
    "food": "Food photography with plating, lighting, and presentation details",
    "abstract": "Abstract art with shapes, colors, and composition style",
    "logo": "Logo design with typography, shapes, and branding elements",
}

# Category keywords for auto-detection
CATEGORY_KEYWORDS: Final[dict[str, list[str]]] = {
    "photography": [
        "photo",
        "photograph",
        "portrait",
        "landscape",
        "macro",
        "shot",
        "camera",
    ],
    "character": [
        "character",
        "person",
        "hero",
        "villain",
        "avatar",
        "portrait",
        "figure",
    ],
    "scene": [
        "scene",
        "environment",
        "landscape",
        "cityscape",
        "interior",
        "setting",
        "location",
    ],
    "food": [
        "food",
        "dish",
        "meal",
        "cuisine",
        "plate",
        "dessert",
        "recipe",
    ],
    "abstract": [
        "abstract",
        "geometric",
        "pattern",
        "composition",
        "shapes",
        "design",
    ],
    "logo": [
        "logo",
        "brand",
        "icon",
        "emblem",
        "symbol",
        "wordmark",
    ],
}


def get_template(template_name: str) -> str:
    """Get template instructions by name.

    Args:
        template_name: Name of the template (photography, character, scene, food, abstract, logo)

    Returns:
        Template instructions string

    Raises:
        ValueError: If template name is not recognized
    """
    if template_name not in TEMPLATES:
        available = ", ".join(TEMPLATES.keys())
        raise ValueError(
            f"Unknown template: {template_name}. Available templates: {available}"
        )
    return TEMPLATES[template_name]


def detect_category(description: str) -> str | None:
    """Auto-detect category from description using keyword matching.

    Args:
        description: User's simple description

    Returns:
        Detected category name or None if no match

    Example:
        >>> detect_category("a character in armor")
        'character'
        >>> detect_category("food on a plate")
        'food'
    """
    description_lower = description.lower()

    # Count keyword matches for each category
    scores: dict[str, int] = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword in description_lower)
        if score > 0:
            scores[category] = score

    # Return category with highest score
    if scores:
        return max(scores, key=scores.get)  # type: ignore[arg-type]

    return None


def list_templates() -> list[tuple[str, str]]:
    """Get list of available templates with descriptions.

    Returns:
        List of (template_name, description) tuples

    Example:
        >>> templates = list_templates()
        >>> templates[0]
        ('photography', 'Professional photography with camera...')
    """
    return [(name, TEMPLATE_DESCRIPTIONS[name]) for name in TEMPLATES.keys()]
