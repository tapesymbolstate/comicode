"""Advanced Templates: ThreeRowLayout and MangaPage.

Beyond basic templates like FourKoma and TwoByTwo, Comix provides
more sophisticated page layouts for professional manga and comic work:

- ThreeRowLayout: Flexible rows with varying panel counts
- MangaPage: Preset-based layouts for common manga patterns

This example demonstrates:
- ThreeRowLayout with custom panel configurations
- MangaPage with different presets (six_panel, dialogue, action)
- Custom row heights and proportions
- Combining templates for varied page designs
"""
# Status: ✅ Working (v0.1.108)

from comix import Stickman
from comix.page.templates import ThreeRowLayout, MangaPage


def create_three_row_basic() -> None:
    """Basic ThreeRowLayout with default [1, 2, 1] configuration."""
    page = ThreeRowLayout(width=600, height=800)

    # Row 1: Single wide establishing shot
    char1 = Stickman(height=100, color="#1976D2")
    char1.move_to((290, 130))
    char1.set_expression("neutral")
    bubble1 = char1.say("ThreeRowLayout default:\n1 panel - 2 panels - 1 panel")
    page.rows[0][0].add_content(char1, bubble1)

    # Row 2: Two panels for dialogue
    char2a = Stickman(height=70, color="#E91E63")
    char2a.move_to((135, 130))
    char2a.set_expression("happy")
    bubble2a = char2a.say("Left panel!")
    page.rows[1][0].add_content(char2a, bubble2a)

    char2b = Stickman(height=70, color="#4CAF50")
    char2b.move_to((135, 130))
    char2b.set_expression("excited")
    bubble2b = char2b.say("Right panel!")
    page.rows[1][1].add_content(char2b, bubble2b)

    # Row 3: Single wide reaction panel
    char3 = Stickman(height=100, color="#FF9800")
    char3.move_to((290, 130))
    char3.set_expression("surprised")
    bubble3 = char3.shout("Great for pacing!")
    page.rows[2][0].add_content(char3, bubble3)

    page.render("examples/output/22_three_row_basic.png")
    print("Created examples/output/22_three_row_basic.png")


def create_three_row_custom() -> None:
    """ThreeRowLayout with custom panel counts [2, 3, 2]."""
    page = ThreeRowLayout(
        width=700,
        height=900,
        row_panels=[2, 3, 2],
        row_heights=[1.0, 1.2, 1.0],  # Middle row is taller
    )

    # Row 1: Two introduction panels
    chars_row1 = [
        ("Alice", "#FF6B9D", "happy", "Hi there!"),
        ("Bob", "#4ECDC4", "excited", "Hello!"),
    ]
    for i, (name, color, expr, text) in enumerate(chars_row1):
        char = Stickman(height=70, color=color)
        char.move_to((170, 120))
        char.set_expression(expr)
        bubble = char.say(text)
        page.rows[0][i].add_content(char, bubble)

    # Row 2: Three action panels
    actions = [
        ("surprised", "What?!", 100),
        ("angry", "No way!", 100),
        ("scared", "Yikes!", 100),
    ]
    for i, (expr, text, height) in enumerate(actions):
        char = Stickman(height=height, color="#7B1FA2")
        char.move_to((110, 140))
        char.set_expression(expr)
        bubble = char.say(text)
        page.rows[1][i].add_content(char, bubble)

    # Row 3: Two resolution panels
    conclusions = [
        ("confused", "So...what happened?"),
        ("sleepy", "I'm so tired now..."),
    ]
    for i, (expr, text) in enumerate(conclusions):
        char = Stickman(height=70, color="#607D8B")
        char.move_to((170, 120))
        char.set_expression(expr)
        bubble = char.say(text)
        page.rows[2][i].add_content(char, bubble)

    page.render("examples/output/22_three_row_custom.png")
    print("Created examples/output/22_three_row_custom.png")


def create_manga_six_panel() -> None:
    """MangaPage with six_panel preset (2 rows x 3 columns)."""
    page = MangaPage(preset="six_panel", width=700, height=600)

    # Create a sequence across 6 panels
    sequence = [
        ("neutral", "Panel 1", "#F44336"),
        ("happy", "Panel 2", "#E91E63"),
        ("excited", "Panel 3", "#9C27B0"),
        ("confused", "Panel 4", "#673AB7"),
        ("surprised", "Panel 5", "#3F51B5"),
        ("sad", "Panel 6", "#2196F3"),
    ]

    for i, (expr, text, color) in enumerate(sequence):
        char = Stickman(height=60, color=color)
        char.move_to((115, 130))
        char.set_expression(expr)
        bubble = char.say(text)
        page.panels[i].add_content(char, bubble)

    page.auto_layout()
    page.render("examples/output/22_manga_six_panel.png")
    print("Created examples/output/22_manga_six_panel.png")


def create_manga_dialogue() -> None:
    """MangaPage with dialogue preset (3 rows x 2 columns)."""
    page = MangaPage(preset="dialogue", width=600, height=900)

    # A conversation between two characters
    dialogue = [
        (True, "happy", "Hey, did you hear?"),
        (False, "confused", "Hear what?"),
        (True, "excited", "We got the deal!"),
        (False, "surprised", "No way!"),
        (True, "excited", "Yes way!"),
        (False, "happy", "That's amazing!"),
    ]

    for i, (is_alice, expr, text) in enumerate(dialogue):
        if is_alice:
            char = Stickman(height=80, color="#E91E63")
            char.move_to((150, 140))
        else:
            char = Stickman(height=80, color="#2196F3")
            char.move_to((150, 140))

        char.set_expression(expr)
        bubble = char.say(text)
        page.panels[i].add_content(char, bubble)

    page.auto_layout()
    page.render("examples/output/22_manga_dialogue.png")
    print("Created examples/output/22_manga_dialogue.png")


def create_manga_action() -> None:
    """MangaPage with action preset (2 rows x 2 columns)."""
    page = MangaPage(preset="action", width=600, height=600)

    # Action sequence
    actions = [
        ("excited", "jumping", "Here I go!"),
        ("angry", "running", "Can't stop me!"),
        ("scared", "standing", "Oh no..."),
        ("surprised", "cheering", "I did it!"),
    ]

    for i, (expr, pose, text) in enumerate(actions):
        char = Stickman(height=80, color="#FF5722")
        char.move_to((150, 150))
        char.set_expression(expr)
        char.set_pose(pose)
        bubble = char.say(text)
        page.panels[i].add_content(char, bubble)

    page.auto_layout()
    page.render("examples/output/22_manga_action.png")
    print("Created examples/output/22_manga_action.png")


def create_manga_custom() -> None:
    """MangaPage with custom rows/cols configuration."""
    # Create a 4x2 layout (4 rows, 2 columns = 8 panels)
    page = MangaPage(rows=4, cols=2, width=600, height=1000)

    # Fill panels with a mini-story
    story = [
        ("neutral", "It was a normal day..."),
        ("happy", "I was happy!"),
        ("confused", "Then something odd happened"),
        ("surprised", "What was that?!"),
        ("scared", "I was terrified!"),
        ("angry", "But then I got mad!"),
        ("excited", "I faced my fears!"),
        ("happy", "And won! The end."),
    ]

    colors = [
        "#F44336", "#E91E63", "#9C27B0", "#3F51B5",
        "#00BCD4", "#4CAF50", "#FF9800", "#795548",
    ]

    for i, ((expr, text), color) in enumerate(zip(story, colors)):
        char = Stickman(height=70, color=color)
        char.move_to((150, 120))
        char.set_expression(expr)
        bubble = char.say(text)
        page.panels[i].add_content(char, bubble)

    page.auto_layout()
    page.render("examples/output/22_manga_custom.png")
    print("Created examples/output/22_manga_custom.png")


def create_three_row_dramatic() -> None:
    """ThreeRowLayout with dramatic height ratios."""
    # [1, 3, 1] panels with [0.3, 1.0, 0.3] heights
    # Creates a dramatic middle row that dominates the page
    page = ThreeRowLayout(
        width=600,
        height=900,
        row_panels=[1, 3, 1],
        row_heights=[0.3, 1.0, 0.3],
    )

    # Top row: Quick setup
    char_top = Stickman(height=60, color="#37474F")
    char_top.move_to((290, 60))
    char_top.set_expression("neutral")
    bubble_top = char_top.say("Meanwhile...")
    page.rows[0][0].add_content(char_top, bubble_top)

    # Middle row: Three dramatic panels
    dramatic = [
        ("surprised", "jumping", "#D32F2F", "NOW!"),
        ("angry", "cheering", "#C2185B", "CHARGE!"),
        ("excited", "running", "#7B1FA2", "GO!"),
    ]

    for i, (expr, pose, color, text) in enumerate(dramatic):
        char = Stickman(height=150, color=color)
        char.move_to((100, 200))
        char.set_expression(expr)
        char.set_pose(pose)
        bubble = char.shout(text)
        page.rows[1][i].add_content(char, bubble)

    # Bottom row: Quick ending
    char_bottom = Stickman(height=60, color="#37474F")
    char_bottom.move_to((290, 60))
    char_bottom.set_expression("sleepy")
    bubble_bottom = char_bottom.say("That was exhausting...")
    page.rows[2][0].add_content(char_bottom, bubble_bottom)

    page.render("examples/output/22_three_row_dramatic.png")
    print("Created examples/output/22_three_row_dramatic.png")


if __name__ == "__main__":
    # ThreeRowLayout examples
    create_three_row_basic()
    create_three_row_custom()
    create_three_row_dramatic()

    # MangaPage examples
    create_manga_six_panel()
    create_manga_dialogue()
    create_manga_action()
    create_manga_custom()

    print("\nAdvanced Templates examples complete!")
