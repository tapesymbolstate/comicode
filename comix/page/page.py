"""Page - Comic page composition (Scene equivalent from Manim)."""

from __future__ import annotations

from pathlib import Path
from typing import Self

from comix.cobject.cobject import CObject
from comix.cobject.panel.panel import Panel
from comix.layout.grid import GridLayout


class Page:
    """Comic page - the main composition class.

    This is the equivalent of Manim's Scene class. A Page contains
    panels and other visual elements, manages layout, and handles rendering.
    """

    def __init__(
        self,
        width: float = 800.0,
        height: float = 1200.0,
        background_color: str = "#FFFFFF",
        margin: float = 20.0,
        gutter: float = 10.0,
    ) -> None:
        self.width = width
        self.height = height
        self.background_color = background_color
        self.margin = margin
        self.gutter = gutter

        self._panels: list[Panel] = []
        self._cobjects: list[CObject] = []
        self._layout: GridLayout | None = None

    def add(self, *cobjects: CObject) -> Self:
        """Add CObjects to the page."""
        for obj in cobjects:
            if isinstance(obj, Panel):
                self._panels.append(obj)
            self._cobjects.append(obj)
        return self

    def remove(self, *cobjects: CObject) -> Self:
        """Remove CObjects from the page."""
        for obj in cobjects:
            if obj in self._panels:
                self._panels.remove(obj)
            if obj in self._cobjects:
                self._cobjects.remove(obj)
        return self

    def set_layout(self, rows: int, cols: int) -> Self:
        """Set grid layout for panels."""
        self._layout = GridLayout(
            rows=rows,
            cols=cols,
            width=self.width - 2 * self.margin,
            height=self.height - 2 * self.margin,
            gutter=self.gutter,
        )
        return self

    def auto_layout(self) -> Self:
        """Apply automatic layout to panels."""
        if self._layout and self._panels:
            positions = self._layout.calculate_positions(len(self._panels))
            for panel, pos in zip(self._panels, positions):
                panel.move_to((pos["center_x"], pos["center_y"]))
                panel.width = pos["width"]
                panel.height = pos["height"]
                panel.generate_points()
        return self

    def build(self) -> None:
        """Build the page content. Override in subclasses."""
        pass

    def render(
        self,
        output_path: str = "output.svg",
        format: str | None = None,
        quality: str = "medium",
    ) -> str:
        """Render the page to a file.

        Args:
            output_path: Output file path.
            format: Output format ("svg", "png", "pdf"). Auto-detected from path if None.
            quality: Rendering quality ("low", "medium", "high").

        Returns:
            Path to the rendered file.
        """
        self.build()
        self.auto_layout()

        if format is None:
            format = Path(output_path).suffix.lstrip(".") or "svg"

        if format == "svg":
            from comix.renderer.svg_renderer import SVGRenderer

            renderer = SVGRenderer(self)
            return renderer.render(output_path)
        else:
            raise NotImplementedError(f"Format '{format}' not yet implemented")

    def show(self) -> None:
        """Preview the page in a web browser."""
        import tempfile
        import webbrowser

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            path = self.render(f.name, format="svg")
            webbrowser.open(f"file://{path}")

    def get_all_cobjects(self) -> list[CObject]:
        """Get all CObjects including nested ones."""
        all_objects: list[CObject] = []
        for obj in self._cobjects:
            all_objects.extend(obj.get_family())
        return all_objects

    def get_render_data(self) -> dict:
        """Get data for rendering."""
        return {
            "width": self.width,
            "height": self.height,
            "background_color": self.background_color,
            "margin": self.margin,
            "gutter": self.gutter,
            "cobjects": [obj.get_render_data() for obj in self._cobjects],
        }


class SinglePanel(Page):
    """Single panel comic."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._main_panel = Panel(
            width=self.width - 2 * self.margin,
            height=self.height - 2 * self.margin,
        )
        self._main_panel.move_to((self.width / 2, self.height / 2))
        self.add(self._main_panel)

    @property
    def panel(self) -> Panel:
        """Get the main panel."""
        return self._main_panel


class Strip(Page):
    """Horizontal or vertical comic strip."""

    def __init__(
        self,
        panels: int = 4,
        direction: str = "horizontal",
        **kwargs,
    ) -> None:
        if direction == "horizontal":
            kwargs.setdefault("width", 1200.0)
            kwargs.setdefault("height", 300.0)
        else:
            kwargs.setdefault("width", 300.0)
            kwargs.setdefault("height", 1200.0)

        super().__init__(**kwargs)

        self.direction = direction
        self.num_panels = panels

        if direction == "horizontal":
            self.set_layout(rows=1, cols=panels)
        else:
            self.set_layout(rows=panels, cols=1)

        for i in range(panels):
            self.add(Panel(name=f"Panel_{i + 1}"))
