"""Showcase of all 9 character types available in Comix.

This example demonstrates the variety of character styles:
1. Stickman - Simple stick figure (default)
2. SimpleFace - Emoji-style face only
3. ChubbyStickman - Rounded, friendly figure
4. Robot - Mechanical with geometric design
5. Chibi - Super-deformed anime style
6. Anime - Natural anime proportions
7. Cartoon - Western cartoon style
8. Superhero - Heroic proportions
9. AnimalStyle - Anthropomorphic animal characters

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
    AnimalStyle,
)


def create_character_showcase() -> None:
    """Create a showcase page with all 9 character types."""
    # Create a 3x3 grid page (9 panels for 9 character types)
    page = Page(width=1200, height=1200)
    page.set_layout(rows=3, cols=3)

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
        (AnimalStyle, "AnimalStyle", "#8B4513", "Furry friends"),
    ]

    # Panel positions for 3x3 grid on 1200x1200 page
    # Columns at x=210, 600, 990; Rows at y=210, 600, 990
    panel_positions = [
        (210, 210), (600, 210), (990, 210),
        (210, 600), (600, 600), (990, 600),
        (210, 990), (600, 990), (990, 990),
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
        elif char_class == AnimalStyle:
            # AnimalStyle has species presets
            char = char_class(name=name, height=120, species="cat", fur_color=color)
        else:
            # Stickman and ChubbyStickman use default parameters
            char = char_class(name=name, height=100, color=color)

        # Position character using global coordinates
        char.move_to(panel_positions[i])

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
    page = Page(width=1500, height=400)
    page.set_layout(rows=1, cols=5)

    # Select 5 representative character types (now including AnimalStyle)
    types_to_compare = [
        (Stickman, "Stickman", "#2C3E50"),
        (ChubbyStickman, "Chubby", "#27AE60"),
        (Anime, "Anime", "#9C27B0"),
        (Robot, "Robot", "#7F8C8D"),
        (AnimalStyle, "Fox", "#D2691E"),
    ]

    # Panel positions for 5x1 grid on 1500x400 page
    panel_positions = [
        (160, 200), (460, 200), (760, 200), (1060, 200), (1360, 200),
    ]

    for i, (char_class, name, color) in enumerate(types_to_compare):
        panel = Panel()

        if char_class == Anime:
            char = char_class(name=name, height=120, color=color)
        elif char_class == Robot:
            char = char_class(name=name, height=100, color=color)
        elif char_class == AnimalStyle:
            char = char_class(name=name, height=110, species="fox", fur_color=color)
        else:
            char = char_class(name=name, height=100, color=color)

        char.move_to(panel_positions[i])
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
        (AnimalStyle, "walking", "#8B4513"),
    ]

    # Panel positions for 3x2 grid on 1200x800 page
    # Columns at x=210, 600, 990; Rows at y=207.5, 592.5
    panel_positions = [
        (210, 207.5), (600, 207.5), (990, 207.5),
        (210, 592.5), (600, 592.5), (990, 592.5),
    ]

    for i, (char_class, pose, color) in enumerate(pose_demos):
        panel = Panel()

        if char_class == Anime:
            char = char_class(height=130, color=color)
        elif char_class == Superhero:
            char = char_class(height=140, color=color, cape=True)
        elif char_class == AnimalStyle:
            char = char_class(height=120, species="dog", fur_color=color)
        elif char_class == Cartoon:
            char = char_class(height=110, color=color)
        else:
            char = char_class(height=100, color=color)

        char.move_to(panel_positions[i])
        char.set_pose(pose)

        bubble = char.say(f"{pose.title()}!")
        panel.add_content(char, bubble)
        page.add(panel)

    page.auto_layout()
    page.render("examples/output/16_pose_showcase.png")
    print("Created examples/output/16_pose_showcase.png")


def create_animal_species_showcase() -> None:
    """Create a showcase of different animal species in AnimalStyle."""
    page = Page(width=1400, height=600)
    page.set_layout(rows=2, cols=4)

    # All 7 species presets available in AnimalStyle
    species_list = [
        ("cat", "#FF8C00", "Meow!"),
        ("dog", "#8B4513", "Woof!"),
        ("rabbit", "#FFB6C1", "Hop hop!"),
        ("fox", "#D2691E", "Clever!"),
        ("bear", "#4A3728", "Roar!"),
        ("bird", "#FFD700", "Tweet!"),
        ("wolf", "#696969", "Howl!"),
    ]

    # Panel positions for 4x2 grid on 1400x600 page
    panel_positions = [
        (185, 157.5), (535, 157.5), (885, 157.5), (1235, 157.5),
        (185, 442.5), (535, 442.5), (885, 442.5), (1235, 442.5),
    ]

    for i, (species, fur_color, speech) in enumerate(species_list):
        panel = Panel()

        char = AnimalStyle(
            name=species.title(),
            height=100,
            species=species,
            fur_color=fur_color,
        )
        char.move_to(panel_positions[i])
        char.set_expression("happy")

        bubble = char.say(speech)
        panel.add_content(char, bubble)
        page.add(panel)

    # Add empty 8th panel (for grid completion)
    page.add(Panel())

    page.auto_layout()
    page.render("examples/output/16_animal_species.png")
    print("Created examples/output/16_animal_species.png")


if __name__ == "__main__":
    create_character_showcase()
    create_expression_comparison()
    create_pose_showcase()
    create_animal_species_showcase()
    print("\nAll character type examples created successfully!")
