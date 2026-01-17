"""Font - Font management system for Comix using fonttools.

Provides font discovery, metrics calculation, and fallback handling.
"""

from __future__ import annotations

import os
import platform
import subprocess
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import ClassVar

from fontTools.ttLib import TTFont


@dataclass
class FontInfo:
    """Information about a font."""

    family: str
    path: Path
    weight: str = "normal"  # normal, bold, 100-900
    style: str = "normal"  # normal, italic, oblique
    full_name: str = ""

    def __post_init__(self) -> None:
        if not self.full_name:
            self.full_name = self.family


@dataclass
class FontMetrics:
    """Font metrics for text measurement."""

    units_per_em: int
    ascender: int
    descender: int
    x_height: int
    cap_height: int
    line_gap: int
    avg_char_width: float

    def get_line_height(self, font_size: float) -> float:
        """Calculate line height for given font size."""
        total = self.ascender - self.descender + self.line_gap
        return (total / self.units_per_em) * font_size

    def get_text_height(self, font_size: float) -> float:
        """Calculate text height (ascender to descender)."""
        return ((self.ascender - self.descender) / self.units_per_em) * font_size

    def get_char_width(self, font_size: float) -> float:
        """Calculate average character width for given font size."""
        return (self.avg_char_width / self.units_per_em) * font_size


@dataclass
class FontRegistry:
    """Registry for managing and discovering fonts.

    Provides system font discovery, font registration, and fallback handling.
    """

    _fonts: dict[str, FontInfo] = field(default_factory=dict)
    _metrics_cache: dict[str, FontMetrics] = field(default_factory=dict)
    _fallback_chains: dict[str, list[str]] = field(default_factory=dict)

    # Default fallback chains for common font families
    DEFAULT_FALLBACKS: ClassVar[dict[str, list[str]]] = {
        "sans-serif": [
            "Arial",
            "Helvetica Neue",
            "Helvetica",
            "Liberation Sans",
            "DejaVu Sans",
        ],
        "serif": [
            "Times New Roman",
            "Times",
            "Liberation Serif",
            "DejaVu Serif",
        ],
        "monospace": [
            "Monaco",
            "Consolas",
            "Liberation Mono",
            "DejaVu Sans Mono",
            "Courier New",
        ],
        "comic": [
            "Comic Sans MS",
            "Comic Neue",
            "Arial",
        ],
    }

    def __post_init__(self) -> None:
        # Initialize default fallback chains
        self._fallback_chains.update(self.DEFAULT_FALLBACKS)

    def register_font(self, font_info: FontInfo) -> None:
        """Register a font with the registry."""
        key = self._make_key(font_info.family, font_info.weight, font_info.style)
        self._fonts[key] = font_info
        # Also register by family name only for simple lookups
        self._fonts[font_info.family.lower()] = font_info

    def get_font(
        self,
        family: str,
        weight: str = "normal",
        style: str = "normal",
    ) -> FontInfo | None:
        """Get a registered font, with fallback support."""
        key = self._make_key(family, weight, style)
        if key in self._fonts:
            return self._fonts[key]

        # Try just the family name
        family_lower = family.lower()
        if family_lower in self._fonts:
            return self._fonts[family_lower]

        # Try fallback chain
        if family_lower in self._fallback_chains:
            for fallback in self._fallback_chains[family_lower]:
                fallback_key = self._make_key(fallback, weight, style)
                if fallback_key in self._fonts:
                    return self._fonts[fallback_key]
                if fallback.lower() in self._fonts:
                    return self._fonts[fallback.lower()]

        return None

    def set_fallback_chain(self, family: str, fallbacks: list[str]) -> None:
        """Set a custom fallback chain for a font family."""
        self._fallback_chains[family.lower()] = fallbacks

    def get_metrics(self, font_info: FontInfo) -> FontMetrics:
        """Get metrics for a font."""
        cache_key = str(font_info.path)
        if cache_key in self._metrics_cache:
            return self._metrics_cache[cache_key]

        metrics = _extract_font_metrics(font_info.path)
        self._metrics_cache[cache_key] = metrics
        return metrics

    def get_metrics_for_family(
        self,
        family: str,
        weight: str = "normal",
        style: str = "normal",
    ) -> FontMetrics | None:
        """Get metrics for a font family."""
        font = self.get_font(family, weight, style)
        if font:
            return self.get_metrics(font)
        return None

    def discover_system_fonts(self) -> int:
        """Discover and register system fonts. Returns count of fonts found."""
        fonts_found = 0
        system = platform.system()

        if system == "Darwin":
            fonts_found = self._discover_macos_fonts()
        elif system == "Linux":
            fonts_found = self._discover_linux_fonts()
        elif system == "Windows":
            fonts_found = self._discover_windows_fonts()

        return fonts_found

    def _discover_macos_fonts(self) -> int:
        """Discover fonts on macOS."""
        fonts_found = 0
        font_dirs = [
            Path("/System/Library/Fonts"),
            Path("/Library/Fonts"),
            Path.home() / "Library/Fonts",
        ]

        for font_dir in font_dirs:
            if font_dir.exists():
                fonts_found += self._scan_font_directory(font_dir)

        return fonts_found

    def _discover_linux_fonts(self) -> int:
        """Discover fonts on Linux using fc-list."""
        fonts_found = 0

        # Try using fc-list for font discovery
        try:
            result = subprocess.run(
                ["fc-list", "--format", "%{file}\n"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    if line and Path(line).exists():
                        font_info = self._load_font_info(Path(line))
                        if font_info:
                            self.register_font(font_info)
                            fonts_found += 1
        except (subprocess.TimeoutExpired, FileNotFoundError):
            # Fallback to scanning common directories
            font_dirs = [
                Path("/usr/share/fonts"),
                Path("/usr/local/share/fonts"),
                Path.home() / ".fonts",
                Path.home() / ".local/share/fonts",
            ]
            for font_dir in font_dirs:
                if font_dir.exists():
                    fonts_found += self._scan_font_directory(font_dir)

        return fonts_found

    def _discover_windows_fonts(self) -> int:
        """Discover fonts on Windows."""
        fonts_found = 0
        font_dir = Path(os.environ.get("WINDIR", "C:\\Windows")) / "Fonts"

        if font_dir.exists():
            fonts_found = self._scan_font_directory(font_dir)

        return fonts_found

    def _scan_font_directory(self, directory: Path) -> int:
        """Scan a directory for font files."""
        fonts_found = 0
        font_extensions = {".ttf", ".otf", ".ttc", ".woff", ".woff2"}

        for path in directory.rglob("*"):
            if path.suffix.lower() in font_extensions:
                font_info = self._load_font_info(path)
                if font_info:
                    self.register_font(font_info)
                    fonts_found += 1

        return fonts_found

    def _load_font_info(self, path: Path) -> FontInfo | None:
        """Load font information from a font file."""
        try:
            font = TTFont(path, fontNumber=0)
            name_table = font.get("name")
            if not name_table:
                return None

            family = ""
            full_name = ""

            # Extract font names from name table
            for record in name_table.names:
                # Family name (nameID 1)
                if record.nameID == 1 and not family:
                    family = record.toUnicode()
                # Full name (nameID 4)
                elif record.nameID == 4 and not full_name:
                    full_name = record.toUnicode()

            if not family:
                family = path.stem

            # Determine weight and style from OS/2 table
            weight = "normal"
            style = "normal"

            os2 = font.get("OS/2")
            if os2:
                weight_class = os2.usWeightClass
                if weight_class >= 700:
                    weight = "bold"
                elif weight_class <= 300:
                    weight = "light"

                if os2.fsSelection & 1:  # Italic bit
                    style = "italic"

            font.close()

            return FontInfo(
                family=family,
                path=path,
                weight=weight,
                style=style,
                full_name=full_name or family,
            )
        except Exception:
            return None

    @staticmethod
    def _make_key(family: str, weight: str, style: str) -> str:
        """Create a cache key for font lookup."""
        return f"{family.lower()}:{weight}:{style}"


def _extract_font_metrics(font_path: Path) -> FontMetrics:
    """Extract font metrics from a font file."""
    try:
        font = TTFont(font_path, fontNumber=0)

        # Get units per em from head table
        head = font.get("head")
        units_per_em = head.unitsPerEm if head else 1000

        # Get metrics from OS/2 table
        os2 = font.get("OS/2")
        if os2:
            ascender = os2.sTypoAscender
            descender = os2.sTypoDescender
            line_gap = os2.sTypoLineGap
            x_height = getattr(os2, "sxHeight", 0) or int(units_per_em * 0.5)
            cap_height = getattr(os2, "sCapHeight", 0) or int(units_per_em * 0.7)
            avg_char_width = os2.xAvgCharWidth
        else:
            # Fallback to hhea table
            hhea = font.get("hhea")
            if hhea:
                ascender = hhea.ascent
                descender = hhea.descent
                line_gap = hhea.lineGap
            else:
                ascender = int(units_per_em * 0.8)
                descender = int(units_per_em * -0.2)
                line_gap = 0

            x_height = int(units_per_em * 0.5)
            cap_height = int(units_per_em * 0.7)
            avg_char_width = int(units_per_em * 0.5)

        font.close()

        return FontMetrics(
            units_per_em=units_per_em,
            ascender=ascender,
            descender=descender,
            x_height=x_height,
            cap_height=cap_height,
            line_gap=line_gap,
            avg_char_width=avg_char_width,
        )
    except Exception:
        # Return default metrics if font loading fails
        return _get_default_metrics()


def _get_default_metrics() -> FontMetrics:
    """Get default font metrics for fallback."""
    return FontMetrics(
        units_per_em=1000,
        ascender=800,
        descender=-200,
        x_height=500,
        cap_height=700,
        line_gap=0,
        avg_char_width=500,
    )


# Global font registry instance
_global_registry: FontRegistry | None = None


def get_font_registry() -> FontRegistry:
    """Get the global font registry, creating it if necessary."""
    global _global_registry
    if _global_registry is None:
        _global_registry = FontRegistry()
    return _global_registry


def init_font_system(discover_system_fonts: bool = True) -> FontRegistry:
    """Initialize the font system and optionally discover system fonts."""
    registry = get_font_registry()
    if discover_system_fonts:
        registry.discover_system_fonts()
    return registry


@lru_cache(maxsize=128)
def get_default_metrics() -> FontMetrics:
    """Get default font metrics (cached)."""
    return _get_default_metrics()


def is_fullwidth_char(char: str) -> bool:
    """Check if a character is full-width (CJK or other wide characters).

    Full-width characters include:
    - CJK Unified Ideographs (Chinese, Japanese Kanji, Korean Hanja)
    - Korean Hangul syllables and Jamo
    - Japanese Hiragana and Katakana
    - Full-width ASCII and punctuation

    Args:
        char: A single character to check

    Returns:
        True if the character is full-width, False otherwise
    """
    if not char:
        return False

    code = ord(char)

    # CJK Unified Ideographs
    if 0x4E00 <= code <= 0x9FFF:
        return True
    # CJK Extension A
    if 0x3400 <= code <= 0x4DBF:
        return True
    # CJK Extension B-F (surrogate pairs in Python handled automatically)
    if 0x20000 <= code <= 0x2EBEF:
        return True
    # Korean Hangul Syllables
    if 0xAC00 <= code <= 0xD7AF:
        return True
    # Korean Hangul Jamo
    if 0x1100 <= code <= 0x11FF:
        return True
    # Korean Hangul Compatibility Jamo
    if 0x3130 <= code <= 0x318F:
        return True
    # Japanese Hiragana
    if 0x3040 <= code <= 0x309F:
        return True
    # Japanese Katakana
    if 0x30A0 <= code <= 0x30FF:
        return True
    # Katakana Phonetic Extensions
    if 0x31F0 <= code <= 0x31FF:
        return True
    # CJK Symbols and Punctuation
    if 0x3000 <= code <= 0x303F:
        return True
    # Fullwidth ASCII and Punctuation
    if 0xFF00 <= code <= 0xFFEF:
        return True
    # CJK Compatibility Forms
    if 0xFE30 <= code <= 0xFE4F:
        return True

    return False


def calculate_text_width_with_cjk(
    text: str,
    font_size: float,
    halfwidth_ratio: float = 0.5,
    fullwidth_ratio: float = 1.0,
) -> float:
    """Calculate text width accounting for CJK full-width characters.

    Full-width characters (CJK) are typically rendered at 1em width,
    while half-width characters (Latin, numbers) are around 0.5em.

    Args:
        text: The text to measure
        font_size: Font size in pixels
        halfwidth_ratio: Width ratio for half-width chars (default 0.5)
        fullwidth_ratio: Width ratio for full-width chars (default 1.0)

    Returns:
        Estimated text width in pixels
    """
    if not text:
        return 0.0

    total_em = 0.0
    for char in text:
        if is_fullwidth_char(char):
            total_em += fullwidth_ratio
        else:
            total_em += halfwidth_ratio

    return total_em * font_size


def estimate_text_width(
    text: str,
    font_size: float,
    font_family: str = "sans-serif",
    font_weight: str = "normal",
) -> float:
    """Estimate text width using font metrics or fallback.

    This function accounts for CJK full-width characters, which are
    typically rendered at full em width, while Latin characters are
    rendered at approximately half em width.

    Args:
        text: The text to measure
        font_size: Font size in pixels
        font_family: Font family name
        font_weight: Font weight (normal, bold)

    Returns:
        Estimated text width in pixels
    """
    registry = get_font_registry()
    metrics = registry.get_metrics_for_family(font_family, font_weight)

    if metrics is None:
        metrics = get_default_metrics()

    # Get the average character width from metrics (used for half-width ratio)
    avg_char_width = metrics.get_char_width(font_size)
    halfwidth_ratio = avg_char_width / font_size if font_size > 0 else 0.5

    # Full-width characters are typically 1em
    return calculate_text_width_with_cjk(
        text, font_size, halfwidth_ratio=halfwidth_ratio, fullwidth_ratio=1.0
    )


def estimate_text_height(
    font_size: float,
    font_family: str = "sans-serif",
    line_height: float = 1.4,
    num_lines: int = 1,
) -> float:
    """Estimate text height using font metrics or fallback.

    Args:
        font_size: Font size in pixels
        font_family: Font family name
        line_height: Line height multiplier
        num_lines: Number of text lines

    Returns:
        Estimated text height in pixels
    """
    registry = get_font_registry()
    metrics = registry.get_metrics_for_family(font_family)

    if metrics is None:
        metrics = get_default_metrics()

    single_line_height = metrics.get_text_height(font_size)
    return single_line_height * line_height * num_lines
