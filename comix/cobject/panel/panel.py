"""Panel - Comic panel (frame) container."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Self

import numpy as np

from comix.cobject.cobject import CObject
from comix.constants import ValidValues, validate_value

if TYPE_CHECKING:
    from comix.cobject.bubble.bubble import Bubble
    from comix.cobject.character.character import Character


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
            }
        )
        return data
