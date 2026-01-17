# Animation Export

## What

Export comic pages with timeline-based animations to animated GIF files, with support for multiple animation types, 27 easing functions, and precise timing control.

## Why

Static comics are great for print, but animated sequences can bring panels to life for web and social media. Animation export enables:

1. **Dynamic storytelling**: Effects like shake, zoom, and fade add dramatic impact
2. **Social sharing**: GIFs are universally supported on social platforms
3. **Character motion**: Characters can move, scale, rotate, and fade smoothly
4. **Effect sequences**: Visual effects can pulse, grow, and burst in sequence
5. **Precise control**: Timeline-based composition allows complex choreography

## Acceptance Criteria

### Must Have
- [x] Timeline class for orchestrating multiple animations with precise timing
- [x] Animation base class with duration, delay, and easing support
- [x] PropertyAnimation for animating any numeric attribute
- [x] EffectAnimation with 7 pre-built patterns (pulse, fade_in, fade_out, grow, shrink, shake_intensify, zoom_burst)
- [x] ObjectAnimation for CObject properties (position, scale, rotation, opacity)
- [x] AnimationGroup for parallel and sequential composition
- [x] 27 easing functions (linear, quad, cubic, quart, sine, expo, elastic, back, bounce - with in/out/inOut variants)
- [x] GIFRenderer class for animated GIF output
- [x] Configurable FPS (1-60), duration, and quality settings
- [x] Loop control (infinite or specific count)

### Should Have
- [x] Progress callback for rendering status
- [x] Frame extraction to individual image files
- [x] PNG and GIF output formats for frames
- [x] Optimize option for smaller file sizes
- [x] Method chaining for fluent API
- [x] Custom easing function registration
- [x] AnimationConfig dataclass for export settings

### Won't Have (This Iteration)
- [ ] Real-time preview during animation editing
- [ ] Keyframe editor UI
- [ ] Audio synchronization (handled by VideoRenderer)
- [ ] 3D transforms
- [ ] Path-based motion (follow curves)

## Context

### User Flow

1. Create Page with content (characters, effects, panels)
2. Create Timeline and add animations at specific times
3. Call `GIFRenderer(page).render("output.gif", timeline)` or use `page.animate()`
4. Share the resulting animated GIF

### Animation System Architecture

The animation system follows a hierarchical design:

```
Animation (base class)
├── PropertyAnimation      # Generic numeric property animation
├── EffectAnimation        # Effect-specific patterns (pulse, fade, grow, etc.)
├── ObjectAnimation        # CObject transforms (position, scale, rotation, opacity)
└── AnimationGroup         # Parallel or sequential composition
```

Timeline orchestrates animations:
```
Timeline
├── at(time).add(animation)     # Add at specific time
├── then(animation, gap)        # Add after previous
├── with_previous(animation)    # Add in parallel with previous
└── apply_at_time(t)            # Apply all animations at time t
```

### Easing Functions

All 27 easing functions follow the standard pattern:

| Category | In | Out | InOut |
|----------|-----|-----|-------|
| Linear | linear | - | - |
| Quadratic | ease_in_quad | ease_out_quad | ease_in_out_quad |
| Cubic | ease_in_cubic | ease_out_cubic | ease_in_out_cubic |
| Quartic | ease_in_quart | ease_out_quart | ease_in_out_quart |
| Sinusoidal | ease_in_sine | ease_out_sine | ease_in_out_sine |
| Exponential | ease_in_expo | ease_out_expo | ease_in_out_expo |
| Elastic | ease_in_elastic | ease_out_elastic | ease_in_out_elastic |
| Back | ease_in_back | ease_out_back | ease_in_out_back |
| Bounce | ease_in_bounce | ease_out_bounce | ease_in_out_bounce |

Aliases: `ease_in` = ease_in_quad, `ease_out` = ease_out_quad, `ease_in_out` = ease_in_out_quad

### Effect Animation Patterns

| Pattern | Properties Animated | Description |
|---------|---------------------|-------------|
| pulse | intensity | Pulsating intensity effect |
| fade_in | opacity | Fade from transparent to opaque |
| fade_out | opacity | Fade from opaque to transparent |
| grow | intensity | Grow from nothing to full |
| shrink | intensity | Shrink from full to nothing |
| shake_intensify | intensity, shake_distance | Increasing shake effect |
| zoom_burst | intensity, inner_radius, outer_radius | Expanding zoom with fade |

### GIF Quality Settings

| Quality | DPI | Use Case |
|---------|-----|----------|
| low | 72 | Quick preview, smallest file |
| medium | 96 | Balanced (default) |
| high | 150 | Best quality, larger file |

### Timing Model

- **Duration**: Animation length in seconds
- **Delay**: Wait before animation starts
- **Total Duration**: delay + duration
- **Progress**: 0.0 (start) to 1.0 (end), with easing applied
- **FPS**: 1-60 frames per second (clamped automatically)

## Examples

### Example 1: Simple Fade-In Animation

```python
from comix import Page, Panel, Stickman
from comix.effect.effect import AppearEffect
from comix.animation import Timeline, EffectAnimation, GIFRenderer

page = Page(width=400, height=300)
panel = Panel(width=360, height=260)
char = Stickman(name="Hero", height=80)
char.move_to((180, 150))

effect = AppearEffect(target=char, style="fade")
panel.add_content(char, effect)
page.add(panel)

timeline = Timeline(page)
timeline.add(EffectAnimation(effect, pattern="fade_in", duration=1.0))

renderer = GIFRenderer(page)
renderer.render("fade_in.gif", timeline, fps=24, duration=1.0)
```

### Example 2: Character Movement with Easing

```python
from comix import Page, Panel, Stickman
from comix.animation import Timeline, ObjectAnimation, GIFRenderer

page = Page(width=600, height=400)
panel = Panel(width=560, height=360)
char = Stickman(name="Runner", height=80)
char.move_to((100, 200))
panel.add_content(char)
page.add(panel)

timeline = Timeline(page)
timeline.add(
    ObjectAnimation(char, duration=1.5)
    .to_position(500, 200)
    .set_easing("ease_in_out_back")
)

renderer = GIFRenderer(page)
renderer.render("movement.gif", timeline, fps=30, duration=1.5)
```

### Example 3: Sequential Animation Chain

```python
from comix import Page, Panel, Stickman
from comix.effect.effect import ShakeEffect, ZoomEffect
from comix.animation import Timeline, EffectAnimation, ObjectAnimation

page = Page(width=500, height=400)
panel = Panel(width=460, height=360)
char = Stickman(name="Star", height=80)
char.move_to((250, 200))

shake = ShakeEffect(target=char, intensity=0.8)
zoom = ZoomEffect(target=char, intensity=0.6)
panel.add_content(char, shake, zoom)
page.add(panel)

timeline = Timeline(page)
# Sequential: shake first, then zoom burst
timeline.add(EffectAnimation(shake, pattern="shake_intensify", duration=0.5))
timeline.then(EffectAnimation(zoom, pattern="zoom_burst", duration=0.8), gap=0.1)

page.animate("sequence.gif", timeline, fps=24, duration=1.4)
```

### Example 4: Parallel Animations with AnimationGroup

```python
from comix import Page, Panel, Stickman
from comix.animation import Timeline, ObjectAnimation, AnimationGroup

page = Page(width=600, height=400)
panel = Panel(width=560, height=360)

char1 = Stickman(name="Left", height=60)
char1.move_to((150, 200))
char2 = Stickman(name="Right", height=60)
char2.move_to((450, 200))

panel.add_content(char1, char2)
page.add(panel)

timeline = Timeline(page)
# Both characters move toward center simultaneously
timeline.add(AnimationGroup(
    ObjectAnimation(char1, duration=1.0).to_position(250, 200),
    ObjectAnimation(char2, duration=1.0).to_position(350, 200),
    mode="parallel"
))

page.animate("parallel.gif", timeline, fps=30, duration=1.0)
```

### Example 5: Extract Frames for Post-Processing

```python
from comix import Page, Panel, Stickman
from comix.animation import Timeline, ObjectAnimation, GIFRenderer

page = Page(width=400, height=300)
panel = Panel(width=360, height=260)
char = Stickman(name="Spinner", height=80)
char.move_to((180, 150))
panel.add_content(char)
page.add(panel)

timeline = Timeline(page)
timeline.add(ObjectAnimation(char, duration=1.0).to_rotation(6.28))  # Full rotation

renderer = GIFRenderer(page)
frame_paths = renderer.render_frames(
    "frames/",
    timeline,
    fps=12,
    duration=1.0,
    format="png",
    progress_callback=lambda curr, total: print(f"Frame {curr}/{total}")
)
print(f"Rendered {len(frame_paths)} frames")
```

### Example 6: Custom Easing Function

```python
from comix.animation.easing import register_easing
import math

# Register a custom "wobble" easing
def wobble(t: float) -> float:
    return t + 0.3 * math.sin(t * math.pi * 4) * (1 - t)

register_easing("wobble", wobble)

# Use in animation
animation = ObjectAnimation(char, duration=1.0).set_easing("wobble")
```

## Related Specs

- [Effect System](effect-system.md) - Visual effects that can be animated
- [Video Export](video-export.md) - Video output with audio support
- [HTML Export](html-export.md) - Interactive web export (non-animated)

## Test Requirements

1. **Animation Base Class**:
   - Test: Duration and delay configuration
   - Test: Easing function lookup and application
   - Test: Progress calculation with delay
   - Test: is_started and is_complete state checks

2. **PropertyAnimation**:
   - Test: Interpolates between start and end values
   - Test: Applies value to target property
   - Test: Reset restores initial value

3. **EffectAnimation**:
   - Test: All 7 patterns apply correctly
   - Test: Reverse option inverts animation
   - Test: Pattern validation

4. **ObjectAnimation**:
   - Test: Position animation with to_position()
   - Test: Scale animation with to_scale()
   - Test: Rotation animation with to_rotation()
   - Test: Opacity animation with to_opacity()
   - Test: Multiple properties animated simultaneously

5. **AnimationGroup**:
   - Test: Parallel mode plays all animations at once
   - Test: Sequential mode plays animations in order
   - Test: Duration calculation for both modes

6. **Timeline**:
   - Test: at() adds animation at specific time
   - Test: then() chains after previous
   - Test: with_previous() adds in parallel
   - Test: apply_at_time() activates correct animations
   - Test: Duration property returns max end time

7. **Easing Functions**:
   - Test: All 27 built-in easings return valid values
   - Test: Custom easing registration works
   - Test: Invalid easing name raises ValueError

8. **GIFRenderer**:
   - Test: Renders animated GIF file
   - Test: FPS clamping (1-60)
   - Test: Duration clamping (min 0.1)
   - Test: Quality settings affect DPI
   - Test: Loop and loop_count options
   - Test: Progress callback called correctly
   - Test: Frame extraction creates files

## Implementation Status

Fully implemented in:
- `/comix/animation/animation.py` - Animation classes
- `/comix/animation/timeline.py` - Timeline orchestration
- `/comix/animation/easing.py` - Easing functions
- `/comix/renderer/gif_renderer.py` - GIF export

Tests in:
- `/tests/test_animation.py`
- `/tests/test_gif_renderer.py`

Working example: `/examples/14_animation_export.py`
