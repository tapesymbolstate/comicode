"""Themes and Styles for consistent comic styling.

Comix provides a powerful styling system with:
- Style: CSS-like properties for individual elements
- Theme: Coordinated styling across all elements
- ColorPalette: Consistent colors throughout a comic
- ThemeRegistry: Global theme management

This example demonstrates:
- Built-in style presets (MANGA, WEBTOON, COMIC, MINIMAL)
- Built-in themes and their visual differences
- Creating custom themes
- Using ThemeRegistry for theme management
"""
# Status: ✅ Working (v0.1.108)

from comix import Page, Panel, Stickman
from comix.style.style import Style, MANGA_STYLE, WEBTOON_STYLE, COMIC_STYLE, MINIMAL_STYLE
from comix.style.theme import (
    Theme,
    ColorPalette,
    ThemeRegistry,
    MANGA_THEME,
    WEBTOON_THEME,
    COMIC_THEME,
    MINIMAL_THEME,
    register_theme,
    get_theme,
)


def create_style_comparison() -> None:
    """Compare the 4 built-in style presets."""
    page = Page(width=900, height=400, background_color="#F5F5F5")

    styles = [
        ("MANGA", MANGA_STYLE, "#FFE4E1"),
        ("WEBTOON", WEBTOON_STYLE, "#E0FFFF"),
        ("COMIC", COMIC_STYLE, "#FFF8DC"),
        ("MINIMAL", MINIMAL_STYLE, "#F0FFF0"),
    ]

    x_offset = 35
    for name, style, bg_color in styles:
        # Create panel with style properties
        panel = Panel(width=200, height=300, background_color=bg_color)

        # Apply border from style
        panel.set_border(
            color=style.border_color,
            width=style.border_width,
            style=style.border_style,
        )

        char = Stickman(height=70)
        char.move_to((100, 150))
        char.set_expression("happy")
        bubble = char.say(f"{name}\nStyle")
        panel.add_content(char, bubble)

        panel.move_to((x_offset + 100, 200))
        page.add(panel)
        x_offset += 220

    page.render("examples/output/20_style_comparison.png")
    print("Created examples/output/20_style_comparison.png")


def create_theme_showcase() -> None:
    """Showcase the 4 built-in themes."""
    themes = [
        ("Manga Theme", MANGA_THEME),
        ("Webtoon Theme", WEBTOON_THEME),
        ("Comic Theme", COMIC_THEME),
        ("Minimal Theme", MINIMAL_THEME),
    ]

    for name, theme in themes:
        # Create a small comic page using this theme's colors
        page = Page(
            width=500,
            height=400,
            background_color=theme.colors.background,
        )
        page.set_layout(rows=1, cols=2)

        # Panel 1
        panel1 = Panel(
            width=220,
            height=350,
            background_color=theme.colors.fill,
        )
        panel_style = theme.get_style_for("panel")
        panel1.set_border(
            color=panel_style.border_color,
            width=panel_style.border_width,
        )

        char1 = Stickman(height=80, color=theme.colors.primary)
        char1.move_to((110, 180))
        char1.set_expression("happy")
        bubble1 = char1.say(name)
        panel1.add_content(char1, bubble1)

        # Panel 2
        panel2 = Panel(
            width=220,
            height=350,
            background_color=theme.colors.fill,
        )
        panel2.set_border(
            color=panel_style.border_color,
            width=panel_style.border_width,
        )

        char2 = Stickman(height=80, color=theme.colors.secondary)
        char2.move_to((110, 180))
        char2.set_expression("excited")
        bubble2 = char2.say(f"Accent:\n{theme.colors.accent}")
        panel2.add_content(char2, bubble2)

        page.add(panel1, panel2)
        page.auto_layout()

        # Clean filename
        filename = name.lower().replace(" ", "_")
        page.render(f"examples/output/20_{filename}.png")
        print(f"Created examples/output/20_{filename}.png")


def create_custom_theme() -> None:
    """Create and use a custom theme."""
    # Define a custom "Cyberpunk" theme
    cyberpunk_palette = ColorPalette(
        primary="#FF00FF",  # Magenta
        secondary="#00FFFF",  # Cyan
        accent="#FFFF00",  # Yellow
        background="#0D0D1A",  # Dark blue-black
        text="#FFFFFF",  # White
        border="#FF00FF",  # Magenta
        fill="#1A1A2E",  # Dark purple
    )

    cyberpunk_theme = Theme(
        name="cyberpunk",
        colors=cyberpunk_palette,
        bubble_style=Style(
            border_color="#00FFFF",
            border_width=2.0,
            fill_color="#1A1A2E",
            font_color="#00FFFF",
            font_size=14.0,
        ),
        panel_style=Style(
            border_color="#FF00FF",
            border_width=3.0,
            fill_color="#1A1A2E",
        ),
        text_style=Style(
            font_color="#FFFFFF",
            font_size=16.0,
        ),
        character_style=Style(
            border_color="#00FFFF",
            border_width=2.0,
        ),
    )

    # Create a comic using the custom theme
    page = Page(
        width=600,
        height=400,
        background_color=cyberpunk_theme.colors.background,
    )
    page.set_layout(rows=1, cols=2)

    panel_style = cyberpunk_theme.get_style_for("panel")

    panel1 = Panel(
        width=270,
        height=350,
        background_color=cyberpunk_theme.colors.fill,
    )
    panel1.set_border(
        color=panel_style.border_color,
        width=panel_style.border_width,
    )

    char1 = Stickman(height=90, color=cyberpunk_theme.colors.primary)
    char1.move_to((135, 180))
    char1.set_expression("excited")
    bubble1 = char1.say("Welcome to\nNight City!")
    panel1.add_content(char1, bubble1)

    panel2 = Panel(
        width=270,
        height=350,
        background_color=cyberpunk_theme.colors.fill,
    )
    panel2.set_border(
        color=panel_style.border_color,
        width=panel_style.border_width,
    )

    char2 = Stickman(height=90, color=cyberpunk_theme.colors.secondary)
    char2.move_to((135, 180))
    char2.set_expression("happy")
    bubble2 = char2.say("Custom theme\nlooks cool!")
    panel2.add_content(char2, bubble2)

    page.add(panel1, panel2)
    page.auto_layout()

    page.render("examples/output/20_cyberpunk_theme.png")
    print("Created examples/output/20_cyberpunk_theme.png")


def create_registry_demo() -> None:
    """Demonstrate ThemeRegistry for managing themes."""
    # Create a registry instance
    registry = ThemeRegistry()

    # List available themes
    print("\nAvailable themes in registry:")
    for theme_name in registry.list_themes():
        theme = registry.get(theme_name)
        if theme:
            print(f"  - {theme_name}: {theme.colors.primary} / {theme.colors.background}")

    # Register a custom theme
    pastel_theme = Theme(
        name="pastel",
        colors=ColorPalette(
            primary="#B5838D",
            secondary="#6D6875",
            accent="#E5989B",
            background="#FFF1E6",
            text="#6D6875",
            border="#B5838D",
            fill="#FFE5D9",
        ),
        bubble_style=Style(
            border_color="#B5838D",
            border_width=2.0,
            fill_color="#FFE5D9",
        ),
        panel_style=Style(
            border_color="#B5838D",
            border_width=2.0,
            fill_color="#FFE5D9",
        ),
    )

    registry.register("pastel", pastel_theme)
    print(f"\nRegistered 'pastel' theme. Total themes: {len(registry.list_themes())}")

    # Use global registry functions
    register_theme("pastel_global", pastel_theme)
    retrieved = get_theme("pastel_global")
    if retrieved:
        print(f"Retrieved theme via global registry: {retrieved.name}")

    # Create a comic with the pastel theme
    page = Page(
        width=400,
        height=300,
        background_color=pastel_theme.colors.background,
    )

    panel = Panel(
        width=350,
        height=250,
        background_color=pastel_theme.colors.fill,
    )
    panel.set_border(
        color=pastel_theme.colors.border,
        width=2.0,
    )

    char = Stickman(height=80, color=pastel_theme.colors.primary)
    char.move_to((175, 130))
    char.set_expression("happy")
    bubble = char.say("Pastel theme\nfrom registry!")
    panel.add_content(char, bubble)

    panel.move_to((200, 150))
    page.add(panel)

    page.render("examples/output/20_registry_theme.png")
    print("Created examples/output/20_registry_theme.png")


def create_style_merge_demo() -> None:
    """Demonstrate style merging for customization."""
    page = Page(width=600, height=300, background_color="#F5F5F5")

    # Start with MANGA_STYLE and customize
    base_style = MANGA_STYLE

    # Create a custom style that overrides some properties
    custom_overrides = Style(
        border_color="#E91E63",  # Pink border
        border_width=4.0,
        fill_color="#FCE4EC",  # Light pink fill
    )

    # Merge: base style + overrides
    merged_style = base_style.merge_with(custom_overrides)

    # Create panels showing the difference
    panel1 = Panel(width=250, height=200, background_color="#FFFFFF")
    panel1.set_border(
        color=base_style.border_color,
        width=base_style.border_width,
    )
    char1 = Stickman(height=60)
    char1.move_to((125, 100))
    bubble1 = char1.say("Base\nMANGA_STYLE")
    panel1.add_content(char1, bubble1)

    panel2 = Panel(width=250, height=200, background_color=merged_style.fill_color)
    panel2.set_border(
        color=merged_style.border_color,
        width=merged_style.border_width,
    )
    char2 = Stickman(height=60, color="#E91E63")
    char2.move_to((125, 100))
    bubble2 = char2.say("Merged\nCustom Style")
    panel2.add_content(char2, bubble2)

    panel1.move_to((160, 150))
    panel2.move_to((440, 150))
    page.add(panel1, panel2)

    page.render("examples/output/20_style_merge.png")
    print("Created examples/output/20_style_merge.png")


if __name__ == "__main__":
    create_style_comparison()
    create_theme_showcase()
    create_custom_theme()
    create_registry_demo()
    create_style_merge_demo()
    print("\nThemes and Styles examples complete!")
