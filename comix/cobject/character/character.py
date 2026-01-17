"""Character - Comic character classes."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self

import numpy as np

from comix.cobject.cobject import CObject

if TYPE_CHECKING:
    from comix.cobject.bubble.bubble import Bubble


class Expression:
    """Character expression definition.

    Expressions are composed of three facial components:
    - eyes: normal, curved, droopy, narrow, wide, uneven, closed, stars, tears
    - mouth: normal, smile, frown, open, wavy, grin, gasp, smirk
    - eyebrows: normal, raised, worried, furrowed, relaxed, asymmetric
    """

    # Standard expressions
    NEUTRAL = "neutral"
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    SURPRISED = "surprised"
    CONFUSED = "confused"
    # Extended expressions
    SLEEPY = "sleepy"
    EXCITED = "excited"
    SCARED = "scared"
    SMIRK = "smirk"
    CRYING = "crying"

    def __init__(
        self,
        name: str = "neutral",
        eyes: str = "normal",
        mouth: str = "normal",
        eyebrows: str = "normal",
    ) -> None:
        self.name = name
        self.eyes = eyes
        self.mouth = mouth
        self.eyebrows = eyebrows

    @classmethod
    def from_name(cls, name: str) -> Expression:
        """Create expression from preset name."""
        presets = {
            # Standard expressions
            "neutral": cls("neutral", "normal", "normal", "normal"),
            "happy": cls("happy", "curved", "smile", "raised"),
            "sad": cls("sad", "droopy", "frown", "worried"),
            "angry": cls("angry", "narrow", "frown", "furrowed"),
            "surprised": cls("surprised", "wide", "open", "raised"),
            "confused": cls("confused", "uneven", "wavy", "raised"),
            # Extended expressions
            "sleepy": cls("sleepy", "closed", "normal", "relaxed"),
            "excited": cls("excited", "stars", "grin", "raised"),
            "scared": cls("scared", "wide", "gasp", "worried"),
            "smirk": cls("smirk", "normal", "smirk", "asymmetric"),
            "crying": cls("crying", "tears", "frown", "worried"),
        }
        return presets.get(name, cls())


class Pose:
    """Character pose definition.

    Poses define limb angles (in degrees) and body tilt:
    - left_arm/right_arm: Arm angles (0=down, positive=forward, negative=back)
    - left_leg/right_leg: Leg angles from vertical (0=straight, positive=forward)
    - body_angle: Body tilt angle (positive=leaning forward)
    """

    # Standard poses
    STANDING = "standing"
    SITTING = "sitting"
    WALKING = "walking"
    RUNNING = "running"
    POINTING = "pointing"
    WAVING = "waving"
    # Extended poses
    JUMPING = "jumping"
    DANCING = "dancing"
    LYING = "lying"
    KNEELING = "kneeling"
    CHEERING = "cheering"
    THINKING = "thinking"

    def __init__(
        self,
        name: str = "standing",
        left_arm: float = 0,
        right_arm: float = 0,
        left_leg: float = 0,
        right_leg: float = 0,
        body_angle: float = 0,
    ) -> None:
        self.name = name
        self.left_arm = left_arm
        self.right_arm = right_arm
        self.left_leg = left_leg
        self.right_leg = right_leg
        self.body_angle = body_angle

    @classmethod
    def from_name(cls, name: str) -> Pose:
        """Create pose from preset name."""
        presets = {
            # Standard poses
            "standing": cls("standing", -15, 15, 0, 0, 0),
            "sitting": cls("sitting", -30, 30, 90, 90, 0),
            "walking": cls("walking", 30, -30, 20, -20, 0),
            "running": cls("running", 60, -60, 45, -45, 10),
            "pointing": cls("pointing", -90, 15, 0, 0, 0),
            "waving": cls("waving", -135, 15, 0, 0, 0),
            # Extended poses
            "jumping": cls("jumping", -45, 45, -30, -30, -5),  # Arms up, legs bent back
            "dancing": cls("dancing", -120, 45, 30, -15, 5),  # Asymmetric dance pose
            "lying": cls("lying", 0, 0, 0, 0, 90),  # Horizontal body
            "kneeling": cls("kneeling", -30, 30, 90, 120, 0),  # One knee down
            "cheering": cls("cheering", -150, -150, 0, 0, -5),  # Both arms raised high
            "thinking": cls("thinking", 60, 15, 0, 0, 0),  # Hand on chin pose
        }
        return presets.get(name, cls())


class Character(CObject):
    """Base class for comic characters."""

    def __init__(
        self,
        name: str = "Character",
        style: str = "stickman",
        color: str = "#000000",
        fill_color: str | None = None,
        height: float = 100.0,
        expression: str | Expression = "neutral",
        pose: str | Pose = "standing",
        facing: str = "right",
        **kwargs: Any,
    ) -> None:
        super().__init__(name=name, **kwargs)

        self.style = style
        self.color = color
        self.fill_color = fill_color
        self.character_height = height
        self.facing = facing

        self._expression = self._resolve_expression(expression)
        self._pose = self._resolve_pose(pose)

        self.generate_points()

    def _resolve_expression(self, expr: str | Expression) -> Expression:
        if isinstance(expr, Expression):
            return expr
        return Expression.from_name(expr)

    def _resolve_pose(self, pose: str | Pose) -> Pose:
        if isinstance(pose, Pose):
            return pose
        return Pose.from_name(pose)

    def set_expression(self, expression: str | Expression) -> Self:
        """Set character expression."""
        self._expression = self._resolve_expression(expression)
        self._needs_update = True
        self.generate_points()
        return self

    def set_pose(self, pose: str | Pose) -> Self:
        """Set character pose."""
        self._pose = self._resolve_pose(pose)
        self._needs_update = True
        self.generate_points()
        return self

    def face(self, direction: str) -> Self:
        """Set facing direction.

        Args:
            direction: "left", "right", "front", or "back"
        """
        self.facing = direction
        self._needs_update = True
        return self

    def say(self, text: str, **bubble_kwargs: Any) -> Bubble:
        """Create a speech bubble attached to this character."""
        from comix.cobject.bubble.bubble import SpeechBubble

        bubble = SpeechBubble(text, **bubble_kwargs)
        bubble.attach_to(self)
        return bubble

    def think(self, text: str, **bubble_kwargs: Any) -> Bubble:
        """Create a thought bubble attached to this character."""
        from comix.cobject.bubble.bubble import ThoughtBubble

        bubble = ThoughtBubble(text, **bubble_kwargs)
        bubble.attach_to(self)
        return bubble

    def shout(self, text: str, **bubble_kwargs: Any) -> Bubble:
        """Create a shout bubble attached to this character."""
        from comix.cobject.bubble.bubble import ShoutBubble

        bubble = ShoutBubble(text, **bubble_kwargs)
        bubble.attach_to(self)
        return bubble

    def whisper(self, text: str, **bubble_kwargs: Any) -> Bubble:
        """Create a whisper bubble attached to this character."""
        from comix.cobject.bubble.bubble import WhisperBubble

        bubble = WhisperBubble(text, **bubble_kwargs)
        bubble.attach_to(self)
        return bubble

    def generate_points(self) -> None:
        """Generate character outline. Override in subclasses."""
        half_h = self.character_height / 2
        half_w = self.character_height * 0.3

        self._points = np.array(
            [
                [-half_w, -half_h],
                [half_w, -half_h],
                [half_w, half_h],
                [-half_w, half_h],
            ],
            dtype=np.float64,
        )

    def get_render_data(self) -> dict[str, Any]:
        """Get data for rendering."""
        data = super().get_render_data()
        data.update(
            {
                "character_name": self.name,
                "style": self.style,
                "color": self.color,
                "fill_color": self.fill_color,
                "character_height": self.character_height,
                "facing": self.facing,
                "expression": {
                    "name": self._expression.name,
                    "eyes": self._expression.eyes,
                    "mouth": self._expression.mouth,
                    "eyebrows": self._expression.eyebrows,
                },
                "pose": {
                    "name": self._pose.name,
                    "left_arm": self._pose.left_arm,
                    "right_arm": self._pose.right_arm,
                    "left_leg": self._pose.left_leg,
                    "right_leg": self._pose.right_leg,
                    "body_angle": self._pose.body_angle,
                },
            }
        )
        return data


class Stickman(Character):
    """Simple stick figure character."""

    def __init__(self, name: str = "Stickman", **kwargs: Any) -> None:
        kwargs.setdefault("style", "stickman")
        super().__init__(name=name, **kwargs)

    def generate_points(self) -> None:
        """Generate stickman figure points."""
        h = self.character_height

        head_radius = h * 0.15
        body_length = h * 0.35
        limb_length = h * 0.25

        points = []

        head_y = h / 2 - head_radius
        neck_y = head_y - head_radius
        hip_y = neck_y - body_length

        for angle in np.linspace(0, 2 * np.pi, 16):
            points.append([head_radius * np.cos(angle), head_y + head_radius * np.sin(angle)])

        points.append([0, neck_y])
        points.append([0, hip_y])

        arm_y = neck_y - body_length * 0.2
        left_arm_angle = np.radians(self._pose.left_arm)
        right_arm_angle = np.radians(self._pose.right_arm)

        points.append([0, arm_y])
        points.append([
            -limb_length * np.cos(left_arm_angle),
            arm_y - limb_length * np.sin(left_arm_angle),
        ])
        points.append([0, arm_y])
        points.append([
            limb_length * np.cos(right_arm_angle),
            arm_y - limb_length * np.sin(right_arm_angle),
        ])

        left_leg_angle = np.radians(90 + self._pose.left_leg)
        right_leg_angle = np.radians(90 + self._pose.right_leg)

        points.append([0, hip_y])
        points.append([
            -limb_length * np.cos(left_leg_angle),
            hip_y - limb_length * np.sin(left_leg_angle),
        ])
        points.append([0, hip_y])
        points.append([
            limb_length * np.cos(right_leg_angle),
            hip_y - limb_length * np.sin(right_leg_angle),
        ])

        self._points = np.array(points, dtype=np.float64)

        if self.facing == "left":
            self._points[:, 0] *= -1


class SimpleFace(Character):
    """Simple emoji-style face character."""

    def __init__(self, name: str = "Face", **kwargs: Any) -> None:
        kwargs.setdefault("style", "simple")
        kwargs.setdefault("height", 60.0)
        super().__init__(name=name, **kwargs)

    def generate_points(self) -> None:
        """Generate simple face points (circle with features)."""
        radius = self.character_height / 2

        points = []
        for angle in np.linspace(0, 2 * np.pi, 32):
            points.append([radius * np.cos(angle), radius * np.sin(angle)])

        self._points = np.array(points, dtype=np.float64)

    def get_render_data(self) -> dict[str, Any]:
        """Get data for rendering."""
        data = super().get_render_data()
        data["face_radius"] = self.character_height / 2
        return data


class ChubbyStickman(Character):
    """Rounded, friendly stick figure character.

    A more approachable version of Stickman with:
    - Larger, rounder head
    - Rounded body (oval torso)
    - Shorter, thicker limbs with rounded ends
    - Suitable for cute/chibi comic styles
    """

    def __init__(self, name: str = "ChubbyStickman", **kwargs: Any) -> None:
        kwargs.setdefault("style", "chubby")
        kwargs.setdefault("fill_color", "#FFFFFF")  # Default white fill for body
        super().__init__(name=name, **kwargs)

    def generate_points(self) -> None:
        """Generate chubby stickman figure points."""
        h = self.character_height

        # Proportions: larger head, shorter body, thicker limbs
        head_radius = h * 0.22  # Larger head than regular stickman (0.15)
        body_height = h * 0.28  # Shorter body
        body_width = h * 0.18  # Oval body width
        limb_length = h * 0.18  # Shorter limbs
        limb_thickness = h * 0.04  # Limb thickness for rounded ends

        points = []

        # Head position (higher up to accommodate larger head)
        head_y = h / 2 - head_radius
        neck_y = head_y - head_radius
        hip_y = neck_y - body_height

        # Generate head circle points
        for angle in np.linspace(0, 2 * np.pi, 24):
            points.append([
                head_radius * np.cos(angle),
                head_y + head_radius * np.sin(angle)
            ])

        # Generate body oval points (ellipse)
        body_center_y = (neck_y + hip_y) / 2
        for angle in np.linspace(0, 2 * np.pi, 16):
            points.append([
                body_width * np.cos(angle),
                body_center_y + (body_height / 2) * np.sin(angle)
            ])

        # Arm attachment point
        arm_y = neck_y - body_height * 0.15

        # Left arm
        left_arm_angle = np.radians(self._pose.left_arm)
        left_arm_end_x = -body_width - limb_length * np.cos(left_arm_angle)
        left_arm_end_y = arm_y - limb_length * np.sin(left_arm_angle)
        points.append([-body_width, arm_y])
        points.append([left_arm_end_x, left_arm_end_y])
        # Add rounded end point
        for angle in np.linspace(0, 2 * np.pi, 8):
            points.append([
                left_arm_end_x + limb_thickness * np.cos(angle),
                left_arm_end_y + limb_thickness * np.sin(angle)
            ])

        # Right arm
        right_arm_angle = np.radians(self._pose.right_arm)
        right_arm_end_x = body_width + limb_length * np.cos(right_arm_angle)
        right_arm_end_y = arm_y - limb_length * np.sin(right_arm_angle)
        points.append([body_width, arm_y])
        points.append([right_arm_end_x, right_arm_end_y])
        # Add rounded end point
        for angle in np.linspace(0, 2 * np.pi, 8):
            points.append([
                right_arm_end_x + limb_thickness * np.cos(angle),
                right_arm_end_y + limb_thickness * np.sin(angle)
            ])

        # Left leg
        left_leg_angle = np.radians(90 + self._pose.left_leg)
        left_leg_end_x = -body_width * 0.5 - limb_length * np.cos(left_leg_angle)
        left_leg_end_y = hip_y - limb_length * np.sin(left_leg_angle)
        points.append([-body_width * 0.5, hip_y])
        points.append([left_leg_end_x, left_leg_end_y])
        # Add rounded end (foot)
        for angle in np.linspace(0, 2 * np.pi, 8):
            points.append([
                left_leg_end_x + limb_thickness * 1.2 * np.cos(angle),
                left_leg_end_y + limb_thickness * np.sin(angle)
            ])

        # Right leg
        right_leg_angle = np.radians(90 + self._pose.right_leg)
        right_leg_end_x = body_width * 0.5 + limb_length * np.cos(right_leg_angle)
        right_leg_end_y = hip_y - limb_length * np.sin(right_leg_angle)
        points.append([body_width * 0.5, hip_y])
        points.append([right_leg_end_x, right_leg_end_y])
        # Add rounded end (foot)
        for angle in np.linspace(0, 2 * np.pi, 8):
            points.append([
                right_leg_end_x + limb_thickness * 1.2 * np.cos(angle),
                right_leg_end_y + limb_thickness * np.sin(angle)
            ])

        self._points = np.array(points, dtype=np.float64)

        if self.facing == "left":
            self._points[:, 0] *= -1

    def get_render_data(self) -> dict[str, Any]:
        """Get data for rendering."""
        data = super().get_render_data()
        # Add chubby-specific render info
        data["head_ratio"] = 0.22  # Larger head ratio
        data["body_width_ratio"] = 0.18  # Body width ratio
        data["limb_thickness"] = self.character_height * 0.04
        return data


class Robot(Character):
    """Robot/mechanical character with geometric design.

    A mechanical character with:
    - Square head with screen-like face display
    - Rectangular body with panel details
    - Angular jointed limbs
    - LED-style eyes and digital display expressions
    - Optional antenna

    Suitable for sci-fi comics, tech themes, and futuristic stories.
    """

    def __init__(
        self,
        name: str = "Robot",
        antenna: bool = True,
        panel_color: str = "#4A4A4A",
        screen_color: str = "#1A1A2E",
        led_color: str = "#00FF88",
        **kwargs: Any,
    ) -> None:
        """Initialize Robot character.

        Args:
            name: Character name
            antenna: Whether to draw antenna on head
            panel_color: Color for body panels (default dark gray)
            screen_color: Color for face screen background (default dark blue)
            led_color: Color for LED elements like eyes (default green)
            **kwargs: Additional Character parameters
        """
        kwargs.setdefault("style", "robot")
        kwargs.setdefault("color", "#333333")
        kwargs.setdefault("fill_color", "#6B7280")  # Metal gray
        self.antenna = antenna
        self.panel_color = panel_color
        self.screen_color = screen_color
        self.led_color = led_color
        super().__init__(name=name, **kwargs)

    def generate_points(self) -> None:
        """Generate robot figure points.

        Structure:
        - Head: Rectangle with rounded corners (indicated by points)
        - Body: Rectangle
        - Arms: Two-segment limbs with joint indicators
        - Legs: Two-segment limbs with joint indicators
        """
        h = self.character_height

        # Proportions for robot
        head_height = h * 0.25
        head_width = h * 0.22
        body_height = h * 0.30
        body_width = h * 0.26
        limb_length = h * 0.22
        joint_size = h * 0.03
        antenna_height = h * 0.08

        points = []

        # Calculate positions
        head_top = h / 2
        if self.antenna:
            head_top -= antenna_height
        head_bottom = head_top - head_height
        neck_y = head_bottom
        body_top = neck_y - h * 0.02  # Small gap for neck
        body_bottom = body_top - body_height
        hip_y = body_bottom

        # Antenna (if enabled) - 2 points
        if self.antenna:
            points.append([0, head_top + antenna_height])  # Antenna tip
            points.append([0, head_top])  # Antenna base

        # Head rectangle - 4 corner points (clockwise from top-left)
        points.append([-head_width / 2, head_top])  # Top-left
        points.append([head_width / 2, head_top])   # Top-right
        points.append([head_width / 2, head_bottom])  # Bottom-right
        points.append([-head_width / 2, head_bottom])  # Bottom-left

        # Body rectangle - 4 corner points
        points.append([-body_width / 2, body_top])  # Top-left
        points.append([body_width / 2, body_top])   # Top-right
        points.append([body_width / 2, body_bottom])  # Bottom-right
        points.append([-body_width / 2, body_bottom])  # Bottom-left

        # Arms - each arm has: shoulder, elbow, hand positions + joint circle points
        arm_y = body_top - body_height * 0.15

        # Left arm
        left_arm_angle = np.radians(self._pose.left_arm)
        shoulder_left = [-body_width / 2, arm_y]
        elbow_left_x = shoulder_left[0] - limb_length * 0.5 * np.cos(left_arm_angle)
        elbow_left_y = arm_y - limb_length * 0.5 * np.sin(left_arm_angle)
        hand_left_x = shoulder_left[0] - limb_length * np.cos(left_arm_angle)
        hand_left_y = arm_y - limb_length * np.sin(left_arm_angle)

        points.append(shoulder_left)
        points.append([elbow_left_x, elbow_left_y])
        points.append([hand_left_x, hand_left_y])
        # Joint circle indicator (4 points around elbow)
        for angle in [0, np.pi / 2, np.pi, 3 * np.pi / 2]:
            points.append([
                elbow_left_x + joint_size * np.cos(angle),
                elbow_left_y + joint_size * np.sin(angle)
            ])

        # Right arm
        right_arm_angle = np.radians(self._pose.right_arm)
        shoulder_right = [body_width / 2, arm_y]
        elbow_right_x = shoulder_right[0] + limb_length * 0.5 * np.cos(right_arm_angle)
        elbow_right_y = arm_y - limb_length * 0.5 * np.sin(right_arm_angle)
        hand_right_x = shoulder_right[0] + limb_length * np.cos(right_arm_angle)
        hand_right_y = arm_y - limb_length * np.sin(right_arm_angle)

        points.append(shoulder_right)
        points.append([elbow_right_x, elbow_right_y])
        points.append([hand_right_x, hand_right_y])
        # Joint circle indicator
        for angle in [0, np.pi / 2, np.pi, 3 * np.pi / 2]:
            points.append([
                elbow_right_x + joint_size * np.cos(angle),
                elbow_right_y + joint_size * np.sin(angle)
            ])

        # Legs - similar structure
        leg_start_y = hip_y

        # Left leg
        left_leg_angle = np.radians(90 + self._pose.left_leg)
        hip_left = [-body_width / 4, leg_start_y]
        knee_left_x = hip_left[0] - limb_length * 0.5 * np.cos(left_leg_angle)
        knee_left_y = leg_start_y - limb_length * 0.5 * np.sin(left_leg_angle)
        foot_left_x = hip_left[0] - limb_length * np.cos(left_leg_angle)
        foot_left_y = leg_start_y - limb_length * np.sin(left_leg_angle)

        points.append(hip_left)
        points.append([knee_left_x, knee_left_y])
        points.append([foot_left_x, foot_left_y])
        # Knee joint indicator
        for angle in [0, np.pi / 2, np.pi, 3 * np.pi / 2]:
            points.append([
                knee_left_x + joint_size * np.cos(angle),
                knee_left_y + joint_size * np.sin(angle)
            ])

        # Right leg
        right_leg_angle = np.radians(90 + self._pose.right_leg)
        hip_right = [body_width / 4, leg_start_y]
        knee_right_x = hip_right[0] + limb_length * 0.5 * np.cos(right_leg_angle)
        knee_right_y = leg_start_y - limb_length * 0.5 * np.sin(right_leg_angle)
        foot_right_x = hip_right[0] + limb_length * np.cos(right_leg_angle)
        foot_right_y = leg_start_y - limb_length * np.sin(right_leg_angle)

        points.append(hip_right)
        points.append([knee_right_x, knee_right_y])
        points.append([foot_right_x, foot_right_y])
        # Knee joint indicator
        for angle in [0, np.pi / 2, np.pi, 3 * np.pi / 2]:
            points.append([
                knee_right_x + joint_size * np.cos(angle),
                knee_right_y + joint_size * np.sin(angle)
            ])

        self._points = np.array(points, dtype=np.float64)

        if self.facing == "left":
            self._points[:, 0] *= -1

    def get_render_data(self) -> dict[str, Any]:
        """Get data for rendering."""
        data = super().get_render_data()
        # Add robot-specific render info
        data["antenna"] = self.antenna
        data["panel_color"] = self.panel_color
        data["screen_color"] = self.screen_color
        data["led_color"] = self.led_color
        data["head_height_ratio"] = 0.25
        data["head_width_ratio"] = 0.22
        data["body_height_ratio"] = 0.30
        data["body_width_ratio"] = 0.26
        data["joint_size"] = self.character_height * 0.03
        return data
