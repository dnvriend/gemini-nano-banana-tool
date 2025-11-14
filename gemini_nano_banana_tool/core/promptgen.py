"""Prompt generation for image creation using LLM enhancement.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from typing import Any

from google import genai
from google.genai import types

from .prompt_templates import detect_category, get_template


class PromptGenerationError(Exception):
    """Raised when prompt generation fails."""


def generate_prompt(
    client: genai.Client,
    description: str,
    template: str | None = None,
    category: str | None = None,
    style: str | None = None,
    model: str = "gemini-2.0-flash-exp",
) -> dict[str, Any]:
    """Generate detailed image prompt from simple description using LLM.

    Args:
        client: Gemini client instance
        description: Simple description of desired image
        template: Template to use (photography, character, scene, food, abstract, logo)
        category: Category hint (overrides template detection)
        style: Style hint (photorealistic, watercolor, anime, etc.)
        model: Gemini model to use for generation (default: gemini-2.0-flash-exp)

    Returns:
        dict with keys:
            - prompt: Generated detailed prompt
            - original: Original description
            - template_used: Template name used (if any)
            - category: Detected or specified category
            - style: Specified style (if any)
            - tokens_used: Token count for generation

    Raises:
        PromptGenerationError: If prompt generation fails

    Example:
        >>> client = create_client()
        >>> result = generate_prompt(client, "wizard cat")
        >>> print(result['prompt'])
        'Photorealistic image of a wizard cat...'
    """
    # Auto-detect category if not specified and no template
    detected_category = category or (
        detect_category(description) if not template else None
    )

    # Build system prompt with best practices
    system_prompt = """You are an expert prompt engineer for Gemini 2.5 Flash Image (Nano Banana).
Transform simple descriptions into detailed, effective image generation prompts.

Follow these principles:
1. Be specific and descriptive - include details about subjects, objects, and their relationships
2. Include style, mood, and atmosphere - specify artistic approach and emotional tone
3. Describe composition and perspective - camera angles, framing, depth
4. Specify colors and palette - be explicit about color choices
5. Include technical details - quality level, detail, texture, lighting

Output only the enhanced prompt text, nothing else. Do not include explanations or metadata.
Make the prompt detailed but concise (aim for 50-100 words).
"""

    # Add template instructions if specified
    if template:
        try:
            template_instructions = get_template(template)
            system_prompt += f"\n\nUse this template approach:\n{template_instructions}"
        except ValueError as e:
            raise PromptGenerationError(str(e)) from e

    # Build user prompt
    user_prompt = (
        "Transform this simple description into a detailed image generation prompt:\n\n"
        f"{description}"
    )

    # Add category hint if available
    if detected_category:
        user_prompt += f"\n\nCategory context: {detected_category}"

    # Add style hint if provided
    if style:
        user_prompt += f"\nDesired style: {style}"

    try:
        # Generate prompt using Gemini
        response = client.models.generate_content(
            model=model,
            contents=system_prompt + "\n\n" + user_prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,  # Some creativity but consistent
                max_output_tokens=500,  # Enough for detailed prompts
            ),
        )

        # Extract generated prompt
        if not response.candidates:
            raise PromptGenerationError(
                "No response from model. The request may have been blocked."
            )

        candidate = response.candidates[0]
        if not candidate.content or not candidate.content.parts:
            raise PromptGenerationError("Empty response from model")

        text_content = candidate.content.parts[0].text
        if text_content is None:
            raise PromptGenerationError("Empty text in response")
        generated_prompt = text_content.strip()

        # Get token count
        token_count = (
            response.usage_metadata.total_token_count
            if response.usage_metadata
            else 0
        )

        return {
            "prompt": generated_prompt,
            "original": description,
            "template_used": template,
            "category": detected_category or category,
            "style": style,
            "tokens_used": token_count,
        }

    except Exception as e:
        raise PromptGenerationError(f"Prompt generation failed: {e}") from e


def format_verbose_output(result: dict[str, Any]) -> str:
    """Format prompt generation result as verbose human-readable text.

    Args:
        result: Result dictionary from generate_prompt()

    Returns:
        Formatted verbose output string

    Example:
        >>> result = generate_prompt(client, "wizard cat")
        >>> print(format_verbose_output(result))
        Original Description:
          wizard cat
        ...
    """
    lines = [
        "=" * 70,
        "Prompt Generation Analysis",
        "=" * 70,
        "",
        "Original Description:",
        f"  {result['original']}",
        "",
    ]

    if result.get("template_used"):
        lines.append(f"Template Used: {result['template_used']}")

    if result.get("category"):
        lines.append(f"Category: {result['category']}")

    if result.get("style"):
        lines.append(f"Style: {result['style']}")

    lines.extend(
        [
            f"Tokens Used: {result['tokens_used']}",
            "",
            "=" * 70,
            "Generated Prompt:",
            "=" * 70,
            "",
            result["prompt"],
            "",
        ]
    )

    return "\n".join(lines)
