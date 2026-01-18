"""Single panel with multiple characters (group scene).

Demonstrates how to position multiple characters and speech bubbles
in a single panel without overlap. Uses manual bubble positioning
to ensure clean, readable dialogue placement.
"""

from comix import Page, Panel, Stickman

# Create a page with a single large panel
page = Page(width=800, height=600)
panel = Panel(width=760, height=560)
panel.move_to((400, 300))

# Three characters standing in a row
alice = Stickman(name="Alice", height=100, color="#FF6B9D")
alice.move_to((200, 380))

bob = Stickman(name="Bob", height=110, color="#4ECDC4")
bob.move_to((400, 380))

charlie = Stickman(name="Charlie", height=95, color="#95E1D3")
charlie.move_to((600, 380))

# Create bubbles with manual positioning to avoid overlap
# Stagger vertically for clear reading order (left to right, top to bottom)
bubble_a = alice.say("Let's work together!")
bubble_a.move_to((200, 200))  # Top left

bubble_b = bob.say("Great idea!")
bubble_b.move_to((400, 130))  # Top center (slightly higher)

bubble_c = charlie.say("I'm in!")
bubble_c.move_to((600, 200))  # Top right

# Add all content to panel (disable auto-positioning since we positioned manually)
panel.add_content(alice, bob, charlie, auto_position_bubbles=False)
panel.add_content(bubble_a, bubble_b, bubble_c, auto_position_bubbles=False)

page.add(panel)
page.render("examples/output/03_group_scene.png")

print("Created examples/output/03_group_scene.png")
