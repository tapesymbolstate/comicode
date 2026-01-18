"""New page templates: NewspaperStrip and Widescreen.

This example demonstrates the newly added page templates:
- NewspaperStrip: Classic 3-4 horizontal panel newspaper format
- Widescreen: Cinematic 16:9 aspect ratio panels for modern webcomics
"""
# Status: ✅ Working (v0.1.108)

from comix import Stickman
from comix.page.templates import NewspaperStrip, Widescreen

# Example 1: Classic Newspaper Strip (like Peanuts, Garfield, Calvin & Hobbes)
print("Creating NewspaperStrip example (3 panels)...")
strip = NewspaperStrip(panels=3)
strip.auto_layout()

newspaper_story = [
    ("neutral", "I should be productive today", strip.panels[0]),
    ("happy", "Time to make a to-do list!", strip.panels[1]),
    ("sleepy", "1. Make to-do list. Done!", strip.panels[2]),
]

for expression, text, panel in newspaper_story:
    char = Stickman(height=70)
    char.move_to(panel.position)
    char.set_expression(expression)
    bubble = char.say(text)
    panel.add_content(char, bubble)

strip.render("examples/output/24_newspaper_strip.png")

# Example 2: 4-Panel Newspaper Strip (classic Sunday comic feel)
print("Creating NewspaperStrip example (4 panels)...")
strip4 = NewspaperStrip(panels=4)
strip4.auto_layout()

coding_story = [
    ("neutral", "Let me fix this bug..."),
    ("confused", "Why isn't it working?"),
    ("angry", "I've been at this for hours!"),
    ("surprised", "Oh. Missing semicolon."),
]

for i, (expression, text) in enumerate(coding_story):
    panel = strip4.panels[i]
    char = Stickman(height=60)
    char.move_to(panel.position)
    char.set_expression(expression)
    bubble = char.say(text)
    panel.add_content(char, bubble)

strip4.render("examples/output/24_newspaper_strip_4panel.png")

# Example 3: Widescreen Cinematic Layout (modern webcomic style)
print("Creating Widescreen example (16:9 aspect)...")
widescreen = Widescreen(panels=3, width=1000)
widescreen.auto_layout()

cinematic_story = [
    ("neutral", "Establishing shot - our hero arrives"),
    ("excited", "The adventure begins!"),
    ("surprised", "Plot twist!"),
]

for i, (expression, text) in enumerate(cinematic_story):
    panel = widescreen.panels[i]
    char = Stickman(height=80)
    char.move_to(panel.position)
    char.set_expression(expression)
    bubble = char.say(text)
    panel.add_content(char, bubble)

widescreen.render("examples/output/24_widescreen.png")

# Example 4: Ultra-wide Widescreen (21:9 cinematic)
print("Creating Widescreen example (21:9 ultra-wide)...")
ultrawide = Widescreen(panels=2, aspect_ratio=21 / 9, width=1200)
ultrawide.auto_layout()

epic_story = [
    ("excited", "The epic panoramic shot..."),
    ("happy", "Perfect for dramatic landscapes!"),
]

for i, (expression, text) in enumerate(epic_story):
    panel = ultrawide.panels[i]
    char = Stickman(height=60)
    char.move_to(panel.position)
    char.set_expression(expression)
    bubble = char.say(text)
    panel.add_content(char, bubble)

ultrawide.render("examples/output/24_widescreen_ultrawide.png")

print("Created all new template examples in examples/output/")
print("  - 24_newspaper_strip.png (3 panels)")
print("  - 24_newspaper_strip_4panel.png (4 panels)")
print("  - 24_widescreen.png (16:9 aspect)")
print("  - 24_widescreen_ultrawide.png (21:9 ultra-wide)")
