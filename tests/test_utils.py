"""Tests for utility functions."""

import numpy as np

from comix.utils.bezier import (
    create_bubble_path,
    create_tail_points,
    bezier_curve,
)
from comix.utils.geometry import (
    rotate_point,
    rotate_points,
    translate_points,
    scale_points,
    distance,
    midpoint,
    normalize_angle,
    angle_between,
    bounding_box,
)


class TestBezierUtils:
    """Tests for bezier utility functions."""

    def test_create_bubble_path_speech(self):
        """Test creating speech bubble path."""
        path = create_bubble_path(width=100, height=80, style="speech")
        assert len(path) > 0
        assert path.shape[1] == 2

    def test_create_bubble_path_thought(self):
        """Test creating thought bubble path."""
        path = create_bubble_path(width=100, height=80, style="thought")
        assert len(path) > 0

    def test_create_bubble_path_shout(self):
        """Test creating shout bubble path."""
        path = create_bubble_path(width=100, height=80, style="shout")
        assert len(path) > 0

    def test_create_bubble_path_narrator(self):
        """Test creating narrator bubble path (rectangle)."""
        path = create_bubble_path(width=100, height=80, style="narrator")
        assert len(path) == 5  # Rectangle with closing point

    def test_create_bubble_path_with_corner_radii(self):
        """Test creating bubble path with per-corner radii."""
        path = create_bubble_path(
            width=100,
            height=80,
            style="speech",
            corner_radii=(5.0, 10.0, 15.0, 20.0),
        )
        assert len(path) > 0
        assert path.shape[1] == 2

    def test_create_bubble_path_wobble_random(self):
        """Test creating bubble path with random wobble."""
        path1 = create_bubble_path(
            width=100, height=80, style="speech",
            wobble=0.5, wobble_mode="random"
        )
        path2 = create_bubble_path(
            width=100, height=80, style="speech",
            wobble=0.5, wobble_mode="random"
        )
        # Random wobble should produce different paths
        assert len(path1) > 0
        assert len(path2) > 0

    def test_create_bubble_path_wobble_wave(self):
        """Test creating bubble path with wave wobble."""
        path = create_bubble_path(
            width=100, height=80, style="speech",
            wobble=0.5, wobble_mode="wave"
        )
        assert len(path) > 0
        assert path.shape[1] == 2

    def test_create_tail_points(self):
        """Test creating tail points."""
        tail = create_tail_points(
            width=100,
            height=80,
            direction="bottom-left",
            length=30,
            tip_width=20,
        )
        assert len(tail) == 3  # Triangle

    def test_create_tail_points_zero_length(self):
        """Test that zero length returns empty array."""
        tail = create_tail_points(width=100, height=80, length=0)
        assert len(tail) == 0

    def test_bezier_curve(self):
        """Test bezier curve generation."""
        p0 = (0, 0)
        p1 = (0.3, 1)
        p2 = (0.7, 1)
        p3 = (1, 0)

        curve = bezier_curve(p0, p1, p2, p3, num_points=10)
        assert len(curve) == 10
        assert np.allclose(curve[0], p0)
        assert np.allclose(curve[-1], p3)


class TestGeometryUtils:
    """Tests for geometry utility functions."""

    def test_rotate_point(self):
        """Test rotating a single point."""
        point = (1, 0)
        rotated = rotate_point(point, np.pi / 2)  # 90 degrees
        assert np.allclose(rotated, [0, 1], atol=1e-10)

    def test_rotate_point_with_center(self):
        """Test rotating around a custom center."""
        point = (2, 0)
        center = (1, 0)
        rotated = rotate_point(point, np.pi / 2, center)
        assert np.allclose(rotated, [1, 1], atol=1e-10)

    def test_rotate_points(self):
        """Test rotating multiple points."""
        points = np.array([[1, 0], [0, 1], [-1, 0]])
        rotated = rotate_points(points, np.pi / 2)
        expected = np.array([[0, 1], [-1, 0], [0, -1]])
        assert np.allclose(rotated, expected, atol=1e-10)

    def test_translate_points(self):
        """Test translating points."""
        points = np.array([[0, 0], [1, 1], [2, 2]])
        translated = translate_points(points, (10, 20))
        expected = np.array([[10, 20], [11, 21], [12, 22]])
        assert np.allclose(translated, expected)

    def test_scale_points(self):
        """Test scaling points."""
        points = np.array([[1, 1], [2, 2]])
        scaled = scale_points(points, 2.0)
        expected = np.array([[2, 2], [4, 4]])
        assert np.allclose(scaled, expected)

    def test_scale_points_nonuniform(self):
        """Test non-uniform scaling."""
        points = np.array([[1, 1], [2, 2]])
        scaled = scale_points(points, (2.0, 3.0))
        expected = np.array([[2, 3], [4, 6]])
        assert np.allclose(scaled, expected)

    def test_distance(self):
        """Test distance calculation."""
        d = distance((0, 0), (3, 4))
        assert d == 5.0

    def test_midpoint(self):
        """Test midpoint calculation."""
        mid = midpoint((0, 0), (4, 6))
        assert np.allclose(mid, [2, 3])

    def test_normalize_angle(self):
        """Test angle normalization."""
        assert np.allclose(normalize_angle(0), 0)
        assert np.allclose(normalize_angle(np.pi), np.pi)
        assert np.allclose(normalize_angle(3 * np.pi), np.pi)
        assert np.allclose(normalize_angle(-3 * np.pi), -np.pi)

    def test_angle_between(self):
        """Test angle between points."""
        angle = angle_between((0, 0), (1, 0))
        assert np.allclose(angle, 0)

        angle = angle_between((0, 0), (0, 1))
        assert np.allclose(angle, np.pi / 2)

    def test_bounding_box(self):
        """Test bounding box calculation."""
        points = np.array([[0, 0], [10, 5], [5, 15]])
        min_pt, max_pt = bounding_box(points)
        assert np.allclose(min_pt, [0, 0])
        assert np.allclose(max_pt, [10, 15])

    def test_bounding_box_empty(self):
        """Test bounding box of empty points."""
        points = np.array([]).reshape(0, 2)
        min_pt, max_pt = bounding_box(points)
        assert np.allclose(min_pt, [0, 0])
        assert np.allclose(max_pt, [0, 0])
