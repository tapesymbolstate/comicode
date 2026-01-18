"""ConstraintLayout for precise, relational positioning.

ConstraintLayout is the most sophisticated layout system in Comix.
It allows you to define relationships between elements using constraints
like "panel2.left = panel1.right + 10" or "panel.center_x = container.center_x".

This example demonstrates:
- Basic edge constraints (left, right, top, bottom)
- Relative positioning between elements
- Center alignment and proportional sizing
- Complex multi-panel arrangements
"""

from comix import Page, Panel, Stickman
from comix.layout.constraints import ConstraintLayout


def create_basic_constraints() -> None:
    """Basic constraint positioning - edges relative to container."""
    page = Page(width=800, height=600, background_color="#FAFAFA")

    # Create panels
    panel1 = Panel(width=200, height=250, background_color="#E3F2FD")
    panel2 = Panel(width=200, height=250, background_color="#FCE4EC")
    panel3 = Panel(width=420, height=200, background_color="#E8F5E9")

    # Add characters
    alice = Stickman(height=80, color="#1976D2")
    alice.move_to((100, 150))
    alice.set_expression("happy")
    bubble1 = alice.say("Top left!")
    panel1.add_content(alice, bubble1)

    bob = Stickman(height=80, color="#C2185B")
    bob.move_to((100, 150))
    bob.set_expression("excited")
    bubble2 = bob.say("Top right!")
    panel2.add_content(bob, bubble2)

    charlie = Stickman(height=70, color="#388E3C")
    charlie.move_to((210, 100))
    charlie.set_expression("surprised")
    bubble3 = charlie.say("I span the full width below!")
    panel3.add_content(charlie, bubble3)

    # Create constraint layout
    layout = ConstraintLayout(width=800, height=600)

    # Panel 1: Fixed to top-left corner with margin
    layout.add(
        panel1,
        left=layout.left + 20,
        top=layout.top + 20,
        width=200,
        height=250,
    )

    # Panel 2: Right side, same vertical position as panel 1
    layout.add(
        panel2,
        right=layout.right - 20,
        top=layout.top + 20,
        width=200,
        height=250,
    )

    # Panel 3: Below both panels, spans the width
    layout.add(
        panel3,
        left=layout.left + 20,
        right=layout.right - 20,
        top=layout.ref(panel1).bottom + 20,
        height=200,
    )

    # Solve and apply
    layout.apply()

    page.add(panel1, panel2, panel3)
    page.render("examples/output/19_basic_constraints.png")
    print("Created examples/output/19_basic_constraints.png")


def create_relative_positioning() -> None:
    """Position elements relative to each other."""
    page = Page(width=800, height=600, background_color="#FFF8E1")

    # Create a chain of panels positioned relative to each other
    panels = [
        Panel(width=150, height=150, background_color="#FFCCBC"),
        Panel(width=150, height=150, background_color="#D7CCC8"),
        Panel(width=150, height=150, background_color="#CFD8DC"),
        Panel(width=150, height=150, background_color="#C5CAE9"),
    ]

    expressions = ["neutral", "happy", "excited", "surprised"]
    for i, (panel, expr) in enumerate(zip(panels, expressions)):
        char = Stickman(height=60)
        char.move_to((75, 90))
        char.set_expression(expr)
        bubble = char.say(f"#{i + 1}")
        panel.add_content(char, bubble)

    layout = ConstraintLayout(width=800, height=600)

    # First panel: centered horizontally at top
    layout.add(
        panels[0],
        center_x=layout.center_x,
        top=layout.top + 30,
        width=150,
        height=150,
    )

    # Second panel: to the right and below panel 1
    layout.add(
        panels[1],
        left=layout.ref(panels[0]).right + 20,
        top=layout.ref(panels[0]).bottom + 20,
        width=150,
        height=150,
    )

    # Third panel: to the left of and below panel 1
    layout.add(
        panels[2],
        right=layout.ref(panels[0]).left - 20,
        top=layout.ref(panels[0]).bottom + 20,
        width=150,
        height=150,
    )

    # Fourth panel: centered below panels 2 and 3
    layout.add(
        panels[3],
        center_x=layout.center_x,
        top=layout.ref(panels[1]).bottom + 20,
        width=150,
        height=150,
    )

    layout.apply()

    for panel in panels:
        page.add(panel)

    page.render("examples/output/19_relative_positioning.png")
    print("Created examples/output/19_relative_positioning.png")


def create_proportional_layout() -> None:
    """Use arithmetic on constraints for proportional sizing."""
    page = Page(width=900, height=600, background_color="#ECEFF1")

    # Create panels that share space proportionally
    main_panel = Panel(width=400, height=400, background_color="#B3E5FC")
    side_panel1 = Panel(width=200, height=195, background_color="#C8E6C9")
    side_panel2 = Panel(width=200, height=195, background_color="#FFECB3")

    # Add content
    hero = Stickman(height=120, color="#0277BD")
    hero.move_to((200, 200))
    hero.set_expression("excited")
    hero.set_pose("cheering")
    bubble_hero = hero.shout("Main panel!")
    main_panel.add_content(hero, bubble_hero)

    char1 = Stickman(height=60, color="#2E7D32")
    char1.move_to((100, 100))
    char1.set_expression("happy")
    bubble1 = char1.say("Side 1")
    side_panel1.add_content(char1, bubble1)

    char2 = Stickman(height=60, color="#FF8F00")
    char2.move_to((100, 100))
    char2.set_expression("neutral")
    bubble2 = char2.say("Side 2")
    side_panel2.add_content(char2, bubble2)

    layout = ConstraintLayout(width=900, height=600)
    margin = 20
    gutter = 15

    # Main panel: takes 2/3 of width
    layout.add(
        main_panel,
        left=layout.left + margin,
        top=layout.top + margin,
        width=(layout.container_width - margin * 2 - gutter) * 0.66,
        bottom=layout.bottom - margin,
    )

    # Side panels: share remaining 1/3 vertically
    layout.add(
        side_panel1,
        left=layout.ref(main_panel).right + gutter,
        right=layout.right - margin,
        top=layout.top + margin,
        height=(layout.container_height - margin * 2 - gutter) / 2,
    )

    layout.add(
        side_panel2,
        left=layout.ref(main_panel).right + gutter,
        right=layout.right - margin,
        top=layout.ref(side_panel1).bottom + gutter,
        bottom=layout.bottom - margin,
    )

    layout.apply()

    page.add(main_panel, side_panel1, side_panel2)
    page.render("examples/output/19_proportional_layout.png")
    print("Created examples/output/19_proportional_layout.png")


def create_manga_style_layout() -> None:
    """Create a complex manga-style page using constraints."""
    page = Page(width=700, height=1000, background_color="#FFFFFF")

    # Create panels for a dynamic manga layout
    splash = Panel(width=400, height=350, background_color="#F3E5F5")
    top_right = Panel(width=250, height=170, background_color="#E8EAF6")
    mid_right = Panel(width=250, height=170, background_color="#E0F7FA")
    bottom_left = Panel(width=200, height=280, background_color="#FFF3E0")
    bottom_mid = Panel(width=200, height=280, background_color="#E8F5E9")
    bottom_right = Panel(width=250, height=280, background_color="#FFEBEE")

    # Add dramatic content
    hero = Stickman(height=150, color="#7B1FA2")
    hero.move_to((200, 180))
    hero.set_expression("excited")
    hero.set_pose("jumping")
    bubble_hero = hero.shout("Dynamic entry!")
    splash.add_content(hero, bubble_hero)

    # Add supporting characters
    chars = [
        (top_right, "surprised", "What?!", 50),
        (mid_right, "scared", "No way!", 50),
        (bottom_left, "confused", "Huh?", 60),
        (bottom_mid, "angry", "You!", 60),
        (bottom_right, "happy", "Amazing!", 70),
    ]

    for panel, expr, text, height in chars:
        char = Stickman(height=height)
        char.move_to((panel.width / 2, panel.height / 2))
        char.set_expression(expr)
        bubble = char.say(text)
        panel.add_content(char, bubble)

    # Complex constraint layout
    layout = ConstraintLayout(width=700, height=1000)
    margin = 15
    gutter = 10

    # Splash panel: large area top-left
    layout.add(
        splash,
        left=layout.left + margin,
        top=layout.top + margin,
        width=400,
        height=350,
    )

    # Top right: small panel
    layout.add(
        top_right,
        left=layout.ref(splash).right + gutter,
        right=layout.right - margin,
        top=layout.top + margin,
        height=170,
    )

    # Mid right: below top right
    layout.add(
        mid_right,
        left=layout.ref(splash).right + gutter,
        right=layout.right - margin,
        top=layout.ref(top_right).bottom + gutter,
        height=170,
    )

    # Bottom row: three panels
    layout.add(
        bottom_left,
        left=layout.left + margin,
        top=layout.ref(splash).bottom + gutter,
        width=200,
        bottom=layout.bottom - margin,
    )

    layout.add(
        bottom_mid,
        left=layout.ref(bottom_left).right + gutter,
        top=layout.ref(splash).bottom + gutter,
        width=200,
        bottom=layout.bottom - margin,
    )

    layout.add(
        bottom_right,
        left=layout.ref(bottom_mid).right + gutter,
        right=layout.right - margin,
        top=layout.ref(mid_right).bottom + gutter,
        bottom=layout.bottom - margin,
    )

    layout.apply()

    page.add(splash, top_right, mid_right, bottom_left, bottom_mid, bottom_right)
    page.render("examples/output/19_manga_style.png")
    print("Created examples/output/19_manga_style.png")


if __name__ == "__main__":
    create_basic_constraints()
    create_relative_positioning()
    create_proportional_layout()
    create_manga_style_layout()
    print("\nConstraintLayout examples complete!")
