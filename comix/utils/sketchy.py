"""Utilities for hand-drawn/sketchy rendering effects."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def apply_hand_drawn_effect(
    points: list[tuple[float, float]],
    roughness: float = 1.0,
    segment_length: float = 10.0,
    seed: int | None = None,
) -> list[tuple[float, float]]:
    """Apply hand-drawn jitter effect to a sequence of points.

    Transforms clean geometric paths into wobbly, organic lines that look
    hand-drawn. Uses perpendicular jitter and segment subdivision for smooth
    sketchy appearance.

    Args:
        points: Original path points [(x, y), ...]
        roughness: Jitter intensity multiplier (0.0-2.0 typical). Higher values
            create more pronounced wobble. 0.5=subtle, 1.0=normal, 2.0=heavy.
        segment_length: Target length for subdivided segments in pixels.
            Smaller values create smoother wobbles but more points.
        seed: Random seed for reproducibility. None = random each time.

    Returns:
        Modified points with hand-drawn wobble effect applied.

    Example:
        >>> points = [(0, 0), (100, 0), (100, 100)]
        >>> sketchy_points = apply_hand_drawn_effect(points, roughness=1.0)
        >>> # sketchy_points will have wobbly edges
    """
    if not points or len(points) < 2:
        return points

    if roughness <= 0.0:
        return points

    if seed is not None:
        np.random.seed(seed)

    subdivided = _subdivide_path(points, segment_length)
    jittered = _jitter_points(subdivided, roughness)

    return [(float(x), float(y)) for x, y in jittered]


def _subdivide_path(
    points: list[tuple[float, float]],
    max_segment_length: float = 10.0,
) -> list[tuple[float, float]]:
    """Break long segments into shorter ones for smoother wobble.

    Args:
        points: Original path points
        max_segment_length: Maximum length of each segment in pixels

    Returns:
        Path with additional intermediate points inserted
    """
    if len(points) < 2:
        return points

    result = [points[0]]

    for i in range(len(points) - 1):
        p1 = np.array(points[i], dtype=np.float64)
        p2 = np.array(points[i + 1], dtype=np.float64)

        segment_vec = p2 - p1
        segment_length = np.linalg.norm(segment_vec)

        if segment_length > max_segment_length:
            num_subdivisions = int(np.ceil(segment_length / max_segment_length))
            for j in range(1, num_subdivisions):
                t = j / num_subdivisions
                intermediate = p1 + t * segment_vec
                result.append(tuple(intermediate))

        result.append(tuple(p2))

    return result


def _jitter_points(
    points: list[tuple[float, float]],
    roughness: float,
) -> NDArray[np.float64]:
    """Apply perpendicular jitter to points for hand-drawn effect.

    Args:
        points: Points to jitter
        roughness: Jitter intensity multiplier

    Returns:
        Jittered points as numpy array
    """
    if len(points) < 2:
        return np.array(points, dtype=np.float64)

    points_array = np.array(points, dtype=np.float64)
    result = []

    for i, (x, y) in enumerate(points_array):
        if i == 0 or i == len(points_array) - 1:
            jitter_scale = 0.2
        else:
            jitter_scale = 1.0

        if i < len(points_array) - 1:
            dx = points_array[i+1][0] - x
            dy = points_array[i+1][1] - y
        else:
            dx = x - points_array[i-1][0]
            dy = y - points_array[i-1][1]

        length = np.sqrt(dx*dx + dy*dy)
        if length > 0.001:
            perp_x = -dy / length
            perp_y = dx / length
        else:
            perp_x, perp_y = 0, 0

        jitter_amount = np.random.randn() * roughness * 0.5 * jitter_scale
        new_x = x + perp_x * jitter_amount
        new_y = y + perp_y * jitter_amount

        result.append([new_x, new_y])

    return np.array(result, dtype=np.float64)


def circle_to_polygon(
    center: tuple[float, float],
    radius: float,
    num_segments: int = 48,
) -> list[tuple[float, float]]:
    """Convert circle to polygon points for hand-drawn rendering.

    Args:
        center: Circle center (x, y)
        radius: Circle radius
        num_segments: Number of polygon vertices. More = smoother. Use 48-64
            for large circles, 24-32 for small ones.

    Returns:
        Polygon vertices approximating the circle

    Example:
        >>> points = circle_to_polygon((100, 100), 50, num_segments=48)
        >>> jittered = apply_hand_drawn_effect(points, roughness=1.0)
        >>> # Render jittered as polygon for sketchy circle
    """
    angles = np.linspace(0, 2 * np.pi, num_segments, endpoint=False)
    points = [
        (center[0] + radius * np.cos(angle), center[1] + radius * np.sin(angle))
        for angle in angles
    ]
    points.append(points[0])
    return points


def create_curved_segment(
    start: tuple[float, float],
    end: tuple[float, float],
    curve_amount: float = 0.0,
    num_points: int = 8,
) -> list[tuple[float, float]]:
    """Create a curved segment between two points using quadratic bezier.

    Args:
        start: Start point (x, y)
        end: End point (x, y)
        curve_amount: How much to curve (0.0-0.3 typical for natural look).
                      Positive curves left, negative curves right.
        num_points: Number of points in the curve

    Returns:
        List of points forming a smooth curve

    Example:
        >>> # Natural arm curve
        >>> shoulder = (100, 100)
        >>> elbow = (150, 150)
        >>> curved_arm = create_curved_segment(shoulder, elbow, curve_amount=0.15)
    """
    if abs(curve_amount) < 0.001 or num_points < 2:
        return [start, end]

    start_arr = np.array(start, dtype=np.float64)
    end_arr = np.array(end, dtype=np.float64)

    # Vector from start to end
    direction = end_arr - start_arr
    length = np.linalg.norm(direction)

    if length < 1.0:
        return [start, end]

    # Perpendicular vector (rotate 90 degrees)
    perp = np.array([-direction[1], direction[0]], dtype=np.float64)
    perp = perp / np.linalg.norm(perp)

    # Control point at midpoint with perpendicular offset
    midpoint = (start_arr + end_arr) / 2
    control_offset = curve_amount * length
    control = midpoint + perp * control_offset

    # Generate points along quadratic bezier curve
    points = []
    for i in range(num_points + 1):
        t = i / num_points

        # Quadratic bezier formula: (1-t)^2*P0 + 2*(1-t)*t*P1 + t^2*P2
        point = (
            (1 - t) ** 2 * start_arr
            + 2 * (1 - t) * t * control
            + t**2 * end_arr
        )
        points.append((float(point[0]), float(point[1])))

    return points
