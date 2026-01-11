"""Bezier curve utilities for bubble shapes."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def create_bubble_path(
    width: float,
    height: float,
    style: str = "speech",
    corner_radius: float = 20.0,
    corner_radii: tuple[float, float, float, float] | None = None,
    wobble: float = 0.0,
    wobble_mode: str = "random",
    num_points_per_segment: int = 8,
) -> NDArray[np.float64]:
    """Create bubble outline path.

    Args:
        width: Bubble width.
        height: Bubble height.
        style: Bubble style ("speech", "thought", "shout", "whisper", "narrator").
        corner_radius: Corner rounding radius (used if corner_radii is None).
        corner_radii: Per-corner radii as (top-right, bottom-right, bottom-left, top-left).
        wobble: Wobble intensity factor (0-1).
        wobble_mode: Wobble style - "random" for noise, "wave" for sine wave oscillation.
        num_points_per_segment: Points per curve segment.

    Returns:
        Array of (x, y) points forming the bubble outline.
    """
    half_w = width / 2
    half_h = height / 2

    # Calculate effective corner radii
    max_radius = min(half_w, half_h)
    if corner_radii is not None:
        radii = tuple(min(r, max_radius) for r in corner_radii)
    else:
        r = min(corner_radius, max_radius)
        radii = (r, r, r, r)

    if style == "narrator":
        return _create_rectangle_path(half_w, half_h)

    if style == "shout":
        return _create_spiky_path(half_w, half_h, num_spikes=12)

    if style == "thought":
        return _create_cloud_path(half_w, half_h, num_bumps=8)

    points = _create_rounded_rect_path_multi(half_w, half_h, radii, num_points_per_segment)

    if wobble > 0:
        points = _apply_wobble(points, wobble, wobble_mode)

    return points


def _apply_wobble(
    points: NDArray[np.float64],
    wobble: float,
    mode: str = "random",
) -> NDArray[np.float64]:
    """Apply wobble effect to path points.

    Args:
        points: Array of (x, y) points.
        wobble: Wobble intensity (0-1).
        mode: Wobble style - "random" or "wave".

    Returns:
        Modified points array with wobble applied.
    """
    if mode == "wave":
        # Sine wave wobble - creates a rhythmic oscillation
        num_points = len(points)
        wave_freq = 3.0  # Number of wave cycles
        wave_amp = wobble * 3.0

        # Calculate angle from center for each point
        angles = np.arctan2(points[:, 1], points[:, 0])
        wave = wave_amp * np.sin(wave_freq * angles * 2)

        # Apply wave perpendicular to the outline
        normals = np.column_stack([np.cos(angles), np.sin(angles)])
        points = points + normals * wave.reshape(-1, 1)
    else:
        # Random noise wobble
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
    return _create_rounded_rect_path_multi(half_w, half_h, (radius, radius, radius, radius), num_points)


def _create_rounded_rect_path_multi(
    half_w: float,
    half_h: float,
    radii: tuple[float, float, float, float],
    num_points: int,
) -> NDArray[np.float64]:
    """Create rounded rectangle path with per-corner radii.

    Args:
        half_w: Half width of the rectangle.
        half_h: Half height of the rectangle.
        radii: Corner radii as (top-right, bottom-right, bottom-left, top-left).
        num_points: Points per corner arc.

    Returns:
        Array of (x, y) points forming the rounded rectangle.
    """
    tr, br, bl, tl = radii
    points = []

    # Top-right corner
    cx, cy = half_w - tr, -half_h + tr
    angles = np.linspace(-np.pi / 2, 0, num_points)
    for angle in angles:
        x = cx + tr * np.cos(angle)
        y = cy + tr * np.sin(angle)
        points.append([x, y])

    # Bottom-right corner
    cx, cy = half_w - br, half_h - br
    angles = np.linspace(0, np.pi / 2, num_points)
    for angle in angles:
        x = cx + br * np.cos(angle)
        y = cy + br * np.sin(angle)
        points.append([x, y])

    # Bottom-left corner
    cx, cy = -half_w + bl, half_h - bl
    angles = np.linspace(np.pi / 2, np.pi, num_points)
    for angle in angles:
        x = cx + bl * np.cos(angle)
        y = cy + bl * np.sin(angle)
        points.append([x, y])

    # Top-left corner
    cx, cy = -half_w + tl, -half_h + tl
    angles = np.linspace(np.pi, 3 * np.pi / 2, num_points)
    for angle in angles:
        x = cx + tl * np.cos(angle)
        y = cy + tl * np.sin(angle)
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
