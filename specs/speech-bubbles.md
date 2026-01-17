# Speech Bubbles - Adding Dialogue to Characters

## What
A system for creating speech bubbles that contain text and attach to characters, with automatic positioning and sizing.

## Why
Dialogue is essential to comics. Speech bubbles must:
- Display text inside a bordered, rounded rectangle
- Have a "tail" pointing to the speaking character
- Auto-size to fit text content
- Support word wrapping for long text

Without visible bubble borders and proper attachment, dialogue appears as floating text without context.

## Acceptance Criteria

### Must Have
- [x] SpeechBubble renders with visible border (stroke around bubble)
- [x] SpeechBubble renders with white/light background (fill color)
- [x] SpeechBubble displays text inside the bubble boundaries
- [x] SpeechBubble has a tail pointing toward attached character
- [x] SpeechBubble auto-sizes width and height to fit text
- [x] Long text automatically wraps to multiple lines
- [x] `character.say("text")` creates and attaches bubble automatically
- [x] Bubble can be manually positioned with `.move_to(x, y)` if needed

### Should Have
- [x] Bubble supports different types: Speech, Thought, Shout, Whisper, Narrator
- [x] ThoughtBubble has cloud-like border (rounded/wavy)
- [x] ShoutBubble has jagged/spiky border
- [x] WhisperBubble has dashed border
- [x] NarratorBubble has rectangular border with no tail
- [x] `character.think("text")` creates ThoughtBubble
- [x] `character.shout("text")` creates ShoutBubble
- [x] Bubble padding can be customized
- [x] Text alignment can be set (left, center, right)

### Won't Have (This Iteration)
- [ ] Bubbles with multiple tails (pointing to multiple characters)
- [ ] Curved/wavy tail paths
- [ ] Bubble-to-bubble connectors for sequential dialogue
- [ ] Rich text formatting (bold, italic) inside bubbles
- [ ] Image or emoji support inside bubbles

## Context

### User Flow (Automatic Attachment)

1. Developer creates character and positions it
2. Developer calls `bubble = character.say("Hello")`
3. Bubble is created with:
   - Text content = "Hello"
   - Width/height auto-calculated based on text
   - Position calculated to be above character's head
   - Tail pointing down toward character
4. Developer adds bubble to panel: `panel.add_content(bubble)`
5. Renderer draws bubble with border, fill, text, and tail

### User Flow (Manual Positioning)

1. Developer creates bubble: `bubble = SpeechBubble(text="Hello")`
2. Developer positions bubble: `bubble.move_to((300, 100))`
3. Developer sets tail target: `bubble.point_to(character)`
4. Developer adds to panel: `panel.add_content(bubble)`

### Edge Cases

- **Empty text**: Render bubble with minimum size (padding only)
- **Very long text (1000+ chars)**: Auto-wrap and expand bubble vertically
- **Text with newlines**: Respect explicit line breaks
- **Text wider than panel**: Wrap at panel boundaries or specified max_width
- **Bubble positioned outside panel**: Render anyway, may be clipped
- **Tail target off-screen**: Tail points in general direction, may not be visible
- **Multiple bubbles attached to same character**: Stack above each other or side-by-side

### Technical Constraints

- Text measurement must account for font size, family, and style
- Must support CJK characters (Korean, Japanese, Chinese) with proper width calculation
- Bubble path must be generated with rounded corners (bezier curves)
- Tail must be a triangle or curved path connecting bubble to target
- Rendering must work in both SVG and Cairo backends
- Font fallback must work if specified font unavailable

### Current Issues Identified

Based on test output showing text but no bubble border:
1. Bubble path generation may not be working (`create_bubble_path()`)
2. Renderer may not be drawing the bubble border/fill
3. Tail may not be rendering
4. Only text object is being rendered, bubble container is skipped

### Related Specs

- `getting-started.md` (basic bubble usage)
- `character-basics.md` (character.say() method)
- `text-rendering.md` (text layout and wrapping)

## Examples

### Example 1: Basic Speech Bubble

```python
from comix import Stickman, SpeechBubble, Panel

panel = Panel(width=400, height=400)

char = Stickman(height=100)
char.move_to((200, 300))

bubble = SpeechBubble(text="Hello World!")
bubble.attach_to(char)

panel.add_content(char, bubble)
```

**Expected Visual**:
```
   ┌──────────────┐
   │ Hello World! │
   └──────┬───────┘
         │ tail pointing down
         ▼
       O   <- character head
      /|\
      / \
```

### Example 2: Using character.say()

```python
from comix import Stickman, Panel

panel = Panel(width=400, height=400)

char = Stickman(height=100)
char.move_to((200, 300))

bubble = char.say("This is easier!")
# Bubble auto-created and positioned

panel.add_content(char, bubble)
```

**Expected Result**: Same as Example 1, but with simpler code.

### Example 3: Different Bubble Types

```python
from comix import Stickman, Panel

panel = Panel(width=800, height=300)

char = Stickman(height=80)
char.move_to((200, 200))

speech = char.say("Normal speech")
thought = char.think("Internal thought")
shout = char.shout("LOUD YELLING!")

# Bubbles will have different visual styles
panel.add_content(char, speech)  # For separate panels
```

**Expected Result**:
- `speech`: Rounded rectangle bubble
- `thought`: Cloud-like wavy border
- `shout`: Jagged spiky border, bold text

### Example 4: Long Text Wrapping

```python
from comix import Stickman, SpeechBubble, Panel

panel = Panel(width=400, height=400)

char = Stickman(height=100)
char.move_to((200, 300))

long_text = "This is a very long sentence that should automatically wrap into multiple lines within the bubble."

bubble = SpeechBubble(
    text=long_text,
    max_width=200  # Force wrapping at 200px
)
bubble.attach_to(char)

panel.add_content(char, bubble)
```

**Expected Result**: Bubble with text wrapped into multiple lines, bubble expanded vertically to fit.

### Example 5: Manual Positioning

```python
from comix import Stickman, SpeechBubble, Panel

panel = Panel(width=400, height=400)

char = Stickman(height=100)
char.move_to((300, 300))

bubble = SpeechBubble(text="Custom position")
bubble.move_to((150, 150))  # Top-left corner
bubble.point_to(char)        # Tail points to character

panel.add_content(char, bubble)
```

**Expected Result**: Bubble at (150, 150) with tail curving toward character at (300, 300).

### Example 6: Narrator Bubble (No Tail)

```python
from comix import NarratorBubble, Panel

panel = Panel(width=400, height=400)

narration = NarratorBubble(
    text="Meanwhile, at the secret base...",
    width=350
)
narration.move_to((200, 50))  # Top of panel

panel.add_content(narration)
```

**Expected Result**: Rectangular bubble at top of panel with no tail, formal appearance.

## Open Questions

- [x] Should bubble auto-position above or beside character? **Decision**: Above by default, configurable
- [x] What's default bubble padding? **Decision**: (15, 20, 15, 20) - top, right, bottom, left
- [x] Should bubble overlap character or stay separated? **Decision**: Separated with configurable buffer
- [x] Max line length before wrapping? **Decision**: Based on max_width or auto-calculated
- [ ] Should bubbles auto-avoid overlapping each other? **Decision needed** (complex, defer to future)

## Test Requirements

1. **Bubble rendering**:
   - Test: SVG output contains `<path>` for bubble outline
   - Test: SVG output contains `fill` and `stroke` attributes
   - Test: Cairo PNG shows visible bubble border (not just text)

2. **Text inside bubble**:
   - Test: Text is positioned inside bubble boundaries
   - Test: Text does not overflow bubble edges

3. **Auto-sizing**:
   - Test: Bubble width/height match text dimensions + padding
   - Test: Long text expands bubble vertically

4. **Tail rendering**:
   - Test: SVG output contains tail path pointing to target
   - Test: Tail connects bubble to character position

5. **Different bubble types**:
   - Test: SpeechBubble has rounded corners
   - Test: ThoughtBubble has cloud-like border
   - Test: ShoutBubble has jagged edges
   - Test: NarratorBubble has no tail

## Bug Fixes Required

Based on current diagnosis (text renders but no bubble border):

1. **Investigate** `Bubble.generate_points()` - ensure bubble path is generated
2. **Investigate** `create_bubble_path()` utility - verify bezier curve generation
3. **Investigate** SVG/Cairo renderers - ensure they draw bubble fill and stroke
4. **Verify** bubble is added to render queue (not just text child)
5. **Add tests** to verify bubble border visibility in output
