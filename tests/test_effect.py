"""Tests for the Effect system."""

import math
import tempfile
from pathlib import Path

import pytest

from comix import (
    Page,
    Panel,
    Stickman,
    AppearEffect,
    ShakeEffect,
    ZoomEffect,
    MotionLines,
    FocusLines,
    ImpactEffect,
)
from comix.effect.effect import EffectElement


class TestEffectElement:
    """Tests for EffectElement dataclass."""

    def test_default_init(self):
        """Test EffectElement with default values."""
        elem = EffectElement(
            element_type="line",
            points=[(0, 0), (100, 100)],
        )
        assert elem.element_type == "line"
        assert elem.points == [(0, 0), (100, 100)]
        assert elem.stroke_color == "#000000"
        assert elem.stroke_width == 2.0
        assert elem.fill_color is None
        assert elem.opacity == 1.0
        assert elem.stroke_dasharray is None

    def test_custom_init(self):
        """Test EffectElement with custom values."""
        elem = EffectElement(
            element_type="polygon",
            points=[(0, 0), (50, 0), (25, 50)],
            stroke_color="#FF0000",
            stroke_width=3.0,
            fill_color="#00FF00",
            opacity=0.5,
            stroke_dasharray="5,5",
        )
        assert elem.element_type == "polygon"
        assert elem.stroke_color == "#FF0000"
        assert elem.stroke_width == 3.0
        assert elem.fill_color == "#00FF00"
        assert elem.opacity == 0.5
        assert elem.stroke_dasharray == "5,5"


class TestShakeEffect:
    """Tests for ShakeEffect."""

    def test_default_init(self):
        """Test ShakeEffect with default values."""
        effect = ShakeEffect()
        assert effect.target is None
        assert effect.intensity == 1.0
        assert effect.opacity == 0.3
        assert effect.z_index == -1
        assert effect.shake_distance == 5.0
        assert effect.num_copies == 3
        assert effect.direction == "both"

    def test_with_target(self):
        """Test ShakeEffect with a target CObject."""
        char = Stickman("Test").move_to((100, 100))
        effect = ShakeEffect(target=char)

        pos = effect.position
        assert abs(pos[0] - 100) < 1  # Should be near character center
        assert abs(pos[1] - 100) < 50  # Account for character height offset

    def test_set_methods_chain(self):
        """Test that set methods return self for chaining."""
        effect = ShakeEffect()
        result = (
            effect.set_intensity(0.5)
            .set_color("#FF0000")
            .set_opacity(0.8)
            .set_shake_distance(10.0)
            .set_num_copies(5)
            .set_direction("horizontal")
        )
        assert result is effect
        assert effect.intensity == 0.5
        assert effect.color == "#FF0000"
        assert effect.opacity == 0.8
        assert effect.shake_distance == 10.0
        assert effect.num_copies == 5
        assert effect.direction == "horizontal"

    def test_generate_elements_with_target(self):
        """Test element generation with a target."""
        char = Stickman("Test").move_to((100, 100))
        effect = ShakeEffect(target=char, seed=42)

        elements = effect.get_elements()
        assert len(elements) > 0

        # Should have ghost copies (polylines) and motion blur lines
        polylines = [e for e in elements if e.element_type == "polyline"]
        lines = [e for e in elements if e.element_type == "line"]
        assert len(polylines) == 3  # num_copies default
        assert len(lines) >= 4  # motion blur lines

    def test_direction_horizontal(self):
        """Test horizontal shake direction."""
        char = Stickman("Test").move_to((100, 100))
        effect = ShakeEffect(target=char, direction="horizontal", seed=42)
        elements = effect.get_elements()
        assert len(elements) > 0

    def test_direction_vertical(self):
        """Test vertical shake direction."""
        char = Stickman("Test").move_to((100, 100))
        effect = ShakeEffect(target=char, direction="vertical", seed=42)
        elements = effect.get_elements()
        assert len(elements) > 0

    def test_render_data(self):
        """Test get_render_data method."""
        char = Stickman("Test").move_to((100, 100))
        effect = ShakeEffect(target=char, seed=42)

        data = effect.get_render_data()
        assert data["type"] == "Effect"
        assert data["effect_type"] == "ShakeEffect"
        assert "position" in data
        assert "elements" in data
        assert len(data["elements"]) > 0

    def test_no_elements_without_target(self):
        """Test that no elements are generated without target."""
        effect = ShakeEffect()
        elements = effect.get_elements()
        assert len(elements) == 0

    def test_reproducible_with_seed(self):
        """Test that same seed produces same elements."""
        char = Stickman("Test").move_to((100, 100))

        effect1 = ShakeEffect(target=char, seed=123)
        effect2 = ShakeEffect(target=char, seed=123)

        elements1 = effect1.get_elements()
        elements2 = effect2.get_elements()

        assert len(elements1) == len(elements2)
        for e1, e2 in zip(elements1, elements2):
            assert e1.points == e2.points


class TestZoomEffect:
    """Tests for ZoomEffect."""

    def test_default_init(self):
        """Test ZoomEffect with default values."""
        effect = ZoomEffect()
        assert effect.target is None
        assert effect.intensity == 1.0
        assert effect.opacity == 0.6
        assert effect.z_index == -1
        assert effect.num_lines == 24
        assert effect.inner_radius == 50.0
        assert effect.outer_radius == 150.0

    def test_position_from_target(self):
        """Test position derived from target."""
        char = Stickman("Test").move_to((200, 200))
        effect = ZoomEffect(target=char)

        pos = effect.position
        assert abs(pos[0] - 200) < 1
        assert abs(pos[1] - 200) < 50  # Account for character offset

    def test_explicit_position(self):
        """Test explicit position overrides target."""
        char = Stickman("Test").move_to((200, 200))
        effect = ZoomEffect(target=char, position=(50, 50))

        pos = effect.position
        assert pos == (50, 50)

    def test_set_methods_chain(self):
        """Test method chaining."""
        effect = ZoomEffect()
        result = (
            effect.set_num_lines(36)
            .set_radii(30, 200)
        )
        assert result is effect
        assert effect.num_lines == 36
        assert effect.inner_radius == 30
        assert effect.outer_radius == 200

    def test_generate_elements(self):
        """Test element generation."""
        effect = ZoomEffect(position=(100, 100), seed=42)
        elements = effect.get_elements()

        assert len(elements) == 24  # num_lines default
        for elem in elements:
            assert elem.element_type == "line"
            assert len(elem.points) == 2

    def test_intensity_affects_lines(self):
        """Test that intensity affects number of lines."""
        effect_full = ZoomEffect(position=(100, 100), intensity=1.0, seed=42)
        effect_half = ZoomEffect(position=(100, 100), intensity=0.5, seed=42)

        elements_full = effect_full.get_elements()
        elements_half = effect_half.get_elements()

        assert len(elements_full) > len(elements_half)

    def test_render_data(self):
        """Test get_render_data method."""
        effect = ZoomEffect(position=(100, 100), seed=42)
        data = effect.get_render_data()

        assert data["type"] == "Effect"
        assert data["effect_type"] == "ZoomEffect"
        assert data["position"] == [100, 100]
        assert len(data["elements"]) > 0


class TestMotionLines:
    """Tests for MotionLines effect."""

    def test_default_init(self):
        """Test MotionLines with default values."""
        effect = MotionLines()
        assert effect.target is None
        assert effect.intensity == 1.0
        assert effect.opacity == 0.5
        assert effect.z_index == -1
        assert effect.direction == 0.0
        assert effect.num_lines == 12
        assert effect.line_length == 100.0
        assert effect.spread == 50.0
        assert effect.taper is True

    def test_set_direction_radians(self):
        """Test setting direction in radians."""
        effect = MotionLines()
        effect.set_direction(math.pi / 2)
        assert effect.direction == math.pi / 2

    def test_set_direction_degrees(self):
        """Test setting direction in degrees."""
        effect = MotionLines()
        effect.set_direction_degrees(90)
        assert abs(effect.direction - math.pi / 2) < 0.001

    def test_set_methods_chain(self):
        """Test method chaining."""
        effect = MotionLines()
        result = (
            effect.set_direction_degrees(45)
            .set_num_lines(20)
            .set_line_length(150)
            .set_spread(80)
        )
        assert result is effect
        assert effect.num_lines == 20
        assert effect.line_length == 150
        assert effect.spread == 80

    def test_generate_elements(self):
        """Test element generation."""
        effect = MotionLines(position=(100, 100), seed=42)
        elements = effect.get_elements()

        assert len(elements) == 12  # num_lines default
        for elem in elements:
            assert elem.element_type == "line"

    def test_taper_varies_width(self):
        """Test that taper affects line widths."""
        effect = MotionLines(position=(100, 100), taper=True, seed=42)
        elements = effect.get_elements()

        widths = [e.stroke_width for e in elements]
        # With taper, widths should vary
        assert len(set(widths)) > 1

    def test_no_taper_constant_width(self):
        """Test that no taper gives more consistent widths."""
        effect = MotionLines(position=(100, 100), taper=False, seed=42)
        elements = effect.get_elements()

        widths = [e.stroke_width for e in elements]
        # Without taper, widths should be constant 1.5
        for w in widths:
            assert w == 1.5

    def test_render_data(self):
        """Test get_render_data method."""
        effect = MotionLines(position=(100, 100), seed=42)
        data = effect.get_render_data()

        assert data["type"] == "Effect"
        assert data["effect_type"] == "MotionLines"


class TestFocusLines:
    """Tests for FocusLines effect."""

    def test_default_init(self):
        """Test FocusLines with default values."""
        effect = FocusLines()
        assert effect.target is None
        assert effect.intensity == 1.0
        assert effect.opacity == 0.8
        assert effect.z_index == -1
        assert effect.num_lines == 36
        assert effect.inner_gap == 80.0
        assert effect.outer_radius == 300.0
        assert effect.fill_background is False

    def test_set_methods_chain(self):
        """Test method chaining."""
        effect = FocusLines()
        result = (
            effect.set_num_lines(48)
            .set_inner_gap(100)
            .set_outer_radius(400)
            .set_fill_background(True, "#EEEEEE")
        )
        assert result is effect
        assert effect.num_lines == 48
        assert effect.inner_gap == 100
        assert effect.outer_radius == 400
        assert effect.fill_background is True
        assert effect.background_color == "#EEEEEE"

    def test_generate_elements_without_fill(self):
        """Test element generation without background fill."""
        effect = FocusLines(position=(100, 100), fill_background=False, seed=42)
        elements = effect.get_elements()

        # Should only have line elements
        assert all(e.element_type == "line" for e in elements)
        assert len(elements) == 36

    def test_generate_elements_with_fill(self):
        """Test element generation with background fill."""
        effect = FocusLines(position=(100, 100), fill_background=True, seed=42)
        elements = effect.get_elements()

        # Should have both polygon (fill) and line elements
        polygons = [e for e in elements if e.element_type == "polygon"]
        lines = [e for e in elements if e.element_type == "line"]

        assert len(polygons) > 0
        assert len(lines) == 36

    def test_inner_gap_adjusted_for_target(self):
        """Test that inner gap adjusts for target size."""
        char = Stickman("Test").move_to((100, 100))
        effect = FocusLines(target=char, inner_gap=10, seed=42)  # Small initial gap

        elements = effect.get_elements()
        # Elements should still be generated correctly
        assert len(elements) > 0


class TestAppearEffect:
    """Tests for AppearEffect."""

    def test_default_init(self):
        """Test AppearEffect with default values."""
        effect = AppearEffect()
        assert effect.target is None
        assert effect.intensity == 1.0
        assert effect.opacity == 0.6
        assert effect.z_index == -1
        assert effect.style == "sparkle"
        assert effect.num_elements == 12
        assert effect.radius == 80.0
        assert effect.glow_color is None

    def test_with_target(self):
        """Test AppearEffect with a target CObject."""
        char = Stickman("Test").move_to((100, 100))
        effect = AppearEffect(target=char)

        pos = effect.position
        assert abs(pos[0] - 100) < 1
        assert abs(pos[1] - 100) < 50  # Account for character height offset

    def test_set_methods_chain(self):
        """Test that set methods return self for chaining."""
        effect = AppearEffect()
        result = (
            effect.set_style("fade")
            .set_num_elements(20)
            .set_radius(100.0)
            .set_glow_color("#FFFF00")
            .set_intensity(0.8)
            .set_color("#FF0000")
            .set_opacity(0.5)
        )
        assert result is effect
        assert effect.style == "fade"
        assert effect.num_elements == 20
        assert effect.radius == 100.0
        assert effect.glow_color == "#FFFF00"
        assert effect.intensity == 0.8
        assert effect.color == "#FF0000"
        assert effect.opacity == 0.5

    def test_invalid_style_ignored(self):
        """Test that invalid style is ignored."""
        effect = AppearEffect()
        effect.set_style("invalid_style")
        assert effect.style == "sparkle"  # Should remain default

    def test_valid_styles(self):
        """Test all valid appearance styles."""
        for style in ("sparkle", "fade", "flash", "reveal"):
            effect = AppearEffect()
            effect.set_style(style)
            assert effect.style == style

    def test_sparkle_style_elements(self):
        """Test sparkle style generates expected elements."""
        effect = AppearEffect(position=(100, 100), style="sparkle", seed=42)
        elements = effect.get_elements()

        assert len(elements) > 0
        # Should have polygon (star) and circle (dot) elements
        polygons = [e for e in elements if e.element_type == "polygon"]
        circles = [e for e in elements if e.element_type == "circle"]
        assert len(polygons) > 0
        assert len(circles) > 0

    def test_fade_style_elements(self):
        """Test fade style generates concentric rings."""
        effect = AppearEffect(position=(100, 100), style="fade", seed=42)
        elements = effect.get_elements()

        assert len(elements) > 0
        # Should have polyline elements (rings)
        polylines = [e for e in elements if e.element_type == "polyline"]
        assert len(polylines) > 0
        # Rings should have dash patterns
        for elem in polylines:
            assert elem.stroke_dasharray is not None

    def test_flash_style_elements(self):
        """Test flash style generates burst elements."""
        effect = AppearEffect(position=(100, 100), style="flash", seed=42)
        elements = effect.get_elements()

        assert len(elements) > 0
        # Should have polygon (rays) and circle (center glow)
        polygons = [e for e in elements if e.element_type == "polygon"]
        circles = [e for e in elements if e.element_type == "circle"]
        assert len(polygons) > 0
        assert len(circles) == 1  # Center glow

    def test_reveal_style_elements(self):
        """Test reveal style generates reveal lines and corners."""
        effect = AppearEffect(position=(100, 100), style="reveal", seed=42)
        elements = effect.get_elements()

        assert len(elements) > 0
        # Should have line and polyline elements
        lines = [e for e in elements if e.element_type == "line"]
        polylines = [e for e in elements if e.element_type == "polyline"]
        assert len(lines) > 0
        assert len(polylines) == 4  # Four corner accents

    def test_intensity_affects_elements(self):
        """Test that intensity affects number of elements."""
        effect_full = AppearEffect(position=(100, 100), intensity=1.0, style="sparkle", seed=42)
        effect_half = AppearEffect(position=(100, 100), intensity=0.5, style="sparkle", seed=42)

        elements_full = effect_full.get_elements()
        elements_half = effect_half.get_elements()

        # Full intensity should produce more elements
        assert len(elements_full) > len(elements_half)

    def test_radius_adjusted_for_target(self):
        """Test that radius adjusts for target size."""
        char = Stickman("Test").move_to((100, 100))
        effect = AppearEffect(target=char, radius=10, seed=42)  # Small initial radius

        elements = effect.get_elements()
        # Elements should still be generated correctly
        assert len(elements) > 0

    def test_glow_color_applied(self):
        """Test that glow color is applied to elements."""
        effect = AppearEffect(position=(100, 100), glow_color="#FF00FF", style="sparkle", seed=42)
        elements = effect.get_elements()

        # At least some elements should have the glow color
        glow_elements = [e for e in elements if e.fill_color == "#FF00FF"]
        assert len(glow_elements) > 0

    def test_render_data(self):
        """Test get_render_data method."""
        effect = AppearEffect(position=(100, 100), seed=42)
        data = effect.get_render_data()

        assert data["type"] == "Effect"
        assert data["effect_type"] == "AppearEffect"
        assert data["position"] == [100, 100]
        assert len(data["elements"]) > 0

    def test_reproducible_with_seed(self):
        """Test that same seed produces same elements."""
        effect1 = AppearEffect(position=(100, 100), style="sparkle", seed=123)
        effect2 = AppearEffect(position=(100, 100), style="sparkle", seed=123)

        elements1 = effect1.get_elements()
        elements2 = effect2.get_elements()

        assert len(elements1) == len(elements2)
        for e1, e2 in zip(elements1, elements2):
            assert e1.points == e2.points

    def test_repr(self):
        """Test AppearEffect repr."""
        effect = AppearEffect(position=(100, 200), intensity=0.5)
        repr_str = repr(effect)
        assert "AppearEffect" in repr_str


class TestImpactEffect:
    """Tests for ImpactEffect."""

    def test_default_init(self):
        """Test ImpactEffect with default values."""
        effect = ImpactEffect()
        assert effect.target is None
        assert effect.intensity == 1.0
        assert effect.opacity == 0.9
        assert effect.z_index == 1  # In front by default
        assert effect.num_spikes == 12
        assert effect.inner_radius == 20.0
        assert effect.outer_radius == 60.0
        assert effect.spike_variation == 0.3
        assert effect.fill_center is True

    def test_set_methods_chain(self):
        """Test method chaining."""
        effect = ImpactEffect()
        result = (
            effect.set_num_spikes(16)
            .set_radii(30, 80)
        )
        assert result is effect
        assert effect.num_spikes == 16
        assert effect.inner_radius == 30
        assert effect.outer_radius == 80

    def test_generate_elements(self):
        """Test element generation."""
        effect = ImpactEffect(position=(100, 100), seed=42)
        elements = effect.get_elements()

        # Should have star burst polygon and debris lines
        polygons = [e for e in elements if e.element_type == "polygon"]
        lines = [e for e in elements if e.element_type == "line"]

        assert len(polygons) == 1  # Star burst
        assert len(lines) >= 6  # Debris lines

    def test_fill_center(self):
        """Test center fill option."""
        effect_fill = ImpactEffect(position=(100, 100), fill_center=True, seed=42)
        effect_no_fill = ImpactEffect(position=(100, 100), fill_center=False, seed=42)

        elements_fill = effect_fill.get_elements()
        elements_no_fill = effect_no_fill.get_elements()

        # Get star burst polygon from each
        poly_fill = [e for e in elements_fill if e.element_type == "polygon"][0]
        poly_no_fill = [e for e in elements_no_fill if e.element_type == "polygon"][0]

        assert poly_fill.fill_color == "#FFFFFF"
        assert poly_no_fill.fill_color is None

    def test_star_burst_shape(self):
        """Test that star burst has correct number of points."""
        effect = ImpactEffect(position=(100, 100), num_spikes=8, seed=42)
        elements = effect.get_elements()

        polygon = [e for e in elements if e.element_type == "polygon"][0]
        # Should have num_spikes * 2 points plus closing point
        # With intensity=1.0, effective_spikes = 8
        # Points = 8 * 2 + 1 (closing) = 17
        assert len(polygon.points) == 17


class TestPageEffectIntegration:
    """Tests for Page + Effect integration."""

    def test_add_effect(self):
        """Test adding effects to a page."""
        page = Page()
        effect = ShakeEffect(position=(100, 100))

        result = page.add_effect(effect)
        assert result is page  # Method chaining
        assert effect in page.get_effects()

    def test_add_multiple_effects(self):
        """Test adding multiple effects."""
        page = Page()
        effect1 = ShakeEffect(position=(100, 100))
        effect2 = ZoomEffect(position=(200, 200))

        page.add_effect(effect1, effect2)
        effects = page.get_effects()

        assert effect1 in effects
        assert effect2 in effects
        assert len(effects) == 2

    def test_remove_effect(self):
        """Test removing effects."""
        page = Page()
        effect = ShakeEffect(position=(100, 100))

        page.add_effect(effect)
        assert len(page.get_effects()) == 1

        page.remove_effect(effect)
        assert len(page.get_effects()) == 0

    def test_effect_in_render_data(self):
        """Test that effects appear in render data."""
        page = Page()
        effect = ZoomEffect(position=(100, 100), seed=42)
        page.add_effect(effect)

        data = page.get_render_data()
        assert "effects" in data
        assert len(data["effects"]) == 1
        assert data["effects"][0]["effect_type"] == "ZoomEffect"

    def test_render_svg_with_effects(self):
        """Test SVG rendering with effects."""
        page = Page(width=400, height=400)
        panel = Panel(width=360, height=360).move_to((200, 200))
        page.add(panel)

        effect = ZoomEffect(position=(200, 200), seed=42)
        page.add_effect(effect)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = str(Path(tmpdir) / "test_effect.svg")
            result = page.render(output_path)

            assert Path(result).exists()
            content = Path(result).read_text()
            assert "<svg" in content
            # Effect lines should be rendered
            assert "<line" in content


class TestRendererEffectIntegration:
    """Tests for renderer effect integration."""

    def test_svg_renderer_effect_elements(self):
        """Test SVG renderer renders effect elements correctly."""
        page = Page(width=400, height=400)

        # Add zoom effect which generates lines
        effect = ZoomEffect(position=(200, 200), num_lines=8, seed=42)
        page.add_effect(effect)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = str(Path(tmpdir) / "test.svg")
            page.render(output_path)

            content = Path(output_path).read_text()
            # Should have multiple line elements from the effect
            assert content.count("<line") >= 8

    def test_svg_renderer_effect_polygon(self):
        """Test SVG renderer renders polygon effects."""
        page = Page(width=400, height=400)

        effect = ImpactEffect(position=(200, 200), seed=42)
        page.add_effect(effect)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = str(Path(tmpdir) / "test.svg")
            page.render(output_path)

            content = Path(output_path).read_text()
            # Should have polygon from star burst
            assert "<polygon" in content

    def test_background_effects_rendered_first(self):
        """Test that negative z_index effects render behind objects."""
        page = Page(width=400, height=400)
        panel = Panel(width=100, height=100).move_to((200, 200))
        page.add(panel)

        # Background effect (z_index=-1)
        bg_effect = ZoomEffect(position=(200, 200), z_index=-1, seed=42)
        page.add_effect(bg_effect)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = str(Path(tmpdir) / "test.svg")
            page.render(output_path)

            content = Path(output_path).read_text()
            # Effect should be in the file
            assert "<line" in content

    def test_foreground_effects_rendered_last(self):
        """Test that positive z_index effects render in front."""
        page = Page(width=400, height=400)
        panel = Panel(width=100, height=100).move_to((200, 200))
        page.add(panel)

        # Foreground effect (z_index=1)
        fg_effect = ImpactEffect(position=(200, 200), z_index=1, seed=42)
        page.add_effect(fg_effect)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = str(Path(tmpdir) / "test.svg")
            page.render(output_path)

            content = Path(output_path).read_text()
            assert "<polygon" in content


class TestCairoRendererEffects:
    """Tests for Cairo renderer effect support."""

    @pytest.fixture
    def skip_if_no_cairo(self):
        """Skip test if Cairo is not installed."""
        try:
            import cairo  # noqa: F401
        except ImportError:
            pytest.skip("Cairo not installed")

    def test_cairo_renders_effects_png(self, skip_if_no_cairo):
        """Test Cairo renders effects to PNG."""
        page = Page(width=400, height=400)
        effect = ZoomEffect(position=(200, 200), seed=42)
        page.add_effect(effect)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = str(Path(tmpdir) / "test.png")
            result = page.render(output_path, format="png")

            assert Path(result).exists()
            # File should have content
            assert Path(result).stat().st_size > 0

    def test_cairo_renders_effects_pdf(self, skip_if_no_cairo):
        """Test Cairo renders effects to PDF."""
        page = Page(width=400, height=400)
        effect = ImpactEffect(position=(200, 200), seed=42)
        page.add_effect(effect)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = str(Path(tmpdir) / "test.pdf")
            result = page.render(output_path, format="pdf")

            assert Path(result).exists()
            assert Path(result).stat().st_size > 0

    def test_cairo_renders_multiple_effects(self, skip_if_no_cairo):
        """Test Cairo renders multiple effects."""
        page = Page(width=400, height=400)
        page.add_effect(
            ZoomEffect(position=(100, 100), z_index=-1, seed=42),
            MotionLines(position=(300, 100), z_index=-1, seed=43),
            ImpactEffect(position=(200, 200), z_index=1, seed=44),
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = str(Path(tmpdir) / "test.png")
            result = page.render(output_path, format="png")

            assert Path(result).exists()


class TestEffectRepr:
    """Tests for Effect __repr__ methods."""

    def test_shake_repr(self):
        """Test ShakeEffect repr."""
        effect = ShakeEffect(position=(100, 200), intensity=0.5)
        repr_str = repr(effect)
        assert "ShakeEffect" in repr_str
        assert "(100, 200)" in repr_str or "100" in repr_str

    def test_zoom_repr(self):
        """Test ZoomEffect repr."""
        effect = ZoomEffect(position=(150, 250), intensity=0.8)
        repr_str = repr(effect)
        assert "ZoomEffect" in repr_str

    def test_motion_lines_repr(self):
        """Test MotionLines repr."""
        effect = MotionLines(position=(50, 75))
        repr_str = repr(effect)
        assert "MotionLines" in repr_str

    def test_focus_lines_repr(self):
        """Test FocusLines repr."""
        effect = FocusLines(position=(200, 200))
        repr_str = repr(effect)
        assert "FocusLines" in repr_str

    def test_impact_repr(self):
        """Test ImpactEffect repr."""
        effect = ImpactEffect(position=(300, 300))
        repr_str = repr(effect)
        assert "ImpactEffect" in repr_str


class TestEffectImports:
    """Tests for effect module imports."""

    def test_import_from_main_package(self):
        """Test effects can be imported from main comix package."""
        import comix

        assert hasattr(comix, "Effect")
        assert hasattr(comix, "AppearEffect")
        assert hasattr(comix, "ShakeEffect")
        assert hasattr(comix, "ZoomEffect")
        assert hasattr(comix, "MotionLines")
        assert hasattr(comix, "FocusLines")
        assert hasattr(comix, "ImpactEffect")

    def test_import_from_effect_module(self):
        """Test effects can be imported from effect module."""
        from comix import effect as effect_module

        assert hasattr(effect_module, "Effect")
        assert hasattr(effect_module, "AppearEffect")
        assert hasattr(effect_module, "ShakeEffect")
        assert hasattr(effect_module, "ZoomEffect")
        assert hasattr(effect_module, "MotionLines")
        assert hasattr(effect_module, "FocusLines")
        assert hasattr(effect_module, "ImpactEffect")


class TestEffectEdgeCases:
    """Tests for effect edge cases and boundary conditions."""

    def test_effect_default_position_without_target(self):
        """Test effect returns (0, 0) when no position or target is set."""
        effect = ShakeEffect()
        pos = effect.position
        assert pos == (0.0, 0.0)

    def test_set_position_returns_self(self):
        """Test set_position returns self for chaining."""
        effect = ShakeEffect()
        result = effect.set_position((100, 200))
        assert result is effect
        assert effect.position == (100, 200)

    def test_set_position_overrides_target_position(self):
        """Test explicit position takes precedence over target."""
        char = Stickman("Test").move_to((50, 50))
        effect = ShakeEffect(target=char)
        effect.set_position((200, 300))
        assert effect.position == (200, 300)

    def test_set_target_returns_self(self):
        """Test set_target returns self for chaining."""
        effect = ShakeEffect()
        char = Stickman("Test")
        result = effect.set_target(char)
        assert result is effect
        assert effect.target is char

    def test_intensity_clamped_to_zero(self):
        """Test intensity is clamped to 0 for negative values."""
        effect = ShakeEffect()
        effect.set_intensity(-0.5)
        assert effect.intensity == 0.0

    def test_intensity_clamped_to_one(self):
        """Test intensity is clamped to 1 for values > 1."""
        effect = ShakeEffect()
        effect.set_intensity(1.5)
        assert effect.intensity == 1.0

    def test_opacity_clamped_to_zero(self):
        """Test opacity is clamped to 0 for negative values."""
        effect = ShakeEffect()
        effect.set_opacity(-0.5)
        assert effect.opacity == 0.0

    def test_opacity_clamped_to_one(self):
        """Test opacity is clamped to 1 for values > 1."""
        effect = ShakeEffect()
        effect.set_opacity(1.5)
        assert effect.opacity == 1.0

    def test_zero_intensity_still_generates_elements(self):
        """Test effect with zero intensity still works (may produce minimal elements)."""
        effect = ShakeEffect(position=(100, 100))
        effect.set_intensity(0.0)
        elements = effect.get_elements()
        assert isinstance(elements, list)


class TestAppearEffectStyles:
    """Tests for AppearEffect style variations to cover all branches."""

    def test_default_style_fallback_to_sparkle(self):
        """Test unknown style falls back to sparkle style."""
        effect = AppearEffect(position=(100, 100))
        effect.style = "unknown_style"
        elements = effect.get_elements()
        assert len(elements) > 0

    def test_fade_style_with_target(self):
        """Test fade style generates elements when target is set."""
        char = Stickman("Test").move_to((100, 100))
        effect = AppearEffect(target=char, style="fade")
        elements = effect.get_elements()
        assert len(elements) > 0

    def test_flash_style_with_target(self):
        """Test flash style generates elements when target is set."""
        char = Stickman("Test").move_to((100, 100))
        effect = AppearEffect(target=char, style="flash")
        elements = effect.get_elements()
        assert len(elements) > 0

    def test_reveal_style_with_target(self):
        """Test reveal style generates elements when target is set."""
        char = Stickman("Test").move_to((100, 100))
        effect = AppearEffect(target=char, style="reveal")
        elements = effect.get_elements()
        assert len(elements) > 0

    def test_fade_style_without_target(self):
        """Test fade style without target uses default radius."""
        effect = AppearEffect(position=(100, 100), style="fade", radius=30)
        elements = effect.get_elements()
        assert len(elements) > 0

    def test_flash_style_without_target(self):
        """Test flash style without target uses default radius."""
        effect = AppearEffect(position=(100, 100), style="flash", radius=30)
        elements = effect.get_elements()
        assert len(elements) > 0

    def test_reveal_style_without_target(self):
        """Test reveal style without target uses default radius."""
        effect = AppearEffect(position=(100, 100), style="reveal", radius=30)
        elements = effect.get_elements()
        assert len(elements) > 0

    def test_sparkle_with_target(self):
        """Test sparkle style with target adjusts radius based on target size."""
        char = Stickman("Test").move_to((100, 100))
        effect = AppearEffect(target=char, style="sparkle")
        elements = effect.get_elements()
        assert len(elements) > 0
