# Comix Specifications

This directory contains specifications for the Comix comic creation library, written in the Ralph Wiggum methodology (JTBD → Spec format).

## Overview

Comix is a Python library for creating comics programmatically, inspired by Manim's API design but focused on comic/manga creation instead of mathematical animations.

**Current Status**: All 8 phases implemented. 1743 tests passing, mypy and ruff pass. **However, visual bugs exist** - see CRITICAL-BUGS-AND-FIXES.md for details.

## ⚠️ CRITICAL: Visual Bugs

**READ THIS FIRST**: [CRITICAL-BUGS-AND-FIXES.md](CRITICAL-BUGS-AND-FIXES.md)

Tests pass but visual output has issues:
- Speech bubble overlapping in group scenes
- GridLayout coordinate transformation problems
- Character expression/pose rendering incomplete

## Active Specs

### Core Workflows

- [Getting Started](getting-started.md) - Creating your first comic (2-panel dialogue)
- [Character Basics](character-basics.md) - Creating and positioning stick figure characters
- [Speech Bubbles](speech-bubbles.md) - Adding dialogue with automatic bubble attachment
- [Page Rendering](page-rendering.md) - Exporting comics to PNG and PDF formats
- [Working Examples](working-examples.md) - Runnable Python scripts demonstrating usage

### Critical Issues

- **[CRITICAL-BUGS-AND-FIXES.md](CRITICAL-BUGS-AND-FIXES.md)** - Real visual bugs that need fixing despite tests passing

### Extended Features

- [Effect System](effect-system.md) - Visual effects (shake, zoom, motion lines, focus, impact)
- [Parser DSL](parser-dsl.md) - Markup language for rapid comic creation
- [AI Images](ai-images.md) - DALL-E and Replicate AI image generation
- [Preview Server](preview-server.md) - Live reload development server
- [HTML Export](html-export.md) - Interactive HTML export with zoom, pan, themes
- [Animation Export](animation-export.md) - Timeline-based GIF animations with easing
- [Video Export](video-export.md) - MP4/WebM video export with audio support

### Architecture (Reference)

- [PRD.md](PRD.md) - Product Requirements Document with full architecture design

## Quick Status

| Spec | Status |
|------|--------|
| **CRITICAL-BUGS-AND-FIXES** | 🔴 **Active bugs - priority fixes needed** |
| Getting Started | ⚠️ Code works, visual bugs exist |
| Character Basics | ⚠️ Code works, visual bugs exist |
| Speech Bubbles | 🔴 Bubble overlapping issues |
| Page Rendering | ⚠️ GridLayout coordinate bugs |
| Working Examples | ⚠️ Examples execute, output has visual issues |
| Effect System | ✅ Complete |
| Parser DSL | ✅ Complete |
| AI Images | ✅ Complete |
| Preview Server | ✅ Complete |
| HTML Export | ✅ Complete |
| Animation Export | ✅ Complete |
| Video Export | ✅ Complete |

### Examples Status (examples/output/)

All 23 examples (01-23) execute without errors. **However, visual output has bugs** - bubbles overlap, layout positioning incorrect in some cases. See CRITICAL-BUGS-AND-FIXES.md for details.

## Features

### Character Types
- **Stickman** - Basic stick figure with expressions
- **SimpleFace** - Emoticon-style face
- **ChubbyStickman** - Rounded, friendly stick figure
- **Robot** - Mechanical character for sci-fi themes
- **Chibi** - Cute anime-style character
- **Anime** - Natural proportion anime character
- **Superhero** - Heroic character with costume options
- **Cartoon** - Classic Western cartoon style

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

### Effects
- AppearEffect, ShakeEffect, ZoomEffect
- MotionLines, FocusLines, ImpactEffect

### Rendering
- **SVG** - Vector output (always available)
- **PNG** - Raster output (optional, requires pycairo)
- **PDF** - Document output (optional, requires pycairo)
- **Multi-page PDF** - Book class for compiling pages
- **Interactive HTML** - Standalone HTML with zoom, pan, themes
- **Animated GIF** - Timeline-based animation export (optional, requires Pillow)
- **Video (MP4/WebM)** - Video export with ffmpeg and audio track support (optional, requires imageio-ffmpeg)

## Acceptance Criteria Flow

```
CRITICAL-BUGS-AND-FIXES.md (⚠️ FIX THESE FIRST)
    ↓
getting-started.md
    ├─> character-basics.md (all character types implemented)
    ├─> speech-bubbles.md (all bubble types implemented, but overlapping issue)
    └─> page-rendering.md (all formats supported, GridLayout has bugs)
         └─> working-examples.md (examples execute but visual bugs exist)
```

**Current Reality**: Core features implemented and tests pass. **However, visual quality has issues** - see CRITICAL-BUGS-AND-FIXES.md for P0/P1 bug fixes needed.

## How to Use These Specs

### For AI Agents (Ralph Loop)

**⚠️ MANDATORY FIRST STEP**: Read [CRITICAL-BUGS-AND-FIXES.md](CRITICAL-BUGS-AND-FIXES.md) before any work.

1. **Read CRITICAL-BUGS-AND-FIXES.md** - understand current visual bugs
2. Read relevant spec file (e.g., `character-basics.md`)
3. Identify "Must Have" acceptance criteria
4. Verify implementation matches spec
5. **CRITICAL**: Run examples and visually verify PNG output (tests passing ≠ visual correctness)
6. Update IMPLEMENTATION_PLAN.md with findings

### For Human Developers

1. Start with `getting-started.md` to understand basic workflow
2. Read `working-examples.md` for runnable code
3. Refer to specific specs (character, bubbles, etc.) for details
4. Use acceptance criteria as test checklist
5. Use examples as templates for your own comics

## Testing Against Specs

**⚠️ CRITICAL**: Tests passing does NOT mean visual output is correct. You MUST validate PNG files visually.

Each spec includes "Test Requirements" section. To validate:

```bash
# 1. Run all tests (these pass but don't validate visual quality)
uv run pytest

# 2. Run specific category
uv run pytest tests/test_character.py
uv run pytest tests/test_bubble.py
uv run pytest tests/test_renderer.py

# 3. Run examples (MOST IMPORTANT)
uv run python examples/01_simple_dialogue.py

# 4. MANDATORY: Visually check PNG output
# - Open examples/output/01_simple_dialogue.png
# - Verify characters are complete (not just heads)
# - Verify bubbles have borders and don't overlap
# - Verify layout is correct (panels positioned properly)

# See CRITICAL-BUGS-AND-FIXES.md for known visual issues
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

**Version**: 0.1.61 (as of 2026-01-18)
**Last Updated**: 2026-01-18
**Maintainer**: Claude Code Ralph Agent

**⚠️ KNOWN ISSUES**: Visual bugs exist despite tests passing. See [CRITICAL-BUGS-AND-FIXES.md](CRITICAL-BUGS-AND-FIXES.md) for P0/P1 priority fixes.
