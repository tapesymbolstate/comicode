"""Tests for the constants module."""

from comix.constants import (
    VERSION,
    Colors,
    Dimensions,
    Typography,
    Borders,
    Effects,
    Server,
    Quality,
    Anchors,
    Directions,
)


class TestVersion:
    """Tests for VERSION constant."""

    def test_version_is_string(self) -> None:
        """VERSION should be a string."""
        assert isinstance(VERSION, str)

    def test_version_format(self) -> None:
        """VERSION should follow semver format."""
        parts = VERSION.split(".")
        assert len(parts) == 3
        assert all(part.isdigit() for part in parts)


class TestColors:
    """Tests for Colors constants."""

    def test_black_is_hex_black(self) -> None:
        """BLACK should be the hex code for black."""
        assert Colors.BLACK == "#000000"

    def test_white_is_hex_white(self) -> None:
        """WHITE should be the hex code for white."""
        assert Colors.WHITE == "#FFFFFF"

    def test_all_colors_are_hex_strings(self) -> None:
        """All color constants should be valid hex color strings."""
        color_attrs = [
            attr for attr in dir(Colors)
            if not attr.startswith("_") and isinstance(getattr(Colors, attr), str)
        ]
        for attr in color_attrs:
            color = getattr(Colors, attr)
            assert color.startswith("#"), f"{attr} should start with #"
            # Should be 7 chars (#RRGGBB) or 9 chars (#RRGGBBAA)
            assert len(color) in (7, 9), f"{attr} should be 7 or 9 chars"

    def test_default_colors_exist(self) -> None:
        """Default color aliases should exist."""
        assert Colors.DEFAULT_STROKE == Colors.BLACK
        assert Colors.DEFAULT_FILL == Colors.WHITE
        assert Colors.DEFAULT_TEXT == Colors.BLACK
        assert Colors.DEFAULT_BACKGROUND == Colors.WHITE


class TestDimensions:
    """Tests for Dimensions constants."""

    def test_page_dimensions(self) -> None:
        """Page dimensions should be the standard 800x1200."""
        assert Dimensions.PAGE_WIDTH == 800.0
        assert Dimensions.PAGE_HEIGHT == 1200.0

    def test_preview_dimensions(self) -> None:
        """Preview dimensions should be 800x600."""
        assert Dimensions.PREVIEW_WIDTH == 800.0
        assert Dimensions.PREVIEW_HEIGHT == 600.0

    def test_default_sizes_are_positive(self) -> None:
        """All default sizes should be positive numbers."""
        assert Dimensions.DEFAULT_SIZE > 0
        assert Dimensions.DEFAULT_PANEL_SIZE > 0
        assert Dimensions.DEFAULT_CELL_SIZE > 0
        assert Dimensions.DEFAULT_MARGIN >= 0
        assert Dimensions.DEFAULT_GUTTER >= 0
        assert Dimensions.DEFAULT_PADDING >= 0
        assert Dimensions.DEFAULT_CHARACTER_HEIGHT > 0

    def test_bubble_padding_is_tuple(self) -> None:
        """Bubble padding should be a 4-tuple."""
        assert isinstance(Dimensions.BUBBLE_PADDING, tuple)
        assert len(Dimensions.BUBBLE_PADDING) == 4
        assert all(p >= 0 for p in Dimensions.BUBBLE_PADDING)


class TestTypography:
    """Tests for Typography constants."""

    def test_default_font_family(self) -> None:
        """Default font family should be sans-serif."""
        assert Typography.DEFAULT_FONT_FAMILY == "sans-serif"

    def test_default_font_size(self) -> None:
        """Default font size should be 16."""
        assert Typography.DEFAULT_FONT_SIZE == 16.0

    def test_default_line_height(self) -> None:
        """Default line height should be 1.4."""
        assert Typography.DEFAULT_LINE_HEIGHT == 1.4

    def test_font_sizes_are_ordered(self) -> None:
        """Font size presets should be in ascending order."""
        sizes = [
            Typography.FONT_SIZE_SMALL,
            Typography.FONT_SIZE_NORMAL,
            Typography.FONT_SIZE_MEDIUM,
            Typography.FONT_SIZE_LARGE,
            Typography.FONT_SIZE_XLARGE,
            Typography.FONT_SIZE_TITLE,
        ]
        assert sizes == sorted(sizes)

    def test_width_ratios_are_valid(self) -> None:
        """Width ratios should be between 0 and 1."""
        assert 0 < Typography.CJK_WIDTH_RATIO <= 1
        assert 0 < Typography.LATIN_WIDTH_RATIO <= 1


class TestBorders:
    """Tests for Borders constants."""

    def test_border_widths_are_ordered(self) -> None:
        """Border width presets should be in ascending order."""
        widths = [
            Borders.WIDTH_NONE,
            Borders.WIDTH_THIN,
            Borders.WIDTH_NORMAL,
            Borders.WIDTH_THICK,
            Borders.WIDTH_BOLD,
        ]
        assert widths == sorted(widths)

    def test_border_styles(self) -> None:
        """Border styles should be valid CSS-like values."""
        assert Borders.STYLE_SOLID == "solid"
        assert Borders.STYLE_DASHED == "dashed"
        assert Borders.STYLE_DOTTED == "dotted"

    def test_corner_radii_are_ordered(self) -> None:
        """Corner radius presets should be in ascending order."""
        radii = [
            Borders.RADIUS_NONE,
            Borders.RADIUS_SMALL,
            Borders.RADIUS_MEDIUM,
            Borders.RADIUS_LARGE,
            Borders.RADIUS_ROUND,
        ]
        assert radii == sorted(radii)


class TestEffects:
    """Tests for Effects constants."""

    def test_default_intensity_and_opacity(self) -> None:
        """Default intensity and opacity should be 1.0."""
        assert Effects.DEFAULT_INTENSITY == 1.0
        assert Effects.DEFAULT_OPACITY == 1.0

    def test_shake_defaults_are_positive(self) -> None:
        """Shake effect defaults should be positive."""
        assert Effects.SHAKE_DEFAULT_COUNT > 0
        assert Effects.SHAKE_DEFAULT_OFFSET > 0

    def test_zoom_defaults_are_positive(self) -> None:
        """Zoom effect defaults should be positive."""
        assert Effects.ZOOM_DEFAULT_SCALE > 0
        assert Effects.ZOOM_DEFAULT_LINES > 0

    def test_motion_defaults_are_positive(self) -> None:
        """Motion lines defaults should be positive."""
        assert Effects.MOTION_DEFAULT_COUNT > 0
        assert Effects.MOTION_DEFAULT_LENGTH > 0

    def test_focus_defaults_are_positive(self) -> None:
        """Focus lines defaults should be positive."""
        assert Effects.FOCUS_DEFAULT_COUNT > 0
        assert Effects.FOCUS_DEFAULT_MIN_LENGTH > 0
        assert Effects.FOCUS_DEFAULT_MAX_LENGTH > Effects.FOCUS_DEFAULT_MIN_LENGTH


class TestServer:
    """Tests for Server constants."""

    def test_default_host(self) -> None:
        """Default host should be localhost."""
        assert Server.DEFAULT_HOST == "localhost"

    def test_default_port(self) -> None:
        """Default port should be 8000."""
        assert Server.DEFAULT_PORT == 8000


class TestQuality:
    """Tests for Quality constants."""

    def test_dpi_values_are_ordered(self) -> None:
        """DPI values should be in ascending order."""
        assert Quality.DPI_LOW < Quality.DPI_MEDIUM < Quality.DPI_HIGH

    def test_quality_level_names(self) -> None:
        """Quality level names should be standard."""
        assert Quality.LEVEL_LOW == "low"
        assert Quality.LEVEL_MEDIUM == "medium"
        assert Quality.LEVEL_HIGH == "high"


class TestAnchors:
    """Tests for Anchors constants."""

    def test_corner_anchors(self) -> None:
        """Corner anchor constants should exist."""
        assert Anchors.TOP_LEFT == "top-left"
        assert Anchors.TOP_RIGHT == "top-right"
        assert Anchors.BOTTOM_LEFT == "bottom-left"
        assert Anchors.BOTTOM_RIGHT == "bottom-right"

    def test_edge_anchors(self) -> None:
        """Edge anchor constants should exist."""
        assert Anchors.TOP == "top"
        assert Anchors.BOTTOM == "bottom"
        assert Anchors.LEFT == "left"
        assert Anchors.RIGHT == "right"

    def test_center_anchor(self) -> None:
        """Center anchor constant should exist."""
        assert Anchors.CENTER == "center"


class TestDirections:
    """Tests for Directions constants."""

    def test_basic_directions(self) -> None:
        """Basic direction constants should exist."""
        assert Directions.LEFT == "left"
        assert Directions.RIGHT == "right"
        assert Directions.UP == "up"
        assert Directions.DOWN == "down"

    def test_facing_directions(self) -> None:
        """Facing direction constants should exist."""
        assert Directions.FRONT == "front"
        assert Directions.BACK == "back"

    def test_orientation_directions(self) -> None:
        """Orientation constants should exist."""
        assert Directions.HORIZONTAL == "horizontal"
        assert Directions.VERTICAL == "vertical"


class TestModuleExports:
    """Tests for module exports from comix package."""

    def test_constants_exported_from_main_package(self) -> None:
        """Constants should be accessible from the main comix package."""
        import comix

        assert hasattr(comix, "VERSION")
        assert hasattr(comix, "Colors")
        assert hasattr(comix, "Dimensions")
        assert hasattr(comix, "Typography")
        assert hasattr(comix, "Borders")
        assert hasattr(comix, "Effects")
        assert hasattr(comix, "Server")
        assert hasattr(comix, "Quality")
        assert hasattr(comix, "Anchors")
        assert hasattr(comix, "Directions")

    def test_version_matches_package_version(self) -> None:
        """VERSION should match __version__."""
        import comix

        assert comix.VERSION == comix.__version__
