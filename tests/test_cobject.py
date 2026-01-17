"""Tests for CObject base class."""

import numpy as np

from comix.cobject.cobject import CObject
from comix.style.style import Style, MANGA_STYLE


class TestCObject:
    """Tests for CObject class."""

    def test_init_default(self):
        """Test default initialization."""
        obj = CObject()
        assert np.allclose(obj.position, [0, 0])
        assert obj.scale == 1.0
        assert obj.rotation == 0.0
        assert obj.opacity == 1.0
        assert obj.z_index == 0
        assert obj.name == "CObject"

    def test_init_custom(self):
        """Test custom initialization."""
        obj = CObject(
            position=(100, 200),
            scale=2.0,
            rotation=0.5,
            opacity=0.8,
            z_index=5,
            name="test",
        )
        assert np.allclose(obj.position, [100, 200])
        assert obj.scale == 2.0
        assert obj.rotation == 0.5
        assert obj.opacity == 0.8
        assert obj.z_index == 5
        assert obj.name == "test"

    def test_move_to(self):
        """Test move_to method."""
        obj = CObject()
        result = obj.move_to((50, 75))
        assert result is obj  # Returns self for chaining
        assert np.allclose(obj.position, [50, 75])

    def test_shift(self):
        """Test shift method."""
        obj = CObject(position=(10, 20))
        obj.shift((5, -10))
        assert np.allclose(obj.position, [15, 10])

    def test_set_scale(self):
        """Test set_scale method."""
        obj = CObject()
        result = obj.set_scale(2.5)
        assert result is obj
        assert obj.scale == 2.5

    def test_set_opacity(self):
        """Test set_opacity method."""
        obj = CObject()
        obj.set_opacity(0.5)
        assert obj.opacity == 0.5

        obj.set_opacity(1.5)
        assert obj.opacity == 1.0

        obj.set_opacity(-0.5)
        assert obj.opacity == 0.0

    def test_rotate(self):
        """Test rotate method."""
        obj = CObject()
        obj.rotate(0.5)
        assert obj.rotation == 0.5
        obj.rotate(0.3)
        assert obj.rotation == 0.8

    def test_set_rotation(self):
        """Test set_rotation method."""
        obj = CObject(rotation=0.5)
        obj.set_rotation(1.0)
        assert obj.rotation == 1.0

    def test_add_remove_submobjects(self):
        """Test hierarchy management."""
        parent = CObject(name="parent")
        child1 = CObject(name="child1")
        child2 = CObject(name="child2")

        parent.add(child1, child2)
        assert child1 in parent.submobjects
        assert child2 in parent.submobjects
        assert child1.parent is parent
        assert child2.parent is parent

        parent.remove(child1)
        assert child1 not in parent.submobjects
        assert child1.parent is None
        assert child2 in parent.submobjects

    def test_get_family(self):
        """Test get_family method."""
        parent = CObject(name="parent")
        child = CObject(name="child")
        grandchild = CObject(name="grandchild")

        parent.add(child)
        child.add(grandchild)

        family = parent.get_family()
        assert len(family) == 3
        assert parent in family
        assert child in family
        assert grandchild in family

    def test_method_chaining(self):
        """Test that methods can be chained."""
        obj = CObject()
        result = (
            obj.move_to((100, 100))
            .set_scale(2.0)
            .set_opacity(0.8)
            .rotate(0.5)
        )
        assert result is obj
        assert np.allclose(obj.position, [100, 100])
        assert obj.scale == 2.0
        assert obj.opacity == 0.8
        assert obj.rotation == 0.5

    def test_get_render_data(self):
        """Test get_render_data method."""
        obj = CObject(
            position=(50, 100),
            scale=1.5,
            rotation=0.5,
            opacity=0.9,
            z_index=3,
            name="test",
        )
        data = obj.get_render_data()

        assert data["type"] == "CObject"
        assert data["position"] == [50, 100]
        assert data["scale"] == 1.5
        assert data["rotation"] == 0.5
        assert data["opacity"] == 0.9
        assert data["z_index"] == 3
        assert data["name"] == "test"


class TestCObjectStyle:
    """Tests for CObject style functionality."""

    def test_init_with_style(self) -> None:
        """Test creating CObject with style."""
        style = Style(border_color="#FF0000")
        obj = CObject(style=style)
        assert obj.get_style() == style

    def test_set_style(self) -> None:
        """Test set_style method."""
        obj = CObject()
        style = Style(border_width=3.0)
        result = obj.set_style(style)
        assert result is obj  # Returns self for chaining
        assert obj.get_style() == style

    def test_get_style_none(self) -> None:
        """Test get_style when no style is set."""
        obj = CObject()
        assert obj.get_style() is None

    def test_apply_style(self) -> None:
        """Test apply_style method."""
        obj = CObject()
        result = obj.apply_style(MANGA_STYLE)
        assert result is obj
        assert obj.get_style() == MANGA_STYLE

    def test_get_effective_style_no_style(self) -> None:
        """Test get_effective_style when no style is set."""
        obj = CObject()
        style = obj.get_effective_style()
        # Should return default Style
        assert isinstance(style, Style)
        assert style.border_width == 2.0  # Default value

    def test_get_effective_style_with_style(self) -> None:
        """Test get_effective_style with own style."""
        style = Style(border_color="#FF0000", border_width=5.0)
        obj = CObject(style=style)
        effective = obj.get_effective_style()
        assert effective.border_color == "#FF0000"
        assert effective.border_width == 5.0

    def test_style_inheritance_from_parent(self) -> None:
        """Test that child inherits style from parent."""
        parent_style = Style(border_color="#FF0000", border_width=5.0)
        parent = CObject(style=parent_style)
        child = CObject()
        parent.add(child)

        effective = child.get_effective_style()
        assert effective.border_color == "#FF0000"
        assert effective.border_width == 5.0

    def test_style_override_parent(self) -> None:
        """Test that child style overrides parent style."""
        parent_style = Style(border_color="#FF0000", border_width=5.0)
        child_style = Style(border_color="#00FF00")

        parent = CObject(style=parent_style)
        child = CObject(style=child_style)
        parent.add(child)

        effective = child.get_effective_style()
        assert effective.border_color == "#00FF00"  # Child override
        assert effective.border_width == 5.0  # Inherited from parent

    def test_get_render_data_with_style(self) -> None:
        """Test that style is included in render data."""
        style = Style(border_color="#FF0000", border_width=5.0)
        obj = CObject(style=style)
        data = obj.get_render_data()

        assert "style" in data
        assert data["style"]["border_color"] == "#FF0000"
        assert data["style"]["border_width"] == 5.0

    def test_get_render_data_without_style(self) -> None:
        """Test that style is not in render data when not set."""
        obj = CObject()
        data = obj.get_render_data()
        assert "style" not in data

    def test_style_method_chaining(self) -> None:
        """Test that style methods can be chained."""
        obj = CObject()
        result = (
            obj.move_to((100, 100))
            .set_style(MANGA_STYLE)
            .set_scale(2.0)
        )
        assert result is obj
        assert obj.get_style() == MANGA_STYLE


class TestCObjectConvenienceMethods:
    """Tests for CObject convenience methods."""

    def test_center_in_both_axes(self) -> None:
        """Test centering in both axes."""
        obj = CObject()
        obj._points = np.array([[-10, -10], [10, 10]], dtype=np.float64)
        bounds = (0.0, 0.0, 100.0, 100.0)
        result = obj.center_in(bounds)
        assert result is obj
        assert np.allclose(obj.position, [50, 50])

    def test_center_in_x_axis(self) -> None:
        """Test centering in x axis only."""
        obj = CObject(position=(0, 25))
        obj._points = np.array([[-10, -10], [10, 10]], dtype=np.float64)
        bounds = (0.0, 0.0, 100.0, 100.0)
        obj.center_in(bounds, axis="x")
        assert obj.position[0] == 50
        assert obj.position[1] == 25

    def test_center_in_y_axis(self) -> None:
        """Test centering in y axis only."""
        obj = CObject(position=(25, 0))
        obj._points = np.array([[-10, -10], [10, 10]], dtype=np.float64)
        bounds = (0.0, 0.0, 100.0, 100.0)
        obj.center_in(bounds, axis="y")
        assert obj.position[0] == 25
        assert obj.position[1] == 50

    def test_center_in_with_offset_bounds(self) -> None:
        """Test centering with non-zero origin bounds."""
        obj = CObject()
        obj._points = np.array([[-10, -10], [10, 10]], dtype=np.float64)
        bounds = (100.0, 200.0, 50.0, 50.0)
        obj.center_in(bounds)
        assert np.allclose(obj.position, [125, 225])

    def test_to_corner_top_left(self) -> None:
        """Test moving to top-left corner."""
        obj = CObject()
        obj._points = np.array([[-10, -10], [10, 10]], dtype=np.float64)
        bounds = (0.0, 0.0, 100.0, 100.0)
        result = obj.to_corner("top-left", bounds, buff=5.0)
        assert result is obj
        # With 20x20 object, half_w=10, half_h=10
        # top-left: x = 0 + 5 + 10 = 15, y = 0 + 5 + 10 = 15
        assert np.allclose(obj.position, [15, 15])

    def test_to_corner_top_right(self) -> None:
        """Test moving to top-right corner."""
        obj = CObject()
        obj._points = np.array([[-10, -10], [10, 10]], dtype=np.float64)
        bounds = (0.0, 0.0, 100.0, 100.0)
        obj.to_corner("top-right", bounds, buff=5.0)
        # x = 100 - 5 - 10 = 85, y = 5 + 10 = 15
        assert np.allclose(obj.position, [85, 15])

    def test_to_corner_bottom_left(self) -> None:
        """Test moving to bottom-left corner."""
        obj = CObject()
        obj._points = np.array([[-10, -10], [10, 10]], dtype=np.float64)
        bounds = (0.0, 0.0, 100.0, 100.0)
        obj.to_corner("bottom-left", bounds, buff=5.0)
        # x = 5 + 10 = 15, y = 100 - 5 - 10 = 85
        assert np.allclose(obj.position, [15, 85])

    def test_to_corner_bottom_right(self) -> None:
        """Test moving to bottom-right corner."""
        obj = CObject()
        obj._points = np.array([[-10, -10], [10, 10]], dtype=np.float64)
        bounds = (0.0, 0.0, 100.0, 100.0)
        obj.to_corner("bottom-right", bounds, buff=5.0)
        # x = 100 - 5 - 10 = 85, y = 100 - 5 - 10 = 85
        assert np.allclose(obj.position, [85, 85])

    def test_to_corner_invalid(self) -> None:
        """Test to_corner with invalid corner raises error."""
        import pytest
        obj = CObject()
        obj._points = np.array([[-10, -10], [10, 10]], dtype=np.float64)
        bounds = (0.0, 0.0, 100.0, 100.0)
        with pytest.raises(ValueError, match="Invalid corner"):
            obj.to_corner("invalid", bounds)

    def test_to_edge_top(self) -> None:
        """Test moving to top edge."""
        obj = CObject()
        obj._points = np.array([[-10, -10], [10, 10]], dtype=np.float64)
        bounds = (0.0, 0.0, 100.0, 100.0)
        result = obj.to_edge("top", bounds, buff=5.0)
        assert result is obj
        # x = 50 (center), y = 0 + 5 + 10 = 15
        assert np.allclose(obj.position, [50, 15])

    def test_to_edge_bottom(self) -> None:
        """Test moving to bottom edge."""
        obj = CObject()
        obj._points = np.array([[-10, -10], [10, 10]], dtype=np.float64)
        bounds = (0.0, 0.0, 100.0, 100.0)
        obj.to_edge("bottom", bounds, buff=5.0)
        # x = 50, y = 100 - 5 - 10 = 85
        assert np.allclose(obj.position, [50, 85])

    def test_to_edge_left(self) -> None:
        """Test moving to left edge."""
        obj = CObject()
        obj._points = np.array([[-10, -10], [10, 10]], dtype=np.float64)
        bounds = (0.0, 0.0, 100.0, 100.0)
        obj.to_edge("left", bounds, buff=5.0)
        # x = 0 + 5 + 10 = 15, y = 50
        assert np.allclose(obj.position, [15, 50])

    def test_to_edge_right(self) -> None:
        """Test moving to right edge."""
        obj = CObject()
        obj._points = np.array([[-10, -10], [10, 10]], dtype=np.float64)
        bounds = (0.0, 0.0, 100.0, 100.0)
        obj.to_edge("right", bounds, buff=5.0)
        # x = 100 - 5 - 10 = 85, y = 50
        assert np.allclose(obj.position, [85, 50])

    def test_to_edge_invalid(self) -> None:
        """Test to_edge with invalid edge raises error."""
        import pytest
        obj = CObject()
        obj._points = np.array([[-10, -10], [10, 10]], dtype=np.float64)
        bounds = (0.0, 0.0, 100.0, 100.0)
        with pytest.raises(ValueError, match="Invalid edge"):
            obj.to_edge("invalid", bounds)

    def test_hide(self) -> None:
        """Test hide method."""
        obj = CObject(opacity=1.0)
        result = obj.hide()
        assert result is obj
        assert obj.opacity == 0.0

    def test_show(self) -> None:
        """Test show method."""
        obj = CObject(opacity=0.0)
        result = obj.show()
        assert result is obj
        assert obj.opacity == 1.0

    def test_is_visible_true(self) -> None:
        """Test is_visible when visible."""
        obj = CObject(opacity=0.5)
        assert obj.is_visible() is True

    def test_is_visible_false(self) -> None:
        """Test is_visible when hidden."""
        obj = CObject(opacity=0.0)
        assert obj.is_visible() is False

    def test_copy_basic(self) -> None:
        """Test copy creates independent object."""
        obj = CObject(
            position=(50, 100),
            scale=2.0,
            rotation=0.5,
            opacity=0.8,
            name="original",
        )
        copied = obj.copy()

        assert copied is not obj
        assert np.allclose(copied.position, obj.position)
        assert copied.scale == obj.scale
        assert copied.rotation == obj.rotation
        assert copied.opacity == obj.opacity
        assert copied.name == obj.name
        assert copied.parent is None

    def test_copy_independence(self) -> None:
        """Test that copy is independent of original."""
        obj = CObject(position=(50, 100))
        copied = obj.copy()

        # Modify original
        obj.move_to((200, 300))
        obj.set_scale(5.0)

        # Copy should be unchanged
        assert np.allclose(copied.position, [50, 100])
        assert copied.scale == 1.0

    def test_copy_with_submobjects(self) -> None:
        """Test copy includes submobjects."""
        parent = CObject(name="parent")
        child = CObject(name="child")
        parent.add(child)

        copied = parent.copy()

        assert len(copied.submobjects) == 1
        assert copied.submobjects[0] is not child
        assert copied.submobjects[0].name == "child"

    def test_copy_parent_not_set(self) -> None:
        """Test that copy has no parent even if original did."""
        parent = CObject(name="parent")
        child = CObject(name="child")
        parent.add(child)

        copied_child = child.copy()
        assert copied_child.parent is None

    def test_scale_to_fit_width(self) -> None:
        """Test scale_to_fit_width method."""
        obj = CObject()
        obj._points = np.array([[-50, -25], [50, 25]], dtype=np.float64)
        # Width = 100, Height = 50
        result = obj.scale_to_fit_width(200.0)
        assert result is obj
        # Scale should be 2.0 (200 / 100)
        assert obj.scale == 2.0

    def test_scale_to_fit_width_zero_width(self) -> None:
        """Test scale_to_fit_width with zero width object."""
        obj = CObject()
        # No points, so width is 0
        obj.scale_to_fit_width(200.0)
        assert obj.scale == 1.0  # Should remain unchanged

    def test_scale_to_fit_height(self) -> None:
        """Test scale_to_fit_height method."""
        obj = CObject()
        obj._points = np.array([[-50, -25], [50, 25]], dtype=np.float64)
        # Width = 100, Height = 50
        result = obj.scale_to_fit_height(100.0)
        assert result is obj
        # Scale should be 2.0 (100 / 50)
        assert obj.scale == 2.0

    def test_scale_to_fit_height_zero_height(self) -> None:
        """Test scale_to_fit_height with zero height object."""
        obj = CObject()
        obj.scale_to_fit_height(200.0)
        assert obj.scale == 1.0

    def test_scale_to_fit_preserve_ratio(self) -> None:
        """Test scale_to_fit with aspect ratio preservation."""
        obj = CObject()
        obj._points = np.array([[-50, -25], [50, 25]], dtype=np.float64)
        # Width = 100, Height = 50, aspect ratio = 2:1
        result = obj.scale_to_fit(200.0, 200.0, preserve_aspect_ratio=True)
        assert result is obj
        # Should scale by 2.0 (limited by width since height would require 4x)
        assert obj.scale == 2.0

    def test_scale_to_fit_no_preserve_ratio(self) -> None:
        """Test scale_to_fit without aspect ratio preservation."""
        obj = CObject()
        obj._points = np.array([[-50, -25], [50, 25]], dtype=np.float64)
        # Width = 100, Height = 50
        obj.scale_to_fit(200.0, 100.0, preserve_aspect_ratio=False)
        # scale_x = 2.0, scale_y = 2.0, average = 2.0
        assert obj.scale == 2.0

    def test_scale_to_fit_zero_dimensions(self) -> None:
        """Test scale_to_fit with zero dimension object."""
        obj = CObject()
        obj.scale_to_fit(200.0, 200.0)
        assert obj.scale == 1.0

    def test_hide_show_chaining(self) -> None:
        """Test hide and show can be chained."""
        obj = CObject()
        result = obj.hide().move_to((100, 100)).show()
        assert result is obj
        assert obj.opacity == 1.0
        assert np.allclose(obj.position, [100, 100])

    def test_convenience_methods_chaining(self) -> None:
        """Test multiple convenience methods can be chained together."""
        obj = CObject()
        obj._points = np.array([[-10, -10], [10, 10]], dtype=np.float64)
        bounds = (0.0, 0.0, 100.0, 100.0)
        result = (
            obj.center_in(bounds)
            .scale_to_fit_width(40.0)
            .hide()
        )
        assert result is obj
        assert np.allclose(obj.position, [50, 50])
        assert obj.scale == 2.0  # 40 / 20
        assert obj.opacity == 0.0


class TestCObjectNextTo:
    """Tests for CObject next_to positioning method."""

    def test_next_to_right(self) -> None:
        """Test positioning next to another object on the right."""
        obj1 = CObject()
        obj1._points = np.array([[-25, -25], [25, 25]], dtype=np.float64)
        obj1.move_to((100, 100))

        obj2 = CObject()
        obj2._points = np.array([[-10, -10], [10, 10]], dtype=np.float64)

        result = obj2.next_to(obj1, direction="right", buff=10.0)

        assert result is obj2
        # obj1 center at 100, half_width=25, buff=10, obj2 half_width=10
        # new_x = 100 + 25 + 10 + 10 = 145
        assert obj2.position[0] == 145.0
        assert obj2.position[1] == 100.0  # Same y as obj1 center

    def test_next_to_left(self) -> None:
        """Test positioning next to another object on the left."""
        obj1 = CObject()
        obj1._points = np.array([[-25, -25], [25, 25]], dtype=np.float64)
        obj1.move_to((100, 100))

        obj2 = CObject()
        obj2._points = np.array([[-10, -10], [10, 10]], dtype=np.float64)

        obj2.next_to(obj1, direction="left", buff=10.0)

        # new_x = 100 - 25 - 10 - 10 = 55
        assert obj2.position[0] == 55.0
        assert obj2.position[1] == 100.0

    def test_next_to_up(self) -> None:
        """Test positioning next to another object above."""
        obj1 = CObject()
        obj1._points = np.array([[-25, -25], [25, 25]], dtype=np.float64)
        obj1.move_to((100, 100))

        obj2 = CObject()
        obj2._points = np.array([[-10, -10], [10, 10]], dtype=np.float64)

        obj2.next_to(obj1, direction="up", buff=10.0)

        assert obj2.position[0] == 100.0  # Same x as obj1 center
        # new_y = 100 + 25 + 10 + 10 = 145
        assert obj2.position[1] == 145.0

    def test_next_to_down(self) -> None:
        """Test positioning next to another object below."""
        obj1 = CObject()
        obj1._points = np.array([[-25, -25], [25, 25]], dtype=np.float64)
        obj1.move_to((100, 100))

        obj2 = CObject()
        obj2._points = np.array([[-10, -10], [10, 10]], dtype=np.float64)

        obj2.next_to(obj1, direction="down", buff=10.0)

        assert obj2.position[0] == 100.0
        # new_y = 100 - 25 - 10 - 10 = 55
        assert obj2.position[1] == 55.0

    def test_next_to_invalid_direction(self) -> None:
        """Test next_to with invalid direction defaults to center."""
        obj1 = CObject()
        obj1._points = np.array([[-25, -25], [25, 25]], dtype=np.float64)
        obj1.move_to((100, 100))

        obj2 = CObject()
        obj2._points = np.array([[-10, -10], [10, 10]], dtype=np.float64)

        obj2.next_to(obj1, direction="invalid", buff=10.0)

        # Invalid direction defaults to centering on obj1
        assert obj2.position[0] == 100.0
        assert obj2.position[1] == 100.0

    def test_next_to_default_buff(self) -> None:
        """Test next_to with default buffer."""
        obj1 = CObject()
        obj1._points = np.array([[-20, -20], [20, 20]], dtype=np.float64)
        obj1.move_to((50, 50))

        obj2 = CObject()
        obj2._points = np.array([[-10, -10], [10, 10]], dtype=np.float64)

        obj2.next_to(obj1)  # Default direction is "right", buff is 10.0

        # new_x = 50 + 20 + 10 + 10 = 90
        assert obj2.position[0] == 90.0


class TestCObjectAlignTo:
    """Tests for CObject align_to positioning method."""

    def test_align_to_left(self) -> None:
        """Test aligning to another object's left edge."""
        obj1 = CObject()
        obj1._points = np.array([[0, 0], [100, 100]], dtype=np.float64)
        obj1.move_to((50, 50))
        # obj1 bbox: min=[0,0], max=[100,100] after translation at (50,50)
        # Actually with position offset: min=[50,50], max=[150,150]

        obj2 = CObject()
        obj2._points = np.array([[0, 0], [40, 40]], dtype=np.float64)
        obj2.move_to((200, 200))
        # obj2 bbox: [200,200] to [240,240]

        result = obj2.align_to(obj1, edge="left")

        assert result is obj2
        # obj1 left edge (bbox[0][0]) = 50
        # obj2 left edge (bbox[0][0]) = 200
        # offset = 50 - 200 = -150
        # new obj2.position[0] = 200 + (-150) = 50
        assert obj2.position[0] == 50.0

    def test_align_to_right(self) -> None:
        """Test aligning to another object's right edge."""
        obj1 = CObject()
        obj1._points = np.array([[0, 0], [100, 100]], dtype=np.float64)
        obj1.move_to((50, 50))
        # obj1 bbox: [50,50] to [150,150]

        obj2 = CObject()
        obj2._points = np.array([[0, 0], [40, 40]], dtype=np.float64)
        obj2.move_to((0, 0))
        # obj2 bbox: [0,0] to [40,40]

        obj2.align_to(obj1, edge="right")

        # obj1 right edge = 150
        # obj2 right edge = 40
        # offset = 150 - 40 = 110
        assert obj2.position[0] == 110.0

    def test_align_to_top(self) -> None:
        """Test aligning to another object's top edge."""
        obj1 = CObject()
        obj1._points = np.array([[0, 0], [100, 100]], dtype=np.float64)
        obj1.move_to((50, 50))
        # obj1 bbox: [50,50] to [150,150]

        obj2 = CObject()
        obj2._points = np.array([[0, 0], [40, 40]], dtype=np.float64)
        obj2.move_to((0, 0))
        # obj2 bbox: [0,0] to [40,40]

        obj2.align_to(obj1, edge="top")

        # obj1 top edge (bbox[1][1]) = 150
        # obj2 top edge = 40
        # offset = 150 - 40 = 110
        assert obj2.position[1] == 110.0

    def test_align_to_bottom(self) -> None:
        """Test aligning to another object's bottom edge."""
        obj1 = CObject()
        obj1._points = np.array([[0, 0], [100, 100]], dtype=np.float64)
        obj1.move_to((50, 50))
        # obj1 bbox: [50,50] to [150,150]

        obj2 = CObject()
        obj2._points = np.array([[0, 0], [40, 40]], dtype=np.float64)
        obj2.move_to((200, 200))
        # obj2 bbox: [200,200] to [240,240]

        obj2.align_to(obj1, edge="bottom")

        # obj1 bottom edge = 50
        # obj2 bottom edge = 200
        # offset = 50 - 200 = -150
        assert obj2.position[1] == 50.0

    def test_align_to_center(self) -> None:
        """Test aligning to another object's center."""
        obj1 = CObject()
        obj1._points = np.array([[-50, -50], [50, 50]], dtype=np.float64)
        obj1.move_to((100, 100))
        # obj1 center at (100, 100)

        obj2 = CObject()
        obj2._points = np.array([[-20, -20], [20, 20]], dtype=np.float64)
        obj2.move_to((0, 0))

        obj2.align_to(obj1, edge="center")

        # Should move to obj1's center
        assert np.allclose(obj2.position, [100, 100])

    def test_align_to_returns_self(self) -> None:
        """Test align_to returns self for chaining."""
        obj1 = CObject()
        obj1._points = np.array([[-10, -10], [10, 10]], dtype=np.float64)

        obj2 = CObject()
        obj2._points = np.array([[-10, -10], [10, 10]], dtype=np.float64)

        result = obj2.align_to(obj1, edge="left")
        assert result is obj2


class TestCObjectBoundingBox:
    """Tests for CObject bounding box calculations."""

    def test_get_bounding_box_empty_points(self) -> None:
        """Test bounding box with no points returns position."""
        obj = CObject(position=(50, 75))
        bbox = obj.get_bounding_box()

        # With no points, should return position as both min and max
        assert np.allclose(bbox[0], [50, 75])
        assert np.allclose(bbox[1], [50, 75])

    def test_get_bounding_box_with_submobjects(self) -> None:
        """Test bounding box includes submobjects."""
        parent = CObject()
        parent._points = np.array([[0, 0], [50, 50]], dtype=np.float64)

        child = CObject()
        child._points = np.array([[60, 60], [100, 100]], dtype=np.float64)

        parent.add(child)
        bbox = parent.get_bounding_box()

        # Should encompass both parent and child
        assert bbox[0][0] == 0.0  # min x
        assert bbox[0][1] == 0.0  # min y
        assert bbox[1][0] == 100.0  # max x
        assert bbox[1][1] == 100.0  # max y

    def test_get_transformed_points_with_scale(self) -> None:
        """Test transformed points with scaling."""
        obj = CObject(position=(0, 0), scale=2.0)
        obj._points = np.array([[10, 10], [20, 20]], dtype=np.float64)

        transformed = obj._get_transformed_points()

        # Points should be scaled by 2
        assert np.allclose(transformed[0], [20, 20])
        assert np.allclose(transformed[1], [40, 40])

    def test_get_transformed_points_with_rotation(self) -> None:
        """Test transformed points with rotation."""
        import math
        obj = CObject(position=(0, 0), rotation=math.pi / 2)  # 90 degrees
        obj._points = np.array([[10, 0]], dtype=np.float64)

        transformed = obj._get_transformed_points()

        # Point at (10, 0) rotated 90 degrees should be at (0, 10)
        assert np.allclose(transformed[0], [0, 10], atol=1e-10)

    def test_get_transformed_points_with_position(self) -> None:
        """Test transformed points with position offset."""
        obj = CObject(position=(100, 200))
        obj._points = np.array([[0, 0], [10, 10]], dtype=np.float64)

        transformed = obj._get_transformed_points()

        assert np.allclose(transformed[0], [100, 200])
        assert np.allclose(transformed[1], [110, 210])

    def test_get_width_and_height(self) -> None:
        """Test get_width and get_height methods."""
        obj = CObject()
        obj._points = np.array([[0, 0], [100, 50]], dtype=np.float64)

        assert obj.get_width() == 100.0
        assert obj.get_height() == 50.0

    def test_get_center(self) -> None:
        """Test get_center method."""
        obj = CObject()
        obj._points = np.array([[0, 0], [100, 100]], dtype=np.float64)

        center = obj.get_center()
        assert np.allclose(center, [50, 50])


class TestCObjectRepr:
    """Tests for CObject string representation."""

    def test_repr(self) -> None:
        """Test __repr__ method."""
        obj = CObject(name="test_obj", position=(50, 100))
        repr_str = repr(obj)

        assert "CObject" in repr_str
        assert "test_obj" in repr_str
        assert "50" in repr_str
        assert "100" in repr_str
