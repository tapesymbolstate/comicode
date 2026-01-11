"""Bubble - Speech bubble classes for comic dialogue."""

from __future__ import annotations

from typing import TYPE_CHECKING, Self

import numpy as np
from numpy.typing import NDArray

from comix.cobject.cobject import CObject
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
        **kwargs,
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
        """Calculate bubble size based on text content."""
        if self._auto_width or self._auto_height:
            char_count = len(self.text)
            estimated_text_width = char_count * self.font_size * 0.6
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

    def attach_to(self, character: CObject, anchor: str = "top") -> Self:
        """Attach the bubble above a character.

        Args:
            character: The character to attach to.
            anchor: Position relative to character ("top", "top-left", "top-right").
        """
        char_bbox = character.get_bounding_box()
        char_center = character.get_center()

        bubble_offset = self._height / 2 + 20

        if anchor == "top":
            new_x = char_center[0]
            new_y = char_bbox[1][1] + bubble_offset
            self.tail_direction = "bottom"
        elif anchor == "top-left":
            new_x = char_center[0] - 30
            new_y = char_bbox[1][1] + bubble_offset
            self.tail_direction = "bottom-right"
        elif anchor == "top-right":
            new_x = char_center[0] + 30
            new_y = char_bbox[1][1] + bubble_offset
            self.tail_direction = "bottom-left"
        else:
            new_x = char_center[0]
            new_y = char_bbox[1][1] + bubble_offset
            self.tail_direction = "bottom"

        self.move_to((new_x, new_y))
        self.point_to(character)
        self.generate_points()
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

    def get_render_data(self) -> dict:
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

    def __init__(self, text: str = "", **kwargs) -> None:
        kwargs.setdefault("bubble_type", Bubble.SPEECH)
        super().__init__(text=text, **kwargs)


class ThoughtBubble(Bubble):
    """Cloud-shaped thought bubble."""

    def __init__(self, text: str = "", **kwargs) -> None:
        kwargs.setdefault("bubble_type", Bubble.THOUGHT)
        kwargs.setdefault("corner_radius", 999)
        kwargs.setdefault("border_style", "solid")
        super().__init__(text=text, **kwargs)


class ShoutBubble(Bubble):
    """Spiky emphasis bubble for shouting."""

    def __init__(self, text: str = "", **kwargs) -> None:
        kwargs.setdefault("bubble_type", Bubble.SHOUT)
        kwargs.setdefault("border_width", 3.0)
        kwargs.setdefault("font_size", 20.0)
        super().__init__(text=text, **kwargs)


class WhisperBubble(Bubble):
    """Dashed bubble for whispering."""

    def __init__(self, text: str = "", **kwargs) -> None:
        kwargs.setdefault("bubble_type", Bubble.WHISPER)
        kwargs.setdefault("border_style", "dashed")
        kwargs.setdefault("font_size", 14.0)
        super().__init__(text=text, **kwargs)


class NarratorBubble(Bubble):
    """Rectangular box for narration."""

    def __init__(self, text: str = "", **kwargs) -> None:
        kwargs.setdefault("bubble_type", Bubble.NARRATOR)
        kwargs.setdefault("corner_radius", 0.0)
        kwargs.setdefault("tail_length", 0.0)
        super().__init__(text=text, **kwargs)
