"""Text - Text rendering classes for comics."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self

import numpy as np

from comix.cobject.cobject import CObject
from comix.style.font import calculate_text_width_with_cjk

if TYPE_CHECKING:
    from comix.style.style import Style


class Text(CObject):
    """Basic text element."""

    def __init__(
        self,
        text: str = "",
        font_family: str = "sans-serif",
        font_size: float = 16.0,
        font_weight: str = "normal",
        font_style: str = "normal",
        color: str = "#000000",
        align: str = "left",
        line_height: float = 1.4,
        max_width: float | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)

        self.text = text
        self.font_family = font_family
        self.font_size = font_size
        self.font_weight = font_weight
        self.font_style = font_style
        self.color = color
        self.align = align
        self.line_height = line_height
        self.max_width = max_width

        self._calculate_bounds()

    def _calculate_bounds(self) -> None:
        """Calculate text bounding box based on content.

        Uses CJK-aware width calculation for proper handling of
        Korean, Japanese, and Chinese characters which are full-width.
        """
        # Use CJK-aware width calculation (full-width chars = 1em, half-width = 0.6em)
        total_width = calculate_text_width_with_cjk(
            self.text, self.font_size, halfwidth_ratio=0.6, fullwidth_ratio=1.0
        )

        if self.max_width and total_width > self.max_width:
            num_lines = int(np.ceil(total_width / self.max_width))
            width = self.max_width
        else:
            num_lines = 1
            width = total_width

        height = num_lines * self.font_size * self.line_height

        half_w = width / 2
        half_h = height / 2

        self._points = np.array(
            [
                [-half_w, -half_h],
                [half_w, -half_h],
                [half_w, half_h],
                [-half_w, half_h],
            ],
            dtype=np.float64,
        )

        self._text_width = width
        self._text_height = height

    def set_text(self, text: str) -> Self:
        """Update the text content."""
        self.text = text
        self._calculate_bounds()
        return self

    def set_font(
        self,
        family: str | None = None,
        size: float | None = None,
        weight: str | None = None,
        style: str | None = None,
    ) -> Self:
        """Update font properties."""
        if family is not None:
            self.font_family = family
        if size is not None:
            self.font_size = size
        if weight is not None:
            self.font_weight = weight
        if style is not None:
            self.font_style = style
        self._calculate_bounds()
        return self

    def set_color(self, color: str) -> Self:
        """Set the text color."""
        self.color = color
        return self

    def apply_style(self, style: Style) -> Self:
        """Apply style properties to this text element.

        Copies relevant font and text properties from the Style object.

        Args:
            style: The Style object to apply.

        Returns:
            Self for method chaining.
        """
        super().apply_style(style)

        # Apply font properties
        self.font_family = style.font_family
        self.font_size = style.font_size
        self.font_weight = style.font_weight
        self.font_style = style.font_style
        self.color = style.font_color
        self.align = style.text_align
        self.line_height = style.line_height

        # Recalculate bounds since font properties changed
        self._calculate_bounds()

        return self

    def get_render_data(self) -> dict[str, Any]:
        """Get data for rendering."""
        data = super().get_render_data()
        data.update(
            {
                "text": self.text,
                "font_family": self.font_family,
                "font_size": self.font_size,
                "font_weight": self.font_weight,
                "font_style": self.font_style,
                "color": self.color,
                "align": self.align,
                "line_height": self.line_height,
                "max_width": self.max_width,
                "text_width": getattr(self, "_text_width", 0),
                "text_height": getattr(self, "_text_height", 0),
            }
        )
        return data


class StyledText(Text):
    """Text with additional styling options."""

    def __init__(
        self,
        text: str = "",
        background_color: str | None = None,
        padding: tuple[float, float, float, float] = (0, 0, 0, 0),
        border_color: str | None = None,
        border_width: float = 0,
        **kwargs: Any,
    ) -> None:
        super().__init__(text=text, **kwargs)

        self.background_color = background_color
        self.text_padding = padding
        self.border_color = border_color
        self.border_width = border_width

    def get_render_data(self) -> dict[str, Any]:
        """Get data for rendering."""
        data = super().get_render_data()
        data.update(
            {
                "background_color": self.background_color,
                "text_padding": self.text_padding,
                "border_color": self.border_color,
                "text_border_width": self.border_width,
            }
        )
        return data


class SFX(Text):
    """Sound effect text (onomatopoeia)."""

    def __init__(
        self,
        text: str = "",
        outline: bool = True,
        outline_color: str = "#FFFFFF",
        outline_width: float = 3.0,
        shadow: bool = False,
        shadow_color: str = "#00000033",
        shadow_offset: tuple[float, float] = (2.0, 2.0),
        **kwargs: Any,
    ) -> None:
        kwargs.setdefault("font_size", 32.0)
        kwargs.setdefault("font_weight", "bold")
        super().__init__(text=text, **kwargs)

        self.outline = outline
        self.outline_color = outline_color
        self.outline_width = outline_width
        self.shadow = shadow
        self.shadow_color = shadow_color
        self.shadow_offset = shadow_offset

    def get_render_data(self) -> dict[str, Any]:
        """Get data for rendering."""
        data = super().get_render_data()
        data.update(
            {
                "sfx": True,
                "outline": self.outline,
                "outline_color": self.outline_color,
                "outline_width": self.outline_width,
                "shadow": self.shadow,
                "shadow_color": self.shadow_color,
                "shadow_offset": list(self.shadow_offset),
            }
        )
        return data
