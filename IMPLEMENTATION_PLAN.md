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

## Next: Phase 3 - Layout Engine

- [ ] FlowLayout for automatic positioning
- [ ] Auto bubble positioning relative to characters
- [ ] Constraint-based layouts

## Future: Phase 4 - Extensions

- [ ] AI image integration (OpenAI/Replicate)
- [ ] Markup parser for DSL-based comic creation
- [ ] Web preview with hot reload
- [ ] Effect system for webtoons (shake, zoom, motion lines)
- [ ] Cairo renderer for PNG/PDF output

## Technical Notes

- Using Manim-inspired architecture with method chaining
- NumPy for coordinate calculations
- SVG as primary output format
- fonttools for font metrics
- All tests passing (180/180)
- Python 3.13 required

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
