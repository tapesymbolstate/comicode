# Implementation Plan

## Status: Core Features Complete (Phases 1-5) + Simplified Focus

**Current Git Tag: v0.1.70**

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
- **Character system**: 8 styles (Stickman, SimpleFace, ChubbyStickman, Robot, Chibi, Anime, Superhero, Cartoon) with 11 expressions and 12 poses
- **Layout**: GridLayout, FlowLayout, ConstraintLayout with collision detection
- **Renderers**: SVG (always available), Cairo PNG/PDF (optional)
- **Effects**: 6 types (AppearEffect, ShakeEffect, ZoomEffect, MotionLines, FocusLines, ImpactEffect)
- **Templates**: 7 page templates (FourKoma, SplashPage, TwoByTwo, WebComic, ThreeRowLayout, MangaPage, ActionPage)
- **Multi-page PDF**: Book class for compiling multiple pages
- **Working Examples**: 23 example scripts demonstrating all core features

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

## Note: Stable Release (v0.1.68)

All systems stable with 1761 tests passing. Version numbers synchronized across all files.

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
