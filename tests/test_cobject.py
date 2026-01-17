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
