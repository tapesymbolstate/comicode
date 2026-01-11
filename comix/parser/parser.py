"""Markup Parser for Comix DSL.

Parses a simple markup language to create comic pages:

    [page 2x2]

    # panel 1
    철수(left, surprised): "뭐라고?!"
    영희(right, smug): "응, 진짜야"

    # panel 2
    철수(closeup): "..."
    sfx: 충격

    # panel 3
    [background: 카페 전경]
    narrator: "그날 이후..."

    # panel 4
    철수(center): "믿을 수 없어"
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from comix.page.page import Page


class ParseError(Exception):
    """Error raised when parsing fails."""

    def __init__(self, message: str, line_number: int = 0, line: str = "") -> None:
        self.line_number = line_number
        self.line = line
        super().__init__(f"Line {line_number}: {message}\n  {line}")


@dataclass
class CharacterAction:
    """Represents a character's action in a panel."""

    name: str
    text: str
    expression: str = "neutral"
    position: str = "center"
    facing: str = "right"
    bubble_type: str = "speech"  # speech, thought, shout, whisper


@dataclass
class SFXAction:
    """Represents a sound effect in a panel."""

    text: str
    position: tuple[float, float] | None = None


@dataclass
class NarratorAction:
    """Represents a narrator box in a panel."""

    text: str


@dataclass
class BackgroundDirective:
    """Represents a background setting for a panel."""

    description: str


@dataclass
class PanelSpec:
    """Specification for a single panel."""

    number: int
    actions: list[CharacterAction | SFXAction | NarratorAction | BackgroundDirective] = field(
        default_factory=list
    )
    background: str | None = None


@dataclass
class PageSpec:
    """Specification for a comic page."""

    rows: int
    cols: int
    panels: list[PanelSpec] = field(default_factory=list)
    width: float = 800.0
    height: float = 1200.0


# Pattern definitions
PAGE_PATTERN = re.compile(r"^\s*\[page\s+(\d+)x(\d+)(?:\s+(\d+)x(\d+))?\]\s*$")
PANEL_PATTERN = re.compile(r"^\s*#\s*panel\s+(\d+)\s*$", re.IGNORECASE)
CHARACTER_PATTERN = re.compile(
    r"^\s*([가-힣\w]+)\s*\(([^)]*)\)\s*:\s*[\"'](.+?)[\"']\s*$"
)
SFX_PATTERN = re.compile(r"^\s*sfx\s*:\s*(.+?)\s*$", re.IGNORECASE)
NARRATOR_PATTERN = re.compile(r"^\s*narrator\s*:\s*[\"'](.+?)[\"']\s*$", re.IGNORECASE)
BACKGROUND_PATTERN = re.compile(r"^\s*\[background\s*:\s*(.+?)\]\s*$", re.IGNORECASE)

# Known modifiers
EXPRESSIONS = {"neutral", "happy", "sad", "angry", "surprised", "confused", "smug"}
POSITIONS = {"left", "right", "center", "closeup", "top", "bottom"}
DIRECTIONS = {"left", "right", "front", "back"}
BUBBLE_TYPES = {"speech", "thought", "think", "shout", "whisper"}


def _parse_modifiers(modifier_str: str) -> dict[str, str]:
    """Parse modifier string into expression, position, facing, bubble_type.

    Examples:
        "left, surprised" -> {"position": "left", "expression": "surprised"}
        "right" -> {"position": "right"}
        "closeup" -> {"position": "closeup"}
        "left, thought" -> {"position": "left", "bubble_type": "thought"}
    """
    result: dict[str, str] = {
        "expression": "neutral",
        "position": "center",
        "facing": "right",
        "bubble_type": "speech",
    }

    if not modifier_str.strip():
        return result

    parts = [p.strip().lower() for p in modifier_str.split(",")]

    for part in parts:
        if part in EXPRESSIONS:
            result["expression"] = part
        elif part in POSITIONS:
            result["position"] = part
            # Set facing based on position for left/right
            if part == "left":
                result["facing"] = "right"
            elif part == "right":
                result["facing"] = "left"
        elif part in DIRECTIONS:
            result["facing"] = part
        elif part in BUBBLE_TYPES:
            # Normalize "think" to "thought"
            result["bubble_type"] = "thought" if part == "think" else part

    return result


class MarkupParser:
    """Parser for Comix markup language."""

    def __init__(self, text: str) -> None:
        self.text = text
        self.lines = text.split("\n")
        self.current_line = 0
        self._page_spec: PageSpec | None = None
        self._current_panel: PanelSpec | None = None

    def parse(self) -> PageSpec:
        """Parse the markup and return a PageSpec."""
        self._page_spec = None
        self._current_panel = None

        for i, line in enumerate(self.lines):
            self.current_line = i + 1
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("//") or stripped.startswith("#!"):
                continue

            # Try to match each pattern
            if self._try_page(stripped):
                continue
            if self._try_panel(stripped):
                continue
            if self._try_background(stripped):
                continue
            if self._try_narrator(stripped):
                continue
            if self._try_sfx(stripped):
                continue
            if self._try_character(stripped):
                continue

            # If starts with #, it might be a panel marker we don't recognize
            if stripped.startswith("#"):
                continue  # Ignore unrecognized # lines as comments

        # Finalize last panel
        if self._current_panel and self._page_spec:
            self._page_spec.panels.append(self._current_panel)

        if self._page_spec is None:
            # Create default page if none specified
            self._page_spec = PageSpec(rows=1, cols=1)

        # Ensure we have enough panels for the grid
        expected_panels = self._page_spec.rows * self._page_spec.cols
        while len(self._page_spec.panels) < expected_panels:
            panel_num = len(self._page_spec.panels) + 1
            self._page_spec.panels.append(PanelSpec(number=panel_num))

        return self._page_spec

    def _try_page(self, line: str) -> bool:
        """Try to parse a page declaration."""
        match = PAGE_PATTERN.match(line)
        if match:
            rows = int(match.group(1))
            cols = int(match.group(2))
            width = 800.0
            height = 1200.0
            if match.group(3) and match.group(4):
                width = float(match.group(3))
                height = float(match.group(4))
            self._page_spec = PageSpec(rows=rows, cols=cols, width=width, height=height)
            return True
        return False

    def _try_panel(self, line: str) -> bool:
        """Try to parse a panel marker."""
        match = PANEL_PATTERN.match(line)
        if match:
            # Save current panel
            if self._current_panel and self._page_spec:
                self._page_spec.panels.append(self._current_panel)

            # Create page spec if not exists
            if self._page_spec is None:
                self._page_spec = PageSpec(rows=1, cols=1)

            panel_num = int(match.group(1))
            self._current_panel = PanelSpec(number=panel_num)
            return True
        return False

    def _try_background(self, line: str) -> bool:
        """Try to parse a background directive."""
        match = BACKGROUND_PATTERN.match(line)
        if match:
            description = match.group(1).strip()

            # Ensure we have a panel
            if self._current_panel is None:
                if self._page_spec is None:
                    self._page_spec = PageSpec(rows=1, cols=1)
                self._current_panel = PanelSpec(number=1)

            self._current_panel.background = description
            self._current_panel.actions.append(BackgroundDirective(description=description))
            return True
        return False

    def _try_narrator(self, line: str) -> bool:
        """Try to parse a narrator line."""
        match = NARRATOR_PATTERN.match(line)
        if match:
            text = match.group(1)

            # Ensure we have a panel
            if self._current_panel is None:
                if self._page_spec is None:
                    self._page_spec = PageSpec(rows=1, cols=1)
                self._current_panel = PanelSpec(number=1)

            self._current_panel.actions.append(NarratorAction(text=text))
            return True
        return False

    def _try_sfx(self, line: str) -> bool:
        """Try to parse a sound effect line."""
        match = SFX_PATTERN.match(line)
        if match:
            text = match.group(1).strip()

            # Ensure we have a panel
            if self._current_panel is None:
                if self._page_spec is None:
                    self._page_spec = PageSpec(rows=1, cols=1)
                self._current_panel = PanelSpec(number=1)

            self._current_panel.actions.append(SFXAction(text=text))
            return True
        return False

    def _try_character(self, line: str) -> bool:
        """Try to parse a character dialogue line."""
        match = CHARACTER_PATTERN.match(line)
        if match:
            name = match.group(1)
            modifiers_str = match.group(2)
            text = match.group(3)

            modifiers = _parse_modifiers(modifiers_str)

            # Ensure we have a panel
            if self._current_panel is None:
                if self._page_spec is None:
                    self._page_spec = PageSpec(rows=1, cols=1)
                self._current_panel = PanelSpec(number=1)

            action = CharacterAction(
                name=name,
                text=text,
                expression=modifiers["expression"],
                position=modifiers["position"],
                facing=modifiers["facing"],
                bubble_type=modifiers["bubble_type"],
            )
            self._current_panel.actions.append(action)
            return True
        return False

    def to_page(self) -> "Page":
        """Parse and convert to a Page object."""
        from comix.page.page import Page
        from comix.cobject.panel.panel import Panel
        from comix.cobject.character.character import Stickman
        from comix.cobject.bubble.bubble import (
            SpeechBubble,
            ThoughtBubble,
            ShoutBubble,
            WhisperBubble,
            NarratorBubble,
        )
        from comix.cobject.text.text import SFX

        spec = self.parse()

        # Create page
        page = Page(width=spec.width, height=spec.height)
        page.set_layout(rows=spec.rows, cols=spec.cols)

        # Character position mapping (relative to panel center)
        position_offsets = {
            "left": (-80, 0),
            "right": (80, 0),
            "center": (0, 0),
            "closeup": (0, 0),
            "top": (0, 50),
            "bottom": (0, -50),
        }

        # Create panels
        for panel_spec in spec.panels:
            panel = Panel(name=f"Panel_{panel_spec.number}")
            page.add(panel)

            # Track characters for bubble attachment
            characters: dict[str, Stickman] = {}
            bubbles = []

            for action in panel_spec.actions:
                if isinstance(action, CharacterAction):
                    # Get or create character
                    if action.name not in characters:
                        offset = position_offsets.get(action.position, (0, 0))
                        char = Stickman(action.name)
                        char.shift(offset)
                        char.set_expression(action.expression)
                        char.face(action.facing)
                        characters[action.name] = char
                        panel.add(char)
                    else:
                        char = characters[action.name]
                        char.set_expression(action.expression)

                    # Create appropriate bubble type
                    bubble: SpeechBubble | ThoughtBubble | ShoutBubble | WhisperBubble
                    if action.bubble_type == "thought":
                        bubble = ThoughtBubble(action.text)
                    elif action.bubble_type == "shout":
                        bubble = ShoutBubble(action.text)
                    elif action.bubble_type == "whisper":
                        bubble = WhisperBubble(action.text)
                    else:
                        bubble = SpeechBubble(action.text)

                    bubble.attach_to(char)
                    bubbles.append(bubble)
                    panel.add(bubble)

                elif isinstance(action, SFXAction):
                    sfx = SFX(action.text)
                    panel.add(sfx)

                elif isinstance(action, NarratorAction):
                    narrator = NarratorBubble(action.text)
                    narrator.move_to((0, -40))  # Position at bottom
                    panel.add(narrator)

                elif isinstance(action, BackgroundDirective):
                    # Set background based on the description content
                    desc = action.description.strip()
                    # Check if it's a color (hex or named)
                    if desc.startswith("#") or desc.lower() in {
                        "white", "black", "red", "green", "blue", "yellow",
                        "orange", "purple", "pink", "gray", "grey", "brown",
                        "cyan", "magenta", "transparent", "none",
                    }:
                        panel.set_background(color=desc)
                    # Check if it's an image path
                    elif any(desc.lower().endswith(ext) for ext in (
                        ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"
                    )):
                        panel.set_background(image=desc)
                    else:
                        # Store description for potential AI generation
                        panel.background_description = desc

        return page


def parse_markup(markup: str) -> Page:
    """Parse markup text and return a Page object.

    This is the main entry point for the markup parser.

    Args:
        markup: The markup text to parse.

    Returns:
        A Page object with all panels and content configured.

    Example:
        >>> page = parse_markup('''
        ... [page 2x2]
        ...
        ... # panel 1
        ... Alice(left, happy): "Hello!"
        ... Bob(right): "Hi there!"
        ...
        ... # panel 2
        ... sfx: BOOM
        ... ''')
        >>> page.render("comic.svg")
    """
    parser = MarkupParser(markup)
    return parser.to_page()
