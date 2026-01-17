# Interactive HTML Export

## What

Export comic pages and multi-page books to standalone, interactive HTML files with zoom, pan, themes, and keyboard navigation.

## Why

Static image exports (PNG, PDF) work well for printing and simple viewing, but modern web delivery requires interactivity. Interactive HTML export enables:

1. **Web publishing**: Easily share comics online without server infrastructure
2. **Responsive viewing**: Readers can zoom and pan to see details on any device
3. **Accessibility**: Dark/light themes accommodate different viewing preferences
4. **Book navigation**: Multi-page comics work seamlessly in a single file
5. **Mobile support**: Touch gestures work naturally on phones and tablets

## Acceptance Criteria

### Must Have
- [x] HTMLRenderer class that wraps SVGRenderer for content generation
- [x] Single-page HTML export with `render(output_path)` method
- [x] Multi-page book export with `render_book(book, output_path)` method
- [x] Embedded SVG content for crisp scaling at any zoom level
- [x] Zoom controls: mouse wheel, +/- buttons, keyboard shortcuts (+, -, 0)
- [x] Pan functionality: mouse drag, touch swipe
- [x] Theme toggle: dark/light modes with T keyboard shortcut
- [x] Fullscreen mode with F keyboard shortcut
- [x] Page navigation for books: arrow keys, prev/next buttons

### Should Have
- [x] Configurable feature toggles (enable_zoom, enable_pan, etc.)
- [x] Configurable zoom range (min_zoom, max_zoom)
- [x] Initial theme selection (light or dark)
- [x] Custom title for HTML document
- [x] Hover effects on panels
- [x] Page indicator showing current/total pages
- [x] Status bar with zoom level and usage instructions
- [x] Touch support for mobile (pinch zoom, swipe navigation)
- [x] Smooth animations for zoom transitions
- [x] Responsive design for different screen sizes

### Won't Have (This Iteration)
- [ ] WebSocket-based live reload (use preview server instead)
- [ ] Offline service worker caching
- [ ] Custom CSS theme injection
- [ ] Export to web components

## Context

### User Flow

1. Create Page or Book with content
2. Call `page.render("output.html")` or use HTMLRenderer directly
3. Open resulting HTML file in any modern browser
4. Interact with zoom, pan, and theme controls
5. Share the single HTML file - no dependencies needed

### Technical Architecture

HTMLRenderer builds on SVGRenderer:
1. Calls `page.build()` and `page.auto_layout()` to prepare content
2. Uses SVGRenderer to generate SVG string content
3. Wraps SVG in HTML document with embedded CSS (~500 lines) and JavaScript (~300 lines)
4. All assets are embedded - no external dependencies

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| + / = | Zoom in |
| - | Zoom out |
| 0 | Fit to screen |
| T | Toggle dark/light theme |
| F | Toggle fullscreen |
| ← | Previous page (book mode) |
| → | Next page (book mode) |
| Home | First page (book mode) |
| End | Last page (book mode) |

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| title | str | "Comic" | HTML document title |
| theme | str | "light" | Initial theme ("light" or "dark") |
| enable_zoom | bool | True | Enable zoom functionality |
| enable_pan | bool | True | Enable pan functionality |
| enable_hover | bool | True | Enable panel hover effects |
| enable_fullscreen | bool | True | Enable fullscreen mode |
| min_zoom | float | 0.5 | Minimum zoom level |
| max_zoom | float | 4.0 | Maximum zoom level |

## Examples

### Example 1: Simple HTML Export

```python
from comix import Page, Panel, Stickman

page = Page(width=800, height=400)
page.set_layout(rows=1, cols=2)

panel1 = Panel(width=360, height=360)
alice = Stickman(name="Alice", height=80)
alice.move_to((180, 200))
bubble = alice.say("Try zooming!")
panel1.add_content(alice, bubble)
page.add(panel1)

# Export to HTML with all interactive features
page.render("comic.html", title="My Interactive Comic")
```

### Example 2: Dark Theme Export

```python
from comix import Page, Panel, Stickman

page = Page(width=600, height=600)
panel = Panel(width=550, height=550)
char = Stickman(name="Night Owl", height=100)
char.move_to((275, 300))
bubble = char.say("Dark theme!")
panel.add_content(char, bubble)
page.add(panel)

# Export with dark theme
page.render("dark_comic.html", title="Dark Mode Comic", theme="dark")
```

### Example 3: Multi-Page Book

```python
from comix import Page, Panel, Stickman, TwoByTwo, Book, HTMLRenderer

page1 = TwoByTwo(width=800, height=800)
# ... add content to page1 panels

page2 = Page(width=800, height=600)
# ... add content to page2

book = Book(title="My Comic Book")
book.add_page(page1)
book.add_page(page2)

# Export book with navigation
renderer = HTMLRenderer(title="My Adventure")
renderer.render_book(book, "book.html")
```

### Example 4: Minimal UI (No Controls)

```python
from comix import Page, Panel, Stickman

page = Page(width=500, height=400)
# ... add content

# Export with minimal UI
page.render(
    "minimal.html",
    title="Clean Comic",
    enable_zoom=False,
    enable_pan=False,
    enable_fullscreen=False,
)
```

### Example 5: Using HTMLRenderer Directly

```python
from comix import Page, HTMLRenderer

page = Page(width=800, height=600)
# ... add content

# Use HTMLRenderer for more control
renderer = HTMLRenderer(
    page=page,
    title="Custom Comic",
    theme="dark",
    min_zoom=0.25,
    max_zoom=8.0,
)

# Get HTML as string
html_string = renderer.render_to_string()

# Or save to file
renderer.render("custom.html")
```

## Related Specs

- [Page Rendering](page-rendering.md) - Core rendering concepts
- [Preview Server](preview-server.md) - Live development workflow

## Test Requirements

1. **HTMLRenderer Initialization**:
   - Test: Default values for all options
   - Test: Custom configuration via constructor
   - Test: Theme validation (light/dark)

2. **Single Page Rendering**:
   - Test: render() creates valid HTML file
   - Test: render_to_string() returns HTML content
   - Test: SVG content is properly embedded
   - Test: Error when page is None

3. **Book Rendering**:
   - Test: render_book() handles multiple pages
   - Test: Navigation controls appear in book mode
   - Test: Page count and indicator correct

4. **Feature Toggles**:
   - Test: enable_zoom=False hides zoom controls
   - Test: enable_fullscreen=False hides fullscreen button
   - Test: Disabled features not in JavaScript config

5. **HTML Output Validity**:
   - Test: Output is valid HTML5
   - Test: CSS and JavaScript properly embedded
   - Test: Title properly escaped
   - Test: Theme class applied to body

## Implementation Status

Fully implemented in `/comix/renderer/html_renderer.py` with tests in `/tests/test_html_renderer.py`.

Working example: `/examples/11_html_export.py` generates 4 HTML variants demonstrating all features.
