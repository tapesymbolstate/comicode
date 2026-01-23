"""Style - CSS-like styling system for Comix."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Style:
    """Style definition for visual elements.

    Similar to CSS, defines visual properties that can be applied
    to CObjects.
    """

    border_color: str = "#000000"
    border_width: float = 2.0
    border_style: str = "solid"

    fill_color: str = "#FFFFFF"
    fill_opacity: float = 1.0

    font_family: str = "sans-serif"
    font_size: float = 16.0
    font_weight: str = "normal"
    font_style: str = "normal"
    font_color: str = "#000000"
    text_align: str = "left"
    line_height: float = 1.4

    shadow: bool = False
    shadow_color: str = "#00000033"
    shadow_offset: tuple[float, float] = (2.0, 2.0)
    shadow_blur: float = 4.0

    hand_drawn: bool = False
    hand_drawn_roughness: float = 1.0
    hand_drawn_seed: int | None = None

    def merge_with(self, other: Style) -> Style:
        """Merge with another style, with other taking precedence."""
        merged_data = {}
        for key in self.__dataclass_fields__:
            self_value = getattr(self, key)
            other_value = getattr(other, key)
            default_value = self.__dataclass_fields__[key].default
            if other_value != default_value:
                merged_data[key] = other_value
            else:
                merged_data[key] = self_value
        return Style(**merged_data)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "border_color": self.border_color,
            "border_width": self.border_width,
            "border_style": self.border_style,
            "fill_color": self.fill_color,
            "fill_opacity": self.fill_opacity,
            "font_family": self.font_family,
            "font_size": self.font_size,
            "font_weight": self.font_weight,
            "font_style": self.font_style,
            "font_color": self.font_color,
            "text_align": self.text_align,
            "line_height": self.line_height,
            "shadow": self.shadow,
            "shadow_color": self.shadow_color,
            "shadow_offset": self.shadow_offset,
            "shadow_blur": self.shadow_blur,
            "hand_drawn": self.hand_drawn,
            "hand_drawn_roughness": self.hand_drawn_roughness,
            "hand_drawn_seed": self.hand_drawn_seed,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Style:
        """Create Style from dictionary."""
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


MANGA_STYLE = Style(
    border_color="#000000",
    border_width=2.0,
    font_family="sans-serif",
    font_size=14.0,
)

WEBTOON_STYLE = Style(
    border_color="#333333",
    border_width=0.0,
    font_family="sans-serif",
    font_size=16.0,
    shadow=True,
)

COMIC_STYLE = Style(
    border_color="#000000",
    border_width=3.0,
    font_family="sans-serif",
    font_size=18.0,
    font_weight="bold",
)

MINIMAL_STYLE = Style(
    border_color="#CCCCCC",
    border_width=1.0,
    font_family="sans-serif",
    font_size=14.0,
    fill_color="#FAFAFA",
)
