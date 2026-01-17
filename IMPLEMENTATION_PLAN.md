# Implementation Plan

## Status: All Phases Complete + Extended Character Library

All 4 phases have been implemented with **1229 tests passing**, mypy clean, and ruff clean.

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
- **Character system**: Stickman, SimpleFace, ChubbyStickman, Robot, Chibi, Anime with full Expression/Pose support
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
- **Extended Expression System**: Added 5 new preset expressions for richer character emotions:
  - **sleepy**: closed eyes, normal mouth, relaxed eyebrows
  - **excited**: star eyes, grin mouth, raised eyebrows
  - **scared**: wide eyes, gasp mouth, worried eyebrows
  - **smirk**: normal eyes, asymmetric smirk mouth, asymmetric eyebrows
  - **crying**: tears eyes (with blue tear drops), frown mouth, worried eyebrows
- **Extended Pose System**: Added 6 new preset poses for more dynamic character positioning:
  - **jumping**: arms up, legs bent back, slight forward lean
  - **dancing**: asymmetric arm positions with body twist
  - **lying**: horizontal body orientation (90° body angle)
  - **kneeling**: one knee down pose
  - **cheering**: both arms raised high in celebration
  - **thinking**: hand on chin thoughtful pose
- **New Facial Component Types**: Added new component types for expressions:
  - **Eyes**: closed (sleepy curves), stars (sparkle effect), tears (with blue tear drops)
  - **Mouth**: grin (wide smile with teeth), gasp (larger open mouth), smirk (asymmetric half-smile)
  - **Eyebrows**: relaxed (low, slightly droopy), asymmetric (one raised, one flat)
- Both SVG and Cairo renderers fully support all new expression components (17 new tests).
- **ChubbyStickman Character**: New character style with rounded, friendlier appearance:
  - Larger head (22% of height vs 15% for regular Stickman)
  - Oval body shape for a rounder look
  - Shorter, thicker limbs with rounded ends (hands/feet)
  - Default white fill color for body parts
  - Full expression support (eyes, mouth, eyebrows render on the face)
  - Full pose support (all 12 poses work correctly)
  - Both SVG and Cairo renderers fully support ChubbyStickman rendering (24 new tests)
- **Stickman Expression Rendering**: Added face feature rendering to basic Stickman character:
  - Eyes, mouth, and eyebrows now render inside the head circle
  - All 11 expression types supported (neutral, happy, sad, angry, surprised, confused, sleepy, excited, scared, smirk, crying)
  - Both SVG and Cairo renderers fully support Stickman expression rendering (6 new tests)
  - Parity with ChubbyStickman and SimpleFace for expression support
- **Optional Dependency Fallback Tests**: Added tests for ImportError handling in comix/__init__.py and comix/renderer/__init__.py. Tests verify fallback behavior when pycairo or watchdog dependencies are unavailable (5 new tests).
- **Robot Character**: New mechanical/robot character style for sci-fi and tech-themed comics:
  - Square head with screen-like face display
  - Rectangular body with panel details and chest indicator light
  - Angular jointed limbs with circular joint indicators
  - LED-style eyes and digital display mouth expressions
  - Optional antenna (configurable)
  - Customizable colors: panel color, screen color, LED color
  - Full expression support (11 expressions) with robot-specific rendering
  - Full pose support (12 poses)
  - Both SVG and Cairo renderers fully support Robot rendering (32 new tests)
- **Chibi Character**: New cute/super-deformed anime-style character for kawaii and chibi comics:
  - Large head (40% of total height) with big expressive eyes
  - Small compact body with stubby limbs
  - 5 hair styles: spiky, long, short, twintails, none
  - Customizable colors: hair_color, skin_color, outfit_color
  - Optional blush marks for extra cuteness
  - Chibi-style facial features (large eyes with highlights, small cute mouth)
  - Full expression support (11 expressions) with chibi-specific rendering
  - Full pose support (12 poses)
  - Both SVG and Cairo renderers fully support Chibi rendering (36 new tests)
- **Anime Character**: Anime/manga style character with natural proportions for serious manga scenes:
  - Natural proportions (head is ~1/7 of height, not super-deformed)
  - Large expressive eyes with iris, pupil, and highlight rendering
  - Visible neck and shoulders with defined body shape
  - 7 hair styles: flowing, ponytail, short, spiky, bob, twintails, none
  - Customizable colors: hair_color, skin_color, outfit_color, eye_color
  - Gender option for body proportions (neutral, masculine, feminine)
  - Anime-style facial features with eye highlights and small mouth
  - Full expression support (11 expressions) with anime-specific eye rendering
  - Full pose support (12 poses)
  - Both SVG and Cairo renderers fully support Anime rendering (33 new tests)

### Technical Stack

- Python 3.13, managed with `uv`
- NumPy for coordinate calculations
- fonttools for font metrics
- pycairo (optional) for PNG/PDF output
- watchdog (optional) for file watching

## Future Enhancements (Ideas)

These are potential improvements, not planned work:

1. **Animation Export**: Animated GIF/video for webtoon scroll effects
2. **Additional Character Styles**: New character classes beyond existing ones (e.g., DetailedFace, RealisticStyle)
3. **Web Renderer**: HTML output with interactive features

## Known Issues

None currently tracked.
