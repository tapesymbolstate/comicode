"""Constants and default values for the Comix framework.

This module centralizes commonly used default values to ensure consistency
across the framework and make it easy to adjust defaults in one place.
"""

from typing import Final

# =============================================================================
# VERSION
# =============================================================================

VERSION: Final[str] = "0.1.74"

# =============================================================================
# COLORS - Standard colors used throughout the framework
# =============================================================================


class Colors:
    """Standard color constants used across the framework."""

    # Primary colors
    BLACK: Final[str] = "#000000"
    WHITE: Final[str] = "#FFFFFF"

    # Grayscale
    GRAY_100: Final[str] = "#FAFAFA"  # Lightest
    GRAY_200: Final[str] = "#F5F5F5"
    GRAY_300: Final[str] = "#EEEEEE"
    GRAY_400: Final[str] = "#CCCCCC"
    GRAY_500: Final[str] = "#999999"
    GRAY_600: Final[str] = "#666666"
    GRAY_700: Final[str] = "#333333"
    GRAY_800: Final[str] = "#1A1A1A"  # Darkest

    # Transparent variations
    SHADOW: Final[str] = "#00000033"  # 20% black for shadows
    SHADOW_DARK: Final[str] = "#00000066"  # 40% black for darker shadows

    # Paper colors (for backgrounds)
    PAPER_WHITE: Final[str] = "#FFFFFF"
    PAPER_CREAM: Final[str] = "#FFFEF0"
    PAPER_WARM: Final[str] = "#FFF8E7"

    # Default element colors
    DEFAULT_STROKE: Final[str] = BLACK
    DEFAULT_FILL: Final[str] = WHITE
    DEFAULT_TEXT: Final[str] = BLACK
    DEFAULT_BACKGROUND: Final[str] = WHITE


# =============================================================================
# DIMENSIONS - Standard sizes and measurements
# =============================================================================


class Dimensions:
    """Standard dimensions used across the framework."""

    # Page sizes (width x height)
    PAGE_WIDTH: Final[float] = 800.0
    PAGE_HEIGHT: Final[float] = 1200.0

    # Preview/viewport sizes
    PREVIEW_WIDTH: Final[float] = 800.0
    PREVIEW_HEIGHT: Final[float] = 600.0

    # Default element sizes
    DEFAULT_SIZE: Final[float] = 100.0
    DEFAULT_PANEL_SIZE: Final[float] = 300.0
    DEFAULT_CELL_SIZE: Final[float] = 200.0

    # Layout spacing
    DEFAULT_MARGIN: Final[float] = 20.0
    DEFAULT_GUTTER: Final[float] = 10.0
    DEFAULT_PADDING: Final[float] = 10.0

    # Bubble padding (top, right, bottom, left)
    BUBBLE_PADDING: Final[tuple[float, float, float, float]] = (15.0, 20.0, 15.0, 20.0)

    # Character
    DEFAULT_CHARACTER_HEIGHT: Final[float] = 100.0


# =============================================================================
# TYPOGRAPHY - Font-related constants
# =============================================================================


class Typography:
    """Typography constants used across the framework."""

    # Default font settings
    DEFAULT_FONT_FAMILY: Final[str] = "sans-serif"
    DEFAULT_FONT_SIZE: Final[float] = 16.0
    DEFAULT_LINE_HEIGHT: Final[float] = 1.4

    # Font size presets
    FONT_SIZE_SMALL: Final[float] = 12.0
    FONT_SIZE_NORMAL: Final[float] = 14.0
    FONT_SIZE_MEDIUM: Final[float] = 16.0
    FONT_SIZE_LARGE: Final[float] = 18.0
    FONT_SIZE_XLARGE: Final[float] = 24.0
    FONT_SIZE_TITLE: Final[float] = 32.0

    # Text width estimation ratios
    CJK_WIDTH_RATIO: Final[float] = 0.6  # CJK characters relative to font size
    LATIN_WIDTH_RATIO: Final[float] = 0.5  # Latin characters relative to font size


# =============================================================================
# BORDERS - Border-related constants
# =============================================================================


class Borders:
    """Border constants used across the framework."""

    # Border widths
    WIDTH_NONE: Final[float] = 0.0
    WIDTH_THIN: Final[float] = 1.0
    WIDTH_NORMAL: Final[float] = 2.0
    WIDTH_THICK: Final[float] = 3.0
    WIDTH_BOLD: Final[float] = 4.0

    # Border styles
    STYLE_SOLID: Final[str] = "solid"
    STYLE_DASHED: Final[str] = "dashed"
    STYLE_DOTTED: Final[str] = "dotted"

    # Corner radii
    RADIUS_NONE: Final[float] = 0.0
    RADIUS_SMALL: Final[float] = 5.0
    RADIUS_MEDIUM: Final[float] = 10.0
    RADIUS_LARGE: Final[float] = 20.0
    RADIUS_ROUND: Final[float] = 999.0  # Fully rounded


# =============================================================================
# EFFECTS - Effect-related constants
# =============================================================================


class Effects:
    """Effect constants used across the framework."""

    # Default effect values
    DEFAULT_INTENSITY: Final[float] = 1.0
    DEFAULT_OPACITY: Final[float] = 1.0

    # Shake effect
    SHAKE_DEFAULT_COUNT: Final[int] = 3
    SHAKE_DEFAULT_OFFSET: Final[float] = 5.0

    # Zoom effect
    ZOOM_DEFAULT_SCALE: Final[float] = 1.2
    ZOOM_DEFAULT_LINES: Final[int] = 12

    # Motion lines
    MOTION_DEFAULT_COUNT: Final[int] = 8
    MOTION_DEFAULT_LENGTH: Final[float] = 50.0

    # Focus lines
    FOCUS_DEFAULT_COUNT: Final[int] = 24
    FOCUS_DEFAULT_MIN_LENGTH: Final[float] = 100.0
    FOCUS_DEFAULT_MAX_LENGTH: Final[float] = 300.0


# =============================================================================
# SERVER - Network-related constants
# =============================================================================


class Server:
    """Server constants for preview functionality."""

    DEFAULT_HOST: Final[str] = "localhost"
    DEFAULT_PORT: Final[int] = 8000


# =============================================================================
# QUALITY - Rendering quality constants
# =============================================================================


class Quality:
    """Rendering quality constants."""

    # DPI settings
    DPI_LOW: Final[int] = 72
    DPI_MEDIUM: Final[int] = 150
    DPI_HIGH: Final[int] = 300

    # Quality level names
    LEVEL_LOW: Final[str] = "low"
    LEVEL_MEDIUM: Final[str] = "medium"
    LEVEL_HIGH: Final[str] = "high"


# =============================================================================
# ANCHOR POSITIONS - Standard positioning anchors
# =============================================================================


class Anchors:
    """Anchor position constants for element positioning."""

    # Corners
    TOP_LEFT: Final[str] = "top-left"
    TOP_RIGHT: Final[str] = "top-right"
    BOTTOM_LEFT: Final[str] = "bottom-left"
    BOTTOM_RIGHT: Final[str] = "bottom-right"

    # Edges
    TOP: Final[str] = "top"
    BOTTOM: Final[str] = "bottom"
    LEFT: Final[str] = "left"
    RIGHT: Final[str] = "right"

    # Center
    CENTER: Final[str] = "center"

    # Sides (aliases)
    SIDE_LEFT: Final[str] = "side-left"
    SIDE_RIGHT: Final[str] = "side-right"


# =============================================================================
# DIRECTIONS - Direction constants
# =============================================================================


class Directions:
    """Direction constants for facing and movement."""

    LEFT: Final[str] = "left"
    RIGHT: Final[str] = "right"
    UP: Final[str] = "up"
    DOWN: Final[str] = "down"
    FRONT: Final[str] = "front"
    BACK: Final[str] = "back"
    HORIZONTAL: Final[str] = "horizontal"
    VERTICAL: Final[str] = "vertical"


# =============================================================================
# VALID VALUES - Sets of valid parameter values for validation
# =============================================================================


class ValidValues:
    """Valid parameter values for validation."""

    # Border styles
    BORDER_STYLES: Final[frozenset[str]] = frozenset(
        {"solid", "dashed", "dotted", "none"}
    )

    # Bubble types
    BUBBLE_TYPES: Final[frozenset[str]] = frozenset(
        {"speech", "thought", "shout", "whisper", "narrator"}
    )

    # Text alignments
    TEXT_ALIGNMENTS: Final[frozenset[str]] = frozenset({"left", "center", "right"})

    # Quality levels
    QUALITY_LEVELS: Final[frozenset[str]] = frozenset({"low", "medium", "high"})

    # Facing directions
    FACING_DIRECTIONS: Final[frozenset[str]] = frozenset(
        {"left", "right", "front", "back"}
    )

    # Positioning directions
    POSITION_DIRECTIONS: Final[frozenset[str]] = frozenset(
        {"up", "down", "left", "right"}
    )

    # Edge alignments
    EDGE_ALIGNMENTS: Final[frozenset[str]] = frozenset(
        {"top", "bottom", "left", "right", "center"}
    )

    # Flow directions
    FLOW_DIRECTIONS: Final[frozenset[str]] = frozenset({"horizontal", "vertical"})


# =============================================================================
# VALIDATION UTILITIES
# =============================================================================


def validate_value(
    value: str,
    valid_set: frozenset[str],
    param_name: str,
    context: str = "",
) -> None:
    """Validate that a value is in a set of valid values.

    Args:
        value: The value to validate.
        valid_set: Set of valid values.
        param_name: Name of the parameter (for error messages).
        context: Optional context string (e.g., class name).

    Raises:
        ValueError: If value is not in valid_set.
    """
    if value not in valid_set:
        valid_list = ", ".join(sorted(valid_set))
        ctx = f" in {context}" if context else ""
        raise ValueError(
            f"Invalid {param_name}{ctx}: '{value}'. "
            f"Must be one of: {valid_list}"
        )
