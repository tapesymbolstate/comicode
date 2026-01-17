# Visual Effects - Manga-Style Effect System

## What

A comprehensive visual effects system that adds manga-style dramatic effects to comic panels, including shake effects, zoom lines, motion lines, focus lines, appear effects, and impact effects.

## Why

Comics rely heavily on visual effects to convey emotion, motion, and dramatic moments. Without effects, scenes feel static and lack the dynamic energy that makes manga and comics engaging. The effect system enables:

1. **Emotional emphasis**: Shake effects for surprise or fear
2. **Movement indication**: Motion lines show speed and direction
3. **Focus attention**: Focus lines draw readers' eyes to important elements
4. **Dramatic reveals**: Appear effects for character entrances
5. **Impact moments**: Explosion-like effects for action scenes

## Acceptance Criteria

### Must Have
- [x] Base `Effect` class with common properties (position, intensity, color, opacity)
- [x] 6 effect types: ShakeEffect, ZoomEffect, MotionLines, FocusLines, AppearEffect, ImpactEffect
- [x] Target-based positioning (attach effect to a CObject)
- [x] Position-based placement (explicit x, y coordinates)
- [x] Intensity control (0.0 to 1.0) affecting element count
- [x] Z-index layering for rendering order
- [x] Method chaining API for configuration
- [x] SVG renderer support
- [x] Cairo renderer support (PNG/PDF)

### Should Have
- [x] Seed parameter for reproducible random effects
- [x] Lazy element generation with caching
- [x] Effect-specific configuration methods
- [x] Multiple styles for AppearEffect (sparkle, fade, flash, reveal)
- [x] Customizable colors and opacities per effect

### Won't Have (This Iteration)
- [ ] Animated effects (defer to future animation system)
- [ ] Custom effect element shapes (uses built-in types only)
- [ ] Real-time effect preview during editing

## Context

### User Flow

1. Create an effect instance with target or position
2. Configure effect-specific parameters via setters
3. Add effect to page using `page.add_effect(effect)`
4. Render page - effects are drawn based on z_index
5. Effects behind objects (z_index=-1) or in front (z_index=1)

### Effect Types Summary

| Effect | Purpose | Default Z-Index | Key Parameters |
|--------|---------|-----------------|----------------|
| ShakeEffect | Tremor/vibration with ghost copies | -1 | shake_distance, num_copies, direction |
| ZoomEffect | Radial speed lines | -1 | num_lines, inner_radius, outer_radius |
| MotionLines | Parallel speed lines | -1 | direction, num_lines, line_length, spread |
| FocusLines | Converging dramatic lines | -1 | num_lines, inner_gap, outer_radius |
| AppearEffect | Reveal/materialization | -1 | style, num_elements, radius |
| ImpactEffect | Explosion burst | 1 | num_spikes, inner_radius, outer_radius |

### Technical Constraints

- Intensity and opacity auto-clamp to [0.0, 1.0]
- Effects without targets default to position (0, 0)
- All setters mark effect as needing regeneration
- Random generation uses seed for reproducibility when set

## Examples

### Example 1: Shake Effect on Character

```python
from comix import Page, Stickman
from comix.effect import ShakeEffect

page = Page(width=400, height=400)
char = Stickman(name="Frightened").move_to((200, 200))
page.add(char)

effect = ShakeEffect(target=char) \
    .set_intensity(0.8) \
    .set_shake_distance(10.0) \
    .set_num_copies(4)
page.add_effect(effect)
```

**Expected Visual**: Character with ghost copies showing trembling motion.

### Example 2: Focus Lines for Dramatic Moment

```python
from comix import Page
from comix.effect import FocusLines

page = Page(width=800, height=600)

effect = FocusLines(position=(400, 300)) \
    .set_num_lines(48) \
    .set_inner_gap(100.0) \
    .set_outer_radius(400.0) \
    .set_fill_background(True)
page.add_effect(effect)
```

**Expected Visual**: Radial lines converging toward center with filled triangles.

### Example 3: Motion Lines for Movement

```python
from comix import Page, Stickman
from comix.effect import MotionLines
import math

page = Page(width=600, height=400)
char = Stickman(name="Runner").move_to((400, 200))
page.add(char)

effect = MotionLines(target=char) \
    .set_direction(math.pi)  # Moving left
    .set_num_lines(16) \
    .set_line_length(120.0)
page.add_effect(effect)
```

**Expected Visual**: Parallel lines trailing behind character indicating leftward motion.

### Example 4: Appear Effect Styles

```python
from comix.effect import AppearEffect

# Sparkle style (default)
sparkle = AppearEffect(position=(100, 100), style="sparkle")

# Fade style - concentric rings
fade = AppearEffect(position=(200, 100), style="fade")

# Flash style - radial rays
flash = AppearEffect(position=(300, 100), style="flash")

# Reveal style - horizontal lines
reveal = AppearEffect(position=(400, 100), style="reveal")
```

### Example 5: Impact Effect

```python
from comix.effect import ImpactEffect

effect = ImpactEffect(position=(300, 200)) \
    .set_num_spikes(16) \
    .set_radii(inner=30.0, outer=80.0) \
    .set_color("#FF0000") \
    .set_fill_center(True)
```

**Expected Visual**: Star-burst explosion pattern with filled white center.

## Open Questions

- [x] Should effects support animation? **Decision**: Defer to future animation system
- [x] Should effects be applied to panels or pages? **Decision**: Pages, with position relative to page coordinates
- [x] How handle multiple effects on same target? **Decision**: Each effect renders independently, layered by z_index

## Test Requirements

1. **Effect Creation**:
   - Test: Default values for all effect types
   - Test: Custom parameter initialization
   - Test: Target-based positioning uses target center
   - Test: Position-based placement without target

2. **Element Generation**:
   - Test: Element count scales with intensity
   - Test: Regeneration on parameter changes
   - Test: Caching prevents redundant generation
   - Test: Seed produces reproducible results

3. **Rendering**:
   - Test: SVG output contains expected elements
   - Test: Cairo rendering produces visible output
   - Test: Z-index ordering correct
   - Test: Opacity applied correctly

4. **Method Chaining**:
   - Test: All setters return self
   - Test: Chained configuration produces expected state

## Implementation Status

Fully implemented in `/comix/effect/effect.py` with 101 tests in `/tests/test_effect.py`.
