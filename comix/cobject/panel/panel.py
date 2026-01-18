"""Panel - Comic panel (frame) container."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Self

import numpy as np

from comix.cobject.cobject import CObject
from comix.constants import ValidValues, validate_value

if TYPE_CHECKING:
    from comix.cobject.bubble.bubble import Bubble
    from comix.cobject.character.character import Character

logger = logging.getLogger(__name__)


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

    def add_content(
        self,
        *cobjects: CObject,
        auto_position_bubbles: bool = True,
    ) -> Self:
        """Add content to the panel with optional automatic bubble positioning.

        When auto_position_bubbles is True (default), bubbles are automatically
        repositioned to avoid overlapping with each other while staying attached
        to their target characters.

        Args:
            *cobjects: Visual elements to add (characters, bubbles, text, etc.)
            auto_position_bubbles: If True, automatically reposition bubbles
                to avoid collisions. Default is True.

        Returns:
            Self for method chaining.
        """
        # Import here to avoid circular imports
        from comix.cobject.bubble.bubble import Bubble
        from comix.cobject.character.character import Character

        # Separate objects into categories for processing
        characters: list[Character] = []
        bubbles: list[Bubble] = []
        other_objects: list[CObject] = []

        for obj in cobjects:
            if isinstance(obj, Character):
                characters.append(obj)
            elif isinstance(obj, Bubble):
                bubbles.append(obj)
            else:
                other_objects.append(obj)

        # Add all objects to content list and parent
        for obj in cobjects:
            self._content.append(obj)
            self.add(obj)

        # Automatically reposition bubbles to avoid collisions if enabled
        if auto_position_bubbles and bubbles:
            # Get existing bubbles in this panel (added before this call)
            existing_bubbles: list[Bubble] = [
                obj for obj in self._content
                if isinstance(obj, Bubble) and obj not in bubbles
            ]

            # Calculate panel bounds for bubble positioning
            panel_pos = self.get_center()
            half_w = self.width / 2 - self.padding
            half_h = self.height / 2 - self.padding
            bounds = (
                panel_pos[0] - half_w,
                panel_pos[1] - half_h,
                panel_pos[0] + half_w,
                panel_pos[1] + half_h,
            )

            # Reposition each new bubble to avoid collisions
            all_positioned: list[Bubble] = list(existing_bubbles)
            for bubble in bubbles:
                # Find the character this bubble is attached to (if any)
                target_char: Character | None = None
                if bubble.tail_target is not None:
                    if isinstance(bubble.tail_target, Character):
                        target_char = bubble.tail_target
                    elif isinstance(bubble.tail_target, CObject):
                        # Check if it's a character by looking in our characters list
                        for char in characters:
                            if char is bubble.tail_target:
                                target_char = char
                                break

                if target_char is not None:
                    # Use auto_attach_to to find a non-colliding position
                    bubble.auto_attach_to(
                        target_char,
                        avoid_bubbles=all_positioned,
                        bounds=bounds,
                    )

                all_positioned.append(bubble)

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
        """Set border properties.

        Args:
            color: Border color (hex string, e.g., "#000000").
            width: Border width in pixels.
            style: Border style ("solid", "dashed", "dotted", "none").
            radius: Corner radius for rounded borders.

        Returns:
            Self for method chaining.

        Raises:
            ValueError: If style is not a valid border style.
        """
        if color is not None:
            self.border.color = color
        if width is not None:
            self.border.width = width
        if style is not None:
            validate_value(style, ValidValues.BORDER_STYLES, "style", "Panel.set_border")
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
                "shape": "rectangle",
                "clip_path": self._points.tolist() if hasattr(self, "_points") else [],
            }
        )
        return data

    def split_diagonal(
        self,
        angle: float = 45.0,
        direction: str = "top-left-to-bottom-right",
    ) -> tuple["IrregularPanel", "IrregularPanel"]:
        """Split this panel along a diagonal line, creating two triangular panels.

        Divides the panel along a diagonal line at the specified angle.
        This is useful for creating dynamic manga-style layouts where panels
        are split diagonally for dramatic effect.

        Args:
            angle: Angle of the diagonal cut in degrees (default 45).
                   Values are clamped to 5-85 degrees for practical results.
            direction: Direction of the diagonal split. Valid values:
                - "top-left-to-bottom-right" (default): Diagonal from top-left
                  to bottom-right corner, creating upper-right and lower-left panels.
                - "top-right-to-bottom-left": Diagonal from top-right to
                  bottom-left corner, creating upper-left and lower-right panels.

        Returns:
            A tuple of two IrregularPanel objects representing the split portions:
            - For "top-left-to-bottom-right": (upper_right_panel, lower_left_panel)
            - For "top-right-to-bottom-left": (upper_left_panel, lower_right_panel)

        Raises:
            ValueError: If direction is not a valid split direction.

        Example:
            >>> panel = Panel(width=400, height=400)
            >>> top_half, bottom_half = panel.split_diagonal(
            ...     angle=45,
            ...     direction="top-left-to-bottom-right"
            ... )
            >>> # Both panels inherit the original panel's position
            >>> page.add(top_half, bottom_half)

        Note:
            - Both resulting panels are positioned at the original panel's center.
            - Content from the original panel is NOT automatically transferred.
            - Border and background settings are copied to both new panels.
            - The original panel is not modified.
        """
        valid_directions = ("top-left-to-bottom-right", "top-right-to-bottom-left")
        if direction not in valid_directions:
            raise ValueError(
                f"Invalid direction '{direction}' for split_diagonal. "
                f"Valid directions: {', '.join(valid_directions)}"
            )

        # Clamp angle to reasonable range (reserved for future angle-based splitting)
        angle = max(5.0, min(85.0, angle))
        _ = angle  # Angle reserved for future non-corner splitting implementations

        half_w = self.width / 2
        half_h = self.height / 2

        # Corner-to-corner splitting is the most common manga technique
        if direction == "top-left-to-bottom-right":
            # Split from top-left corner to bottom-right corner
            # Panel 1: Upper-right triangle (top-left, top-right, bottom-right)
            panel1_points = [
                (-half_w, half_h),   # Top-left
                (half_w, half_h),    # Top-right
                (half_w, -half_h),   # Bottom-right
            ]
            # Panel 2: Lower-left triangle (top-left, bottom-right, bottom-left)
            panel2_points = [
                (-half_w, half_h),   # Top-left
                (half_w, -half_h),   # Bottom-right
                (-half_w, -half_h),  # Bottom-left
            ]
        else:  # top-right-to-bottom-left
            # Split from top-right corner to bottom-left corner
            # Panel 1: Upper-left triangle (top-left, top-right, bottom-left)
            panel1_points = [
                (-half_w, half_h),   # Top-left
                (half_w, half_h),    # Top-right
                (-half_w, -half_h),  # Bottom-left
            ]
            # Panel 2: Lower-right triangle (top-right, bottom-right, bottom-left)
            panel2_points = [
                (half_w, half_h),    # Top-right
                (half_w, -half_h),   # Bottom-right
                (-half_w, -half_h),  # Bottom-left
            ]

        # Create the two irregular panels
        panel1 = IrregularPanel(
            points=panel1_points,
            border=Border(
                color=self.border.color,
                width=self.border.width,
                style=self.border.style,
                radius=self.border.radius,
            ),
            background_color=self.background_color,
            padding=self.padding,
        )

        panel2 = IrregularPanel(
            points=panel2_points,
            border=Border(
                color=self.border.color,
                width=self.border.width,
                style=self.border.style,
                radius=self.border.radius,
            ),
            background_color=self.background_color,
            padding=self.padding,
        )

        # Position both panels at the original panel's center
        original_center = self.get_center()
        center_tuple = (float(original_center[0]), float(original_center[1]))
        panel1.move_to(center_tuple)
        panel2.move_to(center_tuple)

        return (panel1, panel2)

    def split_curve(
        self,
        control_points: list[tuple[float, float]] | None = None,
        direction: str = "top-left-to-bottom-right",
        curve_intensity: float = 0.3,
        num_curve_points: int = 20,
    ) -> tuple["IrregularPanel", "IrregularPanel"]:
        """Split this panel along a curved bezier line, creating two curved panels.

        Divides the panel along a curved line using bezier control points.
        This is useful for creating dynamic manga-style layouts with flowing,
        organic panel divisions instead of straight diagonal cuts.

        Args:
            control_points: Optional list of (x, y) tuples defining bezier control
                points. If None, default S-curve control points are generated based
                on direction and curve_intensity. Points should be in relative
                coordinates (-0.5 to 0.5 for each axis).
            direction: Direction of the curved split. Valid values:
                - "top-left-to-bottom-right" (default): Curve from top-left area
                  to bottom-right area.
                - "top-right-to-bottom-left": Curve from top-right area to
                  bottom-left area.
            curve_intensity: How much the curve bulges (0.0-1.0). Higher values
                create more pronounced curves. Default is 0.3. Only used when
                control_points is None.
            num_curve_points: Number of points to generate along the curve.
                Higher values create smoother curves. Default is 20.

        Returns:
            A tuple of two IrregularPanel objects representing the split portions.

        Raises:
            ValueError: If direction is not valid or control_points has < 2 points.

        Example:
            >>> panel = Panel(width=400, height=400)
            >>> # Simple curved split with default S-curve
            >>> top_panel, bottom_panel = panel.split_curve()
            >>>
            >>> # Custom bezier curve control points (relative coordinates)
            >>> ctrl = [(-0.5, 0.5), (-0.2, 0.3), (0.2, -0.3), (0.5, -0.5)]
            >>> left_panel, right_panel = panel.split_curve(control_points=ctrl)

        Note:
            - Both resulting panels are positioned at the original panel's center.
            - Content from the original panel is NOT automatically transferred.
            - Border and background settings are copied to both new panels.
            - The original panel is not modified.
        """
        from comix.utils.bezier import bezier_curve

        valid_directions = ("top-left-to-bottom-right", "top-right-to-bottom-left")
        if direction not in valid_directions:
            raise ValueError(
                f"Invalid direction '{direction}' for split_curve. "
                f"Valid directions: {', '.join(valid_directions)}"
            )

        half_w = self.width / 2
        half_h = self.height / 2

        # Generate default control points if not provided
        if control_points is None:
            curve_intensity = max(0.0, min(1.0, curve_intensity))

            if direction == "top-left-to-bottom-right":
                # S-curve from top-left to bottom-right
                control_points = [
                    (-0.5, 0.5),   # Start: top-left corner
                    (-0.5 + curve_intensity, 0.5 - curve_intensity * 0.5),  # Control 1
                    (0.5 - curve_intensity, -0.5 + curve_intensity * 0.5),  # Control 2
                    (0.5, -0.5),   # End: bottom-right corner
                ]
            else:  # top-right-to-bottom-left
                # S-curve from top-right to bottom-left
                control_points = [
                    (0.5, 0.5),    # Start: top-right corner
                    (0.5 - curve_intensity, 0.5 - curve_intensity * 0.5),  # Control 1
                    (-0.5 + curve_intensity, -0.5 + curve_intensity * 0.5),  # Control 2
                    (-0.5, -0.5),  # End: bottom-left corner
                ]

        if len(control_points) < 2:
            raise ValueError(
                f"split_curve requires at least 2 control points, got: {len(control_points)}"
            )

        # Convert relative coordinates to absolute coordinates
        abs_control_points = [
            (p[0] * self.width, p[1] * self.height) for p in control_points
        ]

        # Generate curve points using cubic bezier
        if len(abs_control_points) == 2:
            # Linear interpolation for 2 points
            p0, p1 = abs_control_points
            t_values = np.linspace(0, 1, num_curve_points)
            curve_points = [
                (p0[0] + t * (p1[0] - p0[0]), p0[1] + t * (p1[1] - p0[1]))
                for t in t_values
            ]
        elif len(abs_control_points) == 3:
            # Quadratic bezier for 3 points
            p0, p1, p2 = abs_control_points
            t_values = np.linspace(0, 1, num_curve_points)
            curve_points = [
                (
                    (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0],
                    (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1],
                )
                for t in t_values
            ]
        else:
            # Cubic bezier for 4+ points (use first 4)
            p0 = abs_control_points[0]
            p1 = abs_control_points[1]
            p2 = abs_control_points[-2] if len(abs_control_points) > 3 else abs_control_points[1]
            p3 = abs_control_points[-1]
            curve_array = bezier_curve(p0, p1, p2, p3, num_curve_points)
            curve_points = [(pt[0], pt[1]) for pt in curve_array]

        # Build panel polygons based on direction
        # Panel 1 includes the "upper/left" side of the curve
        # Panel 2 includes the "lower/right" side of the curve

        if direction == "top-left-to-bottom-right":
            # Panel 1: Top-right region (above the curve)
            # Corners: top-left, top-right, bottom-right, then curve back to top-left
            panel1_points = [
                (-half_w, half_h),   # Top-left
                (half_w, half_h),    # Top-right
                (half_w, -half_h),   # Bottom-right
            ]
            # Add curve points in reverse (from bottom-right to top-left)
            panel1_points.extend(reversed(curve_points))

            # Panel 2: Bottom-left region (below the curve)
            # Start with curve, then corners
            panel2_points = list(curve_points)
            panel2_points.append((-half_w, -half_h))  # Bottom-left corner
        else:  # top-right-to-bottom-left
            # Panel 1: Top-left region (left of the curve)
            panel1_points = [
                (-half_w, half_h),   # Top-left
            ]
            # Add curve points (from top-right to bottom-left)
            panel1_points.extend(curve_points)
            panel1_points.append((-half_w, -half_h))  # Bottom-left corner

            # Panel 2: Bottom-right region (right of the curve)
            # Corners first, then curve in reverse
            panel2_points = [
                (half_w, half_h),    # Top-right
                (half_w, -half_h),   # Bottom-right
            ]
            panel2_points.extend(reversed(curve_points))

        # Create the two irregular panels
        panel1 = IrregularPanel(
            points=panel1_points,
            border=Border(
                color=self.border.color,
                width=self.border.width,
                style=self.border.style,
                radius=self.border.radius,
            ),
            background_color=self.background_color,
            padding=self.padding,
        )

        panel2 = IrregularPanel(
            points=panel2_points,
            border=Border(
                color=self.border.color,
                width=self.border.width,
                style=self.border.style,
                radius=self.border.radius,
            ),
            background_color=self.background_color,
            padding=self.padding,
        )

        # Position both panels at the original panel's center
        original_center = self.get_center()
        center_tuple = (float(original_center[0]), float(original_center[1]))
        panel1.move_to(center_tuple)
        panel2.move_to(center_tuple)

        return (panel1, panel2)


class DiagonalPanel(Panel):
    """Panel with one corner cut diagonally.

    Creates dynamic, manga-style panels where one corner is cut at an angle.
    Commonly used for shock, surprise, or dramatic moments in comics.

    Args:
        width: Panel width in pixels.
        height: Panel height in pixels.
        diagonal_angle: Angle of the diagonal cut in degrees (default 45).
        direction: Which corner to cut ("top-left", "top-right",
            "bottom-left", "bottom-right").
        **kwargs: Additional Panel parameters.

    Example:
        >>> panel = DiagonalPanel(
        ...     width=400,
        ...     height=400,
        ...     diagonal_angle=45,
        ...     direction="top-left"
        ... )
    """

    VALID_DIRECTIONS = ("top-left", "top-right", "bottom-left", "bottom-right")

    def __init__(
        self,
        width: float = 300.0,
        height: float = 300.0,
        diagonal_angle: float = 45.0,
        direction: str = "top-left",
        **kwargs: Any,
    ) -> None:
        if direction not in self.VALID_DIRECTIONS:
            logger.warning(
                "Invalid diagonal direction '%s', falling back to 'top-left'. "
                "Valid directions: %s",
                direction,
                ", ".join(self.VALID_DIRECTIONS),
            )
            direction = "top-left"

        # Clamp angle to reasonable range
        diagonal_angle = max(5.0, min(85.0, diagonal_angle))

        self.diagonal_angle = diagonal_angle
        self.direction = direction

        super().__init__(width=width, height=height, **kwargs)

    def generate_points(self) -> None:
        """Generate diagonal panel polygon points."""
        half_w = self.width / 2
        half_h = self.height / 2

        # Calculate cut depth based on angle
        angle_rad = np.radians(self.diagonal_angle)
        cut_ratio = min(0.5, np.tan(angle_rad) * 0.3)

        # Determine cut dimensions
        cut_x = self.width * cut_ratio
        cut_y = self.height * cut_ratio

        # Base rectangle corners (clockwise from top-left)
        top_left = (-half_w, half_h)
        top_right = (half_w, half_h)
        bottom_right = (half_w, -half_h)
        bottom_left = (-half_w, -half_h)

        # Create polygon based on which corner is cut
        if self.direction == "top-left":
            points = [
                (-half_w + cut_x, half_h),  # Cut start on top
                top_right,
                bottom_right,
                bottom_left,
                (-half_w, half_h - cut_y),  # Cut end on left
            ]
        elif self.direction == "top-right":
            points = [
                top_left,
                (half_w - cut_x, half_h),  # Cut start on top
                (half_w, half_h - cut_y),  # Cut end on right
                bottom_right,
                bottom_left,
            ]
        elif self.direction == "bottom-right":
            points = [
                top_left,
                top_right,
                (half_w, -half_h + cut_y),  # Cut start on right
                (half_w - cut_x, -half_h),  # Cut end on bottom
                bottom_left,
            ]
        else:  # bottom-left
            points = [
                top_left,
                top_right,
                bottom_right,
                (-half_w + cut_x, -half_h),  # Cut start on bottom
                (-half_w, -half_h + cut_y),  # Cut end on left
            ]

        # Close the polygon
        points.append(points[0])
        self._points = np.array(points, dtype=np.float64)

    def get_render_data(self) -> dict[str, Any]:
        """Get data for rendering."""
        data = super().get_render_data()
        data.update(
            {
                "shape": "diagonal",
                "diagonal_angle": self.diagonal_angle,
                "diagonal_direction": self.direction,
            }
        )
        return data


class TrapezoidPanel(Panel):
    """Trapezoid-shaped panel with different top and bottom widths.

    Creates panels that are wider at one end than the other, useful for
    action sequences, perspective effects, and dynamic layouts.

    Args:
        top_width: Width at the top of the panel.
        bottom_width: Width at the bottom of the panel.
        height: Panel height in pixels.
        **kwargs: Additional Panel parameters.

    Example:
        >>> panel = TrapezoidPanel(
        ...     top_width=600,
        ...     bottom_width=300,
        ...     height=800
        ... )
    """

    def __init__(
        self,
        top_width: float = 300.0,
        bottom_width: float = 200.0,
        height: float = 300.0,
        **kwargs: Any,
    ) -> None:
        # Validate widths
        if top_width <= 0:
            raise ValueError(f"top_width must be positive, got: {top_width}")
        if bottom_width <= 0:
            raise ValueError(f"bottom_width must be positive, got: {bottom_width}")
        if height <= 0:
            raise ValueError(f"height must be positive, got: {height}")

        self.top_width = top_width
        self.bottom_width = bottom_width

        # Use max width for bounding box purposes
        max_width = max(top_width, bottom_width)
        super().__init__(width=max_width, height=height, **kwargs)

    def generate_points(self) -> None:
        """Generate trapezoid panel polygon points."""
        half_h = self.height / 2
        half_top = self.top_width / 2
        half_bottom = self.bottom_width / 2

        # Trapezoid corners (clockwise from top-left)
        points = [
            (-half_top, half_h),      # Top-left
            (half_top, half_h),       # Top-right
            (half_bottom, -half_h),   # Bottom-right
            (-half_bottom, -half_h),  # Bottom-left
            (-half_top, half_h),      # Close path
        ]

        self._points = np.array(points, dtype=np.float64)

    def get_render_data(self) -> dict[str, Any]:
        """Get data for rendering."""
        data = super().get_render_data()
        data.update(
            {
                "shape": "trapezoid",
                "top_width": self.top_width,
                "bottom_width": self.bottom_width,
            }
        )
        return data


class IrregularPanel(Panel):
    """Panel with custom polygon shape.

    Creates panels with arbitrary polygon shapes for special effects,
    star-bursts, or unique artistic layouts.

    Args:
        points: List of (x, y) tuples defining the polygon vertices.
            Points should be in order (clockwise or counter-clockwise).
            Coordinates are relative to the panel center.
        **kwargs: Additional Panel parameters.

    Example:
        >>> # Star-burst panel shape
        >>> star_points = [
        ...     (0, 100), (30, 30), (100, 0), (30, -30),
        ...     (0, -100), (-30, -30), (-100, 0), (-30, 30)
        ... ]
        >>> panel = IrregularPanel(points=star_points)

    Note:
        - The polygon will be auto-closed (no need to repeat first point).
        - Self-intersecting polygons may render unexpectedly.
        - Very complex polygons (100+ points) may slow rendering.
    """

    def __init__(
        self,
        points: list[tuple[float, float]],
        **kwargs: Any,
    ) -> None:
        # Validate points
        if len(points) < 3:
            raise ValueError(
                f"IrregularPanel requires at least 3 points, got: {len(points)}"
            )

        # Warn about very complex polygons
        if len(points) > 100:
            logger.warning(
                "IrregularPanel has %d points, which may slow rendering. "
                "Consider simplifying the polygon.",
                len(points),
            )

        self.polygon_points = list(points)

        # Calculate bounding box for width/height
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        width = max(xs) - min(xs)
        height = max(ys) - min(ys)

        # Check for self-intersection
        if self._is_self_intersecting(points):
            logger.warning(
                "IrregularPanel polygon appears to be self-intersecting. "
                "This may cause unexpected rendering results."
            )

        super().__init__(width=width, height=height, **kwargs)

    def _is_self_intersecting(
        self, points: list[tuple[float, float]]
    ) -> bool:
        """Check if polygon edges intersect (basic check)."""
        n = len(points)
        if n < 4:
            return False

        def ccw(a: tuple[float, float], b: tuple[float, float], c: tuple[float, float]) -> bool:
            """Check counter-clockwise orientation."""
            return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])

        def intersects(
            p1: tuple[float, float],
            p2: tuple[float, float],
            p3: tuple[float, float],
            p4: tuple[float, float],
        ) -> bool:
            """Check if line segment p1-p2 intersects p3-p4."""
            return ccw(p1, p3, p4) != ccw(p2, p3, p4) and ccw(p1, p2, p3) != ccw(p1, p2, p4)

        # Check non-adjacent edges for intersection
        for i in range(n):
            for j in range(i + 2, n):
                # Skip adjacent edges
                if i == 0 and j == n - 1:
                    continue
                if intersects(points[i], points[(i + 1) % n], points[j], points[(j + 1) % n]):
                    return True
        return False

    def generate_points(self) -> None:
        """Generate irregular panel polygon points."""
        # Center the polygon
        xs = [p[0] for p in self.polygon_points]
        ys = [p[1] for p in self.polygon_points]
        center_x = (max(xs) + min(xs)) / 2
        center_y = (max(ys) + min(ys)) / 2

        # Create centered points
        centered_points = [
            (p[0] - center_x, p[1] - center_y)
            for p in self.polygon_points
        ]

        # Close the polygon
        centered_points.append(centered_points[0])

        self._points = np.array(centered_points, dtype=np.float64)

    def get_render_data(self) -> dict[str, Any]:
        """Get data for rendering."""
        data = super().get_render_data()
        data.update(
            {
                "shape": "irregular",
                "polygon_points": self.polygon_points,
            }
        )
        return data
