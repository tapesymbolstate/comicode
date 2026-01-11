"""Tests for Cairo Renderer."""

import pytest
import tempfile
from pathlib import Path

from comix.page.page import Page
from comix.cobject.panel.panel import Panel
from comix.cobject.bubble.bubble import SpeechBubble, ThoughtBubble
from comix.cobject.character.character import Stickman, SimpleFace
from comix.cobject.text.text import Text, SFX
from comix.cobject.shapes.shapes import Rectangle, Circle, Line
from comix.cobject.panel.panel import Border

# Skip all tests if Cairo is not available
try:
    from comix.renderer.cairo_renderer import CairoRenderer
    CAIRO_AVAILABLE = True
except ImportError:
    CAIRO_AVAILABLE = False


@pytest.mark.skipif(not CAIRO_AVAILABLE, reason="Cairo not installed")
class TestCairoRenderer:
    """Tests for CairoRenderer class."""

    def test_render_png_empty_page(self):
        """Test rendering an empty page to PNG."""
        page = Page(width=400, height=300)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")

            assert Path(output_path).exists()
            # Check file is a valid PNG (starts with PNG signature)
            with open(output_path, "rb") as png_file:
                signature = png_file.read(8)
                assert signature[:4] == b"\x89PNG"
            Path(output_path).unlink()

    def test_render_pdf_empty_page(self):
        """Test rendering an empty page to PDF."""
        page = Page(width=400, height=300)

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="pdf")

            assert Path(output_path).exists()
            # Check file is a valid PDF (starts with %PDF)
            with open(output_path, "rb") as pdf_file:
                signature = pdf_file.read(4)
                assert signature == b"%PDF"
            Path(output_path).unlink()

    def test_render_png_via_page(self):
        """Test rendering PNG via Page.render() method."""
        page = Page(width=400, height=300)
        panel = Panel(width=300, height=200)
        panel.move_to((200, 150))
        page.add(panel)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            output_path = page.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_pdf_via_page(self):
        """Test rendering PDF via Page.render() method."""
        page = Page(width=400, height=300)
        panel = Panel(width=300, height=200)
        panel.move_to((200, 150))
        page.add(panel)

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            output_path = page.render(f.name, format="pdf")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_panel(self):
        """Test rendering a panel."""
        page = Page(width=400, height=300)
        panel = Panel(width=300, height=200, background_color="#EEEEEE")
        panel.move_to((200, 150))
        page.add(panel)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            # Verify file size is reasonable (not empty)
            assert Path(output_path).stat().st_size > 100
            Path(output_path).unlink()

    def test_render_bubble(self):
        """Test rendering a speech bubble."""
        page = Page(width=400, height=300)
        bubble = SpeechBubble(text="Hello!").move_to((200, 150))
        page.add(bubble)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_thought_bubble(self):
        """Test rendering a thought bubble."""
        page = Page(width=400, height=300)
        bubble = ThoughtBubble(text="Hmm...").move_to((200, 150))
        page.add(bubble)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_bubble_with_emphasis(self):
        """Test rendering a bubble with emphasis effect."""
        page = Page(width=400, height=300)
        bubble = SpeechBubble(text="Important!", emphasis=True).move_to((200, 150))
        page.add(bubble)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_stickman(self):
        """Test rendering a stickman character."""
        page = Page(width=400, height=300)
        char = Stickman(name="Test").move_to((200, 150))
        page.add(char)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_simple_face(self):
        """Test rendering a simple face character."""
        page = Page(width=400, height=300)
        face = SimpleFace(name="Smiley").move_to((200, 150))
        face.set_expression("happy")
        page.add(face)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_simple_face_neutral(self):
        """Test rendering a simple face with neutral expression."""
        page = Page(width=400, height=300)
        face = SimpleFace(name="Neutral").move_to((200, 150))
        page.add(face)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_shapes(self):
        """Test rendering basic shapes."""
        page = Page(width=400, height=300)
        rect = Rectangle(width=100, height=50).move_to((100, 100))
        circle = Circle(radius=30).move_to((250, 100))
        line = Line(start=(0, 0), end=(100, 100)).move_to((200, 200))
        page.add(rect, circle, line)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_rounded_rectangle(self):
        """Test rendering a rounded rectangle."""
        page = Page(width=400, height=300)
        rect = Rectangle(width=100, height=50, corner_radius=10).move_to((200, 150))
        page.add(rect)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_dashed_line(self):
        """Test rendering a dashed line."""
        page = Page(width=400, height=300)
        line = Line(start=(0, 0), end=(200, 0), stroke_style="dashed").move_to((100, 150))
        page.add(line)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_text(self):
        """Test rendering text."""
        page = Page(width=400, height=300)
        text = Text(text="Hello World", font_size=24).move_to((200, 150))
        page.add(text)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_sfx(self):
        """Test rendering SFX text with outline."""
        page = Page(width=400, height=300)
        sfx = SFX(text="BOOM!", color="#FF0000", outline=True).move_to((200, 150))
        page.add(sfx)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_with_opacity(self):
        """Test rendering objects with opacity."""
        page = Page(width=400, height=300)
        rect = Rectangle(width=100, height=100).move_to((200, 150)).set_opacity(0.5)
        page.add(rect)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
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

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            # Verify file size for complex scene
            assert Path(output_path).stat().st_size > 1000
            Path(output_path).unlink()

    def test_quality_low(self):
        """Test rendering with low quality (72 DPI)."""
        page = Page(width=400, height=300)
        panel = Panel(width=300, height=200)
        panel.move_to((200, 150))
        page.add(panel)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png", quality="low")
            assert Path(output_path).exists()
            assert Path(output_path).stat().st_size > 0  # Verify file is not empty
            Path(output_path).unlink()

    def test_quality_high(self):
        """Test rendering with high quality (300 DPI)."""
        page = Page(width=400, height=300)
        panel = Panel(width=300, height=200)
        panel.move_to((200, 150))
        page.add(panel)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png", quality="high")
            assert Path(output_path).exists()
            # High quality should produce larger file
            size_high = Path(output_path).stat().st_size
            assert size_high > 0
            Path(output_path).unlink()

    def test_quality_comparison(self):
        """Test that higher quality produces larger files."""
        page = Page(width=400, height=300)
        panel = Panel(width=300, height=200)
        panel.move_to((200, 150))
        page.add(panel)

        renderer = CairoRenderer(page)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f_low:
            output_low = renderer.render(f_low.name, format="png", quality="low")
            size_low = Path(output_low).stat().st_size

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f_high:
            output_high = renderer.render(f_high.name, format="png", quality="high")
            size_high = Path(output_high).stat().st_size

        # High quality should produce larger file
        assert size_high > size_low

        Path(output_low).unlink()
        Path(output_high).unlink()

    def test_auto_format_detection_png(self):
        """Test automatic format detection from file extension for PNG."""
        page = Page(width=400, height=300)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name)  # No format specified
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_auto_format_detection_pdf(self):
        """Test automatic format detection from file extension for PDF."""
        page = Page(width=400, height=300)

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name)  # No format specified
            assert Path(output_path).exists()
            # Verify it's a PDF
            with open(output_path, "rb") as pdf_file:
                signature = pdf_file.read(4)
                assert signature == b"%PDF"
            Path(output_path).unlink()

    def test_render_nested_objects(self):
        """Test rendering nested CObjects (parent-child hierarchy)."""
        page = Page(width=400, height=300)
        panel = Panel(width=300, height=200)
        panel.move_to((200, 150))

        rect = Rectangle(width=50, height=30).move_to((100, 100))
        circle = Circle(radius=20).move_to((150, 100))
        panel.add_content(rect, circle)
        page.add(panel)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_panel_with_rounded_border(self):
        """Test rendering a panel with rounded borders."""
        page = Page(width=400, height=300)
        panel = Panel(width=300, height=200, border=Border(color="#000000", width=3, radius=15))
        panel.move_to((200, 150))
        page.add(panel)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_panel_with_dashed_border(self):
        """Test rendering a panel with dashed border."""
        page = Page(width=400, height=300)
        panel = Panel(width=300, height=200, border=Border(color="#000000", width=2, style="dashed"))
        panel.move_to((200, 150))
        page.add(panel)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_creates_directory(self):
        """Test that render creates output directory if it doesn't exist."""
        page = Page(width=400, height=300)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "subdir" / "output.png"
            renderer = CairoRenderer(page)
            result = renderer.render(str(output_path), format="png")
            assert Path(result).exists()
            Path(result).unlink()


@pytest.mark.skipif(not CAIRO_AVAILABLE, reason="Cairo not installed")
class TestCairoRendererIntegration:
    """Integration tests for Cairo renderer with Page class."""

    def test_page_render_png_format_option(self):
        """Test Page.render() with format='png' option."""
        page = Page(width=400, height=300)
        page.add(Panel(width=300, height=200).move_to((200, 150)))

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            output = page.render(f.name, format="png")
            assert Path(output).exists()
            Path(output).unlink()

    def test_page_render_pdf_format_option(self):
        """Test Page.render() with format='pdf' option."""
        page = Page(width=400, height=300)
        page.add(Panel(width=300, height=200).move_to((200, 150)))

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            output = page.render(f.name, format="pdf")
            assert Path(output).exists()
            Path(output).unlink()

    def test_page_render_quality_options(self):
        """Test Page.render() with different quality options."""
        page = Page(width=400, height=300)
        page.add(Panel(width=300, height=200).move_to((200, 150)))

        for quality in ["low", "medium", "high"]:
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
                output = page.render(f.name, format="png", quality=quality)
                assert Path(output).exists()
                Path(output).unlink()
