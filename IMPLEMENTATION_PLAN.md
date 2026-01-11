# Implementation Plan

## Completed: Phase 1 - Core (MVP)

All Phase 1 items have been implemented and tested (92 tests passing):

- [x] CObject base class with transformation methods (move_to, shift, scale, rotate, hierarchy)
- [x] Panel class with borders and backgrounds
- [x] Bubble base class with speech variants (SpeechBubble, ThoughtBubble, ShoutBubble, WhisperBubble, NarratorBubble)
- [x] Text and StyledText classes including SFX for sound effects
- [x] Character base class with Stickman and SimpleFace implementations
- [x] Expression and Pose systems for character states
- [x] Page class (Scene equivalent) with layout support
- [x] SinglePanel and Strip convenience classes
- [x] GridLayout for panel arrangement
- [x] SVG Renderer with full element support
- [x] Basic CLI with render and preview commands
- [x] Utility modules (bezier curves, geometry transforms)
- [x] Style system with presets (manga, webtoon, comic, minimal)

## Completed: Phase 2 - Styling Enhancements

All Phase 2 items have been implemented and tested (180 tests passing):

- [x] Font management with fonttools
  - FontInfo, FontMetrics dataclasses
  - FontRegistry for font discovery and management
  - System font detection (macOS, Linux, Windows)
  - Font fallback chains
  - Text width/height estimation
- [x] Custom bubble shapes
  - Per-corner radius customization (corner_radii parameter)
  - Enhanced wobble with modes ("random", "wave")
  - Emphasis effect (shadow + thicker border)
- [x] Enhanced style inheritance
  - Style attached to CObject base class
  - get_effective_style() for cascade resolution
  - apply_style() method on Bubble and Text classes
  - Parent-to-child style inheritance
- [x] Theme system for consistent styling
  - ColorPalette for coordinated colors
  - Theme class with element-specific styles
  - ThemeRegistry for theme management
  - Built-in themes (manga, webtoon, comic, minimal)
  - Global theme functions (get_theme, set_default_theme, etc.)

## Completed: Phase 3 - Layout Engine

All Phase 3 items have been implemented and tested (220 tests passing):

- [x] FlowLayout for automatic positioning
  - Horizontal and vertical flow directions
  - Wrap and nowrap modes
  - Main axis alignment (start, center, end)
  - Cross axis alignment (start, center, end)
  - Respects individual object dimensions
  - Offset support for margin handling
- [x] Auto bubble positioning relative to characters
  - Enhanced attach_to() with 8 anchor positions (top, top-left, top-right, left, right, bottom, bottom-left, bottom-right)
  - Configurable buffer distance
  - Collision detection with overlaps_with() method
  - auto_attach_to() for intelligent position selection avoiding collisions
  - auto_position_bubbles() utility for positioning multiple bubbles
  - Boundary constraint support
  - Preferred anchor order customization
- [x] Page integration with set_flow_layout() method

## Completed: Phase 4 - Extensions

All Phase 4 items have been implemented and tested (451 tests passing):
- [x] Cairo renderer for PNG/PDF output (250 tests passing)
  - Full CairoRenderer class with PNG and PDF support
  - Quality settings (low=72 DPI, medium=150 DPI, high=300 DPI)
  - Renders all element types: Panel, Bubble, Text, Character, Shapes
  - Page.render() integration with format="png" and format="pdf"
  - 30 comprehensive tests for Cairo rendering
- [x] Effect system for webtoons
  - Effect base class with position, intensity, color, opacity, z_index
  - ShakeEffect: visual tremor with ghost copies and motion blur lines
  - ZoomEffect: radial speed lines for emphasis
  - MotionLines: parallel speed lines for movement direction
  - FocusLines: manga-style dramatic focus lines with optional fill
  - ImpactEffect: burst patterns for collisions and impacts
  - Page.add_effect() and Page.remove_effect() methods
  - SVG and Cairo renderer integration
  - 55 comprehensive tests for Effect system
- [x] Markup parser for DSL-based comic creation (347 tests passing)
  - MarkupParser class with regex-based parsing
  - Supports page layout: `[page 2x2]`
  - Panel markers: `# panel 1`
  - Character dialogue: `Character(position, expression): "text"`
  - Sound effects: `sfx: BOOM`
  - Narrator boxes: `narrator: "text"`
  - Background directives: `[background: description]`
  - Korean character names and dialogue support
  - Multiple bubble types: speech, thought, shout, whisper
  - Automatic Page object generation with panels, characters, and bubbles
  - 42 comprehensive tests for parser
- [x] AI image integration (OpenAI/Replicate) (390 tests passing)
  - Image base class for displaying images from files, URLs, or base64 data
  - AIImage class for AI-generated images via OpenAI DALL-E or Replicate
  - Supports async generation with generate_async() and sync with generate()
  - Multiple fit modes: contain, cover, fill, none
  - Aspect ratio preservation
  - SVG and Cairo renderer support for Image/AIImage
  - Placeholder rendering when no image data available
  - 43 comprehensive tests for image module

- [x] Web preview with hot reload
  - PreviewServer class with HTTP server and file watching
  - ScriptLoader for dynamic script reloading
  - HTML wrapper with auto-refresh JavaScript using long-polling
  - `comix serve script.py` CLI command
  - Watchdog integration for file change detection
  - Fallback to polling when watchdog is not available
  - Auto port selection when port is busy
  - 27 comprehensive tests for preview module
- [x] Constraint-based layouts (451 tests passing)
  - ConstraintLayout class for declarative positioning
  - ConstraintValue with arithmetic operations (+, -, *, /)
  - ElementRef for referencing container and element edges
  - Support for left, right, top, bottom, width, height, center_x, center_y constraints
  - Cross-element references (position relative to other elements)
  - Proportional constraints (e.g., width = container_width * 0.5)
  - Iterative constraint solver with dependency resolution
  - Priority levels (REQUIRED, HIGH, MEDIUM, LOW)
  - Method chaining API
  - 34 comprehensive tests for constraint system

## Technical Notes

- Using Manim-inspired architecture with method chaining
- NumPy for coordinate calculations
- SVG as primary output format, PNG/PDF via Cairo
- fonttools for font metrics
- pycairo for PNG/PDF rendering
- watchdog for file watching (optional)
- All tests passing (451/451) with no deprecation warnings
- Mypy type checking passing (0 errors)
- Python 3.13 required
- Uses asyncio.run() for async-to-sync bridging (Python 3.7+ compatible)

## API Changes (Phase 3)

### FlowLayout class (new)
- `FlowLayout(width, height, direction, spacing, wrap, alignment, cross_alignment, offset_x, offset_y)`
- `calculate_positions(num_cells)` - GridLayout-compatible interface
- `calculate_positions_for_objects(objects)` - Respects object dimensions

### Page class
- Added `set_flow_layout(direction, spacing, wrap, alignment, cross_alignment)` method
- `auto_layout()` now works with both GridLayout and FlowLayout

### Bubble class
- Enhanced `attach_to(character, anchor, buffer)` with 8 anchor positions
- Added `overlaps_with(other, margin)` for collision detection
- Added `auto_attach_to(character, avoid_bubbles, bounds, preferred_anchors, buffer)` for intelligent positioning

### New functions
- `auto_position_bubbles(character_bubble_pairs, bounds, buffer)` - Position multiple bubbles avoiding collisions

### Exports
- `FlowLayout` and `GridLayout` now exported from main package
- `auto_position_bubbles` exported from main package

## API Changes (Phase 2)

### Bubble class
- Renamed `style` parameter to `bubble_type` to avoid conflict with Style object
- Added `corner_radii: tuple[float, float, float, float] | None` for per-corner radius
- Added `wobble_mode: str` ("random" or "wave")
- `emphasis: bool` now renders shadow + thicker border

### CObject base class
- Added `style: Style | None` parameter to constructor
- Added `set_style()`, `get_style()`, `get_effective_style()`, `apply_style()` methods
- Style included in `get_render_data()` when set

### New modules
- `comix/style/font.py` - Font management system
- `comix/style/theme.py` - Theme system
- `comix/layout/flow.py` - FlowLayout system

## API Changes (Phase 4)

### CairoRenderer class (new)
- `CairoRenderer(page: Page)` - Initialize with a Page
- `render(output_path, format, quality)` - Render to PNG or PDF
  - `format`: "png" or "pdf" (auto-detected from extension)
  - `quality`: "low" (72 DPI), "medium" (150 DPI), "high" (300 DPI)

### Page class
- `render(output_path, format, quality)` now supports "png" and "pdf" formats
- Quality parameter passed through to CairoRenderer

### Dependencies
- Optional `cairo` extras: `uv sync --extra cairo`
- Requires pycairo>=1.26.0, Pillow>=10.0.0

### New module
- `comix/renderer/cairo_renderer.py` - Cairo-based PNG/PDF rendering

### Effect system (new)

#### Effect base class
- `Effect(target, position, z_index, intensity, color, opacity, seed)` - Base class for effects
- `set_position(position)` - Set effect position
- `set_target(target)` - Set target CObject
- `set_intensity(intensity)` - Set effect intensity (0-1)
- `set_color(color)` - Set effect color
- `set_opacity(opacity)` - Set effect opacity
- `get_elements()` - Get generated EffectElements
- `get_render_data()` - Get render data for renderers

#### ShakeEffect
- `ShakeEffect(target, position, shake_distance, num_copies, direction)` - Visual tremor effect
- `direction`: "horizontal", "vertical", or "both"
- Generates ghost copies and motion blur lines

#### ZoomEffect
- `ZoomEffect(target, position, num_lines, inner_radius, outer_radius)` - Radial zoom/emphasis
- Generates radial speed lines converging on target

#### MotionLines
- `MotionLines(target, position, direction, num_lines, line_length, spread, taper)` - Speed lines
- `set_direction(radians)` or `set_direction_degrees(degrees)` - Set motion direction
- Generates parallel lines indicating movement

#### FocusLines
- `FocusLines(target, position, num_lines, inner_gap, outer_radius, fill_background)` - Dramatic focus
- `set_fill_background(fill, color)` - Enable alternating fill pattern
- Manga-style converging lines

#### ImpactEffect
- `ImpactEffect(target, position, num_spikes, inner_radius, outer_radius, fill_center)` - Impact burst
- Star burst pattern with debris lines

#### Page class additions
- `add_effect(*effects)` - Add effects to page
- `remove_effect(*effects)` - Remove effects from page
- `get_effects()` - Get all effects on page

#### Exports
- All effect classes exported from main `comix` package
- Also available from `comix.effect` module

### New module
- `comix/effect/effect.py` - Effect system implementation

### Markup Parser (new)

#### parse_markup function
- `parse_markup(markup: str) -> Page` - Parse markup text and return a Page object

#### MarkupParser class
- `MarkupParser(text: str)` - Initialize with markup text
- `parse() -> PageSpec` - Parse and return structured specification
- `to_page() -> Page` - Parse and convert to Page object

#### Markup Language Syntax

```
[page RxC]                           # Page with grid layout (rows x cols)
[page RxC WxH]                       # Page with custom size (width x height)

# panel N                            # Panel marker

Character(position, expression): "text"  # Character dialogue
Character(thought): "text"           # Thought bubble
Character(shout): "text"             # Shout bubble
Character(whisper): "text"           # Whisper bubble

sfx: TEXT                            # Sound effect
narrator: "text"                     # Narrator box
[background: description]            # Background directive

// comment                           # Line comment (ignored)
```

#### Supported Modifiers
- Expressions: neutral, happy, sad, angry, surprised, confused, smug
- Positions: left, right, center, closeup, top, bottom
- Directions: left, right, front, back
- Bubble types: speech, thought, think, shout, whisper

#### Exports
- `parse_markup`, `MarkupParser`, `ParseError` exported from main `comix` package
- Also available from `comix.parser` module

### New module
- `comix/parser/parser.py` - Markup parser implementation

### Image system (new)

#### Image class
- `Image(source, width, height, preserve_aspect_ratio, fit)` - Display images in comics
- `set_source(source)` - Set image source (file path, URL, or data URI)
- `set_size(width, height)` - Set display dimensions
- `set_fit(fit)` - Set fit mode ("contain", "cover", "fill", "none")
- `load_from_file(path)` - Load image from file with auto MIME detection
- `set_base64_data(data, mime_type)` - Set image from base64 data
- `get_base64_data()` - Get base64-encoded image data
- `get_data_uri()` - Get complete data URI

#### AIImage class
- `AIImage(prompt, provider, model, width, height, quality, style, negative_prompt, seed)` - AI-generated images
- `set_prompt(prompt)` - Set generation prompt
- `set_provider(provider)` - Set AI provider (AIProvider.OPENAI or AIProvider.REPLICATE)
- `set_model(model)` - Set specific model
- `generate()` - Synchronous image generation
- `generate_async()` - Asynchronous image generation
- `get_generation_metadata()` - Get metadata about the generation

#### AIProvider enum
- `AIProvider.OPENAI` - OpenAI DALL-E provider
- `AIProvider.REPLICATE` - Replicate API provider

#### Dependencies
- Optional `ai` extras: `uv sync --extra ai`
- Requires openai>=1.0.0, replicate>=0.5.0

#### Exports
- `Image`, `AIImage`, `AIProvider`, `AIImageError` exported from main `comix` package
- Also available from `comix.cobject.image` module

### New module
- `comix/cobject/image/image.py` - Image CObject implementation
- `comix/cobject/image/ai_image.py` - AIImage with OpenAI/Replicate support

### Web Preview (new)

#### PreviewServer class
- `PreviewServer(script_path, port, host, open_browser, use_watchdog)` - Live preview server
- `start(blocking)` - Start the server
- `stop()` - Stop the server

#### ScriptLoader class
- `ScriptLoader(script_path)` - Loads and reloads comic scripts
- `load_page()` - Load Page from script
- `render_svg()` - Render page to SVG string
- `get_version()` - Get current render version
- `has_file_changed()` - Check if script file changed

#### serve function
- `serve(script_path, port, host, open_browser)` - Convenience function to start preview server

#### CLI Command
- `comix serve script.py` - Start live preview server with hot reload
  - `-p, --port`: Port to run the server on (default: 8000)
  - `-H, --host`: Host to bind to (default: localhost)
  - `--no-browser`: Don't open browser automatically

#### Dependencies
- Optional `web` extras: `uv sync --extra web`
- Requires watchdog>=4.0.0

#### Exports
- `PreviewServer`, `PreviewError`, `preview_serve` exported from main `comix` package (when watchdog is available)
- Also available from `comix.preview` module

### New module
- `comix/preview/server.py` - Web preview server implementation

### Constraint Layout (new)

#### ConstraintLayout class
- `ConstraintLayout(width, height, offset_x, offset_y)` - Initialize constraint layout
- `add(element, name, left, right, top, bottom, width, height, center_x, center_y, priority)` - Add element with constraints
- `constrain(element, property_name, value, priority)` - Add constraint to existing element
- `ref(element)` - Get ElementRef for building constraints
- `solve()` - Solve constraints and return positions
- `apply()` - Solve and apply positions to elements
- `get_position(element)` - Get resolved position for element
- `calculate_positions(num_cells)` - GridLayout/FlowLayout compatibility

#### Container edge properties
- `layout.left`, `layout.right`, `layout.top`, `layout.bottom` - Container edges
- `layout.center_x`, `layout.center_y` - Container center
- `layout.container_width`, `layout.container_height` - Container dimensions

#### ConstraintValue arithmetic
- Supports `+`, `-`, `*`, `/` operations
- Example: `layout.container_width * 0.5 - 20`

#### ElementRef class
- Properties: `left`, `right`, `top`, `bottom`, `center_x`, `center_y`, `width`, `height`
- Use with `layout.ref(element)` for cross-element constraints

#### ConstraintPriority enum
- `REQUIRED` - Must be satisfied
- `HIGH` - Strong preference
- `MEDIUM` - Normal preference
- `LOW` - Weak preference

#### Exports
- `ConstraintLayout`, `ConstraintPriority` exported from main `comix` package
- Also available from `comix.layout` module

### New module
- `comix/layout/constraints.py` - Constraint-based layout system

## Completed: Package Export Improvements

Added missing exports to main `comix` package for better usability:

### Panel Classes (new exports)
- `Border` - Border style dataclass for panels (color, width, style, radius)

### Character Classes (new exports)
- `Expression` - Character expression definition with presets (neutral, happy, sad, angry, surprised, confused)
- `Pose` - Character pose definition with presets (standing, sitting, walking, running, pointing, waving)

### Shape Classes (new exports)
- `Rectangle` - Rectangle shape with configurable size, fill, stroke, corner radius
- `Circle` - Circle shape with configurable radius, fill, stroke
- `Line` - Line segment with start/end points, stroke styling

### Style System (new exports)
- `Style` - CSS-like style definition dataclass
- `MANGA_STYLE`, `WEBTOON_STYLE`, `COMIC_STYLE`, `MINIMAL_STYLE` - Preset styles

### Theme System (new exports)
- `Theme` - Global theming definition
- `ColorPalette` - Coordinated color definitions
- `ThemeRegistry` - Theme management class
- `MANGA_THEME`, `WEBTOON_THEME`, `COMIC_THEME`, `MINIMAL_THEME` - Preset themes
- `get_theme()`, `get_default_theme()`, `set_default_theme()`, `register_theme()`, `get_theme_registry()` - Global theme functions

All classes were already implemented but not exported from the main package. Now users can import directly:
```python
from comix import (
    Border, Expression, Pose,
    Rectangle, Circle, Line,
    Style, Theme, MANGA_STYLE, MANGA_THEME,
)
```

### Geometry Utilities (new exports)
- `distance` - Calculate distance between two points
- `midpoint` - Calculate midpoint between two points
- `bounding_box` - Calculate bounding box of points
- `normalize_angle` - Normalize angle to [-π, π] range
- `angle_between` - Calculate angle from one point to another
- `rotate_point` - Rotate a single point around a center
- `rotate_points` - Rotate multiple points around a center
- `translate_points` - Translate points by an offset
- `scale_points` - Scale points around a center

### Bezier Utilities (new exports)
- `create_bubble_path` - Generate SVG path data for bubble shapes
- `create_tail_points` - Generate points for bubble tail connectors

### Font System (new exports)
- `FontInfo` - Font information dataclass
- `FontMetrics` - Font metrics for text measurement
- `FontRegistry` - Registry for font discovery and management
- `get_font_registry()` - Access the global font registry
- `estimate_text_width()` - Estimate text width for given font
- `estimate_text_height()` - Estimate text height for given font

### Renderer Classes (new exports)
- `SVGRenderer` - SVG output renderer (always available)
- `CairoRenderer` - PNG/PDF output renderer (optional, requires pycairo)

### Constraint Layout Utilities (new exports)
- `ConstraintValue` - Constraint value with arithmetic operations (+, -, *, /)
- `ElementRef` - Reference to element edges for cross-element constraints

Users can now import these utilities directly:
```python
from comix import (
    distance, midpoint, bounding_box,
    FontRegistry, estimate_text_width,
    SVGRenderer, CairoRenderer,
    ConstraintValue, ElementRef,
)
```
