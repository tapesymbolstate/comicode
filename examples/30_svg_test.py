#!/usr/bin/env python3
"""Generate SVG to inspect the actual output."""

from pathlib import Path

from comix import Page, Panel, Stickman, Style


def create_svg_test() -> Page:
    """Simple test to check SVG output."""
    page = Page(width=800, height=400, background_color="#FFFFFF")

    panel = Panel(width=750, height=350)
    panel.move_to((400, 200))
    panel.set_style(Style(hand_drawn=True, hand_drawn_roughness=2.5, hand_drawn_seed=42))

    char = Stickman(height=150, proportion_style="xkcd")
    char.move_to((400, 230))
    char.set_expression("happy")
    # Extended arms to make curves visible
    char.set_arm_angles(left_shoulder=160, right_shoulder=20)

    panel.add_content(char)
    page.add(panel)

    return page


if __name__ == "__main__":
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)

    page = create_svg_test()

    # Render as SVG to inspect
    svg_path = output_dir / "30_svg_test.svg"
    page.render(str(svg_path), format="svg")
    print(f"Created SVG: {svg_path}")
    print("Open this file to inspect the actual polyline points")
