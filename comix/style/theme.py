"""Theme - Global theming system for Comix.

Provides coordinated styling across all elements in a comic.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from comix.style.style import Style, MANGA_STYLE, WEBTOON_STYLE, COMIC_STYLE, MINIMAL_STYLE


@dataclass
class ColorPalette:
    """Color palette for a theme.

    Defines the primary colors used throughout the theme.
    """

    primary: str = "#000000"
    secondary: str = "#333333"
    accent: str = "#FF0000"
    background: str = "#FFFFFF"
    text: str = "#000000"
    border: str = "#000000"
    fill: str = "#FFFFFF"

    def to_dict(self) -> dict[str, str]:
        """Convert palette to dictionary."""
        return {
            "primary": self.primary,
            "secondary": self.secondary,
            "accent": self.accent,
            "background": self.background,
            "text": self.text,
            "border": self.border,
            "fill": self.fill,
        }

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> ColorPalette:
        """Create ColorPalette from dictionary."""
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class Theme:
    """Theme definition for consistent styling across a comic.

    A theme provides:
    - A color palette for consistent colors
    - Default styles for different element types
    - Typography settings
    """

    name: str = "default"
    colors: ColorPalette = field(default_factory=ColorPalette)

    # Default styles for different element types
    bubble_style: Style = field(default_factory=Style)
    panel_style: Style = field(default_factory=Style)
    text_style: Style = field(default_factory=Style)
    character_style: Style = field(default_factory=Style)

    # Typography settings
    default_font: str = "sans-serif"
    bubble_font: str = "sans-serif"
    title_font: str = "sans-serif"
    sfx_font: str = "sans-serif"

    def get_style_for(self, element_type: str) -> Style:
        """Get the appropriate style for an element type.

        Args:
            element_type: Type of element ("bubble", "panel", "text", "character").

        Returns:
            The Style object for that element type.
        """
        style_map = {
            "bubble": self.bubble_style,
            "panel": self.panel_style,
            "text": self.text_style,
            "character": self.character_style,
        }
        return style_map.get(element_type.lower(), self.bubble_style)

    def create_style(self, **overrides: Any) -> Style:
        """Create a new Style based on this theme's defaults with overrides.

        Args:
            **overrides: Style properties to override.

        Returns:
            A new Style object with theme defaults and overrides applied.
        """
        base_style = Style(
            border_color=self.colors.border,
            fill_color=self.colors.fill,
            font_color=self.colors.text,
            font_family=self.default_font,
        )

        if overrides:
            override_style = Style(**overrides)
            return base_style.merge_with(override_style)

        return base_style

    def to_dict(self) -> dict[str, Any]:
        """Convert theme to dictionary."""
        return {
            "name": self.name,
            "colors": self.colors.to_dict(),
            "bubble_style": self.bubble_style.to_dict(),
            "panel_style": self.panel_style.to_dict(),
            "text_style": self.text_style.to_dict(),
            "character_style": self.character_style.to_dict(),
            "default_font": self.default_font,
            "bubble_font": self.bubble_font,
            "title_font": self.title_font,
            "sfx_font": self.sfx_font,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Theme:
        """Create Theme from dictionary."""
        colors = ColorPalette.from_dict(data.get("colors", {}))
        bubble_style = Style.from_dict(data.get("bubble_style", {}))
        panel_style = Style.from_dict(data.get("panel_style", {}))
        text_style = Style.from_dict(data.get("text_style", {}))
        character_style = Style.from_dict(data.get("character_style", {}))

        return cls(
            name=data.get("name", "default"),
            colors=colors,
            bubble_style=bubble_style,
            panel_style=panel_style,
            text_style=text_style,
            character_style=character_style,
            default_font=data.get("default_font", "sans-serif"),
            bubble_font=data.get("bubble_font", "sans-serif"),
            title_font=data.get("title_font", "sans-serif"),
            sfx_font=data.get("sfx_font", "sans-serif"),
        )


# === Built-in Themes ===

MANGA_THEME = Theme(
    name="manga",
    colors=ColorPalette(
        primary="#000000",
        secondary="#666666",
        accent="#000000",
        background="#FFFFFF",
        text="#000000",
        border="#000000",
        fill="#FFFFFF",
    ),
    bubble_style=MANGA_STYLE,
    panel_style=Style(
        border_color="#000000",
        border_width=2.0,
        fill_color="#FFFFFF",
    ),
    text_style=Style(
        font_family="sans-serif",
        font_size=14.0,
        font_color="#000000",
    ),
    character_style=Style(
        border_color="#000000",
        border_width=2.0,
    ),
    default_font="sans-serif",
    bubble_font="sans-serif",
)

WEBTOON_THEME = Theme(
    name="webtoon",
    colors=ColorPalette(
        primary="#333333",
        secondary="#666666",
        accent="#4A90D9",
        background="#FFFFFF",
        text="#333333",
        border="#333333",
        fill="#FFFFFF",
    ),
    bubble_style=WEBTOON_STYLE,
    panel_style=Style(
        border_color="#333333",
        border_width=0.0,
        fill_color="#FFFFFF",
        shadow=True,
    ),
    text_style=Style(
        font_family="sans-serif",
        font_size=16.0,
        font_color="#333333",
    ),
    character_style=Style(
        border_color="#333333",
        border_width=1.0,
    ),
    default_font="sans-serif",
    bubble_font="sans-serif",
)

COMIC_THEME = Theme(
    name="comic",
    colors=ColorPalette(
        primary="#000000",
        secondary="#333333",
        accent="#FF0000",
        background="#FFFEF0",
        text="#000000",
        border="#000000",
        fill="#FFFEF0",
    ),
    bubble_style=COMIC_STYLE,
    panel_style=Style(
        border_color="#000000",
        border_width=3.0,
        fill_color="#FFFEF0",
    ),
    text_style=Style(
        font_family="sans-serif",
        font_size=18.0,
        font_weight="bold",
        font_color="#000000",
    ),
    character_style=Style(
        border_color="#000000",
        border_width=3.0,
    ),
    default_font="sans-serif",
    bubble_font="sans-serif",
)

MINIMAL_THEME = Theme(
    name="minimal",
    colors=ColorPalette(
        primary="#333333",
        secondary="#999999",
        accent="#666666",
        background="#FAFAFA",
        text="#333333",
        border="#CCCCCC",
        fill="#FAFAFA",
    ),
    bubble_style=MINIMAL_STYLE,
    panel_style=Style(
        border_color="#CCCCCC",
        border_width=1.0,
        fill_color="#FAFAFA",
    ),
    text_style=Style(
        font_family="sans-serif",
        font_size=14.0,
        font_color="#333333",
    ),
    character_style=Style(
        border_color="#666666",
        border_width=1.0,
    ),
    default_font="sans-serif",
    bubble_font="sans-serif",
)


# === Theme Registry ===

class ThemeRegistry:
    """Registry for managing themes.

    Provides theme lookup, registration, and default theme management.
    """

    def __init__(self) -> None:
        self._themes: dict[str, Theme] = {}
        self._default_theme: str = "default"

        # Register built-in themes
        self.register("default", Theme())
        self.register("manga", MANGA_THEME)
        self.register("webtoon", WEBTOON_THEME)
        self.register("comic", COMIC_THEME)
        self.register("minimal", MINIMAL_THEME)

    def register(self, name: str, theme: Theme) -> None:
        """Register a theme with the registry."""
        self._themes[name.lower()] = theme

    def get(self, name: str) -> Theme | None:
        """Get a theme by name."""
        return self._themes.get(name.lower())

    def get_default(self) -> Theme:
        """Get the default theme."""
        return self._themes.get(self._default_theme, Theme())

    def set_default(self, name: str) -> bool:
        """Set the default theme by name.

        Returns:
            True if theme exists and was set, False otherwise.
        """
        if name.lower() in self._themes:
            self._default_theme = name.lower()
            return True
        return False

    def list_themes(self) -> list[str]:
        """List all registered theme names."""
        return list(self._themes.keys())

    def unregister(self, name: str) -> bool:
        """Unregister a theme by name.

        Returns:
            True if theme was removed, False if not found.
        """
        if name.lower() in self._themes:
            del self._themes[name.lower()]
            return True
        return False


# Global theme registry instance
_global_registry: ThemeRegistry | None = None


def get_theme_registry() -> ThemeRegistry:
    """Get the global theme registry, creating it if necessary."""
    global _global_registry
    if _global_registry is None:
        _global_registry = ThemeRegistry()
    return _global_registry


def get_theme(name: str) -> Theme | None:
    """Get a theme by name from the global registry."""
    return get_theme_registry().get(name)


def get_default_theme() -> Theme:
    """Get the default theme from the global registry."""
    return get_theme_registry().get_default()


def set_default_theme(name: str) -> bool:
    """Set the default theme in the global registry."""
    return get_theme_registry().set_default(name)


def register_theme(name: str, theme: Theme) -> None:
    """Register a theme with the global registry."""
    get_theme_registry().register(name, theme)
