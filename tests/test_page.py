"""Tests for Page class."""

import tempfile
from pathlib import Path

from comix.page.page import Page, SinglePanel, Strip
from comix.cobject.panel.panel import Panel
from comix.cobject.character.character import Stickman


class TestPage:
    """Tests for Page class."""

    def test_default_init(self):
        """Test default initialization."""
        page = Page()
        assert page.width == 800.0
        assert page.height == 1200.0
        assert page.background_color == "#FFFFFF"
        assert page.margin == 20.0
        assert page.gutter == 10.0

    def test_custom_init(self):
        """Test custom initialization."""
        page = Page(
            width=1000,
            height=800,
            background_color="#EEEEEE",
            margin=30,
            gutter=15,
        )
        assert page.width == 1000
        assert page.height == 800
        assert page.background_color == "#EEEEEE"
        assert page.margin == 30
        assert page.gutter == 15

    def test_add_remove(self):
        """Test adding and removing objects."""
        page = Page()
        panel = Panel()
        char = Stickman()

        page.add(panel, char)
        assert panel in page._panels
        assert panel in page._cobjects
        assert char in page._cobjects
        assert char not in page._panels

        page.remove(panel)
        assert panel not in page._panels
        assert panel not in page._cobjects

    def test_set_layout(self):
        """Test setting layout."""
        page = Page()
        result = page.set_layout(rows=2, cols=3)
        assert result is page
        assert page._layout is not None
        assert page._layout.rows == 2
        assert page._layout.cols == 3

    def test_auto_layout(self):
        """Test automatic layout."""
        page = Page(width=800, height=600, margin=0, gutter=0)
        page.set_layout(rows=2, cols=2)

        for _ in range(4):
            page.add(Panel())

        page.auto_layout()

        expected_width = 400
        expected_height = 300

        for panel in page._panels:
            assert panel.width == expected_width
            assert panel.height == expected_height

    def test_render_svg(self):
        """Test rendering to SVG."""
        page = Page(width=400, height=300)
        panel = Panel(width=360, height=260)
        panel.move_to((200, 150))
        page.add(panel)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = page.render(f.name, format="svg")
            assert Path(output_path).exists()
            content = Path(output_path).read_text()
            assert "<svg" in content
            assert 'width="400px"' in content
            Path(output_path).unlink()

    def test_get_all_cobjects(self):
        """Test getting all cobjects including nested."""
        page = Page()
        panel = Panel()
        char = Stickman()
        panel.add_content(char)
        page.add(panel)

        all_objects = page.get_all_cobjects()
        assert panel in all_objects
        assert char in all_objects


class TestSinglePanel:
    """Tests for SinglePanel class."""

    def test_default_init(self):
        """Test default initialization."""
        page = SinglePanel()
        assert len(page._panels) == 1
        assert page.panel is page._panels[0]

    def test_panel_size(self):
        """Test panel fills page minus margins."""
        page = SinglePanel(width=800, height=600, margin=20)
        assert page.panel.width == 760
        assert page.panel.height == 560


class TestStrip:
    """Tests for Strip class."""

    def test_horizontal_strip(self):
        """Test horizontal strip creation."""
        strip = Strip(panels=4, direction="horizontal")
        assert strip.num_panels == 4
        assert strip.direction == "horizontal"
        assert len(strip._panels) == 4
        assert strip.width == 1200
        assert strip.height == 300

    def test_vertical_strip(self):
        """Test vertical strip creation."""
        strip = Strip(panels=3, direction="vertical")
        assert strip.num_panels == 3
        assert strip.direction == "vertical"
        assert len(strip._panels) == 3
        assert strip.width == 300
        assert strip.height == 1200
