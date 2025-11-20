"""Conversation state management for multi-turn image generation.

This module provides functionality to maintain conversation history across
multiple image generation turns, enabling progressive refinement.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class ConversationTurn:
    """Represents a single turn in a conversation."""

    def __init__(
        self,
        prompt: str,
        output_path: str | None = None,
        reference_images: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ):
        """Initialize a conversation turn.

        Args:
            prompt: Text prompt for this turn
            output_path: Path to generated image (if any)
            reference_images: Reference images used in this turn
            metadata: Additional metadata (token count, etc.)
        """
        self.prompt = prompt
        self.output_path = output_path
        self.reference_images = reference_images or []
        self.metadata = metadata or {}
        self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> dict[str, Any]:
        """Convert turn to dictionary for serialization."""
        return {
            "prompt": self.prompt,
            "output_path": self.output_path,
            "reference_images": self.reference_images,
            "metadata": self.metadata,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ConversationTurn:
        """Create turn from dictionary."""
        turn = cls(
            prompt=data["prompt"],
            output_path=data.get("output_path"),
            reference_images=data.get("reference_images", []),
            metadata=data.get("metadata", {}),
        )
        turn.timestamp = data.get("timestamp", datetime.now().isoformat())
        return turn


class Conversation:
    """Manages conversation state for multi-turn image generation."""

    def __init__(
        self,
        model: str,
        aspect_ratio: str = "1:1",
        conversation_id: str | None = None,
    ):
        """Initialize a conversation.

        Args:
            model: Gemini model to use
            aspect_ratio: Aspect ratio for generated images
            conversation_id: Unique conversation ID (auto-generated if None)
        """
        self.conversation_id = conversation_id or datetime.now().strftime("%Y%m%d_%H%M%S")
        self.model = model
        self.aspect_ratio = aspect_ratio
        self.turns: list[ConversationTurn] = []
        self.created_at = datetime.now().isoformat()
        self.updated_at = self.created_at

    def add_turn(self, turn: ConversationTurn) -> None:
        """Add a turn to the conversation.

        Args:
            turn: Conversation turn to add
        """
        self.turns.append(turn)
        self.updated_at = datetime.now().isoformat()
        logger.debug(f"Added turn {len(self.turns)} to conversation {self.conversation_id}")

    def get_history(self) -> list[ConversationTurn]:
        """Get conversation history.

        Returns:
            List of conversation turns
        """
        return self.turns

    def to_dict(self) -> dict[str, Any]:
        """Convert conversation to dictionary for serialization."""
        return {
            "conversation_id": self.conversation_id,
            "model": self.model,
            "aspect_ratio": self.aspect_ratio,
            "turns": [turn.to_dict() for turn in self.turns],
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Conversation:
        """Create conversation from dictionary."""
        conv = cls(
            model=data["model"],
            aspect_ratio=data.get("aspect_ratio", "1:1"),
            conversation_id=data.get("conversation_id"),
        )
        conv.created_at = data.get("created_at", datetime.now().isoformat())
        conv.updated_at = data.get("updated_at", conv.created_at)
        conv.turns = [ConversationTurn.from_dict(t) for t in data.get("turns", [])]
        return conv

    def save(self, file_path: str) -> None:
        """Save conversation to JSON file.

        Args:
            file_path: Path to save conversation file
        """
        logger.debug(f"Saving conversation to: {file_path}")
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
        logger.info(f"Conversation saved: {file_path}")

    @classmethod
    def load(cls, file_path: str) -> Conversation:
        """Load conversation from JSON file.

        Args:
            file_path: Path to conversation file

        Returns:
            Loaded conversation

        Raises:
            FileNotFoundError: If conversation file doesn't exist
            ValueError: If conversation file is invalid
        """
        logger.debug(f"Loading conversation from: {file_path}")
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Conversation file not found: {file_path}")

        try:
            with open(file_path, encoding="utf-8") as f:
                data = json.load(f)
            logger.info(f"Conversation loaded: {file_path} (turns={len(data.get('turns', []))})")
            return cls.from_dict(data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid conversation file format: {e}") from e
