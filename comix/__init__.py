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
from comix.effect.effect import (
    Effect,
    ShakeEffect,
    ZoomEffect,
    MotionLines,
    FocusLines,
    ImpactEffect,
)
from comix.layout.flow import FlowLayout
from comix.layout.grid import GridLayout
from comix.page.page import Page, SinglePanel, Strip
from comix.parser import parse_markup, MarkupParser, ParseError

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
    # Effects
    "Effect",
    "ShakeEffect",
    "ZoomEffect",
    "MotionLines",
    "FocusLines",
    "ImpactEffect",
    # Layout
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
]

__version__ = "0.1.0"
