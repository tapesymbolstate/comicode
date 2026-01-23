#!/usr/bin/env python3
"""Example 33: XKCD Style with Natural Curves

Combines hand-drawn (sketchy) rendering with natural limb curves
to create organic, comic-like characters similar to xkcd style.
"""

from pathlib import Path

from comix import Page, Panel, Stickman, Style


def create_xkcd_comparison() -> Page:
    """Compare normal vs curved in xkcd style."""
    page = Page(width=1400, height=500, background_color="#FFFFFF")

    # Left: xkcd style WITHOUT curves
    panel1 = Panel(width=650, height=450)
    panel1.move_to((340, 250))

    char1 = Stickman(name="Straight", height=150, proportion_style="xkcd")
    char1.move_to((340, 270))
    char1.set_expression("happy")
    char1.set_arm_angles(left_shoulder=160, left_elbow=30, right_shoulder=20, right_elbow=30)
    char1.set_leg_angles(left_hip=30, left_knee=20, right_hip=150, right_knee=20)
    char1.set_style(Style(hand_drawn=True, hand_drawn_roughness=2.5, hand_drawn_seed=42))
    bubble1 = char1.say("Hand-drawn\n(no curves)", width=180, height=70)
    bubble1.set_style(Style(hand_drawn=True, hand_drawn_roughness=2.5, hand_drawn_seed=42))

    panel1.add_content(char1, bubble1)
    page.add(panel1)

    # Right: xkcd style WITH natural curves
    panel2 = Panel(width=650, height=450)
    panel2.move_to((1060, 250))

    char2 = Stickman(name="Curved", height=150, proportion_style="xkcd")
    char2.move_to((1060, 270))
    char2.set_expression("happy")
    char2.set_arm_angles(left_shoulder=160, left_elbow=30, right_shoulder=20, right_elbow=30)
    char2.set_leg_angles(left_hip=30, left_knee=20, right_hip=150, right_knee=20)
    # Add natural curves
    char2.enable_auto_curves(True, strength=0.12)
    char2.set_style(Style(hand_drawn=True, hand_drawn_roughness=2.5, hand_drawn_seed=42))
    bubble2 = char2.say("Hand-drawn\n+ Curves!", width=180, height=70)
    bubble2.set_style(Style(hand_drawn=True, hand_drawn_roughness=2.5, hand_drawn_seed=42))

    panel2.add_content(char2, bubble2)
    page.add(panel2)

    return page


def create_action_comic() -> Page:
    """Create a mini comic with curved characters."""
    page = Page(width=1800, height=600, background_color="#FFFFFF")

    # Panel 1: Character running
    panel1 = Panel(width=550, height=550)
    panel1.move_to((300, 300))
    panel1.set_style(Style(hand_drawn=True, hand_drawn_roughness=2.0, hand_drawn_seed=100))

    char1 = Stickman(height=140, proportion_style="xkcd")
    char1.move_to((300, 320))
    char1.set_expression("excited")
    char1.set_arm_angles(left_shoulder=45, left_elbow=30, right_shoulder=225, right_elbow=30)
    char1.set_leg_angles(left_hip=45, left_knee=40, right_hip=135, right_knee=40)
    char1.enable_auto_curves(True, strength=0.15)
    char1.set_style(Style(hand_drawn=True, hand_drawn_roughness=2.0, hand_drawn_seed=100))

    bubble1 = char1.say("Running!", width=120, height=50)
    bubble1.set_style(Style(hand_drawn=True, hand_drawn_roughness=2.0, hand_drawn_seed=100))

    panel1.add_content(char1, bubble1)
    page.add(panel1)

    # Panel 2: Character jumping
    panel2 = Panel(width=550, height=550)
    panel2.move_to((900, 300))
    panel2.set_style(Style(hand_drawn=True, hand_drawn_roughness=2.0, hand_drawn_seed=101))

    char2 = Stickman(height=140, proportion_style="xkcd")
    char2.move_to((900, 300))
    char2.set_expression("happy")
    char2.set_arm_angles(left_shoulder=135, left_elbow=20, right_shoulder=135, right_elbow=20)
    char2.set_leg_angles(left_hip=45, left_knee=30, right_hip=135, right_knee=30)
    char2.enable_auto_curves(True, strength=0.18)
    char2.set_style(Style(hand_drawn=True, hand_drawn_roughness=2.0, hand_drawn_seed=101))

    bubble2 = char2.say("Jumping!", width=120, height=50)
    bubble2.set_style(Style(hand_drawn=True, hand_drawn_roughness=2.0, hand_drawn_seed=101))

    panel2.add_content(char2, bubble2)
    page.add(panel2)

    # Panel 3: Character dancing
    panel3 = Panel(width=550, height=550)
    panel3.move_to((1500, 300))
    panel3.set_style(Style(hand_drawn=True, hand_drawn_roughness=2.0, hand_drawn_seed=102))

    char3 = Stickman(height=140, proportion_style="xkcd")
    char3.move_to((1500, 320))
    char3.set_expression("excited")
    char3.set_arm_angles(left_shoulder=160, left_elbow=45, right_shoulder=20, right_elbow=45)
    char3.set_leg_angles(left_hip=20, left_knee=15, right_hip=160, right_knee=15)
    char3.enable_auto_curves(True, strength=0.15)
    char3.set_limb_curves(spine=0.12)  # Add spine curve for dancing pose
    char3.set_style(Style(hand_drawn=True, hand_drawn_roughness=2.0, hand_drawn_seed=102))

    bubble3 = char3.say("Dancing!", width=120, height=50)
    bubble3.set_style(Style(hand_drawn=True, hand_drawn_roughness=2.0, hand_drawn_seed=102))

    panel3.add_content(char3, bubble3)
    page.add(panel3)

    return page


def create_manual_curve_examples() -> Page:
    """Show manual curve control for specific effects."""
    page = Page(width=1800, height=600, background_color="#FFFFFF")

    # Panel 1: Waving with curved arm
    panel1 = Panel(width=550, height=550)
    panel1.move_to((300, 300))
    panel1.set_style(Style(hand_drawn=True, hand_drawn_roughness=2.2, hand_drawn_seed=200))

    char1 = Stickman(height=150, proportion_style="xkcd")
    char1.move_to((300, 330))
    char1.set_expression("happy")
    char1.set_arm_angles(left_shoulder=135, left_elbow=10, right_shoulder=90, right_elbow=5)
    # Manual curve for waving arm
    char1.set_limb_curves(left_upper_arm=0.15, left_forearm=0.12)
    char1.set_style(Style(hand_drawn=True, hand_drawn_roughness=2.2, hand_drawn_seed=200))

    bubble1 = char1.say("Hi there!", width=130, height=50)
    bubble1.set_style(Style(hand_drawn=True, hand_drawn_roughness=2.2, hand_drawn_seed=200))

    panel1.add_content(char1, bubble1)
    page.add(panel1)

    # Panel 2: Leaning with spine curve
    panel2 = Panel(width=550, height=550)
    panel2.move_to((900, 300))
    panel2.set_style(Style(hand_drawn=True, hand_drawn_roughness=2.2, hand_drawn_seed=201))

    char2 = Stickman(height=150, proportion_style="xkcd")
    char2.move_to((900, 330))
    char2.set_expression("confused")
    char2.set_arm_angles(left_shoulder=90, right_shoulder=90)
    # Spine curve for leaning
    char2.set_limb_curves(spine=0.18)
    char2.set_style(Style(hand_drawn=True, hand_drawn_roughness=2.2, hand_drawn_seed=201))

    bubble2 = char2.say("Hmm...", width=120, height=50)
    bubble2.set_style(Style(hand_drawn=True, hand_drawn_roughness=2.2, hand_drawn_seed=201))

    panel2.add_content(char2, bubble2)
    page.add(panel2)

    # Panel 3: Stretching with all curves
    panel3 = Panel(width=550, height=550)
    panel3.move_to((1500, 300))
    panel3.set_style(Style(hand_drawn=True, hand_drawn_roughness=2.2, hand_drawn_seed=202))

    char3 = Stickman(height=150, proportion_style="xkcd")
    char3.move_to((1500, 330))
    char3.set_expression("happy")
    char3.set_arm_angles(left_shoulder=180, left_elbow=10, right_shoulder=180, right_elbow=10)
    # All limbs curved
    char3.set_limb_curves(
        left_upper_arm=0.10,
        left_forearm=0.08,
        right_upper_arm=-0.10,
        right_forearm=-0.08,
        spine=-0.08,
    )
    char3.set_style(Style(hand_drawn=True, hand_drawn_roughness=2.2, hand_drawn_seed=202))

    bubble3 = char3.say("Stretch!", width=120, height=50)
    bubble3.set_style(Style(hand_drawn=True, hand_drawn_roughness=2.2, hand_drawn_seed=202))

    panel3.add_content(char3, bubble3)
    page.add(panel3)

    return page


if __name__ == "__main__":
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)

    demos = [
        ("xkcd_comparison", create_xkcd_comparison()),
        ("action_comic", create_action_comic()),
        ("manual_curves", create_manual_curve_examples()),
    ]

    for name, page in demos:
        output_path = output_dir / f"33_{name}.png"
        page.render(str(output_path))
        print(f"Created: {output_path}")

    print("\n✓ XKCD-style comics with curves generated!")
    print("\nThis demonstrates:")
    print("  ✓ Natural curves + hand-drawn effects")
    print("  ✓ Organic, comic-like appearance")
    print("  ✓ Manual control for specific poses")
    print("  ✓ Auto curves for quick natural look")
