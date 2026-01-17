"""Showcase of different speech bubble types."""

from comix import (
    Page,
    Panel,
    ShoutBubble,
    SpeechBubble,
    Stickman,
    ThoughtBubble,
    WhisperBubble,
)

# Create a page with 4 rows
page = Page(width=800, height=1000)
page.set_layout(rows=4, cols=1)

# Speech bubble (normal dialogue)
panel1 = Panel()
char1 = Stickman(height=80)
char1.move_to((400, 125))
bubble1 = SpeechBubble(text="This is normal speech")
bubble1.attach_to(char1)
panel1.add_content(char1, bubble1)

# Thought bubble (internal thoughts)
panel2 = Panel()
char2 = Stickman(height=80)
char2.move_to((400, 125))
bubble2 = ThoughtBubble(text="This is a thought...")
bubble2.attach_to(char2)
panel2.add_content(char2, bubble2)

# Shout bubble (loud exclamation)
panel3 = Panel()
char3 = Stickman(height=80)
char3.move_to((400, 125))
bubble3 = ShoutBubble(text="THIS IS SHOUTING!")
bubble3.attach_to(char3)
panel3.add_content(char3, bubble3)

# Whisper bubble (quiet speech)
panel4 = Panel()
char4 = Stickman(height=80)
char4.move_to((400, 125))
bubble4 = WhisperBubble(text="this is a whisper...")
bubble4.attach_to(char4)
panel4.add_content(char4, bubble4)

page.add(panel1, panel2, panel3, panel4)
page.auto_layout()
page.render("examples/output/05_bubble_types.png")

print("Created examples/output/05_bubble_types.png")
