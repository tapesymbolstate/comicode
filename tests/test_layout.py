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
