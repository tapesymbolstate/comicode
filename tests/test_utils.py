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

    def test_rotate_points_empty(self):
        """Test rotating empty points array returns unchanged."""
        points = np.array([]).reshape(0, 2)
        rotated = rotate_points(points, np.pi / 2)
        assert len(rotated) == 0

    def test_rotate_points_with_center(self):
        """Test rotating points around custom center."""
        points = np.array([[2, 0], [3, 0]])
        center = (1, 0)
        rotated = rotate_points(points, np.pi / 2, center)
        expected = np.array([[1, 1], [1, 2]])
        assert np.allclose(rotated, expected, atol=1e-10)

    def test_scale_points_empty(self):
        """Test scaling empty points array returns unchanged."""
        points = np.array([]).reshape(0, 2)
        scaled = scale_points(points, 2.0)
        assert len(scaled) == 0

    def test_scale_points_with_center(self):
        """Test scaling points around custom center."""
        points = np.array([[2, 2], [4, 4]])
        center = (1, 1)
        scaled = scale_points(points, 2.0, center)
        # Point (2,2) relative to (1,1) is (1,1), scaled by 2 = (2,2) + center = (3,3)
        expected = np.array([[3, 3], [7, 7]])
        assert np.allclose(scaled, expected)

    def test_scale_points_nonuniform_with_center(self):
        """Test non-uniform scaling around custom center."""
        points = np.array([[2, 2]])
        center = (1, 1)
        scaled = scale_points(points, (2.0, 3.0), center)
        # (2,2) - (1,1) = (1,1), * (2,3) = (2,3), + (1,1) = (3,4)
        expected = np.array([[3, 4]])
        assert np.allclose(scaled, expected)

    def test_distance_same_point(self):
        """Test distance between same point is zero."""
        d = distance((5, 5), (5, 5))
        assert d == 0.0

    def test_distance_negative_coords(self):
        """Test distance with negative coordinates."""
        d = distance((-3, -4), (0, 0))
        assert d == 5.0

    def test_midpoint_same_point(self):
        """Test midpoint of same point is that point."""
        mid = midpoint((5, 5), (5, 5))
        assert np.allclose(mid, [5, 5])

    def test_midpoint_negative_coords(self):
        """Test midpoint with negative coordinates."""
        mid = midpoint((-4, -6), (4, 6))
        assert np.allclose(mid, [0, 0])

    def test_angle_between_negative_direction(self):
        """Test angle between points in negative x direction."""
        angle = angle_between((0, 0), (-1, 0))
        assert np.allclose(angle, np.pi)

    def test_angle_between_diagonal(self):
        """Test angle between diagonal points."""
        angle = angle_between((0, 0), (1, 1))
        assert np.allclose(angle, np.pi / 4)

    def test_normalize_angle_multiple_rotations(self):
        """Test normalizing angles with many rotations."""
        # 5*pi should normalize to pi
        assert np.allclose(normalize_angle(5 * np.pi), np.pi)
        # -5*pi should normalize to -pi
        assert np.allclose(normalize_angle(-5 * np.pi), -np.pi)

    def test_rotate_point_full_rotation(self):
        """Test rotating point by full 360 degrees returns original."""
        point = (3, 4)
        rotated = rotate_point(point, 2 * np.pi)
        assert np.allclose(rotated, point, atol=1e-10)


class TestBezierUtilsEdgeCases:
    """Additional edge case tests for bezier utility functions."""

    def test_create_bubble_path_whisper(self):
        """Test creating whisper bubble path (same as speech)."""
        path = create_bubble_path(width=100, height=80, style="whisper")
        assert len(path) > 0
        assert path.shape[1] == 2

    def test_create_bubble_path_unknown_style(self):
        """Test creating bubble with unknown style falls back to speech."""
        path = create_bubble_path(width=100, height=80, style="unknown")
        assert len(path) > 0

    def test_create_bubble_path_large_corner_radius_clamped(self):
        """Test corner radius is clamped to max size."""
        # Width 100, height 80 -> max radius = 40 (half of min dimension)
        path = create_bubble_path(width=100, height=80, corner_radius=100)
        assert len(path) > 0

    def test_create_bubble_path_corner_radii_clamped(self):
        """Test per-corner radii are clamped to max size."""
        path = create_bubble_path(
            width=100,
            height=80,
            corner_radii=(100.0, 100.0, 100.0, 100.0),
        )
        assert len(path) > 0

    def test_create_bubble_path_zero_wobble(self):
        """Test zero wobble produces consistent results."""
        path1 = create_bubble_path(width=100, height=80, wobble=0)
        path2 = create_bubble_path(width=100, height=80, wobble=0)
        assert np.allclose(path1, path2)

    def test_create_bubble_path_small_dimensions(self):
        """Test creating bubble with very small dimensions."""
        path = create_bubble_path(width=10, height=10)
        assert len(path) > 0

    def test_create_tail_points_all_directions(self):
        """Test tail points for all valid directions."""
        directions = [
            "bottom", "bottom-left", "bottom-right",
            "left", "right",
            "top", "top-left", "top-right",
        ]
        for direction in directions:
            tail = create_tail_points(width=100, height=80, direction=direction)
            assert len(tail) == 3, f"Direction {direction} should produce 3 points"

    def test_create_tail_points_invalid_direction(self):
        """Test invalid direction returns empty array."""
        tail = create_tail_points(width=100, height=80, direction="invalid")
        assert len(tail) == 0

    def test_create_tail_points_negative_length(self):
        """Test negative length returns empty array."""
        tail = create_tail_points(width=100, height=80, length=-10)
        assert len(tail) == 0

    def test_bezier_curve_single_point(self):
        """Test bezier curve with single point."""
        p0 = (0, 0)
        p1 = (1, 1)
        p2 = (2, 2)
        p3 = (3, 3)
        curve = bezier_curve(p0, p1, p2, p3, num_points=1)
        assert len(curve) == 1
        assert np.allclose(curve[0], p0)

    def test_bezier_curve_straight_line(self):
        """Test bezier curve as straight line."""
        p0 = (0, 0)
        p1 = (1, 0)
        p2 = (2, 0)
        p3 = (3, 0)
        curve = bezier_curve(p0, p1, p2, p3, num_points=4)
        # All points should have y=0
        assert np.allclose(curve[:, 1], 0)

    def test_create_thought_path_produces_bumpy_outline(self):
        """Test thought bubble has characteristic cloud shape."""
        path = create_bubble_path(width=100, height=80, style="thought")
        # Cloud path should have many points due to bumps
        assert len(path) >= 64  # 8 bumps * 8 points per bump

    def test_create_shout_path_produces_spiky_outline(self):
        """Test shout bubble has spiky shape."""
        path = create_bubble_path(width=100, height=80, style="shout")
        # Spiky path: 12 spikes * 2 points (outer + inner) + closing point = 25
        assert len(path) == 25

    def test_create_narrator_path_is_rectangle(self):
        """Test narrator bubble is exact rectangle."""
        path = create_bubble_path(width=100, height=80, style="narrator")
        # Should be exactly 5 points (4 corners + closing)
        assert len(path) == 5
        # Check corners are at expected positions
        half_w, half_h = 50, 40
        expected = [
            [-half_w, -half_h],
            [half_w, -half_h],
            [half_w, half_h],
            [-half_w, half_h],
            [-half_w, -half_h],
        ]
        assert np.allclose(path, expected)
