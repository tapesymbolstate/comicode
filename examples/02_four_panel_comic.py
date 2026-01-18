"""Four-panel comic (4koma style) with a simple joke."""
# Status: ✅ Working (v0.1.108)

from comix import FourKoma, Stickman

# Use FourKoma template (4 vertical panels)
comic = FourKoma(width=400, height=1200)

# Setup - Introduce the joke (panel center y ≈ 161)
char1 = Stickman(height=80)
char1.move_to((200, 161))
bubble1 = char1.say("I have a joke about construction")
comic.setup.add_content(char1, bubble1)

# Development - Build anticipation (panel center y ≈ 454)
char2 = Stickman(height=80)
char2.move_to((200, 454))
bubble2 = char2.say("Oh? Tell me!")
comic.development.add_content(char2, bubble2)

# Twist - Deliver the punchline (panel center y ≈ 746)
char3 = Stickman(height=80)
char3.move_to((200, 746))
bubble3 = char3.say("Sorry, I'm still working on it")
comic.turn.add_content(char3, bubble3)

# Conclusion - Reaction (panel center y ≈ 1039)
char4 = Stickman(height=80)
char4.move_to((200, 1039))
char4.set_expression("confused")
bubble4 = char4.think("...")
comic.punchline.add_content(char4, bubble4)

comic.render("examples/output/02_four_panel_comic.png")

print("Created examples/output/02_four_panel_comic.png")
