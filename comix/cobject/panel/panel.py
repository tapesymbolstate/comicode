"""Panel - Comic panel (frame) container."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Self

import numpy as np

from comix.cobject.cobject import CObject


@dataclass
class Border:
    """Border style for panels."""

    color: str = "#000000"
    width: float = 2.0
    style: str = "solid"  # "solid", "dashed", "dotted", "none"
    radius: float = 0.0  # Corner radius


class Panel(CObject):
    """Comic panel (frame) - a container for visual elements.

    Panels are the basic building blocks of a comic page. Each panel
    contains characters, bubbles, and other visual elements.
    """

    def __init__(
        self,
        width: float = 300.0,
        height: float = 300.0,
        border: Border | None = None,
        background_color: str = "#FFFFFF",
        padding: float = 10.0,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.width = width
        self.height = height
        self.border = border or Border()
        self.background_color = background_color
        self.padding = padding
        self.background_image: str | None = None
        self.background_description: str | None = None  # For AI generation

        self._content: list[CObject] = []
        self.generate_points()

    def generate_points(self) -> None:
        """Generate panel rectangle points."""
        half_w = self.width / 2
        half_h = self.height / 2

        self._points = np.array(
            [
                [-half_w, -half_h],
                [half_w, -half_h],
                [half_w, half_h],
                [-half_w, half_h],
                [-half_w, -half_h],  # Close the path
            ],
            dtype=np.float64,
        )

    def add_content(self, *cobjects: CObject) -> Self:
        """Add content to the panel."""
        for obj in cobjects:
            self._content.append(obj)
            self.add(obj)
        return self

    def set_background(
        self, color: str | None = None, image: str | None = None
    ) -> Self:
        """Set the panel background."""
        if color is not None:
            self.background_color = color
        if image is not None:
            self.background_image = image
        return self

    def set_border(
        self,
        color: str | None = None,
        width: float | None = None,
        style: str | None = None,
        radius: float | None = None,
    ) -> Self:
        """Set border properties."""
        if color is not None:
            self.border.color = color
        if width is not None:
            self.border.width = width
        if style is not None:
            self.border.style = style
        if radius is not None:
            self.border.radius = radius
        return self

    def get_content_bounds(self) -> tuple[float, float, float, float]:
        """Get the bounds for content (accounting for padding).

        Returns:
            (x_min, y_min, x_max, y_max) relative to panel center.
        """
        half_w = self.width / 2 - self.padding
        half_h = self.height / 2 - self.padding
        return (-half_w, -half_h, half_w, half_h)

    def get_render_data(self) -> dict[str, Any]:
        """Get data for rendering."""
        data = super().get_render_data()
        data.update(
            {
                "width": self.width,
                "height": self.height,
                "border": {
                    "color": self.border.color,
                    "width": self.border.width,
                    "style": self.border.style,
                    "radius": self.border.radius,
                },
                "background_color": self.background_color,
                "background_image": self.background_image,
                "background_description": self.background_description,
                "padding": self.padding,
                "content": [obj.get_render_data() for obj in self._content],
            }
        )
        return data
