# Changelog

All notable changes to this project are documented in this file.

## [v0.1.39] - 2026-01-18

### Features
- **Video Export System** (Phase 8 Complete):
  - Added `VideoRenderer` class for MP4/WebM video output
  - Uses imageio-ffmpeg for cross-platform video encoding
  - Quality settings: low (72 DPI), medium (96 DPI), high (150 DPI)
  - Progress callback support for tracking rendering progress
  - Frame extraction for post-processing workflows
  - Proper handling of odd dimensions (video codecs require even dimensions)
  - JPEG frame export with alpha channel compositing
  - New example 15: Video Export (`15_video_export.py`)

### Technical
- Added `video` optional dependency group in pyproject.toml (imageio[ffmpeg], imageio[pyav])
- Added mypy overrides for imageio modules
- Added 25 new tests for VideoRenderer

### Documentation
- Updated README.md with video export information
- Updated IMPLEMENTATION_PLAN.md to Phase 8 complete
- Updated example count from 14 to 15

## [v0.1.38] - 2026-01-18

### Documentation
- Updated IMPLEMENTATION_PLAN.md version number

## [v0.1.37] - 2026-01-18

### Features
- **Animation Export System** (Phase 7 Complete):
  - Added `GIFRenderer` class for animated GIF output
  - `Timeline` class for orchestrating animations with precise timing
  - `Animation` base class with 28 easing functions (linear, quad, cubic, quart, sine, expo, elastic, back, bounce - each with in/out/inOut variants, plus convenience aliases)
  - `EffectAnimation` for animating visual effects
  - `ObjectAnimation` for animating CObject properties (position, rotation, scale, opacity)
  - `PropertyAnimation` for generic property animation
  - `AnimationGroup` for parallel/sequential animation groups
  - New example 14: Animation Export (`14_animation_export.py`)

### Documentation
- Updated IMPLEMENTATION_PLAN.md to reflect Phase 7 completion
- Updated example count from 13 to 14

## [v0.1.36] - 2026-01-18

### Documentation
- Updated IMPLEMENTATION_PLAN.md version number

## [v0.1.35] - 2026-01-18

### Documentation
- Updated IMPLEMENTATION_PLAN.md version number

## [v0.1.34] - 2026-01-18

### Documentation
- Updated AGENTS.md project structure documentation
- Updated IMPLEMENTATION_PLAN.md version number

## [v0.1.33] - 2026-01-18

### Documentation
- Updated CHANGELOG.md with all missing version entries from v0.1.20 through v0.1.32
- Changelog now accurately documents all releases including Interactive HTML Export, parser examples, and security fixes

## [v0.1.32] - 2026-01-18

### Security
- **Critical**: Fixed SSL certificate verification vulnerability in `ai_image.py`
  - The `_download_image` method was using `verify=False` when downloading generated images from Replicate
  - Now uses proper SSL certificate verification for secure downloads

## [v0.1.31] - 2026-01-18

### Documentation
- Updated IMPLEMENTATION_PLAN.md to v0.1.31
- Updated PRD.md to reflect all implemented features including Interactive HTML Export

## [v0.1.30] - 2026-01-18

### Documentation
- Updated documentation to reflect 13 working examples in examples/ directory

## [v0.1.29] - 2026-01-18

### Examples
- Added example 12: Parser DSL (`12_parser_dsl.py`) - Demonstrates markup DSL for rapid comic creation with 5 examples including Korean Unicode support
- Added example 13: Visual Effects (`13_visual_effects.py`) - Showcases all 6 manga-style effects (ShakeEffect, ZoomEffect, MotionLines, FocusLines, AppearEffect, ImpactEffect)

## [v0.1.28] - 2026-01-18

### Documentation
- Added `specs/html-export.md` specification for Interactive HTML Export feature
- Updated documentation test counts

## [v0.1.27] - 2026-01-18

### Features
- **Interactive HTML Export** (Phase 6 Complete):
  - Added `HTMLRenderer` class wrapping SVGRenderer for HTML output
  - Single-page and multi-page book export support
  - **Zoom controls**: Mouse wheel, +/- buttons, keyboard shortcuts (+, -, 0)
  - **Pan functionality**: Mouse drag, touch swipe support
  - **Theme toggle**: Dark/light modes with T keyboard shortcut
  - **Fullscreen mode**: F keyboard shortcut
  - **Page navigation**: Arrow keys, prev/next buttons for multi-page comics
  - Configurable feature toggles and zoom range
  - Custom title support and hover effects on panels
  - Page indicator for multi-page books
  - Status bar with usage instructions
  - Touch support for mobile devices
  - Smooth animations for zoom transitions
  - Responsive design

## [v0.1.26] - 2026-01-18

### Documentation
- Added missing specs for extended features:
  - `specs/effect-system.md`: Visual effects system specification
  - `specs/parser-dsl.md`: Markup DSL parser specification
  - `specs/ai-images.md`: AI image integration specification
  - `specs/preview-server.md`: Preview server specification

## [v0.1.25] - 2026-01-18

### Documentation
- Cleaned up IMPLEMENTATION_PLAN.md for readability and maintainability

## [v0.1.24] - 2026-01-18

### Bug Fixes
- Fixed PreviewServer socket cleanup to properly release ports on shutdown
- Updated documentation test counts

## [v0.1.23] - 2026-01-18

### Documentation
- Updated specs for consistency across all specification documents
- Added Book PDF character rendering test

## [v0.1.22] - 2026-01-18

### Tests
- Added edge case tests for effects system
- Added edge case tests for bubble positioning
- Added edge case tests for character type resolution

## [v0.1.21] - 2026-01-18

### Tests
- Added comprehensive pose and expression test coverage for all 8 character types
- Ensures all 11 expressions and 12 poses work correctly across all character styles

## [v0.1.20] - 2026-01-18

### Documentation
- Updated specs/README.md test count to 1536
- Updated IMPLEMENTATION_PLAN.md and CHANGELOG.md

## [v0.1.19] - 2026-01-18

### Refactoring
- Extracted script loading utilities to reduce code duplication:
  - Added `comix/utils/script_loader.py` with shared functions for loading Python scripts and finding Page objects
  - `load_script_module()`: Load a Python script as a module with proper cache invalidation
  - `find_page_in_module()`: Find Page class or instance in a module
  - `load_page_from_script()`: Convenience function combining both operations
  - `ScriptLoadError`: Exception for script loading failures

### Code Quality
- Refactored CLI commands (`render`, `preview`, `compile`) to use shared utilities
- Refactored preview server `ScriptLoader` class to use shared utilities
- Removed ~70 lines of duplicated code across 4 files

### Tests
- Added 19 new tests in `tests/test_script_loader.py`:
  - Tests for loading valid/invalid scripts
  - Tests for module cache handling
  - Tests for finding Page classes and instances
  - Tests for error handling (missing files, syntax errors, import errors)
  - Tests for utility exports

## [v0.1.18] - 2026-01-18

### Documentation
- Updated specs to document undocumented implementation features:
  - specs/character-basics.md: Added shout() and whisper() convenience methods
  - specs/speech-bubbles.md: Documented auto-positioning system (auto_attach_to, overlaps_with, auto_position_bubbles) and marked collision avoidance question as resolved
  - specs/PRD.md: Added MINIMAL_STYLE preset definition

## [v0.1.17] - 2026-01-18

### Documentation
- Added CHANGELOG.md to consolidate version history and release notes
- Cleaned up IMPLEMENTATION_PLAN.md by moving historical verification notes to CHANGELOG.md
- Reduced IMPLEMENTATION_PLAN.md from 368 to 266 lines for better maintainability

## [v0.1.16] - 2026-01-18

### Documentation
- Updated test count in specs/README.md from "1507 tests passing (1 skipped)" to "1517 tests passing"

## [v0.1.15] - 2026-01-18

### Code Quality
- Moved function-level imports to module level in SVG and Cairo renderers
  - `svg_renderer.py`: Added base64 and math imports at module level, removed 5 inline imports
  - `cairo_renderer.py`: Added base64 import at module level, removed 6 redundant inline imports

## [v0.1.14] - 2026-01-18

### Test Cleanup
- Removed always-skipped placeholder test `test_render_single_page` from `TestBookRender` class
- Test count now shows 1517 passed, 0 skipped

## [v0.1.13] - 2026-01-18

### Documentation
- Updated PRD.md: Marked all 4 roadmap phases as complete
- Updated visual-validation-requirements.md: Added note clarifying these are process guidelines
- Updated examples-maintenance.md: Corrected outdated "broken" status to show all 10 examples working

## [v0.1.12] - 2026-01-18

### Tests
- Added edge case tests and warning logging for character expressions/poses

## [v0.1.11] - 2026-01-18

### Features
- Added `progress_callback` parameter to `Book.render()` and `CairoRenderer.render_book()` methods
- Callback receives `(current_page, total_pages)` arguments (1-indexed)
- Added 5 new tests in `tests/test_book.py::TestProgressCallback`

## [v0.1.10] - 2026-01-18

### Documentation
- Updated specs/README.md test count from 1460 to 1502

## [v0.1.9] - 2026-01-18

### Configuration
- Added `[[tool.mypy.overrides]]` configuration in pyproject.toml for third-party libraries
- fontTools, svgwrite, openai, and replicate modules configured with `ignore_missing_imports = true`

## [v0.1.8] - 2026-01-18

### Code Quality
- Removed obsolete `# type: ignore` comments from fontTools, svgwrite, openai, and replicate imports
- mypy now passes with 0 errors

## [v0.1.7] - 2026-01-18

### Bug Fixes
- **Critical**: Fixed double position bug in character rendering where positions were added twice
- **Critical**: Fixed double position bug in bubble rendering
- Fixed example coordinate issues in examples 01, 02, 04, 05, 06, 07, and 09

### Documentation
- Created comprehensive README.md with installation instructions and quick start examples

## [v0.1.6] - 2026-01-18

### Bug Fixes
- Fixed Anime/Superhero/Cartoon character rendering bug where these types fell through to generic renderer
- Fixed in both `svg_renderer.py` and `cairo_renderer.py`

### Tests
- Added 37 new character rendering tests
- Coverage improved from 85% to 98%
  - svg_renderer.py: 71% → 98%
  - cairo_renderer.py: 64% → 98%

## [v0.1.5] - 2026-01-18

### Cleanup
- Removed accidental `book.pdf` artifact from repository root
- Added `book.pdf` to `.gitignore`

## [v0.1.0] - 2026-01-18

### Initial Release
All 5 implementation phases complete with 1517 tests passing.

#### Features
- **CObject hierarchy**: Full transformation API with convenience methods
- **Bubble system**: 5 types (Speech, Thought, Shout, Whisper, Narrator)
- **Character system**: 8 character styles (Stickman, SimpleFace, ChubbyStickman, Robot, Chibi, Anime, Superhero, Cartoon)
- **Expressions**: 11 preset expressions (neutral, happy, sad, angry, surprised, confused, sleepy, excited, scared, smirk, crying)
- **Poses**: 12 preset poses (standing, sitting, waving, pointing, walking, running, jumping, dancing, lying, kneeling, cheering, thinking)
- **Layout**: GridLayout, FlowLayout, ConstraintLayout with priority-based solving
- **Renderers**: SVG (always available), Cairo PNG/PDF (optional)
- **Effects**: 6 effect types (AppearEffect, ShakeEffect, ZoomEffect, MotionLines, FocusLines, ImpactEffect)
- **Parser**: DSL markup for rapid comic creation
- **AI Images**: OpenAI DALL-E and Replicate integration
- **Preview Server**: Hot reload web preview with file watching
- **Multi-page PDF**: Book class with compile CLI command
- **Templates**: 7 pre-built page layouts (FourKoma, SplashPage, TwoByTwo, WebComic, ThreeRowLayout, MangaPage, ActionPage)
