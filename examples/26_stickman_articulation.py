#!/usr/bin/env python3
"""Example 26: Stickman Articulation - Joint and Limb Control.

This example demonstrates the new articulation system for Stickman characters,
which allows precise control over individual joint angles and hand gestures.

Features demonstrated:
- set_arm_angles() for shoulder and elbow control
- set_leg_angles() for hip and knee control
- set_hands() for hand gesture options
- point_at() helper for automatic arm positioning
- ArmController and LegController presets
- Method chaining for fluent configuration
"""

from pathlib import Path

from comix import Page, Panel, Stickman, NarratorBubble, Circle


def create_joint_angles_demo() -> Page:
    """Demonstrate direct joint angle control.

    Shows how to use set_arm_angles() and set_leg_angles() to create
    custom poses with precise joint control.
    """
    page = Page(width=800, height=400, background_color="#FFFFFF")

    # Panel positions (global coordinates)
    panel_positions = [(100, 200), (300, 200), (500, 200), (700, 200)]
    panel_width = 180

    # Panel 1: Arms down (default)
    panel1 = Panel(width=panel_width, height=350)
    panel1.move_to(panel_positions[0])
    char1 = Stickman(height=120)
    char1.move_to(panel_positions[0])
    char1.set_arm_angles(left_shoulder=0, right_shoulder=0)
    char1.set_leg_angles(left_hip=0, right_hip=0)
    label1 = NarratorBubble("Arms: 0\nLegs: 0", width=120, height=50)
    label1.move_to((panel_positions[0][0], panel_positions[0][1] - 130))
    panel1.add_content(char1, label1)
    page.add(panel1)

    # Panel 2: Arms forward (90 degrees)
    panel2 = Panel(width=panel_width, height=350)
    panel2.move_to(panel_positions[1])
    char2 = Stickman(height=120)
    char2.move_to(panel_positions[1])
    char2.set_arm_angles(left_shoulder=90, right_shoulder=90)
    label2 = NarratorBubble("Arms: 90\n(forward)", width=120, height=50)
    label2.move_to((panel_positions[1][0], panel_positions[1][1] - 130))
    panel2.add_content(char2, label2)
    page.add(panel2)

    # Panel 3: Arms up (180 degrees)
    panel3 = Panel(width=panel_width, height=350)
    panel3.move_to(panel_positions[2])
    char3 = Stickman(height=120)
    char3.move_to(panel_positions[2])
    char3.set_arm_angles(left_shoulder=180, right_shoulder=180)
    label3 = NarratorBubble("Arms: 180\n(up)", width=120, height=50)
    label3.move_to((panel_positions[2][0], panel_positions[2][1] - 130))
    panel3.add_content(char3, label3)
    page.add(panel3)

    # Panel 4: Walking pose with bent limbs
    panel4 = Panel(width=panel_width, height=350)
    panel4.move_to(panel_positions[3])
    char4 = Stickman(height=120)
    char4.move_to(panel_positions[3])
    char4.set_arm_angles(left_shoulder=30, left_elbow=15, right_shoulder=-30, right_elbow=15)
    char4.set_leg_angles(left_hip=30, left_knee=15, right_hip=-20, right_knee=10)
    label4 = NarratorBubble("Walking\n(custom)", width=120, height=50)
    label4.move_to((panel_positions[3][0], panel_positions[3][1] - 130))
    panel4.add_content(char4, label4)
    page.add(panel4)

    return page


def create_hand_gestures_demo() -> Page:
    """Demonstrate hand gesture options.

    Shows all 7 available hand gesture types.
    """
    page = Page(width=840, height=400, background_color="#FFFFFF")

    gestures = ["none", "fist", "open", "point", "peace", "thumbs_up", "relaxed"]
    panel_width = 110
    start_x = 65

    for i, gesture in enumerate(gestures):
        x_pos = start_x + i * (panel_width + 5)
        panel = Panel(width=panel_width, height=350)
        panel.move_to((x_pos, 200))

        char = Stickman(height=100)
        char.move_to((x_pos, 220))
        char.set_arm_angles(left_shoulder=135, left_elbow=45, right_shoulder=135, right_elbow=45)
        char.set_hands(left=gesture, right=gesture)

        label = NarratorBubble(gesture, width=100, height=35)
        label.move_to((x_pos, 60))

        panel.add_content(char, label)
        page.add(panel)

    return page


def create_point_at_demo() -> Page:
    """Demonstrate the point_at() helper method.

    Shows how to automatically point at a target object.
    """
    page = Page(width=600, height=400, background_color="#FFFFFF")

    panel = Panel(width=550, height=350)
    panel.move_to((300, 200))

    # Create a target circle
    target = Circle(radius=25, stroke_color="#FF4444", fill_color="#FF8888")
    target.move_to((450, 100))

    # Create character and point at target
    char = Stickman(height=120)
    char.move_to((150, 250))
    char.point_at(target, arm="right", hand="point", elbow_bend=0)

    # Add narrator label
    label = NarratorBubble("point_at() helper", width=150, height=35)
    label.move_to((300, 50))

    panel.add_content(char, target, label)
    page.add(panel)

    return page


def create_controller_presets_demo() -> Page:
    """Demonstrate ArmController and LegController presets.

    Shows convenient preset methods for common poses.
    """
    page = Page(width=800, height=400, background_color="#FFFFFF")

    presets = [
        ("waving", "standing", "Waving"),
        ("pointing", "walking", "Pointing"),
        ("thinking", "sitting", "Thinking"),
        ("raised", "kneeling", "Raised"),
    ]

    panel_width = 180
    start_x = 105

    for i, (arm_preset, leg_preset, label_text) in enumerate(presets):
        x_pos = start_x + i * (panel_width + 10)
        panel = Panel(width=panel_width, height=350)
        panel.move_to((x_pos, 200))

        char = Stickman(height=110)
        char.move_to((x_pos, 220))

        # Use controller presets
        char.left_arm.set_preset(arm_preset)
        char.left_leg_ctrl.set_preset(leg_preset)

        label = NarratorBubble(label_text, width=130, height=40)
        label.move_to((x_pos, 60))

        panel.add_content(char, label)
        page.add(panel)

    return page


def create_elbow_knee_bends_demo() -> Page:
    """Demonstrate elbow and knee bend angles.

    Shows how elbow and knee bends affect limb positioning.
    """
    page = Page(width=800, height=400, background_color="#FFFFFF")

    bends = [
        (0, "0 (straight)"),
        (45, "45 (slight)"),
        (90, "90 (right)"),
        (135, "135 (deep)"),
    ]

    panel_width = 180
    start_x = 105

    for i, (bend_angle, label_text) in enumerate(bends):
        x_pos = start_x + i * (panel_width + 10)
        panel = Panel(width=panel_width, height=350)
        panel.move_to((x_pos, 200))

        char = Stickman(height=110)
        char.move_to((x_pos, 220))

        # Set arms with varying elbow bends
        char.set_arm_angles(left_shoulder=90, left_elbow=bend_angle,
                           right_shoulder=90, right_elbow=bend_angle)

        label = NarratorBubble(f"Elbow: {label_text}", width=140, height=40)
        label.move_to((x_pos, 60))

        panel.add_content(char, label)
        page.add(panel)

    return page


def create_custom_poses_showcase() -> Page:
    """Showcase custom poses using the articulation system.

    Demonstrates various realistic poses created with joint angles.
    """
    page = Page(width=800, height=400, background_color="#FFFFFF")

    # Define custom poses
    poses = [
        # Cheering pose
        {
            "arms": {"left_shoulder": 150, "left_elbow": 30, "right_shoulder": 150, "right_elbow": 30},
            "legs": {"left_hip": 0, "left_knee": 0, "right_hip": 0, "right_knee": 0},
            "hands": {"left": "open", "right": "open"},
            "label": "Cheering!",
        },
        # Boxing pose
        {
            "arms": {"left_shoulder": 90, "left_elbow": 120, "right_shoulder": 90, "right_elbow": 90},
            "legs": {"left_hip": 10, "left_knee": 15, "right_hip": -10, "right_knee": 15},
            "hands": {"left": "fist", "right": "fist"},
            "label": "Boxing",
        },
        # Relaxed standing
        {
            "arms": {"left_shoulder": 10, "left_elbow": 15, "right_shoulder": -10, "right_elbow": 15},
            "legs": {"left_hip": 0, "left_knee": 5, "right_hip": 0, "right_knee": 5},
            "hands": {"left": "relaxed", "right": "relaxed"},
            "label": "Relaxed",
        },
        # Victory pose
        {
            "arms": {"left_shoulder": 135, "left_elbow": 0, "right_shoulder": 135, "right_elbow": 0},
            "legs": {"left_hip": 0, "left_knee": 0, "right_hip": 0, "right_knee": 0},
            "hands": {"left": "peace", "right": "peace"},
            "label": "Victory!",
        },
    ]

    panel_width = 180
    start_x = 105

    for i, pose in enumerate(poses):
        x_pos = start_x + i * (panel_width + 10)
        panel = Panel(width=panel_width, height=350)
        panel.move_to((x_pos, 200))

        char = Stickman(height=110)
        char.move_to((x_pos, 220))

        # Apply pose using method chaining
        char.set_arm_angles(**pose["arms"]).set_leg_angles(**pose["legs"]).set_hands(**pose["hands"])

        label = NarratorBubble(pose["label"], width=120, height=40)
        label.move_to((x_pos, 60))

        panel.add_content(char, label)
        page.add(panel)

    return page


if __name__ == "__main__":
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)

    # Create all demo pages
    demos = [
        ("joint_angles", create_joint_angles_demo()),
        ("hand_gestures", create_hand_gestures_demo()),
        ("point_at", create_point_at_demo()),
        ("controller_presets", create_controller_presets_demo()),
        ("elbow_knee_bends", create_elbow_knee_bends_demo()),
        ("custom_poses", create_custom_poses_showcase()),
    ]

    for name, page in demos:
        output_path = output_dir / f"26_articulation_{name}.png"
        page.render(str(output_path))
        print(f"Created: {output_path}")

    print("\nAll articulation examples generated successfully!")
    print("\nFeatures demonstrated:")
    print("  - set_arm_angles(): Control shoulder and elbow angles independently")
    print("  - set_leg_angles(): Control hip and knee angles independently")
    print("  - set_hands(): 7 hand gesture options (none, fist, open, point, peace, thumbs_up, relaxed)")
    print("  - point_at(): Automatically calculate arm angles to point at a target")
    print("  - ArmController/LegController: Convenient preset methods for common poses")
    print("  - Method chaining: Fluent API for setting multiple properties")
