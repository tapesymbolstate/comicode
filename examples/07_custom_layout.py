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
characters = [
    ("neutral", "#FF6B9D", "Panel 1: Setup"),
    ("happy", "#4ECDC4", "Panel 2: Joy"),
    ("sad", "#95E1D3", "Panel 3: Sorrow"),
    ("angry", "#F38181", "Panel 4: Anger"),
    ("surprised", "#AA96DA", "Panel 5: Shock"),
    ("confused", "#FCBAD3", "Panel 6: Puzzled"),
]

for i, (expression, color, text) in enumerate(characters):
    panel = Panel()
    char = Stickman(height=80, color=color)
    char.move_to((150, 100))
    char.set_expression(expression)
    bubble = char.say(text)
    panel.add_content(char, bubble)
    page.add(panel)

# Apply the 3x2 grid layout
page.auto_layout()

# Render to PNG
page.render("examples/output/07_custom_layout.png")
print("Created examples/output/07_custom_layout.png")
