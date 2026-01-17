"""Tests for layout classes."""

import pytest

from comix.layout.flow import FlowLayout
from comix.layout.grid import GridLayout
from comix.cobject.panel.panel import Panel
from comix.page.page import Page


class TestGridLayout:
    """Tests for GridLayout class."""

    def test_default_init(self):
        """Test default initialization."""
        layout = GridLayout()
        assert layout.rows == 1
        assert layout.cols == 1
        assert layout.width == 800.0
        assert layout.height == 1200.0
        assert layout.gutter == 10.0
        assert layout.offset_x == 0.0
        assert layout.offset_y == 0.0

    def test_custom_init(self):
        """Test custom initialization."""
        layout = GridLayout(
            rows=3,
            cols=4,
            width=1000.0,
            height=800.0,
            gutter=20.0,
            offset_x=10.0,
            offset_y=15.0,
        )
        assert layout.rows == 3
        assert layout.cols == 4
        assert layout.width == 1000.0
        assert layout.height == 800.0
        assert layout.gutter == 20.0
        assert layout.offset_x == 10.0
        assert layout.offset_y == 15.0

    def test_calculate_positions_2x2(self):
        """Test calculating positions for a 2x2 grid."""
        layout = GridLayout(
            rows=2,
            cols=2,
            width=400.0,
            height=400.0,
            gutter=0.0,
        )
        positions = layout.calculate_positions(4)

        assert len(positions) == 4

        # Check cell dimensions
        for pos in positions:
            assert pos["width"] == 200.0
            assert pos["height"] == 200.0

        # Check positions (centers)
        assert positions[0]["center_x"] == 100.0
        assert positions[0]["center_y"] == 100.0
        assert positions[1]["center_x"] == 300.0
        assert positions[1]["center_y"] == 100.0
        assert positions[2]["center_x"] == 100.0
        assert positions[2]["center_y"] == 300.0
        assert positions[3]["center_x"] == 300.0
        assert positions[3]["center_y"] == 300.0

    def test_calculate_positions_with_gutter(self):
        """Test positions with gutters."""
        layout = GridLayout(
            rows=2,
            cols=2,
            width=410.0,
            height=410.0,
            gutter=10.0,
        )
        positions = layout.calculate_positions(4)

        # Cell size: (410 - 10) / 2 = 200
        assert positions[0]["width"] == 200.0
        assert positions[0]["height"] == 200.0

    def test_get_cell(self):
        """Test getting a specific cell."""
        layout = GridLayout(
            rows=3,
            cols=3,
            width=300.0,
            height=300.0,
            gutter=0.0,
        )
        cell = layout.get_cell(1, 1)

        assert cell["row"] == 1
        assert cell["col"] == 1
        assert cell["center_x"] == 150.0
        assert cell["center_y"] == 150.0


class TestGridLayoutEdgeCases:
    """Edge case tests for GridLayout class."""

    def test_zero_rows_cols_enforces_minimum(self):
        """Test that zero rows/cols are enforced to minimum of 1."""
        layout = GridLayout(rows=0, cols=0)
        assert layout.rows == 1
        assert layout.cols == 1

    def test_negative_rows_cols_enforces_minimum(self):
        """Test that negative rows/cols are enforced to minimum of 1."""
        layout = GridLayout(rows=-5, cols=-3)
        assert layout.rows == 1
        assert layout.cols == 1

    def test_single_cell_grid_positioning(self):
        """Test 1x1 grid positioning."""
        layout = GridLayout(
            rows=1,
            cols=1,
            width=200.0,
            height=300.0,
            gutter=0.0,
        )
        positions = layout.calculate_positions(1)

        assert len(positions) == 1
        assert positions[0]["center_x"] == 100.0
        assert positions[0]["center_y"] == 150.0
        assert positions[0]["width"] == 200.0
        assert positions[0]["height"] == 300.0
        assert positions[0]["row"] == 0
        assert positions[0]["col"] == 0

    def test_single_cell_with_gutter(self):
        """Test 1x1 grid with gutter (gutter should not affect single cell)."""
        layout = GridLayout(
            rows=1,
            cols=1,
            width=200.0,
            height=300.0,
            gutter=50.0,
        )
        positions = layout.calculate_positions(1)

        # Gutter only applies between cells, so single cell gets full size
        assert positions[0]["width"] == 200.0
        assert positions[0]["height"] == 300.0

    def test_single_cell_with_offset(self):
        """Test 1x1 grid with offsets."""
        layout = GridLayout(
            rows=1,
            cols=1,
            width=100.0,
            height=100.0,
            gutter=0.0,
            offset_x=50.0,
            offset_y=25.0,
        )
        positions = layout.calculate_positions(1)

        assert positions[0]["center_x"] == 100.0  # 50 + 50
        assert positions[0]["center_y"] == 75.0  # 25 + 50

    def test_large_grid_dimensions(self):
        """Test grid with many rows and columns (100x100)."""
        layout = GridLayout(
            rows=100,
            cols=100,
            width=10000.0,
            height=10000.0,
            gutter=0.0,
        )
        positions = layout.calculate_positions(100)  # Only first 100 cells

        assert len(positions) == 100
        # Cell size should be 100x100
        assert positions[0]["width"] == 100.0
        assert positions[0]["height"] == 100.0
        # Last cell in first row
        assert positions[99]["row"] == 0
        assert positions[99]["col"] == 99

    def test_very_large_grid_with_all_cells(self):
        """Test grid with 50x50 = 2500 cells."""
        layout = GridLayout(
            rows=50,
            cols=50,
            width=5000.0,
            height=5000.0,
            gutter=0.0,
        )
        positions = layout.calculate_positions()  # All cells

        assert len(positions) == 2500
        # Verify last cell position
        last = positions[-1]
        assert last["row"] == 49
        assert last["col"] == 49

    def test_calculate_positions_zero_cells_treated_as_all(self):
        """Test that zero num_cells is treated as falsy and returns all cells.

        Note: The implementation uses `num_cells if num_cells else ...`,
        so 0 is treated as None (falsy) and returns all cells.
        """
        layout = GridLayout(rows=3, cols=3, width=300.0, height=300.0)
        positions = layout.calculate_positions(0)

        # 0 is falsy, so treated same as None - returns all 9 cells
        assert len(positions) == 9

    def test_calculate_positions_none_returns_all(self):
        """Test None num_cells returns all cells."""
        layout = GridLayout(rows=2, cols=3, width=300.0, height=200.0, gutter=0.0)
        positions = layout.calculate_positions(None)

        assert len(positions) == 6

    def test_calculate_positions_more_than_available(self):
        """Test requesting more cells than available stops at grid bounds."""
        layout = GridLayout(rows=2, cols=2, width=200.0, height=200.0, gutter=0.0)
        positions = layout.calculate_positions(10)  # Only 4 cells exist

        assert len(positions) == 4

    def test_very_small_dimensions(self):
        """Test grid with very small dimensions."""
        layout = GridLayout(
            rows=2,
            cols=2,
            width=4.0,
            height=4.0,
            gutter=0.0,
        )
        positions = layout.calculate_positions(4)

        assert len(positions) == 4
        assert positions[0]["width"] == 2.0
        assert positions[0]["height"] == 2.0

    def test_zero_gutter(self):
        """Test grid with explicit zero gutter."""
        layout = GridLayout(
            rows=2,
            cols=2,
            width=200.0,
            height=200.0,
            gutter=0.0,
        )
        positions = layout.calculate_positions(4)

        # Cells should touch with no gap
        assert positions[0]["width"] == 100.0
        assert positions[1]["center_x"] - positions[0]["center_x"] == 100.0

    def test_large_gutter_relative_to_size(self):
        """Test grid where gutter is large relative to total size."""
        layout = GridLayout(
            rows=3,
            cols=3,
            width=100.0,
            height=100.0,
            gutter=20.0,  # 2 gutters = 40px, leaving 60px for 3 cells
        )
        positions = layout.calculate_positions(9)

        # Cell width = (100 - 40) / 3 = 20
        assert positions[0]["width"] == 20.0
        assert positions[0]["height"] == 20.0

    def test_negative_offset(self):
        """Test grid with negative offsets."""
        layout = GridLayout(
            rows=1,
            cols=1,
            width=100.0,
            height=100.0,
            gutter=0.0,
            offset_x=-50.0,
            offset_y=-25.0,
        )
        positions = layout.calculate_positions(1)

        assert positions[0]["center_x"] == 0.0  # -50 + 50
        assert positions[0]["center_y"] == 25.0  # -25 + 50

    def test_large_offset(self):
        """Test grid with offsets larger than page dimensions."""
        layout = GridLayout(
            rows=1,
            cols=1,
            width=100.0,
            height=100.0,
            gutter=0.0,
            offset_x=500.0,
            offset_y=300.0,
        )
        positions = layout.calculate_positions(1)

        # Cell will be positioned outside original bounds
        assert positions[0]["center_x"] == 550.0  # 500 + 50
        assert positions[0]["center_y"] == 350.0  # 300 + 50

    def test_get_cell_first_cell(self):
        """Test get_cell for first cell (0,0)."""
        layout = GridLayout(rows=3, cols=3, width=300.0, height=300.0, gutter=0.0)
        cell = layout.get_cell(0, 0)

        assert cell["row"] == 0
        assert cell["col"] == 0
        assert cell["center_x"] == 50.0
        assert cell["center_y"] == 50.0

    def test_get_cell_last_cell(self):
        """Test get_cell for last cell."""
        layout = GridLayout(rows=3, cols=3, width=300.0, height=300.0, gutter=0.0)
        cell = layout.get_cell(2, 2)

        assert cell["row"] == 2
        assert cell["col"] == 2
        assert cell["center_x"] == 250.0
        assert cell["center_y"] == 250.0

    def test_get_cell_with_gutter(self):
        """Test get_cell with gutters."""
        layout = GridLayout(
            rows=2,
            cols=2,
            width=210.0,
            height=210.0,
            gutter=10.0,
        )
        # Cell size = (210-10)/2 = 100
        cell = layout.get_cell(1, 1)

        assert cell["width"] == 100.0
        # center_x = 0 + 1*(100+10) + 50 = 160
        assert cell["center_x"] == 160.0

    def test_get_cell_out_of_bounds(self):
        """Test get_cell with indices beyond grid bounds (no validation)."""
        layout = GridLayout(rows=2, cols=2, width=200.0, height=200.0, gutter=0.0)
        # Note: GridLayout doesn't validate bounds, it calculates position anyway
        cell = layout.get_cell(5, 5)

        # Position will be calculated even though it's outside the grid
        assert cell["row"] == 5
        assert cell["col"] == 5

    def test_extreme_aspect_ratio_wide(self):
        """Test grid with extreme width:height ratio."""
        layout = GridLayout(
            rows=1,
            cols=10,
            width=1000.0,
            height=10.0,
            gutter=0.0,
        )
        positions = layout.calculate_positions(10)

        assert len(positions) == 10
        # Each cell: 100x10
        assert positions[0]["width"] == 100.0
        assert positions[0]["height"] == 10.0

    def test_extreme_aspect_ratio_tall(self):
        """Test grid with extreme height:width ratio."""
        layout = GridLayout(
            rows=10,
            cols=1,
            width=10.0,
            height=1000.0,
            gutter=0.0,
        )
        positions = layout.calculate_positions(10)

        assert len(positions) == 10
        # Each cell: 10x100
        assert positions[0]["width"] == 10.0
        assert positions[0]["height"] == 100.0

    def test_floating_point_dimensions(self):
        """Test grid with non-integer dimensions."""
        layout = GridLayout(
            rows=3,
            cols=3,
            width=100.7,
            height=100.3,
            gutter=0.5,
        )
        positions = layout.calculate_positions(9)

        assert len(positions) == 9
        # Cell width = (100.7 - 1.0) / 3 = 33.233...
        assert positions[0]["width"] == pytest.approx(33.2333, rel=1e-3)

    def test_cell_position_consistency(self):
        """Test that calculate_positions and get_cell return consistent results."""
        layout = GridLayout(
            rows=3,
            cols=4,
            width=400.0,
            height=300.0,
            gutter=5.0,
        )
        positions = layout.calculate_positions(12)

        for pos in positions:
            cell = layout.get_cell(pos["row"], pos["col"])
            assert cell["center_x"] == pytest.approx(pos["center_x"])
            assert cell["center_y"] == pytest.approx(pos["center_y"])
            assert cell["width"] == pytest.approx(pos["width"])
            assert cell["height"] == pytest.approx(pos["height"])


class TestFlowLayout:
    """Tests for FlowLayout class."""

    def test_default_init(self):
        """Test default initialization."""
        layout = FlowLayout()
        assert layout.width == 800.0
        assert layout.height == 1200.0
        assert layout.direction == "horizontal"
        assert layout.spacing == 10.0
        assert layout.wrap == "wrap"
        assert layout.alignment == "start"
        assert layout.cross_alignment == "start"
        assert layout.offset_x == 0.0
        assert layout.offset_y == 0.0

    def test_custom_init(self):
        """Test custom initialization."""
        layout = FlowLayout(
            width=1000.0,
            height=600.0,
            direction="vertical",
            spacing=20.0,
            wrap="nowrap",
            alignment="center",
            cross_alignment="end",
            offset_x=50.0,
            offset_y=30.0,
        )
        assert layout.width == 1000.0
        assert layout.height == 600.0
        assert layout.direction == "vertical"
        assert layout.spacing == 20.0
        assert layout.wrap == "nowrap"
        assert layout.alignment == "center"
        assert layout.cross_alignment == "end"
        assert layout.offset_x == 50.0
        assert layout.offset_y == 30.0

    def test_calculate_positions_empty(self):
        """Test with empty input."""
        layout = FlowLayout()
        assert layout.calculate_positions(0) == []
        assert layout.calculate_positions(None) == []

    def test_calculate_positions_for_objects_empty(self):
        """Test with empty object list."""
        layout = FlowLayout()
        assert layout.calculate_positions_for_objects([]) == []

    def test_horizontal_flow_nowrap(self):
        """Test horizontal flow without wrapping."""
        layout = FlowLayout(
            width=1000.0,
            height=100.0,
            direction="horizontal",
            spacing=10.0,
            wrap="nowrap",
            alignment="start",
        )

        panels = [Panel(width=100, height=100) for _ in range(3)]
        positions = layout.calculate_positions_for_objects(panels)

        assert len(positions) == 3

        # Check positions (start-aligned)
        assert positions[0]["center_x"] == 50.0
        assert positions[1]["center_x"] == 160.0  # 100 + 10 + 50
        assert positions[2]["center_x"] == 270.0  # 200 + 20 + 50

    def test_horizontal_flow_wrap(self):
        """Test horizontal flow with wrapping."""
        layout = FlowLayout(
            width=250.0,
            height=500.0,
            direction="horizontal",
            spacing=10.0,
            wrap="wrap",
            alignment="start",
        )

        panels = [Panel(width=100, height=100) for _ in range(5)]
        positions = layout.calculate_positions_for_objects(panels)

        assert len(positions) == 5

        # First row: 2 panels (100 + 10 + 100 = 210 < 250)
        # Second row: 2 panels
        # Third row: 1 panel
        assert positions[0]["center_y"] == 50.0  # First row
        assert positions[1]["center_y"] == 50.0  # First row
        assert positions[2]["center_y"] == 160.0  # Second row (100 + 10 + 50)
        assert positions[3]["center_y"] == 160.0  # Second row
        assert positions[4]["center_y"] == 270.0  # Third row

    def test_horizontal_flow_center_alignment(self):
        """Test horizontal flow with center alignment."""
        layout = FlowLayout(
            width=400.0,
            height=100.0,
            direction="horizontal",
            spacing=0.0,
            wrap="nowrap",
            alignment="center",
        )

        panels = [Panel(width=100, height=100) for _ in range(2)]
        positions = layout.calculate_positions_for_objects(panels)

        # Total width: 200, remaining: 200, offset: 100
        assert positions[0]["center_x"] == 150.0  # 100 + 50
        assert positions[1]["center_x"] == 250.0  # 100 + 100 + 50

    def test_horizontal_flow_end_alignment(self):
        """Test horizontal flow with end alignment."""
        layout = FlowLayout(
            width=400.0,
            height=100.0,
            direction="horizontal",
            spacing=0.0,
            wrap="nowrap",
            alignment="end",
        )

        panels = [Panel(width=100, height=100) for _ in range(2)]
        positions = layout.calculate_positions_for_objects(panels)

        # Panels pushed to end
        assert positions[0]["center_x"] == 250.0  # 200 + 50
        assert positions[1]["center_x"] == 350.0  # 300 + 50

    def test_vertical_flow_nowrap(self):
        """Test vertical flow without wrapping."""
        layout = FlowLayout(
            width=100.0,
            height=1000.0,
            direction="vertical",
            spacing=10.0,
            wrap="nowrap",
            alignment="start",
        )

        panels = [Panel(width=100, height=100) for _ in range(3)]
        positions = layout.calculate_positions_for_objects(panels)

        assert len(positions) == 3

        # Check positions (start-aligned)
        assert positions[0]["center_y"] == 50.0
        assert positions[1]["center_y"] == 160.0  # 100 + 10 + 50
        assert positions[2]["center_y"] == 270.0  # 200 + 20 + 50

    def test_vertical_flow_wrap(self):
        """Test vertical flow with wrapping."""
        layout = FlowLayout(
            width=500.0,
            height=250.0,
            direction="vertical",
            spacing=10.0,
            wrap="wrap",
            alignment="start",
        )

        panels = [Panel(width=100, height=100) for _ in range(5)]
        positions = layout.calculate_positions_for_objects(panels)

        assert len(positions) == 5

        # First column: 2 panels (100 + 10 + 100 = 210 < 250)
        # Second column: 2 panels
        # Third column: 1 panel
        assert positions[0]["center_x"] == 50.0  # First column
        assert positions[1]["center_x"] == 50.0  # First column
        assert positions[2]["center_x"] == 160.0  # Second column
        assert positions[3]["center_x"] == 160.0  # Second column
        assert positions[4]["center_x"] == 270.0  # Third column

    def test_vertical_flow_center_alignment(self):
        """Test vertical flow with center alignment."""
        layout = FlowLayout(
            width=100.0,
            height=400.0,
            direction="vertical",
            spacing=0.0,
            wrap="nowrap",
            alignment="center",
        )

        panels = [Panel(width=100, height=100) for _ in range(2)]
        positions = layout.calculate_positions_for_objects(panels)

        # Total height: 200, remaining: 200, offset: 100
        assert positions[0]["center_y"] == 150.0  # 100 + 50
        assert positions[1]["center_y"] == 250.0  # 100 + 100 + 50

    def test_cross_alignment_center(self):
        """Test cross alignment with different sized items."""
        layout = FlowLayout(
            width=300.0,
            height=200.0,
            direction="horizontal",
            spacing=10.0,
            wrap="nowrap",
            alignment="start",
            cross_alignment="center",
        )

        # Different height panels
        panels = [
            Panel(width=100, height=50),
            Panel(width=100, height=100),
            Panel(width=100, height=75),
        ]
        positions = layout.calculate_positions_for_objects(panels)

        # All should be centered vertically within row height of 100
        assert positions[0]["center_y"] == 50.0  # Centered in row height 100
        assert positions[1]["center_y"] == 50.0  # Full height
        assert positions[2]["center_y"] == 50.0  # Centered in row height 100

    def test_with_offset(self):
        """Test layout with offsets."""
        layout = FlowLayout(
            width=200.0,
            height=200.0,
            direction="horizontal",
            spacing=0.0,
            wrap="nowrap",
            offset_x=100.0,
            offset_y=50.0,
        )

        panels = [Panel(width=100, height=100)]
        positions = layout.calculate_positions_for_objects(panels)

        assert positions[0]["center_x"] == 150.0  # 100 + 50
        assert positions[0]["center_y"] == 100.0  # 50 + 50

    def test_mixed_sizes(self):
        """Test layout with mixed size objects."""
        layout = FlowLayout(
            width=400.0,
            height=300.0,
            direction="horizontal",
            spacing=10.0,
            wrap="wrap",
        )

        panels = [
            Panel(width=150, height=100),
            Panel(width=100, height=150),
            Panel(width=200, height=80),
        ]
        positions = layout.calculate_positions_for_objects(panels)

        assert len(positions) == 3

        # Check that widths are preserved
        assert positions[0]["width"] == 150.0
        assert positions[1]["width"] == 100.0
        assert positions[2]["width"] == 200.0

        # Check that heights are preserved
        assert positions[0]["height"] == 100.0
        assert positions[1]["height"] == 150.0
        assert positions[2]["height"] == 80.0


class TestPageFlowLayout:
    """Tests for Page with FlowLayout."""

    def test_set_flow_layout(self):
        """Test setting flow layout on page."""
        page = Page()
        result = page.set_flow_layout(
            direction="horizontal",
            spacing=15.0,
            alignment="center",
        )

        assert result is page
        assert page._layout is not None
        assert isinstance(page._layout, FlowLayout)
        assert page._layout.direction == "horizontal"
        assert page._layout.spacing == 15.0
        assert page._layout.alignment == "center"

    def test_flow_layout_default_spacing(self):
        """Test flow layout uses page gutter as default spacing."""
        page = Page(gutter=25.0)
        page.set_flow_layout()

        assert page._layout.spacing == 25.0

    def test_auto_layout_with_flow(self):
        """Test auto_layout works with FlowLayout."""
        page = Page(width=500, height=300, margin=0, gutter=10)
        page.set_flow_layout(direction="horizontal", wrap="nowrap")

        page.add(Panel(width=100, height=100))
        page.add(Panel(width=100, height=100))
        page.add(Panel(width=100, height=100))

        page.auto_layout()

        # Panels should be positioned horizontally
        assert page._panels[0].position[0] == pytest.approx(50.0)
        assert page._panels[1].position[0] == pytest.approx(160.0)
        assert page._panels[2].position[0] == pytest.approx(270.0)

    def test_flow_layout_preserves_panel_sizes(self):
        """Test that FlowLayout preserves original panel sizes."""
        page = Page(width=800, height=600, margin=0, gutter=10)
        page.set_flow_layout(direction="horizontal")

        page.add(Panel(width=150, height=200))
        page.add(Panel(width=100, height=100))

        page.auto_layout()

        # Sizes should be preserved (not overwritten like GridLayout)
        assert page._panels[0].width == 150
        assert page._panels[0].height == 200
        assert page._panels[1].width == 100
        assert page._panels[1].height == 100

    def test_method_chaining(self):
        """Test method chaining with flow layout."""
        page = (
            Page()
            .set_flow_layout(direction="vertical", alignment="center")
            .add(Panel(), Panel(), Panel())
            .auto_layout()
        )

        assert len(page._panels) == 3
        assert page._layout is not None


class TestFlowLayoutExtended:
    """Extended tests for FlowLayout edge cases."""

    def test_vertical_flow_end_alignment(self):
        """Test vertical flow with end alignment."""
        layout = FlowLayout(
            width=100.0,
            height=400.0,
            direction="vertical",
            spacing=0.0,
            wrap="nowrap",
            alignment="end",
        )

        panels = [Panel(width=100, height=100) for _ in range(2)]
        positions = layout.calculate_positions_for_objects(panels)

        # Total height: 200, remaining: 200, start_y = 200
        assert positions[0]["center_y"] == 250.0  # 200 + 50
        assert positions[1]["center_y"] == 350.0  # 200 + 100 + 50

    def test_vertical_cross_alignment_center(self):
        """Test vertical flow with center cross alignment."""
        layout = FlowLayout(
            width=200.0,
            height=400.0,
            direction="vertical",
            spacing=10.0,
            wrap="nowrap",
            alignment="start",
            cross_alignment="center",
        )

        panels = [
            Panel(width=50, height=100),
            Panel(width=100, height=100),
            Panel(width=75, height=100),
        ]
        positions = layout.calculate_positions_for_objects(panels)

        # All should be centered horizontally within column width of 100
        assert positions[0]["center_x"] == 50.0  # Centered in col_width 100
        assert positions[1]["center_x"] == 50.0  # Full width
        assert positions[2]["center_x"] == 50.0  # Centered in col_width 100

    def test_vertical_cross_alignment_end(self):
        """Test vertical flow with end cross alignment."""
        layout = FlowLayout(
            width=200.0,
            height=400.0,
            direction="vertical",
            spacing=0.0,
            wrap="nowrap",
            alignment="start",
            cross_alignment="end",
        )

        panels = [
            Panel(width=50, height=100),
            Panel(width=100, height=100),
        ]
        positions = layout.calculate_positions_for_objects(panels)

        # Both should be aligned to right edge of column (col_width = 100)
        # Panel 1: half_width = 25, center_x = 100 - 25 = 75
        assert positions[0]["center_x"] == 75.0
        # Panel 2: half_width = 50, center_x = 100 - 50 = 50
        assert positions[1]["center_x"] == 50.0

    def test_horizontal_cross_alignment_end(self):
        """Test horizontal flow with end cross alignment."""
        layout = FlowLayout(
            width=400.0,
            height=200.0,
            direction="horizontal",
            spacing=0.0,
            wrap="nowrap",
            alignment="start",
            cross_alignment="end",
        )

        panels = [
            Panel(width=100, height=50),
            Panel(width=100, height=100),
        ]
        positions = layout.calculate_positions_for_objects(panels)

        # Row height is 100 (max of panels)
        # Panel 1: height=50, half_h=25, center_y = 0 + 100 - 25 = 75
        assert positions[0]["center_y"] == 75.0
        # Panel 2: height=100, half_h=50, center_y = 0 + 100 - 50 = 50
        assert positions[1]["center_y"] == 50.0

    def test_calculate_positions_with_bounding_box_fallback(self):
        """Test calculate_positions_for_objects with objects using bounding box."""
        from comix.cobject.cobject import CObject
        import numpy as np

        layout = FlowLayout(
            width=400.0,
            height=200.0,
            direction="horizontal",
            spacing=10.0,
        )

        # Create CObjects without explicit width/height
        obj1 = CObject()
        obj1._points = np.array([[-50, -25], [50, 25]], dtype=np.float64)

        obj2 = CObject()
        obj2._points = np.array([[-30, -30], [30, 30]], dtype=np.float64)

        positions = layout.calculate_positions_for_objects([obj1, obj2])

        assert len(positions) == 2
        assert positions[0]["width"] == 100.0
        assert positions[0]["height"] == 50.0
        assert positions[1]["width"] == 60.0
        assert positions[1]["height"] == 60.0

    def test_calculate_positions_with_attribute_error_fallback(self):
        """Test calculate_positions_for_objects with fallback to default size."""

        class MinimalObject:
            """Object without width/height or get_width/get_height."""
            pass

        layout = FlowLayout(
            width=400.0,
            height=200.0,
            direction="horizontal",
            spacing=10.0,
        )

        obj = MinimalObject()
        positions = layout.calculate_positions_for_objects([obj])

        # Should fallback to 100x100 default
        assert len(positions) == 1
        assert positions[0]["width"] == 100.0
        assert positions[0]["height"] == 100.0

    def test_vertical_wrap_multiple_columns(self):
        """Test vertical flow wrapping to multiple columns."""
        layout = FlowLayout(
            width=400.0,
            height=150.0,  # Only fits one 100px panel per column
            direction="vertical",
            spacing=10.0,
            wrap="wrap",
            alignment="start",
        )

        panels = [Panel(width=100, height=100) for _ in range(4)]
        positions = layout.calculate_positions_for_objects(panels)

        assert len(positions) == 4
        # Each panel should be in its own column
        assert positions[0]["center_x"] == 50.0  # Column 1
        assert positions[1]["center_x"] == 160.0  # Column 2
        assert positions[2]["center_x"] == 270.0  # Column 3
        assert positions[3]["center_x"] == 380.0  # Column 4

    def test_horizontal_equal_cell_mode_wrap(self):
        """Test calculate_positions with num_cells in wrap mode."""
        layout = FlowLayout(
            width=500.0,
            height=400.0,
            direction="horizontal",
            spacing=10.0,
            wrap="wrap",
        )

        positions = layout.calculate_positions(6)

        assert len(positions) == 6
        # Should create reasonable cell sizes
        for pos in positions:
            assert pos["width"] > 0
            assert pos["height"] > 0

    def test_vertical_equal_cell_mode_wrap(self):
        """Test calculate_positions with num_cells in vertical wrap mode."""
        layout = FlowLayout(
            width=400.0,
            height=500.0,
            direction="vertical",
            spacing=10.0,
            wrap="wrap",
        )

        positions = layout.calculate_positions(6)

        assert len(positions) == 6
        for pos in positions:
            assert pos["width"] > 0
            assert pos["height"] > 0

    def test_horizontal_equal_cell_mode_nowrap(self):
        """Test calculate_positions with num_cells in horizontal nowrap mode."""
        layout = FlowLayout(
            width=400.0,
            height=100.0,
            direction="horizontal",
            spacing=10.0,
            wrap="nowrap",
        )

        positions = layout.calculate_positions(4)

        assert len(positions) == 4
        # In nowrap mode, cells should span full height
        for pos in positions:
            assert pos["height"] == 100.0

    def test_vertical_equal_cell_mode_nowrap(self):
        """Test calculate_positions with num_cells in vertical nowrap mode."""
        layout = FlowLayout(
            width=100.0,
            height=400.0,
            direction="vertical",
            spacing=10.0,
            wrap="nowrap",
        )

        positions = layout.calculate_positions(4)

        assert len(positions) == 4
        # In nowrap mode, cells should span full width
        for pos in positions:
            assert pos["width"] == 100.0
