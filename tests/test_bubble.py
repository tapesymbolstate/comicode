"""Tests for Bubble classes."""

import numpy as np
import pytest

from comix.cobject.bubble.bubble import (
    Bubble,
    SpeechBubble,
    ThoughtBubble,
    ShoutBubble,
    WhisperBubble,
    NarratorBubble,
)
from comix.cobject.character.character import Stickman


class TestBubble:
    """Tests for Bubble base class."""

    def test_default_init(self):
        """Test default initialization."""
        bubble = Bubble()
        assert bubble.text == ""
        assert bubble.style == "speech"
        assert bubble.border_color == "#000000"
        assert bubble.fill_color == "#FFFFFF"
        assert bubble.font_size == 16.0

    def test_with_text(self):
        """Test initialization with text."""
        bubble = Bubble(text="Hello!")
        assert bubble.text == "Hello!"
        assert bubble.bubble_width > 0
        assert bubble.bubble_height > 0

    def test_set_text(self):
        """Test set_text method."""
        bubble = Bubble(text="Initial")
        result = bubble.set_text("Updated")
        assert result is bubble
        assert bubble.text == "Updated"

    def test_point_to(self):
        """Test point_to method."""
        bubble = Bubble(text="Hello")
        target = (100, 200)
        result = bubble.point_to(target)
        assert result is bubble
        assert bubble.tail_target == target

    def test_get_render_data(self):
        """Test get_render_data method."""
        bubble = Bubble(text="Test", font_size=20)
        data = bubble.get_render_data()

        assert data["text"] == "Test"
        assert data["bubble_type"] == "speech"
        assert data["font_size"] == 20
        assert "points" in data
        assert "tail_points" in data


class TestSpeechBubble:
    """Tests for SpeechBubble class."""

    def test_style(self):
        """Test that style is set correctly."""
        bubble = SpeechBubble(text="Hello")
        assert bubble.style == "speech"


class TestThoughtBubble:
    """Tests for ThoughtBubble class."""

    def test_style(self):
        """Test that style is set correctly."""
        bubble = ThoughtBubble(text="Thinking...")
        assert bubble.style == "thought"
        assert bubble.corner_radius == 999


class TestShoutBubble:
    """Tests for ShoutBubble class."""

    def test_style(self):
        """Test that style is set correctly."""
        bubble = ShoutBubble(text="WHAT?!")
        assert bubble.style == "shout"
        assert bubble.border_width == 3.0
        assert bubble.font_size == 20.0


class TestWhisperBubble:
    """Tests for WhisperBubble class."""

    def test_style(self):
        """Test that style is set correctly."""
        bubble = WhisperBubble(text="psst...")
        assert bubble.style == "whisper"
        assert bubble.border_style == "dashed"
        assert bubble.font_size == 14.0


class TestNarratorBubble:
    """Tests for NarratorBubble class."""

    def test_style(self):
        """Test that style is set correctly."""
        bubble = NarratorBubble(text="Meanwhile...")
        assert bubble.style == "narrator"
        assert bubble.corner_radius == 0.0
        assert bubble.tail_length == 0.0


class TestBubbleWithCharacter:
    """Tests for bubble attachment to characters."""

    def test_attach_to_character(self):
        """Test attaching bubble to a character."""
        char = Stickman(name="Test").move_to((100, 100))
        bubble = SpeechBubble(text="Hello!")
        bubble.attach_to(char)

        assert bubble.tail_target is char
        assert bubble.position[1] > char.get_center()[1]
