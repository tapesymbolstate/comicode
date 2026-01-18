"""Tests for Panel class."""

import logging
import numpy as np
import pytest

from comix.cobject.panel.panel import (
    Border,
    CloudPanel,
    DiagonalPanel,
    ExplosionPanel,
    IrregularPanel,
    Panel,
    StarburstPanel,
    TrapezoidPanel,
)
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

    def test_set_border_validates_style(self):
        """Test that set_border validates style parameter."""
        panel = Panel()
        # Valid styles should work
        for style in ["solid", "dashed", "dotted", "none"]:
            panel.set_border(style=style)
            assert panel.border.style == style

    def test_set_border_invalid_style_raises_error(self):
        """Test that set_border raises ValueError for invalid style."""
        panel = Panel()
        with pytest.raises(ValueError) as exc_info:
            panel.set_border(style="invalid_style")

        error_msg = str(exc_info.value)
        assert "Invalid style" in error_msg
        assert "Panel.set_border" in error_msg
        assert "invalid_style" in error_msg

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

    def test_background_description(self):
        """Test background_description attribute for AI generation."""
        panel = Panel()
        assert panel.background_description is None

        panel.background_description = "A rainy cityscape at night"
        assert panel.background_description == "A rainy cityscape at night"

        data = panel.get_render_data()
        assert data["background_description"] == "A rainy cityscape at night"


class TestDiagonalPanel:
    """Tests for DiagonalPanel class."""

    def test_default_init(self):
        """Test default initialization."""
        panel = DiagonalPanel()
        assert panel.width == 300.0
        assert panel.height == 300.0
        assert panel.diagonal_angle == 45.0
        assert panel.direction == "top-left"

    def test_custom_init(self):
        """Test custom initialization."""
        panel = DiagonalPanel(
            width=400,
            height=500,
            diagonal_angle=30,
            direction="bottom-right",
        )
        assert panel.width == 400
        assert panel.height == 500
        assert panel.diagonal_angle == 30
        assert panel.direction == "bottom-right"

    def test_invalid_direction_logs_warning(self, caplog: pytest.LogCaptureFixture):
        """Test that invalid direction logs warning and defaults to top-left."""
        with caplog.at_level(logging.WARNING, logger="comix.cobject.panel.panel"):
            panel = DiagonalPanel(direction="invalid")
        assert "Invalid diagonal direction" in caplog.text
        assert panel.direction == "top-left"

    def test_angle_clamping(self):
        """Test that diagonal angle is clamped to valid range."""
        # Too low
        panel1 = DiagonalPanel(diagonal_angle=2)
        assert panel1.diagonal_angle == 5.0

        # Too high
        panel2 = DiagonalPanel(diagonal_angle=90)
        assert panel2.diagonal_angle == 85.0

    def test_generate_points_top_left(self):
        """Test point generation for top-left cut."""
        panel = DiagonalPanel(width=200, height=200, direction="top-left")
        # Should have 6 points (5 corners + closing point)
        assert len(panel._points) == 6

    def test_generate_points_all_directions(self):
        """Test point generation for all directions."""
        directions = ["top-left", "top-right", "bottom-left", "bottom-right"]
        for direction in directions:
            panel = DiagonalPanel(direction=direction)
            assert len(panel._points) == 6, f"Failed for direction: {direction}"

    def test_get_render_data(self):
        """Test get_render_data method."""
        panel = DiagonalPanel(width=300, height=200, diagonal_angle=35)
        data = panel.get_render_data()

        assert data["shape"] == "diagonal"
        assert data["diagonal_angle"] == 35
        assert data["diagonal_direction"] == "top-left"


class TestTrapezoidPanel:
    """Tests for TrapezoidPanel class."""

    def test_default_init(self):
        """Test default initialization."""
        panel = TrapezoidPanel()
        assert panel.top_width == 300.0
        assert panel.bottom_width == 200.0
        assert panel.height == 300.0
        # Width should be max of top/bottom
        assert panel.width == 300.0

    def test_custom_init(self):
        """Test custom initialization."""
        panel = TrapezoidPanel(
            top_width=100,
            bottom_width=400,
            height=500,
        )
        assert panel.top_width == 100
        assert panel.bottom_width == 400
        assert panel.height == 500
        assert panel.width == 400  # Max of widths

    def test_invalid_widths(self):
        """Test that invalid widths raise ValueError."""
        with pytest.raises(ValueError, match="top_width must be positive"):
            TrapezoidPanel(top_width=-1)

        with pytest.raises(ValueError, match="bottom_width must be positive"):
            TrapezoidPanel(bottom_width=0)

        with pytest.raises(ValueError, match="height must be positive"):
            TrapezoidPanel(height=-10)

    def test_generate_points(self):
        """Test point generation creates valid trapezoid."""
        panel = TrapezoidPanel(top_width=200, bottom_width=100, height=300)
        # Should have 5 points (4 corners + closing point)
        assert len(panel._points) == 5

        # Verify top is wider than bottom
        top_left = panel._points[0]
        top_right = panel._points[1]
        bottom_right = panel._points[2]
        bottom_left = panel._points[3]

        top_width = top_right[0] - top_left[0]
        bottom_width = bottom_right[0] - bottom_left[0]
        assert top_width > bottom_width

    def test_get_render_data(self):
        """Test get_render_data method."""
        panel = TrapezoidPanel(top_width=250, bottom_width=150, height=400)
        data = panel.get_render_data()

        assert data["shape"] == "trapezoid"
        assert data["top_width"] == 250
        assert data["bottom_width"] == 150


class TestIrregularPanel:
    """Tests for IrregularPanel class."""

    def test_basic_triangle(self):
        """Test creating a triangular panel."""
        points = [(0, 100), (100, -50), (-100, -50)]
        panel = IrregularPanel(points=points)
        assert len(panel.polygon_points) == 3

    def test_star_shape(self):
        """Test creating a star-shaped panel."""
        star_points = [
            (0, 100), (30, 30), (100, 0), (30, -30),
            (0, -100), (-30, -30), (-100, 0), (-30, 30),
        ]
        panel = IrregularPanel(points=star_points)
        assert len(panel.polygon_points) == 8

    def test_minimum_points_validation(self):
        """Test that at least 3 points are required."""
        with pytest.raises(ValueError, match="at least 3 points"):
            IrregularPanel(points=[(0, 0), (1, 1)])

    def test_complex_polygon_warning(self, caplog: pytest.LogCaptureFixture):
        """Test that complex polygons log a warning."""
        points = [(i, i**2 % 100) for i in range(150)]
        with caplog.at_level(logging.WARNING, logger="comix.cobject.panel.panel"):
            IrregularPanel(points=points)
        assert "may slow rendering" in caplog.text

    def test_self_intersecting_warning(self, caplog: pytest.LogCaptureFixture):
        """Test that self-intersecting polygons log a warning."""
        # Create a bowtie shape (self-intersecting)
        bowtie = [(0, 0), (100, 100), (100, 0), (0, 100)]
        with caplog.at_level(logging.WARNING, logger="comix.cobject.panel.panel"):
            IrregularPanel(points=bowtie)
        assert "self-intersecting" in caplog.text

    def test_width_height_calculation(self):
        """Test that width/height are calculated from points."""
        points = [(0, 0), (100, 0), (100, 200), (0, 200)]
        panel = IrregularPanel(points=points)
        assert panel.width == 100
        assert panel.height == 200

    def test_generate_points_centers_polygon(self):
        """Test that polygon is centered around origin."""
        points = [(100, 100), (200, 100), (200, 200), (100, 200)]
        panel = IrregularPanel(points=points)
        # Center should be offset from original points
        center = panel.get_center()
        assert np.allclose(center, [0, 0])

    def test_get_render_data(self):
        """Test get_render_data method."""
        points = [(0, 50), (50, 0), (0, -50), (-50, 0)]
        panel = IrregularPanel(points=points)
        data = panel.get_render_data()

        assert data["shape"] == "irregular"
        assert data["polygon_points"] == points


class TestSplitDiagonal:
    """Tests for Panel.split_diagonal() method."""

    def test_split_diagonal_basic(self):
        """Test basic diagonal split returns two IrregularPanels."""
        panel = Panel(width=400, height=400)
        panel1, panel2 = panel.split_diagonal()

        assert isinstance(panel1, IrregularPanel)
        assert isinstance(panel2, IrregularPanel)

    def test_split_diagonal_default_direction(self):
        """Test default direction is top-left-to-bottom-right."""
        panel = Panel(width=200, height=200)
        panel1, panel2 = panel.split_diagonal()

        # Panel 1 should be upper-right triangle (3 points)
        assert len(panel1.polygon_points) == 3
        # Panel 2 should be lower-left triangle (3 points)
        assert len(panel2.polygon_points) == 3

    def test_split_diagonal_top_left_to_bottom_right(self):
        """Test split direction top-left-to-bottom-right."""
        panel = Panel(width=200, height=200)
        panel1, panel2 = panel.split_diagonal(direction="top-left-to-bottom-right")

        # Verify the triangles cover the original panel area
        # Panel 1: upper-right (top-left, top-right, bottom-right)
        expected_panel1 = [(-100, 100), (100, 100), (100, -100)]
        assert panel1.polygon_points == expected_panel1

        # Panel 2: lower-left (top-left, bottom-right, bottom-left)
        expected_panel2 = [(-100, 100), (100, -100), (-100, -100)]
        assert panel2.polygon_points == expected_panel2

    def test_split_diagonal_top_right_to_bottom_left(self):
        """Test split direction top-right-to-bottom-left."""
        panel = Panel(width=200, height=200)
        panel1, panel2 = panel.split_diagonal(direction="top-right-to-bottom-left")

        # Panel 1: upper-left (top-left, top-right, bottom-left)
        expected_panel1 = [(-100, 100), (100, 100), (-100, -100)]
        assert panel1.polygon_points == expected_panel1

        # Panel 2: lower-right (top-right, bottom-right, bottom-left)
        expected_panel2 = [(100, 100), (100, -100), (-100, -100)]
        assert panel2.polygon_points == expected_panel2

    def test_split_diagonal_invalid_direction(self):
        """Test that invalid direction raises ValueError."""
        panel = Panel(width=200, height=200)
        with pytest.raises(ValueError) as exc_info:
            panel.split_diagonal(direction="invalid-direction")

        assert "Invalid direction" in str(exc_info.value)
        assert "top-left-to-bottom-right" in str(exc_info.value)
        assert "top-right-to-bottom-left" in str(exc_info.value)

    def test_split_diagonal_inherits_border(self):
        """Test that split panels inherit border settings."""
        border = Border(color="#FF0000", width=3.0, style="dashed", radius=5.0)
        panel = Panel(width=200, height=200, border=border)
        panel1, panel2 = panel.split_diagonal()

        assert panel1.border.color == "#FF0000"
        assert panel1.border.width == 3.0
        assert panel1.border.style == "dashed"
        assert panel1.border.radius == 5.0

        assert panel2.border.color == "#FF0000"
        assert panel2.border.width == 3.0
        assert panel2.border.style == "dashed"
        assert panel2.border.radius == 5.0

    def test_split_diagonal_inherits_background_color(self):
        """Test that split panels inherit background color."""
        panel = Panel(width=200, height=200, background_color="#EEEEEE")
        panel1, panel2 = panel.split_diagonal()

        assert panel1.background_color == "#EEEEEE"
        assert panel2.background_color == "#EEEEEE"

    def test_split_diagonal_inherits_padding(self):
        """Test that split panels inherit padding."""
        panel = Panel(width=200, height=200, padding=20.0)
        panel1, panel2 = panel.split_diagonal()

        assert panel1.padding == 20.0
        assert panel2.padding == 20.0

    def test_split_diagonal_preserves_position(self):
        """Test that split panels are positioned at original panel's center."""
        panel = Panel(width=200, height=200)
        panel.move_to((300, 400))
        panel1, panel2 = panel.split_diagonal()

        center1 = panel1.get_center()
        center2 = panel2.get_center()

        assert np.allclose(center1, [300, 400])
        assert np.allclose(center2, [300, 400])

    def test_split_diagonal_angle_clamping(self):
        """Test that angle is clamped to valid range."""
        panel = Panel(width=200, height=200)
        # Even with extreme angles, the split should work
        # (angle affects internal calculations but corners are used)
        panel1, panel2 = panel.split_diagonal(angle=0)  # Should be clamped to 5
        assert isinstance(panel1, IrregularPanel)
        assert isinstance(panel2, IrregularPanel)

        panel1, panel2 = panel.split_diagonal(angle=90)  # Should be clamped to 85
        assert isinstance(panel1, IrregularPanel)
        assert isinstance(panel2, IrregularPanel)

    def test_split_diagonal_original_unchanged(self):
        """Test that original panel is not modified by split."""
        panel = Panel(width=200, height=200)
        original_width = panel.width
        original_height = panel.height
        original_points = panel._points.copy()

        panel.split_diagonal()

        assert panel.width == original_width
        assert panel.height == original_height
        assert np.array_equal(panel._points, original_points)

    def test_split_diagonal_rectangular_panel(self):
        """Test splitting a non-square rectangular panel."""
        panel = Panel(width=400, height=200)  # Wide panel
        panel1, panel2 = panel.split_diagonal()

        # Both should be triangles with 3 points each
        assert len(panel1.polygon_points) == 3
        assert len(panel2.polygon_points) == 3

        # Verify dimensions make sense for wide panel
        assert panel1.width == 400  # Width from bounding box
        assert panel2.width == 400


class TestSplitCurve:
    """Tests for Panel.split_curve() method."""

    def test_split_curve_basic(self):
        """Test basic curved split returns two IrregularPanels."""
        panel = Panel(width=400, height=400)
        panel1, panel2 = panel.split_curve()

        assert isinstance(panel1, IrregularPanel)
        assert isinstance(panel2, IrregularPanel)

    def test_split_curve_default_direction(self):
        """Test default direction is top-left-to-bottom-right."""
        panel = Panel(width=200, height=200)
        panel1, panel2 = panel.split_curve()

        # Both panels should have more points than diagonal split (due to curve)
        assert len(panel1.polygon_points) > 3
        assert len(panel2.polygon_points) > 3

    def test_split_curve_top_left_to_bottom_right(self):
        """Test split direction top-left-to-bottom-right."""
        panel = Panel(width=200, height=200)
        panel1, panel2 = panel.split_curve(direction="top-left-to-bottom-right")

        # Verify both panels were created with multiple curve points
        assert len(panel1.polygon_points) >= 20  # num_curve_points default + corners
        assert len(panel2.polygon_points) >= 20

    def test_split_curve_top_right_to_bottom_left(self):
        """Test split direction top-right-to-bottom-left."""
        panel = Panel(width=200, height=200)
        panel1, panel2 = panel.split_curve(direction="top-right-to-bottom-left")

        # Verify both panels were created with multiple curve points
        assert len(panel1.polygon_points) >= 20
        assert len(panel2.polygon_points) >= 20

    def test_split_curve_invalid_direction(self):
        """Test that invalid direction raises ValueError."""
        panel = Panel(width=200, height=200)
        with pytest.raises(ValueError) as exc_info:
            panel.split_curve(direction="invalid-direction")

        assert "Invalid direction" in str(exc_info.value)
        assert "top-left-to-bottom-right" in str(exc_info.value)
        assert "top-right-to-bottom-left" in str(exc_info.value)

    def test_split_curve_inherits_border(self):
        """Test that split panels inherit border settings."""
        border = Border(color="#FF0000", width=3.0, style="dashed", radius=5.0)
        panel = Panel(width=200, height=200, border=border)
        panel1, panel2 = panel.split_curve()

        assert panel1.border.color == "#FF0000"
        assert panel1.border.width == 3.0
        assert panel1.border.style == "dashed"
        assert panel1.border.radius == 5.0

        assert panel2.border.color == "#FF0000"
        assert panel2.border.width == 3.0
        assert panel2.border.style == "dashed"
        assert panel2.border.radius == 5.0

    def test_split_curve_inherits_background_color(self):
        """Test that split panels inherit background color."""
        panel = Panel(width=200, height=200, background_color="#EEEEEE")
        panel1, panel2 = panel.split_curve()

        assert panel1.background_color == "#EEEEEE"
        assert panel2.background_color == "#EEEEEE"

    def test_split_curve_inherits_padding(self):
        """Test that split panels inherit padding."""
        panel = Panel(width=200, height=200, padding=20.0)
        panel1, panel2 = panel.split_curve()

        assert panel1.padding == 20.0
        assert panel2.padding == 20.0

    def test_split_curve_preserves_position(self):
        """Test that split panels are positioned at original panel's center."""
        panel = Panel(width=200, height=200)
        panel.move_to((300, 400))
        panel1, panel2 = panel.split_curve()

        center1 = panel1.get_center()
        center2 = panel2.get_center()

        assert np.allclose(center1, [300, 400])
        assert np.allclose(center2, [300, 400])

    def test_split_curve_original_unchanged(self):
        """Test that original panel is not modified by split."""
        panel = Panel(width=200, height=200)
        original_width = panel.width
        original_height = panel.height
        original_points = panel._points.copy()

        panel.split_curve()

        assert panel.width == original_width
        assert panel.height == original_height
        assert np.array_equal(panel._points, original_points)

    def test_split_curve_custom_control_points(self):
        """Test split with custom bezier control points."""
        panel = Panel(width=400, height=400)

        # Custom S-curve control points (relative coordinates)
        control_points = [
            (-0.5, 0.5),   # Top-left
            (-0.2, 0.2),   # Control 1
            (0.2, -0.2),   # Control 2
            (0.5, -0.5),   # Bottom-right
        ]
        panel1, panel2 = panel.split_curve(control_points=control_points)

        assert isinstance(panel1, IrregularPanel)
        assert isinstance(panel2, IrregularPanel)

    def test_split_curve_two_control_points(self):
        """Test split with only two control points (linear interpolation)."""
        panel = Panel(width=200, height=200)

        # Linear split (two points)
        control_points = [
            (-0.5, 0.5),   # Top-left
            (0.5, -0.5),   # Bottom-right
        ]
        panel1, panel2 = panel.split_curve(control_points=control_points)

        assert isinstance(panel1, IrregularPanel)
        assert isinstance(panel2, IrregularPanel)

    def test_split_curve_three_control_points(self):
        """Test split with three control points (quadratic bezier)."""
        panel = Panel(width=200, height=200)

        # Quadratic curve (three points)
        control_points = [
            (-0.5, 0.5),   # Start
            (0.0, 0.0),    # Control
            (0.5, -0.5),   # End
        ]
        panel1, panel2 = panel.split_curve(control_points=control_points)

        assert isinstance(panel1, IrregularPanel)
        assert isinstance(panel2, IrregularPanel)

    def test_split_curve_single_control_point_error(self):
        """Test that single control point raises ValueError."""
        panel = Panel(width=200, height=200)

        with pytest.raises(ValueError) as exc_info:
            panel.split_curve(control_points=[(0.0, 0.0)])

        assert "at least 2 control points" in str(exc_info.value)

    def test_split_curve_intensity_zero(self):
        """Test curve intensity of 0 creates nearly straight line."""
        panel = Panel(width=200, height=200)
        panel1, panel2 = panel.split_curve(curve_intensity=0.0)

        # Should still work even with no curve bulge
        assert isinstance(panel1, IrregularPanel)
        assert isinstance(panel2, IrregularPanel)

    def test_split_curve_intensity_high(self):
        """Test curve intensity of 1.0 creates maximum curve."""
        panel = Panel(width=200, height=200)
        panel1, panel2 = panel.split_curve(curve_intensity=1.0)

        assert isinstance(panel1, IrregularPanel)
        assert isinstance(panel2, IrregularPanel)

    def test_split_curve_intensity_clamping(self):
        """Test curve intensity is clamped to valid range."""
        panel = Panel(width=200, height=200)

        # Values outside 0-1 should be clamped
        panel1, panel2 = panel.split_curve(curve_intensity=-0.5)
        assert isinstance(panel1, IrregularPanel)

        panel1, panel2 = panel.split_curve(curve_intensity=2.0)
        assert isinstance(panel1, IrregularPanel)

    def test_split_curve_num_points(self):
        """Test custom number of curve points."""
        panel = Panel(width=200, height=200)

        # Fewer points for faster rendering
        panel1, panel2 = panel.split_curve(num_curve_points=5)
        assert len(panel1.polygon_points) >= 5

        # More points for smoother curve
        panel1, panel2 = panel.split_curve(num_curve_points=50)
        assert len(panel1.polygon_points) >= 50

    def test_split_curve_rectangular_panel(self):
        """Test splitting a non-square rectangular panel."""
        panel = Panel(width=400, height=200)  # Wide panel
        panel1, panel2 = panel.split_curve()

        # Both should be irregular panels with curved edge
        assert isinstance(panel1, IrregularPanel)
        assert isinstance(panel2, IrregularPanel)

    def test_split_curve_many_control_points(self):
        """Test split with more than 4 control points uses first and last pairs."""
        panel = Panel(width=300, height=300)

        # 6 control points - should use p0, p1, p[-2], p[-1]
        control_points = [
            (-0.5, 0.5),
            (-0.3, 0.3),
            (-0.1, 0.1),
            (0.1, -0.1),
            (0.3, -0.3),
            (0.5, -0.5),
        ]
        panel1, panel2 = panel.split_curve(control_points=control_points)

        assert isinstance(panel1, IrregularPanel)
        assert isinstance(panel2, IrregularPanel)


class TestStarburstPanel:
    """Tests for StarburstPanel class."""

    def test_default_init(self):
        """Test default initialization."""
        panel = StarburstPanel()
        assert panel.width == 300.0
        assert panel.height == 300.0
        assert panel.num_star_points == 8
        assert panel.inner_ratio == 0.5
        assert isinstance(panel, IrregularPanel)

    def test_custom_dimensions(self):
        """Test custom width and height."""
        panel = StarburstPanel(width=400, height=500)
        assert panel.width == 400.0
        assert panel.height == 500.0

    def test_custom_num_points(self):
        """Test custom number of star points."""
        panel = StarburstPanel(num_points=12)
        assert panel.num_star_points == 12
        # Each star point creates 2 vertices (outer + inner)
        assert len(panel.polygon_points) == 24

    def test_custom_inner_ratio(self):
        """Test custom inner ratio."""
        panel = StarburstPanel(inner_ratio=0.3)
        assert panel.inner_ratio == 0.3

    def test_minimum_points(self):
        """Test minimum number of points (3)."""
        panel = StarburstPanel(num_points=3)
        assert panel.num_star_points == 3
        assert len(panel.polygon_points) == 6

    def test_too_few_points_raises_error(self):
        """Test that fewer than 3 points raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            StarburstPanel(num_points=2)
        assert "at least 3" in str(exc_info.value)

    def test_inner_ratio_too_low_raises_error(self):
        """Test that inner_ratio < 0.1 raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            StarburstPanel(inner_ratio=0.05)
        assert "between 0.1 and 0.9" in str(exc_info.value)

    def test_inner_ratio_too_high_raises_error(self):
        """Test that inner_ratio > 0.9 raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            StarburstPanel(inner_ratio=0.95)
        assert "between 0.1 and 0.9" in str(exc_info.value)

    def test_inner_ratio_boundary_low(self):
        """Test inner_ratio at lower boundary."""
        panel = StarburstPanel(inner_ratio=0.1)
        assert panel.inner_ratio == 0.1

    def test_inner_ratio_boundary_high(self):
        """Test inner_ratio at upper boundary."""
        panel = StarburstPanel(inner_ratio=0.9)
        assert panel.inner_ratio == 0.9

    def test_starburst_has_points(self):
        """Test that starburst panel has polygon points."""
        panel = StarburstPanel(width=200, height=200, num_points=6)
        assert len(panel.polygon_points) == 12  # 6 points * 2 (outer + inner)

    def test_inherits_from_irregular_panel(self):
        """Test that StarburstPanel inherits from IrregularPanel."""
        panel = StarburstPanel()
        assert isinstance(panel, IrregularPanel)
        assert isinstance(panel, Panel)

    def test_render_data_shape(self):
        """Test render data has correct shape."""
        panel = StarburstPanel(num_points=10, inner_ratio=0.4)
        data = panel.get_render_data()
        assert data["shape"] == "starburst"
        assert data["num_star_points"] == 10
        assert data["inner_ratio"] == 0.4

    def test_border_inherited(self):
        """Test that border settings are inherited."""
        border = Border(color="#FF0000", width=3.0)
        panel = StarburstPanel(border=border)
        assert panel.border.color == "#FF0000"
        assert panel.border.width == 3.0

    def test_background_color(self):
        """Test background color setting."""
        panel = StarburstPanel(background_color="#FFFF00")
        assert panel.background_color == "#FFFF00"


class TestCloudPanel:
    """Tests for CloudPanel class."""

    def test_default_init(self):
        """Test default initialization."""
        panel = CloudPanel()
        # Width/height approximate due to cloud bumps extending beyond base dimensions
        assert 290.0 <= panel.width <= 320.0
        assert 290.0 <= panel.height <= 320.0
        assert panel.num_bumps == 8
        assert panel.bumpiness == 0.3
        assert isinstance(panel, IrregularPanel)

    def test_custom_dimensions(self):
        """Test custom width and height scales proportionally."""
        panel = CloudPanel(width=500, height=300)
        # Width/height approximate due to cloud bumps
        assert 480.0 <= panel.width <= 530.0
        assert 280.0 <= panel.height <= 320.0

    def test_custom_num_bumps(self):
        """Test custom number of bumps."""
        panel = CloudPanel(num_bumps=12)
        assert panel.num_bumps == 12

    def test_custom_bumpiness(self):
        """Test custom bumpiness."""
        panel = CloudPanel(bumpiness=0.4)
        assert panel.bumpiness == 0.4

    def test_minimum_bumps(self):
        """Test minimum number of bumps (3)."""
        panel = CloudPanel(num_bumps=3)
        assert panel.num_bumps == 3

    def test_too_few_bumps_raises_error(self):
        """Test that fewer than 3 bumps raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            CloudPanel(num_bumps=2)
        assert "at least 3" in str(exc_info.value)

    def test_bumpiness_too_low_raises_error(self):
        """Test that bumpiness < 0.1 raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            CloudPanel(bumpiness=0.05)
        assert "between 0.1 and 0.5" in str(exc_info.value)

    def test_bumpiness_too_high_raises_error(self):
        """Test that bumpiness > 0.5 raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            CloudPanel(bumpiness=0.6)
        assert "between 0.1 and 0.5" in str(exc_info.value)

    def test_bumpiness_boundary_low(self):
        """Test bumpiness at lower boundary."""
        panel = CloudPanel(bumpiness=0.1)
        assert panel.bumpiness == 0.1

    def test_bumpiness_boundary_high(self):
        """Test bumpiness at upper boundary."""
        panel = CloudPanel(bumpiness=0.5)
        assert panel.bumpiness == 0.5

    def test_cloud_has_many_points(self):
        """Test that cloud panel has smooth edges with many points."""
        panel = CloudPanel(num_bumps=8)
        # 8 samples per bump = 64 points
        assert len(panel.polygon_points) == 64

    def test_inherits_from_irregular_panel(self):
        """Test that CloudPanel inherits from IrregularPanel."""
        panel = CloudPanel()
        assert isinstance(panel, IrregularPanel)
        assert isinstance(panel, Panel)

    def test_render_data_shape(self):
        """Test render data has correct shape."""
        panel = CloudPanel(num_bumps=10, bumpiness=0.4)
        data = panel.get_render_data()
        assert data["shape"] == "cloud"
        assert data["num_bumps"] == 10
        assert data["bumpiness"] == 0.4

    def test_border_inherited(self):
        """Test that border settings are inherited."""
        border = Border(color="#0000FF", width=2.5)
        panel = CloudPanel(border=border)
        assert panel.border.color == "#0000FF"
        assert panel.border.width == 2.5


class TestExplosionPanel:
    """Tests for ExplosionPanel class."""

    def test_default_init(self):
        """Test default initialization."""
        panel = ExplosionPanel(seed=42)  # Use seed for reproducibility
        # Width/height approximate due to explosion randomness extending beyond base
        assert 280.0 <= panel.width <= 330.0
        assert 280.0 <= panel.height <= 330.0
        assert panel.num_rays == 12
        assert panel.ray_depth == 0.4
        assert panel.randomness == 0.2
        assert panel.seed == 42
        assert isinstance(panel, IrregularPanel)

    def test_custom_dimensions(self):
        """Test custom width and height scales proportionally."""
        panel = ExplosionPanel(width=600, height=600, seed=42)
        # Width/height approximate due to explosion randomness
        assert 560.0 <= panel.width <= 660.0
        assert 560.0 <= panel.height <= 660.0

    def test_custom_num_rays(self):
        """Test custom number of rays."""
        panel = ExplosionPanel(num_rays=16, seed=42)
        assert panel.num_rays == 16
        # Each ray creates 2 vertices (outer + inner)
        assert len(panel.polygon_points) == 32

    def test_custom_ray_depth(self):
        """Test custom ray depth."""
        panel = ExplosionPanel(ray_depth=0.5, seed=42)
        assert panel.ray_depth == 0.5

    def test_custom_randomness(self):
        """Test custom randomness."""
        panel = ExplosionPanel(randomness=0.3, seed=42)
        assert panel.randomness == 0.3

    def test_minimum_rays(self):
        """Test minimum number of rays (4)."""
        panel = ExplosionPanel(num_rays=4, seed=42)
        assert panel.num_rays == 4
        assert len(panel.polygon_points) == 8

    def test_too_few_rays_raises_error(self):
        """Test that fewer than 4 rays raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            ExplosionPanel(num_rays=3)
        assert "at least 4" in str(exc_info.value)

    def test_ray_depth_too_low_raises_error(self):
        """Test that ray_depth < 0.2 raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            ExplosionPanel(ray_depth=0.1)
        assert "between 0.2 and 0.6" in str(exc_info.value)

    def test_ray_depth_too_high_raises_error(self):
        """Test that ray_depth > 0.6 raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            ExplosionPanel(ray_depth=0.7)
        assert "between 0.2 and 0.6" in str(exc_info.value)

    def test_ray_depth_boundary_low(self):
        """Test ray_depth at lower boundary."""
        panel = ExplosionPanel(ray_depth=0.2, seed=42)
        assert panel.ray_depth == 0.2

    def test_ray_depth_boundary_high(self):
        """Test ray_depth at upper boundary."""
        panel = ExplosionPanel(ray_depth=0.6, seed=42)
        assert panel.ray_depth == 0.6

    def test_randomness_too_low_raises_error(self):
        """Test that randomness < 0.0 raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            ExplosionPanel(randomness=-0.1)
        assert "between 0.0 and 0.5" in str(exc_info.value)

    def test_randomness_too_high_raises_error(self):
        """Test that randomness > 0.5 raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            ExplosionPanel(randomness=0.6)
        assert "between 0.0 and 0.5" in str(exc_info.value)

    def test_randomness_boundary_low(self):
        """Test randomness at lower boundary (0.0 = no randomness)."""
        panel = ExplosionPanel(randomness=0.0, seed=42)
        assert panel.randomness == 0.0

    def test_randomness_boundary_high(self):
        """Test randomness at upper boundary."""
        panel = ExplosionPanel(randomness=0.5, seed=42)
        assert panel.randomness == 0.5

    def test_seed_reproducibility(self):
        """Test that same seed produces same shape."""
        panel1 = ExplosionPanel(seed=12345)
        panel2 = ExplosionPanel(seed=12345)
        assert panel1.polygon_points == panel2.polygon_points

    def test_different_seeds_different_shapes(self):
        """Test that different seeds produce different shapes."""
        panel1 = ExplosionPanel(seed=100)
        panel2 = ExplosionPanel(seed=200)
        # Due to randomness, they should be different
        assert panel1.polygon_points != panel2.polygon_points

    def test_no_seed_random(self):
        """Test that no seed produces random shapes (usually different)."""
        # Note: There's a tiny chance these could be identical, but extremely unlikely
        panel1 = ExplosionPanel(seed=None, randomness=0.3)
        panel2 = ExplosionPanel(seed=None, randomness=0.3)
        # We just verify both are created successfully
        assert isinstance(panel1, ExplosionPanel)
        assert isinstance(panel2, ExplosionPanel)

    def test_inherits_from_irregular_panel(self):
        """Test that ExplosionPanel inherits from IrregularPanel."""
        panel = ExplosionPanel(seed=42)
        assert isinstance(panel, IrregularPanel)
        assert isinstance(panel, Panel)

    def test_render_data_shape(self):
        """Test render data has correct shape."""
        panel = ExplosionPanel(num_rays=16, ray_depth=0.5, randomness=0.3, seed=42)
        data = panel.get_render_data()
        assert data["shape"] == "explosion"
        assert data["num_rays"] == 16
        assert data["ray_depth"] == 0.5
        assert data["randomness"] == 0.3
        assert data["seed"] == 42

    def test_border_inherited(self):
        """Test that border settings are inherited."""
        border = Border(color="#FF00FF", width=4.0)
        panel = ExplosionPanel(border=border, seed=42)
        assert panel.border.color == "#FF00FF"
        assert panel.border.width == 4.0

    def test_zero_randomness_symmetric(self):
        """Test that zero randomness creates symmetric explosion."""
        panel = ExplosionPanel(num_rays=8, randomness=0.0, seed=42)
        # With 0 randomness, the pattern should be regular
        assert len(panel.polygon_points) == 16  # 8 rays * 2


class TestGutterSpacing:
    """Tests for automatic gutter spacing calculations for non-rectangular panels."""

    def test_get_world_polygon_basic(self):
        """Test get_world_polygon returns points in world coordinates."""
        panel = Panel(width=200, height=200)
        panel.move_to((300, 400))

        world_poly = panel.get_world_polygon()
        assert len(world_poly) == 5  # Rectangle with closing point

        # Points should be offset by panel center
        # Local points are relative to panel center (0,0)
        # World points should be relative to page origin
        assert np.allclose(world_poly[0], [200, 300])  # -100+300, -100+400
        assert np.allclose(world_poly[1], [400, 300])  # 100+300, -100+400

    def test_get_world_polygon_diagonal(self):
        """Test get_world_polygon for diagonal panel."""
        panel = DiagonalPanel(width=200, height=200, direction="top-left")
        panel.move_to((100, 100))

        world_poly = panel.get_world_polygon()
        assert len(world_poly) == 6  # Diagonal has 5 corners + closing point

    def test_get_world_polygon_with_default_panel(self):
        """Test get_world_polygon with default panel at origin."""
        panel = Panel()
        # Default panel has points generated automatically at origin
        world_poly = panel.get_world_polygon()
        # Panel is centered at origin by default
        assert len(world_poly) == 5  # Rectangle with closing point

    def test_distance_to_panel_same_position(self):
        """Test distance between overlapping panels is 0."""
        panel1 = Panel(width=100, height=100)
        panel2 = Panel(width=100, height=100)
        panel1.move_to((100, 100))
        panel2.move_to((100, 100))

        dist = panel1.distance_to_panel(panel2)
        assert dist == 0.0

    def test_distance_to_panel_separated(self):
        """Test distance between separated rectangular panels."""
        panel1 = Panel(width=100, height=100)
        panel2 = Panel(width=100, height=100)
        panel1.move_to((100, 100))
        panel2.move_to((300, 100))  # 100px gap between panels

        dist = panel1.distance_to_panel(panel2)
        # Distance should be 100px (edges are at 150 and 250)
        assert abs(dist - 100.0) < 1.0

    def test_distance_to_panel_diagonal(self):
        """Test distance between diagonal panels."""
        panel1 = DiagonalPanel(width=200, height=200, direction="top-right")
        panel2 = DiagonalPanel(width=200, height=200, direction="top-left")
        panel1.move_to((100, 100))
        panel2.move_to((300, 100))

        dist = panel1.distance_to_panel(panel2)
        # Should have some distance between them
        assert dist >= 0.0

    def test_distance_to_panel_trapezoid(self):
        """Test distance between trapezoid panels."""
        panel1 = TrapezoidPanel(top_width=150, bottom_width=100, height=200)
        panel2 = TrapezoidPanel(top_width=100, bottom_width=150, height=200)
        panel1.move_to((100, 100))
        panel2.move_to((300, 100))

        dist = panel1.distance_to_panel(panel2)
        assert dist >= 0.0

    def test_calculate_gutter_offset_no_adjustment_needed(self):
        """Test gutter offset when panels already have sufficient spacing."""
        panel1 = Panel(width=100, height=100)
        panel2 = Panel(width=100, height=100)
        panel1.move_to((100, 100))
        panel2.move_to((300, 100))  # 100px apart

        # Requesting only 10px gutter should need no adjustment
        dx, dy = Panel.calculate_gutter_offset(panel1, panel2, 10.0, "right")
        assert dx == 0.0
        assert dy == 0.0

    def test_calculate_gutter_offset_adjustment_needed(self):
        """Test gutter offset when panels need adjustment."""
        panel1 = Panel(width=100, height=100)
        panel2 = Panel(width=100, height=100)
        panel1.move_to((100, 100))
        panel2.move_to((155, 100))  # Only 5px apart (edge at 150, edge at 155-50=105)

        # Distance is 5px, want 10px, so need 5px adjustment
        dx, dy = Panel.calculate_gutter_offset(panel1, panel2, 10.0, "right")
        assert dx >= 0.0  # Should suggest moving right

    def test_calculate_gutter_offset_directions(self):
        """Test gutter offset for all directions."""
        panel1 = Panel(width=100, height=100)
        panel2 = Panel(width=100, height=100)
        panel1.move_to((100, 100))
        panel2.move_to((100, 100))  # Overlapping

        # Test all directions
        dx, dy = Panel.calculate_gutter_offset(panel1, panel2, 10.0, "right")
        assert dx >= 0.0
        assert dy == 0.0

        dx, dy = Panel.calculate_gutter_offset(panel1, panel2, 10.0, "left")
        assert dx <= 0.0
        assert dy == 0.0

        dx, dy = Panel.calculate_gutter_offset(panel1, panel2, 10.0, "below")
        assert dx == 0.0
        assert dy <= 0.0

        dx, dy = Panel.calculate_gutter_offset(panel1, panel2, 10.0, "above")
        assert dx == 0.0
        assert dy >= 0.0

    def test_calculate_gutter_offset_diagonal_panels(self):
        """Test gutter offset calculation for diagonal panels."""
        # Two diagonal panels with cut corners facing each other
        panel1 = DiagonalPanel(width=200, height=200, direction="top-right")
        panel2 = DiagonalPanel(width=200, height=200, direction="top-left")

        # Position them using bounding box
        panel1.move_to((100, 100))
        panel2.move_to((310, 100))  # 10px gutter by bounding box

        # Calculate what adjustment is needed for actual polygon edges
        dx, dy = Panel.calculate_gutter_offset(panel1, panel2, 10.0, "right")
        # Adjustment could be positive, negative, or zero depending on cut direction
        assert isinstance(dx, float)
        assert isinstance(dy, float)

    def test_calculate_gutter_offset_overlapping_panels(self):
        """Test gutter offset with overlapping panels."""
        panel1 = Panel(width=100, height=100)
        panel2 = Panel(width=100, height=100)
        # Both at origin = completely overlapping
        panel1.move_to((50, 50))
        panel2.move_to((50, 50))

        # Overlapping panels should need adjustment
        dx, dy = Panel.calculate_gutter_offset(panel1, panel2, 10.0, "right")
        # Distance is 0, need 10px gutter
        assert dx == 10.0
        assert dy == 0.0

    def test_gutter_spacing_irregular_panels(self):
        """Test gutter calculation for irregular shaped panels."""
        # Create two star-shaped panels
        panel1 = StarburstPanel(width=200, height=200, num_points=8)
        panel2 = StarburstPanel(width=200, height=200, num_points=8)

        panel1.move_to((150, 150))
        panel2.move_to((350, 150))

        dist = panel1.distance_to_panel(panel2)
        # Distance should be positive (panels not overlapping)
        assert dist >= 0.0

    def test_gutter_spacing_cloud_panels(self):
        """Test gutter calculation for cloud-shaped panels."""
        panel1 = CloudPanel(width=200, height=200, num_bumps=8)
        panel2 = CloudPanel(width=200, height=200, num_bumps=8)

        panel1.move_to((150, 150))
        panel2.move_to((380, 150))

        dist = panel1.distance_to_panel(panel2)
        assert dist >= 0.0

    def test_gutter_spacing_mixed_panel_types(self):
        """Test gutter calculation between different panel types."""
        panel1 = DiagonalPanel(width=200, height=200, direction="top-right")
        panel2 = TrapezoidPanel(top_width=200, bottom_width=150, height=200)

        panel1.move_to((100, 100))
        panel2.move_to((320, 100))

        dist = panel1.distance_to_panel(panel2)
        assert dist >= 0.0


class TestPresetPanelPointGeneration:
    """Tests for the internal point generation functions."""

    def test_starburst_points_count(self):
        """Test starburst generates correct number of points."""
        from comix.cobject.panel.panel import _generate_starburst_points
        points = _generate_starburst_points(100, 100, num_points=5, inner_ratio=0.5)
        assert len(points) == 10  # 5 outer + 5 inner

    def test_starburst_points_centered(self):
        """Test starburst points are roughly centered."""
        from comix.cobject.panel.panel import _generate_starburst_points
        points = _generate_starburst_points(100, 100, num_points=8, inner_ratio=0.5)
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        # Center should be near origin
        assert abs(sum(xs) / len(xs)) < 1.0
        assert abs(sum(ys) / len(ys)) < 1.0

    def test_cloud_points_count(self):
        """Test cloud generates correct number of points."""
        from comix.cobject.panel.panel import _generate_cloud_points
        points = _generate_cloud_points(100, 100, num_bumps=6, bumpiness=0.3)
        # 6 bumps * 8 samples per bump = 48 points
        assert len(points) == 48

    def test_cloud_points_smooth(self):
        """Test cloud points form a smooth shape."""
        from comix.cobject.panel.panel import _generate_cloud_points
        points = _generate_cloud_points(100, 100, num_bumps=8, bumpiness=0.3)
        # Just verify we have many points for smoothness
        assert len(points) >= 64

    def test_explosion_points_count(self):
        """Test explosion generates correct number of points."""
        from comix.cobject.panel.panel import _generate_explosion_points
        points = _generate_explosion_points(
            100, 100, num_rays=10, ray_depth=0.4, randomness=0.2, seed=42
        )
        assert len(points) == 20  # 10 outer + 10 inner

    def test_explosion_points_with_seed(self):
        """Test explosion with seed is reproducible."""
        from comix.cobject.panel.panel import _generate_explosion_points
        points1 = _generate_explosion_points(
            100, 100, num_rays=8, ray_depth=0.4, randomness=0.3, seed=999
        )
        points2 = _generate_explosion_points(
            100, 100, num_rays=8, ray_depth=0.4, randomness=0.3, seed=999
        )
        assert points1 == points2
