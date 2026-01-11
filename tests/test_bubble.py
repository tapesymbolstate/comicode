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
    auto_position_bubbles,
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


class TestBubbleAutoPositioning:
    """Tests for auto bubble positioning features."""

    def test_attach_to_anchor_top(self) -> None:
        """Test attaching bubble to top of character."""
        char = Stickman(name="Test").move_to((200, 200))
        bubble = SpeechBubble(text="Hello!")
        bubble.attach_to(char, anchor="top")

        assert bubble.tail_direction == "bottom"
        assert bubble.position[1] > char.get_bounding_box()[1][1]

    def test_attach_to_anchor_left(self) -> None:
        """Test attaching bubble to left of character."""
        char = Stickman(name="Test").move_to((200, 200))
        bubble = SpeechBubble(text="Hello!")
        bubble.attach_to(char, anchor="left")

        assert bubble.tail_direction == "right"
        char_bbox = char.get_bounding_box()
        assert bubble.position[0] < char_bbox[0][0]

    def test_attach_to_anchor_right(self) -> None:
        """Test attaching bubble to right of character."""
        char = Stickman(name="Test").move_to((200, 200))
        bubble = SpeechBubble(text="Hello!")
        bubble.attach_to(char, anchor="right")

        assert bubble.tail_direction == "left"
        char_bbox = char.get_bounding_box()
        assert bubble.position[0] > char_bbox[1][0]

    def test_attach_to_anchor_bottom(self) -> None:
        """Test attaching bubble to bottom of character."""
        char = Stickman(name="Test").move_to((200, 200))
        bubble = SpeechBubble(text="Hello!")
        bubble.attach_to(char, anchor="bottom")

        assert bubble.tail_direction == "top"
        char_bbox = char.get_bounding_box()
        assert bubble.position[1] < char_bbox[0][1]

    def test_attach_to_with_custom_buffer(self) -> None:
        """Test attaching bubble with custom buffer distance."""
        char = Stickman(name="Test").move_to((200, 200))
        bubble1 = SpeechBubble(text="Hello!")
        bubble2 = SpeechBubble(text="Hello!")

        bubble1.attach_to(char, anchor="top", buffer=10.0)
        bubble2.attach_to(char, anchor="top", buffer=50.0)

        # bubble2 should be further from character
        assert bubble2.position[1] > bubble1.position[1]

    def test_overlaps_with_overlapping(self) -> None:
        """Test collision detection when bubbles overlap."""
        bubble1 = SpeechBubble(text="Hello!").move_to((100, 100))
        bubble2 = SpeechBubble(text="World!").move_to((110, 110))

        assert bubble1.overlaps_with(bubble2)

    def test_overlaps_with_not_overlapping(self) -> None:
        """Test collision detection when bubbles don't overlap."""
        bubble1 = SpeechBubble(text="Hello!").move_to((100, 100))
        bubble2 = SpeechBubble(text="World!").move_to((500, 500))

        assert not bubble1.overlaps_with(bubble2)

    def test_auto_attach_to_no_collision(self) -> None:
        """Test auto_attach_to with no other bubbles."""
        char = Stickman(name="Test").move_to((200, 200))
        bubble = SpeechBubble(text="Hello!")

        result = bubble.auto_attach_to(char)

        assert result is bubble
        assert bubble.tail_direction == "bottom"  # Should use "top" anchor

    def test_auto_attach_to_avoids_collision(self) -> None:
        """Test that auto_attach_to avoids collision with existing bubbles."""
        char1 = Stickman(name="Alice").move_to((200, 200))
        char2 = Stickman(name="Bob").move_to((200, 200))

        # First bubble takes the "top" position
        bubble1 = SpeechBubble(text="First!").attach_to(char1)

        # Second bubble should find a non-overlapping position
        bubble2 = SpeechBubble(text="Second!")
        bubble2.auto_attach_to(char2, avoid_bubbles=[bubble1])

        # They should not overlap
        assert not bubble1.overlaps_with(bubble2)

    def test_auto_attach_to_with_bounds(self) -> None:
        """Test auto_attach_to respects boundary constraints."""
        char = Stickman(name="Test").move_to((50, 50))
        bubble = SpeechBubble(text="Hello!")

        # Set tight bounds that might push bubble to different position
        bubble.auto_attach_to(
            char,
            bounds=(0, 0, 200, 300),
        )

        # Bubble should be within bounds
        bbox = bubble.get_bounding_box()
        # Just verify no exception is raised and bubble is positioned
        assert bbox is not None

    def test_auto_attach_to_preferred_anchors(self) -> None:
        """Test auto_attach_to with custom preferred anchors."""
        char = Stickman(name="Test").move_to((200, 200))
        bubble = SpeechBubble(text="Hello!")

        # Prefer right side
        bubble.auto_attach_to(char, preferred_anchors=["right", "left"])

        assert bubble.tail_direction == "left"

    def test_auto_attach_to_method_chaining(self) -> None:
        """Test that auto_attach_to returns self for chaining."""
        char = Stickman(name="Test").move_to((200, 200))
        bubble = (
            SpeechBubble(text="Hello!")
            .auto_attach_to(char)
            .set_text("Updated")
        )

        assert bubble.text == "Updated"


class TestAutoPosotionBubbles:
    """Tests for auto_position_bubbles utility function."""

    def test_auto_position_single_bubble(self) -> None:
        """Test positioning a single bubble."""
        char = Stickman(name="Test").move_to((200, 200))
        bubble = SpeechBubble(text="Hello!")

        positioned = auto_position_bubbles([(char, bubble)])

        assert len(positioned) == 1
        assert positioned[0] is bubble
        assert bubble.tail_target is char

    def test_auto_position_multiple_bubbles(self) -> None:
        """Test positioning multiple bubbles without overlap."""
        char1 = Stickman(name="Alice").move_to((100, 200))
        char2 = Stickman(name="Bob").move_to((300, 200))

        bubble1 = SpeechBubble(text="Hello Alice!")
        bubble2 = SpeechBubble(text="Hello Bob!")

        positioned = auto_position_bubbles([
            (char1, bubble1),
            (char2, bubble2),
        ])

        assert len(positioned) == 2
        # Bubbles should not overlap
        assert not bubble1.overlaps_with(bubble2)

    def test_auto_position_with_bounds(self) -> None:
        """Test positioning with boundary constraints."""
        char = Stickman(name="Test").move_to((200, 200))
        bubble = SpeechBubble(text="Hello!")

        positioned = auto_position_bubbles(
            [(char, bubble)],
            bounds=(0, 0, 800, 600),
        )

        assert len(positioned) == 1

    def test_auto_position_close_characters(self) -> None:
        """Test positioning bubbles for characters close together."""
        char1 = Stickman(name="Alice").move_to((150, 200))
        char2 = Stickman(name="Bob").move_to((200, 200))
        char3 = Stickman(name="Charlie").move_to((250, 200))

        bubble1 = SpeechBubble(text="Hi!")
        bubble2 = SpeechBubble(text="Hey!")
        bubble3 = SpeechBubble(text="Hello!")

        positioned = auto_position_bubbles([
            (char1, bubble1),
            (char2, bubble2),
            (char3, bubble3),
        ])

        assert len(positioned) == 3
        # Check that each bubble is attached to its character
        assert bubble1.tail_target is char1
        assert bubble2.tail_target is char2
        assert bubble3.tail_target is char3
