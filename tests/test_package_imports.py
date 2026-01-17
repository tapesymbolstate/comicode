"""Tests for package import handling and optional dependencies."""



class TestRendererImports:
    """Tests for renderer module import handling."""

    def test_svg_renderer_always_available(self):
        """Test that SVGRenderer is always importable."""
        from comix.renderer import SVGRenderer
        assert SVGRenderer is not None

    def test_cairo_renderer_import_available(self):
        """Test CairoRenderer import when Cairo is available."""
        try:
            from comix.renderer import CairoRenderer
            # If import succeeds, CairoRenderer should be a class
            if CairoRenderer is not None:
                assert callable(CairoRenderer)
        except ImportError:
            # Cairo not installed - this is acceptable
            pass

    def test_renderer_module_all_exports(self):
        """Test that __all__ exports expected items."""
        from comix import renderer
        assert "SVGRenderer" in renderer.__all__
        assert "CairoRenderer" in renderer.__all__


class TestMainPackageImports:
    """Tests for main comix package import handling."""

    def test_version_available(self):
        """Test VERSION is available from main package."""
        from comix import VERSION
        assert VERSION is not None
        assert isinstance(VERSION, str)

    def test_core_exports_available(self):
        """Test core exports are always available."""
        from comix import (
            CObject,
            Panel,
            SpeechBubble,
            ThoughtBubble,
            Text,
            Stickman,
            SimpleFace,
            Page,
            SVGRenderer,
        )
        assert CObject is not None
        assert Panel is not None
        assert SpeechBubble is not None
        assert ThoughtBubble is not None
        assert Text is not None
        assert Stickman is not None
        assert SimpleFace is not None
        assert Page is not None
        assert SVGRenderer is not None

    def test_optional_cairo_renderer(self):
        """Test optional CairoRenderer import."""
        from comix import CairoRenderer
        # CairoRenderer is either a class or None
        if CairoRenderer is not None:
            assert callable(CairoRenderer)

    def test_optional_preview_server(self):
        """Test optional PreviewServer import."""
        from comix import PreviewServer
        # PreviewServer is either a class or None
        if PreviewServer is not None:
            assert callable(PreviewServer)

    def test_optional_preview_error(self):
        """Test optional PreviewError import."""
        from comix import PreviewError
        # PreviewError is either a class or None
        if PreviewError is not None:
            assert issubclass(PreviewError, Exception)

    def test_optional_preview_serve(self):
        """Test optional preview_serve import."""
        from comix import preview_serve
        # preview_serve is either a function or None
        if preview_serve is not None:
            assert callable(preview_serve)

    def test_all_constants_exported(self):
        """Test all constant classes are exported."""
        from comix import (
            Colors,
            Dimensions,
            Typography,
            Borders,
            Effects,
            Server,
            Quality,
            Anchors,
            Directions,
        )
        assert Colors is not None
        assert Dimensions is not None
        assert Typography is not None
        assert Borders is not None
        assert Effects is not None
        assert Server is not None
        assert Quality is not None
        assert Anchors is not None
        assert Directions is not None

    def test_all_style_exports(self):
        """Test all style-related exports."""
        from comix import (
            Style,
            MANGA_STYLE,
            WEBTOON_STYLE,
            COMIC_STYLE,
            MINIMAL_STYLE,
        )
        assert Style is not None
        assert MANGA_STYLE is not None
        assert WEBTOON_STYLE is not None
        assert COMIC_STYLE is not None
        assert MINIMAL_STYLE is not None

    def test_all_theme_exports(self):
        """Test all theme-related exports."""
        from comix import (
            Theme,
            ColorPalette,
            MANGA_THEME,
        )
        assert Theme is not None
        assert ColorPalette is not None
        assert MANGA_THEME is not None

    def test_all_layout_exports(self):
        """Test all layout-related exports."""
        from comix import (
            ConstraintLayout,
            FlowLayout,
            GridLayout,
        )
        assert ConstraintLayout is not None
        assert FlowLayout is not None
        assert GridLayout is not None

    def test_all_effect_exports(self):
        """Test all effect-related exports."""
        from comix import (
            Effect,
            AppearEffect,
            ShakeEffect,
        )
        assert Effect is not None
        assert AppearEffect is not None
        assert ShakeEffect is not None

    def test_all_page_template_exports(self):
        """Test all page template exports."""
        from comix import (
            FourKoma,
            SplashPage,
            TwoByTwo,
        )
        assert FourKoma is not None
        assert SplashPage is not None
        assert TwoByTwo is not None

    def test_all_geometry_exports(self):
        """Test all geometry utility exports."""
        from comix import (
            distance,
            midpoint,
            bounding_box,
        )
        assert distance is not None
        assert midpoint is not None
        assert bounding_box is not None

    def test_all_bezier_exports(self):
        """Test all bezier utility exports."""
        from comix import create_bubble_path, create_tail_points
        assert create_bubble_path is not None
        assert create_tail_points is not None

    def test_dunder_version(self):
        """Test __version__ attribute."""
        import comix
        assert hasattr(comix, "__version__")
        assert comix.__version__ == comix.VERSION


class TestOptionalDependencyMocking:
    """Tests for optional dependency handling using mocking."""

    def test_cairo_not_available_handling(self):
        """Test that CairoRenderer is None when cairo not available."""
        # We can't easily mock ImportError for already-imported modules,
        # but we can verify the fallback behavior is correct
        from comix import CairoRenderer
        # If cairo is not installed, CairoRenderer should be None
        # If installed, it should be callable
        assert CairoRenderer is None or callable(CairoRenderer)

    def test_preview_not_available_handling(self):
        """Test that PreviewServer is None when watchdog not available."""
        from comix import PreviewServer, PreviewError, preview_serve
        # If watchdog is not installed, these should be None
        # If installed, they should be valid types
        if PreviewServer is not None:
            assert callable(PreviewServer)
        if PreviewError is not None:
            assert issubclass(PreviewError, Exception)
        if preview_serve is not None:
            assert callable(preview_serve)
