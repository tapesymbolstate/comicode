"""StyledText, SFX, and NarratorBubble for enhanced storytelling.

Comix provides specialized text elements beyond basic speech bubbles:
- StyledText: Text with background, padding, and border
- SFX: Sound effect text with outline and shadow
- NarratorBubble: Rectangular caption boxes for narration

This example demonstrates:
- Caption boxes for scene descriptions
- Sound effects (onomatopoeia)
- Time and place indicators
- Story narration
- Combining multiple text types in panels
"""
# Status: ✅ Working (v0.1.108)

from comix import Page, Panel, Stickman
from comix.cobject.text.text import Text, StyledText, SFX
from comix.cobject.bubble.bubble import NarratorBubble


def create_narrator_demo() -> None:
    """Demonstrate NarratorBubble for story narration."""
    page = Page(width=800, height=600, background_color="#F5F5F5")
    page.set_layout(rows=2, cols=2)

    # Panel 1: Scene introduction with narrator
    panel1 = Panel()
    narrator1 = NarratorBubble(
        text="Once upon a time, in a land far away...",
        fill_color="#FFFACD",
        border_color="#DAA520",
        border_width=2.0,
        font_size=14.0,
    )
    narrator1.move_to((200, 50))

    char1 = Stickman(height=80)
    char1.move_to((200, 220))
    char1.set_expression("happy")
    panel1.add_content(narrator1, char1)

    # Panel 2: Time/place caption
    panel2 = Panel()
    time_caption = NarratorBubble(
        text="Three days later...",
        fill_color="#E0E0E0",
        border_color="#9E9E9E",
        font_size=12.0,
    )
    time_caption.move_to((200, 40))

    char2 = Stickman(height=80)
    char2.move_to((200, 200))
    char2.set_expression("confused")
    bubble2 = char2.say("Where am I?")
    panel2.add_content(time_caption, char2, bubble2)

    # Panel 3: Internal monologue narrator
    panel3 = Panel()
    thought_narrator = NarratorBubble(
        text="He wondered if he had made the right choice.",
        fill_color="#E3F2FD",
        border_color="#1976D2",
        border_width=1.5,
        font_size=13.0,
    )
    thought_narrator.move_to((200, 50))

    char3 = Stickman(height=80, color="#1976D2")
    char3.move_to((200, 220))
    char3.set_expression("sad")
    char3.set_pose("thinking")
    panel3.add_content(thought_narrator, char3)

    # Panel 4: Dramatic narrator
    panel4 = Panel()
    dramatic_narrator = NarratorBubble(
        text="Little did he know, adventure awaited!",
        fill_color="#FFCDD2",
        border_color="#D32F2F",
        border_width=2.5,
        font_size=15.0,
    )
    dramatic_narrator.move_to((200, 50))

    char4 = Stickman(height=80, color="#D32F2F")
    char4.move_to((200, 220))
    char4.set_expression("excited")
    char4.set_pose("pointing")
    panel4.add_content(dramatic_narrator, char4)

    page.add(panel1, panel2, panel3, panel4)
    page.auto_layout()

    page.render("examples/output/21_narrator_demo.png")
    print("Created examples/output/21_narrator_demo.png")


def create_sfx_demo() -> None:
    """Demonstrate SFX for sound effects."""
    page = Page(width=800, height=500, background_color="#FAFAFA")
    page.set_layout(rows=1, cols=3)

    # Panel 1: Impact SFX
    panel1 = Panel()
    sfx1 = SFX(
        text="BOOM!",
        color="#FF0000",
        outline_color="#FFFF00",
        outline_width=4.0,
        font_size=48.0,
    )
    sfx1.move_to((200, 120))

    char1 = Stickman(height=70)
    char1.move_to((200, 280))
    char1.set_expression("surprised")
    panel1.add_content(sfx1, char1)

    # Panel 2: Motion SFX
    panel2 = Panel()
    sfx2 = SFX(
        text="WHOOSH!",
        color="#00BCD4",
        outline_color="#FFFFFF",
        outline_width=3.0,
        font_size=36.0,
        shadow=True,
        shadow_color="#00000066",
        shadow_offset=(3.0, 3.0),
    )
    sfx2.move_to((200, 100))

    char2 = Stickman(height=70)
    char2.move_to((200, 280))
    char2.set_expression("excited")
    char2.set_pose("running")
    panel2.add_content(sfx2, char2)

    # Panel 3: Soft SFX
    panel3 = Panel()
    sfx3 = SFX(
        text="*knock knock*",
        color="#795548",
        outline_color="#FFFFFF",
        outline_width=2.0,
        font_size=24.0,
    )
    sfx3.move_to((200, 100))

    char3 = Stickman(height=70)
    char3.move_to((200, 280))
    char3.set_expression("neutral")
    char3.set_pose("standing")
    bubble3 = char3.say("Come in!")
    panel3.add_content(sfx3, char3, bubble3)

    page.add(panel1, panel2, panel3)
    page.auto_layout()

    page.render("examples/output/21_sfx_demo.png")
    print("Created examples/output/21_sfx_demo.png")


def create_styled_text_demo() -> None:
    """Demonstrate StyledText for captions and labels."""
    page = Page(width=800, height=400, background_color="#ECEFF1")

    panel = Panel(width=760, height=360, background_color="#FFFFFF")

    # Location indicator (top-left)
    location = StyledText(
        text="Tokyo, Japan",
        background_color="#263238",
        padding=(8, 15, 8, 15),
        color="#FFFFFF",
        font_size=14.0,
    )
    location.move_to((80, 40))

    # Time indicator (below location)
    time_text = StyledText(
        text="10:32 AM",
        background_color="#37474F",
        padding=(5, 10, 5, 10),
        color="#ECEFF1",
        font_size=12.0,
    )
    time_text.move_to((60, 70))

    # Warning label (top-right)
    warning = StyledText(
        text="CAUTION!",
        background_color="#FFEB3B",
        padding=(8, 15, 8, 15),
        border_color="#F57F17",
        border_width=2.0,
        color="#000000",
        font_size=16.0,
    )
    warning.move_to((680, 40))

    # Character with speech
    char = Stickman(height=100)
    char.move_to((380, 200))
    char.set_expression("happy")
    bubble = char.say("StyledText is\ngreat for labels!")

    # Footnote (bottom)
    footnote = StyledText(
        text="*This is a demonstration panel",
        background_color="#E0E0E0",
        padding=(5, 10, 5, 10),
        color="#616161",
        font_size=11.0,
    )
    footnote.move_to((380, 340))

    panel.add_content(location, time_text, warning, char, bubble, footnote)
    panel.move_to((400, 200))
    page.add(panel)

    page.render("examples/output/21_styled_text_demo.png")
    print("Created examples/output/21_styled_text_demo.png")


def create_combined_demo() -> None:
    """Combine all text types in a story page."""
    page = Page(width=800, height=800, background_color="#FAFAFA")
    page.set_layout(rows=2, cols=2)

    # Panel 1: Scene setting
    panel1 = Panel()
    location = StyledText(
        text="Midnight",
        background_color="#1A237E",
        padding=(5, 12, 5, 12),
        color="#FFFFFF",
        font_size=12.0,
    )
    location.move_to((60, 30))

    narrator1 = NarratorBubble(
        text="The city was quiet...",
        fill_color="#E8EAF6",
        border_color="#3F51B5",
        font_size=13.0,
    )
    narrator1.move_to((200, 80))

    char1 = Stickman(height=70, color="#303F9F")
    char1.move_to((200, 230))
    char1.set_expression("sleepy")
    panel1.add_content(location, narrator1, char1)

    # Panel 2: Sudden action
    panel2 = Panel()
    sfx_crash = SFX(
        text="CRASH!",
        color="#D32F2F",
        outline_color="#FFCDD2",
        outline_width=4.0,
        font_size=40.0,
    )
    sfx_crash.move_to((200, 100))

    char2 = Stickman(height=70, color="#C62828")
    char2.move_to((200, 230))
    char2.set_expression("surprised")
    bubble2 = char2.shout("What?!")
    panel2.add_content(sfx_crash, char2, bubble2)

    # Panel 3: Investigation
    panel3 = Panel()
    narrator2 = NarratorBubble(
        text="He rushed to investigate.",
        fill_color="#E3F2FD",
        border_color="#1976D2",
        font_size=13.0,
    )
    narrator2.move_to((200, 50))

    sfx_steps = SFX(
        text="tap tap tap",
        color="#546E7A",
        outline_color="#FFFFFF",
        outline_width=2.0,
        font_size=18.0,
    )
    sfx_steps.move_to((200, 270))

    char3 = Stickman(height=70, color="#0277BD")
    char3.move_to((200, 180))
    char3.set_expression("confused")
    char3.set_pose("running")
    panel3.add_content(narrator2, char3, sfx_steps)

    # Panel 4: Discovery
    panel4 = Panel()
    label = StyledText(
        text="To be continued...",
        background_color="#FFF3E0",
        padding=(8, 15, 8, 15),
        border_color="#FF9800",
        border_width=2.0,
        color="#E65100",
        font_size=16.0,
    )
    label.move_to((200, 250))

    char4 = Stickman(height=70, color="#F57C00")
    char4.move_to((200, 150))
    char4.set_expression("excited")
    bubble4 = char4.say("What did\nI find?!")
    panel4.add_content(char4, bubble4, label)

    page.add(panel1, panel2, panel3, panel4)
    page.auto_layout()

    page.render("examples/output/21_combined_demo.png")
    print("Created examples/output/21_combined_demo.png")


def create_text_types_reference() -> None:
    """Create a reference showing all text types side by side."""
    page = Page(width=600, height=500, background_color="#FFFFFF")

    # Basic Text
    basic_text = Text(
        text="Basic Text",
        font_size=18.0,
        color="#333333",
    )
    basic_text.move_to((150, 60))

    # StyledText
    styled_text = StyledText(
        text="StyledText",
        background_color="#E3F2FD",
        padding=(8, 15, 8, 15),
        border_color="#1976D2",
        border_width=2.0,
        font_size=18.0,
        color="#0D47A1",
    )
    styled_text.move_to((450, 60))

    # SFX
    sfx_text = SFX(
        text="SFX!",
        color="#D32F2F",
        outline_color="#FFFFFF",
        outline_width=3.0,
        font_size=32.0,
    )
    sfx_text.move_to((150, 160))

    # SFX with shadow
    sfx_shadow = SFX(
        text="SFX+Shadow",
        color="#7B1FA2",
        outline_color="#FFFFFF",
        outline_width=2.0,
        font_size=28.0,
        shadow=True,
        shadow_offset=(4.0, 4.0),
    )
    sfx_shadow.move_to((450, 160))

    # NarratorBubble (default)
    narrator_default = NarratorBubble(
        text="NarratorBubble",
        font_size=14.0,
    )
    narrator_default.move_to((150, 280))

    # NarratorBubble (styled)
    narrator_styled = NarratorBubble(
        text="Styled Narrator",
        fill_color="#FFF9C4",
        border_color="#F9A825",
        border_width=2.0,
        font_size=14.0,
    )
    narrator_styled.move_to((450, 280))

    # Description labels
    descriptions = [
        ("Standard text element", 150, 100),
        ("Text with box styling", 450, 100),
        ("Bold sound effects", 150, 210),
        ("SFX with shadow", 450, 210),
        ("Caption for narration", 150, 340),
        ("Custom styled caption", 450, 340),
    ]

    panel = Panel(width=560, height=420, background_color="#FAFAFA")
    panel.add_content(
        basic_text,
        styled_text,
        sfx_text,
        sfx_shadow,
        narrator_default,
        narrator_styled,
    )

    for text, x, y in descriptions:
        desc = Text(text=text, font_size=11.0, color="#757575")
        desc.move_to((x, y))
        panel.add_content(desc)

    panel.move_to((300, 250))
    page.add(panel)

    page.render("examples/output/21_text_reference.png")
    print("Created examples/output/21_text_reference.png")


if __name__ == "__main__":
    create_narrator_demo()
    create_sfx_demo()
    create_styled_text_demo()
    create_combined_demo()
    create_text_types_reference()
    print("\nText and Narration examples complete!")
