# Comix Specifications

This directory contains specifications for the Comix comic creation library, written in the Ralph Wiggum methodology (JTBD → Spec format).

## Overview

Comix is a Python library for creating comics programmatically, inspired by Manim's API design but focused on comic/manga creation instead of mathematical animations.

**Current Goal**: Enable developers to create simple comics with stick figures and speech bubbles.

## Active Specs

### Core Workflows

- [Getting Started](getting-started.md) - Creating your first comic (2-panel dialogue)
- [Character Basics](character-basics.md) - Creating and positioning stick figure characters
- [Speech Bubbles](speech-bubbles.md) - Adding dialogue with automatic bubble attachment
- [Page Rendering](page-rendering.md) - Exporting comics to PNG and PDF formats
- [Working Examples](working-examples.md) - Runnable Python scripts demonstrating usage

### Architecture (Reference)

- [PRD.md](PRD.md) - Product Requirements Document with full architecture design

## Quick Status

| Spec | Status | Blocking Issues |
|------|--------|----------------|
| Getting Started | 🔴 Needs fixes | Characters render partially (head only), bubbles show text but no borders |
| Character Basics | 🔴 Needs fixes | `Stickman.generate_points()` incomplete - missing body/arms/legs |
| Speech Bubbles | 🔴 Needs fixes | Bubble border not rendering - only text appears |
| Page Rendering | 🟡 Partially working | Basic PNG works, but content incomplete due to above issues |
| Working Examples | 🔴 Not started | Blocked by core functionality fixes |

## Known Issues

Based on testing (test_simple.py):

1. **Stickman Partial Rendering**:
   - Only head (triangle/circle) renders
   - Body, arms, legs missing from output
   - Likely issue: `generate_points()` not creating all body part points
   - Impact: Characters appear incomplete

2. **Speech Bubble Missing Border**:
   - Text renders correctly
   - Bubble border (rounded rectangle) not visible
   - Bubble tail not visible
   - Likely issue: `create_bubble_path()` or renderer not drawing bubble shape
   - Impact: Dialogue appears as floating text without context

3. **Integration**:
   - Basic workflow executes without errors
   - `page.render()` creates PNG files
   - SVG/Cairo renderers functional but not rendering all elements
   - Layout system works

## Acceptance Criteria Flow

```
getting-started.md
    ├─> character-basics.md (depends on characters rendering completely)
    ├─> speech-bubbles.md (depends on bubbles rendering with borders)
    └─> page-rendering.md (depends on all above working)
         └─> working-examples.md (depends on page rendering working correctly)
```

All specs depend on two critical fixes:
1. Complete Stickman rendering (all body parts)
2. Complete SpeechBubble rendering (border + tail + text)

## Implementation Priority

To unblock the full workflow:

### P0: Critical Fixes (Blocker)

1. **Fix Stickman rendering** (character-basics.md):
   - Investigate `comix/cobject/character/character.py::Stickman.generate_points()`
   - Ensure head, body, arms, legs all generate point data
   - Verify SVG/Cairo renderers process all body part points
   - Add test: `test_stickman_complete_rendering()` verifies all parts present

2. **Fix SpeechBubble rendering** (speech-bubbles.md):
   - Investigate `comix/cobject/bubble/bubble.py::Bubble.generate_points()`
   - Investigate `comix/utils/bezier.py::create_bubble_path()`
   - Ensure bubble path (border) is generated
   - Ensure bubble tail is generated
   - Verify renderers draw bubble fill, stroke, and tail
   - Add test: `test_bubble_border_visible()` verifies border in output

### P1: Examples & Documentation

3. **Create working examples** (working-examples.md):
   - Create `examples/` directory
   - Implement 01-05 basic examples
   - Verify all examples execute and produce correct output
   - Write examples/README.md

### P2: Polish

4. **Error handling improvements**:
   - Add validation for common errors (missing fonts, invalid paths)
   - Improve error messages with actionable guidance
   - Add fallback behaviors where appropriate

5. **Performance optimization**:
   - Implement quality="low" for fast previews
   - Optimize rendering for common cases
   - Add progress callbacks for long renders

## How to Use These Specs

### For AI Agents (Ralph Loop)

1. Read relevant spec file (e.g., `character-basics.md`)
2. Identify "Must Have" acceptance criteria
3. Investigate existing code to find gaps
4. Implement missing functionality
5. Write tests that verify acceptance criteria
6. Validate against examples in spec

### For Human Developers

1. Start with `getting-started.md` to understand basic workflow
2. Read `working-examples.md` for runnable code
3. Refer to specific specs (character, bubbles, etc.) for details
4. Use acceptance criteria as test checklist
5. Use examples as templates for your own comics

## Testing Against Specs

Each spec includes "Test Requirements" section. To validate:

```bash
# Run all tests
uv run pytest

# Run specific category
uv run pytest tests/test_character.py
uv run pytest tests/test_bubble.py
uv run pytest tests/test_renderer.py

# Validate examples
uv run python examples/01_simple_dialogue.py
# Check examples/output/01_simple_dialogue.png visually
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

## Future Specs (Parking Lot)

Features not yet scoped:

- **Page Layouts** - Grid layouts, templates (FourKoma, Splash, etc.)
- **Parser/DSL** - Text-based markup for rapid comic creation
- **Effects** - Motion lines, impact effects, shake
- **Themes** - Manga, webtoon, comic book presets
- **AI Images** - Integration with DALL-E/Replicate
- **Advanced Characters** - SimpleFace, Robot, Chibi, etc.
- **Multi-Format Export** - SVG, HTML, animated GIF

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

**Version**: 0.0.63 (as of 2026-01-18)
**Last Updated**: 2026-01-18
**Maintainer**: Claude Code Ralph Agent
