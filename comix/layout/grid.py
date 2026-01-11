"""Grid layout for comic panels."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CellPosition:
    """Position and size of a grid cell."""

    center_x: float
    center_y: float
    width: float
    height: float
    row: int
    col: int


class GridLayout:
    """Grid-based layout for arranging panels.

    Divides the available space into a grid of rows and columns,
    with configurable gutters between cells.
    """

    def __init__(
        self,
        rows: int = 1,
        cols: int = 1,
        width: float = 800.0,
        height: float = 1200.0,
        gutter: float = 10.0,
        offset_x: float = 0.0,
        offset_y: float = 0.0,
    ) -> None:
        self.rows = max(1, rows)
        self.cols = max(1, cols)
        self.width = width
        self.height = height
        self.gutter = gutter
        self.offset_x = offset_x
        self.offset_y = offset_y

    def calculate_positions(self, num_cells: int | None = None) -> list[dict]:
        """Calculate positions for all cells in the grid.

        Args:
            num_cells: Number of cells to calculate. If None, calculates all.

        Returns:
            List of position dictionaries with center, width, height, row, col.
        """
        total_gutter_width = (self.cols - 1) * self.gutter
        total_gutter_height = (self.rows - 1) * self.gutter

        cell_width = (self.width - total_gutter_width) / self.cols
        cell_height = (self.height - total_gutter_height) / self.rows

        positions = []
        cells_needed = num_cells if num_cells else self.rows * self.cols

        for i in range(cells_needed):
            row = i // self.cols
            col = i % self.cols

            if row >= self.rows:
                break

            center_x = (
                self.offset_x
                + col * (cell_width + self.gutter)
                + cell_width / 2
            )
            center_y = (
                self.offset_y
                + row * (cell_height + self.gutter)
                + cell_height / 2
            )

            positions.append(
                {
                    "center_x": center_x,
                    "center_y": center_y,
                    "width": cell_width,
                    "height": cell_height,
                    "row": row,
                    "col": col,
                }
            )

        return positions

    def get_cell(self, row: int, col: int) -> dict:
        """Get position data for a specific cell."""
        total_gutter_width = (self.cols - 1) * self.gutter
        total_gutter_height = (self.rows - 1) * self.gutter

        cell_width = (self.width - total_gutter_width) / self.cols
        cell_height = (self.height - total_gutter_height) / self.rows

        center_x = (
            self.offset_x
            + col * (cell_width + self.gutter)
            + cell_width / 2
        )
        center_y = (
            self.offset_y
            + row * (cell_height + self.gutter)
            + cell_height / 2
        )

        return {
            "center_x": center_x,
            "center_y": center_y,
            "width": cell_width,
            "height": cell_height,
            "row": row,
            "col": col,
        }
