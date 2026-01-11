"""Tests for CObject base class."""

import numpy as np
import pytest

from comix.cobject.cobject import CObject


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
