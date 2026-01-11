"""Tests for Style class."""


from comix.style.style import (
    Style,
    MANGA_STYLE,
    WEBTOON_STYLE,
    COMIC_STYLE,
    MINIMAL_STYLE,
)


class TestStyle:
    """Tests for Style dataclass."""

    def test_default_init(self) -> None:
        """Test default Style initialization."""
        style = Style()
        assert style.border_color == "#000000"
        assert style.border_width == 2.0
        assert style.border_style == "solid"
        assert style.fill_color == "#FFFFFF"
        assert style.fill_opacity == 1.0
        assert style.font_family == "sans-serif"
        assert style.font_size == 16.0
        assert style.font_weight == "normal"
        assert style.font_style == "normal"
        assert style.font_color == "#000000"
        assert style.text_align == "left"
        assert style.line_height == 1.4
        assert style.shadow is False

    def test_custom_init(self) -> None:
        """Test Style with custom values."""
        style = Style(
            border_color="#FF0000",
            border_width=5.0,
            font_size=24.0,
            shadow=True,
        )
        assert style.border_color == "#FF0000"
        assert style.border_width == 5.0
        assert style.font_size == 24.0
        assert style.shadow is True

    def test_to_dict(self) -> None:
        """Test Style to_dict method."""
        style = Style(border_color="#FF0000", border_width=5.0)
        d = style.to_dict()

        assert d["border_color"] == "#FF0000"
        assert d["border_width"] == 5.0
        assert d["fill_color"] == "#FFFFFF"
        assert "shadow" in d

    def test_from_dict(self) -> None:
        """Test Style from_dict class method."""
        data = {
            "border_color": "#00FF00",
            "border_width": 3.0,
            "font_size": 20.0,
        }
        style = Style.from_dict(data)

        assert style.border_color == "#00FF00"
        assert style.border_width == 3.0
        assert style.font_size == 20.0
        # Other values should be defaults
        assert style.fill_color == "#FFFFFF"

    def test_from_dict_ignores_invalid_keys(self) -> None:
        """Test that from_dict ignores invalid keys."""
        data = {
            "border_color": "#00FF00",
            "invalid_key": "should be ignored",
            "another_invalid": 123,
        }
        style = Style.from_dict(data)
        assert style.border_color == "#00FF00"
        # Should not raise error for invalid keys

    def test_merge_with_basic(self) -> None:
        """Test merge_with method basic functionality."""
        base = Style(border_color="#000000", border_width=2.0)
        override = Style(border_color="#FF0000")

        merged = base.merge_with(override)
        assert merged.border_color == "#FF0000"  # Overridden
        assert merged.border_width == 2.0  # From base

    def test_merge_with_preserves_non_defaults(self) -> None:
        """Test that merge_with preserves non-default values from base."""
        base = Style(border_color="#0000FF", border_width=5.0, font_size=24.0)
        override = Style(font_color="#FF0000")  # Only font_color is non-default

        merged = base.merge_with(override)
        assert merged.border_color == "#0000FF"  # From base
        assert merged.border_width == 5.0  # From base
        assert merged.font_size == 24.0  # From base
        assert merged.font_color == "#FF0000"  # Overridden

    def test_merge_with_full_override(self) -> None:
        """Test merge_with with complete style override."""
        base = Style()
        override = Style(
            border_color="#FF0000",
            border_width=10.0,
            font_size=32.0,
            shadow=True,
        )

        merged = base.merge_with(override)
        assert merged.border_color == "#FF0000"
        assert merged.border_width == 10.0
        assert merged.font_size == 32.0
        assert merged.shadow is True

    def test_merge_with_returns_new_style(self) -> None:
        """Test that merge_with returns a new Style instance."""
        base = Style()
        override = Style(border_color="#FF0000")

        merged = base.merge_with(override)
        assert merged is not base
        assert merged is not override


class TestStylePresets:
    """Tests for style presets."""

    def test_manga_style(self) -> None:
        """Test MANGA_STYLE preset."""
        assert MANGA_STYLE.border_color == "#000000"
        assert MANGA_STYLE.border_width == 2.0
        assert MANGA_STYLE.font_size == 14.0

    def test_webtoon_style(self) -> None:
        """Test WEBTOON_STYLE preset."""
        assert WEBTOON_STYLE.border_color == "#333333"
        assert WEBTOON_STYLE.border_width == 0.0
        assert WEBTOON_STYLE.shadow is True
        assert WEBTOON_STYLE.font_size == 16.0

    def test_comic_style(self) -> None:
        """Test COMIC_STYLE preset."""
        assert COMIC_STYLE.border_color == "#000000"
        assert COMIC_STYLE.border_width == 3.0
        assert COMIC_STYLE.font_size == 18.0
        assert COMIC_STYLE.font_weight == "bold"

    def test_minimal_style(self) -> None:
        """Test MINIMAL_STYLE preset."""
        assert MINIMAL_STYLE.border_color == "#CCCCCC"
        assert MINIMAL_STYLE.border_width == 1.0
        assert MINIMAL_STYLE.fill_color == "#FAFAFA"
        assert MINIMAL_STYLE.font_size == 14.0
