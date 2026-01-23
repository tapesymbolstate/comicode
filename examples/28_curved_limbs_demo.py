#!/usr/bin/env python3
"""Example 28: Curved Limbs Demonstration.

This example specifically demonstrates the natural curve effect applied to
character limbs and torso in hand-drawn style. Uses extended poses to make
the curves clearly visible.
"""

from pathlib import Path

from comix import Page, Panel, Stickman, Style


def create_curved_limbs_demo() -> Page:
    """Demonstrate curved limbs with extended poses."""
    page = Page(width=1400, height=500, background_color="#FFFFFF")

    # Left: Normal rendering (straight lines)
    panel1 = Panel(width=650, height=450)
    panel1.move_to((340, 250))

    char1 = Stickman(name="Normal", height=150, proportion_style="xkcd")
    char1.move_to((340, 300))
    char1.set_expression("neutral")
    # Extended pose to show lines clearly
    char1.set_arm_angles(left_shoulder=160, left_elbow=30, right_shoulder=20, right_elbow=30)
    char1.set_leg_angles(left_hip=30, left_knee=20, right_hip=150, right_knee=20)

    bubble1 = char1.say("Straight lines\\n(normal)", width=180, height=70)

    panel1.add_content(char1, bubble1)
    page.add(panel1)

    # Right: Hand-drawn with curved limbs
    panel2 = Panel(width=650, height=450)
    panel2.move_to((1060, 250))
    panel2.set_style(Style(hand_drawn=True, hand_drawn_roughness=2.5, hand_drawn_seed=42))

    char2 = Stickman(name="Curved", height=150, proportion_style="xkcd")
    char2.move_to((1060, 300))
    char2.set_expression("happy")
    # Same extended pose
    char2.set_arm_angles(left_shoulder=160, left_elbow=30, right_shoulder=20, right_elbow=30)
    char2.set_leg_angles(left_hip=30, left_knee=20, right_hip=150, right_knee=20)
    # Set style on character directly
    char2.set_style(Style(hand_drawn=True, hand_drawn_roughness=2.5, hand_drawn_seed=42))

    bubble2 = char2.say("Curved limbs!\\n(xkcd-style)", width=180, height=70)
    bubble2.set_style(Style(hand_drawn=True, hand_drawn_roughness=2.5, hand_drawn_seed=42))

    panel2.add_content(char2, bubble2)
    page.add(panel2)

    return page


def create_action_poses_demo() -> Page:
    """Demonstrate curves with various action poses."""
    page = Page(width=1600, height=500, background_color="#FFFFFF")

    poses = [
        {
            "label": "Running",
            "left_shoulder": 45,
            "left_elbow": 30,
            "right_shoulder": 225,
            "right_elbow": 30,
            "left_hip": 45,
            "left_knee": 40,
            "right_hip": 135,
            "right_knee": 40,
        },
        {
            "label": "Jumping",
            "left_shoulder": 135,
            "left_elbow": 20,
            "right_shoulder": 135,
            "right_elbow": 20,
            "left_hip": 45,
            "left_knee": 30,
            "right_hip": 135,
            "right_knee": 30,
        },
        {
            "label": "Dancing",
            "left_shoulder": 160,
            "left_elbow": 45,
            "right_shoulder": 20,
            "right_elbow": 45,
            "left_hip": 20,
            "left_knee": 15,
            "right_hip": 160,
            "right_knee": 15,
        },
        {
            "label": "Stretching",
            "left_shoulder": 180,
            "left_elbow": 10,
            "right_shoulder": 0,
            "right_elbow": 10,
            "left_hip": 90,
            "left_knee": 10,
            "right_hip": 90,
            "right_knee": 10,
        },
    ]

    panel_width = 350
    start_x = 200

    for i, pose in enumerate(poses):
        x_pos = start_x + i * (panel_width + 20)

        panel = Panel(width=panel_width, height=450)
        panel.move_to((x_pos, 250))
        panel.set_style(Style(
            hand_drawn=True,
            hand_drawn_roughness=2.5,
            hand_drawn_seed=100 + i
        ))

        char = Stickman(height=140, proportion_style="xkcd")
        char.move_to((x_pos, 290))
        char.set_expression("happy")

        char.set_arm_angles(
            left_shoulder=pose["left_shoulder"],
            left_elbow=pose["left_elbow"],
            right_shoulder=pose["right_shoulder"],
            right_elbow=pose["right_elbow"],
        )
        char.set_leg_angles(
            left_hip=pose["left_hip"],
            left_knee=pose["left_knee"],
            right_hip=pose["right_hip"],
            right_knee=pose["right_knee"],
        )
        # Set style on character directly
        char.set_style(Style(
            hand_drawn=True,
            hand_drawn_roughness=2.5,
            hand_drawn_seed=100 + i
        ))

        bubble = char.say(pose["label"], width=140, height=50)
        bubble.set_style(Style(
            hand_drawn=True,
            hand_drawn_roughness=2.5,
            hand_drawn_seed=100 + i
        ))

        panel.add_content(char, bubble)
        page.add(panel)

    return page


def create_curve_comparison() -> Page:
    """Side-by-side close-up showing curve detail."""
    page = Page(width=1200, height=600, background_color="#FFFFFF")

    # Large character on left - normal
    panel1 = Panel(width=550, height=550)
    panel1.move_to((300, 300))

    char1 = Stickman(height=200, proportion_style="xkcd")
    char1.move_to((300, 350))
    char1.set_expression("neutral")
    char1.set_arm_angles(left_shoulder=135, left_elbow=45, right_shoulder=45, right_elbow=45)

    panel1.add_content(char1)
    page.add(panel1)

    # Large character on right - curved
    panel2 = Panel(width=550, height=550)
    panel2.move_to((900, 300))
    panel2.set_style(Style(hand_drawn=True, hand_drawn_roughness=2.5, hand_drawn_seed=999))

    char2 = Stickman(height=200, proportion_style="xkcd")
    char2.move_to((900, 350))
    char2.set_expression("happy")
    char2.set_arm_angles(left_shoulder=135, left_elbow=45, right_shoulder=45, right_elbow=45)
    char2.set_style(Style(hand_drawn=True, hand_drawn_roughness=2.5, hand_drawn_seed=999))

    panel2.add_content(char2)
    page.add(panel2)

    return page


if __name__ == "__main__":
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)

    demos = [
        ("curved_limbs_demo", create_curved_limbs_demo()),
        ("action_poses", create_action_poses_demo()),
        ("curve_closeup", create_curve_comparison()),
    ]

    for name, page in demos:
        output_path = output_dir / f"28_{name}.png"
        page.render(str(output_path))
        print(f"Created: {output_path}")

    print("\nAll curved limbs examples generated successfully!")
    print("\nKey feature:")
    print("  - Limbs are naturally curved instead of straight lines")
    print("  - Combined with hand-drawn jitter for organic appearance")
    print("  - Most visible in extended poses (arms/legs spread)")
