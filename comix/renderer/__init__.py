"""Renderer module - output rendering backends."""

from comix.renderer.svg_renderer import SVGRenderer
from comix.renderer.html_renderer import HTMLRenderer

# CairoRenderer requires optional dependencies
try:
    from comix.renderer.cairo_renderer import CairoRenderer
except ImportError:
    CairoRenderer = None  # type: ignore[assignment, misc]

__all__ = ["SVGRenderer", "CairoRenderer", "HTMLRenderer"]
