# Comicode

A code-based comic creation framework inspired by [Manim](https://www.manim.community/). Create comics, manga, and webtoons using Python with a fluent, chainable API.

## Features

- **9 Character Types**: Stickman, SimpleFace, ChubbyStickman, Robot, Chibi, Anime, Superhero, Cartoon, AnimalStyle
- **11 Expressions**: neutral, happy, sad, angry, surprised, confused, sleepy, excited, scared, smirk, crying
- **12 Poses**: standing, sitting, waving, pointing, walking, running, jumping, dancing, lying, kneeling, cheering, thinking
- **5 Bubble Types**: Speech, Thought, Shout, Whisper, Narrator
- **9 Page Templates**: FourKoma, TwoByTwo, SplashPage, WebComic, ThreeRowLayout, MangaPage, ActionPage, NewspaperStrip, Widescreen
- **6 Visual Effects**: AppearEffect, ShakeEffect, ZoomEffect, MotionLines, FocusLines, ImpactEffect
- **Multiple Output Formats**: SVG (always available), PNG/PDF (with optional Cairo)

## Installation

**Prerequisites**: Python 3.13+

```bash
# Clone the repository
git clone https://github.com/anthropics/comicode.git
cd comicode

# Install with uv (recommended)
uv sync

# Optional: Install Cairo for PNG/PDF rendering
uv sync --extra cairo
```

## Quick Start

### Minimal Example

```python
from comix import Page, Panel, Stickman

# Create a page and panel
page = Page(width=400, height=300)
panel = Panel(width=360, height=260)
panel.move_to((200, 150))

# Create a character and add dialogue
char = Stickman(name="Bob", height=80)
char.move_to((200, 180))
bubble = char.say("Hello World!")

# Build and render
panel.add_content(char, bubble)
page.add(panel)
page.render("hello.png")
```

### Two-Panel Dialogue

```python
from comix import Page, Panel, Stickman

page = Page(width=800, height=400)
page.set_layout(rows=1, cols=2)

# Panel 1: Alice asks
panel1 = Panel()
alice = Stickman(name="Alice", height=100, color="#E91E63")
alice.move_to((200, 220))
bubble1 = alice.say("How are you?")
panel1.add_content(alice, bubble1)

# Panel 2: Bob responds
panel2 = Panel()
bob = Stickman(name="Bob", height=100, color="#2196F3")
bob.move_to((600, 220))
bubble2 = bob.say("I'm great!")
panel2.add_content(bob, bubble2)

page.add(panel1, panel2)
page.auto_layout()
page.render("dialogue.png")
```

### Using Templates

```python
from comix import Stickman
from comix.page.templates import FourKoma

# Create a 4-panel comic (manga style)
comic = FourKoma()

char = Stickman(name="Hero", height=80)

# Add content to each panel using semantic properties
char.move_to((150, 150))
char.set_expression("neutral")
comic.setup.add_content(char, char.say("Monday morning..."))

char.move_to((150, 150))
char.set_expression("surprised")
comic.development.add_content(char, char.say("Wait, is that...?"))

char.move_to((150, 150))
char.set_expression("excited")
comic.climax.add_content(char, char.say("FREE DONUTS!"))

char.move_to((150, 150))
char.set_expression("happy")
comic.conclusion.add_content(char, char.say("Best day ever!"))

comic.render("4koma.png")
```

## Character Types

```python
from comix import Stickman, SimpleFace, ChubbyStickman, Robot, Chibi, Anime, Superhero, Cartoon, AnimalStyle

# Basic stick figure
stickman = Stickman(name="Bob", height=100)

# Simple emoticon face
face = SimpleFace(name="Smiley", height=50)

# Rounded friendly figure
chubby = ChubbyStickman(name="Buddy", height=100)

# Mechanical robot
robot = Robot(name="R2", height=100, led_color="#00FF00")

# Cute chibi style
chibi = Chibi(name="Mochi", height=80, hair_style="twintails")

# Anime/manga style
anime = Anime(name="Sakura", height=120, hair_style="ponytail", eye_color="#8B4513")

# Superhero with costume
hero = Superhero(name="Captain", height=120, cape=True, emblem="star")

# Classic cartoon style
toon = Cartoon(name="Toony", height=100, body_shape="pear", gloves=True)

# Anthropomorphic animal character
animal = AnimalStyle(name="Felix", height=100, species="cat", fur_color="#FF9800")
```

## Expressions and Poses

```python
# Set expression
char.set_expression("happy")  # or: neutral, sad, angry, surprised, confused, sleepy, excited, scared, smirk, crying

# Set pose
char.set_pose("waving")  # or: standing, sitting, pointing, walking, running, jumping, dancing, lying, kneeling, cheering, thinking

# Face direction
char.face("left")  # or "right"
```

## Speech Bubbles

```python
# Convenience methods
bubble = char.say("Hello!")      # Speech bubble
bubble = char.think("Hmm...")    # Thought bubble
bubble = char.shout("STOP!")     # Shout bubble
bubble = char.whisper("Psst...")  # Whisper bubble

# Or create directly
from comix import SpeechBubble, ThoughtBubble, NarratorBubble

bubble = SpeechBubble("Hello!")
bubble.attach_to(char)

narrator = NarratorBubble("Meanwhile...")  # No tail
```

## Rendering Options

```python
# PNG (requires pycairo)
page.render("output.png")
page.render("output.png", quality="high")  # 300 DPI
page.render("output.png", dpi=150)

# PDF (requires pycairo)
page.render("output.pdf", format="pdf")

# SVG (always available)
page.render("output.svg", format="svg")

# Multi-page PDF
from comix import Book

book = Book()
book.add_page(page1)
book.add_page(page2)
book.render("comic.pdf")
```

## CLI Commands

```bash
# Show library info
comix info

# Render a Python script
comix render script.py -o output.png

# Compile multiple pages to PDF
comix compile page1.py page2.py -o book.pdf
```

## Examples

See the `examples/` directory for 26 working examples:

```bash
# Run an example
uv run python examples/01_simple_dialogue.py

# View the output
open examples/output/01_simple_dialogue.png
```

## Development

```bash
# Run tests
uv run pytest

# Type check
uv run mypy comix/

# Lint
uv run ruff check .
```

## Documentation

### Core Features
- [Getting Started Guide](specs/getting-started.md)
- [Character Basics](specs/character-basics.md)
- [Speech Bubbles](specs/speech-bubbles.md)
- [Page Rendering](specs/page-rendering.md)
- [Working Examples](specs/working-examples.md)

### Advanced Features (Optional)
See `specs/future-features/` for HTML export, animations, video, AI images, and preview server.

## License

MIT
