"""Manual positioning and styling of comic elements.

This example demonstrates precise control over:
- Manual panel placement with move_to()
- Character positioning with next_to() and align_to()
- Custom colors and styling
- Bubble attachment and positioning
"""
# Status: ✅ Working (v0.1.108)

from comix import Page, Panel, Stickman
from comix.cobject.bubble import SpeechBubble

# Create a page (no auto-layout, all manual positioning)
page = Page(width=800, height=600)

# Manually position a large main panel
main_panel = Panel(width=500, height=400)
main_panel.move_to((300, 300))
main_panel.set_border(color="#333333", width=3, style="solid")

# Position characters manually within the panel
# Alice on the left
alice = Stickman(name="Alice", height=120, color="#FF6B9D")
alice.move_to((150, 350))
alice.face("right")
alice.set_expression("happy")

# Bob on the right, facing left
bob = Stickman(name="Bob", height=120, color="#4ECDC4")
bob.move_to((450, 350))
bob.face("left")
bob.set_expression("surprised")

# Manually create and position bubbles
bubble1 = SpeechBubble(text="Hi Bob!", width=100, height=60)
bubble1.move_to((150, 180))
bubble1.attach_to(alice)

bubble2 = SpeechBubble(text="Oh, hi Alice!", width=120, height=60)
bubble2.move_to((450, 180))
bubble2.attach_to(bob)

# Add everything to main panel
main_panel.add_content(alice, bob, bubble1, bubble2)

# Add a smaller side panel for narration
side_panel = Panel(width=200, height=150)
side_panel.move_to((700, 150))
side_panel.set_border(color="#666666", width=2, style="dashed")

narrator_char = Stickman(height=50, color="#95E1D3")
narrator_char.move_to((100, 100))
narrator_text = narrator_char.say("Meanwhile...")
side_panel.add_content(narrator_char, narrator_text)

# Add panels to page (order matters for rendering)
page.add(main_panel, side_panel)

# Render without auto_layout() to preserve manual positions
page.render("examples/output/08_manual_positioning.png")
print("Created examples/output/08_manual_positioning.png")
