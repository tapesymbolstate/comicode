"""Utils module - utility functions for Comix."""

from comix.utils.bezier import create_bubble_path, create_tail_points
from comix.utils.geometry import (
    rotate_point,
    rotate_points,
    translate_points,
    scale_points,
    distance,
    midpoint,
    bounding_box,
    normalize_angle,
    angle_between,
)
from comix.utils.script_loader import (
    ScriptLoadError,
    load_script_module,
    find_page_in_module,
    load_page_from_script,
)

__all__ = [
    "create_bubble_path",
    "create_tail_points",
    "rotate_point",
    "rotate_points",
    "translate_points",
    "scale_points",
    "distance",
    "midpoint",
    "bounding_box",
    "normalize_angle",
    "angle_between",
    "ScriptLoadError",
    "load_script_module",
    "find_page_in_module",
    "load_page_from_script",
]
