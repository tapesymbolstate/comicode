# Changelog

All notable changes to this project are documented in this file.

## [v0.1.110] - 2026-01-18

### Added
- 20 new edge case tests for geometry utilities in tests/test_utils.py:
  - Rotation edge cases (0°, 180°, 270°, large angles > 360°, negative angles)
  - scale_points with negative factors (mirroring) and zero factor
  - distance and midpoint with large/small coordinate values
  - angle_between edge cases including same point and negative quadrant
  - normalize_angle boundary cases (0, ±π)
  - bounding_box with single point and negative coordinates

### Documentation
- Version numbers synchronized across pyproject.toml, comix/constants.py, specs/README.md, and IMPLEMENTATION_PLAN.md

### Tests
- Test count: 2107 passed, 30 skipped (2137 collected)
- Improved test coverage for comix/utils/geometry.py functions

## [v0.1.109] - 2026-01-18

### Documentation
- Fixed version inconsistency in specs/README.md (footer showed 0.1.107 instead of current version)
- Version numbers synchronized across pyproject.toml, comix/constants.py, specs/README.md, and IMPLEMENTATION_PLAN.md

### Tests
- Test count: 2087 passed, 30 skipped (2117 collected)

## [v0.1.108] - 2026-01-18

### Documentation
- Added status indicators (✅/🔴/🚧) to examples/README.md for all 26 examples
- Added status comments to all 26 example files (e.g., `# Status: ✅ Working (v0.1.108)`)
- Updated examples-maintenance.md: Marked all "Must Have" acceptance criteria as complete
- Version numbers synchronized across pyproject.toml, comix/constants.py, specs/README.md, and IMPLEMENTATION_PLAN.md

### Tests
- Test count: 2087 passed, 30 skipped (2117 collected)

## [v0.1.107] - 2026-01-18

### Documentation
- Added missing CHANGELOG entries for v0.1.105 and v0.1.106
- Updated version references in specs/examples-maintenance.md and specs/visual-validation-requirements.md from v0.1.105 to v0.1.106
- Version numbers synchronized across pyproject.toml, comix/constants.py, specs/README.md, and IMPLEMENTATION_PLAN.md

### Tests
- Test count: 2087 passed, 30 skipped (2117 collected)

## [v0.1.106] - 2026-01-18

### Documentation
- Fixed documentation inconsistencies across spec files:
  - specs/getting-started.md: Updated character count from 8 to 9, added AnimalStyle to character list
  - specs/visual-validation-requirements.md: Updated version references from v0.1.101 to v0.1.105
  - specs/examples-maintenance.md: Updated version references from v0.1.101 to v0.1.105
  - specs/working-examples.md: Added Example 26 (stickman_articulation.py) to embedded README examples list
- Version numbers synchronized across pyproject.toml, comix/constants.py, specs/README.md, and IMPLEMENTATION_PLAN.md

### Tests
- Test count: 2087 passed, 30 skipped (2117 collected)

## [v0.1.105] - 2026-01-18

### Documentation
- Updated stickman-articulation.md spec: Marked 4 Open Questions as resolved with implementation decisions
  - Elbow/knee angles: 0° = straight (implemented)
  - Hyperextension: Not supported, angles clamped to 0-180° (implemented)
  - Hand gestures: Simple geometric representations with 7 options (implemented)
  - point_at(): Only adjusts arm angles, not body position (implemented)
- Version numbers synchronized across pyproject.toml, comix/constants.py, specs/README.md, and IMPLEMENTATION_PLAN.md

### Tests
- Test count: 2087 passed, 30 skipped (2117 collected)

## [v0.1.104] - 2026-01-18

### Bug Fixes
- **Fixed 3 missing assertions in test_character.py**: Tests for `test_facing_flips_points` in Stickman, ChubbyStickman, and Robot classes were calling `np.allclose()` without asserting the result, meaning the tests would pass even if the assertion would fail
  - Line 325: Added `assert` to Stickman.test_facing_flips_points
  - Line 778: Added `assert` to ChubbyStickman.test_facing_flips_points
  - Line 909: Added `assert` to Robot.test_facing_flips_points

### Tests
- Test count: 2087 passed, 30 skipped (2117 collected)

## [v0.1.99] - 2026-01-18

### Bug Fixes
- **Fixed mypy type errors in character.py**: ArmController.set_preset() now properly casts preset dict values to correct types (float for angles, str for hand gesture)
- **Fixed ruff error**: Removed unused `shoulder_offset` variable in point_at() method
- **Fixed ruff error**: Moved ArmController/LegController imports to top of test_character.py to resolve E402 (module-level import not at top of file)

### Tests
- Test count: 2087 passed, 30 skipped (2117 collected)

## [v0.1.98] - 2026-01-18

### Features
- **Stickman Articulation System**: Added joint-level control for precise limb positioning
  - New methods: `set_arm_angles()`, `set_leg_angles()`, `set_hands()`, `point_at()`
  - Shoulder angles (0-360°): 0° = down, 90° = forward, 180° = up, 270° = back
  - Elbow/Knee angles (0-180°): 0° = straight, 90° = right angle, 180° = fully bent
  - 7 hand gesture options: none, fist, open, point, peace, thumbs_up, relaxed
  - ArmController and LegController helper classes with preset poses

### Examples
- Added example 26 (26_stickman_articulation.py) demonstrating all articulation features

### Tests
- Added 72 new tests for articulation functionality
- Test count: 2087 passed, 30 skipped (2117 collected)

### Documentation
- Updated stickman-articulation.md spec to mark implementation complete

## [v0.1.97] - 2026-01-18

### Maintenance
- **Regenerated all example outputs**: Updated 76 example output files after Stickman Y-axis fix
  - All examples now display characters with correct orientation
  - PNG, PDF, HTML, and GIF outputs regenerated to match current code
- Version numbers synchronized across all files

## [v0.1.96] - 2026-01-18

### Bug Fixes
- **Fixed Stickman upside-down rendering**: Corrected Y-axis coordinate calculations in Stickman character
  - Root cause: Graphics coordinates use top-left origin where Y increases downward
  - Original code was subtracting Y to move down the body, causing head to render at bottom
  - Solution: Now correctly adds Y coordinates to move down (head_top → neck → hips → feet)
  - Before fix: Min Y = -69.60 (feet), Max Y = 49.93 (head) ❌
  - After fix: Min Y = -49.93 (head), Max Y = 69.60 (feet) ✅

### Documentation
- Updated stickman-reference-based.md with critical bug fix documentation
- Added detailed explanation of Y-axis coordinate system
- Version numbers synchronized across all files
- Removed test_stickman_fix.png from repository

## [v0.1.95] - 2026-01-18

### Documentation
- Fixed documentation inconsistencies: Updated test counts in specs/visual-validation-requirements.md and specs/CRITICAL-BUGS-AND-FIXES.md (1982/2014 → 2015)
- Added missing CHANGELOG entry for v0.1.94
- Version numbers synchronized across pyproject.toml, comix/constants.py, specs/README.md, and IMPLEMENTATION_PLAN.md

## [v0.1.94] - 2026-01-18

### Features
- **Realistic proportion style for Stickman**: Added `proportion_style="realistic"` for ideal 8-head figure drawing proportions
  - Uses balanced proportions: head_ratio=0.125, torso_ratio=0.375, arm_ratio=0.375, leg_ratio=0.50
  - Stickman now supports 5 proportion styles: classic, xkcd, tall, realistic, child

### Tests
- Added 1 new test for realistic proportion style
- Test count: 2015 passed, 30 skipped (2045 collected)

### Documentation
- Updated stickman-reference-based.md spec to mark "realistic" style decision as complete

## [v0.1.93] - 2026-01-18

### Documentation
- Fixed version inconsistency in specs/README.md (0.1.90 → 0.1.93)
- Version numbers synchronized across pyproject.toml, comix/constants.py, specs/README.md, and IMPLEMENTATION_PLAN.md

## [v0.1.74] - 2026-01-18

### Features
- **Automatic tail width scaling**: Speech bubble tails now automatically scale their width based on distance to the character
  - Closer bubbles get wider tails (max 30px) for prominent connection
  - Farther bubbles get narrower tails (min 8px) for subtle pointer
  - New parameters: `auto_tail_width`, `min_tail_width`, `max_tail_width`, `tail_width_close_distance`, `tail_width_far_distance`
  - New method: `get_effective_tail_width()` returns the calculated tail width
  - Enabled by default with `auto_tail_width=True`

### Tests
- Added 15 new tests for tail width scaling functionality
- Test count: 1854 passed, 30 skipped (1884 collected)

### Documentation
- Updated bubble-tail-improvements.md to mark tail width scaling as implemented
- All "Should Have" acceptance criteria in bubble-tail-improvements.md now complete
- Updated version numbers across all files

## [v0.1.73] - 2026-01-18

### Features
- **Panel.split_curve() method**: Split panels along curved bezier lines for flowing, organic panel divisions
  - Supports custom bezier control points for precise curve control
  - Automatic S-curve generation with configurable `curve_intensity` (0.0-1.0)
  - Both directions: "top-left-to-bottom-right" and "top-right-to-bottom-left"
  - Supports 2, 3, or 4+ control points (linear, quadratic, or cubic bezier)
  - Split panels inherit border, background, and padding from original

### Tests
- Added 20 new tests for split_curve functionality
- Test count: 1839 passed, 30 skipped (1869 collected)

### Documentation
- Updated panel-shapes.md to mark split_curve() as implemented
- Updated version numbers across all files

## [v0.1.72] - 2026-01-18

### Features
- **NewspaperStrip template**: Classic 3-4 horizontal panel layout for newspaper-style comics
- **Widescreen template**: Cinematic 16:9 aspect ratio panels for modern webcomics

### Tests
- Added 22 new tests for new templates
- Test count: 1819 passed, 30 skipped (1849 collected)

### Documentation
- Added example 24 demonstrating new templates

## [v0.1.71] - 2026-01-18

### Features
- **Panel.split_diagonal() method**: Dynamic comic layout splitting for triangular panel pieces
  - Supports two directions: "top-left-to-bottom-right" and "top-right-to-bottom-left"
  - Split panels inherit border, background, and padding from original

### Tests
- Added 12 new tests for split_diagonal functionality

## [v0.1.70] - 2026-01-18

### Features
- **Curved/smooth tail style**: Implemented bezier-curve based tail rendering for speech bubbles
  - `tail_style="smooth"` creates curved, natural-looking tails using bezier curves
  - `tail_style="minimal"` creates short, subtle nub tails
  - `tail_style="classic"` (default) maintains the original triangular tail
- Added `create_smooth_tail_points()` and `create_minimal_tail_points()` utility functions

### Tests
- Added 24 new tests for tail style functionality
- Test count: 1785 passed, 30 skipped

### Documentation
- Updated bubble-tail-improvements.md to mark curved/bezier tail as implemented

## [v0.1.69] - 2026-01-18

### Documentation
- Fixed version inconsistencies across documentation files
- Synchronized version to v0.1.69 across pyproject.toml, constants.py, specs/README.md, IMPLEMENTATION_PLAN.md
- Added missing v0.1.68 changelog entry

## [v0.1.68] - 2026-01-18

### Features
- **Non-rectangular panel shapes**: Added DiagonalPanel, TrapezoidPanel, IrregularPanel for creative layouts
- **Stickman reference-based proportions**: Redesigned with 4 presets (classic, xkcd, tall, child)
- **Bubble tail improvements**: Added tail_mode (auto/fixed/none), smart_attach_to(), auto tail length calculation

### Tests
- Added 48 new tests covering all new features
- Test count: 1761 passed, 30 skipped

### Documentation
- Added spec files: panel-shapes.md, stickman-reference-based.md, bubble-tail-improvements.md

## [v0.1.67] - 2026-01-18

### Documentation
- Fixed test count inconsistencies across documentation files
  - Clarified: 1713 passed + 30 skipped = 1743 collected
- Updated example count from 15 to 23 in specs/visual-validation-requirements.md
- Corrected test count format in specs/CRITICAL-BUGS-AND-FIXES.md

## [v0.1.66] - 2026-01-18

### Documentation
- Fixed version inconsistency in specs/README.md (0.1.64 → 0.1.65)
- Fixed test count in specs/README.md (1743 → 1713)
- Added missing CHANGELOG entries for v0.1.54-v0.1.65

## [v0.1.65] - 2026-01-18

### Bug Fixes
- Fixed mypy type-check errors in optional dependency modules
  - video_renderer.py: Fixed type annotations for optional imageio dependency
  - preview/server.py: Fixed type annotations for optional watchdog dependency
- Improved type safety for optional dependencies (watchdog, imageio)

## [v0.1.64] - 2026-01-18

### Documentation
- Synchronized version numbers to v0.1.64 across pyproject.toml, comix/constants.py, specs/README.md

## [v0.1.63] - 2026-01-18

### Bug Fixes
- Fixed example 07 bubble clipping by adjusting text and positions

### Documentation
- Updated specs/README.md to reflect that all bugs are fixed

## [v0.1.62] - 2026-01-18

### Bug Fixes
- Fixed bubble overlapping bug: Panel.add_content() now automatically repositions bubbles to avoid collisions
- Fixed Cairo/SVG renderer regression: Reverted transform-based coordinate system that broke rendering
- Panel children now use global coordinates (not panel-relative), matching the original design
- Example 16 updated to use global coordinates

## [v0.1.61] - 2026-01-18

### Changes
- Attempted transform-based coordinate system (reverted in v0.1.62 due to visual bugs)

## [v0.1.60] - 2026-01-18

### Documentation
- Updated documentation to reflect visual bug fixes

## [v0.1.59] - 2026-01-18

### Maintenance
- Code cleanup and documentation updates

## [v0.1.58] - 2026-01-18

### Documentation
- Version synchronization across all files

## [v0.1.57] - 2026-01-18

### Documentation
- Updated example documentation

## [v0.1.56] - 2026-01-18

### Documentation
- Updated IMPLEMENTATION_PLAN.md

## [v0.1.55] - 2026-01-18

### Examples
- Added examples 17-23 demonstrating advanced features
  - 17_ai_image_generation.py: AI-generated images
  - 18_flow_layout.py: FlowLayout system
  - 19_constraint_layout.py: ConstraintLayout system
  - 20_themes_and_styles.py: Theme and style system
  - 21_text_and_narration.py: Text and narration features
  - 22_advanced_templates.py: Advanced page templates
  - 23_preview_server.py: Live preview server

## [v0.1.54] - 2026-01-18

### Documentation
- Documentation cleanup and version updates

## [v0.1.53] - 2026-01-18

### Bug Fixes
- Fixed mypy errors in preview server watchdog handling
  - Refactored optional watchdog import pattern to properly handle TYPE_CHECKING and runtime fallbacks
  - Removed unused type ignore comments
  - Used appropriate type annotations for dynamic observer type

### Testing
- Test count now at 1743 tests passing

## [v0.1.52] - 2026-01-18

### Documentation
- Synced all documentation files to v0.1.51 with accurate version references
- Updated PRD.md, README.md, working-examples.md, examples-maintenance.md to reflect 16 examples
- Corrected test count to 1739 (1739 pass + 4 skip)

## [v0.1.51] - 2026-01-18

### Examples
- Added example 16: Character Types showcase (`16_character_types.py`)
  - Demonstrates all 8 character types (Stickman, SimpleFace, ChubbyStickman, Robot, Chibi, Anime, Cartoon, Superhero)
  - Shows expression comparison across different character types
  - Shows pose demonstration with various character types
  - Creates 3 output files: character showcase, expression comparison, and pose showcase

### Documentation
- Updated examples/README.md with new example listing
- Updated IMPLEMENTATION_PLAN.md to v0.1.51 and 16 examples

## [v0.1.50] - 2026-01-18

### Bug Fixes
- Synced VERSION constant in constants.py to match pyproject.toml
- Updated CLI tests to use VERSION constant instead of hardcoded version strings

### Documentation
- Added missing CHANGELOG entries for v0.1.40 through v0.1.49
- Updated IMPLEMENTATION_PLAN.md to v0.1.50

## [v0.1.49] - 2026-01-18

### Documentation
- Updated all spec files to v0.1.49
- Updated IMPLEMENTATION_PLAN.md to v0.1.49

## [v0.1.48] - 2026-01-18

### Documentation
- Synced version references to v0.1.48 across all documentation
- Updated IMPLEMENTATION_PLAN.md to v0.1.48

## [v0.1.47] - 2026-01-18

### Documentation
- Updated IMPLEMENTATION_PLAN.md to v0.1.47

## [v0.1.46] - 2026-01-18

### Documentation
- Corrected easing function count to 28 in documentation
- Fixed version references across documentation
- Updated IMPLEMENTATION_PLAN.md to v0.1.46

## [v0.1.45] - 2026-01-18

### Features
- **Multi-page Book Parser**: Added `parse_book_markup()` function for parsing multi-page comics from markup DSL
  - Supports `===` separator for page breaks
  - Supports `---` separator for panel breaks
  - Returns Book object with multiple Page instances

### Documentation
- Added animation-export.md and video-export.md specifications
- Synced documentation with v0.1.45 test counts

## [v0.1.44] - 2026-01-18

### Documentation
- Synced specs with v0.1.44 test count and version
- Updated IMPLEMENTATION_PLAN.md to v0.1.44

## [v0.1.43] - 2026-01-18

### Features
- **Audio Track Support**: Added audio track support for VideoRenderer
  - Allows mixing audio tracks with video export

### Tests
- Added tests for audio track functionality
- Updated IMPLEMENTATION_PLAN.md to v0.1.43

## [v0.1.42] - 2026-01-18

### Documentation
- Updated test count to 1726 (1722 pass + 4 skip)
- Synced specs with actual example count (15 examples)
- Updated AGENTS.md with animation system and correct example count
- Updated IMPLEMENTATION_PLAN.md to v0.1.42

## [v0.1.41] - 2026-01-18

### Documentation
- Synced specs with IMPLEMENTATION_PLAN.md for v0.1.41
- Updated IMPLEMENTATION_PLAN.md to v0.1.41

## [v0.1.40] - 2026-01-18

### Bug Fixes
- Fixed mypy type errors for watchdog optional dependency

### Documentation
- Updated IMPLEMENTATION_PLAN.md to v0.1.40

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
