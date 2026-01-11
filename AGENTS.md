## Build & Run

- Package manager: `uv`
- Python version: 3.13
- Install deps: `uv sync`
- Run: `uv run python main.py`

## Validation

- Tests: `uv run pytest`
- Typecheck: `uv run mypy comix/`
- Lint: `uv run ruff check .`

## Project Structure

```
comicode/
├── comix/                    # Main package
│   ├── cobject/              # Visual elements (CObject hierarchy)
│   │   ├── panel/            # Panel, Border, Gutter
│   │   ├── bubble/           # Speech bubbles (Speech, Thought, Shout, Whisper, Narrator)
│   │   ├── text/             # Text, StyledText, SFX
│   │   ├── character/        # Character, Stickman, SimpleFace
│   │   ├── shapes/           # Rectangle, Circle, Line
│   │   └── image/            # Image, AIImage
│   ├── page/                 # Page, Strip, SinglePanel
│   ├── effect/               # Visual effects for webtoons
│   ├── layout/               # GridLayout, FlowLayout
│   ├── style/                # Style system with presets
│   ├── renderer/             # SVG, Cairo, Web renderers
│   ├── parser/               # Markup parser (optional)
│   └── utils/                # Color, geometry, bezier utilities
├── specs/                    # PRD and specifications
│   └── PRD.md                # Full architecture design
├── tests/                    # Test files
├── main.py                   # Entry point
└── pyproject.toml            # Project config
```

## Codebase Patterns

- **Manim-inspired API**: Method chaining (`.move_to().face().say()`)
- **Hierarchy**: CObject → Panel/Bubble/Character → Page
- **Rendering**: Page.build() → Page.render() → Renderer
