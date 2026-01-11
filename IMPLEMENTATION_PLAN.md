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

## Next: Phase 4 - Extensions

- [ ] AI image integration (OpenAI/Replicate)
- [ ] Markup parser for DSL-based comic creation
- [ ] Web preview with hot reload
- [ ] Effect system for webtoons (shake, zoom, motion lines)
- [ ] Cairo renderer for PNG/PDF output
- [ ] Constraint-based layouts (advanced)

## Technical Notes

- Using Manim-inspired architecture with method chaining
- NumPy for coordinate calculations
- SVG as primary output format
- fonttools for font metrics
- All tests passing (220/220)
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
