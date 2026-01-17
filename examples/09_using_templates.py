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
print("Creating FourKoma example...")
fourkoma = FourKoma(width=400, height=1200)

story = [
    ("setup", "neutral", "I'm going to learn coding"),
    ("development", "happy", "This is fun!"),
    ("turn", "confused", "Wait, what's a pointer?"),
    ("punchline", "sad", "I give up..."),
]

for panel_name, expression, text in story:
    panel = getattr(fourkoma, panel_name)
    char = Stickman(height=80)
    char.move_to((200, 150))
    char.set_expression(expression)
    bubble = char.say(text)
    panel.add_content(char, bubble)

fourkoma.render("examples/output/09_fourkoma.png")

# Example 2: TwoByTwo template with named corners
print("Creating TwoByTwo example...")
twobytwo = TwoByTwo(width=600, height=600)

corners = [
    ("top_left", "happy", "Top left!"),
    ("top_right", "excited", "Top right!"),
    ("bottom_left", "surprised", "Bottom left!"),
    ("bottom_right", "confused", "Bottom right!"),
]

for corner_name, expression, text in corners:
    panel = getattr(twobytwo, corner_name)
    char = Stickman(height=60)
    char.move_to((150, 75))
    char.set_expression(expression)
    bubble = char.say(text)
    panel.add_content(char, bubble)

twobytwo.render("examples/output/09_twobytwo.png")

# Example 3: ActionPage template for action sequences
print("Creating ActionPage example...")
action = ActionPage(width=600, height=800, small_panels=3, main_ratio=0.6)

# Main panel - the big action
hero = Stickman(height=150, color="#FF6B9D")
hero.move_to((300, 250))
hero.set_expression("excited")
hero.set_pose("cheering")
bubble_main = hero.shout("Victory!")
action.main.add_content(hero, bubble_main)

# Small panels - reactions
reactions = [
    ("happy", "We did it!"),
    ("surprised", "Wow!"),
    ("sleepy", "Finally..."),
]

for i, (expr, text) in enumerate(reactions):
    char = Stickman(height=50)
    char.move_to((100, 80))
    char.set_expression(expr)
    bubble = char.say(text)
    action.small[i].add_content(char, bubble)

action.render("examples/output/09_action_page.png")

# Example 4: WebComic (vertical scroll)
print("Creating WebComic example...")
webcomic = WebComic(width=500, panels=4, panel_height=200)

scroll_story = [
    ("neutral", "Scrolling comics are popular"),
    ("happy", "They work great on mobile"),
    ("excited", "Easy to read on the go!"),
    ("crying", "But my thumb is tired"),
]

for i, (expr, text) in enumerate(scroll_story):
    char = Stickman(height=60)
    char.move_to((250, 100))
    char.set_expression(expr)
    bubble = char.say(text)
    webcomic.panels[i].add_content(char, bubble)

webcomic.render("examples/output/09_webcomic.png")

print("Created all template examples in examples/output/")
