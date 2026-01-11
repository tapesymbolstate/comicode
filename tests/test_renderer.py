"""Tests for SVG Renderer."""

import pytest
import tempfile
from pathlib import Path

from comix.page.page import Page
from comix.cobject.panel.panel import Panel
from comix.cobject.bubble.bubble import SpeechBubble
from comix.cobject.character.character import Stickman, SimpleFace
from comix.cobject.text.text import Text, SFX
from comix.cobject.shapes.shapes import Rectangle, Circle, Line
from comix.renderer.svg_renderer import SVGRenderer


class TestSVGRenderer:
    """Tests for SVGRenderer class."""

    def test_render_empty_page(self):
        """Test rendering an empty page."""
        page = Page(width=400, height=300)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            renderer = SVGRenderer(page)
            output_path = renderer.render(f.name)

            assert Path(output_path).exists()
            content = Path(output_path).read_text()
            assert "<svg" in content
            assert 'width="400px"' in content
            assert 'height="300px"' in content
            Path(output_path).unlink()

    def test_render_panel(self):
        """Test rendering a panel."""
        page = Page(width=400, height=300)
        panel = Panel(width=300, height=200)
        panel.move_to((200, 150))
        page.add(panel)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = page.render(f.name)
            content = Path(output_path).read_text()
            assert "<rect" in content
            Path(output_path).unlink()

    def test_render_bubble(self):
        """Test rendering a bubble."""
        page = Page(width=400, height=300)
        bubble = SpeechBubble(text="Hello!").move_to((200, 150))
        page.add(bubble)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = page.render(f.name)
            content = Path(output_path).read_text()
            assert "Hello!" in content
            Path(output_path).unlink()

    def test_render_stickman(self):
        """Test rendering a stickman character."""
        page = Page(width=400, height=300)
        char = Stickman(name="Test").move_to((200, 150))
        page.add(char)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = page.render(f.name)
            content = Path(output_path).read_text()
            assert "<polygon" in content or "<line" in content
            Path(output_path).unlink()

    def test_render_simple_face(self):
        """Test rendering a simple face character."""
        page = Page(width=400, height=300)
        face = SimpleFace(name="Smiley").move_to((200, 150))
        face.set_expression("happy")
        page.add(face)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = page.render(f.name)
            content = Path(output_path).read_text()
            assert "<circle" in content
            Path(output_path).unlink()

    def test_render_shapes(self):
        """Test rendering basic shapes."""
        page = Page(width=400, height=300)
        rect = Rectangle(width=100, height=50).move_to((100, 100))
        circle = Circle(radius=30).move_to((250, 100))
        line = Line(start=(0, 0), end=(100, 100)).move_to((200, 200))
        page.add(rect, circle, line)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = page.render(f.name)
            content = Path(output_path).read_text()
            assert "<rect" in content
            assert "<circle" in content
            assert "<line" in content
            Path(output_path).unlink()

    def test_render_text(self):
        """Test rendering text."""
        page = Page(width=400, height=300)
        text = Text(text="Hello World", font_size=24).move_to((200, 150))
        page.add(text)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = page.render(f.name)
            content = Path(output_path).read_text()
            assert "Hello World" in content
            assert "<text" in content
            Path(output_path).unlink()

    def test_render_sfx(self):
        """Test rendering SFX text with outline."""
        page = Page(width=400, height=300)
        sfx = SFX(text="BOOM!", color="#FF0000").move_to((200, 150))
        page.add(sfx)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = page.render(f.name)
            content = Path(output_path).read_text()
            assert "BOOM!" in content
            Path(output_path).unlink()

    def test_render_with_opacity(self):
        """Test rendering objects with opacity."""
        page = Page(width=400, height=300)
        rect = Rectangle(width=100, height=100).move_to((200, 150)).set_opacity(0.5)
        page.add(rect)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = page.render(f.name)
            content = Path(output_path).read_text()
            assert 'opacity="0.5"' in content
            Path(output_path).unlink()

    def test_render_complex_scene(self):
        """Test rendering a complex scene with multiple elements."""
        page = Page(width=800, height=600)

        panel = Panel(width=700, height=500)
        panel.move_to((400, 300))

        char1 = Stickman(name="Alice").move_to((300, 350))
        char2 = Stickman(name="Bob").move_to((500, 350)).face("left")

        bubble1 = char1.say("Hello!")
        bubble2 = char2.say("Hi there!")

        panel.add_content(char1, char2, bubble1, bubble2)
        page.add(panel)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = page.render(f.name)
            content = Path(output_path).read_text()

            assert "<svg" in content
            assert "Hello!" in content
            assert "Hi there!" in content
            Path(output_path).unlink()
