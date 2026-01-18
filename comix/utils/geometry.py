"""Geometry utilities for coordinate transformations."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def rotate_point(
    point: tuple[float, float], angle: float, center: tuple[float, float] = (0, 0)
) -> NDArray[np.float64]:
    """Rotate a point around a center.

    Args:
        point: (x, y) point to rotate.
        angle: Rotation angle in radians.
        center: Center of rotation.

    Returns:
        Rotated (x, y) point.
    """
    cos_a = np.cos(angle)
    sin_a = np.sin(angle)

    dx = point[0] - center[0]
    dy = point[1] - center[1]

    x = center[0] + dx * cos_a - dy * sin_a
    y = center[1] + dx * sin_a + dy * cos_a

    return np.array([x, y], dtype=np.float64)


def rotate_points(
    points: NDArray[np.float64], angle: float, center: tuple[float, float] = (0, 0)
) -> NDArray[np.float64]:
    """Rotate multiple points around a center.

    Args:
        points: Array of (x, y) points.
        angle: Rotation angle in radians.
        center: Center of rotation.

    Returns:
        Array of rotated points.
    """
    if len(points) == 0:
        return points

    cos_a = np.cos(angle)
    sin_a = np.sin(angle)

    centered = points - np.array(center)

    rotation_matrix = np.array([[cos_a, -sin_a], [sin_a, cos_a]])
    rotated = centered @ rotation_matrix.T

    return rotated + np.array(center)  # type: ignore[no-any-return]


def translate_points(
    points: NDArray[np.float64], offset: tuple[float, float]
) -> NDArray[np.float64]:
    """Translate points by an offset.

    Args:
        points: Array of (x, y) points.
        offset: (dx, dy) translation offset.

    Returns:
        Array of translated points.
    """
    return points + np.array(offset, dtype=np.float64)


def scale_points(
    points: NDArray[np.float64],
    scale: float | tuple[float, float],
    center: tuple[float, float] = (0, 0),
) -> NDArray[np.float64]:
    """Scale points around a center.

    Args:
        points: Array of (x, y) points.
        scale: Scale factor (uniform) or (sx, sy) for non-uniform scaling.
        center: Center of scaling.

    Returns:
        Array of scaled points.
    """
    if len(points) == 0:
        return points

    if isinstance(scale, (int, float)):
        scale = (scale, scale)

    centered = points - np.array(center)
    scaled = centered * np.array(scale)

    return scaled + np.array(center)  # type: ignore[no-any-return]


def distance(p1: tuple[float, float], p2: tuple[float, float]) -> float:
    """Calculate distance between two points."""
    return float(np.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2))


def midpoint(p1: tuple[float, float], p2: tuple[float, float]) -> NDArray[np.float64]:
    """Calculate midpoint between two points."""
    return np.array([(p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2], dtype=np.float64)


def normalize_angle(angle: float) -> float:
    """Normalize angle to [-pi, pi] range."""
    while angle > np.pi:
        angle -= 2 * np.pi
    while angle < -np.pi:
        angle += 2 * np.pi
    return angle


def angle_between(p1: tuple[float, float], p2: tuple[float, float]) -> float:
    """Calculate angle from p1 to p2."""
    return float(np.arctan2(p2[1] - p1[1], p2[0] - p1[0]))


def bounding_box(
    points: NDArray[np.float64],
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Calculate bounding box of points.

    Returns:
        (min_point, max_point)
    """
    if len(points) == 0:
        return (
            np.array([0.0, 0.0], dtype=np.float64),
            np.array([0.0, 0.0], dtype=np.float64),
        )

    min_point = np.min(points, axis=0)
    max_point = np.max(points, axis=0)

    return (min_point, max_point)


def point_to_segment_distance(
    point: tuple[float, float],
    seg_start: tuple[float, float],
    seg_end: tuple[float, float],
) -> float:
    """Calculate the minimum distance from a point to a line segment.

    Args:
        point: The point (x, y).
        seg_start: Start of the line segment (x, y).
        seg_end: End of the line segment (x, y).

    Returns:
        The minimum distance from the point to the line segment.
    """
    px, py = point
    x1, y1 = seg_start
    x2, y2 = seg_end

    dx = x2 - x1
    dy = y2 - y1

    if dx == 0 and dy == 0:
        return distance(point, seg_start)

    t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)))

    proj_x = x1 + t * dx
    proj_y = y1 + t * dy

    return distance(point, (proj_x, proj_y))


def segment_to_segment_distance(
    seg1_start: tuple[float, float],
    seg1_end: tuple[float, float],
    seg2_start: tuple[float, float],
    seg2_end: tuple[float, float],
) -> float:
    """Calculate the minimum distance between two line segments.

    Args:
        seg1_start: Start of first segment.
        seg1_end: End of first segment.
        seg2_start: Start of second segment.
        seg2_end: End of second segment.

    Returns:
        The minimum distance between the two segments.
    """
    d1 = point_to_segment_distance(seg1_start, seg2_start, seg2_end)
    d2 = point_to_segment_distance(seg1_end, seg2_start, seg2_end)
    d3 = point_to_segment_distance(seg2_start, seg1_start, seg1_end)
    d4 = point_to_segment_distance(seg2_end, seg1_start, seg1_end)

    return min(d1, d2, d3, d4)


def polygon_to_polygon_distance(
    polygon1: NDArray[np.float64],
    polygon2: NDArray[np.float64],
) -> float:
    """Calculate the minimum distance between two polygons.

    This considers all edges of both polygons and finds the minimum distance
    between any pair of edges. Useful for calculating proper gutter spacing
    between non-rectangular panels.

    Args:
        polygon1: Array of (x, y) points defining the first polygon.
        polygon2: Array of (x, y) points defining the second polygon.

    Returns:
        The minimum distance between any edges of the two polygons.
        Returns 0.0 if either polygon is empty or has less than 2 points.
    """
    if len(polygon1) < 2 or len(polygon2) < 2:
        return 0.0

    min_dist = float("inf")

    n1 = len(polygon1)
    n2 = len(polygon2)

    for i in range(n1):
        p1_start = (float(polygon1[i][0]), float(polygon1[i][1]))
        p1_end = (float(polygon1[(i + 1) % n1][0]), float(polygon1[(i + 1) % n1][1]))

        for j in range(n2):
            p2_start = (float(polygon2[j][0]), float(polygon2[j][1]))
            p2_end = (float(polygon2[(j + 1) % n2][0]), float(polygon2[(j + 1) % n2][1]))

            dist = segment_to_segment_distance(p1_start, p1_end, p2_start, p2_end)
            min_dist = min(min_dist, dist)

    return min_dist if min_dist != float("inf") else 0.0


def calculate_gutter_adjustment(
    polygon1: NDArray[np.float64],
    polygon2: NDArray[np.float64],
    desired_gutter: float,
    axis: str = "horizontal",
) -> float:
    """Calculate the position adjustment needed to achieve desired gutter spacing.

    For non-rectangular panels, the bounding box edges may not represent the
    actual panel edges. This function calculates how much to adjust the position
    of polygon2 to achieve the desired gutter spacing from polygon1.

    Args:
        polygon1: Array of (x, y) points for the first (stationary) polygon.
        polygon2: Array of (x, y) points for the second (to be moved) polygon.
        desired_gutter: The desired minimum distance between polygon edges.
        axis: "horizontal" to adjust along x-axis, "vertical" for y-axis.

    Returns:
        The additional offset needed beyond bounding box placement.
        Positive values mean polygon2 should move further away from polygon1.
    """
    if len(polygon1) < 2 or len(polygon2) < 2:
        return 0.0

    current_distance = polygon_to_polygon_distance(polygon1, polygon2)

    adjustment = desired_gutter - current_distance

    return max(0.0, adjustment)
