#!/usr/bin/env python3
"""Test current xkcd style capabilities."""

from comix import Page, Panel, Stickman

page = Page(width=600, height=400, background_color="#FFFFFF")
panel = Panel(width=550, height=350)
panel.move_to((300, 200))

# Create xkcd-style character
char = Stickman(name="Bob", height=100, proportion_style="xkcd")
char.move_to((200, 240))
char.set_expression("neutral")

# Create another character
char2 = Stickman(name="Alice", height=100, proportion_style="xkcd")
char2.move_to((450, 240))
char2.set_expression("happy")
char2.set_arm_angles(left_shoulder=135, right_shoulder=135)

# Add dialogue
bubble1 = char.say("This is the current\nxkcd style!", width=180, height=60)
bubble2 = char2.say("Not bad!", width=120, height=50)

panel.add_content(char, char2, bubble1, bubble2)
page.add(panel)
page.render("examples/output/test_xkcd_current.png")

print("Created: examples/output/test_xkcd_current.png")
print("\nCurrent capabilities:")
print("✅ xkcd proportions")
print("✅ Stick figures")
print("✅ Speech bubbles")
print("✅ Joint articulation")
print("\nMissing for true xkcd style:")
print("❌ Hand-drawn wobbly lines")
print("❌ Sketchy/jittery effect")
print("❌ Free-form curves")
print("❌ xkcd font")
