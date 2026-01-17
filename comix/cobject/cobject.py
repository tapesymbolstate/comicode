"""CObject - Base class for all comic visual elements (Manim's Mobject equivalent)."""

from __future__ import annotations

import copy
from typing import TYPE_CHECKING, Any, Self

import numpy as np
from numpy.typing import NDArray

if TYPE_CHECKING:
    from comix.style.style import Style


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
        style: Style | None = None,
    ) -> None:
        self.position: NDArray[np.float64] = np.array(position, dtype=np.float64)
        self.scale = scale
        self.rotation = rotation
        self.opacity = opacity
        self.z_index = z_index
        self.name = name or self.__class__.__name__
        self._style: Style | None = style

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

    def center_in(
        self,
        bounds: tuple[float, float, float, float],
        axis: str = "both",
    ) -> Self:
        """Center this object within given bounds.

        Args:
            bounds: Bounding rectangle as (x, y, width, height) where (x, y) is top-left.
            axis: Which axis to center on - "x", "y", or "both".

        Returns:
            Self for method chaining.
        """
        x, y, width, height = bounds
        center_x = x + width / 2
        center_y = y + height / 2

        if axis == "x":
            self.position[0] = center_x
        elif axis == "y":
            self.position[1] = center_y
        else:  # "both"
            self.position = np.array([center_x, center_y], dtype=np.float64)

        self._needs_update = True
        return self

    def to_corner(
        self,
        corner: str,
        bounds: tuple[float, float, float, float],
        buff: float = 10.0,
    ) -> Self:
        """Move this object to a corner within given bounds.

        Args:
            corner: Corner position - "top-left", "top-right", "bottom-left", "bottom-right".
            bounds: Bounding rectangle as (x, y, width, height) where (x, y) is top-left.
            buff: Buffer/margin from the corner.

        Returns:
            Self for method chaining.
        """
        x, y, width, height = bounds
        self_bbox = self.get_bounding_box()
        self_half_w = (self_bbox[1][0] - self_bbox[0][0]) / 2
        self_half_h = (self_bbox[1][1] - self_bbox[0][1]) / 2

        if corner == "top-left":
            new_x = x + buff + self_half_w
            new_y = y + buff + self_half_h
        elif corner == "top-right":
            new_x = x + width - buff - self_half_w
            new_y = y + buff + self_half_h
        elif corner == "bottom-left":
            new_x = x + buff + self_half_w
            new_y = y + height - buff - self_half_h
        elif corner == "bottom-right":
            new_x = x + width - buff - self_half_w
            new_y = y + height - buff - self_half_h
        else:
            raise ValueError(
                f"Invalid corner: {corner}. "
                "Use 'top-left', 'top-right', 'bottom-left', or 'bottom-right'."
            )

        return self.move_to((new_x, new_y))

    def to_edge(
        self,
        edge: str,
        bounds: tuple[float, float, float, float],
        buff: float = 10.0,
    ) -> Self:
        """Move this object to an edge within given bounds (centered on the edge).

        Args:
            edge: Edge position - "top", "bottom", "left", "right".
            bounds: Bounding rectangle as (x, y, width, height) where (x, y) is top-left.
            buff: Buffer/margin from the edge.

        Returns:
            Self for method chaining.
        """
        x, y, width, height = bounds
        center_x = x + width / 2
        center_y = y + height / 2
        self_bbox = self.get_bounding_box()
        self_half_w = (self_bbox[1][0] - self_bbox[0][0]) / 2
        self_half_h = (self_bbox[1][1] - self_bbox[0][1]) / 2

        if edge == "top":
            new_x = center_x
            new_y = y + buff + self_half_h
        elif edge == "bottom":
            new_x = center_x
            new_y = y + height - buff - self_half_h
        elif edge == "left":
            new_x = x + buff + self_half_w
            new_y = center_y
        elif edge == "right":
            new_x = x + width - buff - self_half_w
            new_y = center_y
        else:
            raise ValueError(
                f"Invalid edge: {edge}. Use 'top', 'bottom', 'left', or 'right'."
            )

        return self.move_to((new_x, new_y))

    def hide(self) -> Self:
        """Hide this object by setting opacity to 0.

        Returns:
            Self for method chaining.
        """
        return self.set_opacity(0.0)

    def show(self) -> Self:
        """Show this object by setting opacity to 1.

        Returns:
            Self for method chaining.
        """
        return self.set_opacity(1.0)

    def is_visible(self) -> bool:
        """Check if this object is visible (opacity > 0).

        Returns:
            True if opacity is greater than 0.
        """
        return self.opacity > 0.0

    def copy(self) -> Self:
        """Create a deep copy of this object.

        Creates a new instance with the same properties and copies all submobjects.
        The copy will not have a parent.

        Returns:
            A new CObject with copied properties.
        """
        # Deep copy to handle nested objects and numpy arrays
        new_obj = copy.deepcopy(self)
        # Clear parent reference since copy is independent
        new_obj.parent = None
        return new_obj

    def scale_to_fit_width(self, target_width: float) -> Self:
        """Scale this object to fit a target width.

        Args:
            target_width: The desired width.

        Returns:
            Self for method chaining.
        """
        current_width = self.get_width()
        if current_width > 0:
            scale_factor = target_width / current_width
            self.scale *= scale_factor
            self._needs_update = True
        return self

    def scale_to_fit_height(self, target_height: float) -> Self:
        """Scale this object to fit a target height.

        Args:
            target_height: The desired height.

        Returns:
            Self for method chaining.
        """
        current_height = self.get_height()
        if current_height > 0:
            scale_factor = target_height / current_height
            self.scale *= scale_factor
            self._needs_update = True
        return self

    def scale_to_fit(
        self,
        target_width: float,
        target_height: float,
        preserve_aspect_ratio: bool = True,
    ) -> Self:
        """Scale this object to fit within target dimensions.

        Args:
            target_width: Maximum width.
            target_height: Maximum height.
            preserve_aspect_ratio: If True, scale uniformly to fit within bounds.
                If False, scale independently to match exact dimensions.

        Returns:
            Self for method chaining.
        """
        current_width = self.get_width()
        current_height = self.get_height()

        if current_width <= 0 or current_height <= 0:
            return self

        if preserve_aspect_ratio:
            scale_x = target_width / current_width
            scale_y = target_height / current_height
            scale_factor = min(scale_x, scale_y)
            self.scale *= scale_factor
        else:
            # For non-uniform scaling, we adjust position-based scale
            # This is approximate since CObject uses uniform scale
            scale_x = target_width / current_width
            scale_y = target_height / current_height
            # Use average for uniform scale approximation
            self.scale *= (scale_x + scale_y) / 2

        self._needs_update = True
        return self

    # === Style ===

    def set_style(self, style: Style) -> Self:
        """Set the style for this object.

        Args:
            style: The Style object to apply.

        Returns:
            Self for method chaining.
        """
        self._style = style
        self._needs_update = True
        return self

    def get_style(self) -> Style | None:
        """Get the directly applied style (not inherited)."""
        return self._style

    def get_effective_style(self) -> Style:
        """Get the effective style, considering inheritance from parent.

        The style cascade is: self._style > parent._style > default

        Returns:
            The effective Style object for this element.
        """
        from comix.style.style import Style

        # Start with default style
        effective = Style()

        # Apply parent's style if available
        if self.parent is not None:
            parent_style = self.parent.get_effective_style()
            effective = effective.merge_with(parent_style)

        # Apply own style if set
        if self._style is not None:
            effective = effective.merge_with(self._style)

        return effective

    def apply_style(self, style: Style) -> Self:
        """Apply style properties to this object.

        This is a convenience method that copies properties from the Style
        to object-specific attributes. Subclasses should override this to
        apply style properties to their specific attributes.

        Args:
            style: The Style object to apply.

        Returns:
            Self for method chaining.
        """
        self._style = style
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

    def get_render_data(self) -> dict[str, Any]:
        """Get data for rendering."""
        data = {
            "type": self.__class__.__name__,
            "points": self._get_transformed_points().tolist(),
            "position": self.position.tolist(),
            "scale": self.scale,
            "rotation": self.rotation,
            "opacity": self.opacity,
            "z_index": self.z_index,
            "name": self.name,
        }

        # Include effective style if any style is set
        if self._style is not None:
            style = self.get_effective_style()
            data["style"] = style.to_dict()

        return data

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r}, position={self.position.tolist()})"
