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
