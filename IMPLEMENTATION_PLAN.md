# Implementation Plan

## Status: Core Features Complete (Phases 1-5) + Simplified Focus

**Current Git Tag: v0.1.88**

프로젝트를 **정적 만화 제작**에 집중하기 위해 간소화했습니다.
Core phases (1-5) 구현 완료. Advanced features (phases 6-8)는 보류.

### Core Phases (Active)

| Phase | Description | Status |
|-------|-------------|--------|
| Phase 1 | Core MVP (CObject, Panel, Bubble, Text, Character, Page, SVGRenderer) | ✅ Complete |
| Phase 2 | Styling (Font management, Theme system, Style inheritance) | ✅ Complete |
| Phase 3 | Layout Engine (FlowLayout, Auto bubble positioning, Collision detection) | ✅ Complete |
| Phase 4 | Extensions (Cairo renderer, Effects) | ✅ Complete |
| Phase 5 | Multi-page PDF Export (Book class, compile CLI command) | ✅ Complete |

### Advanced Phases (Optional, Available)

| Phase | Description | Status |
|-------|-------------|--------|
| Phase 6 | Interactive HTML Export (HTMLRenderer with zoom, pan, themes) | 📦 Available but not core |
| Phase 7 | Animation Export (GIF renderer, Timeline, Easing functions) | 📦 Available but not core |
| Phase 8 | Video Export (MP4/WebM via VideoRenderer with imageio-ffmpeg) | 📦 Available but not core |

### Core Features

- **CObject hierarchy**: Full transformation API (move_to, shift, scale, rotate)
- **Bubble system**: 5 types (Speech, Thought, Shout, Whisper, Narrator) with auto-positioning
- **Character system**: 9 styles (Stickman, SimpleFace, ChubbyStickman, Robot, Chibi, Anime, Superhero, Cartoon, AnimalStyle) with 11 expressions and 12 poses
- **Layout**: GridLayout, FlowLayout, ConstraintLayout with collision detection
- **Renderers**: SVG (always available), Cairo PNG/PDF (optional)
- **Effects**: 6 types (AppearEffect, ShakeEffect, ZoomEffect, MotionLines, FocusLines, ImpactEffect)
- **Templates**: 9 page templates (FourKoma, SplashPage, TwoByTwo, WebComic, ThreeRowLayout, MangaPage, ActionPage, NewspaperStrip, Widescreen)
- **Multi-page PDF**: Book class for compiling multiple pages
- **Working Examples**: 25 example scripts demonstrating all core features

### Advanced Features (Optional)

다음 기능들은 구현되어 있지만 core에서 제외되었습니다. `specs/future-features/`를 참고하세요:

- **HTML Export**: Interactive HTML with zoom, pan, themes
- **Animation System**: Timeline-based GIF animations with 28 easing functions
- **Video Export**: MP4/WebM output with audio support
- **Parser DSL**: Markup language for rapid comic creation
- **AI Images**: OpenAI DALL-E and Replicate integration
- **Preview Server**: Hot reload web preview

### Technical Stack (Core)

- Python 3.13, managed with `uv`
- NumPy for coordinate calculations
- fonttools for font metrics
- pycairo (optional) for PNG/PDF output

## Project Simplification (2026-01-18)

프로젝트를 정적 만화 제작에 집중하기 위해 다음과 같이 간소화했습니다:

### 변경 사항

1. **문서 구조 정리**:
   - 복잡한 spec들을 `specs/future-features/`로 이동
   - README.md와 specs/README.md에서 core 기능만 강조
   - PRD.md에서 Phase 6-8을 "향후 확장" 섹션으로 이동

2. **Core vs Advanced 분리**:
   - Core: 정적 이미지 렌더링 (PNG, SVG, PDF)
   - Advanced: HTML, Animation, Video, AI, Parser, Preview Server

3. **이유**:
   - 프로젝트 복잡도 감소
   - 핵심 가치에 집중 ("코드로 그림 그리는 만화")
   - 유지보수 부담 감소

### 코드는 그대로 유지

모든 advanced 기능들은 코드베이스에 그대로 남아있으며 언제든 사용 가능합니다.
다만 공식 문서에서는 core 기능만 다룹니다.

## Future Enhancements (Ideas)

Potential improvements for core features:

1. **Additional Character Styles**: New character classes (e.g., DetailedFace, RealisticStyle)
2. **More Templates**: Additional page layout templates

## Known Issues

None currently tracked.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and release notes.

---

## Note: Stable Release (v0.1.88)

All systems stable with 2014 tests passing (+ 30 skipped = 2044 collected). Version numbers synchronized across all files.

v0.1.88 changes:
- Fixed irregular panel rendering bug: SVG and Cairo renderers now properly render non-rectangular panels
- Added example 25 (panel_shapes.py) demonstrating all advanced panel types
- DiagonalPanel, TrapezoidPanel, IrregularPanel, StarburstPanel, CloudPanel, and ExplosionPanel now render with correct background fills
- Panel splitting methods (split_diagonal, split_curve) now render correctly
- Example 25 includes 8 output files showcasing diagonal, trapezoid, starburst, cloud, explosion, split diagonal, split curve, and mixed shapes

v0.1.87 changes:
- Fixed documentation inconsistencies in specs/working-examples.md
- Updated success metrics to reflect all visual bugs fixed (v0.1.85)
- Fixed example count from 23 to 24 in README section
- Updated character count reference to 9 (AnimalStyle)

v0.1.86 changes:
- Fixed documentation inconsistencies: Updated character count from 8 to 9 (AnimalStyle added in v0.1.83)
- Updated page template count from 7 to 9 (NewspaperStrip and Widescreen added in v0.1.72)
- Fixed example count from 15/23 to 24 across all documentation
- Updated specs/working-examples.md: Marked all visual bugs as fixed (v0.1.85)
- Added AnimalStyle to README.md examples and documentation

v0.1.85 changes:
- Fixed example 03 (group_scene) bubble positioning - bubbles no longer overlap with characters
- Improved character spacing and manual bubble positioning for clear reading order
- Added documentation explaining manual positioning for complex multi-character scenes

v0.1.84 changes:
- Updated documentation to reflect 9 character types (added AnimalStyle references)
- Updated specs/README.md with correct version (0.1.83), test counts (2014), and AnimalStyle
- Updated specs/character-basics.md with AnimalStyle character type
- Updated specs/PRD.md with 9 character types
- Enhanced example 16 to showcase all 9 character types including AnimalStyle
- Added new `create_animal_species_showcase()` function demonstrating all 7 animal species
- Documentation now consistent across all spec files

v0.1.83 changes:
- Added `AnimalStyle` character class - anthropomorphic animal characters for furry/mascot-style comics
- 7 species presets: cat, dog, rabbit, fox, bear, bird, wolf
- Species-specific features: head shapes (round, oval, pointed), ear types (pointed, floppy, tall, round, none)
- Customizable colors: fur_color, fur_secondary, eye_color, nose_color, outfit_color
- Optional tail with configurable length and curve
- Override ear_type and has_tail from species presets
- Added 32 new tests for AnimalStyle functionality
- Character system now has 9 styles (was 8)

v0.1.82 changes:
- Documentation updates: IMPLEMENTATION_PLAN.md, CRITICAL-BUGS-AND-FIXES.md
- Updated version tag and test counts

v0.1.81 changes:
- Added `auto_line_width` parameter to Stickman for automatic line width scaling with character height
- Line width now scales proportionally: 100px height = 2.0 line width, 50px = 1.0, 200px = 4.0
- Clamped between MIN_LINE_WIDTH (0.5) and MAX_LINE_WIDTH (6.0)
- Explicit `line_width` parameter overrides auto scaling when specified
- Added `auto_line_width=False` option to disable scaling and use fixed DEFAULT_LINE_WIDTH (2.0)
- Added 15 new tests for auto_line_width functionality
- Updated stickman-reference-based.md spec to mark line width scaling decision as complete

v0.1.80 changes:
- Fixed mypy configuration for optional dependencies (cairo_renderer.py, gif_renderer.py, video_renderer.py)
- Added mypy overrides for cairo and PIL optional dependencies in pyproject.toml
- Fixed inconsistent spacing in PIL.Image.resize() calls

v0.1.79 changes:
- Added automatic gutter spacing calculations for non-rectangular panels
- New geometry utilities: `point_to_segment_distance`, `segment_to_segment_distance`, `polygon_to_polygon_distance`, `calculate_gutter_adjustment`
- New Panel methods: `get_world_polygon()`, `distance_to_panel()`, `calculate_gutter_offset()`
- Enables precise positioning of DiagonalPanel, TrapezoidPanel, IrregularPanel, etc. with exact gutter spacing
- Added 32 new tests for gutter spacing functionality
- Updated panel-shapes.md spec to mark automatic gutter spacing as complete

v0.1.78 changes:
- Added preset panel shapes: StarburstPanel, CloudPanel, ExplosionPanel
- StarburstPanel: Star-shaped panels with configurable num_points and inner_ratio for dramatic moments
- CloudPanel: Cloud-shaped panels with num_bumps and bumpiness for dream sequences/flashbacks
- ExplosionPanel: Explosion-shaped panels with num_rays, ray_depth, randomness, and seed for action scenes
- Added 57 new tests for preset panel shapes
- Updated panel-shapes.md spec to mark preset shapes as complete

v0.1.77 changes:
- Added `line_width` parameter to Stickman for customizable stroke width
- Default line_width is 2.0 (backward compatible), minimum is 0.5
- Line width is now consistent across head outline and all body parts
- Added 13 new tests for line_width functionality (10 in test_character.py, 3 in test_renderer.py)
- Updated stickman-reference-based.md spec to mark line width consistency as complete

v0.1.76 changes:
- Added `head_squash` parameter to Stickman for head shape customization (ellipse/oval heads)
- Positive values flatten head (wider than tall), negative values elongate (taller than wide)
- Default 0.0 maintains perfect circle for backward compatibility
- Added 11 new tests for head_squash functionality
- Updated stickman-reference-based.md spec to mark head curve/roundness as complete

v0.1.75 changes:
- Updated documentation version numbers and test counts
- Added remaining spec enhancement items to Future Enhancements tracking

v0.1.74 changes:
- Added automatic tail width scaling with distance for speech bubbles
- Closer bubbles get wider tails (max 30px), farther bubbles get narrower tails (min 8px)
- New parameters: auto_tail_width, min_tail_width, max_tail_width, tail_width_close_distance, tail_width_far_distance
- Added get_effective_tail_width() method to Bubble class
- Added 15 new tests for tail width scaling functionality
- All "Should Have" items in bubble-tail-improvements.md now complete

v0.1.73 changes:
- Added `Panel.split_curve()` method for splitting panels along curved bezier lines
- Supports custom control points or automatic S-curve generation
- Supports curve_intensity (0.0-1.0) for controlling curve bulge
- Supports both directions: "top-left-to-bottom-right" and "top-right-to-bottom-left"
- Added 20 new tests for split_curve functionality

v0.1.72 changes:
- Added `NewspaperStrip` template for classic 3-4 horizontal panel newspaper comics
- Added `Widescreen` template with cinematic 16:9 aspect ratio panels
- Added example 24 demonstrating new templates
- Added 22 new tests for new templates

v0.1.71 changes:
- Added `Panel.split_diagonal()` method for splitting panels into triangular pieces
- Supports two directions: "top-left-to-bottom-right" and "top-right-to-bottom-left"
- Split panels inherit border, background, and padding from original
- Added 12 new tests for split_diagonal functionality

v0.1.70 changes:
- Added curved/smooth tail style for speech bubbles

v0.1.69 changes:
- Bumped version after tail style improvements

v0.1.68 changes:
- Added non-rectangular panel shapes: DiagonalPanel, TrapezoidPanel, IrregularPanel
- Implemented Stickman reference-based proportions with 4 presets (classic, xkcd, tall, child)
- Added bubble tail improvements: tail_mode (auto/fixed/none), smart_attach_to(), auto tail length calculation
- Added 48 new tests covering all new features
- Spec files implemented: panel-shapes.md, stickman-reference-based.md, bubble-tail-improvements.md

v0.1.67 changes:
- Fixed test count inconsistencies in documentation (1713 passed + 30 skipped = 1743 collected)
- Updated example count from 15 to 23 in specs/visual-validation-requirements.md

v0.1.66 changes:
- Fixed version inconsistency in specs/README.md (0.1.64 → 0.1.65)
- Fixed test count in specs/README.md (1743 → 1713)
- Added missing CHANGELOG entries for v0.1.54-v0.1.65

v0.1.65 changes:
- Fixed mypy type-check errors in optional dependency modules (video_renderer.py, preview/server.py)
- Improved type safety for optional dependencies (watchdog, imageio)

v0.1.64 changes:
- Synchronized version numbers to v0.1.64 across pyproject.toml, comix/constants.py, specs/README.md

v0.1.63 changes:
- Updated specs/README.md to reflect that all bugs are fixed
- Fixed example 07 bubble clipping by adjusting text and positions

v0.1.62 changes:
- Fixed bubble overlapping bug: Panel.add_content() now automatically repositions bubbles to avoid collisions
- Fixed Cairo/SVG renderer regression: Reverted transform-based coordinate system that broke rendering
- Panel children now use global coordinates (not panel-relative), matching the original design
- Example 16 updated to use global coordinates

Previous release (v0.1.61):
- Attempted transform-based coordinate system (reverted in v0.1.62 due to visual bugs)
