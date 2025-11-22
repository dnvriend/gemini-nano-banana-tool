"""Tests for Imagen 4 image generation functionality.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from unittest.mock import Mock, patch

import pytest

from gemini_nano_banana_tool.core.generator import GenerationError, generate_image
from gemini_nano_banana_tool.core.models import is_imagen_model


class TestImagenModelDetection:
    """Test Imagen model detection."""

    def test_is_imagen_model_true(self) -> None:
        """Test detection of Imagen models."""
        assert is_imagen_model("imagen-4.0-generate-001") is True
        assert is_imagen_model("imagen-4.0-ultra-generate-001") is True
        assert is_imagen_model("imagen-4.0-fast-generate-001") is True

    def test_is_imagen_model_false(self) -> None:
        """Test detection of non-Imagen models."""
        assert is_imagen_model("gemini-2.5-flash-image") is False
        assert is_imagen_model("gemini-3-pro-image-preview") is False


class TestImagenGeneration:
    """Test Imagen 4 image generation."""

    @patch("gemini_nano_banana_tool.core.generator.save_image")
    def test_generate_with_imagen_success(self, mock_save: Mock) -> None:
        """Test successful image generation with Imagen 4."""
        # Mock client and response
        mock_client = Mock()
        mock_image = Mock()
        mock_image.image.save = Mock()
        mock_response = Mock()
        mock_response.generated_images = [mock_image]

        mock_client.models.generate_images.return_value = mock_response

        # Generate image
        result = generate_image(
            client=mock_client,
            prompt="A beautiful sunset",
            output_path="test.png",
            model="imagen-4.0-generate-001",
            aspect_ratio="16:9",
        )

        # Verify API call
        mock_client.models.generate_images.assert_called_once()
        call_args = mock_client.models.generate_images.call_args

        # Check model
        assert call_args.kwargs["model"] == "imagen-4.0-generate-001"

        # Check prompt
        assert call_args.kwargs["prompt"] == "A beautiful sunset"

        # Check result
        assert result["model"] == "imagen-4.0-generate-001"
        assert result["output_path"] == "test.png"
        assert result["aspect_ratio"] == "16:9"
        assert result["resolution"] == "1344x768"
        assert result["reference_image_count"] == 0
        assert result["token_count"] is None
        assert result["estimated_cost_usd"] is None
        assert result["estimated_cost_per_image_usd"] == 0.04
        assert result["metadata"]["model_type"] == "imagen"

    @patch("gemini_nano_banana_tool.core.generator.save_image")
    def test_generate_with_imagen_fast(self, mock_save: Mock) -> None:
        """Test image generation with Imagen 4 Fast model."""
        # Mock client and response
        mock_client = Mock()
        mock_image = Mock()
        mock_image.image.save = Mock()
        mock_response = Mock()
        mock_response.generated_images = [mock_image]

        mock_client.models.generate_images.return_value = mock_response

        # Generate image
        result = generate_image(
            client=mock_client,
            prompt="A quick test",
            output_path="test.png",
            model="imagen-4.0-fast-generate-001",
            aspect_ratio="1:1",
        )

        # Check pricing
        assert result["estimated_cost_per_image_usd"] == 0.02

    @patch("gemini_nano_banana_tool.core.generator.save_image")
    def test_generate_with_imagen_ultra(self, mock_save: Mock) -> None:
        """Test image generation with Imagen 4 Ultra model."""
        # Mock client and response
        mock_client = Mock()
        mock_image = Mock()
        mock_image.image.save = Mock()
        mock_response = Mock()
        mock_response.generated_images = [mock_image]

        mock_client.models.generate_images.return_value = mock_response

        # Generate image
        result = generate_image(
            client=mock_client,
            prompt="Ultra quality image",
            output_path="test.png",
            model="imagen-4.0-ultra-generate-001",
            aspect_ratio="1:1",
        )

        # Check pricing
        assert result["estimated_cost_per_image_usd"] == 0.06

    @patch("gemini_nano_banana_tool.core.generator.save_image")
    def test_generate_with_imagen_resolution(self, mock_save: Mock) -> None:
        """Test Imagen generation with resolution parameter."""
        # Mock client and response
        mock_client = Mock()
        mock_image = Mock()
        mock_image.image.save = Mock()
        mock_response = Mock()
        mock_response.generated_images = [mock_image]

        mock_client.models.generate_images.return_value = mock_response

        # Generate image with resolution
        result = generate_image(
            client=mock_client,
            prompt="High res image",
            output_path="test.png",
            model="imagen-4.0-generate-001",
            aspect_ratio="1:1",
            resolution="2K",
        )

        # Verify resolution was passed
        call_args = mock_client.models.generate_images.call_args
        assert call_args.kwargs["config"].image_size == "2K"
        assert result["resolution_quality"] == "2K"

    def test_generate_with_imagen_no_images_returned(self) -> None:
        """Test error handling when no images returned."""
        # Mock client with empty response
        mock_client = Mock()
        mock_response = Mock()
        mock_response.generated_images = []

        mock_client.models.generate_images.return_value = mock_response

        # Should raise GenerationError
        with pytest.raises(GenerationError, match="No images returned from Imagen API"):
            generate_image(
                client=mock_client,
                prompt="Test prompt",
                output_path="test.png",
                model="imagen-4.0-generate-001",
            )

    def test_generate_with_imagen_api_error(self) -> None:
        """Test error handling for Imagen API errors."""
        # Mock client that raises exception
        mock_client = Mock()
        mock_client.models.generate_images.side_effect = Exception("API error")

        # Should raise GenerationError
        with pytest.raises(GenerationError, match="Imagen generation failed"):
            generate_image(
                client=mock_client,
                prompt="Test prompt",
                output_path="test.png",
                model="imagen-4.0-generate-001",
            )


class TestImagenVsGeminiRouting:
    """Test routing between Imagen and Gemini generation paths."""

    @patch("gemini_nano_banana_tool.core.generator._generate_with_imagen")
    def test_imagen_model_routes_correctly(self, mock_imagen: Mock) -> None:
        """Test that Imagen models route to Imagen generation."""
        mock_client = Mock()
        mock_imagen.return_value = {
            "output_path": "test.png",
            "model": "imagen-4.0-generate-001",
            "estimated_cost_per_image_usd": 0.04,
        }

        generate_image(
            client=mock_client,
            prompt="Test",
            output_path="test.png",
            model="imagen-4.0-generate-001",
        )

        # Verify Imagen function was called
        mock_imagen.assert_called_once()

    @patch("gemini_nano_banana_tool.core.generator.save_image")
    def test_gemini_model_routes_correctly(self, mock_save: Mock) -> None:
        """Test that Gemini models use Gemini generation path."""
        # Mock Gemini response
        mock_client = Mock()
        mock_part = Mock()
        mock_part.inline_data.data = b"fake_image_data"

        mock_candidate = Mock()
        mock_candidate.content.parts = [mock_part]

        mock_response = Mock()
        mock_response.candidates = [mock_candidate]
        mock_response.usage_metadata.total_token_count = 1000

        mock_client.models.generate_content.return_value = mock_response

        result = generate_image(
            client=mock_client,
            prompt="Test",
            output_path="test.png",
            model="gemini-2.5-flash-image",
        )

        # Verify Gemini-specific fields
        assert result["token_count"] == 1000
        assert result["estimated_cost_usd"] is not None
        assert result["estimated_cost_per_image_usd"] is None
        assert result["metadata"]["model_type"] == "gemini"
