"""Comix - Code-based comic creation framework inspired by Manim."""

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
    ValidValues,
    validate_value,
)
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
    Anime,
    Cartoon,
    Character,
    Chibi,
    ChubbyStickman,
    Expression,
    Pose,
    Robot,
    SimpleFace,
    Stickman,
    Superhero,
)
from comix.cobject.shapes.shapes import Rectangle, Circle, Line
from comix.cobject.image.image import Image
from comix.cobject.image.ai_image import (
    AIGenerationError,
    AIImage,
    AIImageError,
    AIProvider,
    AIProviderNotAvailableError,
)
from comix.effect.effect import (
    Effect,
    AppearEffect,
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
from comix.page.book import Book
from comix.page.page import Page, SinglePanel, Strip
from comix.page.templates import (
    FourKoma,
    SplashPage,
    TwoByTwo,
    WebComic,
    ThreeRowLayout,
    MangaPage,
    ActionPage,
)
from comix.parser import parse_markup, MarkupParser, ParseError
from comix.renderer.svg_renderer import SVGRenderer
from comix.renderer.html_renderer import HTMLRenderer
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

# Optional animation module (requires pycairo and Pillow)
try:
    from comix.animation import (
        Animation,
        AnimationConfig,
        AnimationGroup,
        EffectAnimation,
        ObjectAnimation,
        PropertyAnimation,
        Timeline,
        TimelineEntry,
        EASING_FUNCTIONS,
        get_easing,
        register_easing,
    )
    from comix.renderer.gif_renderer import GIFRenderer

    _ANIMATION_AVAILABLE = True
except ImportError:
    _ANIMATION_AVAILABLE = False
    Animation = None  # type: ignore[misc, assignment]
    AnimationConfig = None  # type: ignore[misc, assignment]
    AnimationGroup = None  # type: ignore[misc, assignment]
    EffectAnimation = None  # type: ignore[misc, assignment]
    ObjectAnimation = None  # type: ignore[misc, assignment]
    PropertyAnimation = None  # type: ignore[misc, assignment]
    Timeline = None  # type: ignore[misc, assignment]
    TimelineEntry = None  # type: ignore[misc, assignment]
    EASING_FUNCTIONS = None  # type: ignore[assignment]
    get_easing = None  # type: ignore[assignment]
    register_easing = None  # type: ignore[assignment]
    GIFRenderer = None  # type: ignore[misc, assignment]

# Optional video module (requires pycairo, Pillow, and imageio-ffmpeg)
try:
    from comix.renderer.video_renderer import VideoRenderer

    _VIDEO_AVAILABLE = True
except ImportError:
    _VIDEO_AVAILABLE = False
    VideoRenderer = None  # type: ignore[misc, assignment]

__all__ = [
    # Constants
    "VERSION",
    "Colors",
    "Dimensions",
    "Typography",
    "Borders",
    "Effects",
    "Server",
    "Quality",
    "Anchors",
    "Directions",
    "ValidValues",
    # Validation utilities
    "validate_value",
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
    "Anime",
    "Cartoon",
    "Character",
    "Chibi",
    "ChubbyStickman",
    "Expression",
    "Pose",
    "Robot",
    "SimpleFace",
    "Stickman",
    "Superhero",
    # Shapes
    "Rectangle",
    "Circle",
    "Line",
    # Images
    "AIGenerationError",
    "AIImage",
    "AIImageError",
    "AIProvider",
    "AIProviderNotAvailableError",
    "Image",
    # Effects
    "Effect",
    "AppearEffect",
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
    # Page and Book
    "Book",
    "Page",
    "SinglePanel",
    "Strip",
    # Page Templates
    "FourKoma",
    "SplashPage",
    "TwoByTwo",
    "WebComic",
    "ThreeRowLayout",
    "MangaPage",
    "ActionPage",
    # Parser
    "parse_markup",
    "MarkupParser",
    "ParseError",
    # Renderers
    "SVGRenderer",
    "CairoRenderer",
    "HTMLRenderer",
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
    # Animation (optional)
    "Animation",
    "AnimationConfig",
    "AnimationGroup",
    "EffectAnimation",
    "ObjectAnimation",
    "PropertyAnimation",
    "Timeline",
    "TimelineEntry",
    "EASING_FUNCTIONS",
    "get_easing",
    "register_easing",
    "GIFRenderer",
    # Video (optional)
    "VideoRenderer",
]

__version__ = VERSION
