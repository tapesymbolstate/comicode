"""Comix - Code-based comic creation framework inspired by Manim."""

from comix.cobject.cobject import CObject
from comix.cobject.panel.panel import Panel
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
from comix.cobject.character.character import Character, Stickman, SimpleFace
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
from comix.layout.constraints import ConstraintLayout, ConstraintPriority
from comix.layout.flow import FlowLayout
from comix.layout.grid import GridLayout
from comix.page.page import Page, SinglePanel, Strip
from comix.parser import parse_markup, MarkupParser, ParseError

# Optional preview module (requires watchdog)
try:
    from comix.preview import PreviewServer, PreviewError, serve as preview_serve
    _PREVIEW_AVAILABLE = True
except ImportError:
    _PREVIEW_AVAILABLE = False
    PreviewServer = None  # type: ignore[misc, assignment]
    PreviewError = None  # type: ignore[misc, assignment]
    preview_serve = None  # type: ignore[misc, assignment]

__all__ = [
    # Core objects
    "CObject",
    "Panel",
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
    # Preview (optional)
    "PreviewServer",
    "PreviewError",
    "preview_serve",
]

__version__ = "0.1.0"
