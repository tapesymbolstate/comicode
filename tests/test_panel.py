"""Tests for Panel class."""

import numpy as np
import pytest

from comix.cobject.panel.panel import Panel, Border
from comix.cobject.cobject import CObject


class TestBorder:
    """Tests for Border dataclass."""

    def test_default_border(self):
        """Test default border values."""
        border = Border()
        assert border.color == "#000000"
        assert border.width == 2.0
        assert border.style == "solid"
        assert border.radius == 0.0

    def test_custom_border(self):
        """Test custom border values."""
        border = Border(
            color="#FF0000",
            width=3.0,
            style="dashed",
            radius=10.0,
        )
        assert border.color == "#FF0000"
        assert border.width == 3.0
        assert border.style == "dashed"
        assert border.radius == 10.0


class TestPanel:
    """Tests for Panel class."""

    def test_default_init(self):
        """Test default initialization."""
        panel = Panel()
        assert panel.width == 300.0
        assert panel.height == 300.0
        assert panel.background_color == "#FFFFFF"
        assert panel.padding == 10.0
        assert isinstance(panel.border, Border)

    def test_custom_init(self):
        """Test custom initialization."""
        border = Border(color="#FF0000", width=3.0)
        panel = Panel(
            width=400.0,
            height=500.0,
            border=border,
            background_color="#EEEEEE",
            padding=20.0,
        )
        assert panel.width == 400.0
        assert panel.height == 500.0
        assert panel.background_color == "#EEEEEE"
        assert panel.padding == 20.0
        assert panel.border.color == "#FF0000"

    def test_generate_points(self):
        """Test that panel generates correct rectangle points."""
        panel = Panel(width=200, height=100)
        assert len(panel._points) == 5  # Rectangle with closing point

        half_w = 100
        half_h = 50
        expected_points = [
            [-half_w, -half_h],
            [half_w, -half_h],
            [half_w, half_h],
            [-half_w, half_h],
            [-half_w, -half_h],
        ]
        assert np.allclose(panel._points, expected_points)

    def test_add_content(self):
        """Test adding content to panel."""
        panel = Panel()
        obj1 = CObject(name="obj1")
        obj2 = CObject(name="obj2")

        result = panel.add_content(obj1, obj2)
        assert result is panel
        assert obj1 in panel._content
        assert obj2 in panel._content
        assert obj1 in panel.submobjects
        assert obj2 in panel.submobjects

    def test_set_background(self):
        """Test setting background."""
        panel = Panel()
        result = panel.set_background(color="#FF0000", image="bg.png")
        assert result is panel
        assert panel.background_color == "#FF0000"
        assert panel.background_image == "bg.png"

    def test_set_border(self):
        """Test setting border properties."""
        panel = Panel()
        panel.set_border(
            color="#0000FF",
            width=4.0,
            style="dashed",
            radius=15.0,
        )
        assert panel.border.color == "#0000FF"
        assert panel.border.width == 4.0
        assert panel.border.style == "dashed"
        assert panel.border.radius == 15.0

    def test_get_content_bounds(self):
        """Test get_content_bounds method."""
        panel = Panel(width=200, height=100, padding=10)
        bounds = panel.get_content_bounds()
        assert bounds == (-90, -40, 90, 40)

    def test_get_render_data(self):
        """Test get_render_data method."""
        panel = Panel(width=300, height=200)
        data = panel.get_render_data()

        assert data["type"] == "Panel"
        assert data["width"] == 300
        assert data["height"] == 200
        assert data["background_color"] == "#FFFFFF"
        assert "border" in data
        assert data["border"]["color"] == "#000000"
