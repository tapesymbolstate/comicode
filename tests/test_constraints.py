"""Tests for constraint-based layout system."""

from comix.cobject.panel.panel import Panel
from comix.layout.constraints import (
    ConstraintLayout,
    ConstraintPriority,
    ConstraintValue,
    EdgeType,
    ElementRef,
)


class TestConstraintValue:
    """Tests for ConstraintValue class."""

    def test_constraint_value_creation(self) -> None:
        """Test basic constraint value creation."""
        cv = ConstraintValue(source="container", edge=EdgeType.LEFT, offset=10.0)
        assert cv.source == "container"
        assert cv.edge == EdgeType.LEFT
        assert cv.offset == 10.0
        assert cv.multiplier == 1.0

    def test_constraint_value_addition(self) -> None:
        """Test adding offset to constraint value."""
        cv = ConstraintValue(source="container", edge=EdgeType.LEFT)
        cv2 = cv + 20
        assert cv2.offset == 20.0
        assert cv2.source == cv.source
        assert cv2.edge == cv.edge

    def test_constraint_value_subtraction(self) -> None:
        """Test subtracting offset from constraint value."""
        cv = ConstraintValue(source="container", edge=EdgeType.RIGHT, offset=100.0)
        cv2 = cv - 20
        assert cv2.offset == 80.0

    def test_constraint_value_multiplication(self) -> None:
        """Test multiplying constraint value."""
        cv = ConstraintValue(source="container", edge=EdgeType.WIDTH)
        cv2 = cv * 0.5
        assert cv2.multiplier == 0.5

    def test_constraint_value_division(self) -> None:
        """Test dividing constraint value."""
        cv = ConstraintValue(source="container", edge=EdgeType.WIDTH)
        cv2 = cv / 2
        assert cv2.multiplier == 0.5

    def test_constraint_value_chaining(self) -> None:
        """Test chaining arithmetic operations."""
        cv = ConstraintValue(source="container", edge=EdgeType.WIDTH)
        cv2 = cv * 0.5 + 10
        assert cv2.multiplier == 0.5
        assert cv2.offset == 10.0


class TestElementRef:
    """Tests for ElementRef class."""

    def test_element_ref_container(self) -> None:
        """Test container reference."""
        ref = ElementRef(is_container=True)
        left = ref.left
        assert left.source == "container"
        assert left.edge == EdgeType.LEFT

    def test_element_ref_all_edges(self) -> None:
        """Test all edge references."""
        ref = ElementRef(is_container=True)

        assert ref.left.edge == EdgeType.LEFT
        assert ref.right.edge == EdgeType.RIGHT
        assert ref.top.edge == EdgeType.TOP
        assert ref.bottom.edge == EdgeType.BOTTOM
        assert ref.center_x.edge == EdgeType.CENTER_X
        assert ref.center_y.edge == EdgeType.CENTER_Y
        assert ref.width.edge == EdgeType.WIDTH
        assert ref.height.edge == EdgeType.HEIGHT

    def test_element_ref_with_element(self) -> None:
        """Test reference to a specific element."""
        panel = Panel(width=200, height=300)
        ref = ElementRef(element=panel)

        left = ref.left
        assert left.source == panel
        assert left.edge == EdgeType.LEFT


class TestConstraintLayout:
    """Tests for ConstraintLayout class."""

    def test_layout_creation(self) -> None:
        """Test basic layout creation."""
        layout = ConstraintLayout(width=800, height=600)
        assert layout.width == 800
        assert layout.height == 600

    def test_layout_container_bounds(self) -> None:
        """Test container bounds properties."""
        layout = ConstraintLayout(width=800, height=600, offset_x=10, offset_y=20)
        bounds = layout.container_bounds

        assert bounds["left"] == 10
        assert bounds["right"] == 810
        assert bounds["top"] == 20
        assert bounds["bottom"] == 620
        assert bounds["width"] == 800
        assert bounds["height"] == 600
        assert bounds["center_x"] == 410
        assert bounds["center_y"] == 320

    def test_layout_edge_properties(self) -> None:
        """Test container edge property shortcuts."""
        layout = ConstraintLayout(width=800, height=600)

        assert layout.left.edge == EdgeType.LEFT
        assert layout.right.edge == EdgeType.RIGHT
        assert layout.top.edge == EdgeType.TOP
        assert layout.bottom.edge == EdgeType.BOTTOM
        assert layout.center_x.edge == EdgeType.CENTER_X
        assert layout.center_y.edge == EdgeType.CENTER_Y

    def test_add_element_with_absolute_constraints(self) -> None:
        """Test adding element with absolute position constraints."""
        layout = ConstraintLayout(width=800, height=600)
        panel = Panel(width=200, height=300)

        layout.add(panel, left=100, top=50, width=200, height=300)
        positions = layout.solve()

        pos = positions[panel]
        assert pos["left"] == 100
        assert pos["top"] == 50
        assert pos["width"] == 200
        assert pos["height"] == 300
        assert pos["right"] == 300
        assert pos["bottom"] == 350
        assert pos["center_x"] == 200
        assert pos["center_y"] == 200

    def test_add_element_relative_to_container(self) -> None:
        """Test adding element relative to container edges."""
        layout = ConstraintLayout(width=800, height=600)
        panel = Panel(width=200, height=300)

        layout.add(panel, left=layout.left + 20, top=layout.top + 20, width=200, height=300)
        positions = layout.solve()

        pos = positions[panel]
        assert pos["left"] == 20
        assert pos["top"] == 20

    def test_add_element_relative_to_another_element(self) -> None:
        """Test positioning element relative to another."""
        layout = ConstraintLayout(width=800, height=600)
        panel1 = Panel(width=200, height=300)
        panel2 = Panel(width=200, height=300)

        layout.add(panel1, left=0, top=0, width=200, height=300)
        layout.add(
            panel2,
            left=layout.ref(panel1).right + 10,
            top=layout.ref(panel1).top,
            width=layout.ref(panel1).width,
            height=layout.ref(panel1).height,
        )

        positions = layout.solve()

        assert positions[panel1]["left"] == 0
        assert positions[panel1]["right"] == 200

        assert positions[panel2]["left"] == 210  # panel1.right + 10
        assert positions[panel2]["top"] == 0  # same as panel1.top
        assert positions[panel2]["width"] == 200  # same as panel1.width
        assert positions[panel2]["height"] == 300  # same as panel1.height

    def test_center_constraints(self) -> None:
        """Test centering an element."""
        layout = ConstraintLayout(width=800, height=600)
        panel = Panel(width=200, height=100)

        layout.add(panel, center_x=layout.center_x, center_y=layout.center_y, width=200, height=100)
        positions = layout.solve()

        pos = positions[panel]
        assert pos["center_x"] == 400  # 800 / 2
        assert pos["center_y"] == 300  # 600 / 2
        assert pos["left"] == 300  # center_x - width/2
        assert pos["top"] == 250  # center_y - height/2

    def test_infer_width_from_left_right(self) -> None:
        """Test inferring width from left and right constraints."""
        layout = ConstraintLayout(width=800, height=600)
        panel = Panel()

        layout.add(
            panel,
            left=layout.left + 50,
            right=layout.right - 50,
            top=100,
            height=200,
        )
        positions = layout.solve()

        pos = positions[panel]
        assert pos["left"] == 50
        assert pos["right"] == 750
        assert pos["width"] == 700  # inferred from left and right

    def test_infer_height_from_top_bottom(self) -> None:
        """Test inferring height from top and bottom constraints."""
        layout = ConstraintLayout(width=800, height=600)
        panel = Panel()

        layout.add(
            panel,
            left=100,
            width=200,
            top=layout.top + 50,
            bottom=layout.bottom - 50,
        )
        positions = layout.solve()

        pos = positions[panel]
        assert pos["top"] == 50
        assert pos["bottom"] == 550
        assert pos["height"] == 500  # inferred from top and bottom

    def test_apply_positions_to_elements(self) -> None:
        """Test that apply() updates element positions."""
        layout = ConstraintLayout(width=800, height=600)
        panel = Panel(width=100, height=100)

        layout.add(panel, left=200, top=150, width=300, height=250)
        layout.apply()

        # Check that panel position was updated
        assert panel.position[0] == 350  # center_x
        assert panel.position[1] == 275  # center_y
        assert panel.width == 300
        assert panel.height == 250

    def test_named_elements(self) -> None:
        """Test using named elements for constraints."""
        layout = ConstraintLayout(width=800, height=600)
        panel1 = Panel(width=200, height=300)
        panel2 = Panel(width=200, height=300)

        layout.add(panel1, name="first", left=0, top=0, width=200, height=300)
        layout.add(
            panel2,
            name="second",
            left=layout.ref(panel1).right + 10,
            top=layout.ref(panel1).top,
        )

        positions = layout.solve()

        assert "first" in positions or panel1 in positions
        assert "second" in positions or panel2 in positions

    def test_proportional_constraints(self) -> None:
        """Test proportional sizing."""
        layout = ConstraintLayout(width=800, height=600)
        panel = Panel()

        # Panel takes half the container width
        layout.add(
            panel,
            left=layout.left,
            top=layout.top,
            width=layout.container_width * 0.5,
            height=layout.container_height * 0.5,
        )
        positions = layout.solve()

        pos = positions[panel]
        assert pos["width"] == 400  # 800 * 0.5
        assert pos["height"] == 300  # 600 * 0.5

    def test_complex_expression(self) -> None:
        """Test complex constraint expression."""
        layout = ConstraintLayout(width=800, height=600)
        panel = Panel()

        # Half width minus margin
        layout.add(
            panel,
            left=layout.left + 20,
            top=layout.top + 20,
            width=layout.container_width * 0.5 - 30,
            height=200,
        )
        positions = layout.solve()

        pos = positions[panel]
        assert pos["width"] == 370  # 800 * 0.5 - 30

    def test_three_panels_horizontal(self) -> None:
        """Test three panels arranged horizontally."""
        layout = ConstraintLayout(width=900, height=300)
        p1 = Panel()
        p2 = Panel()
        p3 = Panel()
        spacing = 10

        layout.add(p1, left=0, top=0, width=280, height=300)
        layout.add(
            p2,
            left=layout.ref(p1).right + spacing,
            top=layout.ref(p1).top,
            width=layout.ref(p1).width,
            height=layout.ref(p1).height,
        )
        layout.add(
            p3,
            left=layout.ref(p2).right + spacing,
            top=layout.ref(p1).top,
            width=layout.ref(p1).width,
            height=layout.ref(p1).height,
        )

        positions = layout.solve()

        assert positions[p1]["left"] == 0
        assert positions[p1]["right"] == 280
        assert positions[p2]["left"] == 290  # 280 + 10
        assert positions[p2]["right"] == 570
        assert positions[p3]["left"] == 580  # 570 + 10
        assert positions[p3]["right"] == 860

    def test_default_dimensions_used(self) -> None:
        """Test that default dimensions are used when not constrained."""
        layout = ConstraintLayout(width=800, height=600)
        panel = Panel(width=150, height=200)

        # Only constrain position, not size
        layout.add(panel, left=100, top=50)
        positions = layout.solve()

        pos = positions[panel]
        assert pos["width"] == 150  # Uses panel's default width
        assert pos["height"] == 200  # Uses panel's default height

    def test_calculate_positions_compatibility(self) -> None:
        """Test calculate_positions for compatibility with other layouts."""
        layout = ConstraintLayout(width=800, height=600)
        p1 = Panel(width=200, height=300)
        p2 = Panel(width=200, height=300)

        layout.add(p1, left=0, top=0, width=200, height=300)
        layout.add(p2, left=210, top=0, width=200, height=300)

        positions = layout.calculate_positions()

        assert len(positions) == 2
        assert all("center_x" in p for p in positions)
        assert all("center_y" in p for p in positions)
        assert all("width" in p for p in positions)
        assert all("height" in p for p in positions)

    def test_method_chaining(self) -> None:
        """Test that methods support chaining."""
        layout = ConstraintLayout(width=800, height=600)
        p1 = Panel()
        p2 = Panel()

        result = (
            layout.add(p1, left=0, top=0, width=100, height=100)
            .add(p2, left=110, top=0, width=100, height=100)
            .apply()
        )

        assert result is layout

    def test_get_position(self) -> None:
        """Test getting position for a specific element."""
        layout = ConstraintLayout(width=800, height=600)
        panel = Panel(width=200, height=300)

        layout.add(panel, left=100, top=50, width=200, height=300)

        pos = layout.get_position(panel)
        assert pos is not None
        assert pos["left"] == 100
        assert pos["top"] == 50

    def test_offset_in_layout(self) -> None:
        """Test offset applied to all positions."""
        layout = ConstraintLayout(width=800, height=600, offset_x=100, offset_y=50)
        panel = Panel()

        layout.add(panel, left=layout.left, top=layout.top, width=200, height=300)
        positions = layout.solve()

        pos = positions[panel]
        assert pos["left"] == 100  # offset_x
        assert pos["top"] == 50  # offset_y


class TestConstraintPriority:
    """Tests for constraint priorities."""

    def test_priority_levels(self) -> None:
        """Test that all priority levels exist."""
        assert ConstraintPriority.REQUIRED is not None
        assert ConstraintPriority.HIGH is not None
        assert ConstraintPriority.MEDIUM is not None
        assert ConstraintPriority.LOW is not None

    def test_priority_ordering(self) -> None:
        """Test priority ordering (REQUIRED has lowest value = highest priority)."""
        assert ConstraintPriority.REQUIRED.value < ConstraintPriority.HIGH.value
        assert ConstraintPriority.HIGH.value < ConstraintPriority.MEDIUM.value
        assert ConstraintPriority.MEDIUM.value < ConstraintPriority.LOW.value


class TestEdgeCases:
    """Tests for edge cases and error handling."""

    def test_empty_layout(self) -> None:
        """Test solving empty layout."""
        layout = ConstraintLayout(width=800, height=600)
        positions = layout.solve()
        assert positions == {}

    def test_zero_dimensions(self) -> None:
        """Test element with zero dimensions."""
        layout = ConstraintLayout(width=800, height=600)
        panel = Panel()

        layout.add(panel, left=100, top=50, width=0, height=0)
        positions = layout.solve()

        pos = positions[panel]
        assert pos["width"] == 0
        assert pos["height"] == 0
        assert pos["left"] == pos["right"]  # Both at same position

    def test_negative_offset(self) -> None:
        """Test negative offset in constraints."""
        layout = ConstraintLayout(width=800, height=600)
        panel = Panel()

        layout.add(
            panel,
            right=layout.right - 20,
            top=layout.top + 10,
            width=200,
            height=300,
        )
        positions = layout.solve()

        pos = positions[panel]
        assert pos["right"] == 780  # 800 - 20
        assert pos["left"] == 580  # right - width

    def test_multiple_panels_same_position(self) -> None:
        """Test multiple panels at same position (overlapping)."""
        layout = ConstraintLayout(width=800, height=600)
        p1 = Panel()
        p2 = Panel()

        layout.add(p1, left=100, top=100, width=200, height=200)
        layout.add(p2, left=100, top=100, width=200, height=200)

        positions = layout.solve()

        assert positions[p1]["left"] == positions[p2]["left"]
        assert positions[p1]["top"] == positions[p2]["top"]


class TestConstraintValueExtended:
    """Extended tests for ConstraintValue arithmetic operators."""

    def test_right_hand_addition(self) -> None:
        """Test right-hand addition (number + constraint)."""
        cv = ConstraintValue(source="container", edge=EdgeType.LEFT, offset=10.0)
        cv2 = 5 + cv  # type: ignore[operator]
        assert cv2.offset == 15.0
        assert cv2.source == cv.source
        assert cv2.edge == cv.edge

    def test_right_hand_multiplication(self) -> None:
        """Test right-hand multiplication (number * constraint)."""
        cv = ConstraintValue(source="container", edge=EdgeType.WIDTH, multiplier=1.0)
        cv2 = 2 * cv  # type: ignore[operator]
        assert cv2.multiplier == 2.0
        assert cv2.source == cv.source
        assert cv2.edge == cv.edge


class TestElementReferenceEdges:
    """Tests for element reference edge getters."""

    def test_reference_left_edge(self) -> None:
        """Test referencing left edge of another element."""
        layout = ConstraintLayout(width=800, height=600)
        p1 = Panel(width=200, height=150)
        p2 = Panel(width=100, height=100)

        layout.add(p1, left=100, top=100, width=200, height=150)
        layout.add(
            p2,
            left=layout.ref(p1).left,  # Line 250: LEFT edge reference
            top=300,
            width=100,
            height=100,
        )

        positions = layout.solve()
        assert positions[p2]["left"] == 100  # Same as p1's left

    def test_reference_bottom_edge(self) -> None:
        """Test referencing bottom edge of another element."""
        layout = ConstraintLayout(width=800, height=600)
        p1 = Panel(width=200, height=150)
        p2 = Panel(width=100, height=100)

        layout.add(p1, left=100, top=100, width=200, height=150)
        layout.add(
            p2,
            left=100,
            top=layout.ref(p1).bottom + 10,  # Line 256: BOTTOM edge reference
            width=100,
            height=100,
        )

        positions = layout.solve()
        assert positions[p2]["top"] == 260  # p1.top (100) + p1.height (150) + 10

    def test_reference_center_y(self) -> None:
        """Test referencing center_y of another element."""
        layout = ConstraintLayout(width=800, height=600)
        p1 = Panel(width=200, height=200)
        p2 = Panel(width=100, height=50)

        layout.add(p1, left=100, top=100, width=200, height=200)
        layout.add(
            p2,
            left=350,
            center_y=layout.ref(p1).center_y,  # Line 260: CENTER_Y edge reference
            width=100,
            height=50,
        )

        positions = layout.solve()
        # p1's center_y = 100 + 200/2 = 200
        assert positions[p2]["center_y"] == 200

    def test_reference_height(self) -> None:
        """Test referencing height of another element."""
        layout = ConstraintLayout(width=800, height=600)
        p1 = Panel(width=200, height=175)
        p2 = Panel(width=100, height=100)

        layout.add(p1, left=100, top=100, width=200, height=175)
        layout.add(
            p2,
            left=350,
            top=100,
            width=100,
            height=layout.ref(p1).height,  # Line 264: HEIGHT edge reference
        )

        positions = layout.solve()
        assert positions[p2]["height"] == 175  # Same as p1's height


class TestConstraintRefNone:
    """Tests for ref(None) returning container reference."""

    def test_ref_with_none_returns_container(self) -> None:
        """Test that ref(None) returns container reference."""
        layout = ConstraintLayout(width=800, height=600)
        ref = layout.ref(None)
        assert ref.is_container is True

    def test_ref_none_left_equals_layout_left(self) -> None:
        """Test that ref(None).left equals layout.left."""
        layout = ConstraintLayout(width=800, height=600)
        ref = layout.ref(None)
        assert ref.left.source == "container"
        assert ref.left.edge == EdgeType.LEFT


class TestConstrainMethod:
    """Tests for constrain() method."""

    def test_constrain_nonexistent_element_raises_error(self) -> None:
        """Test that constraining non-existent element raises ValueError."""
        import pytest

        layout = ConstraintLayout(width=800, height=600)
        panel = Panel()

        with pytest.raises(ValueError, match="not found in layout"):
            layout.constrain(panel, "left", 100)

    def test_constrain_existing_element_works(self) -> None:
        """Test that constraining existing element works."""
        layout = ConstraintLayout(width=800, height=600)
        panel = Panel(width=200, height=100)

        layout.add(panel, left=100, top=50)
        layout.constrain(panel, "width", 300)

        positions = layout.solve()
        assert positions[panel]["width"] == 300


class TestDefaultDimensionFallbacks:
    """Tests for default dimension assignment branches."""

    def test_default_width_with_center_x_only(self) -> None:
        """Test default width used when only center_x specified."""
        layout = ConstraintLayout(width=800, height=600)
        panel = Panel(width=123, height=200)
        layout.add(panel, center_x=400, top=100, height=200)
        pos = layout.get_position(panel)
        assert pos is not None
        assert pos["width"] == 123

    def test_default_width_with_right_only(self) -> None:
        """Test default width used when only right edge specified."""
        layout = ConstraintLayout(width=800, height=600)
        panel = Panel(width=150, height=200)
        layout.add(panel, right=500, top=100, height=200)
        pos = layout.get_position(panel)
        assert pos is not None
        assert pos["width"] == 150
        assert pos["left"] == 350  # right - width

    def test_default_width_with_no_horizontal_constraints(self) -> None:
        """Test default width when no horizontal constraints specified."""
        layout = ConstraintLayout(width=800, height=600)
        panel = Panel(width=175, height=200)
        layout.add(panel, top=100, height=200)
        pos = layout.get_position(panel)
        assert pos is not None
        assert pos["width"] == 175

    def test_default_height_with_center_y_only(self) -> None:
        """Test default height used when only center_y specified."""
        layout = ConstraintLayout(width=800, height=600)
        panel = Panel(width=200, height=234)
        layout.add(panel, left=100, width=200, center_y=300)
        pos = layout.get_position(panel)
        assert pos is not None
        assert pos["height"] == 234

    def test_default_height_with_bottom_only(self) -> None:
        """Test default height used when only bottom edge specified."""
        layout = ConstraintLayout(width=800, height=600)
        panel = Panel(width=200, height=180)
        layout.add(panel, left=100, width=200, bottom=400)
        pos = layout.get_position(panel)
        assert pos is not None
        assert pos["height"] == 180

    def test_default_height_with_no_vertical_constraints(self) -> None:
        """Test default height when no vertical constraints specified."""
        layout = ConstraintLayout(width=800, height=600)
        panel = Panel(width=200, height=190)
        layout.add(panel, left=100, width=200)
        pos = layout.get_position(panel)
        assert pos is not None
        assert pos["height"] == 190


class TestDefaultPositionFallbacks:
    """Tests for default position fallbacks when no constraints specified."""

    def test_default_horizontal_position_at_container_left(self) -> None:
        """Test element defaults to left edge when no horizontal constraint given."""
        layout = ConstraintLayout(width=800, height=600, offset_x=50)
        panel = Panel(width=200, height=100)
        layout.add(panel, top=100, height=100)
        pos = layout.get_position(panel)
        assert pos is not None
        assert pos["left"] == 50  # container left (with offset)

    def test_default_vertical_position_at_container_top(self) -> None:
        """Test element defaults to top edge when no vertical constraint given."""
        layout = ConstraintLayout(width=800, height=600, offset_y=75)
        panel = Panel(width=200, height=100)
        layout.add(panel, left=100, width=200)
        pos = layout.get_position(panel)
        assert pos is not None
        assert pos["top"] == 75  # container top (with offset)


class TestBottomEdgePositioning:
    """Tests for computing position from bottom edge and height."""

    def test_position_from_bottom_and_height(self) -> None:
        """Test computing position from bottom edge and height."""
        layout = ConstraintLayout(width=800, height=600)
        panel = Panel()
        layout.add(panel, left=100, width=200, bottom=500, height=150)
        pos = layout.get_position(panel)
        assert pos is not None
        assert pos["bottom"] == 500
        assert pos["height"] == 150
        assert pos["top"] == 350  # bottom - height
        assert pos["center_y"] == 425  # top + height/2


class TestCircularDependencies:
    """Tests for circular dependency detection."""

    def test_circular_dependency_resolves_with_defaults(self) -> None:
        """Test that circular dependencies get resolved with defaults."""
        # The implementation actually handles this gracefully by using defaults
        # when progress can't be made
        layout = ConstraintLayout(width=800, height=600)
        p1 = Panel(width=200, height=100)
        p2 = Panel(width=200, height=100)

        # Create potential circular dependency: p1 depends on p2, p2 depends on p1
        layout.add(p1, left=layout.ref(p2).right + 10, top=100, width=200, height=100)
        layout.add(p2, left=layout.ref(p1).right + 10, top=100, width=200, height=100)

        # The solver handles this by falling back to defaults
        positions = layout.solve()
        # Both elements should be resolved with some position
        assert p1 in positions
        assert p2 in positions


class TestConstraintInvalidValueType:
    """Tests for constraint resolution with invalid value types."""

    def test_constraint_resolve_with_none_source(self) -> None:
        """Test constraint resolution when source is None (absolute container)."""
        from comix.layout.constraints import Constraint

        constraint = Constraint(
            target_property="left",
            value=ConstraintValue(source=None, edge=EdgeType.LEFT),
        )
        container_bounds = {"left": 0, "width": 800, "height": 600}
        result = constraint.resolve({}, container_bounds)
        assert result == 0
