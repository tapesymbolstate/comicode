"""Tests for Cairo Renderer."""

import pytest
import tempfile
from pathlib import Path

from comix.page.page import Page
from comix.cobject.panel.panel import Panel
from comix.cobject.bubble.bubble import SpeechBubble, ThoughtBubble
from comix.cobject.character.character import Stickman, SimpleFace, ChubbyStickman, Robot
from comix.cobject.text.text import Text, SFX
from comix.cobject.shapes.shapes import Rectangle, Circle, Line
from comix.cobject.panel.panel import Border
from comix.cobject.image.image import Image
from comix.effect.effect import MotionLines, FocusLines, ImpactEffect, ShakeEffect

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

    def test_render_stickman_with_expression(self):
        """Test rendering a stickman with expression features."""
        page = Page(width=400, height=300)
        char = Stickman(name="Happy", expression="happy").move_to((200, 150))
        page.add(char)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_stickman_all_expressions(self):
        """Test rendering stickman with all expression types."""
        expressions = ["neutral", "happy", "sad", "angry", "surprised", "confused",
                      "sleepy", "excited", "scared", "smirk", "crying"]
        for expr_name in expressions:
            page = Page(width=400, height=300)
            char = Stickman(name="Expressive", expression=expr_name).move_to((200, 150))
            page.add(char)

            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
                renderer = CairoRenderer(page)
                output_path = renderer.render(f.name, format="png")
                assert Path(output_path).exists()
                Path(output_path).unlink()

    def test_render_stickman_with_expression_and_pose(self):
        """Test rendering stickman with both expression and pose."""
        page = Page(width=400, height=300)
        char = Stickman(name="Waving", expression="happy", pose="waving").move_to((200, 150))
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

    def test_render_chubby_stickman(self):
        """Test rendering a chubby stickman character."""
        page = Page(width=400, height=300)
        chubby = ChubbyStickman(name="Chunky").move_to((200, 150))
        page.add(chubby)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_chubby_stickman_with_expression(self):
        """Test rendering a chubby stickman with expression."""
        page = Page(width=400, height=300)
        chubby = ChubbyStickman(name="Happy", expression="happy").move_to((200, 150))
        page.add(chubby)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_chubby_stickman_with_pose(self):
        """Test rendering a chubby stickman with different poses."""
        for pose_name in ["standing", "waving", "jumping", "cheering"]:
            page = Page(width=400, height=300)
            chubby = ChubbyStickman(name="Poser", pose=pose_name).move_to((200, 150))
            page.add(chubby)

            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
                renderer = CairoRenderer(page)
                output_path = renderer.render(f.name, format="png")
                assert Path(output_path).exists()
                Path(output_path).unlink()

    def test_render_chubby_stickman_facing_left(self):
        """Test rendering a chubby stickman facing left."""
        page = Page(width=400, height=300)
        chubby = ChubbyStickman(name="Lefty", facing="left").move_to((200, 150))
        page.add(chubby)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_chubby_stickman_all_expressions(self):
        """Test rendering a chubby stickman with all expression types."""
        expressions = ["neutral", "happy", "sad", "angry", "surprised",
                       "confused", "sleepy", "excited", "scared", "smirk", "crying"]
        for expr_name in expressions:
            page = Page(width=400, height=300)
            chubby = ChubbyStickman(name="Expressive", expression=expr_name).move_to((200, 150))
            page.add(chubby)

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

    def test_render_robot(self):
        """Test rendering a robot character."""
        page = Page(width=400, height=300)
        robot = Robot(name="Robo").move_to((200, 150))
        page.add(robot)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_robot_with_expression(self):
        """Test rendering a robot with expression."""
        page = Page(width=400, height=300)
        robot = Robot(name="HappyBot", expression="happy").move_to((200, 150))
        page.add(robot)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_robot_all_expressions(self):
        """Test rendering a robot with all expression types."""
        expressions = ["neutral", "happy", "sad", "angry", "surprised",
                       "confused", "sleepy", "excited", "scared"]
        for expr_name in expressions:
            page = Page(width=400, height=300)
            robot = Robot(name="Expressive", expression=expr_name).move_to((200, 150))
            page.add(robot)

            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
                renderer = CairoRenderer(page)
                output_path = renderer.render(f.name, format="png")
                assert Path(output_path).exists()
                Path(output_path).unlink()

    def test_render_robot_with_pose(self):
        """Test rendering a robot with different poses."""
        for pose_name in ["standing", "waving", "jumping", "cheering"]:
            page = Page(width=400, height=300)
            robot = Robot(name="Poser", pose=pose_name).move_to((200, 150))
            page.add(robot)

            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
                renderer = CairoRenderer(page)
                output_path = renderer.render(f.name, format="png")
                assert Path(output_path).exists()
                Path(output_path).unlink()

    def test_render_robot_facing_left(self):
        """Test rendering a robot facing left."""
        page = Page(width=400, height=300)
        robot = Robot(name="Lefty", facing="left").move_to((200, 150))
        page.add(robot)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_robot_without_antenna(self):
        """Test rendering a robot without antenna."""
        page = Page(width=400, height=300)
        robot = Robot(name="NoAntenna", antenna=False).move_to((200, 150))
        page.add(robot)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_robot_custom_colors(self):
        """Test rendering a robot with custom colors."""
        page = Page(width=400, height=300)
        robot = Robot(
            name="ColorBot",
            color="#FF0000",
            fill_color="#00FF00",
            panel_color="#0000FF",
            screen_color="#FFFF00",
            led_color="#FF00FF",
        ).move_to((200, 150))
        page.add(robot)

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


@pytest.mark.skipif(not CAIRO_AVAILABLE, reason="Cairo not installed")
class TestCairoRendererCoverage:
    """Additional tests to improve CairoRenderer test coverage."""

    def test_render_image_with_base64_data(self):
        """Test rendering an image element with base64 data."""
        page = Page(width=400, height=300)

        # 1x1 red PNG
        png_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8DwHwAFBQIAX8jx0gAAAABJRU5ErkJggg=="

        img = Image(width=100, height=100)
        img.set_base64_data(png_b64, "image/png")
        img.move_to((200, 150))
        page.add(img)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            assert Path(output_path).stat().st_size > 100
            Path(output_path).unlink()

    def test_render_image_cover_mode(self):
        """Test rendering image with fit='cover' mode."""
        page = Page(width=400, height=300)

        png_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8DwHwAFBQIAX8jx0gAAAABJRU5ErkJggg=="

        img = Image(width=100, height=50)  # Non-square to test cover mode
        img.set_base64_data(png_b64, "image/png")
        img.set_fit("cover")
        img.move_to((200, 150))
        page.add(img)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_image_fill_mode(self):
        """Test rendering image with fit='fill' mode (no aspect ratio preservation)."""
        page = Page(width=400, height=300)

        png_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8DwHwAFBQIAX8jx0gAAAABJRU5ErkJggg=="

        img = Image(width=100, height=50)
        img.set_base64_data(png_b64, "image/png")
        img.set_fit("fill")
        img.preserve_aspect_ratio = False
        img.move_to((200, 150))
        page.add(img)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_image_placeholder_no_data(self):
        """Test image placeholder rendering when base64_data is None."""
        page = Page(width=400, height=300)

        img = Image(width=100, height=100)
        img.move_to((200, 150))
        # No base64 data set - should render placeholder
        page.add(img)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_text_empty_string(self):
        """Test rendering text element with empty string."""
        page = Page(width=400, height=300)
        text = Text(text="").move_to((200, 150))
        page.add(text)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_dotted_line(self):
        """Test rendering a dotted line."""
        page = Page(width=400, height=300)
        line = Line(start=(0, 0), end=(200, 0), stroke_style="dotted").move_to((100, 150))
        page.add(line)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_effect_motion_lines(self):
        """Test rendering motion lines effect."""
        page = Page(width=400, height=300)
        panel = Panel(width=300, height=200)
        panel.move_to((200, 150))

        # MotionLines with position tuple
        effect = MotionLines(position=(200, 150), direction=0.0, intensity=0.7, seed=42)
        page.add_effect(effect)
        page.add(panel)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_effect_focus_lines(self):
        """Test rendering focus lines effect."""
        page = Page(width=400, height=300)
        panel = Panel(width=300, height=200)
        panel.move_to((200, 150))

        # FocusLines with position tuple
        effect = FocusLines(position=(200, 150), intensity=0.8, seed=42)
        page.add_effect(effect)
        page.add(panel)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_effect_impact(self):
        """Test rendering impact effect."""
        page = Page(width=400, height=300)
        panel = Panel(width=300, height=200)
        panel.move_to((200, 150))

        # ImpactEffect with position tuple
        effect = ImpactEffect(position=(200, 150), intensity=1.0, seed=42)
        page.add_effect(effect)
        page.add(panel)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_effect_shake(self):
        """Test rendering shake effect."""
        page = Page(width=400, height=300)
        panel = Panel(width=300, height=200)
        panel.move_to((200, 150))

        # ShakeEffect with target CObject
        effect = ShakeEffect(target=panel, intensity=0.5, seed=42)
        page.add_effect(effect)
        page.add(panel)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_effect_with_opacity(self):
        """Test rendering effect with custom opacity."""
        page = Page(width=400, height=300)

        effect = MotionLines(position=(200, 150), direction=0.0, intensity=0.5, opacity=0.3, seed=42)
        page.add_effect(effect)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_effect_background_z_index(self):
        """Test rendering effects with negative z_index (behind objects)."""
        page = Page(width=400, height=300)
        panel = Panel(width=300, height=200)
        panel.move_to((200, 150))

        # Effect with negative z_index renders behind panel
        effect = FocusLines(position=(200, 150), z_index=-1, seed=42)
        page.add_effect(effect)
        page.add(panel)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_effect_foreground_z_index(self):
        """Test rendering effects with positive z_index (in front)."""
        page = Page(width=400, height=300)
        panel = Panel(width=300, height=200)
        panel.move_to((200, 150))

        # Effect with positive z_index renders in front of panel
        effect = FocusLines(position=(200, 150), z_index=10, seed=42)
        page.add_effect(effect)
        page.add(panel)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_book_multiple_pages(self):
        """Test rendering multiple pages to single PDF using render_book."""
        from comix.page.book import Book

        page1 = Page(width=400, height=300)
        page1.add(Panel(width=300, height=200).move_to((200, 150)))

        page2 = Page(width=400, height=300)
        page2.add(Panel(width=300, height=200).move_to((200, 150)))

        book = Book()
        book.add_page(page1)
        book.add_page(page2)

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            renderer = CairoRenderer(page1)  # Use first page for renderer
            output_path = renderer.render_book([page1, page2], f.name)
            assert Path(output_path).exists()
            # Verify it's a valid PDF
            with open(output_path, "rb") as pdf_file:
                signature = pdf_file.read(4)
                assert signature == b"%PDF"
            Path(output_path).unlink()

    def test_render_book_different_page_sizes(self):
        """Test render_book handles pages with different dimensions."""
        page1 = Page(width=400, height=300)
        page1.add(Panel(width=300, height=200).move_to((200, 150)))

        page2 = Page(width=800, height=600)  # Different size
        page2.add(Panel(width=700, height=500).move_to((400, 300)))

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            renderer = CairoRenderer(page1)
            output_path = renderer.render_book([page1, page2], f.name)
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_book_with_quality(self):
        """Test render_book respects quality parameter."""
        page1 = Page(width=400, height=300)
        page1.add(Panel(width=300, height=200).move_to((200, 150)))

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            renderer = CairoRenderer(page1)
            output_path = renderer.render_book([page1], f.name, quality="high")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_multiline_text(self):
        """Test rendering multiline text."""
        page = Page(width=400, height=300)
        text = Text(text="Line 1\nLine 2\nLine 3", font_size=16).move_to((200, 150))
        page.add(text)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_text_alignment(self):
        """Test rendering text with different alignments."""
        page = Page(width=400, height=300)

        text_left = Text(text="Left", font_size=16, align="left").move_to((100, 100))
        text_center = Text(text="Center", font_size=16, align="center").move_to((200, 150))
        text_right = Text(text="Right", font_size=16, align="right").move_to((300, 200))

        page.add(text_left, text_center, text_right)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_sfx_without_outline(self):
        """Test rendering SFX text without outline."""
        page = Page(width=400, height=300)
        sfx = SFX(text="POW!", color="#0000FF", outline=False).move_to((200, 150))
        page.add(sfx)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_shapes_with_fill(self):
        """Test rendering shapes with fill colors."""
        page = Page(width=400, height=300)
        rect = Rectangle(width=100, height=50, fill_color="#FF0000").move_to((200, 150))
        circle = Circle(radius=30, fill_color="#00FF00").move_to((100, 100))
        page.add(rect, circle)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_shapes_without_stroke(self):
        """Test rendering shapes with only fill (no stroke)."""
        page = Page(width=400, height=300)
        rect = Rectangle(width=100, height=50, fill_color="#FF0000", stroke_color="none").move_to((200, 150))
        page.add(rect)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_character_expressions(self):
        """Test rendering characters with different expressions."""
        page = Page(width=800, height=300)

        expressions = ["neutral", "happy", "sad", "angry", "surprised"]
        for i, expr in enumerate(expressions):
            face = SimpleFace(name=expr).move_to((100 + i * 140, 150))
            face.set_expression(expr)
            page.add(face)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_stickman_facing_directions(self):
        """Test rendering stickman facing different directions."""
        page = Page(width=600, height=300)

        stickman_left = Stickman(name="Left").move_to((150, 150)).face("left")
        stickman_right = Stickman(name="Right").move_to((300, 150)).face("right")
        stickman_front = Stickman(name="Front").move_to((450, 150)).face("front")

        page.add(stickman_left, stickman_right, stickman_front)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()


@pytest.mark.skipif(not CAIRO_AVAILABLE, reason="Cairo not installed")
class TestCairoRendererEdgeCases:
    """Additional tests for edge cases in CairoRenderer."""

    def test_render_custom_cobject_generic_fallback(self):
        """Test rendering custom CObject with unknown type uses generic rendering."""
        from comix.cobject.cobject import CObject
        import numpy as np

        class CustomObject(CObject):
            def __init__(self):
                super().__init__()
                self._points = np.array(
                    [[0, 0], [50, 25], [100, 0], [100, 50], [0, 50]],
                    dtype=np.float64,
                )

            def get_render_data(self):
                data = super().get_render_data()
                data["type"] = "UnknownCustomType"  # Unknown type triggers generic rendering
                return data

        page = Page(width=400, height=300)
        custom = CustomObject()
        custom.move_to((200, 150))
        page.add(custom)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_character_unknown_style(self):
        """Test rendering character with unknown style falls back to generic."""
        from comix.cobject.cobject import CObject
        import numpy as np

        class CustomCharacter(CObject):
            def __init__(self):
                super().__init__()
                self._points = np.array(
                    [[0, 0], [50, 100], [0, 100]],
                    dtype=np.float64,
                )

            def get_render_data(self):
                data = super().get_render_data()
                data["type"] = "Character"
                data["style"] = "custom_unknown_style"  # Unknown style
                return data

        page = Page(width=400, height=300)
        char = CustomCharacter()
        char.move_to((200, 150))
        page.add(char)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_effect_polygon_no_stroke(self):
        """Test rendering effect with polygon that has no stroke."""
        from comix.effect.effect import FocusLines

        page = Page(width=400, height=300)
        # FocusLines with fill_background creates filled polygons
        effect = FocusLines(
            position=(200, 150),
            fill_background=True,
            background_color="#FFFF00",
            seed=42,
        )
        page.add_effect(effect)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_effect_circle_elements(self):
        """Test rendering effects that include circle elements."""
        from comix.effect.effect import AppearEffect

        page = Page(width=400, height=300)
        # AppearEffect with sparkle style generates circles
        effect = AppearEffect(position=(200, 150), style="sparkle", seed=42)
        page.add_effect(effect)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_bubble_with_dashed_border(self):
        """Test rendering bubble with dashed border style."""
        from comix.cobject.bubble.bubble import WhisperBubble

        page = Page(width=400, height=300)
        # WhisperBubble uses dashed border by default
        bubble = WhisperBubble(text="Whisper text")
        bubble.move_to((200, 150))
        page.add(bubble)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_panel_dotted_border(self):
        """Test rendering panel with dotted border style."""
        page = Page(width=400, height=300)
        panel = Panel(width=300, height=200, border=Border(color="#000000", width=2, style="dotted"))
        panel.move_to((200, 150))
        page.add(panel)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_stickman_insufficient_points(self):
        """Test rendering stickman gracefully handles insufficient points."""
        from comix.cobject.cobject import CObject
        import numpy as np

        class MinimalStickman(CObject):
            def __init__(self):
                super().__init__()
                # Only 1 point - not enough to draw
                self._points = np.array([[0, 0]], dtype=np.float64)

            def get_render_data(self):
                data = super().get_render_data()
                data["type"] = "Character"
                data["style"] = "stickman"
                return data

        page = Page(width=400, height=300)
        stickman = MinimalStickman()
        stickman.move_to((200, 150))
        page.add(stickman)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            # Should not raise error - just renders nothing for the stickman
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_panel_background_image(self, tmp_path):
        """Test rendering panel with background image."""
        import base64

        # Create a small test PNG
        png_data = base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8DwHwAFBQIAX8jx0gAAAABJRU5ErkJggg=="
        )
        image_path = tmp_path / "bg.png"
        image_path.write_bytes(png_data)

        page = Page(width=400, height=300)
        panel = Panel(width=300, height=200)
        panel.set_background(image=str(image_path))
        panel.move_to((200, 150))
        page.add(panel)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_panel_background_image_with_rounded_corners(self, tmp_path):
        """Test panel background image respects rounded corners."""
        import base64

        png_data = base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8DwHwAFBQIAX8jx0gAAAABJRU5ErkJggg=="
        )
        image_path = tmp_path / "bg.png"
        image_path.write_bytes(png_data)

        page = Page(width=400, height=300)
        panel = Panel(width=300, height=200, border=Border(radius=20))
        panel.set_background(image=str(image_path))
        panel.move_to((200, 150))
        page.add(panel)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_effect_with_zero_opacity(self):
        """Test rendering effect with zero opacity (invisible)."""
        from comix.effect.effect import FocusLines

        page = Page(width=400, height=300)
        effect = FocusLines(position=(200, 150), opacity=0.0, seed=42)
        page.add_effect(effect)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_generic_object_empty_points(self):
        """Test generic object rendering handles empty points gracefully."""
        from comix.cobject.cobject import CObject
        import numpy as np

        class EmptyPointsObject(CObject):
            def __init__(self):
                super().__init__()
                self._points = np.array([], dtype=np.float64).reshape(0, 2)

            def get_render_data(self):
                data = super().get_render_data()
                data["type"] = "UnknownType"
                return data

        page = Page(width=400, height=300)
        obj = EmptyPointsObject()
        obj.move_to((200, 150))
        page.add(obj)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            # Should not raise error
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()


class TestSimpleFaceExpressionCairo:
    """Tests for SimpleFace expression rendering with Cairo renderer."""

    def test_render_all_expressions_cairo(self):
        """Test all 6 standard expressions render with Cairo."""
        expressions = ["neutral", "happy", "sad", "angry", "surprised", "confused"]

        for expr in expressions:
            page = Page(width=400, height=300)
            face = SimpleFace(name=expr).move_to((200, 150))
            face.set_expression(expr)
            page.add(face)

            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
                renderer = CairoRenderer(page)
                output_path = renderer.render(f.name, format="png")
                assert Path(output_path).exists()
                Path(output_path).unlink()

    def test_render_curved_eyes_cairo(self):
        """Test curved eyes (happy) render correctly with Cairo."""
        from comix.cobject.character.character import Expression

        page = Page(width=400, height=300)
        face = SimpleFace(name="CurvedEyes").move_to((200, 150))
        face._expression = Expression(
            name="custom", eyes="curved", mouth="smile", eyebrows="normal"
        )
        page.add(face)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_narrow_eyes_cairo(self):
        """Test narrow eyes (angry) render correctly with Cairo."""
        from comix.cobject.character.character import Expression

        page = Page(width=400, height=300)
        face = SimpleFace(name="NarrowEyes").move_to((200, 150))
        face._expression = Expression(
            name="custom", eyes="narrow", mouth="frown", eyebrows="furrowed"
        )
        page.add(face)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_wide_eyes_cairo(self):
        """Test wide eyes (surprised) render correctly with Cairo."""
        from comix.cobject.character.character import Expression

        page = Page(width=400, height=300)
        face = SimpleFace(name="WideEyes").move_to((200, 150))
        face._expression = Expression(
            name="custom", eyes="wide", mouth="open", eyebrows="raised"
        )
        page.add(face)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_uneven_eyes_cairo(self):
        """Test uneven eyes (confused) render correctly with Cairo."""
        from comix.cobject.character.character import Expression

        page = Page(width=400, height=300)
        face = SimpleFace(name="UnevenEyes").move_to((200, 150))
        face._expression = Expression(
            name="custom", eyes="uneven", mouth="wavy", eyebrows="raised"
        )
        page.add(face)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_droopy_eyes_cairo(self):
        """Test droopy eyes (sad) render correctly with Cairo."""
        from comix.cobject.character.character import Expression

        page = Page(width=400, height=300)
        face = SimpleFace(name="DroopyEyes").move_to((200, 150))
        face._expression = Expression(
            name="custom", eyes="droopy", mouth="frown", eyebrows="worried"
        )
        page.add(face)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()

    def test_render_all_mouth_types_cairo(self):
        """Test all mouth types render with Cairo."""
        from comix.cobject.character.character import Expression

        mouth_types = ["normal", "smile", "frown", "open", "wavy"]

        for mouth in mouth_types:
            page = Page(width=400, height=300)
            face = SimpleFace(name=f"Mouth_{mouth}").move_to((200, 150))
            face._expression = Expression(
                name="custom", eyes="normal", mouth=mouth, eyebrows="normal"
            )
            page.add(face)

            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
                renderer = CairoRenderer(page)
                output_path = renderer.render(f.name, format="png")
                assert Path(output_path).exists()
                Path(output_path).unlink()

    def test_render_all_eyebrow_types_cairo(self):
        """Test all eyebrow types render with Cairo."""
        from comix.cobject.character.character import Expression

        eyebrow_types = ["normal", "raised", "worried", "furrowed"]

        for brow in eyebrow_types:
            page = Page(width=400, height=300)
            face = SimpleFace(name=f"Brows_{brow}").move_to((200, 150))
            face._expression = Expression(
                name="custom", eyes="normal", mouth="normal", eyebrows=brow
            )
            page.add(face)

            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
                renderer = CairoRenderer(page)
                output_path = renderer.render(f.name, format="png")
                assert Path(output_path).exists()
                Path(output_path).unlink()

    def test_render_expression_with_custom_colors_cairo(self):
        """Test expression rendering with custom colors in Cairo."""
        page = Page(width=400, height=300)
        face = SimpleFace(name="Custom", color="#0000FF", fill_color="#00FF00")
        face.move_to((200, 150))
        face.set_expression("happy")
        page.add(face)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            renderer = CairoRenderer(page)
            output_path = renderer.render(f.name, format="png")
            assert Path(output_path).exists()
            Path(output_path).unlink()
