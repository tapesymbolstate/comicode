#!/usr/bin/env python3
"""Test curved limbs without hand-drawn jitter to see curves clearly."""

from pathlib import Path

from comix import Page, Panel, Stickman, Style


def create_curve_only_test() -> Page:
    """Test curves without hand-drawn jitter."""
    page = Page(width=1400, height=500, background_color="#FFFFFF")

    # Left: Normal (no style applied)
    panel1 = Panel(width=650, height=450)
    panel1.move_to((340, 250))

    char1 = Stickman(name="Normal", height=150, proportion_style="xkcd")
    char1.move_to((340, 300))
    char1.set_expression("neutral")
    char1.set_arm_angles(left_shoulder=160, left_elbow=30, right_shoulder=20, right_elbow=30)
    char1.set_leg_angles(left_hip=30, left_knee=20, right_hip=150, right_knee=20)

    bubble1 = char1.say("No curves\\n(straight)", width=160, height=60)

    panel1.add_content(char1, bubble1)
    page.add(panel1)

    # Right: Hand-drawn WITHOUT jitter (roughness=0) to see ONLY curves
    panel2 = Panel(width=650, height=450)
    panel2.move_to((1060, 250))
    # Enable hand_drawn to trigger curve logic, but set roughness=0 to disable jitter
    panel2.set_style(Style(hand_drawn=True, hand_drawn_roughness=0.0, hand_drawn_seed=42))

    char2 = Stickman(name="Curved", height=150, proportion_style="xkcd")
    char2.move_to((1060, 300))
    char2.set_expression("happy")
    char2.set_arm_angles(left_shoulder=160, left_elbow=30, right_shoulder=20, right_elbow=30)
    char2.set_leg_angles(left_hip=30, left_knee=20, right_hip=150, right_knee=20)

    bubble2 = char2.say("Only curves\\n(no jitter)", width=160, height=60)

    panel2.add_content(char2, bubble2)
    page.add(panel2)

    return page


if __name__ == "__main__":
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)

    page = create_curve_only_test()
    output_path = output_dir / "29_curve_test.png"
    page.render(str(output_path))
    print(f"Created: {output_path}")
    print("\nThis test shows ONLY curves without jitter by setting roughness=0")
