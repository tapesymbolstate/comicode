# Comix Examples

This directory contains working examples demonstrating how to use the Comix library.

## Running Examples

All examples use `uv` for dependency management. Run examples with:

```bash
uv run python examples/01_simple_dialogue.py
```

Generated PNG files will be saved to `examples/output/`.

## Examples List

1. **01_simple_dialogue.py** - Two characters having a conversation (2 panels)
2. **02_four_panel_comic.py** - Traditional 4-panel (4koma) comic structure
3. **03_group_scene.py** - Multiple characters in a single panel
4. **04_expressions.py** - Different character expressions (happy, sad, angry, etc.)
5. **05_bubble_types.py** - Different speech bubble styles (speech, thought, shout, whisper)

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

## Modifying Examples

Feel free to modify these examples to experiment:
- Change character positions with `.move_to((x, y))`
- Add more characters using `Stickman()` or other character types
- Try different expressions: neutral, happy, sad, angry, surprised, confused
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

## Need Help?

- Check the `specs/` directory for detailed documentation
- See `specs/getting-started.md` for basic workflows
- Report issues at https://github.com/anthropics/comicode/issues
