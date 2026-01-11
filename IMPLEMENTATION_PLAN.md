# Implementation Plan

## Completed: Phase 1 - Core (MVP)

All Phase 1 items have been implemented and tested (92 tests passing):

- [x] CObject base class with transformation methods (move_to, shift, scale, rotate, hierarchy)
- [x] Panel class with borders and backgrounds
- [x] Bubble base class with speech variants (SpeechBubble, ThoughtBubble, ShoutBubble, WhisperBubble, NarratorBubble)
- [x] Text and StyledText classes including SFX for sound effects
- [x] Character base class with Stickman and SimpleFace implementations
- [x] Expression and Pose systems for character states
- [x] Page class (Scene equivalent) with layout support
- [x] SinglePanel and Strip convenience classes
- [x] GridLayout for panel arrangement
- [x] SVG Renderer with full element support
- [x] Basic CLI with render and preview commands
- [x] Utility modules (bezier curves, geometry transforms)
- [x] Style system with presets (manga, webtoon, comic, minimal)

## Completed: Phase 2 - Styling Enhancements

All Phase 2 items have been implemented and tested (180 tests passing):

- [x] Font management with fonttools
  - FontInfo, FontMetrics dataclasses
  - FontRegistry for font discovery and management
  - System font detection (macOS, Linux, Windows)
  - Font fallback chains
  - Text width/height estimation
- [x] Custom bubble shapes
  - Per-corner radius customization (corner_radii parameter)
  - Enhanced wobble with modes ("random", "wave")
  - Emphasis effect (shadow + thicker border)
- [x] Enhanced style inheritance
  - Style attached to CObject base class
  - get_effective_style() for cascade resolution
  - apply_style() method on Bubble and Text classes
  - Parent-to-child style inheritance
- [x] Theme system for consistent styling
  - ColorPalette for coordinated colors
  - Theme class with element-specific styles
  - ThemeRegistry for theme management
  - Built-in themes (manga, webtoon, comic, minimal)
  - Global theme functions (get_theme, set_default_theme, etc.)

## Completed: Phase 3 - Layout Engine

All Phase 3 items have been implemented and tested (220 tests passing):

- [x] FlowLayout for automatic positioning
  - Horizontal and vertical flow directions
  - Wrap and nowrap modes
  - Main axis alignment (start, center, end)
  - Cross axis alignment (start, center, end)
  - Respects individual object dimensions
  - Offset support for margin handling
- [x] Auto bubble positioning relative to characters
  - Enhanced attach_to() with 8 anchor positions (top, top-left, top-right, left, right, bottom, bottom-left, bottom-right)
  - Configurable buffer distance
  - Collision detection with overlaps_with() method
  - auto_attach_to() for intelligent position selection avoiding collisions
  - auto_position_bubbles() utility for positioning multiple bubbles
  - Boundary constraint support
  - Preferred anchor order customization
- [x] Page integration with set_flow_layout() method

## In Progress: Phase 4 - Extensions

Completed:
- [x] Cairo renderer for PNG/PDF output (250 tests passing)
  - Full CairoRenderer class with PNG and PDF support
  - Quality settings (low=72 DPI, medium=150 DPI, high=300 DPI)
  - Renders all element types: Panel, Bubble, Text, Character, Shapes
  - Page.render() integration with format="png" and format="pdf"
  - 30 comprehensive tests for Cairo rendering
- [x] Effect system for webtoons (305 tests passing)
  - Effect base class with position, intensity, color, opacity, z_index
  - ShakeEffect: visual tremor with ghost copies and motion blur lines
  - ZoomEffect: radial speed lines for emphasis
  - MotionLines: parallel speed lines for movement direction
  - FocusLines: manga-style dramatic focus lines with optional fill
  - ImpactEffect: burst patterns for collisions and impacts
  - Page.add_effect() and Page.remove_effect() methods
  - SVG and Cairo renderer integration
  - 55 comprehensive tests for Effect system

Remaining:
- [ ] AI image integration (OpenAI/Replicate)
- [ ] Markup parser for DSL-based comic creation
- [ ] Web preview with hot reload
- [ ] Constraint-based layouts (advanced)

## Technical Notes

- Using Manim-inspired architecture with method chaining
- NumPy for coordinate calculations
- SVG as primary output format, PNG/PDF via Cairo
- fonttools for font metrics
- pycairo for PNG/PDF rendering
- All tests passing (305/305)
- Python 3.13 required

## API Changes (Phase 3)

### FlowLayout class (new)
- `FlowLayout(width, height, direction, spacing, wrap, alignment, cross_alignment, offset_x, offset_y)`
- `calculate_positions(num_cells)` - GridLayout-compatible interface
- `calculate_positions_for_objects(objects)` - Respects object dimensions

### Page class
- Added `set_flow_layout(direction, spacing, wrap, alignment, cross_alignment)` method
- `auto_layout()` now works with both GridLayout and FlowLayout

### Bubble class
- Enhanced `attach_to(character, anchor, buffer)` with 8 anchor positions
- Added `overlaps_with(other, margin)` for collision detection
- Added `auto_attach_to(character, avoid_bubbles, bounds, preferred_anchors, buffer)` for intelligent positioning

### New functions
- `auto_position_bubbles(character_bubble_pairs, bounds, buffer)` - Position multiple bubbles avoiding collisions

### Exports
- `FlowLayout` and `GridLayout` now exported from main package
- `auto_position_bubbles` exported from main package

## API Changes (Phase 2)

### Bubble class
- Renamed `style` parameter to `bubble_type` to avoid conflict with Style object
- Added `corner_radii: tuple[float, float, float, float] | None` for per-corner radius
- Added `wobble_mode: str` ("random" or "wave")
- `emphasis: bool` now renders shadow + thicker border

### CObject base class
- Added `style: Style | None` parameter to constructor
- Added `set_style()`, `get_style()`, `get_effective_style()`, `apply_style()` methods
- Style included in `get_render_data()` when set

### New modules
- `comix/style/font.py` - Font management system
- `comix/style/theme.py` - Theme system
- `comix/layout/flow.py` - FlowLayout system

## API Changes (Phase 4)

### CairoRenderer class (new)
- `CairoRenderer(page: Page)` - Initialize with a Page
- `render(output_path, format, quality)` - Render to PNG or PDF
  - `format`: "png" or "pdf" (auto-detected from extension)
  - `quality`: "low" (72 DPI), "medium" (150 DPI), "high" (300 DPI)

### Page class
- `render(output_path, format, quality)` now supports "png" and "pdf" formats
- Quality parameter passed through to CairoRenderer

### Dependencies
- Optional `cairo` extras: `uv sync --extra cairo`
- Requires pycairo>=1.26.0, Pillow>=10.0.0

### New module
- `comix/renderer/cairo_renderer.py` - Cairo-based PNG/PDF rendering

### Effect system (new)

#### Effect base class
- `Effect(target, position, z_index, intensity, color, opacity, seed)` - Base class for effects
- `set_position(position)` - Set effect position
- `set_target(target)` - Set target CObject
- `set_intensity(intensity)` - Set effect intensity (0-1)
- `set_color(color)` - Set effect color
- `set_opacity(opacity)` - Set effect opacity
- `get_elements()` - Get generated EffectElements
- `get_render_data()` - Get render data for renderers

#### ShakeEffect
- `ShakeEffect(target, position, shake_distance, num_copies, direction)` - Visual tremor effect
- `direction`: "horizontal", "vertical", or "both"
- Generates ghost copies and motion blur lines

#### ZoomEffect
- `ZoomEffect(target, position, num_lines, inner_radius, outer_radius)` - Radial zoom/emphasis
- Generates radial speed lines converging on target

#### MotionLines
- `MotionLines(target, position, direction, num_lines, line_length, spread, taper)` - Speed lines
- `set_direction(radians)` or `set_direction_degrees(degrees)` - Set motion direction
- Generates parallel lines indicating movement

#### FocusLines
- `FocusLines(target, position, num_lines, inner_gap, outer_radius, fill_background)` - Dramatic focus
- `set_fill_background(fill, color)` - Enable alternating fill pattern
- Manga-style converging lines

#### ImpactEffect
- `ImpactEffect(target, position, num_spikes, inner_radius, outer_radius, fill_center)` - Impact burst
- Star burst pattern with debris lines

#### Page class additions
- `add_effect(*effects)` - Add effects to page
- `remove_effect(*effects)` - Remove effects from page
- `get_effects()` - Get all effects on page

#### Exports
- All effect classes exported from main `comix` package
- Also available from `comix.effect` module

### New module
- `comix/effect/effect.py` - Effect system implementation
