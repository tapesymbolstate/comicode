"""Simple two-panel dialogue between two stick figures."""

from comix import Page, Panel, Stickman

# Create page with 1x2 layout (two panels side by side)
page = Page(width=800, height=400)
page.set_layout(rows=1, cols=2)

# Panel 1: Alice asks a question
panel1 = Panel()
alice = Stickman(name="Alice", height=100, color="#FF6B9D")
alice.move_to((200, 200))
bubble1 = alice.say("How are you today?")
panel1.add_content(alice, bubble1)

# Panel 2: Bob responds
panel2 = Panel()
bob = Stickman(name="Bob", height=100, color="#4ECDC4")
bob.move_to((600, 200))
bubble2 = bob.say("I'm doing great!")
panel2.add_content(bob, bubble2)

# Assemble and render
page.add(panel1, panel2)
page.auto_layout()
page.render("examples/output/01_simple_dialogue.png")

print("Created examples/output/01_simple_dialogue.png")
