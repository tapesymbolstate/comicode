"""Showcase of all 8 character types available in Comix.

This example demonstrates the variety of character styles:
1. Stickman - Simple stick figure (default)
2. SimpleFace - Emoji-style face only
3. ChubbyStickman - Rounded, friendly figure
4. Robot - Mechanical with geometric design
5. Chibi - Super-deformed anime style
6. Anime - Natural anime proportions
7. Cartoon - Western cartoon style
8. Superhero - Heroic proportions

Each character type has unique visual characteristics while sharing
the same expression and pose APIs.
"""

from comix import (
    Page,
    Panel,
    Stickman,
    SimpleFace,
    ChubbyStickman,
    Robot,
    Chibi,
    Anime,
    Cartoon,
    Superhero,
)


def create_character_showcase() -> None:
    """Create a showcase page with all 8 character types."""
    # Create a 2x4 grid page (8 panels for 8 character types)
    page = Page(width=1000, height=1200)
    page.set_layout(rows=4, cols=2)

    # Define all character types with their distinctive colors
    character_types = [
        (Stickman, "Stickman", "#2C3E50", "Simple and classic"),
        (SimpleFace, "SimpleFace", "#E74C3C", "Emoji-style face"),
        (ChubbyStickman, "ChubbyStickman", "#27AE60", "Friendly and round"),
        (Robot, "Robot", "#7F8C8D", "Mechanical design"),
        (Chibi, "Chibi", "#E91E63", "Super-deformed"),
        (Anime, "Anime", "#9C27B0", "Natural anime style"),
        (Cartoon, "Cartoon", "#FF9800", "Western cartoon"),
        (Superhero, "Superhero", "#3498DB", "Heroic proportions"),
    ]

    for i, (char_class, name, color, description) in enumerate(character_types):
        panel = Panel()

        # Create character with appropriate settings
        if char_class == SimpleFace:
            # SimpleFace is just a face, so use smaller height
            char = char_class(name=name, height=80, color=color)
        elif char_class == Robot:
            # Robot has special parameters
            char = char_class(name=name, height=120, color=color, led_color="#00FF88")
        elif char_class == Chibi:
            # Chibi has hair and outfit options
            char = char_class(name=name, height=100, color=color, hair_color="#FFD700")
        elif char_class == Anime:
            # Anime has hair style and eye color
            char = char_class(name=name, height=140, color=color, eye_color="#3498DB")
        elif char_class == Superhero:
            # Superhero has costume options
            char = char_class(name=name, height=150, color=color, cape=True)
        elif char_class == Cartoon:
            # Cartoon has body shape options
            char = char_class(name=name, height=120, color=color, body_shape="round")
        else:
            # Stickman and ChubbyStickman use default parameters
            char = char_class(name=name, height=100, color=color)

        # Position character relative to panel center (0, 0)
        # Characters are positioned slightly below center to leave room for bubble above
        char.move_to((0, 30))

        # Set a happy expression to show personality
        char.set_expression("happy")

        # Add speech bubble with description
        bubble = char.say(description)

        panel.add_content(char, bubble)
        page.add(panel)

    page.auto_layout()
    page.render("examples/output/16_character_types.png")
    print("Created examples/output/16_character_types.png")


def create_expression_comparison() -> None:
    """Create a comparison showing the same expression across different character types."""
    page = Page(width=1200, height=400)
    page.set_layout(rows=1, cols=4)

    # Select 4 representative character types
    types_to_compare = [
        (Stickman, "Stickman", "#2C3E50"),
        (ChubbyStickman, "Chubby", "#27AE60"),
        (Anime, "Anime", "#9C27B0"),
        (Robot, "Robot", "#7F8C8D"),
    ]

    for i, (char_class, name, color) in enumerate(types_to_compare):
        panel = Panel()

        if char_class == Anime:
            char = char_class(name=name, height=120, color=color)
        elif char_class == Robot:
            char = char_class(name=name, height=100, color=color)
        else:
            char = char_class(name=name, height=100, color=color)

        char.move_to((0, 30))
        char.set_expression("surprised")

        bubble = char.say("Surprised!")
        panel.add_content(char, bubble)
        page.add(panel)

    page.auto_layout()
    page.render("examples/output/16_expression_comparison.png")
    print("Created examples/output/16_expression_comparison.png")


def create_pose_showcase() -> None:
    """Create a showcase of different poses with various character types."""
    page = Page(width=1200, height=800)
    page.set_layout(rows=2, cols=3)

    # Character type and pose combinations
    pose_demos = [
        (Stickman, "standing", "#2C3E50"),
        (ChubbyStickman, "waving", "#27AE60"),
        (Anime, "pointing", "#9C27B0"),
        (Superhero, "jumping", "#3498DB"),
        (Cartoon, "dancing", "#FF9800"),
        (Robot, "walking", "#7F8C8D"),
    ]

    for i, (char_class, pose, color) in enumerate(pose_demos):
        panel = Panel()

        if char_class == Anime:
            char = char_class(height=130, color=color)
        elif char_class == Superhero:
            char = char_class(height=140, color=color, cape=True)
        elif char_class == Robot:
            char = char_class(height=110, color=color)
        elif char_class == Cartoon:
            char = char_class(height=110, color=color)
        else:
            char = char_class(height=100, color=color)

        char.move_to((0, 30))
        char.set_pose(pose)

        bubble = char.say(f"{pose.title()}!")
        panel.add_content(char, bubble)
        page.add(panel)

    page.auto_layout()
    page.render("examples/output/16_pose_showcase.png")
    print("Created examples/output/16_pose_showcase.png")


if __name__ == "__main__":
    create_character_showcase()
    create_expression_comparison()
    create_pose_showcase()
    print("\nAll character type examples created successfully!")
