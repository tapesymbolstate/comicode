"""Tests for Panel Templates."""

import tempfile
from pathlib import Path

from comix.page.templates import (
    FourKoma,
    SplashPage,
    TwoByTwo,
    WebComic,
    ThreeRowLayout,
    MangaPage,
    ActionPage,
    NewspaperStrip,
    Widescreen,
)
from comix.cobject.character.character import Stickman
from comix.cobject.text.text import Text


class TestFourKoma:
    """Tests for FourKoma template."""

    def test_default_init(self):
        """Test default initialization."""
        comic = FourKoma()
        assert comic.width == 300.0
        assert comic.height == 1200.0
        assert len(comic._panels) == 4

    def test_panel_names(self):
        """Test panels have semantic names."""
        comic = FourKoma()
        assert comic.setup.name == "setup"
        assert comic.development.name == "development"
        assert comic.turn.name == "turn"
        assert comic.punchline.name == "punchline"

    def test_panels_property(self):
        """Test panels property returns all panels."""
        comic = FourKoma()
        panels = comic.panels
        assert len(panels) == 4
        assert panels[0] is comic.setup
        assert panels[1] is comic.development
        assert panels[2] is comic.turn
        assert panels[3] is comic.punchline

    def test_custom_dimensions(self):
        """Test custom dimensions override defaults."""
        comic = FourKoma(width=400, height=1600)
        assert comic.width == 400
        assert comic.height == 1600

    def test_auto_layout(self):
        """Test panels are laid out vertically."""
        comic = FourKoma()
        comic.auto_layout()

        # Panels should be stacked vertically
        for i, panel in enumerate(comic.panels):
            assert panel.width > 0
            assert panel.height > 0
            # Each panel should have a unique y position
            if i > 0:
                prev_center = comic.panels[i - 1].position[1]
                curr_center = panel.position[1]
                assert curr_center > prev_center

    def test_render(self):
        """Test rendering to SVG."""
        comic = FourKoma()
        char = Stickman()
        comic.setup.add_content(char)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = comic.render(f.name, format="svg")
            assert Path(output_path).exists()
            content = Path(output_path).read_text()
            assert "<svg" in content
            Path(output_path).unlink()


class TestSplashPage:
    """Tests for SplashPage template."""

    def test_default_init(self):
        """Test default initialization (full page splash)."""
        page = SplashPage()
        assert page.splash is not None
        assert page.header is None
        assert len(page._panels) == 1

    def test_with_header(self):
        """Test splash page with header."""
        page = SplashPage(header_height=100)
        assert page.splash is not None
        assert page.header is not None
        assert len(page._panels) == 2
        assert page.header.name == "header"
        assert page.splash.name == "splash"

    def test_splash_fills_page(self):
        """Test splash panel fills available space."""
        page = SplashPage(width=800, height=1200, margin=20)
        expected_width = 800 - 2 * 20
        expected_height = 1200 - 2 * 20
        assert page.splash.width == expected_width
        assert page.splash.height == expected_height

    def test_splash_with_header_size(self):
        """Test splash panel size with header."""
        page = SplashPage(width=800, height=1200, margin=20, gutter=10, header_height=100)
        content_width = 800 - 2 * 20
        content_height = 1200 - 2 * 20
        expected_splash_height = content_height - 100 - 10  # minus header and gutter

        assert page.header.width == content_width
        assert page.header.height == 100
        assert page.splash.width == content_width
        assert page.splash.height == expected_splash_height

    def test_auto_layout_skipped(self):
        """Test that auto_layout doesn't change pre-positioned panels."""
        import numpy as np

        page = SplashPage()
        original_pos = page.splash.position.copy()
        page.auto_layout()
        assert np.allclose(page.splash.position, original_pos)


class TestTwoByTwo:
    """Tests for TwoByTwo template."""

    def test_default_init(self):
        """Test default initialization."""
        page = TwoByTwo()
        assert len(page._panels) == 4

    def test_panel_properties(self):
        """Test panel position properties."""
        page = TwoByTwo()
        assert page.top_left.name == "top_left"
        assert page.top_right.name == "top_right"
        assert page.bottom_left.name == "bottom_left"
        assert page.bottom_right.name == "bottom_right"

    def test_panels_property(self):
        """Test panels property returns all panels in order."""
        page = TwoByTwo()
        panels = page.panels
        assert len(panels) == 4
        assert panels[0] is page.top_left
        assert panels[1] is page.top_right
        assert panels[2] is page.bottom_left
        assert panels[3] is page.bottom_right

    def test_layout_applied(self):
        """Test 2x2 grid layout is set."""
        page = TwoByTwo()
        assert page._layout is not None
        assert page._layout.rows == 2
        assert page._layout.cols == 2

    def test_auto_layout(self):
        """Test panels are arranged in 2x2 grid."""
        page = TwoByTwo(width=800, height=600, margin=0, gutter=0)
        page.auto_layout()

        # All panels should have same size
        expected_width = 400
        expected_height = 300
        for panel in page.panels:
            assert panel.width == expected_width
            assert panel.height == expected_height


class TestWebComic:
    """Tests for WebComic template."""

    def test_default_init(self):
        """Test default initialization."""
        comic = WebComic()
        assert comic.width == 800.0
        assert comic.num_panels == 4
        assert len(comic._panels) == 4

    def test_custom_panels(self):
        """Test custom panel count."""
        comic = WebComic(panels=6)
        assert comic.num_panels == 6
        assert len(comic._panels) == 6

    def test_calculated_height(self):
        """Test height is calculated based on panels."""
        comic = WebComic(panels=5, panel_height=400, margin=20, gutter=10)
        expected_height = 2 * 20 + 5 * 400 + 4 * 10  # margins + panels + gutters
        assert comic.height == expected_height

    def test_panels_property(self):
        """Test panels property."""
        comic = WebComic(panels=3)
        panels = comic.panels
        assert len(panels) == 3
        for i, panel in enumerate(panels):
            assert panel.name == f"panel_{i + 1}"

    def test_vertical_layout(self):
        """Test panels are stacked vertically."""
        comic = WebComic(panels=3)
        comic.auto_layout()

        # All panels should have same width
        for panel in comic.panels:
            assert panel.width == comic.width - 2 * comic.margin


class TestThreeRowLayout:
    """Tests for ThreeRowLayout template."""

    def test_default_init(self):
        """Test default initialization (1-2-1 pattern)."""
        page = ThreeRowLayout()
        assert len(page.rows) == 3
        assert len(page.rows[0]) == 1
        assert len(page.rows[1]) == 2
        assert len(page.rows[2]) == 1

    def test_custom_row_panels(self):
        """Test custom panels per row."""
        page = ThreeRowLayout(row_panels=[2, 3, 1])
        assert len(page.rows[0]) == 2
        assert len(page.rows[1]) == 3
        assert len(page.rows[2]) == 1
        assert len(page._panels) == 6

    def test_row_heights(self):
        """Test custom row heights."""
        page = ThreeRowLayout(row_heights=[2.0, 1.0, 1.0])
        # First row should be taller
        page.auto_layout()  # This doesn't change pre-positioned panels
        row1_height = page.rows[0][0].height
        row2_height = page.rows[1][0].height
        assert row1_height > row2_height

    def test_panel_names(self):
        """Test panels have row/column based names."""
        page = ThreeRowLayout()
        assert page.rows[0][0].name == "row1_panel1"
        assert page.rows[1][0].name == "row2_panel1"
        assert page.rows[1][1].name == "row2_panel2"
        assert page.rows[2][0].name == "row3_panel1"

    def test_panels_property(self):
        """Test panels property returns all panels."""
        page = ThreeRowLayout(row_panels=[1, 2, 1])
        panels = page.panels
        assert len(panels) == 4

    def test_auto_layout_skipped(self):
        """Test that auto_layout doesn't change pre-positioned panels."""
        page = ThreeRowLayout()
        original_positions = [p.position for p in page.panels]
        page.auto_layout()
        new_positions = [p.position for p in page.panels]
        assert original_positions == new_positions


class TestMangaPage:
    """Tests for MangaPage template."""

    def test_default_init(self):
        """Test default initialization."""
        page = MangaPage()
        assert len(page._panels) == 6  # 2x3 default

    def test_six_panel_preset(self):
        """Test six_panel preset."""
        page = MangaPage(preset="six_panel")
        assert len(page._panels) == 6
        assert page._layout.rows == 2
        assert page._layout.cols == 3

    def test_dialogue_preset(self):
        """Test dialogue preset."""
        page = MangaPage(preset="dialogue")
        assert len(page._panels) == 6
        assert page._layout.rows == 3
        assert page._layout.cols == 2

    def test_action_preset(self):
        """Test action preset."""
        page = MangaPage(preset="action")
        assert len(page._panels) == 4
        assert page._layout.rows == 2
        assert page._layout.cols == 2

    def test_custom_grid(self):
        """Test custom grid layout."""
        page = MangaPage(rows=4, cols=3)
        assert len(page._panels) == 12
        assert page._layout.rows == 4
        assert page._layout.cols == 3

    def test_custom_overrides_preset(self):
        """Test custom values override preset."""
        page = MangaPage(preset="six_panel", rows=3)
        assert page._layout.rows == 3
        assert page._layout.cols == 3  # from preset

    def test_panel_names(self):
        """Test panels have row/col based names."""
        page = MangaPage(rows=2, cols=2)
        names = [p.name for p in page.panels]
        assert "panel_1_1" in names
        assert "panel_1_2" in names
        assert "panel_2_1" in names
        assert "panel_2_2" in names


class TestActionPage:
    """Tests for ActionPage template."""

    def test_default_init(self):
        """Test default initialization."""
        page = ActionPage()
        assert page.main is not None
        assert len(page.small) == 3
        assert len(page._panels) == 4

    def test_custom_small_panels(self):
        """Test custom number of small panels."""
        page = ActionPage(small_panels=4)
        assert len(page.small) == 4
        assert len(page._panels) == 5

    def test_main_ratio(self):
        """Test main panel ratio."""
        page = ActionPage(main_ratio=0.7, width=800, height=1000, margin=0, gutter=0)
        # Main panel should take 70% of page height
        assert page.main.height == 1000 * 0.7

    def test_main_property(self):
        """Test main panel property."""
        page = ActionPage()
        assert page.main.name == "main"

    def test_small_property(self):
        """Test small panels property."""
        page = ActionPage(small_panels=2)
        assert len(page.small) == 2
        assert page.small[0].name == "small_1"
        assert page.small[1].name == "small_2"

    def test_panels_property(self):
        """Test panels property includes main first."""
        page = ActionPage(small_panels=2)
        panels = page.panels
        assert len(panels) == 3
        assert panels[0] is page.main
        assert panels[1] is page.small[0]
        assert panels[2] is page.small[1]

    def test_auto_layout_skipped(self):
        """Test that auto_layout doesn't change pre-positioned panels."""
        import numpy as np

        page = ActionPage()
        original_main_pos = page.main.position.copy()
        original_small_pos = [p.position.copy() for p in page.small]
        page.auto_layout()
        assert np.allclose(page.main.position, original_main_pos)
        for i, panel in enumerate(page.small):
            assert np.allclose(panel.position, original_small_pos[i])


class TestTemplateImports:
    """Test that templates are properly exported."""

    def test_import_from_comix(self):
        """Test templates can be imported from comix."""
        from comix import (
            FourKoma,
            SplashPage,
            TwoByTwo,
            WebComic,
            ThreeRowLayout,
            MangaPage,
            ActionPage,
        )

        # Verify they're the correct classes
        assert FourKoma.__name__ == "FourKoma"
        assert SplashPage.__name__ == "SplashPage"
        assert TwoByTwo.__name__ == "TwoByTwo"
        assert WebComic.__name__ == "WebComic"
        assert ThreeRowLayout.__name__ == "ThreeRowLayout"
        assert MangaPage.__name__ == "MangaPage"
        assert ActionPage.__name__ == "ActionPage"

    def test_import_from_page(self):
        """Test templates can be imported from comix.page."""
        from comix.page import (
            FourKoma,
            SplashPage,
            TwoByTwo,
            WebComic,
            ThreeRowLayout,
            MangaPage,
            ActionPage,
        )

        # Verify instantiation
        assert FourKoma() is not None
        assert SplashPage() is not None
        assert TwoByTwo() is not None
        assert WebComic() is not None
        assert ThreeRowLayout() is not None
        assert MangaPage() is not None
        assert ActionPage() is not None


class TestTemplateRendering:
    """Test that all templates render correctly."""

    def test_fourkoma_renders(self):
        """Test FourKoma renders to SVG."""
        comic = FourKoma()
        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            path = comic.render(f.name)
            assert Path(path).exists()
            content = Path(path).read_text()
            assert "<svg" in content
            assert 'width="300' in content  # Flexible match for 300 or 300.0
            Path(path).unlink()

    def test_splashpage_renders(self):
        """Test SplashPage renders to SVG."""
        page = SplashPage()
        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            path = page.render(f.name)
            assert Path(path).exists()
            Path(path).unlink()

    def test_twobytwo_renders(self):
        """Test TwoByTwo renders to SVG."""
        page = TwoByTwo()
        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            path = page.render(f.name)
            assert Path(path).exists()
            Path(path).unlink()

    def test_webcomic_renders(self):
        """Test WebComic renders to SVG."""
        comic = WebComic(panels=3)
        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            path = comic.render(f.name)
            assert Path(path).exists()
            Path(path).unlink()

    def test_threerowlayout_renders(self):
        """Test ThreeRowLayout renders to SVG."""
        page = ThreeRowLayout()
        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            path = page.render(f.name)
            assert Path(path).exists()
            Path(path).unlink()

    def test_mangapage_renders(self):
        """Test MangaPage renders to SVG."""
        page = MangaPage(preset="six_panel")
        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            path = page.render(f.name)
            assert Path(path).exists()
            Path(path).unlink()

    def test_actionpage_renders(self):
        """Test ActionPage renders to SVG."""
        page = ActionPage()
        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            path = page.render(f.name)
            assert Path(path).exists()
            Path(path).unlink()


class TestTemplateWithContent:
    """Test templates with actual content."""

    def test_fourkoma_with_character(self):
        """Test FourKoma with character content."""
        comic = FourKoma()
        char = Stickman()
        char.move_to((150, 0))

        comic.setup.add_content(char)
        bubble = char.say("Hello!")
        comic.setup.add_content(bubble)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            path = comic.render(f.name)
            content = Path(path).read_text()
            assert "Hello!" in content
            Path(path).unlink()

    def test_splashpage_with_text(self):
        """Test SplashPage with text content."""
        page = SplashPage(header_height=80)
        title = Text("Chapter 1", font_size=32)
        title.move_to((page.width / 2, 40))
        page.header.add_content(title)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            path = page.render(f.name)
            content = Path(path).read_text()
            assert "Chapter 1" in content
            Path(path).unlink()

    def test_actionpage_with_content(self):
        """Test ActionPage with content in multiple panels."""
        page = ActionPage(small_panels=3)

        # Add main action
        main_char = Stickman()
        page.main.add_content(main_char)

        # Add reactions in small panels
        for i, panel in enumerate(page.small):
            text = Text(f"Reaction {i + 1}")
            panel.add_content(text)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            path = page.render(f.name)
            content = Path(path).read_text()
            assert "Reaction 1" in content
            assert "Reaction 2" in content
            assert "Reaction 3" in content
            Path(path).unlink()


class TestNewspaperStrip:
    """Tests for NewspaperStrip template."""

    def test_default_init(self):
        """Test default initialization (3 panels)."""
        strip = NewspaperStrip()
        assert strip.width == 1200.0
        assert strip.height == 300.0
        assert len(strip._panels) == 3

    def test_custom_panel_count(self):
        """Test custom panel count."""
        strip = NewspaperStrip(panels=4)
        assert len(strip._panels) == 4

    def test_panels_property(self):
        """Test panels property returns all panels."""
        strip = NewspaperStrip(panels=3)
        panels = strip.panels
        assert len(panels) == 3
        for i, panel in enumerate(panels):
            assert panel.name == f"panel_{i + 1}"

    def test_first_property(self):
        """Test first panel property."""
        strip = NewspaperStrip()
        assert strip.first is strip.panels[0]
        assert strip.first.name == "panel_1"

    def test_last_property(self):
        """Test last panel property."""
        strip = NewspaperStrip(panels=4)
        assert strip.last is strip.panels[-1]
        assert strip.last.name == "panel_4"

    def test_horizontal_layout(self):
        """Test panels are laid out horizontally."""
        strip = NewspaperStrip(panels=3)
        strip.auto_layout()

        # All panels should have same height
        heights = [p.height for p in strip.panels]
        assert len(set(heights)) == 1

        # Panels should be arranged left to right
        for i in range(len(strip.panels) - 1):
            assert strip.panels[i].position[0] < strip.panels[i + 1].position[0]

    def test_custom_dimensions(self):
        """Test custom dimensions override defaults."""
        strip = NewspaperStrip(width=900, height=250)
        assert strip.width == 900
        assert strip.height == 250

    def test_render(self):
        """Test rendering to SVG."""
        strip = NewspaperStrip()
        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            path = strip.render(f.name)
            assert Path(path).exists()
            content = Path(path).read_text()
            assert "<svg" in content
            assert 'width="1200' in content
            Path(path).unlink()


class TestWidescreen:
    """Tests for Widescreen template."""

    def test_default_init(self):
        """Test default initialization (3 panels, 16:9 aspect)."""
        page = Widescreen()
        assert page.width == 1200.0
        assert len(page._panels) == 3
        assert page.aspect_ratio == 16 / 9

    def test_custom_panel_count(self):
        """Test custom panel count."""
        page = Widescreen(panels=2)
        assert len(page._panels) == 2

    def test_custom_aspect_ratio(self):
        """Test custom aspect ratio."""
        page = Widescreen(aspect_ratio=21 / 9)
        assert page.aspect_ratio == 21 / 9

    def test_calculated_height(self):
        """Test height is calculated based on panels and aspect ratio."""
        # With 16:9 aspect, 1200px width -> (1200 - 40 margin) / (16/9) = ~653 per panel
        page = Widescreen(panels=2, width=1200, margin=20, gutter=10)
        content_width = 1200 - 2 * 20  # 1160
        panel_height = content_width / (16 / 9)  # ~652.5
        expected_height = 2 * 20 + 2 * panel_height + 1 * 10
        assert abs(page.height - expected_height) < 0.01

    def test_panels_property(self):
        """Test panels property returns all panels."""
        page = Widescreen(panels=4)
        panels = page.panels
        assert len(panels) == 4
        for i, panel in enumerate(panels):
            assert panel.name == f"panel_{i + 1}"

    def test_vertical_layout(self):
        """Test panels are stacked vertically."""
        page = Widescreen(panels=3)
        page.auto_layout()

        # All panels should have same width
        widths = [p.width for p in page.panels]
        assert len(set(widths)) == 1

        # Panels should be arranged top to bottom
        for i in range(len(page.panels) - 1):
            assert page.panels[i].position[1] < page.panels[i + 1].position[1]

    def test_ultrawide_aspect(self):
        """Test ultra-wide 21:9 aspect ratio."""
        page = Widescreen(panels=2, aspect_ratio=21 / 9)
        page.auto_layout()

        # Panels should be shorter (wider aspect ratio)
        content_width = page.width - 2 * page.margin
        expected_panel_height = content_width / (21 / 9)
        assert abs(page.panels[0].height - expected_panel_height) < 0.01

    def test_render(self):
        """Test rendering to SVG."""
        page = Widescreen()
        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            path = page.render(f.name)
            assert Path(path).exists()
            content = Path(path).read_text()
            assert "<svg" in content
            Path(path).unlink()


class TestNewTemplateImports:
    """Test that new templates are properly exported."""

    def test_import_from_comix(self):
        """Test new templates can be imported from comix."""
        from comix import NewspaperStrip, Widescreen

        assert NewspaperStrip.__name__ == "NewspaperStrip"
        assert Widescreen.__name__ == "Widescreen"

    def test_import_from_page_templates(self):
        """Test new templates can be imported from comix.page.templates."""
        from comix.page.templates import NewspaperStrip, Widescreen

        assert NewspaperStrip() is not None
        assert Widescreen() is not None


class TestNewTemplateRendering:
    """Test that new templates render correctly."""

    def test_newspaperstrip_renders(self):
        """Test NewspaperStrip renders to SVG."""
        strip = NewspaperStrip()
        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            path = strip.render(f.name)
            assert Path(path).exists()
            content = Path(path).read_text()
            assert "<svg" in content
            Path(path).unlink()

    def test_widescreen_renders(self):
        """Test Widescreen renders to SVG."""
        page = Widescreen()
        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            path = page.render(f.name)
            assert Path(path).exists()
            Path(path).unlink()


class TestNewTemplateWithContent:
    """Test new templates with actual content."""

    def test_newspaperstrip_with_characters(self):
        """Test NewspaperStrip with character content."""
        strip = NewspaperStrip(panels=3)
        strip.auto_layout()

        # Add character to first panel
        char = Stickman()
        char.move_to((strip.first.position[0], strip.first.position[1]))
        strip.first.add_content(char)
        bubble = char.say("Setup!")
        strip.first.add_content(bubble)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            path = strip.render(f.name)
            content = Path(path).read_text()
            assert "Setup!" in content
            Path(path).unlink()

    def test_widescreen_with_text(self):
        """Test Widescreen with text content."""
        page = Widescreen(panels=2)
        page.auto_layout()

        text = Text("Cinematic shot", font_size=24)
        text.move_to(page.panels[0].position)
        page.panels[0].add_content(text)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            path = page.render(f.name)
            content = Path(path).read_text()
            assert "Cinematic shot" in content
            Path(path).unlink()
