"""Tests for Rectangle, Circle, and Line shape classes."""

import numpy as np

from comix.cobject.shapes.shapes import Rectangle, Circle, Line


class TestRectangle:
    """Tests for Rectangle class."""

    def test_default_init(self):
        """Test default initialization."""
        rect = Rectangle()
        assert rect.rect_width == 100.0
        assert rect.rect_height == 100.0
        assert rect.fill_color == "#FFFFFF"
        assert rect.stroke_color == "#000000"
        assert rect.stroke_width == 2.0
        assert rect.corner_radius == 0.0

    def test_custom_dimensions(self):
        """Test initialization with custom dimensions."""
        rect = Rectangle(width=200.0, height=150.0)
        assert rect.rect_width == 200.0
        assert rect.rect_height == 150.0

    def test_custom_colors(self):
        """Test initialization with custom colors."""
        rect = Rectangle(
            fill_color="#FF0000",
            stroke_color="#0000FF",
            stroke_width=5.0,
        )
        assert rect.fill_color == "#FF0000"
        assert rect.stroke_color == "#0000FF"
        assert rect.stroke_width == 5.0

    def test_corner_radius(self):
        """Test initialization with corner radius."""
        rect = Rectangle(corner_radius=10.0)
        assert rect.corner_radius == 10.0

    def test_generate_points(self):
        """Test that points are generated correctly."""
        rect = Rectangle(width=100.0, height=80.0)
        points = rect._points

        # Should have 5 points (closed rectangle)
        assert len(points) == 5

        # Points should be centered at origin
        half_w = 50.0
        half_h = 40.0

        assert np.allclose(points[0], [-half_w, -half_h])
        assert np.allclose(points[1], [half_w, -half_h])
        assert np.allclose(points[2], [half_w, half_h])
        assert np.allclose(points[3], [-half_w, half_h])
        assert np.allclose(points[4], [-half_w, -half_h])  # Closed path

    def test_set_size(self):
        """Test set_size method."""
        rect = Rectangle(width=100.0, height=100.0)
        result = rect.set_size(200.0, 150.0)

        assert result is rect  # Method chaining
        assert rect.rect_width == 200.0
        assert rect.rect_height == 150.0

        # Points should be regenerated
        half_w = 100.0
        half_h = 75.0
        assert np.allclose(rect._points[0], [-half_w, -half_h])
        assert np.allclose(rect._points[2], [half_w, half_h])

    def test_get_render_data(self):
        """Test get_render_data method."""
        rect = Rectangle(
            width=150.0,
            height=100.0,
            fill_color="#EEEEEE",
            stroke_color="#333333",
            stroke_width=3.0,
            corner_radius=8.0,
        )
        data = rect.get_render_data()

        assert data["rect_width"] == 150.0
        assert data["rect_height"] == 100.0
        assert data["fill_color"] == "#EEEEEE"
        assert data["stroke_color"] == "#333333"
        assert data["stroke_width"] == 3.0
        assert data["corner_radius"] == 8.0
        assert "points" in data

    def test_bounding_box(self):
        """Test bounding box calculation."""
        rect = Rectangle(width=100.0, height=60.0)
        bbox = rect.get_bounding_box()

        assert bbox[0][0] == -50.0  # min_x
        assert bbox[0][1] == -30.0  # min_y
        assert bbox[1][0] == 50.0   # max_x
        assert bbox[1][1] == 30.0   # max_y

    def test_move_to(self):
        """Test that rectangle can be positioned."""
        rect = Rectangle(width=100.0, height=100.0)
        rect.move_to((200, 150))

        center = rect.get_center()
        assert np.allclose(center, [200, 150])


class TestCircle:
    """Tests for Circle class."""

    def test_default_init(self):
        """Test default initialization."""
        circle = Circle()
        assert circle.radius == 50.0
        assert circle.fill_color == "#FFFFFF"
        assert circle.stroke_color == "#000000"
        assert circle.stroke_width == 2.0
        assert circle.num_points == 32

    def test_custom_radius(self):
        """Test initialization with custom radius."""
        circle = Circle(radius=100.0)
        assert circle.radius == 100.0

    def test_custom_colors(self):
        """Test initialization with custom colors."""
        circle = Circle(
            fill_color="#00FF00",
            stroke_color="#FF0000",
            stroke_width=4.0,
        )
        assert circle.fill_color == "#00FF00"
        assert circle.stroke_color == "#FF0000"
        assert circle.stroke_width == 4.0

    def test_custom_num_points(self):
        """Test initialization with custom number of points."""
        circle = Circle(num_points=64)
        assert circle.num_points == 64
        assert len(circle._points) == 64

    def test_generate_points(self):
        """Test that points form a circle."""
        circle = Circle(radius=50.0, num_points=4)
        points = circle._points

        # Should have 4 points
        assert len(points) == 4

        # All points should be at distance radius from origin
        for point in points:
            distance = np.sqrt(point[0] ** 2 + point[1] ** 2)
            assert np.isclose(distance, 50.0)

    def test_generate_points_positions(self):
        """Test specific point positions for 4-point circle."""
        circle = Circle(radius=50.0, num_points=4)
        points = circle._points

        # First point should be at (50, 0)
        assert np.allclose(points[0], [50.0, 0.0])
        # Second point should be at (0, 50)
        assert np.allclose(points[1], [0.0, 50.0], atol=1e-10)
        # Third point should be at (-50, 0)
        assert np.allclose(points[2], [-50.0, 0.0], atol=1e-10)
        # Fourth point should be at (0, -50)
        assert np.allclose(points[3], [0.0, -50.0], atol=1e-10)

    def test_set_radius(self):
        """Test set_radius method."""
        circle = Circle(radius=50.0)
        result = circle.set_radius(100.0)

        assert result is circle  # Method chaining
        assert circle.radius == 100.0

        # Points should be regenerated
        for point in circle._points:
            distance = np.sqrt(point[0] ** 2 + point[1] ** 2)
            assert np.isclose(distance, 100.0)

    def test_get_render_data(self):
        """Test get_render_data method."""
        circle = Circle(
            radius=75.0,
            fill_color="#CCCCCC",
            stroke_color="#666666",
            stroke_width=2.5,
        )
        data = circle.get_render_data()

        assert data["radius"] == 75.0
        assert data["fill_color"] == "#CCCCCC"
        assert data["stroke_color"] == "#666666"
        assert data["stroke_width"] == 2.5
        assert "points" in data

    def test_bounding_box(self):
        """Test bounding box calculation."""
        circle = Circle(radius=50.0)
        bbox = circle.get_bounding_box()

        # Bounding box should encompass the circle
        assert bbox[0][0] <= -50.0  # min_x
        assert bbox[0][1] <= -50.0  # min_y
        assert bbox[1][0] >= 50.0   # max_x
        assert bbox[1][1] >= 50.0   # max_y

    def test_move_to(self):
        """Test that circle can be positioned."""
        circle = Circle(radius=50.0)
        circle.move_to((100, 100))

        center = circle.get_center()
        assert np.allclose(center, [100, 100])


class TestLine:
    """Tests for Line class."""

    def test_default_init(self):
        """Test default initialization."""
        line = Line()
        assert np.allclose(line.start_point, [0, 0])
        assert np.allclose(line.end_point, [100, 0])
        assert line.stroke_color == "#000000"
        assert line.stroke_width == 2.0
        assert line.stroke_style == "solid"

    def test_custom_endpoints(self):
        """Test initialization with custom endpoints."""
        line = Line(start=(10, 20), end=(150, 200))
        assert np.allclose(line.start_point, [10, 20])
        assert np.allclose(line.end_point, [150, 200])

    def test_custom_stroke(self):
        """Test initialization with custom stroke properties."""
        line = Line(
            stroke_color="#FF0000",
            stroke_width=5.0,
            stroke_style="dashed",
        )
        assert line.stroke_color == "#FF0000"
        assert line.stroke_width == 5.0
        assert line.stroke_style == "dashed"

    def test_generate_points(self):
        """Test that points are the start and end."""
        line = Line(start=(50, 100), end=(200, 300))
        points = line._points

        assert len(points) == 2
        assert np.allclose(points[0], [50, 100])
        assert np.allclose(points[1], [200, 300])

    def test_set_points(self):
        """Test set_points method."""
        line = Line()
        result = line.set_points((25, 50), (175, 250))

        assert result is line  # Method chaining
        assert np.allclose(line.start_point, [25, 50])
        assert np.allclose(line.end_point, [175, 250])
        assert np.allclose(line._points[0], [25, 50])
        assert np.allclose(line._points[1], [175, 250])

    def test_get_render_data(self):
        """Test get_render_data method."""
        line = Line(
            start=(10, 20),
            end=(100, 80),
            stroke_color="#00FF00",
            stroke_width=3.0,
            stroke_style="dotted",
        )
        data = line.get_render_data()

        assert data["start"] == [10.0, 20.0]
        assert data["end"] == [100.0, 80.0]
        assert data["stroke_color"] == "#00FF00"
        assert data["stroke_width"] == 3.0
        assert data["stroke_style"] == "dotted"
        assert "points" in data

    def test_bounding_box(self):
        """Test bounding box calculation."""
        line = Line(start=(10, 20), end=(100, 80))
        bbox = line.get_bounding_box()

        assert bbox[0][0] == 10.0   # min_x
        assert bbox[0][1] == 20.0   # min_y
        assert bbox[1][0] == 100.0  # max_x
        assert bbox[1][1] == 80.0   # max_y

    def test_bounding_box_reversed(self):
        """Test bounding box with reversed endpoints."""
        line = Line(start=(100, 80), end=(10, 20))
        bbox = line.get_bounding_box()

        assert bbox[0][0] == 10.0   # min_x
        assert bbox[0][1] == 20.0   # min_y
        assert bbox[1][0] == 100.0  # max_x
        assert bbox[1][1] == 80.0   # max_y

    def test_move_to(self):
        """Test that line can be positioned.

        Note: Line points are not centered at origin like Rectangle/Circle.
        A line from (0,0) to (100,0) has its local center at (50,0).
        move_to sets position offset, so the global center becomes position + local center.
        """
        line = Line(start=(0, 0), end=(100, 0))
        line.move_to((100, 50))

        # Line's local center is at (50, 0), so global center is (100+50, 50+0) = (150, 50)
        center = line.get_center()
        assert np.allclose(center, [150, 50])

    def test_diagonal_line(self):
        """Test diagonal line generation."""
        line = Line(start=(0, 0), end=(100, 100))
        points = line._points

        assert len(points) == 2
        assert np.allclose(points[0], [0, 0])
        assert np.allclose(points[1], [100, 100])

    def test_vertical_line(self):
        """Test vertical line generation."""
        line = Line(start=(50, 0), end=(50, 200))
        points = line._points

        assert len(points) == 2
        assert np.allclose(points[0], [50, 0])
        assert np.allclose(points[1], [50, 200])

    def test_negative_coordinates(self):
        """Test line with negative coordinates."""
        line = Line(start=(-50, -25), end=(50, 25))
        points = line._points

        assert np.allclose(points[0], [-50, -25])
        assert np.allclose(points[1], [50, 25])


class TestShapeTransformations:
    """Tests for transformation operations on shapes."""

    def test_rectangle_shift(self):
        """Test shifting a rectangle."""
        rect = Rectangle(width=100.0, height=100.0)
        rect.shift((50, 30))

        center = rect.get_center()
        assert np.allclose(center, [50, 30])

    def test_circle_scale(self):
        """Test scaling a circle."""
        circle = Circle(radius=50.0)
        initial_bbox = circle.get_bounding_box()

        circle.set_scale(2.0)
        scaled_bbox = circle.get_bounding_box()

        # Bounding box should be twice as large
        initial_size = initial_bbox[1] - initial_bbox[0]
        scaled_size = scaled_bbox[1] - scaled_bbox[0]
        assert np.allclose(scaled_size, initial_size * 2)

    def test_line_rotate(self):
        """Test rotating a line.

        Note: rotate() updates self.rotation but doesn't modify _points directly.
        The rotation is applied via _get_transformed_points() during rendering.
        """
        line = Line(start=(0, 0), end=(100, 0))
        line.rotate(np.pi / 2)  # 90 degrees

        # Raw points remain unchanged
        assert np.allclose(line._points[0], [0, 0])
        assert np.allclose(line._points[1], [100, 0])

        # But rotation is stored and applied during rendering
        assert np.isclose(line.rotation, np.pi / 2)

        # Transformed points reflect the rotation
        transformed = line._get_transformed_points()
        # After 90 degree rotation, (100, 0) becomes (0, 100)
        assert np.isclose(transformed[1][0], 0, atol=1e-10)
        assert np.isclose(transformed[1][1], 100, atol=1e-10)


class TestShapeInheritance:
    """Tests that shapes properly inherit from CObject."""

    def test_rectangle_is_cobject(self):
        """Test Rectangle is a CObject."""
        from comix.cobject.cobject import CObject

        rect = Rectangle()
        assert isinstance(rect, CObject)

    def test_circle_is_cobject(self):
        """Test Circle is a CObject."""
        from comix.cobject.cobject import CObject

        circle = Circle()
        assert isinstance(circle, CObject)

    def test_line_is_cobject(self):
        """Test Line is a CObject."""
        from comix.cobject.cobject import CObject

        line = Line()
        assert isinstance(line, CObject)

    def test_rectangle_has_submobjects(self):
        """Test Rectangle has submobjects list."""
        rect = Rectangle()
        assert hasattr(rect, "submobjects")
        assert isinstance(rect.submobjects, list)

    def test_shapes_have_opacity(self):
        """Test shapes inherit opacity."""
        rect = Rectangle()
        circle = Circle()
        line = Line()

        assert hasattr(rect, "opacity")
        assert hasattr(circle, "opacity")
        assert hasattr(line, "opacity")

        rect.set_opacity(0.5)
        assert rect.opacity == 0.5
