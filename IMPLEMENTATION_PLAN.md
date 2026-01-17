# Implementation Plan

## Status: All Phases Complete + Multi-page PDF Export

All 4 phases have been implemented with **1075 tests passing**, mypy clean, and ruff clean.

### Completed Phases Summary

| Phase | Description | Status |
|-------|-------------|--------|
| Phase 1 | Core MVP (CObject, Panel, Bubble, Text, Character, Page, SVGRenderer) | Complete |
| Phase 2 | Styling (Font management, Theme system, Style inheritance) | Complete |
| Phase 3 | Layout Engine (FlowLayout, Auto bubble positioning, Collision detection) | Complete |
| Phase 4 | Extensions (Cairo renderer, Effects, Parser, Images, Preview server, Constraints) | Complete |
| Phase 5 | Multi-page PDF Export (Book class, compile CLI command) | Complete |

### Key Achievements

- **CObject hierarchy**: Full transformation API (move_to, shift, scale, rotate) with convenience methods (center_in, to_corner, to_edge, hide/show, copy, scale_to_fit)
- **Bubble system**: 5 types (Speech, Thought, Shout, Whisper, Narrator) with auto-positioning
- **Character system**: Stickman, SimpleFace with Expression/Pose systems
- **Layout**: GridLayout, FlowLayout, ConstraintLayout with priority-based solving
- **Renderers**: SVG (always available), Cairo PNG/PDF (optional)
- **Effects**: AppearEffect, ShakeEffect, ZoomEffect, MotionLines, FocusLines, ImpactEffect (6 effect types)
- **Parser**: DSL markup for rapid comic creation
- **AI Images**: OpenAI DALL-E and Replicate integration
- **Preview Server**: Hot reload web preview with file watching
- **CJK Text Support**: Proper width estimation for Korean/Japanese/Chinese characters
- **Expanded Test Coverage**: Dedicated test suites for Text/StyledText/SFX, Rectangle/Circle/Line, and Parser (ParseError, expressions, facing directions)
- **CLI Help**: Improved help text with default values and DPI information
- **CLI Command Tests**: Comprehensive test coverage for all CLI commands (info, render, preview, serve, compile) using Click CliRunner (51 tests)
- **SVG Renderer Tests**: Added render_to_string() tests and comprehensive effect rendering tests (18 new tests)
- **Character.whisper()**: Added whisper() method to Character class for creating WhisperBubble (completes the bubble convenience methods: say, think, shout, whisper)
- **BackgroundDirective Rendering**: Parser now properly handles background directives - sets color, image path, or description for AI generation
- **PRD Documentation Sync**: Updated specs/PRD.md to match actual implementation (bubble_type parameter, consolidated module structure, removed non-existent imports, added NarratorBubble class definition)
- **Panel Background Image Rendering**: SVG and Cairo renderers now properly render `background_image` set on panels (via `panel.set_background(image="path.png")` or parser `[background: image.png]`). Supports rounded corner clipping for panels with border radius (6 new tests)
- **Panel Templates**: Pre-built comic page layouts (FourKoma, SplashPage, TwoByTwo, WebComic, ThreeRowLayout, MangaPage, ActionPage) with semantic panel access (53 new tests)
- **Multi-page PDF Export**: Book class for compiling multiple pages into a single PDF document. Supports different page sizes per page, quality settings, and metadata. CLI `compile` command for batch rendering (45 new tests)
- **CObject Convenience Methods**: Added center_in, to_corner, to_edge, hide/show, is_visible, copy, scale_to_fit_width, scale_to_fit_height, scale_to_fit for easier object positioning and manipulation (31 new tests)
- **Constants Module**: Added centralized constants module (`comix/constants.py`) with standardized values for colors, dimensions, typography, borders, effects, server settings, quality levels, anchors, and directions. Exported from main package and used in CLI for VERSION. Includes 35 new tests for constants validation.
- **AIImage Test Coverage**: Comprehensive test coverage for AI image generation (57% to 97% coverage). Tests cover OpenAI and Replicate provider flows, error handling, image downloading, and state management (20 new tests).
- **CairoRenderer Test Coverage**: Extended test coverage for Cairo renderer (72% to 86% coverage). Tests cover image rendering, effects rendering, multi-page PDF, text handling, and character rendering (23 new tests).
- **Test Warning Fixes**: Fixed RuntimeWarning in AIImage tests by properly handling unawaited coroutines in mock tests. Uses `AsyncMock` for async method mocking and properly closes coroutines in sync wrapper tests.
- **Font Module Test Coverage**: Comprehensive test coverage for font management system (70% to 90%+ coverage). Tests cover font metrics extraction (full tables, fallback paths, missing tables), platform-specific font discovery (macOS, Linux, Windows), font info loading (weight/style detection, edge cases), metrics caching, CJK extended Unicode ranges, font system initialization, and directory scanning (54 new tests).
- **Bezier and Geometry Utils Test Coverage**: Comprehensive test coverage for bezier/geometry utility functions. Tests cover all tail directions, edge cases (empty arrays, clamped radii, invalid inputs), bubble path styles (whisper, unknown), scaling/rotation with centers, and mathematical edge cases (27 new tests).
- **CObject Positioning Test Coverage**: Full test coverage for CObject next_to() and align_to() methods, including all directional positioning (up, down, left, right) and edge alignment (top, bottom, left, right, center). Tests cover bounding box calculations with submobjects and transformations (20 new tests).
- **FlowLayout Extended Test Coverage**: Comprehensive tests for FlowLayout edge cases including vertical end alignment, cross-alignment options (start, center, end), bounding box fallback, wrap modes in both directions, and equal cell calculations (11 new tests).
- **Package Import Test Coverage**: Tests verifying all package exports are correctly available, including optional dependencies (CairoRenderer, PreviewServer) and version attributes (20 new tests).
- **ConstraintLayout Test Coverage**: Extended test coverage for constraint-based layout system (86% to 95%+ coverage). Tests cover right-hand arithmetic operators (__radd__, __rmul__), all element edge references (left, bottom, center_y, height), ref(None) behavior, constrain() error handling, default dimension/position fallbacks, bottom+height positioning, and circular dependency resolution (28 new tests).
- **PreviewServer Test Coverage**: Extended test coverage for preview server (81% to 92%+ coverage). Tests cover /poll endpoint functionality, file change detection via polling, render error handling (build/layout errors), has_file_changed with deleted files, server double-start protection, port exhaustion handling, browser opening, spec loader errors, and comprehensive watchdog handler tests (debouncing, file filtering, callback=None) (13 new tests).
- **SVG Renderer Extended Test Coverage**: Comprehensive tests for SVG renderer covering panel/bubble border styles (dashed, dotted), bubble emphasis effects with shadow rendering, rectangle corner radius, line stroke styles, empty text handling, generic object rendering fallback, and image fit modes (32 new tests). Fixed svgwrite validation issue by using fill-opacity instead of 8-character hex colors.
- **Cairo Renderer Extended Test Coverage**: Additional edge case tests for Cairo renderer including generic object fallback rendering, unknown character styles, effect polygons without stroke, effect circle elements, bubble dashed borders, panel dotted borders, stickman with insufficient points, panel background images with rounded corners, and effects with zero opacity (12 new tests).
- **SimpleFace Expression Rendering**: Enhanced SimpleFace character rendering to support all expression types. Both SVG and Cairo renderers now render expressive facial features based on Expression class properties:
  - **Eyes**: normal (round), curved (^_^ happy), droopy (sad), narrow (angry lines), wide (surprised with pupils), uneven (confused)
  - **Mouth**: normal (straight line), smile (upward curve), frown (downward curve), open (surprised O), wavy (uncertain)
  - **Eyebrows**: normal (none), raised (surprised arcs), worried (angled up to center), furrowed (angry angled down)
  The 6 preset expressions (neutral, happy, sad, angry, surprised, confused) now render visually distinct faces. Added 20 new tests for SVG and Cairo expression rendering.
- **CLI Error Handling Test Coverage**: Extended test coverage for CLI error handling paths including spec/loader failures, ImportError scenarios (missing watchdog/Cairo dependencies), script execution errors, book render exceptions, and Page class instantiation in preview command (8 new tests).
- **Parser Edge Case Test Coverage**: Comprehensive tests for parser edge cases including unrecognized hash comments (treated as comments), elements appearing without panel markers (background, narrator, SFX, character), character reuse with expression updates, and invalid syntax handling (9 new tests).

### Technical Stack

- Python 3.13, managed with `uv`
- NumPy for coordinate calculations
- fonttools for font metrics
- pycairo (optional) for PNG/PDF output
- watchdog (optional) for file watching

## Future Enhancements (Ideas)

These are potential improvements, not planned work:

1. **Animation Export**: Animated GIF/video for webtoon scroll effects
2. **Character Library**: Expanded character styles beyond Stickman/SimpleFace
3. **Web Renderer**: HTML output with interactive features

## Known Issues

None currently tracked.
