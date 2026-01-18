# Stickman Character - Reference-Based Design

## What
Redesign Stickman character proportions and structure to match real-world webcomic stick figure standards (xkcd, Cyanide & Happiness, etc.) for authentic and recognizable appearance.

## Why
Current stickman implementation may not match what users expect when they think "stick figure comic character." Real webcomics use specific proportions and conventions that make stick figures appealing and expressive:

- **xkcd standard**: Very simple, clean lines with specific head-to-body ratios
- **Professional proportions**: ~7-8 head heights for adults (anatomically informed)
- **Webcomic conventions**: Distinct visual language users recognize instantly

Without reference-based design, our stickman characters may look "off" or "weird" compared to beloved stick figure comics users are familiar with.

## Acceptance Criteria

### Must Have
- [x] Head size follows webcomic standards (proportional to body)
- [x] Body (torso) length matches real stick figure proportions
- [x] Limb lengths match human proportions (arms reach mid-thigh when standing)
- [x] Clean, simple lines (no over-complication)
- [x] Recognizable as "stick figure" at first glance
- [x] Joints (elbows, knees) positioned anatomically correctly
- [x] Standing pose looks natural and balanced

### Should Have
- [x] Reference-based ratio presets: "xkcd", "classic", "tall", "child" (was "chibi-stick")
- [x] Configurable head_ratio parameter (default: 0.133 for ~7.5 heads height)
- [x] Elbow positioned at waist level when arms down (anatomical accuracy)
- [x] Knees at midpoint of legs
- [x] Slight curve/roundness option for head (not perfectly circular) - `head_squash` parameter
- [ ] Line width consistency across all body parts

### Won't Have (This Iteration)
- [ ] Detailed anatomy (muscles, facial features beyond simple dots/lines)
- [ ] Stick figure with clothing layers
- [ ] Textured or shaded stick figures
- [ ] 3D perspective stick figures

## Context

### Reference Analysis from Web Research

Based on web search findings about professional stick figure design:

**xkcd Style (Randall Munroe)**:
- Very minimalist: single line per limb segment
- Head: simple circle
- Body: single vertical line from head to hips
- Arms: two line segments (shoulder-elbow, elbow-hand)
- Legs: two line segments (hip-knee, knee-foot)
- Expressions: mostly conveyed through body language and head tilt, not facial features
- Proportions: head is relatively small compared to body (~1/8 height)

**Classic Stick Figure (Drawing Tutorials)**:
- Head: circle, typically 1/7 to 1/8 of total height for adults
- Torso: straight line, about 2-3 head heights
- Arms: about 3 head heights total length
- Legs: about 4 head heights total length
- Joints: elbows at waist level, knees at leg midpoint

**Anatomy-Based Proportions**:
- Adult: 7.5-8 head heights total
- Teenage: 6 head heights
- Child: 4 head heights
- Key anatomical markers:
  - Elbow aligns with waist
  - Hands reach mid-thigh
  - Knees are halfway down legs

### Current Implementation Issues

Based on current Stickman code (comix/cobject/character/character.py:310-363):

```python
head_radius = h * 0.15  # 15% = head diameter is 30% of height → ~3.3 head heights (TOO BIG)
body_length = h * 0.35  # 35% for torso
limb_length = h * 0.25  # 25% for each limb
```

**Problems**:
1. **Head too large**: 30% diameter = ~3 head heights (should be ~7.5 heads)
2. **Body too short**: 35% torso seems reasonable but...
3. **Limbs too short**: 25% per arm/leg is short for proper proportions
4. **Total doesn't add up**: head(30%) + body(35%) + legs(25%) = 90%, leaves gaps

**Correct proportions** (7.5 heads standard):
- Head diameter: ~13.3% of height (100/7.5)
- Torso (neck to hip): ~40% of height (3 heads)
- Legs: ~53.3% of height (4 heads)
- Arms: reach to mid-thigh (~40-45% down from shoulders)

### Desired Visual Appearance

**Target reference**: xkcd character

```
     O          ← Head (circle, ~13% of total height)
     |          ← Neck/torso start
    /|\         ← Arms (reach to here when down: ↓)
     |          ← Torso continues
     |          ←                               ↓ (mid-thigh)
    / \         ← Legs (hips to feet, ~53% of height)
```

**Proportions breakdown** (height = 100):
- Head: radius = 6.7 (diameter = 13.4%, giving ~7.5 heads)
- Neck: 2
- Torso: 30
- Hip to foot: 53
- Arms: ~38 (reach to ~40% down body when hanging)

### Edge Cases

- **Very small height (< 50px)**: May not render recognizable head circle (pixels too few)
- **Very large height (> 500px)**: Line width should scale or appear too thin
- **Head too small (< 5px radius)**: Not visible, should warn user
- **Limb angles extreme (> 180°)**: May create unnatural appearance
- **Zero or negative height**: Raise ValueError
- **Facing direction "front" or "back"**: May need different limb representation

### Technical Constraints

- Must maintain compatibility with existing Pose and Expression systems
- Head is first 16 points (circle polygon)
- Body is remaining points as line pairs
- Renderers expect this point structure
- Cannot break existing tests without good reason

### Related Specs

- `character-basics.md` (character system overview)
- `speech-bubbles.md` (character.say() interaction)
- `getting-started.md` (basic usage examples)

## Examples

### Example 1: Default Stickman with Correct Proportions

```python
from comix import Stickman

# Create stickman with reference-based proportions
char = Stickman(height=150)  # Uses "classic" reference by default
char.move_to((400, 300))

# Result: Stickman with proper 7.5 head proportions
# - Head: 20px diameter (13.3% of 150)
# - Torso: 60px (40%)
# - Legs: 80px (53%)
# - Arms: reach to mid-thigh when down
```

**Expected Visual**:
```
Height = 150px

    O     ← 20px circle head (13.3%)
    |
   /|\    ← Arms extend here
    |     ← Torso 60px (40%)
    |
   / \    ← Legs 80px (53%)
```

### Example 2: xkcd Style Reference

```python
from comix import Stickman

# Use xkcd proportions specifically
char = Stickman(
    height=150,
    proportion_style="xkcd"  # Minimalist, small head
)

# Result: Very clean, minimalist stick figure
# - Slightly smaller head than "classic"
# - Very simple, straight lines
# - Minimal joint indicators
```

### Example 3: Comparing Current vs Reference-Based

```python
from comix import Page, Panel, Stickman

page = Page(width=800, height=400)
page.set_layout(rows=1, cols=2)

# Current implementation (before fix)
panel1 = Panel()
old_char = Stickman(height=150)  # Will look "weird" with big head
old_char.move_to((200, 250))
bubble1 = old_char.say("Old proportions")
panel1.add_content(old_char, bubble1)

# New reference-based implementation
panel2 = Panel()
new_char = Stickman(height=150, proportion_style="classic")
new_char.move_to((600, 250))
bubble2 = new_char.say("New proportions!")
panel2.add_content(new_char, bubble2)

page.add(panel1, panel2)
page.render("comparison.png")

# Result: Side-by-side showing improvement
```

### Example 4: Custom Proportions for Stylization

```python
from comix import Stickman

# Create custom proportion set
char = Stickman(
    height=150,
    head_ratio=0.20,  # Larger head (chibi-like stick figure)
    torso_ratio=0.30,
    leg_ratio=0.50
)

# Result: Stylized stick figure with custom ratios
# Useful for special effects or different age groups
```

### Example 5: Tall Adult vs Short Child

```python
from comix import Stickman

# Adult (7.5 heads standard)
adult = Stickman(height=150, proportion_style="classic")

# Child (4 heads standard)
child = Stickman(
    height=100,
    proportion_style="child"  # Larger head ratio, shorter limbs
)

# Result: Visually distinct age representation
```

## Implementation Notes

### Corrected Stickman Proportions

```python
class Stickman(Character):
    # Reference-based proportion presets
    PROPORTION_PRESETS = {
        "classic": {
            "head_ratio": 0.133,  # ~7.5 heads (100/7.5)
            "torso_ratio": 0.40,  # ~3 heads
            "arm_ratio": 0.38,    # Arms reach mid-thigh
            "leg_ratio": 0.53,    # ~4 heads
        },
        "xkcd": {
            "head_ratio": 0.12,   # Slightly smaller head
            "torso_ratio": 0.42,
            "arm_ratio": 0.40,
            "leg_ratio": 0.54,
        },
        "tall": {
            "head_ratio": 0.125,  # 8 heads
            "torso_ratio": 0.42,
            "arm_ratio": 0.40,
            "leg_ratio": 0.55,
        },
        "child": {
            "head_ratio": 0.25,   # 4 heads (larger head)
            "torso_ratio": 0.30,
            "arm_ratio": 0.28,
            "leg_ratio": 0.45,
        },
    }

    def __init__(
        self,
        name: str = "Stickman",
        proportion_style: str = "classic",  # "classic", "xkcd", "tall", "child"
        head_ratio: float | None = None,    # Override with custom ratio
        torso_ratio: float | None = None,
        arm_ratio: float | None = None,
        leg_ratio: float | None = None,
        **kwargs
    ):
        # Get preset proportions
        preset = self.PROPORTION_PRESETS.get(
            proportion_style,
            self.PROPORTION_PRESETS["classic"]
        )

        # Use custom ratios if provided, otherwise use preset
        self.head_ratio = head_ratio or preset["head_ratio"]
        self.torso_ratio = torso_ratio or preset["torso_ratio"]
        self.arm_ratio = arm_ratio or preset["arm_ratio"]
        self.leg_ratio = leg_ratio or preset["leg_ratio"]

        super().__init__(name=name, **kwargs)

    def generate_points(self) -> None:
        """Generate stickman figure points with correct proportions."""
        h = self.character_height

        # Calculate component sizes from ratios
        head_radius = h * self.head_ratio
        torso_length = h * self.torso_ratio
        arm_length = h * self.arm_ratio
        leg_length = h * self.leg_ratio

        points = []

        # Calculate vertical positions (top to bottom)
        head_top = h / 2
        head_center_y = head_top - head_radius
        head_bottom = head_top - 2 * head_radius  # Neck start
        torso_bottom = head_bottom - torso_length  # Hip level
        foot_level = torso_bottom - leg_length

        # Head circle (16 points)
        for angle in np.linspace(0, 2 * np.pi, 16):
            points.append([
                head_radius * np.cos(angle),
                head_center_y + head_radius * np.sin(angle)
            ])

        # Torso line (neck to hips)
        points.append([0, head_bottom])  # Neck
        points.append([0, torso_bottom])  # Hips

        # Arms (shoulders to elbows to hands)
        arm_attachment_y = head_bottom - torso_length * 0.1  # Just below neck
        left_arm_angle = np.radians(self._pose.left_arm)
        right_arm_angle = np.radians(self._pose.right_arm)

        # Left arm (shoulder → elbow → hand)
        elbow_left_x = -arm_length * 0.5 * np.cos(left_arm_angle)
        elbow_left_y = arm_attachment_y - arm_length * 0.5 * np.sin(left_arm_angle)
        hand_left_x = -arm_length * np.cos(left_arm_angle)
        hand_left_y = arm_attachment_y - arm_length * np.sin(left_arm_angle)

        points.append([0, arm_attachment_y])  # Shoulder (center)
        points.append([elbow_left_x, elbow_left_y])  # Elbow
        points.append([elbow_left_x, elbow_left_y])  # Elbow (repeat for line segment)
        points.append([hand_left_x, hand_left_y])  # Hand

        # Right arm
        elbow_right_x = arm_length * 0.5 * np.cos(right_arm_angle)
        elbow_right_y = arm_attachment_y - arm_length * 0.5 * np.sin(right_arm_angle)
        hand_right_x = arm_length * np.cos(right_arm_angle)
        hand_right_y = arm_attachment_y - arm_length * np.sin(right_arm_angle)

        points.append([0, arm_attachment_y])  # Shoulder (center)
        points.append([elbow_right_x, elbow_right_y])  # Elbow
        points.append([elbow_right_x, elbow_right_y])  # Elbow (repeat)
        points.append([hand_right_x, hand_right_y])  # Hand

        # Legs (hips → knees → feet)
        left_leg_angle = np.radians(90 + self._pose.left_leg)
        right_leg_angle = np.radians(90 + self._pose.right_leg)

        # Left leg
        knee_left_x = -leg_length * 0.5 * np.cos(left_leg_angle)
        knee_left_y = torso_bottom - leg_length * 0.5 * np.sin(left_leg_angle)
        foot_left_x = -leg_length * np.cos(left_leg_angle)
        foot_left_y = torso_bottom - leg_length * np.sin(left_leg_angle)

        points.append([0, torso_bottom])  # Hip
        points.append([knee_left_x, knee_left_y])  # Knee
        points.append([knee_left_x, knee_left_y])  # Knee (repeat)
        points.append([foot_left_x, foot_left_y])  # Foot

        # Right leg
        knee_right_x = leg_length * 0.5 * np.cos(right_leg_angle)
        knee_right_y = torso_bottom - leg_length * 0.5 * np.sin(right_leg_angle)
        foot_right_x = leg_length * np.cos(right_leg_angle)
        foot_right_y = torso_bottom - leg_length * np.sin(right_leg_angle)

        points.append([0, torso_bottom])  # Hip
        points.append([knee_right_x, knee_right_y])  # Knee
        points.append([knee_right_x, knee_right_y])  # Knee (repeat)
        points.append([foot_right_x, foot_right_y])  # Foot

        self._points = np.array(points, dtype=np.float64)

        if self.facing == "left":
            self._points[:, 0] *= -1
```

### Validation Tests

```python
def test_stickman_proportions():
    """Verify stickman matches reference proportions."""
    char = Stickman(height=150, proportion_style="classic")
    char.generate_points()

    # Extract head points
    head_points = char._points[:16]
    head_center_x = np.mean(head_points[:, 0])
    head_center_y = np.mean(head_points[:, 1])
    head_radius = np.mean(
        np.linalg.norm(head_points - [head_center_x, head_center_y], axis=1)
    )

    # Verify head size
    expected_head_radius = 150 * 0.133
    assert abs(head_radius - expected_head_radius) < 1.0, \
        f"Head radius {head_radius} != expected {expected_head_radius}"

    # Verify total proportions (~7.5 heads)
    head_count = 150 / (head_radius * 2)
    assert 7.0 < head_count < 8.0, \
        f"Proportion is {head_count} heads, should be ~7.5"
```

## Open Questions

- [x] Should "classic" be default or "xkcd"? **Decision**: "classic" (more universally recognized)
- [x] Should we support custom head_ratio? **Decision**: Yes, for flexibility
- [ ] Should line width scale with height? **Decision needed** (probably yes for very small/large)
- [ ] Should we add "realistic" style (8 heads)? **Decision needed** (useful for some comics)
- [ ] Do we need "front" view with arms/legs spread? **Decision needed** (defer to future)

## Test Requirements

1. **Proportion accuracy**:
   - Test: Default stickman has ~7.5 head height ratio
   - Test: Head diameter is 13.3% of total height
   - Test: Torso length is ~40% of height
   - Test: Legs are ~53% of height

2. **Visual comparison**:
   - Test: Generated stickman matches xkcd reference visually
   - Test: Adult vs child proportions look distinct
   - Test: Standing pose looks natural and balanced

3. **Preset styles**:
   - Test: proportion_style="xkcd" uses xkcd proportions
   - Test: proportion_style="child" has larger head
   - Test: Invalid style falls back to "classic"

4. **Custom ratios**:
   - Test: Custom head_ratio overrides preset
   - Test: Sum of ratios doesn't need to be 1.0 (each is independent)

5. **Backward compatibility**:
   - Test: Existing Stickman() still works (uses classic preset)
   - Test: Poses and expressions still work with new proportions

## Success Metrics

**This spec is successful when:**
1. Stickman with default settings looks like a recognizable stick figure comic character
2. Proportions match xkcd/webcomic standards (~7.5 heads for adults)
3. User feedback confirms "looks right" and "matches what I expected"
4. Standing stickman looks balanced and natural
5. Arms reach mid-thigh when hanging down (anatomically correct)
6. Head is not "too big" or "too small" compared to body
7. No more complaints that stickman "looks weird"

## References and Sources

Research findings about professional stick figure design:

- [xkcd - Wikipedia](https://en.wikipedia.org/wiki/Xkcd) - Details about xkcd's stick figure style
- [Stick figure - explain xkcd](https://www.explainxkcd.com/wiki/index.php/Stick_figure) - Analysis of xkcd character structure
- [How to Draw a Stick Figure: a Complex Guide](https://design.tutsplus.com/tutorials/how-to-draw-a-stick-figure-a-complex-guide--cms-23620) - Professional stick figure drawing techniques
- [Figure Drawing proportion and construction](https://www.slideshare.net/slideshow/figure-drawing-proportion-and-construction/30345738) - Anatomical proportions for figure drawing
- [Drawing Human Proportions Using Stick Figures](https://mydrawingtutorials.com/drawing-human-proportions-with-stick-figures/) - Using stick figures for proper body proportions (8 head count method)
- [Learn How to Draw Human Figures in Correct Proportions](https://www.drawinghowtodraw.com/stepbystepdrawinglessons/2016/04/learn-draw-human-figures-correct-proportions-memorizing-stick-figures/) - Stick figure proportions: 7.5-8 heads for adults

**Key Takeaway**: Professional stick figures use ~7-8 head heights, not the 3-4 heads our current implementation creates. This is the core issue making stickman "look weird."
