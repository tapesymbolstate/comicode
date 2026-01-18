# Character Basics - Creating and Positioning Characters

## What
A system for creating stick figure characters, positioning them in panels, and setting their expressions and poses.

## Why
Characters are the core visual element of comics. Developers need a simple way to create characters that:
- Render completely (head, body, arms, legs - not just partial geometry)
- Can be positioned precisely in panels
- Support basic expressions for emotion
- Support basic poses for body language

Without working character rendering, comics appear broken or incomplete.

## Acceptance Criteria

### Must Have
- [x] Stickman character renders completely (head circle, body line, 2 arms, 2 legs)
- [x] Character can be positioned using `.move_to(x, y)`
- [x] Character can be positioned relative to other objects using `.next_to(other)`
- [x] Character height can be specified and affects all body parts proportionally
- [x] Character defaults to facing right, can face left with `.face("left")`
- [x] Character has default "neutral" expression
- [x] Character can be created with simple code: `char = Stickman()`

### Should Have
- [x] Character supports basic expressions: neutral, happy, sad, angry, surprised - *Implemented: 11 expressions*
- [x] Character supports basic poses: standing, sitting, waving - *Implemented: 12 poses*
- [x] Character.say() method returns SpeechBubble that auto-attaches
- [x] Character.think() method returns ThoughtBubble that auto-attaches
- [x] Character.shout() method returns ShoutBubble that auto-attaches
- [x] Character.whisper() method returns WhisperBubble that auto-attaches
- [x] Character color can be customized
- [x] Character has a name property for debugging

### Implemented Beyond Original Scope
- [x] 9 character styles: Stickman, SimpleFace, ChubbyStickman, Robot, Chibi, Anime, Superhero, Cartoon, AnimalStyle
- [x] 11 expressions: neutral, happy, sad, angry, surprised, confused, sleepy, excited, scared, smirk, crying
- [x] 12 poses: standing, sitting, waving, pointing, walking, running, jumping, dancing, lying, kneeling, cheering, thinking
- [x] AnimalStyle species: cat, dog, rabbit, fox, bear, bird, wolf with customizable fur colors and features

### Won't Have
- [ ] Custom body part proportions (beyond character style presets)
- [ ] Clothing or accessories
- [ ] Shadows or 3D effects

## Context

### User Flow

1. Developer creates character: `char = Stickman(height=100)`
2. Developer positions character: `char.move_to((200, 300))`
3. (Optional) Developer sets expression: `char.set_expression("happy")`
4. (Optional) Developer sets pose: `char.set_pose("waving")`
5. (Optional) Developer sets direction: `char.face("left")`
6. Developer adds to panel: `panel.add_content(char)`
7. Renderer draws complete stick figure at specified location

### Edge Cases

- **Character positioned outside panel bounds**: Render anyway, may be clipped
- **Height = 0 or negative**: Raise ValueError with clear message
- **Unknown expression name**: Fall back to "neutral" and log warning
- **Unknown pose name**: Fall back to "standing" and log warning
- **Two characters overlap**: Both render, last added is on top (z-index)
- **Character added directly to page without panel**: Should work for simple cases

### Technical Constraints

- Rendering must work in both SVG and Cairo backends
- Character geometry must scale proportionally based on height parameter
- Must calculate bounding box correctly for `.next_to()` positioning
- Expression and pose changes must trigger re-render

### Implementation Notes

**Character Proportions** (implemented):
- Head: Circle at top (15% of height for Stickman, varies by style)
- Body: Vertical line from head to pelvis (50% of height)
- Arms: Two lines from shoulders (30% down from head)
- Legs: Two lines from pelvis to feet (35% of height)

### Related Specs

- `getting-started.md` (uses basic character creation)
- `speech-bubbles.md` (characters host bubbles)
- `page-layouts.md` (characters positioned in panels)

## Examples

### Example 1: Basic Character

```python
from comix import Stickman, Panel

panel = Panel(width=400, height=400)

char = Stickman(name="Alice", height=120)
char.move_to((200, 200))

panel.add_content(char)

# Render should show complete stick figure:
# - Round head at (200, 200)
# - Body, arms, legs extending downward
```

**Expected Visual**:
```
    O     <- head (circle)
   /|\    <- body (line) and arms (two lines)
   / \    <- legs (two lines)
```

### Example 2: Character Positioning

```python
from comix import Stickman, Panel, Rectangle

panel = Panel(width=600, height=400)

# Absolute positioning
char1 = Stickman(height=100)
char1.move_to((150, 200))

# Relative positioning
char2 = Stickman(height=100)
char2.next_to(char1, direction="right", buff=50)

panel.add_content(char1, char2)
```

**Expected Result**: Two stick figures side by side with 50 pixels between them.

### Example 3: Expression and Pose

```python
from comix import Stickman, Panel

panel = Panel(width=400, height=400)

char = Stickman(height=120)
char.move_to((200, 250))
char.set_expression("happy")  # Smiling face
char.set_pose("waving")        # One arm raised
char.face("left")              # Facing left

panel.add_content(char)
```

**Expected Result**: Happy stick figure waving with left arm raised, facing left.

### Example 4: Character with Bubbles

```python
from comix import Stickman, Panel

panel = Panel(width=400, height=400)

char = Stickman(height=100)
char.move_to((200, 250))

# Automatic bubble attachment
bubble = char.say("Hello!")  # SpeechBubble auto-positioned above head

panel.add_content(char, bubble)
```

**Expected Result**: Stick figure with speech bubble above head.

### Example 5: Custom Colors

```python
from comix import Stickman, Panel

panel = Panel(width=400, height=400)

char = Stickman(
    name="Bob",
    height=100,
    color="#0066CC",      # Blue character
    fill_color="#CCE5FF"  # Light blue fill
)
char.move_to((200, 200))

panel.add_content(char)
```

**Expected Result**: Blue stick figure with light blue fill.

## Open Questions

- [x] Should characters have default fill color or just stroke? **Decision**: Stroke only by default, optional fill
- [x] Should `.face()` mirror the geometry or just track direction? **Decision**: Mirror geometry
- [x] What's the default character height? **Decision**: 100 pixels
- [x] Should character support `.copy()` for creating duplicates? **Decision**: Yes, implemented via `CObject.copy()`

## Test Requirements

From acceptance criteria, tests must verify:

1. **Complete rendering**:
   - Test: SVG output contains head circle, body line, two arm lines, two leg lines
   - Test: Cairo PNG output shows all body parts when inspected

2. **Positioning**:
   - Test: `move_to((100, 200))` places character center at (100, 200)
   - Test: `next_to(other, "right")` positions character to right of other object

3. **Scaling**:
   - Test: height=50 renders half-size compared to height=100
   - Test: All body parts scale proportionally

4. **Facing**:
   - Test: `.face("left")` mirrors geometry horizontally
   - Test: `.face("right")` returns to default orientation

5. **Expressions and poses**:
   - Test: `.set_expression("happy")` changes facial features
   - Test: `.set_pose("waving")` changes arm positions
   - Test: Unknown expression falls back to "neutral" without error

## Implementation Status

All character rendering issues have been resolved. Full expression and pose rendering is implemented in both SVG and Cairo renderers. See `IMPLEMENTATION_PLAN.md` for details on bug fixes and test coverage.
