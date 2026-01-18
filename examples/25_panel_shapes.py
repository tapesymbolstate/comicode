"""Advanced panel shapes for dynamic comic layouts.

This example demonstrates non-rectangular panel types:
- DiagonalPanel: Panels with cut corners for dramatic effect
- TrapezoidPanel: Perspective-style panels (wider at one end)
- StarburstPanel: Star-shaped panels for shock/surprise moments
- CloudPanel: Dreamy cloud-shaped panels for flashbacks
- ExplosionPanel: Jagged explosion panels for action scenes
- Panel splitting: split_diagonal() and split_curve() methods
"""
# Status: ✅ Working (v0.1.108)

from comix import (
    Page,
    Panel,
    Stickman,
    DiagonalPanel,
    TrapezoidPanel,
    StarburstPanel,
    CloudPanel,
    ExplosionPanel,
)


def create_diagonal_panels_example():
    """DiagonalPanel: Panels with cut corners."""
    print("Creating diagonal panels example...")
    page = Page(width=800, height=600, background_color="#F5F5F5")

    # Four diagonal panels showing different cut directions
    directions = ["top-left", "top-right", "bottom-left", "bottom-right"]
    positions = [(200, 150), (600, 150), (200, 450), (600, 450)]
    expressions = ["surprised", "excited", "confused", "scared"]

    for direction, pos, expr in zip(directions, positions, expressions):
        panel = DiagonalPanel(
            width=300,
            height=200,
            diagonal_angle=45,
            direction=direction,
            background_color="#FFFFFF",
        )
        panel.move_to(pos)

        char = Stickman(height=80)
        char.move_to(pos)
        char.set_expression(expr)
        bubble = char.say(f"{direction} cut!")
        panel.add_content(char, bubble)
        page.add(panel)

    page.render("examples/output/25_diagonal_panels.png")


def create_trapezoid_panel_example():
    """TrapezoidPanel: Perspective panels for depth effect."""
    print("Creating trapezoid panel example...")
    page = Page(width=800, height=600, background_color="#E8E8E8")

    # Trapezoid panel - wider at top (approaching viewer)
    trap1 = TrapezoidPanel(
        top_width=400,
        bottom_width=200,
        height=250,
        background_color="#FFFFFF",
    )
    trap1.move_to((250, 300))

    char1 = Stickman(height=100)
    char1.move_to((250, 300))
    char1.set_expression("excited")
    char1.set_pose("running")
    bubble1 = char1.shout("Coming at you!")
    trap1.add_content(char1, bubble1)
    page.add(trap1)

    # Trapezoid panel - wider at bottom (receding)
    trap2 = TrapezoidPanel(
        top_width=200,
        bottom_width=400,
        height=250,
        background_color="#FFFFFF",
    )
    trap2.move_to((600, 300))

    char2 = Stickman(height=70)
    char2.move_to((600, 320))
    char2.set_expression("sad")
    char2.set_pose("walking")
    bubble2 = char2.say("Walking away...")
    trap2.add_content(char2, bubble2)
    page.add(trap2)

    page.render("examples/output/25_trapezoid_panels.png")


def create_starburst_panel_example():
    """StarburstPanel: Dramatic star shapes for impact moments."""
    print("Creating starburst panel example...")
    page = Page(width=800, height=600, background_color="#2C2C2C")

    # Main starburst for dramatic reveal
    starburst = StarburstPanel(
        width=500,
        height=500,
        num_points=12,
        inner_ratio=0.4,
        background_color="#FFD700",
    )
    starburst.move_to((400, 300))

    char = Stickman(height=150, color="#000000")
    char.move_to((400, 300))
    char.set_expression("excited")
    char.set_pose("cheering")
    bubble = char.shout("VICTORY!")
    starburst.add_content(char, bubble)
    page.add(starburst)

    page.render("examples/output/25_starburst_panel.png")


def create_cloud_panel_example():
    """CloudPanel: Soft cloud shapes for dreams and flashbacks."""
    print("Creating cloud panel example...")
    page = Page(width=800, height=600, background_color="#87CEEB")

    # Cloud panel for a dream sequence
    cloud = CloudPanel(
        width=500,
        height=350,
        num_bumps=10,
        bumpiness=0.35,
        background_color="#FFFFFF",
    )
    cloud.move_to((400, 300))

    char = Stickman(height=80)
    char.move_to((400, 300))
    char.set_expression("sleepy")
    char.set_pose("lying")
    bubble = char.think("In my dreams...")
    cloud.add_content(char, bubble)
    page.add(cloud)

    page.render("examples/output/25_cloud_panel.png")


def create_explosion_panel_example():
    """ExplosionPanel: Jagged shapes for action and impact."""
    print("Creating explosion panel example...")
    page = Page(width=800, height=600, background_color="#333333")

    # Explosion panel for action scene
    explosion = ExplosionPanel(
        width=550,
        height=500,
        num_rays=16,
        ray_depth=0.45,
        randomness=0.25,
        seed=42,
        background_color="#FF4500",
    )
    explosion.move_to((400, 300))

    char = Stickman(height=120, color="#FFFFFF")
    char.move_to((400, 300))
    char.set_expression("angry")
    char.set_pose("jumping")
    bubble = char.shout("BOOM!")
    explosion.add_content(char, bubble)
    page.add(explosion)

    page.render("examples/output/25_explosion_panel.png")


def create_split_diagonal_example():
    """Panel.split_diagonal(): Split panels into triangles."""
    print("Creating split diagonal example...")
    page = Page(width=800, height=600, background_color="#F0F0F0")

    # Create a panel and split it diagonally
    original = Panel(
        width=350,
        height=350,
        background_color="#FFFFFF",
    )
    original.move_to((400, 300))

    # Split into two triangular panels
    upper_panel, lower_panel = original.split_diagonal(
        direction="top-left-to-bottom-right"
    )

    # Add different backgrounds to distinguish
    upper_panel.background_color = "#E3F2FD"
    lower_panel.background_color = "#FFF3E0"

    # Position them side by side for visibility
    upper_panel.move_to((250, 300))
    lower_panel.move_to((550, 300))

    # Add characters to each split panel
    char1 = Stickman(height=70)
    char1.move_to((250, 320))
    char1.set_expression("happy")
    bubble1 = char1.say("Top half!")
    upper_panel.add_content(char1, bubble1)

    char2 = Stickman(height=70)
    char2.move_to((550, 320))
    char2.set_expression("surprised")
    bubble2 = char2.say("Bottom half!")
    lower_panel.add_content(char2, bubble2)

    page.add(upper_panel, lower_panel)
    page.render("examples/output/25_split_diagonal.png")


def create_split_curve_example():
    """Panel.split_curve(): Split panels with curved bezier lines."""
    print("Creating split curve example...")
    page = Page(width=800, height=600, background_color="#F0F0F0")

    # Create and split with curved line
    original = Panel(
        width=350,
        height=350,
        background_color="#FFFFFF",
    )
    original.move_to((400, 300))

    # Split with an S-curve
    left_panel, right_panel = original.split_curve(
        direction="top-left-to-bottom-right",
        curve_intensity=0.4,
        num_curve_points=30,
    )

    # Add different backgrounds
    left_panel.background_color = "#E8F5E9"
    right_panel.background_color = "#FCE4EC"

    # Position for visibility
    left_panel.move_to((250, 300))
    right_panel.move_to((550, 300))

    # Add characters
    char1 = Stickman(height=70)
    char1.move_to((250, 320))
    char1.set_expression("confused")
    bubble1 = char1.say("Curved left!")
    left_panel.add_content(char1, bubble1)

    char2 = Stickman(height=70)
    char2.move_to((550, 320))
    char2.set_expression("excited")
    bubble2 = char2.say("Curved right!")
    right_panel.add_content(char2, bubble2)

    page.add(left_panel, right_panel)
    page.render("examples/output/25_split_curve.png")


def create_mixed_shapes_comic():
    """Complete comic page using multiple panel shapes."""
    print("Creating mixed shapes comic...")
    page = Page(width=800, height=1000, background_color="#FFFFFF")

    # Panel 1: Regular panel (setup)
    panel1 = Panel(width=350, height=200, background_color="#F5F5F5")
    panel1.move_to((200, 120))
    char1 = Stickman(height=70)
    char1.move_to((200, 130))
    char1.set_expression("neutral")
    bubble1 = char1.say("Just a normal day...")
    panel1.add_content(char1, bubble1)
    page.add(panel1)

    # Panel 2: Diagonal panel (tension)
    panel2 = DiagonalPanel(
        width=350, height=200,
        direction="bottom-right",
        background_color="#FFF8E1"
    )
    panel2.move_to((600, 120))
    char2 = Stickman(height=70)
    char2.move_to((600, 130))
    char2.set_expression("surprised")
    bubble2 = char2.say("Wait, what's that?!")
    panel2.add_content(char2, bubble2)
    page.add(panel2)

    # Panel 3: Explosion panel (action!)
    panel3 = ExplosionPanel(
        width=400, height=350,
        num_rays=14,
        ray_depth=0.4,
        randomness=0.2,
        seed=123,
        background_color="#FF6B6B"
    )
    panel3.move_to((250, 400))
    char3 = Stickman(height=100, color="#FFFFFF")
    char3.move_to((250, 400))
    char3.set_expression("angry")
    char3.set_pose("jumping")
    bubble3 = char3.shout("KABOOM!")
    panel3.add_content(char3, bubble3)
    page.add(panel3)

    # Panel 4: Cloud panel (aftermath dream)
    panel4 = CloudPanel(
        width=300, height=250,
        num_bumps=8,
        bumpiness=0.3,
        background_color="#E1F5FE"
    )
    panel4.move_to((600, 420))
    char4 = Stickman(height=60)
    char4.move_to((600, 430))
    char4.set_expression("sleepy")
    bubble4 = char4.think("Was it a dream?")
    panel4.add_content(char4, bubble4)
    page.add(panel4)

    # Panel 5: Trapezoid (walking away)
    panel5 = TrapezoidPanel(
        top_width=200,
        bottom_width=350,
        height=200,
        background_color="#F5F5F5"
    )
    panel5.move_to((250, 720))
    char5 = Stickman(height=60)
    char5.move_to((250, 730))
    char5.set_expression("confused")
    char5.set_pose("walking")
    bubble5 = char5.say("Better go home...")
    panel5.add_content(char5, bubble5)
    page.add(panel5)

    # Panel 6: Starburst (surprise ending!)
    panel6 = StarburstPanel(
        width=300, height=280,
        num_points=10,
        inner_ratio=0.45,
        background_color="#FFD700"
    )
    panel6.move_to((580, 740))
    char6 = Stickman(height=80, color="#000000")
    char6.move_to((580, 750))
    char6.set_expression("excited")
    char6.set_pose("cheering")
    bubble6 = char6.shout("THE END!")
    panel6.add_content(char6, bubble6)
    page.add(panel6)

    page.render("examples/output/25_mixed_shapes_comic.png")


if __name__ == "__main__":
    create_diagonal_panels_example()
    create_trapezoid_panel_example()
    create_starburst_panel_example()
    create_cloud_panel_example()
    create_explosion_panel_example()
    create_split_diagonal_example()
    create_split_curve_example()
    create_mixed_shapes_comic()
    print("\nCreated all panel shape examples in examples/output/")
