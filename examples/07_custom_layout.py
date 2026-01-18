"""Custom page layout with 3x2 grid.

This example demonstrates creating custom grid layouts with:
- 3 columns x 2 rows for 6 panels
- Different gutter (spacing) settings
- Auto-layout positioning
"""

from comix import Page, Panel, Stickman

# Create page with custom 3x2 grid layout
page = Page(width=900, height=600)
page.set_layout(rows=2, cols=3)

# Create 6 panels with different characters and expressions
# Panel centers: row 0 at y=158, row 1 at y=442
# Columns at x=150, 450, 750 (adjusted for bubble positioning)
characters = [
    ("neutral", "#FF6B9D", "Setup", (150, 158)),
    ("happy", "#4ECDC4", "Joy", (450, 158)),
    ("sad", "#95E1D3", "Sorrow", (750, 158)),
    ("angry", "#F38181", "Anger", (150, 442)),
    ("surprised", "#AA96DA", "Shock", (450, 442)),
    ("confused", "#FCBAD3", "Puzzled", (750, 442)),
]

for i, (expression, color, text, pos) in enumerate(characters):
    panel = Panel()
    char = Stickman(height=80, color=color)
    char.move_to(pos)
    char.set_expression(expression)
    bubble = char.say(text)
    panel.add_content(char, bubble)
    page.add(panel)

# Apply the 3x2 grid layout
page.auto_layout()

# Render to PNG
page.render("examples/output/07_custom_layout.png")
print("Created examples/output/07_custom_layout.png")
