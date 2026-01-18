# Comix Specifications

This directory contains specifications for the Comix comic creation library, written in the Ralph Wiggum methodology (JTBD → Spec format).

## Overview

Comix is a Python library for creating comics programmatically, inspired by Manim's API design but focused on comic/manga creation instead of mathematical animations.

**Current Status**: All 8 phases implemented. 2014 tests passing (+ 30 skipped = 2044 collected), mypy and ruff pass. **Version: v0.1.86**

## ✅ Visual Bugs Fixed (v0.1.62)

Previous visual issues have been resolved:
- ✅ Speech bubble overlapping - Fixed via auto_position_bubbles in Panel.add_content()
- ✅ GridLayout coordinate transformation - Fixed by reverting to global coordinates
- ✅ Character expression/pose rendering - Already working correctly

See [CRITICAL-BUGS-AND-FIXES.md](CRITICAL-BUGS-AND-FIXES.md) for historical details.

## Active Specs

### Core Workflows

- [Getting Started](getting-started.md) - Creating your first comic (2-panel dialogue)
- [Character Basics](character-basics.md) - Creating and positioning stick figure characters
- [Speech Bubbles](speech-bubbles.md) - Adding dialogue with automatic bubble attachment
- [Page Rendering](page-rendering.md) - Exporting comics to PNG and PDF formats
- [Working Examples](working-examples.md) - Runnable Python scripts demonstrating usage
- [Effect System](effect-system.md) - Visual effects (shake, zoom, motion lines, focus, impact)

### Bug Tracking (Historical)

- **[CRITICAL-BUGS-AND-FIXES.md](CRITICAL-BUGS-AND-FIXES.md)** - Historical record of fixed visual bugs

### Future Features (Advanced, Optional)

프로젝트를 정적 만화 제작에 집중하기 위해 다음 기능들은 보류되었습니다.
관심있는 경우 참고할 수 있습니다:

- [Parser DSL](parser-dsl.md) - Markup language for rapid comic creation
- [AI Images](ai-images.md) - DALL-E and Replicate AI image generation
- [Preview Server](preview-server.md) - Live reload development server
- [HTML Export](html-export.md) - Interactive HTML export with zoom, pan, themes
- [Animation Export](animation-export.md) - Timeline-based GIF animations with easing
- [Video Export](video-export.md) - MP4/WebM video export with audio support

### Architecture (Reference)

- [PRD.md](PRD.md) - Product Requirements Document with full architecture design

## Quick Status

### Core Features
| Spec | Status |
|------|--------|
| Getting Started | ✅ Complete |
| Character Basics | ✅ Complete |
| Speech Bubbles | ✅ Complete |
| Page Rendering | ✅ Complete |
| Working Examples | ✅ Complete |
| Effect System | ✅ Complete |

### Future Features (Optional)
| Spec | Status |
|------|--------|
| Parser DSL | 📦 Available but not core |
| AI Images | 📦 Available but not core |
| Preview Server | 📦 Available but not core |
| HTML Export | 📦 Available but not core |
| Animation Export | 📦 Available but not core |
| Video Export | 📦 Available but not core |

### Examples Status (examples/output/)

All 24 examples (01-24) execute without errors and produce correct visual output.

## Features

### Character Types (9 styles)
- **Stickman** - Basic stick figure with expressions
- **SimpleFace** - Emoticon-style face
- **ChubbyStickman** - Rounded, friendly stick figure
- **Robot** - Mechanical character for sci-fi themes
- **Chibi** - Cute anime-style character
- **Anime** - Natural proportion anime character
- **Superhero** - Heroic character with costume options
- **Cartoon** - Classic Western cartoon style
- **AnimalStyle** - Anthropomorphic animal characters (cat, dog, rabbit, fox, bear, bird, wolf)

### Expressions (11 types)
neutral, happy, sad, angry, surprised, confused, sleepy, excited, scared, smirk, crying

### Poses (12 types)
standing, sitting, waving, pointing, walking, running, jumping, dancing, lying, kneeling, cheering, thinking

### Bubble Types
- **SpeechBubble** - Standard dialogue
- **ThoughtBubble** - Cloud-like for thoughts
- **ShoutBubble** - Jagged/spiky for emphasis
- **WhisperBubble** - Dashed border for quiet speech
- **NarratorBubble** - Rectangular, no tail for narration

### Page Templates
- **FourKoma** - 4-panel vertical (manga style)
- **TwoByTwo** - 2x2 grid layout
- **SplashPage** - Full-page dramatic
- **WebComic** - Vertical scroll format
- **ThreeRowLayout** - Flexible row-based layout
- **MangaPage** - Traditional manga layouts
- **ActionPage** - Main panel with reaction panels
- **NewspaperStrip** - Classic 3-4 horizontal panels for newspaper comics
- **Widescreen** - Cinematic 16:9 aspect ratio panels

### Effects
- AppearEffect, ShakeEffect, ZoomEffect
- MotionLines, FocusLines, ImpactEffect

### Rendering (Core)
- **SVG** - Vector output (always available)
- **PNG** - Raster output (optional, requires pycairo)
- **PDF** - Document output (optional, requires pycairo)
- **Multi-page PDF** - Book class for compiling pages

## Acceptance Criteria Flow

```
getting-started.md
    ├─> character-basics.md (all character types implemented)
    ├─> speech-bubbles.md (all bubble types implemented with collision avoidance)
    └─> page-rendering.md (all formats supported)
         └─> working-examples.md (all examples execute with correct output)
```

**Current Reality**: All core features implemented, tests pass, and visual output is correct.

## How to Use These Specs

### For AI Agents (Ralph Loop)

1. Read relevant spec file (e.g., `character-basics.md`)
2. Identify "Must Have" acceptance criteria
3. Verify implementation matches spec
4. Run examples and visually verify PNG output
5. Update IMPLEMENTATION_PLAN.md with findings

### For Human Developers

1. Start with `getting-started.md` to understand basic workflow
2. Read `working-examples.md` for runnable code
3. Refer to specific specs (character, bubbles, etc.) for details
4. Use acceptance criteria as test checklist
5. Use examples as templates for your own comics

## Testing Against Specs

Each spec includes "Test Requirements" section. To validate:

```bash
# 1. Run all tests
uv run pytest

# 2. Run specific category
uv run pytest tests/test_character.py
uv run pytest tests/test_bubble.py
uv run pytest tests/test_renderer.py

# 3. Run examples
uv run python examples/01_simple_dialogue.py

# 4. Visually verify PNG output
# - Open examples/output/01_simple_dialogue.png
# - Verify characters are complete
# - Verify bubbles have borders
# - Verify layout is correct
```

## Spec Format

Each spec follows this structure:

- **What**: One-sentence description
- **Why**: User value and problem being solved
- **Acceptance Criteria**: Testable requirements (Must/Should/Won't Have)
- **Context**: User flows, edge cases, constraints
- **Examples**: Concrete code samples
- **Open Questions**: Decisions needed
- **Test Requirements**: How to verify acceptance criteria

## Future Enhancements (Ideas)

Potential features not yet scoped:

- **Additional Character Styles** - New character types (DetailedFace, RealisticStyle)
- **Comic Reader Component** - Web component for viewing multi-page comics

## Contributing

When adding new specs:

1. Follow the "One Sentence Without 'And'" test (one spec per distinct concern)
2. Use the standard spec template (see existing specs)
3. Link related specs in "Related Specs" section
4. Add acceptance criteria that are specific and testable
5. Include concrete examples with expected results
6. Update this README with spec status

## Ralph Loop Context

These specs are designed to work with the Ralph Wiggum AI development methodology:

- **Planning Mode** (`PROMPT_plan.md`): Reads specs to identify gaps and generate implementation plan
- **Building Mode** (`PROMPT_build.md`): Implements according to spec acceptance criteria
- **Validation**: Tests derived from acceptance criteria provide feedback loop

See `IMPLEMENTATION_PLAN.md` for current implementation status.

---

**Version**: 0.1.83 (as of 2026-01-18)
**Last Updated**: 2026-01-18
**Maintainer**: Claude Code Ralph Agent

All systems stable with 2014 tests passing (+ 30 skipped = 2044 collected).
