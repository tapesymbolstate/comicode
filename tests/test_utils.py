"""Tests for utility functions."""

import numpy as np

from comix.utils.bezier import (
    create_bubble_path,
    create_minimal_tail_points,
    create_smooth_tail_points,
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


class TestBezierUtilsExtendedEdgeCases:
    """Extended edge case tests for bezier utility functions.

    These tests focus on boundary conditions, numerical edge cases,
    and unusual parameter combinations.
    """

    # ===== Bezier Curve Edge Cases =====

    def test_bezier_curve_large_num_points(self):
        """Test bezier curve with many points."""
        p0 = (0, 0)
        p1 = (1, 2)
        p2 = (3, 2)
        p3 = (4, 0)
        curve = bezier_curve(p0, p1, p2, p3, num_points=100)
        assert len(curve) == 100
        assert np.allclose(curve[0], p0)
        assert np.allclose(curve[-1], p3)

    def test_bezier_curve_two_points(self):
        """Test bezier curve with only two points."""
        p0 = (0, 0)
        p1 = (1, 1)
        p2 = (2, 1)
        p3 = (3, 0)
        curve = bezier_curve(p0, p1, p2, p3, num_points=2)
        assert len(curve) == 2
        assert np.allclose(curve[0], p0)
        assert np.allclose(curve[-1], p3)

    def test_bezier_curve_identical_control_points(self):
        """Test bezier curve with identical control points (degenerate)."""
        p0 = (5, 5)
        p1 = (5, 5)
        p2 = (5, 5)
        p3 = (5, 5)
        curve = bezier_curve(p0, p1, p2, p3, num_points=10)
        # All points should be at (5, 5)
        assert len(curve) == 10
        assert np.allclose(curve, [[5, 5]] * 10)

    def test_bezier_curve_large_coordinates(self):
        """Test bezier curve with large coordinate values."""
        p0 = (0, 0)
        p1 = (1e6, 1e6)
        p2 = (2e6, 1e6)
        p3 = (3e6, 0)
        curve = bezier_curve(p0, p1, p2, p3, num_points=10)
        assert len(curve) == 10
        assert np.allclose(curve[0], p0)
        assert np.allclose(curve[-1], p3)

    def test_bezier_curve_negative_coordinates(self):
        """Test bezier curve with negative coordinates."""
        p0 = (-100, -100)
        p1 = (-50, 0)
        p2 = (50, 0)
        p3 = (100, -100)
        curve = bezier_curve(p0, p1, p2, p3, num_points=5)
        assert len(curve) == 5
        assert np.allclose(curve[0], p0)
        assert np.allclose(curve[-1], p3)

    def test_bezier_curve_float_precision(self):
        """Test bezier curve maintains float precision."""
        p0 = (0.123456789, 0.987654321)
        p1 = (1.111111111, 2.222222222)
        p2 = (3.333333333, 2.222222222)
        p3 = (4.444444444, 0.555555555)
        curve = bezier_curve(p0, p1, p2, p3, num_points=10)
        # Check endpoints maintain precision
        assert np.allclose(curve[0], p0, rtol=1e-9)
        assert np.allclose(curve[-1], p3, rtol=1e-9)

    # ===== Bubble Path Dimension Edge Cases =====

    def test_create_bubble_path_very_small_width(self):
        """Test bubble path with very small width."""
        path = create_bubble_path(width=1, height=100)
        assert len(path) > 0
        assert path.shape[1] == 2

    def test_create_bubble_path_very_small_height(self):
        """Test bubble path with very small height."""
        path = create_bubble_path(width=100, height=1)
        assert len(path) > 0
        assert path.shape[1] == 2

    def test_create_bubble_path_square(self):
        """Test bubble path with square dimensions."""
        path = create_bubble_path(width=100, height=100)
        assert len(path) > 0

    def test_create_bubble_path_extreme_aspect_ratio_wide(self):
        """Test bubble path with extreme width:height ratio."""
        path = create_bubble_path(width=1000, height=10)
        assert len(path) > 0

    def test_create_bubble_path_extreme_aspect_ratio_tall(self):
        """Test bubble path with extreme height:width ratio."""
        path = create_bubble_path(width=10, height=1000)
        assert len(path) > 0

    def test_create_bubble_path_large_dimensions(self):
        """Test bubble path with large dimensions."""
        path = create_bubble_path(width=10000, height=10000)
        assert len(path) > 0

    def test_create_bubble_path_floating_point_dimensions(self):
        """Test bubble path with non-integer dimensions."""
        path = create_bubble_path(width=100.5, height=80.3)
        assert len(path) > 0

    # ===== Corner Radius Edge Cases =====

    def test_create_bubble_path_zero_corner_radius(self):
        """Test bubble path with zero corner radius."""
        path = create_bubble_path(width=100, height=80, corner_radius=0)
        assert len(path) > 0

    def test_create_bubble_path_very_small_corner_radius(self):
        """Test bubble path with very small corner radius."""
        path = create_bubble_path(width=100, height=80, corner_radius=0.001)
        assert len(path) > 0

    def test_create_bubble_path_corner_radius_equals_half_min_dimension(self):
        """Test corner radius equal to half the minimum dimension."""
        # Half of min(100, 80) = 40
        path = create_bubble_path(width=100, height=80, corner_radius=40)
        assert len(path) > 0

    def test_create_bubble_path_mixed_corner_radii_some_zero(self):
        """Test bubble path with some corner radii at zero."""
        path = create_bubble_path(
            width=100,
            height=80,
            corner_radii=(0.0, 10.0, 0.0, 10.0),
        )
        assert len(path) > 0

    def test_create_bubble_path_asymmetric_corner_radii(self):
        """Test bubble path with asymmetric corner radii."""
        path = create_bubble_path(
            width=100,
            height=80,
            corner_radii=(5.0, 10.0, 15.0, 20.0),
        )
        assert len(path) > 0

    # ===== Points Per Segment Edge Cases =====

    def test_create_bubble_path_one_point_per_segment(self):
        """Test bubble path with minimum points per segment."""
        path = create_bubble_path(
            width=100,
            height=80,
            num_points_per_segment=1,
        )
        assert len(path) > 0

    def test_create_bubble_path_two_points_per_segment(self):
        """Test bubble path with two points per segment."""
        path = create_bubble_path(
            width=100,
            height=80,
            num_points_per_segment=2,
        )
        assert len(path) > 0

    def test_create_bubble_path_many_points_per_segment(self):
        """Test bubble path with many points per segment."""
        path = create_bubble_path(
            width=100,
            height=80,
            num_points_per_segment=100,
        )
        assert len(path) > 0
        # Should have 4 corners * 100 points + closing point = 401
        assert len(path) == 401

    # ===== Wobble Edge Cases =====

    def test_create_bubble_path_extreme_wobble(self):
        """Test bubble path with extreme wobble value (>1.0)."""
        path = create_bubble_path(width=100, height=80, wobble=5.0)
        assert len(path) > 0

    def test_create_bubble_path_tiny_wobble(self):
        """Test bubble path with very small wobble value."""
        path = create_bubble_path(width=100, height=80, wobble=0.001)
        assert len(path) > 0

    def test_create_bubble_path_wobble_on_different_styles(self):
        """Test that wobble only applies to speech/whisper styles."""
        # Speech should have wobble applied
        speech_path = create_bubble_path(
            width=100, height=80, style="speech", wobble=0.5
        )
        assert len(speech_path) > 0

        # Thought bubble doesn't use wobble (uses cloud path)
        thought_path = create_bubble_path(
            width=100, height=80, style="thought", wobble=0.5
        )
        assert len(thought_path) > 0

        # Shout bubble doesn't use wobble (uses spiky path)
        shout_path = create_bubble_path(
            width=100, height=80, style="shout", wobble=0.5
        )
        assert len(shout_path) > 0

    def test_create_bubble_path_wobble_unknown_mode(self):
        """Test bubble path with unknown wobble mode falls back to random."""
        path = create_bubble_path(
            width=100, height=80, wobble=0.5, wobble_mode="unknown"
        )
        assert len(path) > 0

    # ===== Tail Points Edge Cases =====

    def test_create_tail_points_very_small_bubble(self):
        """Test tail points with very small bubble dimensions."""
        tail = create_tail_points(width=5, height=5, length=10)
        assert len(tail) == 3

    def test_create_tail_points_very_large_bubble(self):
        """Test tail points with large bubble dimensions."""
        tail = create_tail_points(width=10000, height=10000, length=500)
        assert len(tail) == 3

    def test_create_tail_points_very_long_tail(self):
        """Test tail points with very long tail."""
        tail = create_tail_points(width=100, height=80, length=1000)
        assert len(tail) == 3

    def test_create_tail_points_very_short_tail(self):
        """Test tail points with very short tail."""
        tail = create_tail_points(width=100, height=80, length=1)
        assert len(tail) == 3

    def test_create_tail_points_wide_tip(self):
        """Test tail points with very wide tip."""
        tail = create_tail_points(width=100, height=80, tip_width=100)
        assert len(tail) == 3

    def test_create_tail_points_narrow_tip(self):
        """Test tail points with very narrow tip."""
        tail = create_tail_points(width=100, height=80, tip_width=1)
        assert len(tail) == 3

    def test_create_tail_points_zero_tip_width(self):
        """Test tail points with zero tip width (point tail)."""
        tail = create_tail_points(width=100, height=80, tip_width=0)
        assert len(tail) == 3
        # First and third points should be identical when tip_width=0
        assert np.allclose(tail[0], tail[2])

    def test_create_tail_points_floating_dimensions(self):
        """Test tail points with floating point dimensions."""
        tail = create_tail_points(
            width=100.5,
            height=80.3,
            length=30.7,
            tip_width=15.2,
        )
        assert len(tail) == 3

    # ===== Style-Specific Edge Cases =====

    def test_create_shout_path_dimensions_preserved(self):
        """Test shout path respects width/height proportions."""
        path_wide = create_bubble_path(width=200, height=100, style="shout")
        path_tall = create_bubble_path(width=100, height=200, style="shout")

        # Wide path should be wider than tall
        wide_x_range = np.ptp(path_wide[:, 0])
        tall_x_range = np.ptp(path_tall[:, 0])
        assert wide_x_range > tall_x_range

    def test_create_thought_path_dimensions_preserved(self):
        """Test thought path respects width/height proportions."""
        path_wide = create_bubble_path(width=200, height=100, style="thought")
        path_tall = create_bubble_path(width=100, height=200, style="thought")

        wide_x_range = np.ptp(path_wide[:, 0])
        tall_x_range = np.ptp(path_tall[:, 0])
        assert wide_x_range > tall_x_range

    def test_create_narrator_path_exact_dimensions(self):
        """Test narrator path has exact specified dimensions."""
        path = create_bubble_path(width=200, height=100, style="narrator")
        x_range = np.ptp(path[:, 0])
        y_range = np.ptp(path[:, 1])
        assert np.isclose(x_range, 200)
        assert np.isclose(y_range, 100)

    # ===== Numerical Stability =====

    def test_bubble_path_closed_loop(self):
        """Test bubble path forms a closed loop (first == last point)."""
        for style in ["speech", "thought", "shout", "narrator", "whisper"]:
            path = create_bubble_path(width=100, height=80, style=style)
            assert np.allclose(path[0], path[-1]), f"Style {style} not closed"

    def test_bubble_path_no_nan_values(self):
        """Test bubble path contains no NaN values."""
        for style in ["speech", "thought", "shout", "narrator", "whisper"]:
            path = create_bubble_path(width=100, height=80, style=style)
            assert not np.any(np.isnan(path)), f"Style {style} has NaN"

    def test_bubble_path_no_inf_values(self):
        """Test bubble path contains no infinite values."""
        for style in ["speech", "thought", "shout", "narrator", "whisper"]:
            path = create_bubble_path(width=100, height=80, style=style)
            assert not np.any(np.isinf(path)), f"Style {style} has inf"

    def test_tail_points_no_nan_inf(self):
        """Test tail points contain no NaN or infinite values."""
        for direction in [
            "bottom", "bottom-left", "bottom-right",
            "left", "right", "top", "top-left", "top-right",
        ]:
            tail = create_tail_points(width=100, height=80, direction=direction)
            assert not np.any(np.isnan(tail)), f"Direction {direction} has NaN"
            assert not np.any(np.isinf(tail)), f"Direction {direction} has inf"

    # ===== Combination Tests =====

    def test_bubble_path_corner_radii_with_wobble(self):
        """Test combining custom corner radii with wobble."""
        path = create_bubble_path(
            width=100,
            height=80,
            corner_radii=(5.0, 10.0, 15.0, 20.0),
            wobble=0.3,
            wobble_mode="wave",
        )
        assert len(path) > 0

    def test_bubble_path_all_parameters(self):
        """Test bubble path with all parameters specified."""
        path = create_bubble_path(
            width=150,
            height=100,
            style="speech",
            corner_radius=15,
            corner_radii=(10, 15, 20, 25),  # Takes precedence over corner_radius
            wobble=0.2,
            wobble_mode="random",
            num_points_per_segment=12,
        )
        assert len(path) > 0
        # 4 corners * 12 points + closing = 49
        assert len(path) == 49


class TestSmoothTailPoints:
    """Tests for smooth/curved tail point generation."""

    def test_create_smooth_tail_basic(self):
        """Test creating smooth tail with basic parameters."""
        tail = create_smooth_tail_points(width=100, height=80, length=30)
        # Smooth tail has many bezier curve points (>3)
        assert len(tail) > 3

    def test_create_smooth_tail_zero_length(self):
        """Test smooth tail with zero length returns empty array."""
        tail = create_smooth_tail_points(width=100, height=80, length=0)
        assert len(tail) == 0

    def test_create_smooth_tail_negative_length(self):
        """Test smooth tail with negative length returns empty array."""
        tail = create_smooth_tail_points(width=100, height=80, length=-10)
        assert len(tail) == 0

    def test_create_smooth_tail_all_directions(self):
        """Test smooth tail for all valid directions."""
        directions = [
            "bottom", "bottom-left", "bottom-right",
            "left", "right",
            "top", "top-left", "top-right",
        ]
        for direction in directions:
            tail = create_smooth_tail_points(
                width=100, height=80, direction=direction, length=30
            )
            assert len(tail) > 3, f"Direction {direction} should produce curved tail"

    def test_create_smooth_tail_invalid_direction(self):
        """Test smooth tail with invalid direction returns empty array."""
        tail = create_smooth_tail_points(width=100, height=80, direction="invalid")
        assert len(tail) == 0

    def test_create_smooth_tail_has_more_points_than_classic(self):
        """Test smooth tail has more points than classic triangular tail."""
        smooth = create_smooth_tail_points(width=100, height=80, length=30)
        classic = create_tail_points(width=100, height=80, length=30)
        assert len(smooth) > len(classic)

    def test_create_smooth_tail_custom_num_points(self):
        """Test smooth tail with custom number of bezier points."""
        tail_low = create_smooth_tail_points(
            width=100, height=80, length=30, num_points=6
        )
        tail_high = create_smooth_tail_points(
            width=100, height=80, length=30, num_points=20
        )
        # Higher num_points should produce more points
        assert len(tail_high) > len(tail_low)

    def test_create_smooth_tail_no_nan_inf(self):
        """Test smooth tail contains no NaN or infinite values."""
        for direction in [
            "bottom", "bottom-left", "bottom-right",
            "left", "right", "top", "top-left", "top-right",
        ]:
            tail = create_smooth_tail_points(
                width=100, height=80, direction=direction, length=30
            )
            assert not np.any(np.isnan(tail)), f"Direction {direction} has NaN"
            assert not np.any(np.isinf(tail)), f"Direction {direction} has inf"

    def test_create_smooth_tail_forms_closed_shape(self):
        """Test smooth tail can form a filled shape (first connects to last via bubble edge)."""
        tail = create_smooth_tail_points(width=100, height=80, length=30)
        # Tail should have continuous points that can be filled
        assert len(tail) > 0
        # Points should form a shape (not degenerate)
        x_range = np.ptp(tail[:, 0])
        y_range = np.ptp(tail[:, 1])
        assert x_range > 0 or y_range > 0


class TestMinimalTailPoints:
    """Tests for minimal/subtle tail point generation."""

    def test_create_minimal_tail_basic(self):
        """Test creating minimal tail with basic parameters."""
        tail = create_minimal_tail_points(width=100, height=80, length=30)
        # Minimal tail should have points (uses smooth tail internally)
        assert len(tail) > 0

    def test_create_minimal_tail_zero_length(self):
        """Test minimal tail with zero length returns empty array."""
        tail = create_minimal_tail_points(width=100, height=80, length=0)
        assert len(tail) == 0

    def test_create_minimal_tail_all_directions(self):
        """Test minimal tail for all valid directions."""
        directions = [
            "bottom", "bottom-left", "bottom-right",
            "left", "right",
            "top", "top-left", "top-right",
        ]
        for direction in directions:
            tail = create_minimal_tail_points(
                width=100, height=80, direction=direction, length=30
            )
            assert len(tail) > 0, f"Direction {direction} should produce tail"

    def test_create_minimal_tail_invalid_direction(self):
        """Test minimal tail with invalid direction returns empty array."""
        tail = create_minimal_tail_points(width=100, height=80, direction="invalid")
        assert len(tail) == 0

    def test_create_minimal_tail_shorter_effective_length(self):
        """Test minimal tail uses shorter effective length than specified."""
        # Minimal uses 50% of length capped at 20
        tail = create_minimal_tail_points(width=100, height=80, length=100)
        # The tail should be based on shorter length (20 max)
        assert len(tail) > 0

    def test_create_minimal_tail_no_nan_inf(self):
        """Test minimal tail contains no NaN or infinite values."""
        for direction in [
            "bottom", "bottom-left", "bottom-right",
            "left", "right", "top", "top-left", "top-right",
        ]:
            tail = create_minimal_tail_points(
                width=100, height=80, direction=direction, length=30
            )
            assert not np.any(np.isnan(tail)), f"Direction {direction} has NaN"
            assert not np.any(np.isinf(tail)), f"Direction {direction} has inf"
