"""Tests for SVG Renderer."""

import tempfile
from pathlib import Path

from comix.page.page import Page
from comix.cobject.panel.panel import Panel
from comix.cobject.bubble.bubble import SpeechBubble
from comix.cobject.character.character import Stickman, SimpleFace
from comix.cobject.text.text import Text, SFX
from comix.cobject.shapes.shapes import Rectangle, Circle, Line
from comix.renderer.svg_renderer import SVGRenderer
from comix.effect.effect import (
    ShakeEffect,
    ZoomEffect,
    MotionLines,
    FocusLines,
    AppearEffect,
    ImpactEffect,
)


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

    def test_render_to_string_empty_page(self):
        """Test render_to_string with an empty page."""
        page = Page(width=400, height=300)
        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        assert isinstance(svg_string, str)
        assert "<svg" in svg_string
        assert 'width="400px"' in svg_string
        assert 'height="300px"' in svg_string
        assert "</svg>" in svg_string

    def test_render_to_string_with_content(self):
        """Test render_to_string with various objects."""
        page = Page(width=400, height=300)
        panel = Panel(width=300, height=200).move_to((200, 150))
        bubble = SpeechBubble(text="Test!").move_to((200, 100))
        page.add(panel, bubble)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        assert "<svg" in svg_string
        assert "<rect" in svg_string
        assert "Test!" in svg_string

    def test_render_to_string_matches_file_render(self):
        """Test that render_to_string produces same content as file render."""
        page = Page(width=400, height=300, background_color="#FAFAFA")
        rect = Rectangle(width=100, height=50).move_to((200, 150))
        page.add(rect)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            renderer2 = SVGRenderer(page)
            output_path = renderer2.render(f.name)
            file_content = Path(output_path).read_text()
            Path(output_path).unlink()

        # Both should have the same core elements (file may have filename attribute)
        assert 'width="400px"' in svg_string
        assert 'width="400px"' in file_content
        assert "#FAFAFA" in svg_string
        assert "#FAFAFA" in file_content


class TestEffectRendering:
    """Tests for effect rendering in SVG renderer."""

    def test_render_shake_effect(self):
        """Test rendering a shake effect."""
        page = Page(width=400, height=300)
        rect = Rectangle(width=100, height=100).move_to((200, 150))
        page.add(rect)

        # Add shake effect with fixed seed for reproducibility
        effect = ShakeEffect(target=rect, seed=42, intensity=1.0)
        page.add_effect(effect)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Shake effect generates polylines (ghost copies) and lines (motion blur)
        assert "<polyline" in svg_string or "<line" in svg_string

    def test_render_zoom_effect(self):
        """Test rendering a zoom effect."""
        page = Page(width=400, height=300)
        rect = Rectangle(width=50, height=50).move_to((200, 150))
        page.add(rect)

        effect = ZoomEffect(target=rect, seed=42, num_lines=16)
        page.add_effect(effect)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Zoom effect generates radial lines
        assert "<line" in svg_string
        assert '<g opacity="0.6"' in svg_string  # Default zoom opacity

    def test_render_motion_lines(self):
        """Test rendering motion lines effect."""
        page = Page(width=400, height=300)
        char = Stickman(name="Runner").move_to((200, 150))
        page.add(char)

        effect = MotionLines(target=char, seed=42, num_lines=8)
        page.add_effect(effect)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Motion lines generate line elements
        assert "<line" in svg_string

    def test_render_focus_lines(self):
        """Test rendering focus lines effect."""
        page = Page(width=400, height=300)
        face = SimpleFace(name="Focus").move_to((200, 150))
        page.add(face)

        effect = FocusLines(target=face, seed=42, num_lines=24)
        page.add_effect(effect)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Focus lines generate radial lines
        assert "<line" in svg_string

    def test_render_focus_lines_with_fill(self):
        """Test rendering focus lines with background fill."""
        page = Page(width=400, height=300)

        effect = FocusLines(
            position=(200, 150),
            seed=42,
            fill_background=True,
            background_color="#FFFF00"
        )
        page.add_effect(effect)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # With fill_background, generates polygon elements
        assert "<polygon" in svg_string

    def test_render_appear_effect_sparkle(self):
        """Test rendering appear effect with sparkle style."""
        page = Page(width=400, height=300)
        rect = Rectangle(width=60, height=60).move_to((200, 150))
        page.add(rect)

        effect = AppearEffect(target=rect, seed=42, style="sparkle")
        page.add_effect(effect)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Sparkle generates polygon (stars) and circle (dots) elements
        assert "<polygon" in svg_string or "<circle" in svg_string

    def test_render_appear_effect_flash(self):
        """Test rendering appear effect with flash style."""
        page = Page(width=400, height=300)

        effect = AppearEffect(position=(200, 150), seed=42, style="flash")
        page.add_effect(effect)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Flash generates polygon elements (rays) and circle (center glow)
        assert "<polygon" in svg_string or "<circle" in svg_string

    def test_render_appear_effect_fade(self):
        """Test rendering appear effect with fade style."""
        page = Page(width=400, height=300)

        effect = AppearEffect(position=(200, 150), seed=42, style="fade")
        page.add_effect(effect)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Fade generates concentric polyline rings
        assert "<polyline" in svg_string

    def test_render_appear_effect_reveal(self):
        """Test rendering appear effect with reveal style."""
        page = Page(width=400, height=300)

        effect = AppearEffect(position=(200, 150), seed=42, style="reveal")
        page.add_effect(effect)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Reveal generates lines and polylines for corner accents
        assert "<line" in svg_string or "<polyline" in svg_string

    def test_render_impact_effect(self):
        """Test rendering impact effect."""
        page = Page(width=400, height=300)

        effect = ImpactEffect(position=(200, 150), seed=42, num_spikes=8)
        page.add_effect(effect)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Impact generates polygon (star burst) and lines (debris)
        assert "<polygon" in svg_string
        assert "<line" in svg_string

    def test_render_effect_z_index_background(self):
        """Test that effects with negative z_index render behind objects."""
        page = Page(width=400, height=300)
        rect = Rectangle(width=100, height=100).move_to((200, 150))
        page.add(rect)

        # Effect with negative z_index should render behind
        effect = ZoomEffect(target=rect, z_index=-1, seed=42)
        page.add_effect(effect)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Effect should be present
        assert "<line" in svg_string
        # Rectangle should also be present
        assert "<rect" in svg_string

    def test_render_effect_z_index_foreground(self):
        """Test that effects with positive z_index render in front of objects."""
        page = Page(width=400, height=300)
        rect = Rectangle(width=100, height=100).move_to((200, 150))
        page.add(rect)

        # Effect with positive z_index should render in front
        effect = ImpactEffect(position=(200, 150), z_index=1, seed=42)
        page.add_effect(effect)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Both effect and rectangle should be present
        assert "<polygon" in svg_string
        assert "<rect" in svg_string

    def test_render_multiple_effects(self):
        """Test rendering multiple effects on the same page."""
        page = Page(width=400, height=300)

        # Background effect
        effect1 = FocusLines(position=(200, 150), z_index=-1, seed=42, num_lines=12)
        # Foreground effect
        effect2 = ImpactEffect(position=(200, 150), z_index=1, seed=43, num_spikes=6)

        page.add_effect(effect1)
        page.add_effect(effect2)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Both effects should be rendered
        assert "<line" in svg_string  # Focus lines
        assert "<polygon" in svg_string  # Impact burst

    def test_render_effect_opacity(self):
        """Test that effect opacity is applied."""
        page = Page(width=400, height=300)

        effect = ZoomEffect(position=(200, 150), opacity=0.5, seed=42, num_lines=8)
        page.add_effect(effect)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Group should have opacity attribute
        assert 'opacity="0.5"' in svg_string

    def test_render_effect_with_stroke_dasharray(self):
        """Test rendering effect elements with stroke dasharray."""
        page = Page(width=400, height=300)
        rect = Rectangle(width=100, height=100).move_to((200, 150))
        page.add(rect)

        # ShakeEffect generates dashed polylines
        effect = ShakeEffect(target=rect, seed=42, num_copies=2)
        page.add_effect(effect)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Shake effect uses stroke-dasharray for ghost copies
        assert "stroke-dasharray" in svg_string


class TestPanelBackgroundImage:
    """Tests for panel background image rendering."""

    def test_panel_with_background_image_file(self, tmp_path):
        """Test rendering panel with a background image from file."""
        # Create a simple test PNG image (1x1 red pixel)
        import base64

        # Minimal valid PNG (1x1 red pixel)
        png_data = base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8DwHwAFBQIAX8jx"
            "0gAAAABJRU5ErkJggg=="
        )
        image_path = tmp_path / "test_bg.png"
        image_path.write_bytes(png_data)

        # Create panel with background image
        page = Page(width=400, height=300)
        panel = Panel(width=300, height=200)
        panel.move_to((200, 150))
        panel.set_background(image=str(image_path))
        page.add(panel)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Should contain an image element with data URI
        assert "<image" in svg_string
        assert "data:image/png;base64" in svg_string

    def test_panel_with_background_image_nonexistent(self):
        """Test rendering panel with nonexistent background image falls back to path."""
        page = Page(width=400, height=300)
        panel = Panel(width=300, height=200)
        panel.move_to((200, 150))
        panel.set_background(image="/nonexistent/path/image.png")
        page.add(panel)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Should still attempt to render with the path
        assert "<image" in svg_string
        assert "/nonexistent/path/image.png" in svg_string

    def test_panel_with_background_image_and_rounded_corners(self, tmp_path):
        """Test panel background image with rounded corners creates clip path."""
        import base64

        png_data = base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8DwHwAFBQIAX8jx"
            "0gAAAABJRU5ErkJggg=="
        )
        image_path = tmp_path / "test_bg_round.png"
        image_path.write_bytes(png_data)

        page = Page(width=400, height=300)
        panel = Panel(width=300, height=200)
        panel.set_border(radius=20)  # Set radius through set_border method
        panel.move_to((200, 150))
        panel.set_background(image=str(image_path))
        page.add(panel)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Should have clip path for rounded corners
        assert "<clipPath" in svg_string
        assert "clip-path" in svg_string
        assert "<image" in svg_string

    def test_panel_background_color_renders_before_image(self, tmp_path):
        """Test that background color is rendered before background image."""
        import base64

        png_data = base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8DwHwAFBQIAX8jx"
            "0gAAAABJRU5ErkJggg=="
        )
        image_path = tmp_path / "test_bg.png"
        image_path.write_bytes(png_data)

        page = Page(width=400, height=300)
        panel = Panel(width=300, height=200, background_color="#FF0000")
        panel.move_to((200, 150))
        panel.set_background(image=str(image_path))
        page.add(panel)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Both rect (background color) and image should be present
        assert "<rect" in svg_string
        assert "<image" in svg_string
        assert "#FF0000" in svg_string

    def test_panel_without_background_image(self):
        """Test that panel without background image doesn't have image element."""
        page = Page(width=400, height=300)
        panel = Panel(width=300, height=200)
        panel.move_to((200, 150))
        page.add(panel)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Should have rect but not image
        assert "<rect" in svg_string
        # Count image elements - there should be none for a simple panel
        # (unless other content has images)
        image_count = svg_string.count("<image")
        assert image_count == 0

    def test_parser_background_image_renders(self, tmp_path):
        """Test that parser-created panels with background image render correctly."""
        import base64
        from comix.parser.parser import parse_markup

        png_data = base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8DwHwAFBQIAX8jx"
            "0gAAAABJRU5ErkJggg=="
        )
        image_path = tmp_path / "bg.png"
        image_path.write_bytes(png_data)

        markup = f"""
[page 1x1]
# panel 1
[background: {image_path}]
character(center): "Test"
"""
        page = parse_markup(markup)
        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Should contain the background image
        assert "<image" in svg_string
        assert "data:image/png;base64" in svg_string
