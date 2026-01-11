"""Flow layout for automatic positioning of comic elements."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

if TYPE_CHECKING:
    from comix.cobject.cobject import CObject


Direction = Literal["horizontal", "vertical"]
Alignment = Literal["start", "center", "end"]
WrapMode = Literal["wrap", "nowrap"]

# Type aliases for clarity
RowItem = tuple[int, float, float]  # (index, width, height)
Row = tuple[list[RowItem], float]  # (items, max_height)
Column = tuple[list[RowItem], float]  # (items, max_width)


class FlowLayout:
    """Flow-based layout for automatic positioning.

    Unlike GridLayout which divides space equally, FlowLayout respects
    each object's natural dimensions and flows them horizontally or
    vertically with optional wrapping.

    Example:
        layout = FlowLayout(
            width=800,
            height=600,
            direction="horizontal",
            spacing=10,
            wrap="wrap",
            alignment="center",
        )
        positions = layout.calculate_positions_for_objects(panels)
    """

    def __init__(
        self,
        width: float = 800.0,
        height: float = 1200.0,
        direction: Direction = "horizontal",
        spacing: float = 10.0,
        wrap: WrapMode = "wrap",
        alignment: Alignment = "start",
        cross_alignment: Alignment = "start",
        offset_x: float = 0.0,
        offset_y: float = 0.0,
    ) -> None:
        """Initialize flow layout.

        Args:
            width: Available width for layout.
            height: Available height for layout.
            direction: Flow direction ("horizontal" or "vertical").
            spacing: Space between items.
            wrap: Whether to wrap to next line ("wrap" or "nowrap").
            alignment: Alignment along main axis ("start", "center", "end").
            cross_alignment: Alignment along cross axis ("start", "center", "end").
            offset_x: Starting X offset.
            offset_y: Starting Y offset.
        """
        self.width = width
        self.height = height
        self.direction = direction
        self.spacing = spacing
        self.wrap = wrap
        self.alignment = alignment
        self.cross_alignment = cross_alignment
        self.offset_x = offset_x
        self.offset_y = offset_y

    def calculate_positions(
        self, num_cells: int | None = None
    ) -> list[dict[str, Any]]:
        """Calculate positions assuming equal-sized cells.

        This method provides compatibility with GridLayout interface.
        For variable-sized objects, use calculate_positions_for_objects().

        Args:
            num_cells: Number of cells to position.

        Returns:
            List of position dictionaries.
        """
        if num_cells is None or num_cells == 0:
            return []

        # For equal-sized mode, calculate cell size to fit all items
        if self.direction == "horizontal":
            if self.wrap == "wrap":
                # Estimate reasonable cell size
                cell_width = min(
                    200.0, (self.width - (num_cells - 1) * self.spacing) / num_cells
                )
                cell_height = 200.0
            else:
                cell_width = (self.width - (num_cells - 1) * self.spacing) / num_cells
                cell_height = self.height
        else:
            if self.wrap == "wrap":
                cell_width = 200.0
                cell_height = min(
                    200.0, (self.height - (num_cells - 1) * self.spacing) / num_cells
                )
            else:
                cell_width = self.width
                cell_height = (self.height - (num_cells - 1) * self.spacing) / num_cells

        # Create dummy size list
        sizes = [(cell_width, cell_height) for _ in range(num_cells)]
        return self._calculate_positions_with_sizes(sizes)

    def calculate_positions_for_objects(
        self, objects: list[CObject]
    ) -> list[dict[str, Any]]:
        """Calculate positions for objects respecting their dimensions.

        Args:
            objects: List of CObjects to position.

        Returns:
            List of position dictionaries with center_x, center_y, width, height.
        """
        if not objects:
            return []

        sizes: list[tuple[float, float]] = []
        for obj in objects:
            width = getattr(obj, "width", None)
            height = getattr(obj, "height", None)

            # Fallback to bounding box if no direct width/height
            if width is None or height is None:
                try:
                    w = obj.get_width()
                    h = obj.get_height()
                    width = width if width is not None else w
                    height = height if height is not None else h
                except (AttributeError, ValueError):
                    width = width if width is not None else 100.0
                    height = height if height is not None else 100.0

            sizes.append((width, height))

        return self._calculate_positions_with_sizes(sizes)

    def _calculate_positions_with_sizes(
        self, sizes: list[tuple[float, float]]
    ) -> list[dict[str, Any]]:
        """Calculate positions given a list of (width, height) sizes.

        Args:
            sizes: List of (width, height) tuples.

        Returns:
            List of position dictionaries.
        """
        if not sizes:
            return []

        if self.direction == "horizontal":
            return self._flow_horizontal(sizes)
        else:
            return self._flow_vertical(sizes)

    def _flow_horizontal(
        self, sizes: list[tuple[float, float]]
    ) -> list[dict[str, Any]]:
        """Flow items horizontally with optional wrapping.

        Args:
            sizes: List of (width, height) tuples.

        Returns:
            List of position dictionaries.
        """
        positions: list[dict[str, Any]] = []
        rows: list[Row] = []
        current_row: list[RowItem] = []
        current_x = 0.0
        row_max_height = 0.0

        # Group items into rows
        for i, (w, h) in enumerate(sizes):
            if self.wrap == "wrap" and current_row:
                # Check if adding this item would exceed width
                needed = current_x + w
                if needed > self.width:
                    # Start new row
                    rows.append((current_row, row_max_height))
                    current_row = []
                    current_x = 0.0
                    row_max_height = 0.0

            current_row.append((i, w, h))
            current_x += w + self.spacing
            row_max_height = max(row_max_height, h)

        # Don't forget the last row
        if current_row:
            rows.append((current_row, row_max_height))

        # Calculate positions for each row
        current_y = 0.0
        for row_idx, (row_items, row_height) in enumerate(rows):
            # Calculate total width of row
            row_width = (
                sum(w for _, w, _ in row_items) + (len(row_items) - 1) * self.spacing
            )

            # Calculate starting x based on alignment
            if self.alignment == "start":
                start_x = 0.0
            elif self.alignment == "center":
                start_x = (self.width - row_width) / 2
            else:  # end
                start_x = self.width - row_width

            # Position items in row
            x = start_x
            for idx, w, h in row_items:
                # Calculate y based on cross alignment within row
                if self.cross_alignment == "start":
                    item_y = current_y + h / 2
                elif self.cross_alignment == "center":
                    item_y = current_y + row_height / 2
                else:  # end
                    item_y = current_y + row_height - h / 2

                positions.append(
                    {
                        "index": idx,
                        "center_x": self.offset_x + x + w / 2,
                        "center_y": self.offset_y + item_y,
                        "width": w,
                        "height": h,
                        "row": row_idx,
                    }
                )
                x += w + self.spacing

            current_y += row_height + self.spacing

        # Sort by original index and remove index field
        positions.sort(key=lambda p: p["index"])
        for p in positions:
            del p["index"]

        return positions

    def _flow_vertical(
        self, sizes: list[tuple[float, float]]
    ) -> list[dict[str, Any]]:
        """Flow items vertically with optional wrapping.

        Args:
            sizes: List of (width, height) tuples.

        Returns:
            List of position dictionaries.
        """
        positions: list[dict[str, Any]] = []
        columns: list[Column] = []
        current_column: list[RowItem] = []
        current_y = 0.0
        col_max_width = 0.0

        # Group items into columns
        for i, (w, h) in enumerate(sizes):
            if self.wrap == "wrap" and current_column:
                # Check if adding this item would exceed height
                needed = current_y + h
                if needed > self.height:
                    # Start new column
                    columns.append((current_column, col_max_width))
                    current_column = []
                    current_y = 0.0
                    col_max_width = 0.0

            current_column.append((i, w, h))
            current_y += h + self.spacing
            col_max_width = max(col_max_width, w)

        # Don't forget the last column
        if current_column:
            columns.append((current_column, col_max_width))

        # Calculate positions for each column
        current_x = 0.0
        for col_idx, (col_items, col_width) in enumerate(columns):
            # Calculate total height of column
            col_height = (
                sum(h for _, _, h in col_items) + (len(col_items) - 1) * self.spacing
            )

            # Calculate starting y based on alignment
            if self.alignment == "start":
                start_y = 0.0
            elif self.alignment == "center":
                start_y = (self.height - col_height) / 2
            else:  # end
                start_y = self.height - col_height

            # Position items in column
            y = start_y
            for idx, w, h in col_items:
                # Calculate x based on cross alignment within column
                if self.cross_alignment == "start":
                    item_x = current_x + w / 2
                elif self.cross_alignment == "center":
                    item_x = current_x + col_width / 2
                else:  # end
                    item_x = current_x + col_width - w / 2

                positions.append(
                    {
                        "index": idx,
                        "center_x": self.offset_x + item_x,
                        "center_y": self.offset_y + y + h / 2,
                        "width": w,
                        "height": h,
                        "col": col_idx,
                    }
                )
                y += h + self.spacing

            current_x += col_width + self.spacing

        # Sort by original index and remove index field
        positions.sort(key=lambda p: p["index"])
        for p in positions:
            del p["index"]

        return positions
