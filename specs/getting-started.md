# Getting Started - Creating Your First Comic

## What
A developer can create a simple 2-panel comic with stick figures and speech bubbles using straightforward procedural code.

## Why
Users need a clear, working starting point to understand how to use the Comix library. Without a minimal working example, developers cannot validate that their setup works or understand the basic workflow: create page → add panels → add characters → add bubbles → render output.

## Acceptance Criteria

### Must Have
- [x] Developer can create a Page object with default or custom dimensions
- [x] Developer can add Panel objects to a Page
- [x] Developer can create Stickman characters and position them in panels
- [x] Developer can add SpeechBubble to characters using `.say()` method
- [x] Developer can render the page to PNG format
- [x] The rendered output displays complete stick figures (head, body, arms, legs)
- [x] The rendered output displays speech bubbles with text inside bordered boxes
- [x] The entire workflow completes in under 10 lines of code for a simple comic
- [x] Font fallback works automatically if specified font is unavailable

### Should Have
- [x] Developer can render to PDF format in addition to PNG
- [x] Developer can manually position speech bubbles with `.move_to()` if automatic attachment doesn't fit
- [x] Helpful error messages when required parameters are missing
- [x] Default values make sense (reasonable panel sizes, font sizes, bubble padding)

### Won't Have (This Iteration)
- [x] Complex layouts beyond simple grid (defer to `page-layouts.md`) - *Implemented: GridLayout, FlowLayout, ConstraintLayout*
- [x] Custom character styles beyond Stickman (defer to future specs) - *Implemented: 8 character types*
- [x] Animation or effects (defer to `effects.md`) - *Implemented: 6 effect types*
- [x] Parser/DSL syntax (defer to `parser.md`) - *Implemented: Full parser*

## Context

### User Flow (Happy Path)

1. Developer imports Page, Panel, Stickman, SpeechBubble
2. Developer creates a Page (default 800x1200 or custom size)
3. Developer creates one or more Panel objects
4. Developer creates Stickman characters with positions
5. Developer adds speech bubbles using `character.say("text")`
6. Developer adds characters and bubbles to panel using `panel.add_content()`
7. Developer adds panels to page using `page.add()`
8. Developer calls `page.render("output.png")` to generate PNG
9. PNG file is created showing complete comic with visible characters and bubbles

### Edge Cases

- **No panels added**: Should render empty page with background color
- **Character without speech bubble**: Should render character only
- **Speech bubble without character**: Should render floating bubble at specified position
- **Very long speech bubble text**: Should auto-wrap text into multiple lines within bubble
- **Font not available**: Should fall back to system fonts (sans-serif) automatically
- **Invalid file path**: Should raise clear IOError with path information
- **Panel outside page bounds**: Should render anyway (may be clipped)

### Technical Constraints

- Must work with only numpy and fonttools as core dependencies
- PNG rendering must work without pycairo (use SVG renderer fallback)
- Must work on macOS, Linux, Windows
- Font discovery must work across different OS font locations

### Related Specs

- `character-basics.md` (depends on this for basic character creation)
- `speech-bubbles.md` (depends on this for bubble attachment)
- `page-rendering.md` (related to output formats)

## Examples

### Example 1: Minimal Comic (Single Panel)

```python
from comix import Page, Panel, Stickman, SpeechBubble

# Create page and panel
page = Page(width=400, height=300)
panel = Panel(width=360, height=260)
panel.move_to((200, 150))

# Add character
char = Stickman(name="Bob", height=80)
char.move_to((200, 150))

# Add speech bubble
bubble = char.say("Hello World!")

# Assemble and render
panel.add_content(char, bubble)
page.add(panel)
page.render("my_first_comic.png")
```

**Expected Result**: PNG file with one panel containing a complete stick figure with a speech bubble saying "Hello World!" above the character's head.

### Example 2: Two-Panel Comic (Dialogue)

```python
from comix import Page, Panel, Stickman

# Create page with 1x2 layout
page = Page(width=800, height=400)
page.set_layout(rows=1, cols=2)

# Panel 1
panel1 = Panel()
alice = Stickman(name="Alice", height=100)
alice.move_to((200, 200))
bubble1 = alice.say("How are you?")
panel1.add_content(alice, bubble1)

# Panel 2
panel2 = Panel()
bob = Stickman(name="Bob", height=100)
bob.move_to((600, 200))
bubble2 = bob.say("I'm great!")
panel2.add_content(bob, bubble2)

# Add panels and auto-layout
page.add(panel1, panel2)
page.auto_layout()
page.render("dialogue.png")
```

**Expected Result**: PNG file with two side-by-side panels showing Alice and Bob having a conversation.

### Example 3: Error Handling

```python
from comix import Page

page = Page()
try:
    page.render("/invalid/path/output.png")
except IOError as e:
    print(f"Cannot save file: {e}")
    # Fallback: render to current directory
    page.render("output.png")
```

**Expected Result**: Clear error message when file path is invalid, allowing graceful fallback.

## Open Questions

- [x] Should `Page.render()` create parent directories if they don't exist? **Decision**: No, fail fast with clear error
- [x] Should speech bubbles auto-size based on text length? **Decision**: Yes, with optional fixed width
- [x] What's the default DPI for PNG rendering? **Decision**: 150 DPI (balance between quality and file size)
- [x] Should there be a `Page.show()` method for quick preview in browser? **Decision**: Yes, implemented with auto-cleanup on exit

## Success Metrics

**This spec is successful when:**
1. A developer can copy-paste Example 1 and get a working PNG output
2. The rendered comic shows complete stick figures (not just heads)
3. Speech bubbles appear with visible borders and text inside
4. Font fallback happens silently without errors
5. All 8 "Must Have" acceptance criteria pass tests
