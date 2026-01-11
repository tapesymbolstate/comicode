"""Tests for Text, StyledText, and SFX classes."""

import numpy as np

from comix.cobject.text.text import Text, StyledText, SFX
from comix.style.style import Style, MANGA_STYLE, COMIC_STYLE


class TestText:
    """Tests for Text class."""

    def test_default_init(self):
        """Test default initialization."""
        text = Text()
        assert text.text == ""
        assert text.font_family == "sans-serif"
        assert text.font_size == 16.0
        assert text.font_weight == "normal"
        assert text.font_style == "normal"
        assert text.color == "#000000"
        assert text.align == "left"
        assert text.line_height == 1.4
        assert text.max_width is None

    def test_with_text(self):
        """Test initialization with text content."""
        text = Text(text="Hello, World!")
        assert text.text == "Hello, World!"
        assert text._text_width > 0
        assert text._text_height > 0

    def test_custom_font_properties(self):
        """Test initialization with custom font properties."""
        text = Text(
            text="Custom",
            font_family="serif",
            font_size=24.0,
            font_weight="bold",
            font_style="italic",
            color="#FF0000",
            align="center",
            line_height=1.6,
        )
        assert text.font_family == "serif"
        assert text.font_size == 24.0
        assert text.font_weight == "bold"
        assert text.font_style == "italic"
        assert text.color == "#FF0000"
        assert text.align == "center"
        assert text.line_height == 1.6

    def test_set_text(self):
        """Test set_text method."""
        text = Text(text="Initial")
        initial_width = text._text_width

        result = text.set_text("Updated text content")
        assert result is text  # Method chaining
        assert text.text == "Updated text content"
        assert text._text_width != initial_width  # Width recalculated

    def test_set_font(self):
        """Test set_font method."""
        text = Text(text="Test")
        initial_width = text._text_width

        result = text.set_font(family="monospace", size=20.0)
        assert result is text  # Method chaining
        assert text.font_family == "monospace"
        assert text.font_size == 20.0
        assert text._text_width != initial_width  # Width recalculated

    def test_set_font_partial(self):
        """Test set_font with only some properties."""
        text = Text(text="Test", font_family="serif", font_size=16.0)

        text.set_font(size=24.0)  # Only change size
        assert text.font_family == "serif"  # Unchanged
        assert text.font_size == 24.0  # Changed

    def test_set_font_weight_and_style(self):
        """Test set_font with weight and style."""
        text = Text(text="Test")
        text.set_font(weight="bold", style="italic")
        assert text.font_weight == "bold"
        assert text.font_style == "italic"

    def test_set_color(self):
        """Test set_color method."""
        text = Text(text="Test")
        result = text.set_color("#00FF00")
        assert result is text  # Method chaining
        assert text.color == "#00FF00"

    def test_apply_style(self):
        """Test apply_style method."""
        text = Text(text="Test")
        style = Style(
            font_family="serif",
            font_size=20.0,
            font_weight="bold",
            font_style="italic",
            font_color="#0000FF",
            text_align="right",
            line_height=1.8,
        )

        result = text.apply_style(style)
        assert result is text  # Method chaining
        assert text.font_family == "serif"
        assert text.font_size == 20.0
        assert text.font_weight == "bold"
        assert text.font_style == "italic"
        assert text.color == "#0000FF"
        assert text.align == "right"
        assert text.line_height == 1.8

    def test_apply_manga_style(self):
        """Test applying MANGA_STYLE preset."""
        text = Text(text="Test")
        text.apply_style(MANGA_STYLE)
        assert text.font_size == 14.0

    def test_apply_comic_style(self):
        """Test applying COMIC_STYLE preset."""
        text = Text(text="Test")
        text.apply_style(COMIC_STYLE)
        assert text.font_size == 18.0
        assert text.font_weight == "bold"

    def test_get_render_data(self):
        """Test get_render_data method."""
        text = Text(text="Render test", font_size=20.0, color="#FF0000")
        data = text.get_render_data()

        assert data["text"] == "Render test"
        assert data["font_family"] == "sans-serif"
        assert data["font_size"] == 20.0
        assert data["font_weight"] == "normal"
        assert data["font_style"] == "normal"
        assert data["color"] == "#FF0000"
        assert data["align"] == "left"
        assert data["line_height"] == 1.4
        assert data["max_width"] is None
        assert "text_width" in data
        assert "text_height" in data
        assert "points" in data

    def test_max_width_wrapping(self):
        """Test text wrapping with max_width."""
        long_text = "This is a very long text that should wrap"
        text_no_wrap = Text(text=long_text)
        text_wrapped = Text(text=long_text, max_width=100.0)

        # Wrapped text should have larger height (multiple lines)
        assert text_wrapped._text_height >= text_no_wrap._text_height
        # Wrapped text width should be constrained
        assert text_wrapped._text_width <= 100.0

    def test_bounding_box_points(self):
        """Test that bounding box points are generated correctly."""
        text = Text(text="Test")
        points = text._points

        assert len(points) == 4
        # Points should form a rectangle centered at origin
        assert np.allclose(points[0], [-text._text_width / 2, -text._text_height / 2])
        assert np.allclose(points[2], [text._text_width / 2, text._text_height / 2])

    def test_cjk_text_width(self):
        """Test that CJK characters are properly handled for width calculation."""
        english_text = Text(text="AB")
        korean_text = Text(text="가나")  # Two Korean characters

        # Korean characters should be wider (full-width)
        assert korean_text._text_width > english_text._text_width

    def test_method_chaining(self):
        """Test that methods can be chained."""
        text = (
            Text(text="Initial")
            .set_text("Updated")
            .set_font(size=24.0)
            .set_color("#0000FF")
        )
        assert text.text == "Updated"
        assert text.font_size == 24.0
        assert text.color == "#0000FF"


class TestStyledText:
    """Tests for StyledText class."""

    def test_default_init(self):
        """Test default initialization."""
        styled = StyledText()
        assert styled.text == ""
        assert styled.background_color is None
        assert styled.text_padding == (0, 0, 0, 0)
        assert styled.border_color is None
        assert styled.border_width == 0

    def test_with_styling(self):
        """Test initialization with styling options."""
        styled = StyledText(
            text="Styled",
            background_color="#EEEEEE",
            padding=(10, 20, 10, 20),
            border_color="#000000",
            border_width=2.0,
        )
        assert styled.text == "Styled"
        assert styled.background_color == "#EEEEEE"
        assert styled.text_padding == (10, 20, 10, 20)
        assert styled.border_color == "#000000"
        assert styled.border_width == 2.0

    def test_inherits_text_properties(self):
        """Test that StyledText inherits Text properties."""
        styled = StyledText(
            text="Test",
            font_size=24.0,
            font_weight="bold",
            color="#FF0000",
        )
        assert styled.font_size == 24.0
        assert styled.font_weight == "bold"
        assert styled.color == "#FF0000"

    def test_get_render_data(self):
        """Test get_render_data includes styled properties."""
        styled = StyledText(
            text="Test",
            background_color="#EEEEEE",
            padding=(5, 10, 5, 10),
            border_color="#000000",
            border_width=1.0,
        )
        data = styled.get_render_data()

        # Check base Text properties
        assert data["text"] == "Test"
        assert data["font_family"] == "sans-serif"

        # Check StyledText-specific properties
        assert data["background_color"] == "#EEEEEE"
        assert data["text_padding"] == (5, 10, 5, 10)
        assert data["border_color"] == "#000000"
        assert data["text_border_width"] == 1.0


class TestSFX:
    """Tests for SFX (sound effect) class."""

    def test_default_init(self):
        """Test default initialization."""
        sfx = SFX()
        assert sfx.text == ""
        assert sfx.font_size == 32.0  # Default SFX size
        assert sfx.font_weight == "bold"  # Default SFX weight
        assert sfx.outline is True
        assert sfx.outline_color == "#FFFFFF"
        assert sfx.outline_width == 3.0
        assert sfx.shadow is False
        assert sfx.shadow_color == "#00000033"
        assert sfx.shadow_offset == (2.0, 2.0)

    def test_with_text(self):
        """Test initialization with text."""
        sfx = SFX(text="BOOM!")
        assert sfx.text == "BOOM!"
        assert sfx._text_width > 0

    def test_custom_outline(self):
        """Test custom outline settings."""
        sfx = SFX(
            text="POW",
            outline=True,
            outline_color="#FF0000",
            outline_width=5.0,
        )
        assert sfx.outline is True
        assert sfx.outline_color == "#FF0000"
        assert sfx.outline_width == 5.0

    def test_with_shadow(self):
        """Test shadow settings."""
        sfx = SFX(
            text="CRASH",
            shadow=True,
            shadow_color="#000000",
            shadow_offset=(4.0, 4.0),
        )
        assert sfx.shadow is True
        assert sfx.shadow_color == "#000000"
        assert sfx.shadow_offset == (4.0, 4.0)

    def test_no_outline(self):
        """Test disabling outline."""
        sfx = SFX(text="test", outline=False)
        assert sfx.outline is False

    def test_custom_font_size(self):
        """Test custom font size overrides default."""
        sfx = SFX(text="ZAP", font_size=48.0)
        assert sfx.font_size == 48.0

    def test_custom_font_weight(self):
        """Test custom font weight overrides default."""
        sfx = SFX(text="whisper", font_weight="normal")
        assert sfx.font_weight == "normal"

    def test_inherits_text_properties(self):
        """Test that SFX inherits Text properties."""
        sfx = SFX(
            text="Test",
            font_family="Impact",
            color="#FF0000",
        )
        assert sfx.font_family == "Impact"
        assert sfx.color == "#FF0000"

    def test_get_render_data(self):
        """Test get_render_data includes SFX properties."""
        sfx = SFX(
            text="WHAM",
            outline=True,
            outline_color="#000000",
            outline_width=4.0,
            shadow=True,
            shadow_color="#333333",
            shadow_offset=(3.0, 3.0),
        )
        data = sfx.get_render_data()

        # Check base Text properties
        assert data["text"] == "WHAM"
        assert data["font_size"] == 32.0
        assert data["font_weight"] == "bold"

        # Check SFX-specific properties
        assert data["sfx"] is True
        assert data["outline"] is True
        assert data["outline_color"] == "#000000"
        assert data["outline_width"] == 4.0
        assert data["shadow"] is True
        assert data["shadow_color"] == "#333333"
        assert data["shadow_offset"] == [3.0, 3.0]

    def test_method_chaining(self):
        """Test that inherited methods can be chained."""
        sfx = SFX(text="Initial").set_text("Updated").set_color("#00FF00")
        assert sfx.text == "Updated"
        assert sfx.color == "#00FF00"
