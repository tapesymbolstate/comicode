"""Tests for font management system."""

from pathlib import Path

import pytest

from comix.style.font import (
    FontInfo,
    FontMetrics,
    FontRegistry,
    get_font_registry,
    get_default_metrics,
    estimate_text_width,
    estimate_text_height,
)


class TestFontInfo:
    """Tests for FontInfo dataclass."""

    def test_default_init(self) -> None:
        """Test creating FontInfo with minimal parameters."""
        info = FontInfo(family="Arial", path=Path("/fonts/arial.ttf"))
        assert info.family == "Arial"
        assert info.path == Path("/fonts/arial.ttf")
        assert info.weight == "normal"
        assert info.style == "normal"
        assert info.full_name == "Arial"

    def test_custom_init(self) -> None:
        """Test creating FontInfo with all parameters."""
        info = FontInfo(
            family="Arial",
            path=Path("/fonts/arial-bold.ttf"),
            weight="bold",
            style="italic",
            full_name="Arial Bold Italic",
        )
        assert info.family == "Arial"
        assert info.weight == "bold"
        assert info.style == "italic"
        assert info.full_name == "Arial Bold Italic"


class TestFontMetrics:
    """Tests for FontMetrics dataclass."""

    def test_init(self) -> None:
        """Test creating FontMetrics."""
        metrics = FontMetrics(
            units_per_em=1000,
            ascender=800,
            descender=-200,
            x_height=500,
            cap_height=700,
            line_gap=0,
            avg_char_width=500,
        )
        assert metrics.units_per_em == 1000
        assert metrics.ascender == 800
        assert metrics.descender == -200

    def test_get_line_height(self) -> None:
        """Test calculating line height."""
        metrics = FontMetrics(
            units_per_em=1000,
            ascender=800,
            descender=-200,
            x_height=500,
            cap_height=700,
            line_gap=100,
            avg_char_width=500,
        )
        # line_height = (800 - (-200) + 100) / 1000 * 16 = 1100/1000 * 16 = 17.6
        line_height = metrics.get_line_height(16.0)
        assert line_height == pytest.approx(17.6)

    def test_get_text_height(self) -> None:
        """Test calculating text height."""
        metrics = FontMetrics(
            units_per_em=1000,
            ascender=800,
            descender=-200,
            x_height=500,
            cap_height=700,
            line_gap=0,
            avg_char_width=500,
        )
        # text_height = (800 - (-200)) / 1000 * 16 = 1000/1000 * 16 = 16
        text_height = metrics.get_text_height(16.0)
        assert text_height == pytest.approx(16.0)

    def test_get_char_width(self) -> None:
        """Test calculating character width."""
        metrics = FontMetrics(
            units_per_em=1000,
            ascender=800,
            descender=-200,
            x_height=500,
            cap_height=700,
            line_gap=0,
            avg_char_width=500,
        )
        # char_width = 500 / 1000 * 16 = 8
        char_width = metrics.get_char_width(16.0)
        assert char_width == pytest.approx(8.0)


class TestFontRegistry:
    """Tests for FontRegistry."""

    def test_init(self) -> None:
        """Test creating FontRegistry."""
        registry = FontRegistry()
        assert registry._fonts == {}
        assert "sans-serif" in registry._fallback_chains
        assert "serif" in registry._fallback_chains

    def test_register_font(self) -> None:
        """Test registering a font."""
        registry = FontRegistry()
        info = FontInfo(family="CustomFont", path=Path("/fonts/custom.ttf"))
        registry.register_font(info)

        assert "customfont:normal:normal" in registry._fonts
        assert "customfont" in registry._fonts

    def test_get_font_exact_match(self) -> None:
        """Test getting a font with exact match."""
        registry = FontRegistry()
        info = FontInfo(
            family="Arial",
            path=Path("/fonts/arial.ttf"),
            weight="normal",
            style="normal",
        )
        registry.register_font(info)

        result = registry.get_font("Arial", "normal", "normal")
        assert result == info

    def test_get_font_case_insensitive(self) -> None:
        """Test getting a font is case insensitive."""
        registry = FontRegistry()
        info = FontInfo(family="Arial", path=Path("/fonts/arial.ttf"))
        registry.register_font(info)

        result = registry.get_font("arial")
        assert result == info

        result = registry.get_font("ARIAL")
        assert result == info

    def test_get_font_not_found(self) -> None:
        """Test getting a font that doesn't exist."""
        registry = FontRegistry()
        result = registry.get_font("NonExistent")
        assert result is None

    def test_fallback_chain(self) -> None:
        """Test that fallback chain works."""
        registry = FontRegistry()
        # Register Arial as fallback for sans-serif
        info = FontInfo(family="Arial", path=Path("/fonts/arial.ttf"))
        registry.register_font(info)

        # Request sans-serif which should fallback to Arial
        result = registry.get_font("sans-serif")
        assert result == info

    def test_set_custom_fallback(self) -> None:
        """Test setting custom fallback chain."""
        registry = FontRegistry()

        # Register custom font
        custom = FontInfo(family="MyFont", path=Path("/fonts/myfont.ttf"))
        registry.register_font(custom)

        # Set MyFont as fallback for "comic"
        registry.set_fallback_chain("custom-family", ["MyFont"])

        result = registry.get_font("custom-family")
        assert result == custom


class TestGlobalRegistry:
    """Tests for global registry functions."""

    def test_get_font_registry(self) -> None:
        """Test getting global font registry."""
        registry = get_font_registry()
        assert isinstance(registry, FontRegistry)

        # Should return same instance
        registry2 = get_font_registry()
        assert registry is registry2

    def test_get_default_metrics(self) -> None:
        """Test getting default font metrics."""
        metrics = get_default_metrics()
        assert isinstance(metrics, FontMetrics)
        assert metrics.units_per_em == 1000
        assert metrics.ascender == 800
        assert metrics.descender == -200


class TestTextMeasurement:
    """Tests for text measurement functions."""

    def test_estimate_text_width(self) -> None:
        """Test estimating text width."""
        width = estimate_text_width("Hello", 16.0)
        # Using default metrics: 500/1000 * 16 = 8 per char, 5 chars = 40
        assert width == pytest.approx(40.0)

    def test_estimate_text_width_empty(self) -> None:
        """Test estimating width of empty text."""
        width = estimate_text_width("", 16.0)
        assert width == 0.0

    def test_estimate_text_height(self) -> None:
        """Test estimating text height."""
        height = estimate_text_height(16.0, line_height=1.0, num_lines=1)
        # Using default metrics: (800 - (-200))/1000 * 16 * 1.0 * 1 = 16
        assert height == pytest.approx(16.0)

    def test_estimate_text_height_multiline(self) -> None:
        """Test estimating height for multiple lines."""
        height = estimate_text_height(16.0, line_height=1.4, num_lines=3)
        # 16 * 1.4 * 3 = 67.2
        assert height == pytest.approx(67.2)


class TestFontDiscovery:
    """Tests for font discovery functionality."""

    def test_discover_system_fonts(self) -> None:
        """Test that font discovery runs without error."""
        registry = FontRegistry()
        # Just verify it runs - actual font count depends on system
        fonts_found = registry.discover_system_fonts()
        # Should find at least 0 fonts (may be more on systems with fonts)
        assert fonts_found >= 0

    def test_default_fallbacks_exist(self) -> None:
        """Test that default fallback chains are initialized."""
        registry = FontRegistry()
        assert "sans-serif" in registry._fallback_chains
        assert "serif" in registry._fallback_chains
        assert "monospace" in registry._fallback_chains
        assert "comic" in registry._fallback_chains
