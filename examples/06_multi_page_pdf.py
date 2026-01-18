"""Multi-page PDF comic using the Book class.

This example demonstrates creating a multi-page comic book with:
- Cover page using SplashPage template
- Story pages using different layouts
- PDF export with all pages combined
"""
# Status: ✅ Working (v0.1.108)

from comix import Book, Page, Panel, Stickman, Text
from comix.page.templates import SplashPage, TwoByTwo

# Create a book with metadata
book = Book(title="My First Comic", author="Comic Creator")

# Page 1: Cover page using SplashPage
cover = SplashPage(width=400, height=600, header_height=80)
title = Text("My First Comic", font_size=32, color="#333333")
title.move_to((200, 40))
cover.header.add_content(title)

hero = Stickman(height=150, color="#FF6B9D")
hero.move_to((200, 350))
hero.set_expression("happy")
cover.splash.add_content(hero)
book.add_page(cover)

# Page 2: Two-panel dialogue (2x1 layout: panels at y=158, y=442)
page2 = Page(width=400, height=600)
page2.set_layout(rows=2, cols=1)

panel1 = Panel()
alice = Stickman(name="Alice", height=80, color="#FF6B9D")
alice.move_to((200, 158))
bubble1 = alice.say("Welcome to my comic!")
panel1.add_content(alice, bubble1)

panel2 = Panel()
bob = Stickman(name="Bob", height=80, color="#4ECDC4")
bob.move_to((200, 442))
bubble2 = bob.say("It's great to be here!")
panel2.add_content(bob, bubble2)

page2.add(panel1, panel2)
page2.auto_layout()
book.add_page(page2)

# Page 3: Four-panel grid using TwoByTwo
# Panel positions: (108,158), (292,158), (108,442), (292,442)
page3 = TwoByTwo(width=400, height=600)

scenes = [
    ("happy", "Let's go on an adventure!", (108, 158)),
    ("excited", "This is exciting!", (292, 158)),
    ("surprised", "Wow, look at that!", (108, 442)),
    ("confused", "Where are we?", (292, 442)),
]

for i, (expr, text, pos) in enumerate(scenes):
    char = Stickman(height=60)
    char.move_to(pos)
    char.set_expression(expr)
    bubble = char.say(text)
    page3.panels[i].add_content(char, bubble)

book.add_page(page3)

# Render to PDF (requires pycairo)
try:
    output_path = book.render("examples/output/06_multi_page_pdf.pdf", quality="medium")
    print(f"Created {output_path}")
except ImportError:
    print("PDF rendering requires pycairo. Install with: uv add pycairo")
    # Fallback: render individual pages as PNG
    for i, page in enumerate(book):
        page.render(f"examples/output/06_multi_page_pdf_page{i+1}.png")
    print("Created individual PNG files instead")
