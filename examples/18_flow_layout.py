"""FlowLayout for responsive, content-aware positioning.

FlowLayout is unique among Comix layout systems because it respects
each object's natural dimensions rather than dividing space equally.
Objects flow horizontally or vertically with optional wrapping.

This example demonstrates:
- Horizontal flow with automatic wrapping
- Vertical flow for column-based layouts
- Alignment options (start, center, end)
- Variable-sized panels that maintain their proportions
"""

from comix import Page, Panel, Stickman
from comix.layout.flow import FlowLayout


def create_horizontal_flow() -> None:
    """Horizontal flow with wrapping - items flow left-to-right, wrap to next row."""
    page = Page(width=800, height=600, background_color="#F5F5F5")

    # Create panels of different sizes
    panels = [
        Panel(width=200, height=150, background_color="#FFE4E1"),  # Wide
        Panel(width=150, height=150, background_color="#E0FFFF"),  # Square
        Panel(width=250, height=150, background_color="#E6E6FA"),  # Wider
        Panel(width=180, height=200, background_color="#F0FFF0"),  # Tall
        Panel(width=150, height=150, background_color="#FFF0F5"),  # Square
        Panel(width=220, height=180, background_color="#FFFACD"),  # Large
    ]

    # Add a character to each panel
    expressions = ["happy", "excited", "surprised", "confused", "neutral", "sleepy"]
    for i, (panel, expr) in enumerate(zip(panels, expressions)):
        char = Stickman(height=60)
        char.move_to((panel.width / 2, panel.height / 2))
        char.set_expression(expr)
        bubble = char.say(f"Panel {i + 1}")
        panel.add_content(char, bubble)

    # Create flow layout with wrapping
    layout = FlowLayout(
        width=760,
        height=560,
        direction="horizontal",
        spacing=15,
        wrap="wrap",
        alignment="center",
        offset_x=20,
        offset_y=20,
    )

    # Calculate positions respecting natural panel sizes
    positions = layout.calculate_positions_for_objects(panels)

    # Apply positions and add to page
    for panel, pos in zip(panels, positions):
        panel.move_to((pos["center_x"], pos["center_y"]))
        page.add(panel)

    page.render("examples/output/18_horizontal_flow.png")
    print("Created examples/output/18_horizontal_flow.png")


def create_vertical_flow() -> None:
    """Vertical flow with wrapping - items flow top-to-bottom, wrap to next column."""
    page = Page(width=900, height=500, background_color="#F0F8FF")

    # Create panels of different heights
    panels = [
        Panel(width=180, height=100, background_color="#FFB6C1"),
        Panel(width=180, height=150, background_color="#98FB98"),
        Panel(width=180, height=120, background_color="#DDA0DD"),
        Panel(width=180, height=180, background_color="#F0E68C"),
        Panel(width=180, height=90, background_color="#ADD8E6"),
        Panel(width=180, height=140, background_color="#FFE4B5"),
    ]

    # Add characters
    poses = ["standing", "waving", "thinking", "pointing", "cheering", "sitting"]
    for i, (panel, pose) in enumerate(zip(panels, poses)):
        char = Stickman(height=50, color="#4A4A4A")
        char.move_to((panel.width / 2, panel.height / 2))
        char.set_pose(pose)
        panel.add_content(char)

    # Create vertical flow layout
    layout = FlowLayout(
        width=860,
        height=460,
        direction="vertical",
        spacing=15,
        wrap="wrap",
        alignment="start",
        cross_alignment="center",
        offset_x=20,
        offset_y=20,
    )

    positions = layout.calculate_positions_for_objects(panels)

    for panel, pos in zip(panels, positions):
        panel.move_to((pos["center_x"], pos["center_y"]))
        page.add(panel)

    page.render("examples/output/18_vertical_flow.png")
    print("Created examples/output/18_vertical_flow.png")


def create_alignment_comparison() -> None:
    """Compare different alignment options in FlowLayout."""
    page = Page(width=900, height=800, background_color="#FAFAFA")

    alignments = ["start", "center", "end"]
    colors = ["#FFCDD2", "#C8E6C9", "#BBDEFB"]

    y_offset = 20
    for alignment, color in zip(alignments, colors):
        # Create 4 small panels for this row
        row_panels = [
            Panel(width=150, height=100, background_color=color),
            Panel(width=100, height=100, background_color=color),
            Panel(width=180, height=100, background_color=color),
            Panel(width=120, height=100, background_color=color),
        ]

        # Add label to first panel
        char = Stickman(height=50)
        char.move_to((75, 50))
        bubble = char.say(f"align: {alignment}")
        row_panels[0].add_content(char, bubble)

        # Create flow layout for this row (no wrap to show alignment)
        layout = FlowLayout(
            width=860,
            height=120,
            direction="horizontal",
            spacing=20,
            wrap="nowrap",
            alignment=alignment,  # type: ignore[arg-type]
            offset_x=20,
            offset_y=y_offset,
        )

        positions = layout.calculate_positions_for_objects(row_panels)

        for panel, pos in zip(row_panels, positions):
            panel.move_to((pos["center_x"], pos["center_y"]))
            page.add(panel)

        y_offset += 140

    # Add cross-alignment demo
    y_offset += 40

    cross_alignments = ["start", "center", "end"]
    for cross_alignment, color in zip(cross_alignments, colors):
        row_panels = [
            Panel(width=150, height=60, background_color=color),
            Panel(width=150, height=100, background_color=color),
            Panel(width=150, height=80, background_color=color),
        ]

        char = Stickman(height=40)
        char.move_to((75, 30))
        bubble = char.say(f"cross: {cross_alignment}")
        row_panels[0].add_content(char, bubble)

        layout = FlowLayout(
            width=860,
            height=120,
            direction="horizontal",
            spacing=20,
            wrap="nowrap",
            alignment="start",
            cross_alignment=cross_alignment,  # type: ignore[arg-type]
            offset_x=20,
            offset_y=y_offset,
        )

        positions = layout.calculate_positions_for_objects(row_panels)

        for panel, pos in zip(row_panels, positions):
            panel.move_to((pos["center_x"], pos["center_y"]))
            page.add(panel)

        y_offset += 140

    page.render("examples/output/18_alignment_comparison.png")
    print("Created examples/output/18_alignment_comparison.png")


if __name__ == "__main__":
    create_horizontal_flow()
    create_vertical_flow()
    create_alignment_comparison()
    print("\nFlowLayout examples complete!")
