"""Tests for HTML renderer."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from comix import (
    Page,
    Panel,
    Stickman,
    Book,
    HTMLRenderer,
)


class TestHTMLRenderer:
    """Tests for HTMLRenderer class."""

    def test_renderer_initialization(self) -> None:
        """Test HTMLRenderer can be initialized."""
        page = Page(width=800, height=600)
        renderer = HTMLRenderer(page)

        assert renderer.page is page
        assert renderer.title == "Comic"
        assert renderer.theme == "light"
        assert renderer.enable_zoom is True
        assert renderer.enable_pan is True
        assert renderer.enable_hover is True
        assert renderer.enable_fullscreen is True
        assert renderer.min_zoom == 0.5
        assert renderer.max_zoom == 4.0

    def test_renderer_with_options(self) -> None:
        """Test HTMLRenderer with custom options."""
        page = Page(width=800, height=600)
        renderer = HTMLRenderer(
            page,
            title="My Comic",
            theme="dark",
            enable_zoom=False,
            enable_pan=False,
            enable_hover=False,
            enable_fullscreen=False,
            min_zoom=0.25,
            max_zoom=8.0,
        )

        assert renderer.title == "My Comic"
        assert renderer.theme == "dark"
        assert renderer.enable_zoom is False
        assert renderer.enable_pan is False
        assert renderer.enable_hover is False
        assert renderer.enable_fullscreen is False
        assert renderer.min_zoom == 0.25
        assert renderer.max_zoom == 8.0

    def test_render_to_file(self) -> None:
        """Test rendering to HTML file."""
        page = Page(width=800, height=600)
        panel = Panel(width=700, height=500)
        char = Stickman(name="Test", height=80)
        char.move_to((350, 300))
        panel.add_content(char)
        page.add(panel)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "test.html"
            result = HTMLRenderer(page).render(str(output_path))

            assert result == str(output_path)
            assert output_path.exists()

            content = output_path.read_text()
            assert "<!DOCTYPE html>" in content
            assert "<html" in content
            assert "Comic" in content  # Default title
            assert "<svg" in content  # Embedded SVG
            assert "comic-viewer" in content

    def test_render_to_string(self) -> None:
        """Test rendering to HTML string."""
        page = Page(width=800, height=600)
        panel = Panel(width=700, height=500)
        page.add(panel)

        renderer = HTMLRenderer(page, title="Test Comic")
        html_content = renderer.render_to_string()

        assert "<!DOCTYPE html>" in html_content
        assert "Test Comic" in html_content
        assert "<svg" in html_content
        assert "theme-light" in html_content

    def test_render_with_dark_theme(self) -> None:
        """Test rendering with dark theme."""
        page = Page(width=800, height=600)
        renderer = HTMLRenderer(page, theme="dark")
        html_content = renderer.render_to_string()

        assert "theme-dark" in html_content

    def test_render_without_zoom(self) -> None:
        """Test rendering without zoom controls."""
        page = Page(width=800, height=600)
        renderer = HTMLRenderer(page, enable_zoom=False)
        html_content = renderer.render_to_string()

        # Config should show zoom disabled
        assert '"enableZoom": false' in html_content

    def test_render_without_fullscreen(self) -> None:
        """Test rendering without fullscreen button."""
        page = Page(width=800, height=600)
        renderer = HTMLRenderer(page, enable_fullscreen=False)
        html_content = renderer.render_to_string()

        # Config should show fullscreen disabled
        assert '"enableFullscreen": false' in html_content

    def test_render_no_page_error(self) -> None:
        """Test error when no page is set."""
        renderer = HTMLRenderer()

        with pytest.raises(ValueError, match="No page to render"):
            renderer.render("test.html")

        with pytest.raises(ValueError, match="No page to render"):
            renderer.render_to_string()

    def test_render_creates_parent_directories(self) -> None:
        """Test that render creates parent directories."""
        page = Page(width=800, height=600)
        renderer = HTMLRenderer(page)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "nested" / "dir" / "test.html"
            result = renderer.render(str(output_path))

            assert output_path.exists()
            assert result == str(output_path)

    def test_html_escaping(self) -> None:
        """Test that HTML special characters are escaped in title."""
        page = Page(width=800, height=600)
        renderer = HTMLRenderer(page, title="<script>alert('xss')</script>")
        html_content = renderer.render_to_string()

        # Title should be escaped
        assert "<script>alert('xss')</script>" not in html_content
        assert "&lt;script&gt;" in html_content

    def test_css_included(self) -> None:
        """Test that CSS styles are included."""
        page = Page(width=800, height=600)
        renderer = HTMLRenderer(page)
        html_content = renderer.render_to_string()

        # Check for key CSS elements
        assert "<style>" in html_content
        assert ".comic-viewer" in html_content
        assert ".toolbar" in html_content
        assert ".canvas-container" in html_content
        assert "--bg-primary" in html_content  # CSS variables

    def test_javascript_included(self) -> None:
        """Test that JavaScript is included."""
        page = Page(width=800, height=600)
        renderer = HTMLRenderer(page)
        html_content = renderer.render_to_string()

        # Check for key JavaScript elements
        assert "<script>" in html_content
        assert "svgPages" in html_content
        assert "config" in html_content
        assert "function init()" in html_content
        assert "function setZoom" in html_content
        assert "setupEventListeners" in html_content

    def test_responsive_meta_tag(self) -> None:
        """Test that responsive viewport meta tag is included."""
        page = Page(width=800, height=600)
        renderer = HTMLRenderer(page)
        html_content = renderer.render_to_string()

        assert 'viewport' in html_content
        assert 'width=device-width' in html_content

    def test_generator_meta_tag(self) -> None:
        """Test that generator meta tag is included."""
        page = Page(width=800, height=600)
        renderer = HTMLRenderer(page)
        html_content = renderer.render_to_string()

        assert 'generator' in html_content
        assert 'Comix' in html_content


class TestHTMLRendererBook:
    """Tests for HTMLRenderer book rendering."""

    def test_render_book(self) -> None:
        """Test rendering a book with multiple pages."""
        page1 = Page(width=800, height=600)
        page1.add(Panel(width=700, height=500))

        page2 = Page(width=800, height=600)
        page2.add(Panel(width=700, height=500))

        book = Book(title="Test Book")
        book.add_page(page1)
        book.add_page(page2)

        renderer = HTMLRenderer()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "book.html"
            result = renderer.render_book(book, str(output_path))

            assert result == str(output_path)
            assert output_path.exists()

            content = output_path.read_text()
            assert "Test Book" in content
            assert '"isBook": true' in content
            assert '"pageCount": 2' in content
            assert "prevPage" in content  # Navigation button
            assert "nextPage" in content  # Navigation button
            assert "Page" in content and "of" in content  # Page indicator

    def test_render_book_navigation_html(self) -> None:
        """Test that book rendering includes navigation."""
        page1 = Page(width=800, height=600)
        page2 = Page(width=800, height=600)

        book = Book(title="Nav Test")
        book.add_page(page1)
        book.add_page(page2)

        renderer = HTMLRenderer()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "book.html"
            renderer.render_book(book, str(output_path))

            content = output_path.read_text()

            # Check navigation elements
            assert 'class="navigation prev"' in content
            assert 'class="navigation next"' in content
            assert 'id="prevPage"' in content
            assert 'id="nextPage"' in content


class TestPageRenderHTML:
    """Tests for Page.render() with HTML format."""

    def test_render_html_by_extension(self) -> None:
        """Test rendering to HTML by file extension."""
        page = Page(width=800, height=600)
        panel = Panel(width=700, height=500)
        page.add(panel)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "comic.html"
            result = page.render(str(output_path))

            assert result == str(output_path)
            assert output_path.exists()

            content = output_path.read_text()
            assert "<!DOCTYPE html>" in content
            assert "<svg" in content

    def test_render_htm_extension(self) -> None:
        """Test rendering to HTML with .htm extension."""
        page = Page(width=800, height=600)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "comic.htm"
            result = page.render(str(output_path))

            assert result == str(output_path)
            assert output_path.exists()

    def test_render_html_explicit_format(self) -> None:
        """Test rendering to HTML with explicit format parameter."""
        page = Page(width=800, height=600)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "comic.xyz"
            result = page.render(str(output_path), format="html")

            assert result == str(output_path)
            assert output_path.exists()

            content = output_path.read_text()
            assert "<!DOCTYPE html>" in content

    def test_render_html_with_options(self) -> None:
        """Test rendering to HTML with custom options."""
        page = Page(width=800, height=600)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "comic.html"
            page.render(
                str(output_path),
                title="Custom Title",
                theme="dark",
                enable_zoom=False,
            )

            content = output_path.read_text()
            assert "Custom Title" in content
            assert "theme-dark" in content
            assert '"enableZoom": false' in content


class TestHTMLRendererInteractivity:
    """Tests for HTML renderer interactive features."""

    def test_zoom_config_in_output(self) -> None:
        """Test zoom configuration is included in output."""
        page = Page(width=800, height=600)
        renderer = HTMLRenderer(page, min_zoom=0.1, max_zoom=10.0)
        html_content = renderer.render_to_string()

        assert '"minZoom": 0.1' in html_content
        assert '"maxZoom": 10.0' in html_content

    def test_hover_enabled_class(self) -> None:
        """Test hover enabled configuration."""
        page = Page(width=800, height=600)
        renderer = HTMLRenderer(page, enable_hover=True)
        html_content = renderer.render_to_string()

        assert '"enableHover": true' in html_content
        # CSS for hover
        assert "hover-enabled" in html_content

    def test_keyboard_shortcuts_documented(self) -> None:
        """Test that keyboard shortcuts are present in JavaScript."""
        page = Page(width=800, height=600)
        renderer = HTMLRenderer(page)
        html_content = renderer.render_to_string()

        # Check keyboard event handlers
        assert "keydown" in html_content
        assert "ArrowLeft" in html_content
        assert "ArrowRight" in html_content

    def test_touch_support_included(self) -> None:
        """Test that touch support is included."""
        page = Page(width=800, height=600)
        renderer = HTMLRenderer(page)
        html_content = renderer.render_to_string()

        # Check touch event handlers
        assert "touchstart" in html_content
        assert "touchmove" in html_content

    def test_theme_toggle_present(self) -> None:
        """Test that theme toggle is present."""
        page = Page(width=800, height=600)
        renderer = HTMLRenderer(page)
        html_content = renderer.render_to_string()

        assert "themeToggle" in html_content
        assert "toggleTheme" in html_content


class TestHTMLRendererEdgeCases:
    """Tests for edge cases in HTML renderer."""

    def test_empty_page(self) -> None:
        """Test rendering an empty page."""
        page = Page(width=800, height=600)
        renderer = HTMLRenderer(page)
        html_content = renderer.render_to_string()

        assert "<!DOCTYPE html>" in html_content
        assert "<svg" in html_content

    def test_special_characters_in_content(self) -> None:
        """Test that special characters in SVG are handled."""
        page = Page(width=800, height=600)
        panel = Panel(width=700, height=500)
        char = Stickman(name="Test<>&\"'", height=80)
        panel.add_content(char)
        page.add(panel)

        renderer = HTMLRenderer(page)
        # Should not raise
        html_content = renderer.render_to_string()
        assert "<!DOCTYPE html>" in html_content

    def test_large_page_dimensions(self) -> None:
        """Test rendering a large page."""
        page = Page(width=5000, height=5000)
        renderer = HTMLRenderer(page)
        html_content = renderer.render_to_string()

        assert "<!DOCTYPE html>" in html_content
        assert "5000" in html_content  # Width/height in SVG

    def test_complex_page_with_all_elements(self) -> None:
        """Test rendering a complex page with multiple elements."""
        page = Page(width=800, height=600)

        panel1 = Panel(width=350, height=250)
        char1 = Stickman(name="Alice", height=80)
        char1.move_to((175, 150))
        bubble1 = char1.say("Hello!")
        panel1.add_content(char1, bubble1)
        panel1.move_to((200, 150))

        panel2 = Panel(width=350, height=250)
        char2 = Stickman(name="Bob", height=80)
        char2.move_to((175, 150))
        bubble2 = char2.say("Hi there!")
        panel2.add_content(char2, bubble2)
        panel2.move_to((600, 150))

        page.add(panel1, panel2)

        renderer = HTMLRenderer(page, title="Complex Test")
        html_content = renderer.render_to_string()

        assert "<!DOCTYPE html>" in html_content
        assert "Complex Test" in html_content
        assert "Hello!" in html_content or "Hello" in html_content
        assert "Hi there!" in html_content or "Hi" in html_content
