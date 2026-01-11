"""Comix - Code-based comic creation framework inspired by Manim."""

from comix.cobject.cobject import CObject
from comix.cobject.panel.panel import Panel, Border
from comix.cobject.bubble.bubble import (
    Bubble,
    SpeechBubble,
    ThoughtBubble,
    ShoutBubble,
    WhisperBubble,
    NarratorBubble,
    auto_position_bubbles,
)
from comix.cobject.text.text import Text, StyledText, SFX
from comix.cobject.character.character import (
    Character,
    Stickman,
    SimpleFace,
    Expression,
    Pose,
)
from comix.cobject.shapes.shapes import Rectangle, Circle, Line
from comix.cobject.image.image import Image
from comix.cobject.image.ai_image import AIImage, AIProvider, AIImageError
from comix.effect.effect import (
    Effect,
    ShakeEffect,
    ZoomEffect,
    MotionLines,
    FocusLines,
    ImpactEffect,
)
from comix.layout.constraints import (
    ConstraintLayout,
    ConstraintPriority,
    ConstraintValue,
    ElementRef,
)
from comix.layout.flow import FlowLayout
from comix.layout.grid import GridLayout
from comix.page.page import Page, SinglePanel, Strip
from comix.parser import parse_markup, MarkupParser, ParseError
from comix.renderer.svg_renderer import SVGRenderer
from comix.style.style import (
    Style,
    MANGA_STYLE,
    WEBTOON_STYLE,
    COMIC_STYLE,
    MINIMAL_STYLE,
)
from comix.style.font import (
    FontInfo,
    FontMetrics,
    FontRegistry,
    get_font_registry,
    estimate_text_width,
    estimate_text_height,
    is_fullwidth_char,
    calculate_text_width_with_cjk,
)
from comix.style.theme import (
    Theme,
    ColorPalette,
    ThemeRegistry,
    MANGA_THEME,
    WEBTOON_THEME,
    COMIC_THEME,
    MINIMAL_THEME,
    get_theme,
    get_default_theme,
    set_default_theme,
    register_theme,
    get_theme_registry,
)
from comix.utils.geometry import (
    distance,
    midpoint,
    bounding_box,
    normalize_angle,
    angle_between,
    rotate_point,
    rotate_points,
    translate_points,
    scale_points,
)
from comix.utils.bezier import create_bubble_path, create_tail_points

# Optional Cairo renderer (requires pycairo)
try:
    from comix.renderer.cairo_renderer import CairoRenderer

    _CAIRO_AVAILABLE = True
except ImportError:
    _CAIRO_AVAILABLE = False
    CairoRenderer = None  # type: ignore[misc, assignment]

# Optional preview module (requires watchdog)
try:
    from comix.preview import PreviewServer, PreviewError, serve as preview_serve

    _PREVIEW_AVAILABLE = True
except ImportError:
    _PREVIEW_AVAILABLE = False
    PreviewServer = None  # type: ignore[misc, assignment]
    PreviewError = None  # type: ignore[misc, assignment]
    preview_serve = None  # type: ignore[assignment]

__all__ = [
    # Core objects
    "CObject",
    "Panel",
    "Border",
    # Bubbles
    "Bubble",
    "SpeechBubble",
    "ThoughtBubble",
    "ShoutBubble",
    "WhisperBubble",
    "NarratorBubble",
    "auto_position_bubbles",
    # Text
    "Text",
    "StyledText",
    "SFX",
    # Characters
    "Character",
    "Stickman",
    "SimpleFace",
    "Expression",
    "Pose",
    # Shapes
    "Rectangle",
    "Circle",
    "Line",
    # Images
    "Image",
    "AIImage",
    "AIProvider",
    "AIImageError",
    # Effects
    "Effect",
    "ShakeEffect",
    "ZoomEffect",
    "MotionLines",
    "FocusLines",
    "ImpactEffect",
    # Layout
    "ConstraintLayout",
    "ConstraintPriority",
    "ConstraintValue",
    "ElementRef",
    "FlowLayout",
    "GridLayout",
    # Page
    "Page",
    "SinglePanel",
    "Strip",
    # Parser
    "parse_markup",
    "MarkupParser",
    "ParseError",
    # Renderers
    "SVGRenderer",
    "CairoRenderer",
    # Style
    "Style",
    "MANGA_STYLE",
    "WEBTOON_STYLE",
    "COMIC_STYLE",
    "MINIMAL_STYLE",
    # Font utilities
    "FontInfo",
    "FontMetrics",
    "FontRegistry",
    "get_font_registry",
    "estimate_text_width",
    "estimate_text_height",
    "is_fullwidth_char",
    "calculate_text_width_with_cjk",
    # Theme
    "Theme",
    "ColorPalette",
    "ThemeRegistry",
    "MANGA_THEME",
    "WEBTOON_THEME",
    "COMIC_THEME",
    "MINIMAL_THEME",
    "get_theme",
    "get_default_theme",
    "set_default_theme",
    "register_theme",
    "get_theme_registry",
    # Geometry utilities
    "distance",
    "midpoint",
    "bounding_box",
    "normalize_angle",
    "angle_between",
    "rotate_point",
    "rotate_points",
    "translate_points",
    "scale_points",
    # Bezier utilities
    "create_bubble_path",
    "create_tail_points",
    # Preview (optional)
    "PreviewServer",
    "PreviewError",
    "preview_serve",
]

__version__ = "0.1.0"
