# Speech Bubble Tail Improvements

## What
Intelligent speech bubble tail rendering that prevents excessive tail lines and provides natural-looking connections between bubbles and characters.

## Why
Current implementation issues:
- **Fixed tail length**: Tail has constant length regardless of distance to character
- **Excessive lines**: When bubble is far from character, tail looks unnaturally long and distracting
- **No distance awareness**: Tail doesn't adapt to bubble-character proximity
- **Visual clutter**: Long tails create visual noise that detracts from comic readability

Professional comics use short, clean tail indicators that subtly show who's speaking without dominating the panel. Overly long tails are considered amateurish.

## Acceptance Criteria

### Must Have
- [ ] Auto-calculate tail length based on bubble-to-character distance
- [ ] Maximum tail length limit (default: 50px) to prevent excessive lines
- [ ] Minimum tail length (default: 15px) for visibility
- [ ] `tail_mode="auto"` (default) calculates length automatically
- [ ] `tail_mode="fixed"` uses specified tail_length
- [ ] `tail_mode="none"` disables tail completely
- [ ] Tail points toward character's center (or custom target point)

### Should Have
- [ ] Curved/bezier tail option for softer appearance
- [ ] `smart_attach_to()` method positions bubble optimally AND sets appropriate tail
- [ ] Tail width scales with distance (closer = wider, farther = narrower)
- [ ] Multiple tail style presets: "classic" (triangle), "smooth" (curved), "minimal" (small nub)
- [ ] Automatic tail omission if bubble is very close to character (< 20px)

### Won't Have (This Iteration)
- [ ] Tail that wraps around obstacles
- [ ] Multiple tails pointing to multiple characters
- [ ] Animated tail transitions
- [ ] Tail collision detection with other objects

## Context

### Problem Description

When using `character.say("Hello!")` or `bubble.attach_to(character)`, the tail is rendered with a fixed length (default 30px). This causes issues:

**Issue 1: Far-away bubbles get long tails**
```
Character here → O
                /|\
                / \



   ┌──────────┐
   │  Hello!  │ ← Bubble positioned 200px above
   └────┬─────┘
        │
        │  ← This line is 170px long (200 - 30)
        │     Looks unnatural!
        │
        ▼
```

**Issue 2: Nearby bubbles look the same**
- Bubble 30px from character: tail = 30px
- Bubble 200px from character: tail = 30px
- Both look identical, but one is appropriate and one is too short

**Issue 3: No option to disable tail**
- Narrator bubbles should have no tail, but removing tail requires setting `tail_length=0` manually
- Not intuitive for users

### Desired Behavior

**Auto-length calculation**:
```python
# Bubble close to character
bubble = char.say("Hi!")  # Auto: tail = 20px (short, appropriate)

# Bubble far from character
bubble = char.say("Hello from afar!")
bubble.move_to((200, 100))  # Auto: tail = 50px (max limit, clean)

# Very close bubble
bubble.move_to(char.get_position())  # Auto: no tail (< 20px threshold)
```

**Manual control**:
```python
# Force specific length
bubble = SpeechBubble(text="Test", tail_mode="fixed", tail_length=40)

# Disable tail
bubble = SpeechBubble(text="Narration", tail_mode="none")
```

### Edge Cases

- **Bubble overlaps character**: No tail (distance < 20px)
- **Bubble very far (500px+)**: Tail capped at max_tail_length (default 50px)
- **No tail_target set**: No tail rendered (or default to bottom if auto-positioning)
- **Bubble positioned manually after attach**: Tail length recalculates on render
- **tail_target is CObject without position**: Use (0, 0) as fallback
- **Bubble inside panel, character outside**: Tail points toward panel edge
- **Multiple bubbles from same character**: Each gets independent tail

### Technical Constraints

- Tail calculation happens during `build()` or `render()`, not at bubble creation
- Must access tail_target position at render time (may have moved)
- Tail points stored as `self._tail_points` array
- Renderers (SVG, Cairo, HTML) all use `data["tail_points"]`
- Must maintain backward compatibility with existing `tail_length` parameter

### Related Specs

- `speech-bubbles.md` (original bubble specification)
- `character-basics.md` (character.say() method)
- `page-rendering.md` (rendering pipeline)

## Examples

### Example 1: Auto-Length Tail (Default Behavior)

```python
from comix import Page, Panel, Stickman

page = Page(width=800, height=600)
panel = Panel()

char = Stickman(height=100)
char.move_to((400, 400))

# Bubble positioned 80px above character
bubble = char.say("Hello!")  # tail_mode="auto" by default
bubble.move_to((400, 250))  # 150px distance from character

panel.add_content(char, bubble)
page.add(panel)
page.render("auto_tail.png")

# Result: tail_length automatically calculated
# distance = 150px
# auto_length = min(150 * 0.4, 50) = 50px (capped at max)
# Tail is 50px long, clean and professional
```

### Example 2: No Tail for Very Close Bubbles

```python
from comix import Page, Panel, Stickman

panel = Panel()
char = Stickman(height=100)
char.move_to((400, 300))

# Bubble very close to character's head
bubble = char.say("Hi!")
bubble.move_to((400, 240))  # Only 60px from character center

panel.add_content(char, bubble)

# Result: tail_length = 0 (automatically disabled)
# distance = 60px, but bubble is already touching head
# No tail needed
```

### Example 3: Fixed Tail Length

```python
from comix import SpeechBubble

# Force specific tail length regardless of distance
bubble = SpeechBubble(
    text="Custom tail!",
    tail_mode="fixed",
    tail_length=35,  # Always 35px
    tail_direction="bottom"
)
bubble.move_to((300, 200))
bubble.point_to((300, 400))  # Target 200px away

# Result: tail is exactly 35px, regardless of 200px distance
```

### Example 4: Disabled Tail for Narrator

```python
from comix import SpeechBubble

# Narrator bubble with no tail
narrator = SpeechBubble(
    text="Meanwhile, at the secret base...",
    tail_mode="none",  # Explicitly disable tail
    width=350
)
narrator.move_to((400, 50))

# Result: no tail rendered, rectangular bubble only
```

### Example 5: Smart Attach with Optimized Tail

```python
from comix import Panel, Stickman, SpeechBubble

panel = Panel(width=600, height=400)
char = Stickman(height=100)
char.move_to((300, 250))

bubble = SpeechBubble(text="Smart positioning!")
bubble.smart_attach_to(char, panel)  # New method

panel.add_content(char, bubble)

# Result: bubble positioned optimally (not overlapping)
# tail_length automatically set based on final position
# tail_direction automatically chosen based on bubble placement
```

### Example 6: Curved Tail Style

```python
from comix import SpeechBubble

bubble = SpeechBubble(
    text="Smooth!",
    tail_style="smooth",  # Use curved bezier tail
    tail_mode="auto"
)
bubble.attach_to(character)

# Result: tail rendered as smooth curve instead of straight triangle
# More organic, less geometric appearance
```

## Implementation Notes

### Auto-Length Calculation

```python
def _calculate_auto_tail_length(
    bubble_pos: tuple[float, float],
    target_pos: tuple[float, float],
    min_length: float = 15.0,
    max_length: float = 50.0,
    distance_threshold: float = 20.0,
    length_ratio: float = 0.4,
) -> float:
    """Calculate automatic tail length based on bubble-target distance.

    Args:
        bubble_pos: Bubble center position
        target_pos: Target (character) center position
        min_length: Minimum tail length in pixels
        max_length: Maximum tail length in pixels
        distance_threshold: Distance below which tail is disabled
        length_ratio: Ratio of distance to use as tail length (0.4 = 40%)

    Returns:
        Calculated tail length, or 0 if disabled
    """
    distance = np.linalg.norm(
        np.array(bubble_pos) - np.array(target_pos)
    )

    # Disable tail if very close
    if distance < distance_threshold:
        return 0.0

    # Calculate proportional length
    auto_length = distance * length_ratio

    # Clamp to min/max range
    return np.clip(auto_length, min_length, max_length)
```

### Bubble Class Changes

```python
class Bubble(CObject):
    def __init__(
        self,
        text: str = "",

        # Tail configuration
        tail_mode: str = "auto",  # "auto", "fixed", "none"
        tail_length: float = 30.0,  # Used when tail_mode="fixed"
        tail_direction: str = "bottom-left",
        tail_width: float = 20.0,
        tail_style: str = "classic",  # "classic", "smooth", "minimal"

        # Auto-length parameters
        min_tail_length: float = 15.0,
        max_tail_length: float = 50.0,
        tail_distance_threshold: float = 20.0,

        **kwargs
    ):
        self.tail_mode = tail_mode
        self.tail_length = tail_length  # Fixed mode value
        self.tail_style = tail_style
        self.min_tail_length = min_tail_length
        self.max_tail_length = max_tail_length
        self.tail_distance_threshold = tail_distance_threshold
        # ...

    def _generate_tail(self) -> None:
        """Generate tail points based on tail_mode."""
        if self.tail_mode == "none":
            self._tail_points = np.zeros((0, 2))
            return

        # Determine effective tail length
        if self.tail_mode == "auto" and self.tail_target is not None:
            bubble_pos = self.get_center()
            if isinstance(self.tail_target, CObject):
                target_pos = self.tail_target.get_center()
            else:
                target_pos = self.tail_target

            effective_length = self._calculate_auto_tail_length(
                bubble_pos,
                target_pos,
                self.min_tail_length,
                self.max_tail_length,
                self.tail_distance_threshold,
            )
        else:  # tail_mode == "fixed"
            effective_length = self.tail_length

        # Generate tail points
        if self.tail_style == "smooth":
            self._tail_points = self._create_curved_tail(effective_length)
        else:  # "classic" or "minimal"
            self._tail_points = create_tail_points(
                width=self.width,
                height=self.height,
                direction=self.tail_direction,
                length=effective_length,
                tip_width=self.tail_width,
            )
```

### Curved Tail Generation

```python
def _create_curved_tail(
    self,
    length: float
) -> np.ndarray:
    """Create smooth curved tail using bezier curve.

    Returns tail as series of points forming smooth curve.
    """
    # Base attachment point on bubble
    base_x, base_y = self._get_tail_base_point()

    # Target tip point
    tip_x, tip_y = self._get_tail_tip_point(length)

    # Control points for smooth curve
    control1 = (base_x, base_y - length * 0.3)
    control2 = (tip_x, tip_y + length * 0.3)

    # Generate bezier curve
    curve_points = bezier_curve(
        (base_x, base_y),
        control1,
        control2,
        (tip_x, tip_y),
        num_points=8
    )

    # Create filled region (curve + narrow parallel curve)
    # Return points forming closed polygon for fill
    return curve_points
```

### Smart Attach Method

```python
def smart_attach_to(
    self,
    character: CObject,
    panel: Panel | None = None,
    preferred_positions: list[str] = ["above", "right", "left", "below"],
) -> Self:
    """Attach bubble to character with intelligent positioning and tail.

    Combines optimal positioning with automatic tail configuration.
    """
    # Find best position that doesn't overlap
    for position in preferred_positions:
        test_pos = self._calculate_position(character, position)
        if panel is None or not self._would_overlap(test_pos, panel):
            self.move_to(test_pos)
            break

    # Set tail target and mode
    self.tail_target = character
    self.tail_mode = "auto"  # Enable automatic tail length

    # Auto-determine tail direction based on bubble position relative to character
    self.tail_direction = self._auto_determine_tail_direction(character)

    return self
```

## Open Questions

- [x] Should tail_mode="auto" be default? **Decision**: Yes, provides best UX
- [x] What's appropriate length_ratio (40%? 50%?)? **Decision**: 40% (prevents overly long tails)
- [x] Should we provide tail_style="curved"? **Decision**: Yes, "smooth" style for organic look
- [ ] Should tail width also scale with distance? **Decision needed** (probably yes for very far bubbles)
- [ ] Should smart_attach_to() replace attach_to()? **Decision needed** (probably keep both)

## Test Requirements

1. **Auto-length calculation**:
   - Test: Bubble 100px from character → tail ≈ 40px
   - Test: Bubble 200px from character → tail = 50px (capped)
   - Test: Bubble 15px from character → tail = 0 (disabled)

2. **Tail modes**:
   - Test: tail_mode="auto" calculates length dynamically
   - Test: tail_mode="fixed" uses specified tail_length
   - Test: tail_mode="none" renders no tail

3. **Backward compatibility**:
   - Test: Existing code without tail_mode still works (defaults to auto)
   - Test: Specifying tail_length without tail_mode uses that length

4. **Curved tails**:
   - Test: tail_style="smooth" renders curved tail
   - Test: Curved tail points toward target correctly

5. **Smart attach**:
   - Test: smart_attach_to() positions bubble without overlap
   - Test: smart_attach_to() sets appropriate tail direction

## Success Metrics

**This spec is successful when:**
1. `char.say("Hello")` produces bubbles with appropriate tail lengths automatically
2. Bubbles far from characters (200px+) have max 50px tails (not excessive lines)
3. Bubbles very close to characters (< 20px) have no tail
4. `tail_mode="none"` creates clean narrator bubbles without tails
5. Curved tails (tail_style="smooth") render smoothly without jaggy edges
6. Visual output looks professional and matches hand-drawn comic conventions
7. No more "계속 줄이 쭉 그어지는" (continuously drawn long lines) problem

## Visual Examples from Professional Comics

**Good tail examples (what we want to achieve)**:
- xkcd: Very short nubs (10-20px), minimalist
- Calvin & Hobbes: Proportional tails that never dominate panel
- Manga: Short triangular tails, often just small indicators

**Bad tail examples (what we want to avoid)**:
- Tails that span more than 1/4 of panel height
- Tails longer than the bubble itself
- Perfectly straight tails over long distances (use curves for >60px)
- Tails when bubble is already touching character

This specification addresses the user's complaint about excessive tail lines and provides professional-quality speech bubble rendering.
