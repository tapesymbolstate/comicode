#!/usr/bin/env python3
"""Example 27: xkcd-Style Hand-Drawn Rendering.

This example demonstrates the hand-drawn/sketchy rendering effects that enable
xkcd-style comics with wobbly lines and organic appearance.

Features demonstrated:
- hand_drawn style property
- hand_drawn_roughness parameter (0.5-2.0)
- Side-by-side comparison (normal vs hand-drawn)
- Different roughness levels
- Reproducible rendering with seed
"""

from pathlib import Path

from comix import Page, Panel, Stickman, Style


def create_comparison_demo() -> Page:
    """Side-by-side comparison: normal vs hand-drawn."""
    page = Page(width=900, height=450, background_color="#FFFFFF")

    panel1 = Panel(width=400, height=350)
    panel1.move_to((230, 225))

    char1 = Stickman(name="Bob", height=100, proportion_style="xkcd")
    char1.move_to((230, 270))
    char1.set_expression("neutral")
    bubble1 = char1.say("Normal rendering\n(clean lines)", width=180, height=70)

    panel1.add_content(char1, bubble1)
    page.add(panel1)

    panel2 = Panel(width=400, height=350)
    panel2.move_to((670, 225))
    panel2.set_style(Style(hand_drawn=True, hand_drawn_roughness=2.5, hand_drawn_seed=42))

    char2 = Stickman(name="Alice", height=100, proportion_style="xkcd")
    char2.move_to((670, 270))
    char2.set_expression("happy")
    char2.set_arm_angles(left_shoulder=135, right_shoulder=135)
    bubble2 = char2.say("Hand-drawn style!\n(xkcd-like)", width=180, height=70)

    panel2.add_content(char2, bubble2)
    page.add(panel2)

    return page


def create_roughness_levels_demo() -> Page:
    """Demonstrate different roughness levels."""
    page = Page(width=1200, height=400, background_color="#FFFFFF")

    roughness_levels = [
        (1.0, "Light\n(1.0)"),
        (2.0, "Normal\n(2.0)"),
        (3.0, "Heavy\n(3.0)"),
        (4.0, "Extreme\n(4.0)"),
    ]

    panel_width = 270
    start_x = 150

    for i, (roughness, label) in enumerate(roughness_levels):
        x_pos = start_x + i * (panel_width + 10)

        panel = Panel(width=panel_width, height=350)
        panel.move_to((x_pos, 200))
        panel.set_style(Style(
            hand_drawn=True,
            hand_drawn_roughness=roughness,
            hand_drawn_seed=42 + i
        ))

        char = Stickman(height=90, proportion_style="xkcd")
        char.move_to((x_pos, 240))
        char.set_expression("happy")

        bubble = char.say(label, width=140, height=60)

        panel.add_content(char, bubble)
        page.add(panel)

    return page


def create_full_comic_demo() -> Page:
    """Complete xkcd-style comic with dialogue."""
    page = Page(width=800, height=600, background_color="#FFFFFF")

    panel1 = Panel(width=750, height=250)
    panel1.move_to((400, 145))
    panel1.set_style(Style(hand_drawn=True, hand_drawn_roughness=2.5, hand_drawn_seed=123))

    char1 = Stickman(name="Scientist", height=100, proportion_style="xkcd")
    char1.move_to((250, 180))
    char1.set_expression("excited")
    char1.set_arm_angles(right_shoulder=120, right_elbow=30)
    bubble1 = char1.say("I've discovered a way to\nmake code draw comics!", width=220, height=70)

    char2 = Stickman(name="Friend", height=100, proportion_style="xkcd")
    char2.move_to((550, 180))
    char2.set_expression("confused")
    bubble2 = char2.say("Isn't that just\nPython?", width=160, height=60)

    panel1.add_content(char1, char2, bubble1, bubble2)
    page.add(panel1)

    panel2 = Panel(width=750, height=250)
    panel2.move_to((400, 425))
    panel2.set_style(Style(hand_drawn=True, hand_drawn_roughness=2.5, hand_drawn_seed=123))

    char3 = Stickman(name="Scientist", height=100, proportion_style="xkcd")
    char3.move_to((250, 460))
    char3.set_expression("smirk")
    bubble3 = char3.say("Yes, but now it looks\nlike xkcd!", width=200, height=70)

    char4 = Stickman(name="Friend", height=100, proportion_style="xkcd")
    char4.move_to((550, 460))
    char4.set_expression("happy")
    char4.set_arm_angles(left_shoulder=135, right_shoulder=135)
    bubble4 = char4.say("Fair enough!", width=140, height=50)

    panel2.add_content(char3, char4, bubble3, bubble4)
    page.add(panel2)

    return page


def create_reproducible_demo() -> Page:
    """Demonstrate reproducible rendering with seed."""
    page = Page(width=900, height=400, background_color="#FFFFFF")

    panel1 = Panel(width=400, height=350)
    panel1.move_to((230, 200))
    panel1.set_style(Style(hand_drawn=True, hand_drawn_roughness=2.5, hand_drawn_seed=999))

    char1 = Stickman(height=100, proportion_style="xkcd")
    char1.move_to((230, 240))
    char1.set_expression("neutral")
    bubble1 = char1.say("Seed: 999\n(always same)", width=160, height=70)

    panel1.add_content(char1, bubble1)
    page.add(panel1)

    panel2 = Panel(width=400, height=350)
    panel2.move_to((670, 200))
    panel2.set_style(Style(hand_drawn=True, hand_drawn_roughness=2.5, hand_drawn_seed=999))

    char2 = Stickman(height=100, proportion_style="xkcd")
    char2.move_to((670, 240))
    char2.set_expression("happy")
    bubble2 = char2.say("Seed: 999\n(identical!)", width=160, height=70)

    panel2.add_content(char2, bubble2)
    page.add(panel2)

    return page


if __name__ == "__main__":
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)

    demos = [
        ("comparison", create_comparison_demo()),
        ("roughness_levels", create_roughness_levels_demo()),
        ("full_comic", create_full_comic_demo()),
        ("reproducible", create_reproducible_demo()),
    ]

    for name, page in demos:
        output_path = output_dir / f"27_xkcd_{name}.png"
        page.render(str(output_path))
        print(f"Created: {output_path}")

    print("\nAll xkcd-style examples generated successfully!")
    print("\nKey features:")
    print("  - hand_drawn: Enable/disable sketchy rendering")
    print("  - hand_drawn_roughness: Control wobble intensity (0.5-2.0)")
    print("  - hand_drawn_seed: Reproducible random jitter")
    print("\nUsage:")
    print("  page.set_style(Style(hand_drawn=True, hand_drawn_roughness=1.0))")
