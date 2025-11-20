"""Tests for gemini_nano_banana_tool.utils module.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import os
import tempfile

import pytest

from gemini_nano_banana_tool.utils import (
    ValidationError,
    format_resolution,
    load_prompt,
    validate_aspect_ratio,
    validate_model,
    validate_reference_images,
)


def test_load_prompt_from_text() -> None:
    """Test loading prompt from direct text."""
    result = load_prompt("Hello World", None, False)
    assert result == "Hello World"
    assert isinstance(result, str)


def test_load_prompt_from_file() -> None:
    """Test loading prompt from file."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write("Test prompt content")
        temp_file = f.name

    try:
        result = load_prompt(None, temp_file, False)
        assert result == "Test prompt content"
    finally:
        os.unlink(temp_file)


def test_load_prompt_empty_fails() -> None:
    """Test that loading with no prompt source raises error."""
    with pytest.raises(ValidationError, match="No prompt provided"):
        load_prompt(None, None, False)


def test_load_prompt_multiple_sources_fails() -> None:
    """Test that providing multiple prompt sources raises error."""
    with pytest.raises(ValidationError, match="Multiple prompt sources"):
        load_prompt("text", "file.txt", False)


def test_validate_aspect_ratio_valid() -> None:
    """Test validating valid aspect ratios."""
    # Should not raise
    validate_aspect_ratio("1:1")
    validate_aspect_ratio("16:9")
    validate_aspect_ratio("9:16")


def test_validate_aspect_ratio_invalid() -> None:
    """Test validating invalid aspect ratio."""
    with pytest.raises(ValidationError, match="Unsupported aspect ratio"):
        validate_aspect_ratio("99:99")


def test_validate_model_valid() -> None:
    """Test validating valid models."""
    # Should not raise
    validate_model("gemini-2.5-flash-image")
    validate_model("gemini-3-pro-image-preview")


def test_validate_model_invalid() -> None:
    """Test validating invalid model."""
    with pytest.raises(ValidationError, match="Unsupported model"):
        validate_model("invalid-model")


def test_validate_reference_images_valid() -> None:
    """Test validating valid reference images."""
    # Create temp files
    temp_files = []
    for i in range(3):
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        temp_file.close()
        temp_files.append(temp_file.name)

    try:
        # Should not raise for 1, 2, or 3 images
        validate_reference_images([temp_files[0]])
        validate_reference_images(temp_files[:2])
        validate_reference_images(temp_files)
    finally:
        for temp_file in temp_files:
            os.unlink(temp_file)


def test_validate_reference_images_too_many() -> None:
    """Test validating too many reference images."""
    # Create 4 temp files
    temp_files = []
    for i in range(4):
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        temp_file.close()
        temp_files.append(temp_file.name)

    try:
        with pytest.raises(ValidationError, match="Too many reference images"):
            validate_reference_images(temp_files)
    finally:
        for temp_file in temp_files:
            os.unlink(temp_file)


def test_validate_reference_images_not_found() -> None:
    """Test validating non-existent reference image."""
    with pytest.raises(ValidationError, match="Reference image not found"):
        validate_reference_images(["/path/that/does/not/exist.jpg"])


def test_format_resolution() -> None:
    """Test formatting resolution from aspect ratio."""
    assert format_resolution("1:1") == "1024x1024"
    assert format_resolution("16:9") == "1344x768"
    assert format_resolution("9:16") == "768x1344"
    assert format_resolution("invalid") == "unknown"
