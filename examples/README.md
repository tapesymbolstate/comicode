# Comix Examples

This directory contains working examples demonstrating how to use the Comix library.

## Running Examples

All examples use `uv` for dependency management. Run examples with:

```bash
uv run python examples/01_simple_dialogue.py
```

Generated PNG files will be saved to `examples/output/`.

## Examples List

**Status Legend**: ✅ Working | 🔴 Broken | 🚧 Work in Progress

### Core Examples (01-05)

1. ✅ **01_simple_dialogue.py** - Two characters having a conversation (2 panels)
2. ✅ **02_four_panel_comic.py** - Traditional 4-panel (4koma) comic structure
3. ✅ **03_group_scene.py** - Multiple characters in a single panel
4. ✅ **04_expressions.py** - Different character expressions (happy, sad, angry, etc.)
5. ✅ **05_bubble_types.py** - Different speech bubble styles (speech, thought, shout, whisper)

### Advanced Examples (06-11)

6. ✅ **06_multi_page_pdf.py** - Creating multi-page PDF comics using the Book class
7. ✅ **07_custom_layout.py** - Custom grid layouts (3x2, 2x3, etc.)
8. ✅ **08_manual_positioning.py** - Precise manual positioning of elements
9. ✅ **09_using_templates.py** - Using built-in templates (FourKoma, TwoByTwo, ActionPage, WebComic)
10. ✅ **10_error_handling.py** - Graceful error handling and fallbacks
11. ✅ **11_html_export.py** - Interactive HTML export with zoom, pan, dark/light themes

### Extended Examples (12-17)

12. ✅ **12_parser_dsl.py** - Create comics from markup text using the DSL parser
13. ✅ **13_visual_effects.py** - Manga-style visual effects (shake, zoom, motion, focus, impact)
14. ✅ **14_animation_export.py** - GIF animation export with Timeline and easing functions
15. ✅ **15_video_export.py** - MP4/WebM video export with quality settings
16. ✅ **16_character_types.py** - Showcase of all 9 character types with expressions and poses
17. ✅ **17_ai_image_generation.py** - AI image generation with DALL-E and Replicate

### Layout & Styling Examples (18-20)

18. ✅ **18_flow_layout.py** - FlowLayout for responsive, content-aware positioning
    - Horizontal flow with automatic wrapping
    - Vertical flow for column-based layouts
    - Alignment options (start, center, end)
    - Variable-sized panels that maintain proportions

19. ✅ **19_constraint_layout.py** - ConstraintLayout for precise, relational positioning
    - Basic edge constraints (left, right, top, bottom)
    - Relative positioning between elements
    - Center alignment and proportional sizing
    - Complex multi-panel manga arrangements

20. ✅ **20_themes_and_styles.py** - Themes and Styles for consistent comic styling
    - Built-in style presets (MANGA, WEBTOON, COMIC, MINIMAL)
    - Built-in themes and their visual differences
    - Creating custom themes with ColorPalette
    - Using ThemeRegistry for theme management

### Text & Templates Examples (21-22)

21. ✅ **21_text_and_narration.py** - StyledText, SFX, and NarratorBubble
    - Caption boxes for scene descriptions
    - Sound effects (onomatopoeia) with outlines
    - Time and place indicators
    - Story narration and combined text types

22. ✅ **22_advanced_templates.py** - ThreeRowLayout and MangaPage templates
    - ThreeRowLayout with custom panel configurations
    - MangaPage presets (six_panel, dialogue, action)
    - Custom row heights and proportions
    - Dramatic layout variations

### Development Workflow (23-26)

23. ✅ **23_preview_server.py** - Preview Server for live development
    - Hot-reload capability for rapid iteration
    - CLI usage: `uv run comix serve script.py`
    - Creating preview-friendly scripts
    - One-shot preview mode

24. ✅ **24_new_templates.py** - NewspaperStrip and Widescreen templates
    - NewspaperStrip for classic 3-4 horizontal panel comics
    - Widescreen for cinematic 16:9 or 21:9 aspect ratio layouts

25. ✅ **25_panel_shapes.py** - Advanced panel shapes for dynamic layouts
    - DiagonalPanel, TrapezoidPanel, StarburstPanel, CloudPanel, ExplosionPanel
    - Panel splitting methods (split_diagonal, split_curve)
    - Mixed shapes comic demonstrating multiple panel types

26. ✅ **26_stickman_articulation.py** - Joint-level control for Stickman characters
    - set_arm_angles() for shoulder and elbow control (0-360° / 0-180°)
    - set_leg_angles() for hip and knee control
    - set_hands() with 7 gesture options (none, fist, open, point, peace, thumbs_up, relaxed)
    - point_at() helper for automatic arm positioning toward a target
    - ArmController/LegController presets for common poses
    - Method chaining for fluent configuration

## Requirements

- Python 3.13+
- Dependencies managed by uv (automatically handled)
- Optional: pycairo for PNG/PDF rendering (all examples use PNG)

## Quick Start

```bash
# From the project root directory
cd /path/to/comicode

# Run an example
uv run python examples/01_simple_dialogue.py

# View the output
open examples/output/01_simple_dialogue.png
```

## Using the Preview Server

For rapid development with live reload:

```bash
# Start preview server (auto-opens browser)
uv run comix serve examples/23_preview_server.py

# One-shot preview (no hot-reload)
uv run comix preview examples/01_simple_dialogue.py
```

## Modifying Examples

Feel free to modify these examples to experiment:
- Change character positions with `.move_to((x, y))`
- Add more characters using `Stickman()` or other character types
- Try different expressions: neutral, happy, sad, angry, surprised, confused, sleepy, excited, scared, smirk, crying
- Customize bubble text
- Adjust page dimensions in `Page(width=..., height=...)`
- Change colors with the `color` parameter

## Character Types

Beyond Stickman, you can also try:
- `SimpleFace` - Emoticon-style face
- `ChubbyStickman` - Rounded, friendly stick figure
- `Robot` - Mechanical character
- `Chibi` - Cute anime-style character
- `Anime` - Natural proportion anime character
- `Superhero` - Heroic character with costume
- `Cartoon` - Classic Western cartoon style
- `AnimalStyle` - Anthropomorphic animal characters (cat, dog, rabbit, fox, bear, bird, wolf)

## Layout Systems

Comix provides three layout systems:

1. **GridLayout** (default) - Equal-size grid positioning via `page.set_layout(rows, cols)`
2. **FlowLayout** - Content-aware flow with wrapping (see example 18)
3. **ConstraintLayout** - Declarative constraints for complex layouts (see example 19)

## Themes & Styling

Apply consistent styling across your comics:

- `MANGA_STYLE` / `MANGA_THEME` - Classic manga look
- `WEBTOON_STYLE` / `WEBTOON_THEME` - Modern webtoon style
- `COMIC_STYLE` / `COMIC_THEME` - Western comic book style
- `MINIMAL_STYLE` / `MINIMAL_THEME` - Clean, minimal design

See example 20 for usage.

## Need Help?

- Check the `specs/` directory for detailed documentation
- See `specs/getting-started.md` for basic workflows
- Report issues at https://github.com/anthropics/comicode/issues
