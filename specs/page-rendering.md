# Page Rendering - Exporting Comics to PNG and PDF

## What
A rendering system that exports completed comic pages to PNG and PDF formats with configurable quality settings.

## Why
The final output of comic creation is a viewable/printable file. Developers need:
- PNG for web sharing and quick previews
- PDF for print-quality output and multi-page documents
- Fast preview mode for development iteration
- High-quality mode for final production

Without working rendering, all the comic creation work produces no usable output.

## Acceptance Criteria

### Must Have
- [x] `page.render("output.png")` creates PNG file with visible comic content
- [x] `page.render("output.pdf", format="pdf")` creates PDF file (requires pycairo)
- [x] PNG rendering works without pycairo (SVG fallback)
- [x] Rendered output matches specified page dimensions (width x height)
- [x] Rendered output includes all panels, characters, bubbles, and text
- [x] SVG renderer always available as baseline
- [x] Clear error if pycairo not installed when PDF requested
- [x] File overwrites existing file at same path

### Should Have
- [x] Quality parameter: "low", "medium" (default), "high"
- [x] Low quality renders faster (72 DPI, simplified)
- [x] High quality renders slower (300 DPI, full detail)
- [x] DPI parameter can be explicitly set for PNG output
- [x] Multi-page PDF support via Book class
- [x] Progress callback for long-running renders
- [x] Render returns path to created file

### Won't Have (This Iteration)
- [x] ~~Animated GIF output~~ → Now available via [Animation Export](animation-export.md)
- [x] ~~HTML/Canvas output~~ → Now available via [HTML Export](html-export.md)
- [ ] Streaming/progressive rendering
- [ ] Render to clipboard
- [ ] Background/async rendering

## Context

### User Flow (PNG Rendering)

1. Developer creates and composes page (panels, characters, bubbles)
2. Developer calls `output_path = page.render("comic.png")`
3. System:
   - Calls `page.build()` if not already built
   - Calls `page.auto_layout()` to position panels
   - Collects all CObjects from page hierarchy
   - Initializes SVG or Cairo renderer
   - Renders background
   - Renders each panel (border, background)
   - Renders each panel's content (characters, bubbles, text)
   - Writes PNG file to specified path
4. Returns absolute path to created file
5. Developer opens PNG to verify output

### User Flow (PDF Rendering)

1. Developer creates page
2. Developer calls `page.render("comic.pdf", format="pdf", quality="high")`
3. System checks for pycairo availability
4. If available: Renders via Cairo to PDF
5. If not available: Raises ImportError with helpful message
6. Returns path to created PDF

### User Flow (Multi-Page PDF)

```python
from comix import Book, Page

book = Book()
book.add_page(page1)
book.add_page(page2)
book.render("multi_page.pdf")
```

### Edge Cases

- **Empty page (no panels)**: Render blank page with background color
- **Panel outside bounds**: Clip to page boundaries or allow overflow (configurable)
- **Very large page (10000x10000)**: Warn about memory usage, render anyway
- **Invalid file path**: Raise IOError with clear message about path problem
- **pycairo not installed + PDF requested**: Raise ImportError with installation instructions
- **Disk full during write**: Raise OSError with clear message
- **File permissions prevent write**: Raise PermissionError with path info
- **Render called multiple times**: Each call overwrites previous file
- **Font missing during render**: Fall back to system font, log warning

### Technical Constraints

- SVG rendering must work without external dependencies (beyond numpy/fonttools)
- Cairo rendering requires pycairo optional dependency
- Must handle coordinate system correctly (origin top-left vs bottom-left)
- Must render in correct z-index order (background → panels → content)
- Must support both file paths and file-like objects
- DPI affects PNG pixel dimensions: pixels = points * (DPI / 72)

### Performance Targets

Based on user preference "fast preview + slow final":

- **Preview mode** (quality="low", DPI=72):
  - Simple 2-panel comic: < 1 second
  - Complex page (10 panels): < 3 seconds

- **Production mode** (quality="high", DPI=300):
  - Simple 2-panel comic: < 5 seconds
  - Complex page (10 panels): < 15 seconds
  - Multi-page PDF (10 pages): < 60 seconds

### Related Specs

- `getting-started.md` (basic rendering workflow)
- `page-layouts.md` (page composition before rendering)

## Examples

### Example 1: Basic PNG Rendering

```python
from comix import Page, Panel, Stickman

page = Page(width=800, height=600)
panel = Panel()
char = Stickman(height=100)
char.move_to((400, 300))
bubble = char.say("Hello!")

panel.add_content(char, bubble)
page.add(panel)
page.auto_layout()

output_path = page.render("my_comic.png")
print(f"Comic saved to: {output_path}")
# Output: Comic saved to: /full/path/to/my_comic.png
```

**Expected Result**: PNG file at specified path showing complete comic.

### Example 2: High-Quality PDF

```python
from comix import Page, Panel, Stickman

page = Page(width=800, height=1200)
# ... compose page ...

output_path = page.render(
    "print_comic.pdf",
    format="pdf",
    quality="high"
)
# Renders at 300 DPI for print quality
```

**Expected Result**: High-resolution PDF suitable for printing.

### Example 3: Custom DPI

```python
from comix import Page

page = Page()
# ... compose page ...

# Web-optimized PNG
page.render("web.png", dpi=96, quality="low")

# Print-optimized PNG
page.render("print.png", dpi=300, quality="high")
```

**Expected Result**: Two PNG files with different resolutions.

### Example 4: Multi-Page PDF

```python
from comix import Book, Page

book = Book()

for i in range(5):
    page = Page()
    # ... create page content ...
    book.add_page(page)

book.render("chapter1.pdf", quality="high")
```

**Expected Result**: Single PDF file with 5 pages.

### Example 5: Error Handling

```python
from comix import Page

page = Page()

# Try PDF without pycairo
try:
    page.render("output.pdf", format="pdf")
except ImportError as e:
    print(f"PDF rendering requires pycairo: {e}")
    # Fallback to PNG
    page.render("output.png")

# Invalid path
try:
    page.render("/nonexistent/directory/output.png")
except IOError as e:
    print(f"Cannot write file: {e}")
```

**Expected Result**: Clear error messages guide user to solutions.

### Example 6: SVG Output (Always Available)

```python
from comix import Page

page = Page()
# ... compose page ...

# SVG is text-based vector format
page.render("comic.svg", format="svg")
# Works without pycairo, produces scalable output
```

**Expected Result**: SVG file that can be opened in browsers or vector editors.

## Open Questions

- [x] Should render() create parent directories? **Decision**: No, fail fast
- [x] Should there be a quick `page.show()` method? **Decision**: Yes, opens SVG in browser for development
- [x] Default DPI for PNG? **Decision**: 150 (balance of quality and file size)
- [x] Should quality setting affect DPI or other parameters? **Decision**: Both DPI and rendering detail
- [ ] Should we support rendering specific panels only? **Decision needed** (defer to future)

## Test Requirements

1. **PNG rendering**:
   - Test: Output file exists at specified path
   - Test: PNG file has correct dimensions
   - Test: PNG contains visible content (not blank/white)

2. **PDF rendering**:
   - Test: PDF file created when pycairo available
   - Test: ImportError raised when pycairo not available
   - Test: PDF is valid (can be opened by PDF readers)

3. **SVG rendering**:
   - Test: SVG file created (always works)
   - Test: SVG contains expected elements (rect, circle, text, path)
   - Test: SVG can be opened in browsers

4. **Quality settings**:
   - Test: Low quality renders faster than high quality
   - Test: High quality produces larger file size
   - Test: DPI affects PNG pixel dimensions

5. **Error handling**:
   - Test: Invalid path raises IOError
   - Test: PDF without pycairo raises ImportError with helpful message

6. **Multi-page**:
   - Test: Book.render() creates multi-page PDF
   - Test: Each page in PDF has correct content

## Implementation Notes

All rendering features are working correctly. Multi-page PDF rendering with characters and bubbles has been verified through example 06_multi_page_pdf.py which produces a valid 3-page PDF with full content.

## Success Metrics

**This spec is successful when:**
1. `page.render("test.png")` produces PNG with all visible content
2. Characters are fully rendered (not just heads)
3. Speech bubbles are visible with borders
4. PDF rendering works when pycairo installed
5. SVG rendering always works as fallback
6. Error messages are helpful when things go wrong
