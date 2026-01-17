# Changelog

All notable changes to this project are documented in this file.

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
