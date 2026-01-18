# Panel Shapes - Professional Panel Division

## What
Advanced panel division system supporting non-rectangular panel shapes including diagonal, trapezoidal, and irregular panel layouts commonly used in professional manga and comics.

## Why
Traditional grid-based rectangular panels can feel monotonous and limiting. Professional comics use varied panel shapes to:
- Create visual dynamism and energy
- Express unstable moods, shock, or surprise
- Add dramatic impact to action sequences
- Break the visual rhythm for storytelling effect
- Guide reader's eye flow across the page

Without support for non-rectangular panels, the library cannot create authentic manga-style layouts or dynamic Western comic pages.

## Acceptance Criteria

### Must Have
- [x] Panel class supports custom polygon shapes (not just rectangles)
- [x] DiagonalPanel class with adjustable diagonal cut angle
- [x] TrapezoidPanel class with configurable top/bottom widths
- [x] IrregularPanel class accepting arbitrary polygon points
- [x] Panel borders render correctly along diagonal/irregular edges
- [x] Content (characters, bubbles) clipped to irregular panel boundaries
- [x] Z-index ordering works correctly for overlapping irregular panels

### Should Have
- [x] Helper functions to create common diagonal cuts (top-left, top-right, bottom-left, bottom-right)
- [x] `split_diagonal(angle, direction)` method to divide existing panel along diagonal
- [x] `split_curve(control_points)` for curved panel divisions
- [ ] Automatic gutter spacing calculations for non-rectangular panels
- [x] Visual validation that diagonal panels render correctly (via unit tests)

### Won't Have (This Iteration)
- [ ] Automatic content repositioning when panel shape changes
- [ ] Curved/wavy panel borders (bezier curves) → future enhancement
- [ ] Panel shapes with holes or multiple disconnected regions
- [ ] 3D perspective panel shapes

## Context

### User Flow (Diagonal Panel)

1. Developer wants to create dramatic diagonal panel layout
2. Developer calls `panel = DiagonalPanel(diagonal_angle=45, direction="top-left")`
3. System creates panel with one corner cut off diagonally
4. Developer adds content: `panel.add_content(character, bubble)`
5. Renderer clips content to diagonal boundary
6. Diagonal panel displays correctly in final output

### User Flow (Trapezoid Panel)

1. Developer needs panel that's wider at top, narrower at bottom
2. Developer calls `panel = TrapezoidPanel(top_width=300, bottom_width=200, height=400)`
3. System creates trapezoidal panel
4. Panel renders with diagonal sides connecting top and bottom edges

### User Flow (Irregular Panel)

1. Developer wants custom panel shape for special effect
2. Developer defines points: `points = [(0,0), (100,50), (200,0), (150,200), (50,200)]`
3. Developer calls `panel = IrregularPanel(points=points)`
4. System creates panel following exact point sequence
5. Content is clipped to custom shape

### Real-World Examples from Research

Based on web research findings:

**Manga Techniques:**
- Diagonal panels express unstable moods, shock, or surprise (MediBang tutorial)
- Characters deliberately placed in center of diagonal cuts for dramatic effect
- Multiple panels with diagonal divisions create visual variety and avoid monotony

**Dynamic Layouts:**
- Irregular panels (non-rectangular shapes) enhance expressiveness (academic research)
- Trapezoidal panels used in action sequences
- Diagonal layouts where panels don't follow vertical or horizontal divisions

**Western Comics:**
- TV Tropes "Odd-Shaped Panel" examples: splash pages, dramatic moments
- Panels can stretch across page height/width with diagonal boundaries
- Fourth-wall breaks often use irregular panel shapes

### Edge Cases

- **Diagonal panel too narrow**: Warn if diagonal cut leaves unusable panel area
- **Overlapping irregular panels**: Z-index determines drawing order
- **Content outside panel boundary**: Clip content to panel shape
- **Very complex polygon (100+ points)**: May slow rendering, warn user
- **Self-intersecting polygon**: Undefined behavior, validate and reject or auto-fix
- **Clockwise vs counter-clockwise point order**: Normalize to consistent winding
- **Panel with zero area**: Raise error
- **Diagonal angle = 0° or 90°**: Falls back to rectangular panel

### Technical Constraints

- SVG: Use `<clipPath>` with polygon for content clipping
- Cairo: Use `cairo_clip()` with polygon path
- HTML: Use CSS `clip-path: polygon(...)`
- Must calculate accurate bounding boxes for irregular shapes
- Panel positioning system must handle non-rectangular bounds
- Gutter spacing becomes complex with irregular shapes

### Related Specs

- `page-rendering.md` (rendering system must support clipping)
- `getting-started.md` (basic panel usage)
- `panel-templates.md` (future: templates using irregular panels)

## Examples

### Example 1: Diagonal Panel (Top-Left Cut)

```python
from comix import Page, DiagonalPanel, Stickman

page = Page(width=800, height=600)

# Create panel with top-left corner cut diagonally
panel = DiagonalPanel(
    width=400,
    height=400,
    diagonal_angle=45,  # degrees
    direction="top-left"
)
panel.move_to((400, 300))

char = Stickman(height=100)
char.move_to((400, 300))
bubble = char.say("Dramatic moment!")

panel.add_content(char, bubble)
page.add(panel)
page.render("diagonal_panel.png")
```

**Expected Visual**:
```
     /----\
    /      \
   |  O    |  <- Character with speech bubble
   | /|\   |
   | / \   |
   \________/
```

### Example 2: Trapezoid Panel for Action Scene

```python
from comix import Page, TrapezoidPanel, Superhero

page = Page(width=800, height=1200)

# Wide at top (explosion), narrow at bottom
panel = TrapezoidPanel(
    top_width=600,
    bottom_width=300,
    height=800
)
panel.move_to((400, 600))

hero = Superhero(height=200)
hero.move_to((400, 400))
hero.set_pose("flying")

panel.add_content(hero)
page.add(panel)
page.render("trapezoid_action.png")
```

**Expected Visual**:
```
 \___________/  <- Wide top
  \         /
   \       /
    \     /
     \   /      <- Narrow bottom
```

### Example 3: Irregular Panel for Speech Emphasis

```python
from comix import Page, IrregularPanel, Stickman

page = Page(width=800, height=600)

# Star-burst panel shape for shout
star_points = [
    (400, 100),   # top
    (450, 250),   # right-top
    (550, 300),   # right
    (450, 350),   # right-bottom
    (400, 500),   # bottom
    (350, 350),   # left-bottom
    (250, 300),   # left
    (350, 250),   # left-top
]

panel = IrregularPanel(points=star_points)

char = Stickman(height=80)
char.move_to((400, 300))
bubble = char.shout("WHAT?!")

panel.add_content(char, bubble)
page.add(panel)
page.render("irregular_shout.png")
```

**Expected Visual**: Starburst-shaped panel

### Example 4: Split Existing Panel Diagonally

```python
from comix import Page, Panel

page = Page(width=800, height=600)

# Start with rectangular panel
panel = Panel(width=400, height=400)

# Split diagonally to create two panels
top_left, bottom_right = panel.split_diagonal(
    angle=45,
    direction="top-left-to-bottom-right"
)

# Add content to each half
top_left.add_content(char1, bubble1)
bottom_right.add_content(char2, bubble2)

page.add(top_left, bottom_right)
page.render("split_diagonal.png")
```

**Expected Result**: Original panel split into two triangular panels

### Example 5: Manga-Style Diagonal Layout

```python
from comix import Page, DiagonalPanel, Panel, Stickman

page = Page(width=800, height=1200)

# Top panel: normal rectangle
panel1 = Panel(width=700, height=300)
panel1.move_to((400, 150))
char1 = Stickman(height=100)
char1.move_to((400, 150))
bubble1 = char1.say("Everything seems normal...")
panel1.add_content(char1, bubble1)

# Middle panel: diagonal cut for shock
panel2 = DiagonalPanel(
    width=700,
    height=400,
    diagonal_angle=30,
    direction="top-right"
)
panel2.move_to((400, 550))
char2 = Stickman(height=100, expression="shocked")
char2.move_to((400, 550))
bubble2 = char2.shout("WHAT?!")
panel2.add_content(char2, bubble2)

# Bottom panel: return to normal
panel3 = Panel(width=700, height=300)
panel3.move_to((400, 950))
char3 = Stickman(height=100)
char3.move_to((400, 950))
bubble3 = char3.say("Never mind...")
panel3.add_content(char3, bubble3)

page.add(panel1, panel2, panel3)
page.auto_layout()
page.render("manga_diagonal.png")
```

**Expected Result**: Three-panel sequence with middle panel diagonally cut to emphasize shock

## Implementation Notes

### Panel Class Extensions

```python
class Panel(CObject):
    def __init__(
        self,
        shape: str = "rectangle",  # "rectangle", "diagonal", "trapezoid", "polygon"
        points: list[tuple[float, float]] | None = None,
        diagonal_angle: float = 45,
        diagonal_direction: str = "top-left",
        **kwargs
    ):
        # Existing init
        self.shape = shape
        self.polygon_points = points
        self.diagonal_angle = diagonal_angle
        self.diagonal_direction = diagonal_direction
        # Generate shape-specific points

    def generate_clip_path(self) -> np.ndarray:
        """Generate polygon points for clipping based on shape."""
        if self.shape == "rectangle":
            return self._rectangle_points()
        elif self.shape == "diagonal":
            return self._diagonal_points()
        elif self.shape == "trapezoid":
            return self._trapezoid_points()
        elif self.shape == "polygon":
            return np.array(self.polygon_points)

    def _diagonal_points(self) -> np.ndarray:
        """Generate points for diagonal panel cut."""
        w, h = self.width, self.height
        angle_rad = np.radians(self.diagonal_angle)

        if self.diagonal_direction == "top-left":
            # Cut off top-left corner
            cut_x = h / np.tan(angle_rad)
            return np.array([
                [0, h],           # bottom-left
                [w, h],           # bottom-right
                [w, 0],           # top-right
                [cut_x, 0],       # cut start
                [0, h - cut_x * np.tan(angle_rad)]  # cut end
            ])
        # ... other directions
```

### Convenience Classes

```python
class DiagonalPanel(Panel):
    """Panel with one corner cut diagonally."""
    def __init__(
        self,
        width: float,
        height: float,
        diagonal_angle: float = 45,
        direction: str = "top-left",
        **kwargs
    ):
        super().__init__(
            shape="diagonal",
            width=width,
            height=height,
            diagonal_angle=diagonal_angle,
            diagonal_direction=direction,
            **kwargs
        )

class TrapezoidPanel(Panel):
    """Trapezoid-shaped panel."""
    def __init__(
        self,
        top_width: float,
        bottom_width: float,
        height: float,
        **kwargs
    ):
        # Calculate trapezoid points
        points = [
            (-top_width/2, height/2),
            (top_width/2, height/2),
            (bottom_width/2, -height/2),
            (-bottom_width/2, -height/2)
        ]
        super().__init__(
            shape="polygon",
            points=points,
            **kwargs
        )

class IrregularPanel(Panel):
    """Panel with arbitrary polygon shape."""
    def __init__(
        self,
        points: list[tuple[float, float]],
        **kwargs
    ):
        super().__init__(
            shape="polygon",
            points=points,
            **kwargs
        )
```

## Open Questions

- [x] Should we validate polygon points for self-intersection? **Decision**: Yes, warn user but attempt to render anyway
- [x] How to handle panel borders on diagonal edges? **Decision**: Render border along exact polygon edges
- [x] Should split_diagonal() return two Panel objects or modify original? **Decision**: Return two new IrregularPanel objects (original unchanged)
- [x] Default diagonal angle? **Decision**: 45 degrees (most common in comics)
- [x] Should we provide preset "starburst", "cloud", "explosion" panel shapes? **Decision: Yes** - Implemented as StarburstPanel, CloudPanel, ExplosionPanel classes

## Test Requirements

1. **Diagonal panel rendering**:
   - Test: DiagonalPanel with all four corner directions
   - Test: Diagonal angles from 15° to 75°
   - Test: Content clipped correctly to diagonal boundary

2. **Trapezoid panel rendering**:
   - Test: Trapezoid wider at top, narrower at bottom
   - Test: Reverse trapezoid (narrow top, wide bottom)
   - Test: Extreme ratios (top_width = 2 * bottom_width)

3. **Irregular panel shapes**:
   - Test: Triangle panel (3 points)
   - Test: Pentagon panel (5 points)
   - Test: Complex polygon (8+ points)
   - Test: Self-intersecting polygon (should warn)

4. **Content clipping**:
   - Test: Character positioned outside panel clips correctly
   - Test: Speech bubble tail extends beyond panel clips correctly
   - Test: Panel border renders along irregular edge

5. **SVG/Cairo/HTML output**:
   - Test: Diagonal panels render in SVG with correct clipPath
   - Test: Cairo PNG shows diagonal panels correctly
   - Test: HTML output uses CSS clip-path correctly

## Success Metrics

**This spec is successful when:**
1. DiagonalPanel(diagonal_angle=45) creates panel with diagonal cut
2. Content (characters, bubbles) clips to diagonal boundary
3. TrapezoidPanel renders with slanted sides
4. IrregularPanel accepts arbitrary polygon points and renders correctly
5. Diagonal panels can be used in page layouts alongside rectangular panels
6. Visual output matches professional manga/comic diagonal panel styles

## References and Sources

Based on research into professional comic panel techniques:

- [만화 컷 분할 강좌【응용편】 | MediBang Paint](https://medibangpaint.com/ko/use/2022/12/how-to-arrange-panels-2-application/) - Diagonal panels for expressing unstable moods and shock
- [Odd-Shaped Panel - TV Tropes](https://tvtropes.org/pmwiki/pmwiki.php/Main/OddShapedPanel) - Examples of irregular panel shapes in comics
- [Pro Artist's Guide to Comic & Manga Layouts, Paneling, Flow | Art Rocket](https://www.clipstudio.net/how-to-draw/archives/160963) - Professional panel layout techniques
- [Automatic Stylistic Manga Layout (Academic Paper)](http://www.ying-cao.com/projects/stylistic_layout/files/layout_paper.pdf) - Analysis of manga panel shapes including irregular panels

These sources confirm that diagonal and irregular panel shapes are essential for professional-quality comics and manga, particularly for dramatic moments and action sequences.
