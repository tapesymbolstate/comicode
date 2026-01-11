"""Tests for CObject base class."""

import numpy as np
import pytest

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
