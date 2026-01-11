"""Style module - styling system for Comix."""

from comix.style.style import Style, MANGA_STYLE, WEBTOON_STYLE, COMIC_STYLE, MINIMAL_STYLE
from comix.style.font import (
    FontInfo,
    FontMetrics,
    FontRegistry,
    get_font_registry,
    init_font_system,
    get_default_metrics,
    estimate_text_width,
    estimate_text_height,
)
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
    set_default_theme,
    register_theme,
)

__all__ = [
    # Style
    "Style",
    "MANGA_STYLE",
    "WEBTOON_STYLE",
    "COMIC_STYLE",
    "MINIMAL_STYLE",
    # Font
    "FontInfo",
    "FontMetrics",
    "FontRegistry",
    "get_font_registry",
    "init_font_system",
    "get_default_metrics",
    "estimate_text_width",
    "estimate_text_height",
    # Theme
    "ColorPalette",
    "Theme",
    "ThemeRegistry",
    "MANGA_THEME",
    "WEBTOON_THEME",
    "COMIC_THEME",
    "MINIMAL_THEME",
    "get_theme_registry",
    "get_theme",
    "get_default_theme",
    "set_default_theme",
    "register_theme",
]
