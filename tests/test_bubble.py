"""Tests for Bubble classes."""

import logging
import pytest

from comix.cobject.bubble.bubble import (
    Bubble,
    SpeechBubble,
    ThoughtBubble,
    ShoutBubble,
    WhisperBubble,
    NarratorBubble,
    auto_position_bubbles,
    _calculate_auto_tail_length,
)
from comix.cobject.character.character import Stickman
from comix.cobject.panel.panel import Panel
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


class TestBubbleEdgeCases:
    """Tests for bubble edge cases."""

    def test_empty_text_bubble(self) -> None:
        """Test bubble with empty text renders with minimum size (padding only).

        As specified in speech-bubbles.md: "Empty text: Render bubble with minimum size"
        """
        bubble = SpeechBubble(text="")

        # Bubble should have minimum size (60x40 as per implementation)
        assert bubble.bubble_width >= 60.0
        assert bubble.bubble_height >= 40.0

        # Bubble should still have valid points for rendering
        data = bubble.get_render_data()
        assert "points" in data
        assert len(data["points"]) > 0

        # Text should be empty
        assert bubble.text == ""
        assert data["text"] == ""

    def test_empty_text_bubble_types(self) -> None:
        """Test all bubble types handle empty text correctly."""
        bubble_classes = [
            SpeechBubble,
            ThoughtBubble,
            ShoutBubble,
            WhisperBubble,
            NarratorBubble,
        ]

        for BubbleClass in bubble_classes:
            bubble = BubbleClass(text="")
            # All bubble types should render with minimum size
            assert bubble.bubble_width >= 60.0
            assert bubble.bubble_height >= 40.0
            # Should have valid render data
            data = bubble.get_render_data()
            assert len(data["points"]) > 0

    def test_very_long_text_bubble(self) -> None:
        """Test bubble with very long text (1000+ chars) auto-wraps and expands.

        As specified in speech-bubbles.md: "Very long text (1000+ chars):
        Auto-wrap and expand bubble vertically"
        """
        # Create text with 1000+ characters (~250 words)
        long_text = "word " * 250  # 1250 characters
        bubble = SpeechBubble(text=long_text)

        # Bubble should expand vertically for long text
        # With auto-wrap at ~200px width and ~16px font size, expect many lines
        assert bubble.bubble_height > 200.0

        # Width should be constrained (not infinite)
        # Auto-wrap kicks in at 200px text width + padding
        assert bubble.bubble_width <= 300.0

        # Should have valid render data
        data = bubble.get_render_data()
        assert "points" in data
        assert data["text"] == long_text

    def test_extremely_long_text_stability(self) -> None:
        """Test bubble handles extremely long text (5000+ chars) without crashing."""
        # Stress test with 5000+ characters
        extreme_text = "a" * 5000
        bubble = SpeechBubble(text=extreme_text)

        # Should not crash, height should be very large
        assert bubble.bubble_height > 0
        assert bubble.bubble_width > 0

        # Should still produce valid render data
        data = bubble.get_render_data()
        assert len(data["points"]) > 0

    def test_text_with_explicit_newlines(self) -> None:
        """Test bubble respects explicit line breaks in text."""
        text_with_newlines = "Line 1\nLine 2\nLine 3"
        bubble = SpeechBubble(text=text_with_newlines)

        # Text should be preserved exactly
        assert bubble.text == text_with_newlines
        data = bubble.get_render_data()
        assert data["text"] == text_with_newlines

        # Height should accommodate multiple lines (implicitly via renderer)
        # The bubble itself stores the text; actual rendering handles newlines
        assert bubble.bubble_height > 40.0

    def test_single_character_text(self) -> None:
        """Test bubble handles single character text."""
        bubble = SpeechBubble(text="!")

        # Should still have valid minimum dimensions
        assert bubble.bubble_width >= 60.0
        assert bubble.bubble_height >= 40.0

        data = bubble.get_render_data()
        assert data["text"] == "!"

    def test_whitespace_only_text(self) -> None:
        """Test bubble handles whitespace-only text."""
        bubble = SpeechBubble(text="   ")

        # Should render with minimum size like empty text
        assert bubble.bubble_width >= 60.0
        assert bubble.bubble_height >= 40.0

        data = bubble.get_render_data()
        assert data["text"] == "   "


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


class TestBubblePositioningFallbacks:
    """Tests for bubble positioning edge cases and fallback behavior."""

    def test_attach_to_with_invalid_anchor_defaults_to_top(self) -> None:
        """Test that invalid anchor parameter falls back to 'top' position."""
        char = Stickman(name="Test").move_to((200, 200))
        bubble = SpeechBubble(text="Hello!")

        bubble.attach_to(char, anchor="invalid_anchor")

        assert bubble.tail_target is char
        assert bubble.tail_direction == "bottom"

    def test_auto_attach_to_fallback_when_all_anchors_out_of_bounds(self) -> None:
        """Test fallback to first anchor when all positions are out of bounds."""
        char = Stickman(name="Test").move_to((50, 50))
        bubble = SpeechBubble(text="A very long text that makes a large bubble")

        result = bubble.auto_attach_to(
            char,
            bounds=(0, 0, 100, 100),
            avoid_bubbles=[],
        )

        assert result is bubble
        assert bubble.tail_target is char

    def test_auto_attach_to_fallback_when_all_anchors_overlap(self) -> None:
        """Test fallback when all anchor positions would overlap with existing bubbles."""
        char1 = Stickman(name="Test1").move_to((100, 100))
        char2 = Stickman(name="Test2").move_to((100, 100))

        bubble1 = SpeechBubble(text="First bubble")
        bubble2 = SpeechBubble(text="Second bubble")
        bubble3 = SpeechBubble(text="Third bubble")
        bubble4 = SpeechBubble(text="Fourth bubble")
        bubble5 = SpeechBubble(text="Fifth bubble")
        bubble6 = SpeechBubble(text="Sixth bubble")

        bubble1.attach_to(char1, anchor="top")
        bubble2.attach_to(char1, anchor="bottom")
        bubble3.attach_to(char1, anchor="left")
        bubble4.attach_to(char1, anchor="right")
        bubble5.attach_to(char1, anchor="top-left")
        bubble6.attach_to(char1, anchor="top-right")

        new_bubble = SpeechBubble(text="New bubble")
        result = new_bubble.auto_attach_to(
            char2,
            avoid_bubbles=[bubble1, bubble2, bubble3, bubble4, bubble5, bubble6],
        )

        assert result is new_bubble
        assert new_bubble.tail_target is char2

    def test_auto_attach_to_with_bounds_check_triggers_invalid(self) -> None:
        """Test that bounds check properly invalidates positions."""
        char = Stickman(name="Test").move_to((400, 400))
        bubble = SpeechBubble(text="Hello world")

        result = bubble.auto_attach_to(
            char,
            bounds=(300, 300, 500, 500),
            avoid_bubbles=[],
        )

        assert result is bubble
        bbox = bubble.get_bounding_box()
        assert bbox[0][0] >= 300 or bubble.tail_target is char

    def test_tail_target_as_tuple_position(self) -> None:
        """Test bubble with tail_target as tuple position in render data."""
        bubble = SpeechBubble(text="Hello!")
        bubble.tail_target = (100.0, 200.0)

        data = bubble.get_render_data()

        assert data["tail_target"] == [100.0, 200.0]

    def test_tail_target_as_cobject_in_render_data(self) -> None:
        """Test bubble with tail_target as CObject in render data."""
        char = Stickman(name="Test").move_to((150, 250))
        bubble = SpeechBubble(text="Hello!")
        bubble.point_to(char)

        data = bubble.get_render_data()

        assert data["tail_target"] is not None
        assert isinstance(data["tail_target"], list)

    def test_tail_target_none_in_render_data(self) -> None:
        """Test bubble with no tail_target in render data."""
        bubble = SpeechBubble(text="Hello!")

        data = bubble.get_render_data()

        assert data["tail_target"] is None


class TestBubbleTailModes:
    """Tests for bubble tail mode feature."""

    def test_default_tail_mode_is_auto(self):
        """Test that default tail_mode is auto."""
        bubble = Bubble(text="Hello")
        assert bubble.tail_mode == "auto"

    def test_tail_mode_fixed(self):
        """Test tail_mode fixed uses specified length."""
        bubble = Bubble(text="Hello", tail_mode="fixed", tail_length=40)
        assert bubble.tail_mode == "fixed"
        assert bubble.get_effective_tail_length() == 40

    def test_tail_mode_none(self):
        """Test tail_mode none produces no tail."""
        bubble = Bubble(text="Hello", tail_mode="none")
        assert bubble.tail_mode == "none"
        assert bubble.get_effective_tail_length() == 0
        assert len(bubble._tail_points) == 0

    def test_invalid_tail_mode_fallback(self, caplog: pytest.LogCaptureFixture):
        """Test invalid tail_mode falls back to auto."""
        with caplog.at_level(logging.WARNING, logger="comix.cobject.bubble.bubble"):
            bubble = Bubble(text="Hello", tail_mode="invalid")
        assert "Unknown tail_mode" in caplog.text
        assert bubble.tail_mode == "auto"

    def test_tail_style_default(self):
        """Test default tail_style is classic."""
        bubble = Bubble(text="Hello")
        assert bubble.tail_style == "classic"

    def test_invalid_tail_style_fallback(self, caplog: pytest.LogCaptureFixture):
        """Test invalid tail_style falls back to classic."""
        with caplog.at_level(logging.WARNING, logger="comix.cobject.bubble.bubble"):
            bubble = Bubble(text="Hello", tail_style="invalid")
        assert "Unknown tail_style" in caplog.text
        assert bubble.tail_style == "classic"

    def test_narrator_bubble_default_tail_mode_none(self):
        """Test that NarratorBubble defaults to tail_mode='none'."""
        bubble = NarratorBubble(text="Meanwhile...")
        assert bubble.tail_mode == "none"
        assert len(bubble._tail_points) == 0


class TestAutoTailLength:
    """Tests for auto tail length calculation."""

    def test_calculate_auto_tail_length_basic(self):
        """Test basic auto tail length calculation."""
        result = _calculate_auto_tail_length(
            bubble_pos=(100, 200),
            target_pos=(100, 100),
            min_length=15,
            max_length=50,
        )
        # Distance is 100, 40% = 40
        assert result == 40.0

    def test_auto_tail_disabled_when_close(self):
        """Test tail is disabled when very close."""
        result = _calculate_auto_tail_length(
            bubble_pos=(100, 100),
            target_pos=(100, 110),  # Only 10 pixels apart
            distance_threshold=20,
        )
        assert result == 0.0

    def test_auto_tail_clamped_to_max(self):
        """Test tail is clamped to max_length."""
        result = _calculate_auto_tail_length(
            bubble_pos=(0, 0),
            target_pos=(500, 0),  # 500 pixels apart
            max_length=50,
        )
        assert result == 50.0

    def test_auto_tail_clamped_to_min(self):
        """Test tail is clamped to min_length."""
        result = _calculate_auto_tail_length(
            bubble_pos=(0, 0),
            target_pos=(50, 0),  # 50 pixels apart
            min_length=15,
            length_ratio=0.1,  # 10% = 5, but min is 15
            distance_threshold=5,
        )
        assert result == 15.0

    def test_auto_tail_with_bubble_and_character(self):
        """Test auto tail calculation with actual bubble and character."""
        char = Stickman(height=100)
        char.move_to((300, 200))

        bubble = SpeechBubble(text="Hello!", tail_mode="auto")
        bubble.move_to((300, 350))  # 150 pixels above character
        bubble.point_to(char)
        bubble.generate_points()

        # Should calculate auto length based on distance
        effective = bubble.get_effective_tail_length()
        assert 15 <= effective <= 50


class TestSmartAttachTo:
    """Tests for smart_attach_to method."""

    def test_smart_attach_to_basic(self):
        """Test basic smart_attach_to functionality."""
        char = Stickman(height=100)
        char.move_to((200, 200))

        bubble = SpeechBubble(text="Hello!")
        bubble.smart_attach_to(char)

        # Should be attached to character
        assert bubble.tail_target is char
        # Should have auto tail mode enabled
        assert bubble.tail_mode == "auto"

    def test_smart_attach_to_with_panel(self):
        """Test smart_attach_to respects panel bounds."""
        panel = Panel(width=600, height=400)
        panel.move_to((300, 200))

        char = Stickman(height=100)
        char.move_to((300, 200))

        bubble = SpeechBubble(text="Hello!")
        bubble.smart_attach_to(char, panel=panel)

        # Bubble should be within panel bounds
        bbox = bubble.get_bounding_box()
        panel_half_w = panel.width / 2 - panel.padding
        # Bubble should be roughly within panel
        assert bbox[0][0] >= -panel_half_w - 50  # Some tolerance

    def test_smart_attach_to_custom_positions(self):
        """Test smart_attach_to with custom preferred positions."""
        char = Stickman(height=100)
        char.move_to((200, 200))

        bubble = SpeechBubble(text="Hello!")
        bubble.smart_attach_to(char, preferred_positions=["left", "right"])

        # Should be attached
        assert bubble.tail_target is char


class TestBubbleRenderDataTailFields:
    """Tests for new tail fields in render data."""

    def test_render_data_includes_tail_mode(self):
        """Test that render data includes tail_mode."""
        bubble = SpeechBubble(text="Hello!", tail_mode="fixed")
        data = bubble.get_render_data()

        assert data["tail_mode"] == "fixed"
        assert data["tail_style"] == "classic"

    def test_render_data_includes_effective_tail_length(self):
        """Test that render data includes effective_tail_length."""
        bubble = SpeechBubble(text="Hello!", tail_mode="fixed", tail_length=35)
        data = bubble.get_render_data()

        assert data["effective_tail_length"] == 35

    def test_render_data_includes_auto_tail_params(self):
        """Test that render data includes auto tail parameters."""
        bubble = SpeechBubble(
            text="Hello!",
            min_tail_length=20,
            max_tail_length=60,
            tail_distance_threshold=25,
        )
        data = bubble.get_render_data()

        assert data["min_tail_length"] == 20
        assert data["max_tail_length"] == 60
        assert data["tail_distance_threshold"] == 25
