#!/usr/bin/env python3
"""Example 11: Interactive HTML Export

Demonstrates the HTML renderer's interactive features:
- Embedded SVG for crisp scaling
- Zoom controls (mouse wheel + buttons)
- Pan with mouse drag
- Dark/light theme toggle
- Fullscreen mode
- Keyboard shortcuts
- Touch support for mobile
"""
# Status: ✅ Working (v0.1.108)

from pathlib import Path

from comix import (
    Page,
    Panel,
    Stickman,
    TwoByTwo,
    Book,
    HTMLRenderer,
)

OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


def create_simple_html() -> None:
    """Create a simple interactive HTML comic."""
    page = Page(width=800, height=400)
    page.set_layout(rows=1, cols=2)

    panel1 = Panel(width=360, height=360)
    alice = Stickman(name="Alice", height=80, color="#E91E63")
    alice.move_to((180, 200))
    bubble1 = alice.say("Try zooming with\nyour mouse wheel!")
    panel1.add_content(alice, bubble1)

    panel2 = Panel(width=360, height=360)
    bob = Stickman(name="Bob", height=80, color="#2196F3")
    bob.move_to((180, 200))
    bubble2 = bob.say("Or drag to pan\naround the comic!")
    panel2.add_content(bob, bubble2)

    page.add(panel1, panel2)
    page.auto_layout()

    output_path = OUTPUT_DIR / "11_html_simple.html"
    page.render(str(output_path), title="Interactive Comic Demo")
    print(f"Created {output_path}")


def create_dark_theme_html() -> None:
    """Create an HTML comic with dark theme."""
    page = Page(width=600, height=600)

    panel = Panel(width=550, height=550)
    char = Stickman(name="Night Owl", height=100, color="#9C27B0")
    char.move_to((275, 300))
    bubble = char.say("Dark theme looks\ngreat at night!")
    panel.add_content(char, bubble)
    panel.move_to((300, 300))

    page.add(panel)

    output_path = OUTPUT_DIR / "11_html_dark.html"
    page.render(
        str(output_path),
        title="Dark Theme Comic",
        theme="dark",
    )
    print(f"Created {output_path}")


def create_multi_page_html() -> None:
    """Create a multi-page HTML comic with navigation."""
    page1 = TwoByTwo(width=800, height=800)
    for i, panel in enumerate(page1.panels):
        char = Stickman(name=f"Character {i+1}", height=60)
        char.move_to((panel.width / 2, panel.height / 2 + 20))
        bubble = char.say(f"Page 1, Panel {i+1}")
        panel.add_content(char, bubble)

    page2 = TwoByTwo(width=800, height=800)
    for i, panel in enumerate(page2.panels):
        char = Stickman(name=f"Character {i+5}", height=60, color="#4CAF50")
        char.move_to((panel.width / 2, panel.height / 2 + 20))
        bubble = char.say(f"Page 2, Panel {i+1}")
        panel.add_content(char, bubble)

    page3 = Page(width=800, height=600)
    panel = Panel(width=700, height=500)
    char = Stickman(name="Narrator", height=100, color="#FF5722")
    char.move_to((350, 280))
    bubble = char.say("The End!\nUse arrow keys\nto navigate.")
    panel.add_content(char, bubble)
    panel.move_to((400, 300))
    page3.add(panel)

    book = Book(title="Multi-Page Comic")
    book.add_page(page1)
    book.add_page(page2)
    book.add_page(page3)

    output_path = OUTPUT_DIR / "11_html_book.html"
    renderer = HTMLRenderer(title="Multi-Page Adventure")
    renderer.render_book(book, str(output_path))
    print(f"Created {output_path}")


def create_minimal_html() -> None:
    """Create an HTML comic with minimal UI (no zoom/pan)."""
    page = Page(width=500, height=400)

    panel = Panel(width=450, height=350)
    char = Stickman(name="Minimalist", height=80)
    char.move_to((225, 200))
    bubble = char.say("Clean and simple!")
    panel.add_content(char, bubble)
    panel.move_to((250, 200))

    page.add(panel)

    output_path = OUTPUT_DIR / "11_html_minimal.html"
    page.render(
        str(output_path),
        title="Minimal Comic",
        enable_zoom=False,
        enable_pan=False,
        enable_fullscreen=False,
    )
    print(f"Created {output_path}")


if __name__ == "__main__":
    print("Creating HTML export examples...")
    print()

    create_simple_html()
    create_dark_theme_html()
    create_multi_page_html()
    create_minimal_html()

    print()
    print("All HTML examples created!")
    print()
    print("Open the HTML files in your browser to test:")
    print("- Mouse wheel to zoom")
    print("- Click and drag to pan")
    print("- Double-click to reset view")
    print("- Press T to toggle theme")
    print("- Press F for fullscreen")
    print("- Arrow keys to navigate pages (in book)")
