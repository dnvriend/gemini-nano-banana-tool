"""Tests for --promptgen flag integration in generate command.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import json
from unittest.mock import Mock, patch

from click.testing import CliRunner

from gemini_nano_banana_tool.cli import main as cli


class TestPromptgenIntegration:
    """Test --promptgen flag integration."""

    @patch("gemini_nano_banana_tool.commands.generate_command.generate_image")
    @patch("gemini_nano_banana_tool.commands.generate_command.generate_prompt")
    @patch("gemini_nano_banana_tool.commands.generate_command.create_client")
    def test_promptgen_flag_enhances_prompt(
        self,
        mock_create_client: Mock,
        mock_generate_prompt: Mock,
        mock_generate_image: Mock,
    ) -> None:
        """Test that --promptgen flag enhances the prompt before generation."""
        # Mock client
        mock_client = Mock()
        mock_create_client.return_value = mock_client

        # Mock promptgen result
        mock_generate_prompt.return_value = {
            "prompt": "Enhanced detailed sunset with vibrant colors and dramatic lighting",
            "original": "sunset",
            "template_used": None,
            "category": None,
            "style": None,
            "tokens_used": 150,
            "estimated_cost_usd": 0.0001,
        }

        # Mock image generation result
        mock_generate_image.return_value = {
            "output_path": "output.png",
            "model": "gemini-2.5-flash-image",
            "aspect_ratio": "1:1",
            "resolution": "1024x1024",
            "resolution_quality": "1K",
            "reference_image_count": 0,
            "token_count": 1000,
            "estimated_cost_usd": 0.03,
            "estimated_cost_per_image_usd": None,
            "metadata": {"model_type": "gemini"},
        }

        # Run command with --promptgen
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(
                cli,
                ["generate", "sunset", "-o", "output.png", "--promptgen"],
            )

        # Verify success
        assert result.exit_code == 0

        # Verify generate_prompt was called with original prompt
        mock_generate_prompt.assert_called_once()
        call_kwargs = mock_generate_prompt.call_args.kwargs
        assert call_kwargs["description"] == "sunset"
        assert call_kwargs["template"] is None

        # Verify generate_image was called with enhanced prompt
        mock_generate_image.assert_called_once()
        image_call_kwargs = mock_generate_image.call_args.kwargs
        assert (
            image_call_kwargs["prompt"]
            == "Enhanced detailed sunset with vibrant colors and dramatic lighting"
        )

        # Verify JSON output includes promptgen metadata
        output = json.loads(result.stdout)
        assert output["promptgen"]["enabled"] is True
        assert output["promptgen"]["original_prompt"] == "sunset"
        assert (
            output["promptgen"]["enhanced_prompt"]
            == "Enhanced detailed sunset with vibrant colors and dramatic lighting"
        )
        assert output["promptgen"]["tokens_used"] == 150
        assert output["promptgen"]["estimated_cost_usd"] == 0.0001

    @patch("gemini_nano_banana_tool.commands.generate_command.generate_image")
    @patch("gemini_nano_banana_tool.commands.generate_command.generate_prompt")
    @patch("gemini_nano_banana_tool.commands.generate_command.create_client")
    def test_promptgen_with_template(
        self,
        mock_create_client: Mock,
        mock_generate_prompt: Mock,
        mock_generate_image: Mock,
    ) -> None:
        """Test --promptgen with --promptgen-template option."""
        # Mock client
        mock_client = Mock()
        mock_create_client.return_value = mock_client

        # Mock promptgen result
        mock_generate_prompt.return_value = {
            "prompt": "Professional portrait photo with studio lighting",
            "original": "person",
            "template_used": "photography",
            "category": None,
            "style": None,
            "tokens_used": 200,
            "estimated_cost_usd": 0.0002,
        }

        # Mock image generation result
        mock_generate_image.return_value = {
            "output_path": "output.png",
            "model": "gemini-2.5-flash-image",
            "aspect_ratio": "1:1",
            "resolution": "1024x1024",
            "resolution_quality": "1K",
            "reference_image_count": 0,
            "token_count": 1000,
            "estimated_cost_usd": 0.03,
            "estimated_cost_per_image_usd": None,
            "metadata": {"model_type": "gemini"},
        }

        # Run command with --promptgen and template
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(
                cli,
                [
                    "generate",
                    "person",
                    "-o",
                    "output.png",
                    "--promptgen",
                    "--promptgen-template",
                    "photography",
                ],
            )

        # Verify success
        assert result.exit_code == 0

        # Verify generate_prompt was called with template
        mock_generate_prompt.assert_called_once()
        call_kwargs = mock_generate_prompt.call_args.kwargs
        assert call_kwargs["description"] == "person"
        assert call_kwargs["template"] == "photography"

        # Verify output includes template metadata
        output = json.loads(result.stdout)
        assert output["promptgen"]["template_used"] == "photography"

    @patch("gemini_nano_banana_tool.commands.generate_command.generate_image")
    @patch("gemini_nano_banana_tool.commands.generate_command.create_client")
    def test_without_promptgen_flag(
        self,
        mock_create_client: Mock,
        mock_generate_image: Mock,
    ) -> None:
        """Test that prompt is not enhanced when --promptgen is not used."""
        # Mock client
        mock_client = Mock()
        mock_create_client.return_value = mock_client

        # Mock image generation result
        mock_generate_image.return_value = {
            "output_path": "output.png",
            "model": "gemini-2.5-flash-image",
            "aspect_ratio": "1:1",
            "resolution": "1024x1024",
            "resolution_quality": "1K",
            "reference_image_count": 0,
            "token_count": 1000,
            "estimated_cost_usd": 0.03,
            "estimated_cost_per_image_usd": None,
            "metadata": {"model_type": "gemini"},
        }

        # Run command without --promptgen
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(
                cli,
                ["generate", "sunset", "-o", "output.png"],
            )

        # Verify success
        assert result.exit_code == 0

        # Verify generate_image was called with original prompt
        mock_generate_image.assert_called_once()
        image_call_kwargs = mock_generate_image.call_args.kwargs
        assert image_call_kwargs["prompt"] == "sunset"

        # Verify JSON output shows promptgen disabled
        output = json.loads(result.stdout)
        assert output["promptgen"]["enabled"] is False

    def test_promptgen_template_without_promptgen_flag(self) -> None:
        """Test that --promptgen-template requires --promptgen flag."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(
                cli,
                [
                    "generate",
                    "sunset",
                    "-o",
                    "output.png",
                    "--promptgen-template",
                    "photography",
                ],
            )

        # Should fail with error
        assert result.exit_code == 1
        assert "--promptgen-template requires --promptgen flag" in result.stderr

    @patch("gemini_nano_banana_tool.commands.generate_command.generate_image")
    @patch("gemini_nano_banana_tool.commands.generate_command.generate_prompt")
    @patch("gemini_nano_banana_tool.commands.generate_command.create_client")
    def test_promptgen_error_handling(
        self,
        mock_create_client: Mock,
        mock_generate_prompt: Mock,
        mock_generate_image: Mock,
    ) -> None:
        """Test error handling when prompt enhancement fails."""
        # Mock client
        mock_client = Mock()
        mock_create_client.return_value = mock_client

        # Mock promptgen to raise error
        from gemini_nano_banana_tool.core.promptgen import PromptGenerationError

        mock_generate_prompt.side_effect = PromptGenerationError("API error")

        # Run command with --promptgen
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(
                cli,
                ["generate", "sunset", "-o", "output.png", "--promptgen"],
            )

        # Should fail gracefully
        assert result.exit_code == 1
        assert "Prompt enhancement failed" in result.stderr

        # Image generation should not be called
        mock_generate_image.assert_not_called()
