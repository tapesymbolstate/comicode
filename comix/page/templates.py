"""Panel Templates - Pre-built comic page layouts.

Common comic and manga page layouts for rapid comic creation.
These templates provide standard panel arrangements used in
professional comics, manga, and webtoons.
"""

from __future__ import annotations

from typing import Any, Self

from comix.cobject.panel.panel import Panel
from comix.page.page import Page


class FourKoma(Page):
    """Traditional Japanese 4-panel vertical comic (4-koma/yon-koma).

    A classic manga format featuring 4 equal panels stacked vertically.
    Commonly used for gag manga and newspaper comic strips.

    The standard dimensions are 300x1200 (portrait) but can be customized.

    Example:
        >>> comic = FourKoma()
        >>> comic.panels[0].add_content(character.say("Setup"))
        >>> comic.panels[1].add_content(character.say("Development"))
        >>> comic.panels[2].add_content(character.say("Turn"))
        >>> comic.panels[3].add_content(character.say("Punchline"))
        >>> comic.render("4koma.svg")
    """

    def __init__(self, **kwargs: Any) -> None:
        """Initialize a 4-koma layout.

        Args:
            **kwargs: Page parameters (width, height, margin, gutter, etc.)
        """
        kwargs.setdefault("width", 300.0)
        kwargs.setdefault("height", 1200.0)
        super().__init__(**kwargs)

        # Set 4x1 grid layout
        self.set_layout(rows=4, cols=1)

        # Create 4 panels with semantic names
        panel_names = ["setup", "development", "turn", "punchline"]
        for name in panel_names:
            self.add(Panel(name=name))

    @property
    def panels(self) -> list[Panel]:
        """Get all four panels in order (top to bottom)."""
        return list(self._panels)

    @property
    def setup(self) -> Panel:
        """Get the first panel (setup/introduction)."""
        return self._panels[0]

    @property
    def development(self) -> Panel:
        """Get the second panel (development)."""
        return self._panels[1]

    @property
    def turn(self) -> Panel:
        """Get the third panel (turn/twist)."""
        return self._panels[2]

    @property
    def punchline(self) -> Panel:
        """Get the fourth panel (punchline/conclusion)."""
        return self._panels[3]


class SplashPage(Page):
    """Full-page splash panel with optional header area.

    Used for dramatic scenes, title pages, and establishing shots.
    The splash panel fills the entire page, with an optional header
    area at the top for titles or chapter headings.

    Example:
        >>> page = SplashPage()
        >>> page.splash.add_content(background_image)
        >>> page.render("splash.svg")

        >>> # With header
        >>> page = SplashPage(header_height=100)
        >>> page.header.add_content(title_text)
        >>> page.splash.add_content(dramatic_scene)
    """

    def __init__(
        self,
        header_height: float = 0.0,
        **kwargs: Any,
    ) -> None:
        """Initialize a splash page.

        Args:
            header_height: Height of optional header area (0 for no header).
            **kwargs: Page parameters (width, height, margin, gutter, etc.)
        """
        super().__init__(**kwargs)

        self._header_height = header_height
        self._header_panel: Panel | None = None

        content_width = self.width - 2 * self.margin
        content_height = self.height - 2 * self.margin

        if header_height > 0:
            # Create header panel
            self._header_panel = Panel(
                width=content_width,
                height=header_height,
                name="header",
            )
            self._header_panel.move_to((
                self.width / 2,
                self.margin + header_height / 2,
            ))
            self.add(self._header_panel)

            # Create splash panel below header
            splash_height = content_height - header_height - self.gutter
            self._splash_panel = Panel(
                width=content_width,
                height=splash_height,
                name="splash",
            )
            self._splash_panel.move_to((
                self.width / 2,
                self.margin + header_height + self.gutter + splash_height / 2,
            ))
        else:
            # Full-page splash
            self._splash_panel = Panel(
                width=content_width,
                height=content_height,
                name="splash",
            )
            self._splash_panel.move_to((self.width / 2, self.height / 2))

        self.add(self._splash_panel)

    @property
    def splash(self) -> Panel:
        """Get the main splash panel."""
        return self._splash_panel

    @property
    def header(self) -> Panel | None:
        """Get the header panel (None if no header)."""
        return self._header_panel

    def auto_layout(self) -> Self:
        """Override to skip grid layout (panels are pre-positioned)."""
        return self


class TwoByTwo(Page):
    """Classic 2x2 grid layout.

    A traditional western comic page layout with 4 equal panels
    arranged in a 2x2 grid. Good for standard narrative pacing.

    Example:
        >>> page = TwoByTwo()
        >>> page.top_left.add_content(scene_1)
        >>> page.top_right.add_content(scene_2)
        >>> page.bottom_left.add_content(scene_3)
        >>> page.bottom_right.add_content(scene_4)
    """

    def __init__(self, **kwargs: Any) -> None:
        """Initialize a 2x2 grid layout.

        Args:
            **kwargs: Page parameters (width, height, margin, gutter, etc.)
        """
        super().__init__(**kwargs)

        # Set 2x2 grid layout
        self.set_layout(rows=2, cols=2)

        # Create 4 panels with position-based names
        panel_names = ["top_left", "top_right", "bottom_left", "bottom_right"]
        for name in panel_names:
            self.add(Panel(name=name))

    @property
    def panels(self) -> list[Panel]:
        """Get all four panels in reading order."""
        return list(self._panels)

    @property
    def top_left(self) -> Panel:
        """Get the top-left panel."""
        return self._panels[0]

    @property
    def top_right(self) -> Panel:
        """Get the top-right panel."""
        return self._panels[1]

    @property
    def bottom_left(self) -> Panel:
        """Get the bottom-left panel."""
        return self._panels[2]

    @property
    def bottom_right(self) -> Panel:
        """Get the bottom-right panel."""
        return self._panels[3]


class WebComic(Page):
    """Vertical scroll format for webtoons and web comics.

    A tall, narrow format optimized for vertical scrolling on screens.
    Panels are stacked vertically with consistent width.

    Example:
        >>> comic = WebComic(panels=5)
        >>> for i, panel in enumerate(comic.panels):
        ...     panel.add_content(scenes[i])
        >>> comic.render("webtoon.svg")
    """

    def __init__(
        self,
        panels: int = 4,
        panel_height: float = 400.0,
        **kwargs: Any,
    ) -> None:
        """Initialize a web comic layout.

        Args:
            panels: Number of panels (stacked vertically).
            panel_height: Height of each panel.
            **kwargs: Page parameters (width, margin, gutter, etc.)
        """
        kwargs.setdefault("width", 800.0)
        # Calculate total height based on panels
        margin = kwargs.get("margin", 20.0)
        gutter = kwargs.get("gutter", 10.0)
        total_height = (
            2 * margin
            + panels * panel_height
            + (panels - 1) * gutter
        )
        kwargs.setdefault("height", total_height)

        super().__init__(**kwargs)

        self._panel_height = panel_height
        self.num_panels = panels

        # Set vertical grid layout
        self.set_layout(rows=panels, cols=1)

        # Create panels
        for i in range(panels):
            self.add(Panel(name=f"panel_{i + 1}"))

    @property
    def panels(self) -> list[Panel]:
        """Get all panels in order (top to bottom)."""
        return list(self._panels)


class ThreeRowLayout(Page):
    """Three-row manga page layout.

    A common manga layout with 3 horizontal rows. Each row can have
    different numbers of panels (e.g., 1 panel top, 2 middle, 1 bottom).

    Example:
        >>> page = ThreeRowLayout(row_panels=[1, 2, 1])
        >>> page.rows[0][0].add_content(establishing_shot)
        >>> page.rows[1][0].add_content(dialogue_1)
        >>> page.rows[1][1].add_content(dialogue_2)
        >>> page.rows[2][0].add_content(reaction)
    """

    def __init__(
        self,
        row_panels: list[int] | None = None,
        row_heights: list[float] | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize a three-row layout.

        Args:
            row_panels: Number of panels per row [top, middle, bottom].
                        Defaults to [1, 2, 1].
            row_heights: Height ratio of each row. Defaults to equal heights.
            **kwargs: Page parameters (width, height, margin, gutter, etc.)
        """
        super().__init__(**kwargs)

        if row_panels is None:
            row_panels = [1, 2, 1]

        if row_heights is None:
            row_heights = [1.0, 1.0, 1.0]

        self._row_panels = row_panels
        self._row_heights = row_heights
        self._rows: list[list[Panel]] = []

        # Calculate dimensions
        content_width = self.width - 2 * self.margin
        content_height = self.height - 2 * self.margin
        total_height_ratio = sum(row_heights)
        available_height = content_height - (len(row_panels) - 1) * self.gutter

        # Create panels for each row
        current_y = self.margin
        for row_idx, (num_panels, height_ratio) in enumerate(
            zip(row_panels, row_heights)
        ):
            row_height = available_height * (height_ratio / total_height_ratio)
            panel_width = (content_width - (num_panels - 1) * self.gutter) / num_panels

            row: list[Panel] = []
            for col_idx in range(num_panels):
                panel = Panel(
                    width=panel_width,
                    height=row_height,
                    name=f"row{row_idx + 1}_panel{col_idx + 1}",
                )
                panel_x = (
                    self.margin
                    + col_idx * (panel_width + self.gutter)
                    + panel_width / 2
                )
                panel_y = current_y + row_height / 2
                panel.move_to((panel_x, panel_y))
                self.add(panel)
                row.append(panel)

            self._rows.append(row)
            current_y += row_height + self.gutter

    @property
    def rows(self) -> list[list[Panel]]:
        """Get panels organized by row."""
        return self._rows

    @property
    def panels(self) -> list[Panel]:
        """Get all panels in reading order."""
        return list(self._panels)

    def auto_layout(self) -> Self:
        """Override to skip grid layout (panels are pre-positioned)."""
        return self


class MangaPage(Page):
    """Flexible manga page with common panel arrangements.

    Supports various manga panel configurations through presets or
    custom layouts. The "six_panel" preset is a common manga layout.

    Presets:
        - "six_panel": 2 rows of 3 panels (classic shounen manga)
        - "action": 1 large + 4 small panels (for action sequences)
        - "dialogue": 3 rows of 2 panels (for conversation scenes)

    Example:
        >>> page = MangaPage(preset="six_panel")
        >>> for panel in page.panels:
        ...     panel.add_content(content)

        >>> # Custom layout
        >>> page = MangaPage(rows=3, cols=2)
    """

    PRESETS = {
        "six_panel": {"rows": 2, "cols": 3},
        "dialogue": {"rows": 3, "cols": 2},
        "action": {"rows": 2, "cols": 2},  # Will be customized
    }

    def __init__(
        self,
        preset: str | None = None,
        rows: int | None = None,
        cols: int | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize a manga page.

        Args:
            preset: Layout preset name ("six_panel", "action", "dialogue").
            rows: Number of rows (overrides preset).
            cols: Number of columns (overrides preset).
            **kwargs: Page parameters (width, height, margin, gutter, etc.)
        """
        super().__init__(**kwargs)

        # Determine layout from preset or explicit values
        if preset and preset in self.PRESETS:
            layout = self.PRESETS[preset]
            rows = rows or layout["rows"]
            cols = cols or layout["cols"]
        else:
            rows = rows or 2
            cols = cols or 3

        self._preset = preset
        num_panels = rows * cols

        # Set grid layout
        self.set_layout(rows=rows, cols=cols)

        # Create panels
        for i in range(num_panels):
            row = i // cols
            col = i % cols
            self.add(Panel(name=f"panel_{row + 1}_{col + 1}"))

    @property
    def panels(self) -> list[Panel]:
        """Get all panels in reading order."""
        return list(self._panels)


class ActionPage(Page):
    """Action-focused page with one large panel and smaller panels.

    Designed for action sequences where one panel dominates the page
    (for the main action) while smaller panels provide context or reactions.

    The main panel takes up the top half of the page, with smaller
    panels arranged below.

    Example:
        >>> page = ActionPage(small_panels=3)
        >>> page.main.add_content(action_scene)
        >>> for i, panel in enumerate(page.small):
        ...     panel.add_content(reactions[i])
    """

    def __init__(
        self,
        small_panels: int = 3,
        main_ratio: float = 0.6,
        **kwargs: Any,
    ) -> None:
        """Initialize an action page.

        Args:
            small_panels: Number of small panels below the main panel.
            main_ratio: Ratio of page height for main panel (0.0-1.0).
            **kwargs: Page parameters (width, height, margin, gutter, etc.)
        """
        super().__init__(**kwargs)

        self._small_panel_count = small_panels
        self._main_ratio = main_ratio

        content_width = self.width - 2 * self.margin
        content_height = self.height - 2 * self.margin

        # Main panel height
        main_height = (content_height - self.gutter) * main_ratio
        small_height = content_height - main_height - self.gutter

        # Create main panel
        self._main_panel = Panel(
            width=content_width,
            height=main_height,
            name="main",
        )
        self._main_panel.move_to((
            self.width / 2,
            self.margin + main_height / 2,
        ))
        self.add(self._main_panel)

        # Create small panels
        small_width = (content_width - (small_panels - 1) * self.gutter) / small_panels
        self._small_panels: list[Panel] = []

        for i in range(small_panels):
            panel = Panel(
                width=small_width,
                height=small_height,
                name=f"small_{i + 1}",
            )
            panel_x = (
                self.margin
                + i * (small_width + self.gutter)
                + small_width / 2
            )
            panel_y = self.margin + main_height + self.gutter + small_height / 2
            panel.move_to((panel_x, panel_y))
            self.add(panel)
            self._small_panels.append(panel)

    @property
    def main(self) -> Panel:
        """Get the main (large) panel."""
        return self._main_panel

    @property
    def small(self) -> list[Panel]:
        """Get the small panels."""
        return self._small_panels

    @property
    def panels(self) -> list[Panel]:
        """Get all panels (main first, then small)."""
        return list(self._panels)

    def auto_layout(self) -> Self:
        """Override to skip grid layout (panels are pre-positioned)."""
        return self
