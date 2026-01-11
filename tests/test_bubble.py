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
from comix.style.style import Style, MANGA_STYLE, COMIC_STYLE


class TestBubble:
    """Tests for Bubble base class."""

    def test_default_init(self):
        """Test default initialization."""
        bubble = Bubble()
        assert bubble.text == ""
        assert bubble.bubble_type == "speech"
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
        assert bubble.bubble_type == "speech"


class TestThoughtBubble:
    """Tests for ThoughtBubble class."""

    def test_style(self):
        """Test that style is set correctly."""
        bubble = ThoughtBubble(text="Thinking...")
        assert bubble.bubble_type == "thought"
        assert bubble.corner_radius == 999


class TestShoutBubble:
    """Tests for ShoutBubble class."""

    def test_style(self):
        """Test that style is set correctly."""
        bubble = ShoutBubble(text="WHAT?!")
        assert bubble.bubble_type == "shout"
        assert bubble.border_width == 3.0
        assert bubble.font_size == 20.0


class TestWhisperBubble:
    """Tests for WhisperBubble class."""

    def test_style(self):
        """Test that style is set correctly."""
        bubble = WhisperBubble(text="psst...")
        assert bubble.bubble_type == "whisper"
        assert bubble.border_style == "dashed"
        assert bubble.font_size == 14.0


class TestNarratorBubble:
    """Tests for NarratorBubble class."""

    def test_style(self):
        """Test that style is set correctly."""
        bubble = NarratorBubble(text="Meanwhile...")
        assert bubble.bubble_type == "narrator"
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


class TestBubbleStyle:
    """Tests for bubble style functionality."""

    def test_apply_style(self) -> None:
        """Test applying a style to bubble."""
        bubble = Bubble(text="Test")
        style = Style(
            border_color="#FF0000",
            border_width=5.0,
            fill_color="#FFFF00",
            font_size=24.0,
            font_family="Comic Sans MS",
        )
        result = bubble.apply_style(style)

        assert result is bubble  # Returns self for chaining
        assert bubble.border_color == "#FF0000"
        assert bubble.border_width == 5.0
        assert bubble.fill_color == "#FFFF00"
        assert bubble.font_size == 24.0
        assert bubble.font_family == "Comic Sans MS"
        assert bubble.get_style() == style

    def test_apply_manga_style(self) -> None:
        """Test applying MANGA_STYLE preset."""
        bubble = Bubble(text="Hello")
        bubble.apply_style(MANGA_STYLE)

        assert bubble.border_color == MANGA_STYLE.border_color
        assert bubble.border_width == MANGA_STYLE.border_width
        assert bubble.font_size == MANGA_STYLE.font_size

    def test_apply_comic_style(self) -> None:
        """Test applying COMIC_STYLE preset."""
        bubble = Bubble(text="BOOM!")
        bubble.apply_style(COMIC_STYLE)

        assert bubble.border_width == 3.0
        assert bubble.font_size == 18.0

    def test_apply_style_recalculates_size(self) -> None:
        """Test that applying style recalculates bubble size."""
        bubble = Bubble(text="Test text")
        original_width = bubble.bubble_width
        original_height = bubble.bubble_height

        # Apply style with much larger font
        large_font_style = Style(font_size=48.0)
        bubble.apply_style(large_font_style)

        # Size should have changed due to larger font
        assert bubble.bubble_height != original_height

    def test_style_method_chaining(self) -> None:
        """Test that style can be chained with other methods."""
        bubble = (
            Bubble(text="Hello")
            .apply_style(MANGA_STYLE)
            .move_to((100, 100))
            .set_text("Updated")
        )
        assert bubble.text == "Updated"
        assert bubble.font_size == MANGA_STYLE.font_size


class TestCustomBubbleShapes:
    """Tests for custom bubble shape features."""

    def test_corner_radii(self) -> None:
        """Test per-corner radius customization."""
        # Different radii for each corner (tr, br, bl, tl)
        bubble = Bubble(
            text="Corners",
            corner_radii=(10.0, 20.0, 30.0, 40.0),
        )
        assert bubble.corner_radii == (10.0, 20.0, 30.0, 40.0)
        data = bubble.get_render_data()
        assert data["corner_radii"] == (10.0, 20.0, 30.0, 40.0)

    def test_corner_radii_none_uses_corner_radius(self) -> None:
        """Test that corner_radii=None uses corner_radius for all corners."""
        bubble = Bubble(text="Test", corner_radius=15.0)
        assert bubble.corner_radii is None
        assert bubble.corner_radius == 15.0

    def test_wobble_mode_random(self) -> None:
        """Test random wobble mode (default)."""
        bubble = Bubble(text="Wobble", wobble=0.5, wobble_mode="random")
        assert bubble.wobble_mode == "random"
        data = bubble.get_render_data()
        assert data["wobble_mode"] == "random"

    def test_wobble_mode_wave(self) -> None:
        """Test wave wobble mode."""
        bubble = Bubble(text="Wave", wobble=0.5, wobble_mode="wave")
        assert bubble.wobble_mode == "wave"
        data = bubble.get_render_data()
        assert data["wobble_mode"] == "wave"

    def test_emphasis_enabled(self) -> None:
        """Test emphasis effect."""
        bubble = Bubble(text="Important!", emphasis=True)
        assert bubble.emphasis is True
        data = bubble.get_render_data()
        assert data["emphasis"] is True

    def test_emphasis_default_false(self) -> None:
        """Test emphasis is disabled by default."""
        bubble = Bubble(text="Normal")
        assert bubble.emphasis is False

    def test_combined_effects(self) -> None:
        """Test combining multiple custom shape options."""
        bubble = Bubble(
            text="Custom",
            corner_radii=(5.0, 10.0, 15.0, 20.0),
            wobble=0.3,
            wobble_mode="wave",
            emphasis=True,
        )
        assert bubble.corner_radii == (5.0, 10.0, 15.0, 20.0)
        assert bubble.wobble == 0.3
        assert bubble.wobble_mode == "wave"
        assert bubble.emphasis is True
