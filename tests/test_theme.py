"""Tests for Theme system."""


from comix.style.theme import (
    ColorPalette,
    Theme,
    ThemeRegistry,
    MANGA_THEME,
    WEBTOON_THEME,
    COMIC_THEME,
    MINIMAL_THEME,
    get_theme_registry,
    get_theme,
    get_default_theme,
    register_theme,
)
from comix.style.style import Style


class TestColorPalette:
    """Tests for ColorPalette."""

    def test_default_init(self) -> None:
        """Test default palette initialization."""
        palette = ColorPalette()
        assert palette.primary == "#000000"
        assert palette.secondary == "#333333"
        assert palette.accent == "#FF0000"
        assert palette.background == "#FFFFFF"
        assert palette.text == "#000000"
        assert palette.border == "#000000"
        assert palette.fill == "#FFFFFF"

    def test_custom_init(self) -> None:
        """Test custom palette initialization."""
        palette = ColorPalette(
            primary="#0000FF",
            accent="#00FF00",
            background="#F0F0F0",
        )
        assert palette.primary == "#0000FF"
        assert palette.accent == "#00FF00"
        assert palette.background == "#F0F0F0"

    def test_to_dict(self) -> None:
        """Test converting palette to dictionary."""
        palette = ColorPalette(primary="#123456")
        d = palette.to_dict()
        assert d["primary"] == "#123456"
        assert "secondary" in d
        assert "accent" in d

    def test_from_dict(self) -> None:
        """Test creating palette from dictionary."""
        data = {"primary": "#AABBCC", "accent": "#112233"}
        palette = ColorPalette.from_dict(data)
        assert palette.primary == "#AABBCC"
        assert palette.accent == "#112233"
        assert palette.secondary == "#333333"  # Default


class TestTheme:
    """Tests for Theme class."""

    def test_default_init(self) -> None:
        """Test default theme initialization."""
        theme = Theme()
        assert theme.name == "default"
        assert isinstance(theme.colors, ColorPalette)
        assert isinstance(theme.bubble_style, Style)
        assert theme.default_font == "sans-serif"

    def test_custom_init(self) -> None:
        """Test custom theme initialization."""
        palette = ColorPalette(primary="#FF0000")
        bubble_style = Style(border_width=5.0)
        theme = Theme(
            name="custom",
            colors=palette,
            bubble_style=bubble_style,
            default_font="Comic Sans MS",
        )
        assert theme.name == "custom"
        assert theme.colors.primary == "#FF0000"
        assert theme.bubble_style.border_width == 5.0
        assert theme.default_font == "Comic Sans MS"

    def test_get_style_for(self) -> None:
        """Test getting style for element type."""
        bubble_style = Style(border_width=3.0)
        panel_style = Style(border_width=5.0)
        theme = Theme(bubble_style=bubble_style, panel_style=panel_style)

        assert theme.get_style_for("bubble").border_width == 3.0
        assert theme.get_style_for("panel").border_width == 5.0

    def test_get_style_for_unknown(self) -> None:
        """Test getting style for unknown element type defaults to bubble."""
        bubble_style = Style(border_width=3.0)
        theme = Theme(bubble_style=bubble_style)

        result = theme.get_style_for("unknown")
        assert result.border_width == 3.0

    def test_create_style(self) -> None:
        """Test creating style with theme defaults."""
        palette = ColorPalette(border="#FF0000", fill="#00FF00", text="#0000FF")
        theme = Theme(colors=palette, default_font="Arial")

        style = theme.create_style()
        assert style.border_color == "#FF0000"
        assert style.fill_color == "#00FF00"
        assert style.font_color == "#0000FF"
        assert style.font_family == "Arial"

    def test_create_style_with_overrides(self) -> None:
        """Test creating style with overrides."""
        theme = Theme()
        style = theme.create_style(border_width=10.0, font_size=24.0)
        assert style.border_width == 10.0
        assert style.font_size == 24.0

    def test_to_dict(self) -> None:
        """Test converting theme to dictionary."""
        theme = Theme(name="test")
        d = theme.to_dict()

        assert d["name"] == "test"
        assert "colors" in d
        assert "bubble_style" in d
        assert "default_font" in d

    def test_from_dict(self) -> None:
        """Test creating theme from dictionary."""
        data = {
            "name": "loaded",
            "colors": {"primary": "#123456"},
            "default_font": "Helvetica",
        }
        theme = Theme.from_dict(data)

        assert theme.name == "loaded"
        assert theme.colors.primary == "#123456"
        assert theme.default_font == "Helvetica"


class TestBuiltInThemes:
    """Tests for built-in themes."""

    def test_manga_theme(self) -> None:
        """Test MANGA_THEME preset."""
        assert MANGA_THEME.name == "manga"
        assert MANGA_THEME.colors.primary == "#000000"
        assert MANGA_THEME.bubble_style.border_width == 2.0

    def test_webtoon_theme(self) -> None:
        """Test WEBTOON_THEME preset."""
        assert WEBTOON_THEME.name == "webtoon"
        assert WEBTOON_THEME.colors.primary == "#333333"
        assert WEBTOON_THEME.bubble_style.shadow is True

    def test_comic_theme(self) -> None:
        """Test COMIC_THEME preset."""
        assert COMIC_THEME.name == "comic"
        assert COMIC_THEME.bubble_style.border_width == 3.0
        assert COMIC_THEME.text_style.font_weight == "bold"

    def test_minimal_theme(self) -> None:
        """Test MINIMAL_THEME preset."""
        assert MINIMAL_THEME.name == "minimal"
        assert MINIMAL_THEME.colors.border == "#CCCCCC"
        assert MINIMAL_THEME.bubble_style.border_width == 1.0


class TestThemeRegistry:
    """Tests for ThemeRegistry."""

    def test_init(self) -> None:
        """Test registry initialization with built-in themes."""
        registry = ThemeRegistry()
        themes = registry.list_themes()
        assert "default" in themes
        assert "manga" in themes
        assert "webtoon" in themes
        assert "comic" in themes
        assert "minimal" in themes

    def test_register_and_get(self) -> None:
        """Test registering and retrieving a theme."""
        registry = ThemeRegistry()
        custom = Theme(name="custom")
        registry.register("custom", custom)

        result = registry.get("custom")
        assert result is not None
        assert result.name == "custom"

    def test_get_nonexistent(self) -> None:
        """Test getting a theme that doesn't exist."""
        registry = ThemeRegistry()
        result = registry.get("nonexistent")
        assert result is None

    def test_get_case_insensitive(self) -> None:
        """Test that theme lookup is case insensitive."""
        registry = ThemeRegistry()
        assert registry.get("MANGA") is not None
        assert registry.get("Manga") is not None
        assert registry.get("manga") is not None

    def test_set_default(self) -> None:
        """Test setting default theme."""
        registry = ThemeRegistry()
        assert registry.set_default("manga") is True
        assert registry.get_default().name == "manga"

    def test_set_default_nonexistent(self) -> None:
        """Test setting default to nonexistent theme."""
        registry = ThemeRegistry()
        assert registry.set_default("nonexistent") is False

    def test_unregister(self) -> None:
        """Test unregistering a theme."""
        registry = ThemeRegistry()
        custom = Theme(name="temp")
        registry.register("temp", custom)

        assert registry.unregister("temp") is True
        assert registry.get("temp") is None

    def test_unregister_nonexistent(self) -> None:
        """Test unregistering nonexistent theme."""
        registry = ThemeRegistry()
        assert registry.unregister("nonexistent") is False


class TestGlobalFunctions:
    """Tests for global theme functions."""

    def test_get_theme_registry(self) -> None:
        """Test getting global theme registry."""
        registry = get_theme_registry()
        assert isinstance(registry, ThemeRegistry)

        # Should return same instance
        registry2 = get_theme_registry()
        assert registry is registry2

    def test_get_theme(self) -> None:
        """Test getting theme from global registry."""
        theme = get_theme("manga")
        assert theme is not None
        assert theme.name == "manga"

    def test_get_default_theme(self) -> None:
        """Test getting default theme."""
        theme = get_default_theme()
        assert isinstance(theme, Theme)

    def test_register_theme(self) -> None:
        """Test registering theme with global registry."""
        custom = Theme(name="global_custom")
        register_theme("global_custom", custom)

        result = get_theme("global_custom")
        assert result is not None
        assert result.name == "global_custom"
