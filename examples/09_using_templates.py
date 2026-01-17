"""Using built-in page templates.

This example demonstrates the variety of pre-built templates:
- FourKoma (4-panel vertical, Japanese style)
- TwoByTwo (2x2 grid, classic layout)
- ActionPage (large panel + small panels)
- WebComic (vertical scroll format)
"""

from comix import Stickman
from comix.page.templates import FourKoma, TwoByTwo, ActionPage, WebComic

# Example 1: FourKoma template with semantic panel names
# Panel positions: setup(200,161), development(200,454), turn(200,746), punchline(200,1039)
print("Creating FourKoma example...")
fourkoma = FourKoma(width=400, height=1200)

story = [
    ("setup", "neutral", "I'm going to learn coding", (200, 161)),
    ("development", "happy", "This is fun!", (200, 454)),
    ("turn", "confused", "Wait, what's a pointer?", (200, 746)),
    ("punchline", "sad", "I give up...", (200, 1039)),
]

for panel_name, expression, text, pos in story:
    panel = getattr(fourkoma, panel_name)
    char = Stickman(height=80)
    char.move_to(pos)
    char.set_expression(expression)
    bubble = char.say(text)
    panel.add_content(char, bubble)

fourkoma.render("examples/output/09_fourkoma.png")

# Example 2: TwoByTwo template with named corners
# Panel positions: top_left(158,158), top_right(442,158), bottom_left(158,442), bottom_right(442,442)
print("Creating TwoByTwo example...")
twobytwo = TwoByTwo(width=600, height=600)

corners = [
    ("top_left", "happy", "Top left!", (158, 158)),
    ("top_right", "excited", "Top right!", (442, 158)),
    ("bottom_left", "surprised", "Bottom left!", (158, 442)),
    ("bottom_right", "confused", "Bottom right!", (442, 442)),
]

for corner_name, expression, text, pos in corners:
    panel = getattr(twobytwo, corner_name)
    char = Stickman(height=60)
    char.move_to(pos)
    char.set_expression(expression)
    bubble = char.say(text)
    panel.add_content(char, bubble)

twobytwo.render("examples/output/09_twobytwo.png")

# Example 3: ActionPage template for action sequences
# Main panel: (300, 245), small panels: (110,630), (300,630), (490,630)
print("Creating ActionPage example...")
action = ActionPage(width=600, height=800, small_panels=3, main_ratio=0.6)

# Main panel - the big action
hero = Stickman(height=150, color="#FF6B9D")
hero.move_to((300, 245))
hero.set_expression("excited")
hero.set_pose("cheering")
bubble_main = hero.shout("Victory!")
action.main.add_content(hero, bubble_main)

# Small panels - reactions
reactions = [
    ("happy", "We did it!", (110, 630)),
    ("surprised", "Wow!", (300, 630)),
    ("sleepy", "Finally...", (490, 630)),
]

for i, (expr, text, pos) in enumerate(reactions):
    char = Stickman(height=50)
    char.move_to(pos)
    char.set_expression(expr)
    bubble = char.say(text)
    action.small[i].add_content(char, bubble)

action.render("examples/output/09_action_page.png")

# Example 4: WebComic (vertical scroll)
# Panel positions: (250,120), (250,330), (250,540), (250,750)
print("Creating WebComic example...")
webcomic = WebComic(width=500, panels=4, panel_height=200)

scroll_story = [
    ("neutral", "Scrolling comics are popular", (250, 120)),
    ("happy", "They work great on mobile", (250, 330)),
    ("excited", "Easy to read on the go!", (250, 540)),
    ("crying", "But my thumb is tired", (250, 750)),
]

for i, (expr, text, pos) in enumerate(scroll_story):
    char = Stickman(height=60)
    char.move_to(pos)
    char.set_expression(expr)
    bubble = char.say(text)
    webcomic.panels[i].add_content(char, bubble)

webcomic.render("examples/output/09_webcomic.png")

print("Created all template examples in examples/output/")
