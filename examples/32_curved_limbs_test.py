#!/usr/bin/env python3
"""Example 32: Natural Curved Limbs Test

Demonstrates the natural curve feature for character limbs and spine.
Shows both manual and automatic curve modes.
"""

from pathlib import Path

from comix import Page, Panel, Stickman


def create_manual_curves_demo() -> Page:
    """Demonstrate manual curve control."""
    page = Page(width=1800, height=600, background_color="#FFFFFF")

    # Panel 1: Normal (no curves)
    panel1 = Panel(width=550, height=550)
    panel1.move_to((300, 300))

    char1 = Stickman(height=180, proportion_style="xkcd")
    char1.move_to((300, 350))
    char1.set_arm_angles(left_shoulder=135, left_elbow=30, right_shoulder=45, right_elbow=20)
    char1.set_leg_angles(left_hip=20, right_hip=150)
    bubble1 = char1.say("No curves\n(straight)", width=140, height=60)

    panel1.add_content(char1, bubble1)
    page.add(panel1)

    # Panel 2: Manual curves (moderate)
    panel2 = Panel(width=550, height=550)
    panel2.move_to((900, 300))

    char2 = Stickman(height=180, proportion_style="xkcd")
    char2.move_to((900, 350))
    char2.set_arm_angles(left_shoulder=135, left_elbow=30, right_shoulder=45, right_elbow=20)
    char2.set_leg_angles(left_hip=20, right_hip=150)
    # Add natural curves
    char2.set_limb_curves(
        left_upper_arm=0.12,
        left_forearm=0.10,
        right_upper_arm=-0.12,
        right_forearm=-0.10,
        left_upper_leg=0.08,
        right_upper_leg=-0.08,
    )
    bubble2 = char2.say("Manual curves\n(0.1-0.12)", width=160, height=60)

    panel2.add_content(char2, bubble2)
    page.add(panel2)

    # Panel 3: Strong manual curves
    panel3 = Panel(width=550, height=550)
    panel3.move_to((1500, 300))

    char3 = Stickman(height=180, proportion_style="xkcd")
    char3.move_to((1500, 350))
    char3.set_arm_angles(left_shoulder=135, left_elbow=30, right_shoulder=45, right_elbow=20)
    char3.set_leg_angles(left_hip=20, right_hip=150)
    # Stronger curves
    char3.set_limb_curves(
        left_upper_arm=0.25,
        left_forearm=0.20,
        right_upper_arm=-0.25,
        right_forearm=-0.20,
        left_upper_leg=0.15,
        right_upper_leg=-0.15,
        spine=0.15,
    )
    bubble3 = char3.say("Strong curves\n(0.2-0.25)", width=160, height=60)

    panel3.add_content(char3, bubble3)
    page.add(panel3)

    return page


def create_auto_curves_demo() -> Page:
    """Demonstrate automatic curve mode."""
    page = Page(width=1800, height=600, background_color="#FFFFFF")

    poses = [
        {
            "label": "Auto: Low",
            "strength": 0.08,
            "left_shoulder": 160,
            "right_shoulder": 20,
            "left_hip": 30,
            "right_hip": 150,
        },
        {
            "label": "Auto: Medium",
            "strength": 0.15,
            "left_shoulder": 160,
            "right_shoulder": 20,
            "left_hip": 30,
            "right_hip": 150,
        },
        {
            "label": "Auto: High",
            "strength": 0.25,
            "left_shoulder": 160,
            "right_shoulder": 20,
            "left_hip": 30,
            "right_hip": 150,
        },
    ]

    for i, pose in enumerate(poses):
        x_pos = 300 + i * 600

        panel = Panel(width=550, height=550)
        panel.move_to((x_pos, 300))

        char = Stickman(height=180, proportion_style="xkcd")
        char.move_to((x_pos, 350))
        char.set_arm_angles(
            left_shoulder=pose["left_shoulder"],
            left_elbow=25,
            right_shoulder=pose["right_shoulder"],
            right_elbow=20,
        )
        char.set_leg_angles(
            left_hip=pose["left_hip"],
            left_knee=15,
            right_hip=pose["right_hip"],
            right_knee=15,
        )
        # Enable auto curves
        char.enable_auto_curves(True, strength=pose["strength"])

        bubble = char.say(
            f"{pose['label']}\n({pose['strength']})", width=160, height=60
        )

        panel.add_content(char, bubble)
        page.add(panel)

    return page


def create_spine_curve_demo() -> Page:
    """Demonstrate spine/torso curves."""
    page = Page(width=1800, height=600, background_color="#FFFFFF")

    curves = [
        {"label": "Straight", "curve": 0.0},
        {"label": "Leaning left\n(0.15)", "curve": 0.15},
        {"label": "Leaning right\n(-0.15)", "curve": -0.15},
    ]

    for i, data in enumerate(curves):
        x_pos = 300 + i * 600

        panel = Panel(width=550, height=550)
        panel.move_to((x_pos, 300))

        char = Stickman(height=180, proportion_style="xkcd")
        char.move_to((x_pos, 350))
        char.set_arm_angles(left_shoulder=90, right_shoulder=90)
        # Set spine curve
        char.set_limb_curves(spine=data["curve"])

        bubble = char.say(data["label"], width=160, height=60)

        panel.add_content(char, bubble)
        page.add(panel)

    return page


if __name__ == "__main__":
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)

    demos = [
        ("manual_curves", create_manual_curves_demo()),
        ("auto_curves", create_auto_curves_demo()),
        ("spine_curves", create_spine_curve_demo()),
    ]

    for name, page in demos:
        output_path = output_dir / f"32_{name}.png"
        page.render(str(output_path))
        print(f"Created: {output_path}")

    print("\n✓ All curved limbs examples generated!")
    print("\nFeatures demonstrated:")
    print("  - Manual curve control per limb segment")
    print("  - Automatic curves based on pose")
    print("  - Spine/torso curves for leaning poses")
    print("  - Natural organic appearance for comics")
