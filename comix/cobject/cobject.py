"""CObject - Base class for all comic visual elements (Manim's Mobject equivalent)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Self

import numpy as np
from numpy.typing import NDArray

if TYPE_CHECKING:
    pass


class CObject:
    """Base class for all comic visual elements.

    This is the equivalent of Manim's Mobject class. All visual elements
    in a comic (panels, bubbles, characters, text) inherit from this class.
    """

    def __init__(
        self,
        position: tuple[float, float] = (0, 0),
        scale: float = 1.0,
        rotation: float = 0.0,
        opacity: float = 1.0,
        z_index: int = 0,
        name: str | None = None,
    ) -> None:
        self.position: NDArray[np.float64] = np.array(position, dtype=np.float64)
        self.scale = scale
        self.rotation = rotation
        self.opacity = opacity
        self.z_index = z_index
        self.name = name or self.__class__.__name__

        self.submobjects: list[CObject] = []
        self.parent: CObject | None = None

        self._points: NDArray[np.float64] = np.zeros((0, 2), dtype=np.float64)
        self._needs_update = True

    # === Manim-style chaining methods ===

    def move_to(self, position: tuple[float, float]) -> Self:
        """Move to absolute position."""
        self.position = np.array(position, dtype=np.float64)
        self._needs_update = True
        return self

    def shift(self, delta: tuple[float, float]) -> Self:
        """Move by relative offset."""
        self.position = self.position + np.array(delta, dtype=np.float64)
        self._needs_update = True
        return self

    def set_scale(self, scale: float) -> Self:
        """Set the scale factor."""
        self.scale = scale
        self._needs_update = True
        return self

    def set_opacity(self, opacity: float) -> Self:
        """Set the opacity (0.0 to 1.0)."""
        self.opacity = max(0.0, min(1.0, opacity))
        self._needs_update = True
        return self

    def rotate(self, angle: float) -> Self:
        """Rotate by angle (in radians)."""
        self.rotation += angle
        self._needs_update = True
        return self

    def set_rotation(self, angle: float) -> Self:
        """Set absolute rotation (in radians)."""
        self.rotation = angle
        self._needs_update = True
        return self

    def next_to(
        self,
        other: CObject,
        direction: str = "right",
        buff: float = 10.0,
    ) -> Self:
        """Position next to another object.

        Args:
            other: The reference object.
            direction: One of "up", "down", "left", "right".
            buff: Buffer space between objects.
        """
        other_center = other.get_center()
        other_bbox = other.get_bounding_box()
        self_bbox = self.get_bounding_box()

        self_half_width = (self_bbox[1][0] - self_bbox[0][0]) / 2
        self_half_height = (self_bbox[1][1] - self_bbox[0][1]) / 2
        other_half_width = (other_bbox[1][0] - other_bbox[0][0]) / 2
        other_half_height = (other_bbox[1][1] - other_bbox[0][1]) / 2

        if direction == "right":
            new_x = other_center[0] + other_half_width + buff + self_half_width
            new_y = other_center[1]
        elif direction == "left":
            new_x = other_center[0] - other_half_width - buff - self_half_width
            new_y = other_center[1]
        elif direction == "up":
            new_x = other_center[0]
            new_y = other_center[1] + other_half_height + buff + self_half_height
        elif direction == "down":
            new_x = other_center[0]
            new_y = other_center[1] - other_half_height - buff - self_half_height
        else:
            new_x, new_y = other_center[0], other_center[1]

        return self.move_to((new_x, new_y))

    def align_to(self, other: CObject, edge: str) -> Self:
        """Align to another object's edge.

        Args:
            other: The reference object.
            edge: One of "top", "bottom", "left", "right", "center".
        """
        other_bbox = other.get_bounding_box()
        self_bbox = self.get_bounding_box()

        if edge == "left":
            offset = other_bbox[0][0] - self_bbox[0][0]
            self.position[0] += offset
        elif edge == "right":
            offset = other_bbox[1][0] - self_bbox[1][0]
            self.position[0] += offset
        elif edge == "top":
            offset = other_bbox[1][1] - self_bbox[1][1]
            self.position[1] += offset
        elif edge == "bottom":
            offset = other_bbox[0][1] - self_bbox[0][1]
            self.position[1] += offset
        elif edge == "center":
            return self.move_to(tuple(other.get_center()))

        self._needs_update = True
        return self

    # === Hierarchy ===

    def add(self, *cobjects: CObject) -> Self:
        """Add child objects."""
        for obj in cobjects:
            if obj not in self.submobjects:
                self.submobjects.append(obj)
                obj.parent = self
        return self

    def remove(self, *cobjects: CObject) -> Self:
        """Remove child objects."""
        for obj in cobjects:
            if obj in self.submobjects:
                self.submobjects.remove(obj)
                obj.parent = None
        return self

    def get_family(self) -> list[CObject]:
        """Get this object and all descendants."""
        family = [self]
        for child in self.submobjects:
            family.extend(child.get_family())
        return family

    # === Bounding box ===

    def get_bounding_box(self) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Get bounding box as (min_point, max_point)."""
        if len(self._points) == 0:
            self.generate_points()

        if len(self._points) == 0:
            return (
                np.array([self.position[0], self.position[1]], dtype=np.float64),
                np.array([self.position[0], self.position[1]], dtype=np.float64),
            )

        all_points = self._get_transformed_points()

        for child in self.submobjects:
            child_bbox = child.get_bounding_box()
            all_points = np.vstack([all_points, child_bbox[0], child_bbox[1]])

        min_point = np.min(all_points, axis=0)
        max_point = np.max(all_points, axis=0)

        return (min_point, max_point)

    def _get_transformed_points(self) -> NDArray[np.float64]:
        """Get points with transformations applied."""
        if len(self._points) == 0:
            return np.array([[self.position[0], self.position[1]]], dtype=np.float64)

        points = self._points.copy()

        if self.scale != 1.0:
            points = points * self.scale

        if self.rotation != 0.0:
            cos_r = np.cos(self.rotation)
            sin_r = np.sin(self.rotation)
            rotation_matrix = np.array([[cos_r, -sin_r], [sin_r, cos_r]])
            points = points @ rotation_matrix.T

        points = points + self.position

        return points

    def get_width(self) -> float:
        """Get the width of the bounding box."""
        bbox = self.get_bounding_box()
        return float(bbox[1][0] - bbox[0][0])

    def get_height(self) -> float:
        """Get the height of the bounding box."""
        bbox = self.get_bounding_box()
        return float(bbox[1][1] - bbox[0][1])

    def get_center(self) -> NDArray[np.float64]:
        """Get the center point."""
        bbox = self.get_bounding_box()
        return (bbox[0] + bbox[1]) / 2

    # === Rendering (override in subclasses) ===

    def generate_points(self) -> None:
        """Generate the points for this object. Override in subclasses."""
        pass

    def get_render_data(self) -> dict:
        """Get data for rendering."""
        return {
            "type": self.__class__.__name__,
            "points": self._get_transformed_points().tolist(),
            "position": self.position.tolist(),
            "scale": self.scale,
            "rotation": self.rotation,
            "opacity": self.opacity,
            "z_index": self.z_index,
            "name": self.name,
        }

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r}, position={self.position.tolist()})"
