"""Single panel with multiple characters (group scene)."""

from comix import Page, Panel, Stickman

# Create a page with a single large panel
page = Page(width=800, height=600)
panel = Panel(width=760, height=560)
panel.move_to((400, 300))

# Three characters standing in a row
alice = Stickman(name="Alice", height=100, color="#FF6B9D")
alice.move_to((250, 350))
bubble_a = alice.say("Let's work together!")

bob = Stickman(name="Bob", height=110, color="#4ECDC4")
bob.move_to((400, 350))
bubble_b = bob.say("Great idea!")

charlie = Stickman(name="Charlie", height=95, color="#95E1D3")
charlie.move_to((550, 350))
bubble_c = charlie.say("I'm in!")

# Add all characters and bubbles to panel
panel.add_content(alice, bob, charlie)
panel.add_content(bubble_a, bubble_b, bubble_c)

page.add(panel)
page.render("examples/output/03_group_scene.png")

print("Created examples/output/03_group_scene.png")
