"""Constraint-based layout for positioning comic elements.

This module provides a declarative constraint system for positioning
CObjects relative to container bounds and each other.

Example:
    layout = ConstraintLayout(width=800, height=600)

    # Add elements with constraints
    layout.add(panel1,
        left=layout.left + 20,
        top=layout.top + 20,
        width=200,
        height=300)

    layout.add(panel2,
        left=panel1.right + 10,
        top=panel1.top,
        width=panel1.width,
        height=panel1.height)

    # Solve and apply positions
    layout.solve()
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import TYPE_CHECKING, Any, Self

if TYPE_CHECKING:
    from comix.cobject.cobject import CObject


class ConstraintPriority(Enum):
    """Priority levels for constraints.

    Higher priority constraints are satisfied first.
    """

    REQUIRED = auto()  # Must be satisfied
    HIGH = auto()  # Strong preference
    MEDIUM = auto()  # Normal preference
    LOW = auto()  # Weak preference


class EdgeType(Enum):
    """Edge types for constraint references."""

    LEFT = "left"
    RIGHT = "right"
    TOP = "top"
    BOTTOM = "bottom"
    CENTER_X = "center_x"
    CENTER_Y = "center_y"
    WIDTH = "width"
    HEIGHT = "height"


@dataclass
class ConstraintValue:
    """A constraint value that can reference other elements or be absolute.

    Supports simple arithmetic for expressing relative constraints.
    """

    # Source can be:
    # - None: absolute value
    # - "container": container bounds
    # - str: reference to another element by name
    # - CObject: reference to another element directly
    source: None | str | CObject = None
    edge: EdgeType | None = None
    offset: float = 0.0
    multiplier: float = 1.0

    def __add__(self, other: float | int) -> ConstraintValue:
        """Add offset to constraint value."""
        return ConstraintValue(
            source=self.source,
            edge=self.edge,
            offset=self.offset + float(other),
            multiplier=self.multiplier,
        )

    def __radd__(self, other: float | int) -> ConstraintValue:
        """Add offset to constraint value (right-hand side)."""
        return self.__add__(other)

    def __sub__(self, other: float | int) -> ConstraintValue:
        """Subtract offset from constraint value."""
        return ConstraintValue(
            source=self.source,
            edge=self.edge,
            offset=self.offset - float(other),
            multiplier=self.multiplier,
        )

    def __mul__(self, other: float | int) -> ConstraintValue:
        """Multiply constraint value."""
        return ConstraintValue(
            source=self.source,
            edge=self.edge,
            offset=self.offset,
            multiplier=self.multiplier * float(other),
        )

    def __rmul__(self, other: float | int) -> ConstraintValue:
        """Multiply constraint value (right-hand side)."""
        return self.__mul__(other)

    def __truediv__(self, other: float | int) -> ConstraintValue:
        """Divide constraint value."""
        return ConstraintValue(
            source=self.source,
            edge=self.edge,
            offset=self.offset,
            multiplier=self.multiplier / float(other),
        )


@dataclass
class ElementRef:
    """Reference to an element for building constraints.

    Provides properties for referencing edges and dimensions.
    """

    name: str | None = None
    element: CObject | None = None
    is_container: bool = False

    @property
    def left(self) -> ConstraintValue:
        """Left edge of the element."""
        source = "container" if self.is_container else (self.element or self.name)
        return ConstraintValue(source=source, edge=EdgeType.LEFT)

    @property
    def right(self) -> ConstraintValue:
        """Right edge of the element."""
        source = "container" if self.is_container else (self.element or self.name)
        return ConstraintValue(source=source, edge=EdgeType.RIGHT)

    @property
    def top(self) -> ConstraintValue:
        """Top edge of the element."""
        source = "container" if self.is_container else (self.element or self.name)
        return ConstraintValue(source=source, edge=EdgeType.TOP)

    @property
    def bottom(self) -> ConstraintValue:
        """Bottom edge of the element."""
        source = "container" if self.is_container else (self.element or self.name)
        return ConstraintValue(source=source, edge=EdgeType.BOTTOM)

    @property
    def center_x(self) -> ConstraintValue:
        """Horizontal center of the element."""
        source = "container" if self.is_container else (self.element or self.name)
        return ConstraintValue(source=source, edge=EdgeType.CENTER_X)

    @property
    def center_y(self) -> ConstraintValue:
        """Vertical center of the element."""
        source = "container" if self.is_container else (self.element or self.name)
        return ConstraintValue(source=source, edge=EdgeType.CENTER_Y)

    @property
    def width(self) -> ConstraintValue:
        """Width of the element."""
        source = "container" if self.is_container else (self.element or self.name)
        return ConstraintValue(source=source, edge=EdgeType.WIDTH)

    @property
    def height(self) -> ConstraintValue:
        """Height of the element."""
        source = "container" if self.is_container else (self.element or self.name)
        return ConstraintValue(source=source, edge=EdgeType.HEIGHT)


@dataclass
class Constraint:
    """A single constraint on an element.

    Constraints define relationships between element properties
    (left, right, top, bottom, width, height, center_x, center_y)
    and either absolute values or other element properties.
    """

    target_property: str  # Property being constrained
    value: float | ConstraintValue  # Target value or reference
    priority: ConstraintPriority = ConstraintPriority.REQUIRED

    def resolve(
        self,
        resolved_positions: dict[str | CObject, dict[str, float]],
        container_bounds: dict[str, float],
    ) -> float | None:
        """Resolve the constraint value.

        Args:
            resolved_positions: Already resolved element positions.
            container_bounds: Container boundaries (left, right, top, bottom, width, height).

        Returns:
            The resolved absolute value, or None if dependencies aren't resolved.
        """
        if isinstance(self.value, (int, float)):
            return float(self.value)

        if not isinstance(self.value, ConstraintValue):
            return None

        # Get source value
        source_value: float | None = None
        source = self.value.source

        if source == "container" or source is None:
            # Reference to container
            edge = self.value.edge
            if edge == EdgeType.LEFT:
                source_value = container_bounds.get("left", 0.0)
            elif edge == EdgeType.RIGHT:
                source_value = container_bounds.get("right", container_bounds.get("width", 0.0))
            elif edge == EdgeType.TOP:
                source_value = container_bounds.get("top", 0.0)
            elif edge == EdgeType.BOTTOM:
                source_value = container_bounds.get(
                    "bottom", container_bounds.get("height", 0.0)
                )
            elif edge == EdgeType.CENTER_X:
                source_value = container_bounds.get("width", 0.0) / 2
            elif edge == EdgeType.CENTER_Y:
                source_value = container_bounds.get("height", 0.0) / 2
            elif edge == EdgeType.WIDTH:
                source_value = container_bounds.get("width", 0.0)
            elif edge == EdgeType.HEIGHT:
                source_value = container_bounds.get("height", 0.0)
        else:
            # Reference to another element
            source_key = source
            if source_key not in resolved_positions:
                return None  # Dependency not yet resolved

            pos = resolved_positions[source_key]
            edge = self.value.edge
            if edge == EdgeType.LEFT:
                source_value = pos.get("left")
            elif edge == EdgeType.RIGHT:
                source_value = pos.get("right")
            elif edge == EdgeType.TOP:
                source_value = pos.get("top")
            elif edge == EdgeType.BOTTOM:
                source_value = pos.get("bottom")
            elif edge == EdgeType.CENTER_X:
                source_value = pos.get("center_x")
            elif edge == EdgeType.CENTER_Y:
                source_value = pos.get("center_y")
            elif edge == EdgeType.WIDTH:
                source_value = pos.get("width")
            elif edge == EdgeType.HEIGHT:
                source_value = pos.get("height")

        if source_value is None:
            return None

        # Apply multiplier and offset
        return source_value * self.value.multiplier + self.value.offset


@dataclass
class ElementConstraints:
    """Collection of constraints for a single element."""

    element: CObject
    name: str | None = None
    constraints: list[Constraint] = field(default_factory=list)

    # Default dimensions if not constrained
    default_width: float = 100.0
    default_height: float = 100.0

    def add_constraint(
        self,
        property_name: str,
        value: float | ConstraintValue,
        priority: ConstraintPriority = ConstraintPriority.REQUIRED,
    ) -> None:
        """Add a constraint to this element.

        Args:
            property_name: Property to constrain (left, right, top, bottom, width, height, center_x, center_y).
            value: Target value or reference.
            priority: Constraint priority.
        """
        self.constraints.append(
            Constraint(target_property=property_name, value=value, priority=priority)
        )


class ConstraintLayout:
    """Constraint-based layout manager.

    Positions elements based on declarative constraints that
    define relationships between element edges and dimensions.

    Example:
        layout = ConstraintLayout(width=800, height=600)

        # Reference to container for constraints
        ref = layout.ref()  # or use layout.left, layout.right, etc.

        # Add element with constraints
        layout.add(panel1,
            left=ref.left + 20,
            top=ref.top + 20,
            width=200,
            height=300)

        # Position relative to another element
        layout.add(panel2,
            left=layout.ref(panel1).right + 10,
            top=layout.ref(panel1).top,
            width=layout.ref(panel1).width,
            height=layout.ref(panel1).height)

        # Solve constraints and apply to elements
        layout.solve()
    """

    def __init__(
        self,
        width: float = 800.0,
        height: float = 1200.0,
        offset_x: float = 0.0,
        offset_y: float = 0.0,
    ) -> None:
        """Initialize constraint layout.

        Args:
            width: Container width.
            height: Container height.
            offset_x: X offset for container origin.
            offset_y: Y offset for container origin.
        """
        self.width = width
        self.height = height
        self.offset_x = offset_x
        self.offset_y = offset_y

        self._elements: dict[str | CObject, ElementConstraints] = {}
        self._resolved: dict[str | CObject, dict[str, float]] = {}
        self._container_ref = ElementRef(is_container=True)

    @property
    def container_bounds(self) -> dict[str, float]:
        """Get container boundary values."""
        return {
            "left": self.offset_x,
            "right": self.offset_x + self.width,
            "top": self.offset_y,
            "bottom": self.offset_y + self.height,
            "width": self.width,
            "height": self.height,
            "center_x": self.offset_x + self.width / 2,
            "center_y": self.offset_y + self.height / 2,
        }

    # Container edge properties for convenient constraint building
    @property
    def left(self) -> ConstraintValue:
        """Left edge of container."""
        return self._container_ref.left

    @property
    def right(self) -> ConstraintValue:
        """Right edge of container."""
        return self._container_ref.right

    @property
    def top(self) -> ConstraintValue:
        """Top edge of container."""
        return self._container_ref.top

    @property
    def bottom(self) -> ConstraintValue:
        """Bottom edge of container."""
        return self._container_ref.bottom

    @property
    def center_x(self) -> ConstraintValue:
        """Horizontal center of container."""
        return self._container_ref.center_x

    @property
    def center_y(self) -> ConstraintValue:
        """Vertical center of container."""
        return self._container_ref.center_y

    @property
    def container_width(self) -> ConstraintValue:
        """Width of container."""
        return self._container_ref.width

    @property
    def container_height(self) -> ConstraintValue:
        """Height of container."""
        return self._container_ref.height

    def ref(self, element: CObject | None = None) -> ElementRef:
        """Get a reference to an element for building constraints.

        Args:
            element: Element to reference, or None for container.

        Returns:
            ElementRef that can be used to build constraints.
        """
        if element is None:
            return self._container_ref
        return ElementRef(element=element)

    def add(
        self,
        element: CObject,
        name: str | None = None,
        *,
        left: float | ConstraintValue | None = None,
        right: float | ConstraintValue | None = None,
        top: float | ConstraintValue | None = None,
        bottom: float | ConstraintValue | None = None,
        width: float | ConstraintValue | None = None,
        height: float | ConstraintValue | None = None,
        center_x: float | ConstraintValue | None = None,
        center_y: float | ConstraintValue | None = None,
        priority: ConstraintPriority = ConstraintPriority.REQUIRED,
    ) -> Self:
        """Add an element with constraints.

        At minimum, you need to constrain:
        - Horizontal position (left, right, or center_x) and width, OR left and right
        - Vertical position (top, bottom, or center_y) and height, OR top and bottom

        Args:
            element: The CObject to position.
            name: Optional name for referencing this element.
            left: Left edge constraint.
            right: Right edge constraint.
            top: Top edge constraint.
            bottom: Bottom edge constraint.
            width: Width constraint.
            height: Height constraint.
            center_x: Horizontal center constraint.
            center_y: Vertical center constraint.
            priority: Default priority for constraints.

        Returns:
            Self for method chaining.
        """
        # Get default dimensions from element
        default_width = getattr(element, "width", 100.0)
        default_height = getattr(element, "height", 100.0)

        key: str | CObject = name if name else element
        elem_constraints = ElementConstraints(
            element=element,
            name=name,
            default_width=default_width,
            default_height=default_height,
        )

        # Add provided constraints
        if left is not None:
            elem_constraints.add_constraint("left", left, priority)
        if right is not None:
            elem_constraints.add_constraint("right", right, priority)
        if top is not None:
            elem_constraints.add_constraint("top", top, priority)
        if bottom is not None:
            elem_constraints.add_constraint("bottom", bottom, priority)
        if width is not None:
            elem_constraints.add_constraint("width", width, priority)
        if height is not None:
            elem_constraints.add_constraint("height", height, priority)
        if center_x is not None:
            elem_constraints.add_constraint("center_x", center_x, priority)
        if center_y is not None:
            elem_constraints.add_constraint("center_y", center_y, priority)

        self._elements[key] = elem_constraints
        return self

    def constrain(
        self,
        element: CObject | str,
        property_name: str,
        value: float | ConstraintValue,
        priority: ConstraintPriority = ConstraintPriority.REQUIRED,
    ) -> Self:
        """Add a constraint to an existing element.

        Args:
            element: Element or element name to constrain.
            property_name: Property to constrain.
            value: Target value or reference.
            priority: Constraint priority.

        Returns:
            Self for method chaining.
        """
        key = element
        if key not in self._elements:
            raise ValueError(f"Element {key} not found in layout. Add it first with add().")

        self._elements[key].add_constraint(property_name, value, priority)
        return self

    def _resolve_element(
        self,
        key: str | CObject,
        elem_constraints: ElementConstraints,
        container_bounds: dict[str, float],
    ) -> dict[str, float] | None:
        """Try to resolve an element's position.

        Args:
            key: Element key.
            elem_constraints: Element's constraints.
            container_bounds: Container bounds.

        Returns:
            Resolved position dict, or None if dependencies not met.
        """
        resolved: dict[str, float | None] = {
            "left": None,
            "right": None,
            "top": None,
            "bottom": None,
            "width": None,
            "height": None,
            "center_x": None,
            "center_y": None,
        }

        # Sort constraints by priority
        sorted_constraints = sorted(
            elem_constraints.constraints, key=lambda c: c.priority.value
        )

        # First pass: resolve all constraints
        # Track if any constraint has unresolved element dependencies
        has_unresolved_dependency = False
        for constraint in sorted_constraints:
            value = constraint.resolve(self._resolved, container_bounds)
            if value is not None:
                resolved[constraint.target_property] = value
            else:
                # Check if this constraint references another element
                if isinstance(constraint.value, ConstraintValue):
                    source = constraint.value.source
                    # If source is an element (not container/None) and not yet resolved
                    if source is not None and source != "container":
                        has_unresolved_dependency = True

        # If we have unresolved element dependencies, wait for them
        if has_unresolved_dependency:
            return None

        # Check if we can compute the final position
        # We need either:
        # - left + width -> can compute right, center_x
        # - right + width -> can compute left, center_x
        # - left + right -> can compute width, center_x
        # - center_x + width -> can compute left, right
        # Same for vertical

        # Try to infer missing values
        has_left = resolved["left"] is not None
        has_right = resolved["right"] is not None
        has_width = resolved["width"] is not None
        has_center_x = resolved["center_x"] is not None

        has_top = resolved["top"] is not None
        has_bottom = resolved["bottom"] is not None
        has_height = resolved["height"] is not None
        has_center_y = resolved["center_y"] is not None

        # Use defaults for width/height if needed
        if not has_width and not (has_left and has_right):
            if has_center_x and not has_left and not has_right:
                resolved["width"] = elem_constraints.default_width
                has_width = True
            elif has_left and not has_right:
                resolved["width"] = elem_constraints.default_width
                has_width = True
            elif has_right and not has_left:
                resolved["width"] = elem_constraints.default_width
                has_width = True
            elif not has_left and not has_right:
                resolved["width"] = elem_constraints.default_width
                has_width = True

        if not has_height and not (has_top and has_bottom):
            if has_center_y and not has_top and not has_bottom:
                resolved["height"] = elem_constraints.default_height
                has_height = True
            elif has_top and not has_bottom:
                resolved["height"] = elem_constraints.default_height
                has_height = True
            elif has_bottom and not has_top:
                resolved["height"] = elem_constraints.default_height
                has_height = True
            elif not has_top and not has_bottom:
                resolved["height"] = elem_constraints.default_height
                has_height = True

        # Compute horizontal position
        if has_left and has_width and resolved["left"] is not None and resolved["width"] is not None:
            resolved["right"] = resolved["left"] + resolved["width"]
            resolved["center_x"] = resolved["left"] + resolved["width"] / 2
        elif has_right and has_width and resolved["right"] is not None and resolved["width"] is not None:
            resolved["left"] = resolved["right"] - resolved["width"]
            resolved["center_x"] = resolved["right"] - resolved["width"] / 2
        elif has_left and has_right and resolved["left"] is not None and resolved["right"] is not None:
            resolved["width"] = resolved["right"] - resolved["left"]
            resolved["center_x"] = (resolved["left"] + resolved["right"]) / 2
        elif has_center_x and has_width and resolved["center_x"] is not None and resolved["width"] is not None:
            resolved["left"] = resolved["center_x"] - resolved["width"] / 2
            resolved["right"] = resolved["center_x"] + resolved["width"] / 2
        else:
            # Default to top-left if nothing specified
            if not has_left and not has_right and not has_center_x:
                left_val = container_bounds["left"]
                width_val = resolved["width"] if resolved["width"] is not None else elem_constraints.default_width
                resolved["left"] = left_val
                resolved["width"] = width_val
                resolved["right"] = left_val + width_val
                resolved["center_x"] = left_val + width_val / 2

        # Compute vertical position
        if has_top and has_height and resolved["top"] is not None and resolved["height"] is not None:
            resolved["bottom"] = resolved["top"] + resolved["height"]
            resolved["center_y"] = resolved["top"] + resolved["height"] / 2
        elif has_bottom and has_height and resolved["bottom"] is not None and resolved["height"] is not None:
            resolved["top"] = resolved["bottom"] - resolved["height"]
            resolved["center_y"] = resolved["bottom"] - resolved["height"] / 2
        elif has_top and has_bottom and resolved["top"] is not None and resolved["bottom"] is not None:
            resolved["height"] = resolved["bottom"] - resolved["top"]
            resolved["center_y"] = (resolved["top"] + resolved["bottom"]) / 2
        elif has_center_y and has_height and resolved["center_y"] is not None and resolved["height"] is not None:
            resolved["top"] = resolved["center_y"] - resolved["height"] / 2
            resolved["bottom"] = resolved["center_y"] + resolved["height"] / 2
        else:
            # Default to top-left if nothing specified
            if not has_top and not has_bottom and not has_center_y:
                top_val = container_bounds["top"]
                height_val = resolved["height"] if resolved["height"] is not None else elem_constraints.default_height
                resolved["top"] = top_val
                resolved["height"] = height_val
                resolved["bottom"] = top_val + height_val
                resolved["center_y"] = top_val + height_val / 2

        # Check if all required values are resolved
        required_keys = ["left", "right", "top", "bottom", "width", "height", "center_x", "center_y"]
        for k in required_keys:
            if resolved[k] is None:
                return None

        # All values are now known to be float, not None
        return {k: v for k, v in resolved.items() if v is not None}

    def solve(self, max_iterations: int = 100) -> dict[str | CObject, dict[str, float]]:
        """Solve all constraints and return resolved positions.

        Uses iterative resolution - elements with no dependencies are
        resolved first, then elements that depend on them, and so on.

        Args:
            max_iterations: Maximum resolution iterations to prevent infinite loops.

        Returns:
            Dictionary mapping element keys to position dictionaries.

        Raises:
            ValueError: If constraints cannot be resolved (circular dependencies, etc.).
        """
        self._resolved.clear()
        container_bounds = self.container_bounds
        unresolved = set(self._elements.keys())

        for iteration in range(max_iterations):
            if not unresolved:
                break

            made_progress = False
            newly_resolved = []

            for key in unresolved:
                elem_constraints = self._elements[key]
                result = self._resolve_element(key, elem_constraints, container_bounds)

                if result is not None:
                    self._resolved[key] = result
                    newly_resolved.append(key)
                    made_progress = True

            for key in newly_resolved:
                unresolved.remove(key)

            if not made_progress and unresolved:
                # Try to resolve with defaults for remaining elements
                for key in list(unresolved):
                    elem = self._elements[key]
                    # Force resolution with defaults
                    default_result = {
                        "left": container_bounds["left"],
                        "top": container_bounds["top"],
                        "width": elem.default_width,
                        "height": elem.default_height,
                        "right": container_bounds["left"] + elem.default_width,
                        "bottom": container_bounds["top"] + elem.default_height,
                        "center_x": container_bounds["left"] + elem.default_width / 2,
                        "center_y": container_bounds["top"] + elem.default_height / 2,
                    }
                    self._resolved[key] = default_result
                    unresolved.remove(key)
                break

        if unresolved:
            unresolved_names = [
                self._elements[k].name or str(k) for k in unresolved
            ]
            raise ValueError(
                f"Could not resolve constraints for: {', '.join(unresolved_names)}. "
                "Check for circular dependencies or missing constraints."
            )

        return self._resolved

    def apply(self) -> Self:
        """Solve constraints and apply positions to elements.

        Returns:
            Self for method chaining.
        """
        positions = self.solve()

        for key, pos in positions.items():
            elem_constraints = self._elements[key]
            element = elem_constraints.element

            # Apply position (center-based)
            element.move_to((pos["center_x"], pos["center_y"]))

            # Apply dimensions if element supports them
            if hasattr(element, "width"):
                element.width = pos["width"]
            if hasattr(element, "height"):
                element.height = pos["height"]

        return self

    def calculate_positions(
        self, num_cells: int | None = None
    ) -> list[dict[str, Any]]:
        """Calculate positions (compatibility with other layout classes).

        This method provides compatibility with GridLayout/FlowLayout interface.
        For constraint layouts, use solve() or apply() instead.

        Args:
            num_cells: Ignored for constraint layouts.

        Returns:
            List of position dictionaries.
        """
        positions = self.solve()
        return [
            {
                "center_x": pos["center_x"],
                "center_y": pos["center_y"],
                "width": pos["width"],
                "height": pos["height"],
            }
            for pos in positions.values()
        ]

    def get_position(self, element: CObject | str) -> dict[str, float] | None:
        """Get resolved position for an element.

        Args:
            element: Element or element name.

        Returns:
            Position dictionary, or None if not resolved.
        """
        if not self._resolved:
            self.solve()
        return self._resolved.get(element)
