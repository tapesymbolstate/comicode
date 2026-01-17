"""Basic geometric shape classes."""

from __future__ import annotations

from typing import Any, Self

import numpy as np

from comix.cobject.cobject import CObject


class Rectangle(CObject):
    """Rectangle shape."""

    def __init__(
        self,
        width: float = 100.0,
        height: float = 100.0,
        fill_color: str = "#FFFFFF",
        stroke_color: str = "#000000",
        stroke_width: float = 2.0,
        corner_radius: float = 0.0,
        stroke_style: str = "solid",
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)

        self.rect_width = width
        self.rect_height = height
        self.fill_color = fill_color
        self.stroke_color = stroke_color
        self.stroke_width = stroke_width
        self.corner_radius = corner_radius
        self.stroke_style = stroke_style

        self.generate_points()

    def generate_points(self) -> None:
        """Generate rectangle corner points."""
        half_w = self.rect_width / 2
        half_h = self.rect_height / 2

        self._points = np.array(
            [
                [-half_w, -half_h],
                [half_w, -half_h],
                [half_w, half_h],
                [-half_w, half_h],
                [-half_w, -half_h],
            ],
            dtype=np.float64,
        )

    def set_size(self, width: float, height: float) -> Self:
        """Set rectangle size."""
        self.rect_width = width
        self.rect_height = height
        self.generate_points()
        return self

    def get_render_data(self) -> dict[str, Any]:
        """Get data for rendering."""
        data = super().get_render_data()
        data.update(
            {
                "rect_width": self.rect_width,
                "rect_height": self.rect_height,
                "fill_color": self.fill_color,
                "stroke_color": self.stroke_color,
                "stroke_width": self.stroke_width,
                "corner_radius": self.corner_radius,
                "stroke_style": self.stroke_style,
            }
        )
        return data


class Circle(CObject):
    """Circle shape."""

    def __init__(
        self,
        radius: float = 50.0,
        fill_color: str = "#FFFFFF",
        stroke_color: str = "#000000",
        stroke_width: float = 2.0,
        num_points: int = 32,
        stroke_style: str = "solid",
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)

        self.radius = radius
        self.fill_color = fill_color
        self.stroke_color = stroke_color
        self.stroke_width = stroke_width
        self.num_points = num_points
        self.stroke_style = stroke_style

        self.generate_points()

    def generate_points(self) -> None:
        """Generate circle points."""
        angles = np.linspace(0, 2 * np.pi, self.num_points, endpoint=False)
        self._points = np.column_stack(
            [self.radius * np.cos(angles), self.radius * np.sin(angles)]
        )

    def set_radius(self, radius: float) -> Self:
        """Set circle radius."""
        self.radius = radius
        self.generate_points()
        return self

    def get_render_data(self) -> dict[str, Any]:
        """Get data for rendering."""
        data = super().get_render_data()
        data.update(
            {
                "radius": self.radius,
                "fill_color": self.fill_color,
                "stroke_color": self.stroke_color,
                "stroke_width": self.stroke_width,
                "stroke_style": self.stroke_style,
            }
        )
        return data


class Line(CObject):
    """Line segment."""

    def __init__(
        self,
        start: tuple[float, float] = (0, 0),
        end: tuple[float, float] = (100, 0),
        stroke_color: str = "#000000",
        stroke_width: float = 2.0,
        stroke_style: str = "solid",
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)

        self.start_point = np.array(start, dtype=np.float64)
        self.end_point = np.array(end, dtype=np.float64)
        self.stroke_color = stroke_color
        self.stroke_width = stroke_width
        self.stroke_style = stroke_style

        self.generate_points()

    def generate_points(self) -> None:
        """Generate line points."""
        self._points = np.array([self.start_point, self.end_point], dtype=np.float64)

    def set_points(
        self, start: tuple[float, float], end: tuple[float, float]
    ) -> Self:
        """Set line endpoints."""
        self.start_point = np.array(start, dtype=np.float64)
        self.end_point = np.array(end, dtype=np.float64)
        self.generate_points()
        return self

    def get_render_data(self) -> dict[str, Any]:
        """Get data for rendering."""
        data = super().get_render_data()
        data.update(
            {
                "start": self.start_point.tolist(),
                "end": self.end_point.tolist(),
                "stroke_color": self.stroke_color,
                "stroke_width": self.stroke_width,
                "stroke_style": self.stroke_style,
            }
        )
        return data
