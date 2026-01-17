# Markup Parser - DSL for Rapid Comic Creation

## What

A domain-specific language (DSL) parser that converts text markup into comic pages, enabling rapid prototyping and simplified comic creation without writing Python code for every element.

## Why

Writing Python code for every panel, character, and dialogue line is verbose and slow for rapid iteration. A text-based markup language enables:

1. **Quick prototyping**: Draft comic layouts in plain text
2. **Non-programmer access**: Writers can define comics without Python knowledge
3. **Readability**: Comic scripts read like screenplays
4. **Portability**: Text files are easy to version control and share
5. **Iteration speed**: Faster than modifying Python code

## Acceptance Criteria

### Must Have
- [x] Page declaration with grid layout (`[page RxC]`)
- [x] Panel markers (`# panel N`)
- [x] Character dialogue with modifiers (`Name(mods): "text"`)
- [x] Support for 11 expressions (neutral, happy, sad, etc.)
- [x] Support for 6 positions (left, right, center, closeup, top, bottom)
- [x] Support for 4 facing directions (left, right, front, back)
- [x] Support for 5 bubble types (speech, thought, shout, whisper)
- [x] Sound effects (`sfx: TEXT`)
- [x] Narrator boxes (`narrator: "text"`)
- [x] Background directives (`[background: ...]`)
- [x] Comments (// and # styles)
- [x] Unicode/Korean character support
- [x] Convert parsed markup to renderable Page object

### Should Have
- [x] Auto-panel creation for content without explicit markers
- [x] Character reuse within same panel
- [x] Position-based facing direction inference
- [x] Both single and double quote support
- [x] Graceful handling of malformed lines
- [x] Page dimension specification (`[page RxC WxH]`)

### Won't Have (This Iteration)
- [ ] Multi-page markup files
- [ ] Custom character styles in markup
- [ ] Effect declarations in markup
- [ ] Import/include statements
- [ ] Variables or macros

## Context

### Markup Syntax Reference

#### Page Declaration
```
[page 2x2]              # 2 rows, 2 columns, default size
[page 3x1 1000x1500]    # 3 rows, 1 column, 1000x1500 pixels
```

#### Panel Markers
```
# panel 1
# panel 2
```

#### Character Dialogue
```
Name(modifiers): "dialogue text"
Name(modifiers): 'dialogue text'

# Modifiers (comma-separated):
# Expressions: neutral, happy, sad, angry, surprised, confused, sleepy, excited, scared, smirk, crying
# Positions: left, right, center, closeup, top, bottom
# Directions: front, back (overrides position-based facing)
# Bubbles: speech, thought, think, shout, whisper
```

#### Sound Effects
```
sfx: BOOM
sfx: 쾅!
```

#### Narrator
```
narrator: "Meanwhile, in another dimension..."
narrator: '나레이션 텍스트'
```

#### Backgrounds
```
[background: #ff5500]           # Hex color
[background: blue]              # Named color
[background: /path/to/img.png]  # Image file
[background: A sunny beach]     # Description (for AI)
```

#### Comments
```
// C-style comment
# Hash comment (must not match panel marker)
#! Shebang style
```

### Position-Based Facing

When a position is specified, facing direction is automatically inferred:
- `left` position → character faces `right`
- `right` position → character faces `left`
- Explicit direction (`front`, `back`) overrides this

### Supported Colors

Named colors: white, black, red, green, blue, yellow, orange, purple, pink, gray, grey, brown, cyan, magenta, transparent, none

### Supported Image Formats

.png, .jpg, .jpeg, .gif, .svg, .webp

## Examples

### Example 1: Simple Two-Character Dialogue

```
[page 1x2]

# panel 1
Alice(left, happy): "Hello, how are you?"
Bob(right): "I'm doing great!"

# panel 2
Alice(left, surprised): "Really?"
Bob(right, happy): "Yes, really!"
```

### Example 2: Korean Dialogue

```
[page 2x2]

# panel 1
철수(left, surprised): "뭐라고?!"
영희(right, smirk): "응, 진짜야"

# panel 2
철수(closeup): "..."
sfx: 충격

# panel 3
[background: 카페 전경]
narrator: "그날 이후..."

# panel 4
철수(center): "믿을 수 없어"
```

### Example 3: Different Bubble Types

```
[page 1x4]

# panel 1
Alice(center, neutral, speech): "This is a speech bubble."

# panel 2
Alice(center, confused, thought): "Am I thinking?"

# panel 3
Alice(center, angry, shout): "I'M SHOUTING!"

# panel 4
Alice(center, scared, whisper): "This is a whisper..."
```

### Example 4: Using the Parser API

```python
from comix.parser import parse_markup

markup = """
[page 2x2]

# panel 1
Alice(left, happy): "Hello!"

# panel 2
Bob(right, surprised): "Hi there!"
"""

# Parse and render
page = parse_markup(markup)
page.render("comic.png", format="png")
```

### Example 5: Direct Parser Access

```python
from comix.parser import MarkupParser

parser = MarkupParser(markup_text)
spec = parser.parse()  # Returns PageSpec

# Inspect specification
print(f"Grid: {spec.rows}x{spec.cols}")
for panel in spec.panels:
    for action in panel.actions:
        print(action)

# Convert to Page
page = parser.to_page()
```

## Open Questions

- [x] Support multi-page in single file? **Decision**: No, use Book class for multi-page
- [x] Handle invalid modifiers? **Decision**: Silently ignore, use defaults
- [x] Allow nested quotes? **Decision**: No, use opposite quote type
- [x] Support custom character styles? **Decision**: Defer to future iteration

## Test Requirements

1. **Page Parsing**:
   - Test: Default 1x1 grid when no declaration
   - Test: Custom dimensions parsed correctly
   - Test: Panel count matches grid

2. **Character Parsing**:
   - Test: Name extraction (ASCII and Unicode)
   - Test: All 11 expressions recognized
   - Test: All 6 positions recognized
   - Test: Direction override works
   - Test: Bubble type selection

3. **Content Parsing**:
   - Test: SFX text extraction
   - Test: Narrator text with both quote types
   - Test: Background color parsing
   - Test: Background image path recognition
   - Test: Background description (non-color, non-image)

4. **Edge Cases**:
   - Test: Empty lines skipped
   - Test: Comments ignored
   - Test: Malformed lines don't crash parser
   - Test: Auto-panel creation without markers
   - Test: Character reuse in same panel

5. **Integration**:
   - Test: Full markup to Page conversion
   - Test: Rendered output contains all elements
   - Test: Korean text renders correctly

## Implementation Status

Fully implemented in `/comix/parser/parser.py` with 76 tests in `/tests/test_parser.py`.
