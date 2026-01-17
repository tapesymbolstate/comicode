"""Showcase of different character expressions."""

from comix import Stickman, TwoByTwo

# Use TwoByTwo template (2x2 grid layout)
page = TwoByTwo(width=800, height=800)

# Four expressions with their panel positions
# TwoByTwo panels: (208,208), (592,208), (208,592), (592,592)
expressions_with_pos = [
    ("neutral", (208, 208)),
    ("happy", (592, 208)),
    ("sad", (208, 592)),
    ("angry", (592, 592)),
]

for i, (expr, pos) in enumerate(expressions_with_pos):
    char = Stickman(height=80)
    char.move_to(pos)
    char.set_expression(expr)
    bubble = char.say(f"I'm {expr}!")
    page.panels[i].add_content(char, bubble)

page.auto_layout()
page.render("examples/output/04_expressions.png")

print("Created examples/output/04_expressions.png")
