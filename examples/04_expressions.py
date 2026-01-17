"""Showcase of different character expressions."""

from comix import Stickman, TwoByTwo

# Use TwoByTwo template (2x2 grid layout)
page = TwoByTwo(width=800, height=800)

# Four expressions to demonstrate
expressions = ["neutral", "happy", "sad", "angry"]

for i, expr in enumerate(expressions):
    char = Stickman(height=80)
    char.move_to((200, 200))
    char.set_expression(expr)
    bubble = char.say(f"I'm {expr}!")
    page.panels[i].add_content(char, bubble)

page.auto_layout()
page.render("examples/output/04_expressions.png")

print("Created examples/output/04_expressions.png")
