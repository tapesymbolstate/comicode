# Working Examples - Executable Comic Creation Examples

> **Status (2026-01-18)**: All 26 examples execute without errors and produce correct visual output. Visual bugs from earlier versions have been fixed (v0.1.85).

## What
A collection of complete, runnable Python scripts that demonstrate common comic creation workflows and serve as templates for developers.

## Why
Documentation alone is not enough. Developers learn best from working code they can run, modify, and experiment with. Examples must:
- Actually execute without errors
- Produce visible, **correct** output ✅
- Cover common use cases
- Be simple enough to understand quickly
- Serve as copy-paste starting points

Without working examples, developers struggle to bridge the gap from API documentation to practical usage.

## Acceptance Criteria

### Must Have
- [x] Example 1: Two-panel dialogue (2 stick figures talking) - ✅ Visual output OK
- [x] Example 2: Four-panel comic (4koma style story) - ✅ Working
- [x] Example 3: Single panel with multiple characters - ✅ Fixed in v0.1.85
- [x] Example 4: Character expressions showcase (happy, sad, angry, etc.) - ✅ Working
- [x] Example 5: Different bubble types (speech, thought, shout) - ✅ Working
- [x] All examples execute without errors using `uv run python example_name.py`
- [x] All examples produce visible PNG output showing complete comic - ✅ All visual bugs fixed (v0.1.85)
- [x] Basic examples (01-04, 07) are under 50 lines; complex examples may be longer for comprehensiveness
- [x] Each example has clear comments explaining each step

### Should Have
- [x] Example 6: Multi-page PDF comic
- [x] Example 7: Custom page layout (3x2 grid)
- [x] Example 8: Manual positioning and styling
- [x] Example 9: Using templates (FourKoma, TwoByTwo, etc.)
- [x] Example 10: Error handling and fallbacks
- [x] examples/ directory in project root
- [x] README in examples/ explaining how to run them
- [x] Output PNG files committed to examples/output/ for preview

### Should Have (Extended Examples)
- [x] Example 11: Interactive HTML export with zoom, pan, themes
- [x] Example 12: Parser/DSL markup for rapid comic creation
- [x] Example 13: Visual effects (shake, zoom, motion, focus, impact)
- [x] Example 14: Animation export (GIF) with Timeline and easing functions
- [x] Example 15: Video export (MP4/WebM) with quality settings
- [x] Example 16: Character types showcase (all 9 character styles)
- [x] Example 17: AI image generation (OpenAI DALL-E, Replicate providers)
- [x] Example 18: FlowLayout for responsive positioning
- [x] Example 19: ConstraintLayout for precise, relational positioning
- [x] Example 20: Themes and Styles for consistent comic styling
- [x] Example 21: Text and Narration (StyledText, SFX, NarratorBubble)
- [x] Example 22: Advanced Templates (ThreeRowLayout, MangaPage)
- [x] Example 23: Preview Server for live development
- [x] Example 24: New Templates (NewspaperStrip, Widescreen)
- [x] Example 25: Panel Shapes (DiagonalPanel, TrapezoidPanel, StarburstPanel, CloudPanel, ExplosionPanel, split_diagonal, split_curve)
- [x] Example 26: Stickman Articulation (joint-level arm/leg control, hand gestures, point_at helper)

### Won't Have (This Iteration)
- [ ] Complex multi-page stories (defer to tutorials)
- [ ] Advanced styling and theming (defer to advanced docs)
- [ ] Video tutorials (defer to future)

## Context

### User Flow

1. Developer clones repository or installs library
2. Developer navigates to examples/ directory
3. Developer reads examples/README.md for overview
4. Developer runs `uv run python examples/01_simple_dialogue.py`
5. Example executes and creates examples/output/01_simple_dialogue.png
6. Developer opens PNG to see result
7. Developer reads example code to understand workflow
8. Developer modifies example code to experiment
9. Developer uses example as template for their own comic

### Examples Structure

```
examples/
├── README.md                   # How to run examples
├── 01_simple_dialogue.py       # Two characters talking
├── 02_four_panel_comic.py      # 4koma story
├── 03_group_scene.py           # Multiple characters in one panel
├── 04_expressions.py           # Show all expression types
├── 05_bubble_types.py          # Speech, thought, shout, whisper
├── 06_multi_page_pdf.py        # Using Book class
├── 07_custom_layout.py         # Grid positioning
├── 08_manual_positioning.py    # Precise control
├── 09_using_templates.py       # FourKoma, TwoByTwo, ActionPage, WebComic
├── 10_error_handling.py        # Graceful degradation
├── 11_html_export.py           # Interactive HTML export
├── 12_parser_dsl.py            # Parser/DSL markup
├── 13_visual_effects.py        # Visual effects
├── 14_animation_export.py      # GIF animation export
├── 15_video_export.py          # MP4/WebM video export
├── 16_character_types.py       # All 9 character type showcase
├── 17_ai_image_generation.py   # AI image generation with DALL-E and Replicate
├── 18_flow_layout.py           # FlowLayout responsive positioning
├── 19_constraint_layout.py     # ConstraintLayout relational positioning
├── 20_themes_and_styles.py     # Themes and Styles system
├── 21_text_and_narration.py    # StyledText, SFX, NarratorBubble
├── 22_advanced_templates.py    # ThreeRowLayout, MangaPage templates
├── 23_preview_server.py        # Preview Server for live development
├── 24_new_templates.py         # NewspaperStrip, Widescreen templates
├── 25_panel_shapes.py          # Panel Shapes (DiagonalPanel, TrapezoidPanel, StarburstPanel, CloudPanel, ExplosionPanel)
├── 26_stickman_articulation.py # Stickman articulation (joint control, hand gestures)
└── output/                     # Generated files
    ├── 01_simple_dialogue.png
    ├── 02_four_panel_comic.png
    ├── ...
    ├── 11_html_*.html          # HTML export variants
    ├── 12_parser_*.png         # Parser DSL outputs
    ├── 13_effect_*.png         # Visual effects outputs
    ├── 14_anim_*.gif           # Animation GIF outputs
    ├── 15_video_*.mp4/webm     # Video outputs
    ├── 16_*.png                # Character type outputs
    ├── 18_*.png                # FlowLayout outputs
    ├── 19_*.png                # ConstraintLayout outputs
    ├── 20_*.png                # Themes/Styles outputs
    ├── 21_*.png                # Text/Narration outputs
    ├── 22_*.png                # Advanced template outputs
    ├── 25_*.png                # Panel shapes outputs
    └── 26_*.png                # Stickman articulation outputs
```

### Related Specs

- `getting-started.md` (examples implement these workflows)
- `character-basics.md` (examples demonstrate character usage)
- `speech-bubbles.md` (examples demonstrate bubble usage)
- `page-rendering.md` (examples render to PNG/PDF)

## Example Content

### 01_simple_dialogue.py

```python
"""Simple two-panel dialogue between two stick figures."""

from comix import Page, Panel, Stickman

# Create page with 1x2 layout (two panels side by side)
page = Page(width=800, height=400)
page.set_layout(rows=1, cols=2)

# Panel 1: Alice asks a question
panel1 = Panel()
alice = Stickman(name="Alice", height=100, color="#FF6B9D")
alice.move_to((200, 200))
bubble1 = alice.say("How are you today?")
panel1.add_content(alice, bubble1)

# Panel 2: Bob responds
panel2 = Panel()
bob = Stickman(name="Bob", height=100, color="#4ECDC4")
bob.move_to((200, 200))
bubble2 = bob.say("I'm doing great!")
panel2.add_content(bob, bubble2)

# Assemble and render
page.add(panel1, panel2)
page.auto_layout()
page.render("examples/output/01_simple_dialogue.png")

print("✓ Created examples/output/01_simple_dialogue.png")
```

### 02_four_panel_comic.py

```python
"""Four-panel comic (4koma style) with a simple joke."""

from comix import Page, Stickman
from comix.page.templates import FourKoma

# Use FourKoma template (4 vertical panels)
comic = FourKoma(width=400, height=1200)

# Setup (起)
char1 = Stickman(height=80)
char1.move_to((200, 150))
bubble1 = char1.say("I have a joke about construction")
comic._panels[0].add_content(char1, bubble1)

# Development (承)
char2 = Stickman(height=80)
char2.move_to((200, 150))
bubble2 = char2.say("Oh? Tell me!")
comic._panels[1].add_content(char2, bubble2)

# Twist (転)
char3 = Stickman(height=80)
char3.move_to((200, 150))
bubble3 = char3.say("Sorry, I'm still working on it")
comic._panels[2].add_content(char3, bubble3)

# Conclusion (結)
char4 = Stickman(height=80)
char4.move_to((200, 150))
char4.set_expression("confused")
bubble4 = char4.think("...")
comic._panels[3].add_content(char4, bubble4)

comic.render("examples/output/02_four_panel_comic.png")

print("✓ Created examples/output/02_four_panel_comic.png")
```

### 03_group_scene.py

```python
"""Single panel with multiple characters (group scene)."""

from comix import Page, Panel, Stickman

page = Page(width=800, height=600)
panel = Panel(width=760, height=560)
panel.move_to((400, 300))

# Three characters standing in a row
alice = Stickman(name="Alice", height=100, color="#FF6B9D")
alice.move_to((250, 350))
bubble_a = alice.say("Let's work together!")

bob = Stickman(name="Bob", height=110, color="#4ECDC4")
bob.move_to((400, 350))
bubble_b = bob.say("Great idea!")

charlie = Stickman(name="Charlie", height=95, color="#95E1D3")
charlie.move_to((550, 350))
bubble_c = charlie.say("I'm in!")

# Add all to panel
panel.add_content(alice, bob, charlie)
panel.add_content(bubble_a, bubble_b, bubble_c)

page.add(panel)
page.render("examples/output/03_group_scene.png")

print("✓ Created examples/output/03_group_scene.png")
```

### 04_expressions.py

```python
"""Showcase of different character expressions."""

from comix import Page, Stickman
from comix.page.templates import TwoByTwo

page = TwoByTwo(width=800, height=800)

expressions = ["neutral", "happy", "sad", "angry"]
for i, expr in enumerate(expressions):
    char = Stickman(height=80)
    char.move_to((200, 200))  # Will be auto-positioned by layout
    char.set_expression(expr)
    bubble = char.say(f"I'm {expr}!")
    page._panels[i].add_content(char, bubble)

page.auto_layout()
page.render("examples/output/04_expressions.png")

print("✓ Created examples/output/04_expressions.png")
```

### 05_bubble_types.py

```python
"""Showcase of different speech bubble types."""

from comix import Page, Panel, Stickman, SpeechBubble, ThoughtBubble, ShoutBubble, WhisperBubble

page = Page(width=800, height=1000)
page.set_layout(rows=4, cols=1)

# Speech bubble (normal)
panel1 = Panel()
char1 = Stickman(height=80)
char1.move_to((400, 125))
bubble1 = SpeechBubble(text="This is normal speech")
bubble1.attach_to(char1)
panel1.add_content(char1, bubble1)

# Thought bubble
panel2 = Panel()
char2 = Stickman(height=80)
char2.move_to((400, 125))
bubble2 = ThoughtBubble(text="This is a thought...")
bubble2.attach_to(char2)
panel2.add_content(char2, bubble2)

# Shout bubble
panel3 = Panel()
char3 = Stickman(height=80)
char3.move_to((400, 125))
bubble3 = ShoutBubble(text="THIS IS SHOUTING!")
bubble3.attach_to(char3)
panel3.add_content(char3, bubble3)

# Whisper bubble
panel4 = Panel()
char4 = Stickman(height=80)
char4.move_to((400, 125))
bubble4 = WhisperBubble(text="this is a whisper...")
bubble4.attach_to(char4)
panel4.add_content(char4, bubble4)

page.add(panel1, panel2, panel3, panel4)
page.auto_layout()
page.render("examples/output/05_bubble_types.png")

print("✓ Created examples/output/05_bubble_types.png")
```

### examples/README.md

```markdown
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
6. **06_multi_page_pdf.py** - Creating multi-page PDF comics with Book class
7. **07_custom_layout.py** - Custom grid layouts (3x2, 2x3, etc.)
8. **08_manual_positioning.py** - Precise manual positioning of elements
9. **09_using_templates.py** - Using built-in templates (FourKoma, TwoByTwo, ActionPage, WebComic)
10. **10_error_handling.py** - Graceful error handling and fallbacks
11. **11_html_export.py** - Interactive HTML export with zoom, pan, dark/light themes
12. **12_parser_dsl.py** - Parser/DSL markup for rapid comic creation
13. **13_visual_effects.py** - Visual effects (shake, zoom, motion, focus, impact)
14. **14_animation_export.py** - GIF animation export with Timeline and easing
15. **15_video_export.py** - MP4/WebM video export with quality settings
16. **16_character_types.py** - All 9 character types with expressions and poses
17. **17_ai_image_generation.py** - AI image generation with DALL-E and Replicate
18. **18_flow_layout.py** - FlowLayout for responsive positioning
19. **19_constraint_layout.py** - ConstraintLayout for precise, relational positioning
20. **20_themes_and_styles.py** - Themes and Styles for consistent comic styling
21. **21_text_and_narration.py** - StyledText, SFX, NarratorBubble
22. **22_advanced_templates.py** - ThreeRowLayout, MangaPage templates
23. **23_preview_server.py** - Preview Server for live development
24. **24_new_templates.py** - NewspaperStrip, Widescreen templates
25. **25_panel_shapes.py** - Advanced panel types (DiagonalPanel, TrapezoidPanel, StarburstPanel, CloudPanel, ExplosionPanel, split_diagonal, split_curve)

## Requirements

- Python 3.13+
- Dependencies managed by uv (automatically handled)
- Optional: pycairo for PDF rendering

## Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/comicode.git
cd comicode

# Run an example
uv run python examples/01_simple_dialogue.py

# View the output
open examples/output/01_simple_dialogue.png
```

## Modifying Examples

Feel free to modify these examples to experiment:
- Change character positions
- Add more characters
- Try different expressions
- Customize bubble text
- Adjust page dimensions
- Change colors

## Need Help?

- Check the `specs/` directory for detailed documentation
- See `getting-started.md` for basic workflows
- Report issues at https://github.com/yourusername/comicode/issues
```

## Test Requirements

1. **Example execution**:
   - Test: Each example script runs without errors
   - Test: Each example produces PNG file in output/ directory
   - Test: Generated PNG files are not empty (file size > 1KB)

2. **Code quality**:
   - Test: Basic examples (01-04, 07) are under 50 lines
   - Test: Each example has explanatory comments
   - Test: Code follows consistent style

3. **Output validation**:
   - Test: PNG files contain visible content (not blank)
   - Test: Characters are fully rendered
   - Test: Bubbles have visible borders
   - Test: Text is readable

4. **README accuracy**:
   - Test: All examples listed in README exist
   - Test: README instructions are accurate
   - Test: File paths in README are correct

## Open Questions

- [x] Should examples be run as part of CI/CD tests? **Decision**: Deferred - examples are tested via manual verification during development
- [x] Should example output PNG files be committed to repo? **Decision**: Yes, for preview
- [x] Should examples support command-line arguments? **Decision**: No, keep simple
- [x] Should there be an index.html to preview all examples? **Decision**: Deferred - nice to have for future

## Success Metrics

**This spec is successful when:**
1. ✅ All 26 examples execute without errors
2. ✅ All examples produce correct visual output (fixed in v0.1.85)
3. ✅ A new developer can run examples within 5 minutes
4. ✅ Examples serve as effective templates for custom comics
5. ✅ Example code is clear enough to understand without extensive docs

**Current Status**: All 5 metrics fully met. All visual bugs fixed in v0.1.85.
