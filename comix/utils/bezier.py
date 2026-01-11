"""Bezier curve utilities for bubble shapes."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def create_bubble_path(
    width: float,
    height: float,
    style: str = "speech",
    corner_radius: float = 20.0,
    wobble: float = 0.0,
    num_points_per_segment: int = 8,
) -> NDArray[np.float64]:
    """Create bubble outline path.

    Args:
        width: Bubble width.
        height: Bubble height.
        style: Bubble style ("speech", "thought", "shout", "whisper", "narrator").
        corner_radius: Corner rounding radius.
        wobble: Random wobble factor (0-1).
        num_points_per_segment: Points per curve segment.

    Returns:
        Array of (x, y) points forming the bubble outline.
    """
    half_w = width / 2
    half_h = height / 2

    radius = min(corner_radius, min(half_w, half_h))

    if style == "narrator":
        return _create_rectangle_path(half_w, half_h)

    if style == "shout":
        return _create_spiky_path(half_w, half_h, num_spikes=12)

    if style == "thought":
        return _create_cloud_path(half_w, half_h, num_bumps=8)

    points = _create_rounded_rect_path(half_w, half_h, radius, num_points_per_segment)

    if wobble > 0:
        noise = np.random.randn(len(points), 2) * wobble * 2
        points = points + noise

    return points


def _create_rectangle_path(half_w: float, half_h: float) -> NDArray[np.float64]:
    """Create simple rectangle path."""
    return np.array(
        [
            [-half_w, -half_h],
            [half_w, -half_h],
            [half_w, half_h],
            [-half_w, half_h],
            [-half_w, -half_h],
        ],
        dtype=np.float64,
    )


def _create_rounded_rect_path(
    half_w: float, half_h: float, radius: float, num_points: int
) -> NDArray[np.float64]:
    """Create rounded rectangle path."""
    points = []

    corners = [
        (half_w - radius, -half_h + radius, -np.pi / 2, 0),
        (half_w - radius, half_h - radius, 0, np.pi / 2),
        (-half_w + radius, half_h - radius, np.pi / 2, np.pi),
        (-half_w + radius, -half_h + radius, np.pi, 3 * np.pi / 2),
    ]

    for cx, cy, start_angle, end_angle in corners:
        angles = np.linspace(start_angle, end_angle, num_points)
        for angle in angles:
            x = cx + radius * np.cos(angle)
            y = cy + radius * np.sin(angle)
            points.append([x, y])

    points.append(points[0])

    return np.array(points, dtype=np.float64)


def _create_spiky_path(
    half_w: float, half_h: float, num_spikes: int = 12
) -> NDArray[np.float64]:
    """Create spiky (shout) bubble path."""
    points = []

    for i in range(num_spikes):
        angle = 2 * np.pi * i / num_spikes
        next_angle = 2 * np.pi * (i + 0.5) / num_spikes

        outer_x = half_w * 1.2 * np.cos(angle)
        outer_y = half_h * 1.2 * np.sin(angle)
        points.append([outer_x, outer_y])

        inner_x = half_w * 0.7 * np.cos(next_angle)
        inner_y = half_h * 0.7 * np.sin(next_angle)
        points.append([inner_x, inner_y])

    points.append(points[0])

    return np.array(points, dtype=np.float64)


def _create_cloud_path(
    half_w: float, half_h: float, num_bumps: int = 8
) -> NDArray[np.float64]:
    """Create cloud (thought) bubble path."""
    points = []

    bump_size = min(half_w, half_h) * 0.3

    for i in range(num_bumps):
        angle = 2 * np.pi * i / num_bumps

        base_x = half_w * 0.7 * np.cos(angle)
        base_y = half_h * 0.7 * np.sin(angle)

        for j in range(8):
            bump_angle = angle + (j / 8 - 0.5) * (2 * np.pi / num_bumps)
            bx = base_x + bump_size * np.cos(bump_angle + np.pi / 4)
            by = base_y + bump_size * np.sin(bump_angle + np.pi / 4)
            points.append([bx, by])

    points.append(points[0])

    return np.array(points, dtype=np.float64)


def create_tail_points(
    width: float,
    height: float,
    direction: str = "bottom-left",
    length: float = 30.0,
    tip_width: float = 20.0,
) -> NDArray[np.float64]:
    """Create speech bubble tail points.

    Args:
        width: Bubble width.
        height: Bubble height.
        direction: Tail direction ("bottom", "bottom-left", "bottom-right", "left", "right").
        length: Tail length.
        tip_width: Width at the base of the tail.

    Returns:
        Array of (x, y) points forming the tail triangle.
    """
    half_w = width / 2
    half_h = height / 2
    half_tip = tip_width / 2

    direction_offsets = {
        "bottom": (0, -half_h, 0, -half_h - length, half_tip, 0),
        "bottom-left": (-half_w * 0.3, -half_h, -half_w * 0.3 - length * 0.5, -half_h - length, half_tip, 0),
        "bottom-right": (half_w * 0.3, -half_h, half_w * 0.3 + length * 0.5, -half_h - length, half_tip, 0),
        "left": (-half_w, 0, -half_w - length, 0, 0, half_tip),
        "right": (half_w, 0, half_w + length, 0, 0, half_tip),
        "top": (0, half_h, 0, half_h + length, half_tip, 0),
        "top-left": (-half_w * 0.3, half_h, -half_w * 0.3 - length * 0.5, half_h + length, half_tip, 0),
        "top-right": (half_w * 0.3, half_h, half_w * 0.3 + length * 0.5, half_h + length, half_tip, 0),
    }

    if direction not in direction_offsets:
        return np.zeros((0, 2), dtype=np.float64)

    base_x, base_y, tip_x, tip_y, dx, dy = direction_offsets[direction]

    if length <= 0:
        return np.zeros((0, 2), dtype=np.float64)

    return np.array(
        [
            [base_x - dx, base_y - dy],
            [tip_x, tip_y],
            [base_x + dx, base_y + dy],
        ],
        dtype=np.float64,
    )


def bezier_curve(
    p0: tuple[float, float],
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    num_points: int = 10,
) -> NDArray[np.float64]:
    """Generate cubic bezier curve points.

    Args:
        p0: Start point.
        p1: First control point.
        p2: Second control point.
        p3: End point.
        num_points: Number of points to generate.

    Returns:
        Array of (x, y) points along the curve.
    """
    t = np.linspace(0, 1, num_points).reshape(-1, 1)

    p0_arr = np.array(p0)
    p1_arr = np.array(p1)
    p2_arr = np.array(p2)
    p3_arr = np.array(p3)

    points = (
        (1 - t) ** 3 * p0_arr
        + 3 * (1 - t) ** 2 * t * p1_arr
        + 3 * (1 - t) * t**2 * p2_arr
        + t**3 * p3_arr
    )

    return np.array(points, dtype=np.float64)
