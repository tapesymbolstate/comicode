"""Bubble - Speech bubble classes for comic dialogue."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self

import numpy as np

from comix.cobject.cobject import CObject
from comix.style.font import calculate_text_width_with_cjk
from comix.utils.bezier import create_bubble_path, create_tail_points

if TYPE_CHECKING:
    from comix.style.style import Style


class Bubble(CObject):
    """Base class for speech bubbles.

    Bubbles contain dialogue text and have a tail pointing to the speaker.
    """

    SPEECH = "speech"
    THOUGHT = "thought"
    SHOUT = "shout"
    WHISPER = "whisper"
    NARRATOR = "narrator"

    def __init__(
        self,
        text: str = "",
        bubble_type: str = "speech",
        width: float | None = None,
        height: float | None = None,
        padding: tuple[float, float, float, float] = (15.0, 20.0, 15.0, 20.0),
        corner_radius: float = 20.0,
        corner_radii: tuple[float, float, float, float] | None = None,
        tail_direction: str = "bottom-left",
        tail_length: float = 30.0,
        tail_width: float = 20.0,
        tail_target: CObject | tuple[float, float] | None = None,
        border_color: str = "#000000",
        border_width: float = 2.0,
        border_style: str = "solid",
        fill_color: str = "#FFFFFF",
        font_family: str = "sans-serif",
        font_size: float = 16.0,
        font_color: str = "#000000",
        text_align: str = "center",
        line_height: float = 1.4,
        wobble: float = 0.0,
        wobble_mode: str = "random",
        emphasis: bool = False,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)

        self.text = text
        self.bubble_type = bubble_type

        self._auto_width = width is None
        self._auto_height = height is None
        self._width = width or 100.0
        self._height = height or 60.0
        self.padding = padding
        self.corner_radius = corner_radius
        self.corner_radii = corner_radii

        self.tail_direction = tail_direction
        self.tail_length = tail_length
        self.tail_width = tail_width
        self.tail_target = tail_target

        self.border_color = border_color
        self.border_width = border_width
        self.border_style = border_style
        self.fill_color = fill_color

        self.font_family = font_family
        self.font_size = font_size
        self.font_color = font_color
        self.text_align = text_align
        self.line_height = line_height

        self.wobble = wobble
        self.wobble_mode = wobble_mode
        self.emphasis = emphasis

        self._calculate_size()
        self.generate_points()

    @property
    def bubble_width(self) -> float:
        return self._width

    @property
    def bubble_height(self) -> float:
        return self._height

    def _calculate_size(self) -> None:
        """Calculate bubble size based on text content.

        Uses CJK-aware width calculation for proper handling of
        Korean, Japanese, and Chinese characters which are full-width.
        """
        if self._auto_width or self._auto_height:
            # Use CJK-aware width calculation (full-width chars = 1em, half-width = 0.6em)
            estimated_text_width = calculate_text_width_with_cjk(
                self.text, self.font_size, halfwidth_ratio=0.6, fullwidth_ratio=1.0
            )
            estimated_text_height = self.font_size * self.line_height

            lines = max(1, int(np.ceil(estimated_text_width / 200)))
            if lines > 1:
                estimated_text_width = 200
                estimated_text_height = lines * self.font_size * self.line_height

            if self._auto_width:
                self._width = estimated_text_width + self.padding[1] + self.padding[3]
                self._width = max(self._width, 60.0)

            if self._auto_height:
                self._height = estimated_text_height + self.padding[0] + self.padding[2]
                self._height = max(self._height, 40.0)

    def generate_points(self) -> None:
        """Generate bubble outline points."""
        self._points = create_bubble_path(
            width=self._width,
            height=self._height,
            style=self.bubble_type,
            corner_radius=self.corner_radius,
            corner_radii=self.corner_radii,
            wobble=self.wobble,
            wobble_mode=self.wobble_mode,
        )

        tail_points = create_tail_points(
            width=self._width,
            height=self._height,
            direction=self.tail_direction,
            length=self.tail_length,
            tip_width=self.tail_width,
        )

        if len(tail_points) > 0:
            self._tail_points = tail_points
        else:
            self._tail_points = np.zeros((0, 2), dtype=np.float64)

    def set_text(self, text: str) -> Self:
        """Update the bubble text."""
        self.text = text
        self._calculate_size()
        self.generate_points()
        return self

    def point_to(self, target: CObject | tuple[float, float]) -> Self:
        """Set the tail to point at a target."""
        self.tail_target = target
        return self

    def attach_to(
        self,
        character: CObject,
        anchor: str = "top",
        buffer: float = 20.0,
    ) -> Self:
        """Attach the bubble relative to a character.

        Args:
            character: The character to attach to.
            anchor: Position relative to character. Options are:
                - "top", "top-left", "top-right": Above the character
                - "left", "right": To the side of the character
                - "bottom", "bottom-left", "bottom-right": Below the character
            buffer: Space between character and bubble.

        Returns:
            Self for method chaining.
        """
        char_bbox = character.get_bounding_box()
        char_center = character.get_center()
        char_min = char_bbox[0]  # (x_min, y_min)
        char_max = char_bbox[1]  # (x_max, y_max)

        # Mapping of anchor positions to (x, y, tail_direction)
        anchor_positions = {
            "top": (
                char_center[0],
                char_max[1] + self._height / 2 + buffer,
                "bottom",
            ),
            "top-left": (
                char_center[0] - 30,
                char_max[1] + self._height / 2 + buffer,
                "bottom-right",
            ),
            "top-right": (
                char_center[0] + 30,
                char_max[1] + self._height / 2 + buffer,
                "bottom-left",
            ),
            "left": (
                char_min[0] - self._width / 2 - buffer,
                char_center[1],
                "right",
            ),
            "right": (
                char_max[0] + self._width / 2 + buffer,
                char_center[1],
                "left",
            ),
            "bottom": (
                char_center[0],
                char_min[1] - self._height / 2 - buffer,
                "top",
            ),
            "bottom-left": (
                char_center[0] - 30,
                char_min[1] - self._height / 2 - buffer,
                "top-right",
            ),
            "bottom-right": (
                char_center[0] + 30,
                char_min[1] - self._height / 2 - buffer,
                "top-left",
            ),
        }

        if anchor in anchor_positions:
            new_x, new_y, tail_dir = anchor_positions[anchor]
        else:
            # Default to top
            new_x, new_y, tail_dir = anchor_positions["top"]

        self.tail_direction = tail_dir
        self.move_to((new_x, new_y))
        self.point_to(character)
        self.generate_points()
        return self

    def overlaps_with(self, other: Bubble, margin: float = 5.0) -> bool:
        """Check if this bubble overlaps with another bubble.

        Args:
            other: Another Bubble to check collision with.
            margin: Extra margin to consider around bubbles.

        Returns:
            True if bubbles overlap, False otherwise.
        """
        self_bbox = self.get_bounding_box()
        other_bbox = other.get_bounding_box()

        self_min = self_bbox[0]
        self_max = self_bbox[1]
        other_min = other_bbox[0]
        other_max = other_bbox[1]

        # Check for overlap with margin
        return not (
            self_max[0] + margin < other_min[0]
            or self_min[0] - margin > other_max[0]
            or self_max[1] + margin < other_min[1]
            or self_min[1] - margin > other_max[1]
        )

    def auto_attach_to(
        self,
        character: CObject,
        avoid_bubbles: list[Bubble] | None = None,
        bounds: tuple[float, float, float, float] | None = None,
        preferred_anchors: list[str] | None = None,
        buffer: float = 20.0,
    ) -> Self:
        """Automatically attach bubble to character, avoiding collisions.

        Tries different anchor positions and selects the first one that
        doesn't overlap with other bubbles and stays within bounds.

        Args:
            character: The character to attach to.
            avoid_bubbles: List of other bubbles to avoid overlapping with.
            bounds: Optional (x_min, y_min, x_max, y_max) boundary constraints.
            preferred_anchors: Preferred anchor order. Defaults to
                ["top", "top-left", "top-right", "left", "right"].
            buffer: Space between character and bubble.

        Returns:
            Self for method chaining.
        """
        if preferred_anchors is None:
            # Default priority: top positions first (standard comic convention)
            preferred_anchors = [
                "top",
                "top-left",
                "top-right",
                "left",
                "right",
            ]

        if avoid_bubbles is None:
            avoid_bubbles = []

        for anchor in preferred_anchors:
            # Try this anchor position
            self.attach_to(character, anchor=anchor, buffer=buffer)

            # Check if position is valid
            is_valid = True

            # Check bounds
            if bounds is not None:
                x_min, y_min, x_max, y_max = bounds
                bbox = self.get_bounding_box()
                if (
                    bbox[0][0] < x_min
                    or bbox[1][0] > x_max
                    or bbox[0][1] < y_min
                    or bbox[1][1] > y_max
                ):
                    is_valid = False

            # Check overlaps with other bubbles
            if is_valid:
                for other in avoid_bubbles:
                    if other is not self and self.overlaps_with(other):
                        is_valid = False
                        break

            if is_valid:
                return self

        # If no valid position found, use the first anchor and restore
        self.attach_to(character, anchor=preferred_anchors[0], buffer=buffer)
        return self

    def apply_style(self, style: Style) -> Self:
        """Apply style properties to this bubble.

        Copies relevant properties from the Style object to this bubble's
        attributes for border, fill, and font properties.

        Args:
            style: The Style object to apply.

        Returns:
            Self for method chaining.
        """
        super().apply_style(style)

        # Apply border properties
        self.border_color = style.border_color
        self.border_width = style.border_width
        self.border_style = style.border_style

        # Apply fill properties
        self.fill_color = style.fill_color

        # Apply font properties
        self.font_family = style.font_family
        self.font_size = style.font_size
        self.font_color = style.font_color
        self.text_align = style.text_align
        self.line_height = style.line_height

        # Recalculate size and regenerate points since font size may have changed
        self._calculate_size()
        self.generate_points()

        return self

    def get_render_data(self) -> dict[str, Any]:
        """Get data for rendering."""
        data = super().get_render_data()

        tail_target_pos = None
        if self.tail_target is not None:
            if isinstance(self.tail_target, CObject):
                tail_target_pos = self.tail_target.get_center().tolist()
            else:
                tail_target_pos = list(self.tail_target)

        data.update(
            {
                "bubble_type": self.bubble_type,
                "text": self.text,
                "width": self._width,
                "height": self._height,
                "padding": self.padding,
                "corner_radius": self.corner_radius,
                "corner_radii": self.corner_radii,
                "tail_direction": self.tail_direction,
                "tail_length": self.tail_length,
                "tail_width": self.tail_width,
                "tail_target": tail_target_pos,
                "tail_points": self._tail_points.tolist() if hasattr(self, "_tail_points") else [],
                "border_color": self.border_color,
                "border_width": self.border_width,
                "border_style": self.border_style,
                "fill_color": self.fill_color,
                "font_family": self.font_family,
                "font_size": self.font_size,
                "font_color": self.font_color,
                "text_align": self.text_align,
                "line_height": self.line_height,
                "wobble": self.wobble,
                "wobble_mode": self.wobble_mode,
                "emphasis": self.emphasis,
            }
        )
        return data


class SpeechBubble(Bubble):
    """Standard speech bubble for dialogue."""

    def __init__(self, text: str = "", **kwargs: Any) -> None:
        kwargs.setdefault("bubble_type", Bubble.SPEECH)
        super().__init__(text=text, **kwargs)


class ThoughtBubble(Bubble):
    """Cloud-shaped thought bubble."""

    def __init__(self, text: str = "", **kwargs: Any) -> None:
        kwargs.setdefault("bubble_type", Bubble.THOUGHT)
        kwargs.setdefault("corner_radius", 999)
        kwargs.setdefault("border_style", "solid")
        super().__init__(text=text, **kwargs)


class ShoutBubble(Bubble):
    """Spiky emphasis bubble for shouting."""

    def __init__(self, text: str = "", **kwargs: Any) -> None:
        kwargs.setdefault("bubble_type", Bubble.SHOUT)
        kwargs.setdefault("border_width", 3.0)
        kwargs.setdefault("font_size", 20.0)
        super().__init__(text=text, **kwargs)


class WhisperBubble(Bubble):
    """Dashed bubble for whispering."""

    def __init__(self, text: str = "", **kwargs: Any) -> None:
        kwargs.setdefault("bubble_type", Bubble.WHISPER)
        kwargs.setdefault("border_style", "dashed")
        kwargs.setdefault("font_size", 14.0)
        super().__init__(text=text, **kwargs)


class NarratorBubble(Bubble):
    """Rectangular box for narration."""

    def __init__(self, text: str = "", **kwargs: Any) -> None:
        kwargs.setdefault("bubble_type", Bubble.NARRATOR)
        kwargs.setdefault("corner_radius", 0.0)
        kwargs.setdefault("tail_length", 0.0)
        super().__init__(text=text, **kwargs)


def auto_position_bubbles(
    character_bubble_pairs: list[tuple[CObject, Bubble]],
    bounds: tuple[float, float, float, float] | None = None,
    buffer: float = 20.0,
) -> list[Bubble]:
    """Automatically position multiple bubbles avoiding collisions.

    Positions bubbles one by one, with each subsequent bubble avoiding
    overlap with previously positioned bubbles.

    Args:
        character_bubble_pairs: List of (character, bubble) pairs to position.
        bounds: Optional (x_min, y_min, x_max, y_max) boundary constraints.
        buffer: Space between character and bubble.

    Returns:
        List of positioned bubbles.

    Example:
        bubbles = auto_position_bubbles([
            (alice, bubble1),
            (bob, bubble2),
            (charlie, bubble3),
        ], bounds=(0, 0, 800, 600))
    """
    positioned: list[Bubble] = []

    for character, bubble in character_bubble_pairs:
        bubble.auto_attach_to(
            character,
            avoid_bubbles=positioned,
            bounds=bounds,
            buffer=buffer,
        )
        positioned.append(bubble)

    return positioned
