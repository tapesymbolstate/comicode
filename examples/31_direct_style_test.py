#!/usr/bin/env python3
"""Test applying style directly to Character."""

from pathlib import Path

from comix import Page, Panel, Stickman, Style


def create_direct_style_test() -> Page:
    """Apply hand_drawn style directly to character."""
    page = Page(width=1400, height=500, background_color="#FFFFFF")

    # Left: Normal
    panel1 = Panel(width=650, height=450)
    panel1.move_to((340, 250))

    char1 = Stickman(height=150, proportion_style="xkcd")
    char1.move_to((340, 300))
    char1.set_expression("neutral")
    char1.set_arm_angles(left_shoulder=160, right_shoulder=20)
    bubble1 = char1.say("Normal\\n(no style)", width=160, height=60)

    panel1.add_content(char1, bubble1)
    page.add(panel1)

    # Right: Style directly on character
    panel2 = Panel(width=650, height=450)
    panel2.move_to((1060, 250))

    char2 = Stickman(height=150, proportion_style="xkcd")
    char2.move_to((1060, 300))
    char2.set_expression("happy")
    char2.set_arm_angles(left_shoulder=160, right_shoulder=20)

    # Set style DIRECTLY on character, not panel
    char2.set_style(Style(hand_drawn=True, hand_drawn_roughness=2.5, hand_drawn_seed=42))

    bubble2 = char2.say("Direct style\\n(on character)", width=180, height=70)

    panel2.add_content(char2, bubble2)
    page.add(panel2)

    return page


if __name__ == "__main__":
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)

    page = create_direct_style_test()
    output_path = output_dir / "31_direct_style_test.png"
    page.render(str(output_path))
    print(f"Created: {output_path}")
