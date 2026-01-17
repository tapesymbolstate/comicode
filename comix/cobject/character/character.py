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


class Chibi(Character):
    """Chibi/super-deformed anime-style character.

    A cute, stylized character with exaggerated proportions:
    - Very large head (40% of height) with big expressive eyes
    - Small, simplified body (bean-shaped torso)
    - Short stubby limbs
    - Rounded, cute aesthetic

    Suitable for comedic scenes, cute moments, and kawaii-style comics.
    """

    def __init__(
        self,
        name: str = "Chibi",
        hair_style: str = "spiky",
        hair_color: str = "#333333",
        skin_color: str = "#FFE4C4",
        outfit_color: str = "#4A90D9",
        blush: bool = False,
        **kwargs: Any,
    ) -> None:
        """Initialize Chibi character.

        Args:
            name: Character name
            hair_style: Hair style ("spiky", "long", "short", "twintails", "none")
            hair_color: Color for hair
            skin_color: Skin tone color (default bisque)
            outfit_color: Color for simple outfit/body
            blush: Whether to show cute blush marks on cheeks
            **kwargs: Additional Character parameters
        """
        kwargs.setdefault("style", "chibi")
        kwargs.setdefault("color", "#333333")
        kwargs.setdefault("fill_color", skin_color)
        self.hair_style = hair_style
        self.hair_color = hair_color
        self.skin_color = skin_color
        self.outfit_color = outfit_color
        self.blush = blush
        super().__init__(name=name, **kwargs)

    def generate_points(self) -> None:
        """Generate chibi figure points.

        Structure:
        - Head: Large circle (40% of height)
        - Body: Small bean/oval shape
        - Arms: Short stubby limbs
        - Legs: Short stubby limbs
        """
        h = self.character_height

        # Chibi proportions: huge head, tiny body
        head_radius = h * 0.20  # 40% of height for head diameter
        body_height = h * 0.22
        body_width = h * 0.16
        limb_length = h * 0.12
        limb_thickness = h * 0.05

        points = []

        # Head position - takes up top portion
        head_y = h / 2 - head_radius
        head_bottom = head_y - head_radius
        body_top = head_bottom - h * 0.02  # Small gap
        body_bottom = body_top - body_height

        # Generate large head circle points
        for angle in np.linspace(0, 2 * np.pi, 32):
            points.append([
                head_radius * np.cos(angle),
                head_y + head_radius * np.sin(angle)
            ])

        # Generate body oval (bean shape) points
        body_center_y = (body_top + body_bottom) / 2
        for angle in np.linspace(0, 2 * np.pi, 20):
            points.append([
                body_width * np.cos(angle),
                body_center_y + (body_height / 2) * np.sin(angle)
            ])

        # Arms - short and stubby
        arm_y = body_top - body_height * 0.2

        # Left arm
        left_arm_angle = np.radians(self._pose.left_arm)
        left_arm_end_x = -body_width - limb_length * np.cos(left_arm_angle)
        left_arm_end_y = arm_y - limb_length * np.sin(left_arm_angle)
        points.append([-body_width, arm_y])
        points.append([left_arm_end_x, left_arm_end_y])
        # Rounded hand
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
        # Rounded hand
        for angle in np.linspace(0, 2 * np.pi, 8):
            points.append([
                right_arm_end_x + limb_thickness * np.cos(angle),
                right_arm_end_y + limb_thickness * np.sin(angle)
            ])

        # Legs - short and stubby
        leg_start_y = body_bottom

        # Left leg
        left_leg_angle = np.radians(90 + self._pose.left_leg)
        left_leg_end_x = -body_width * 0.4 - limb_length * np.cos(left_leg_angle)
        left_leg_end_y = leg_start_y - limb_length * np.sin(left_leg_angle)
        points.append([-body_width * 0.4, leg_start_y])
        points.append([left_leg_end_x, left_leg_end_y])
        # Rounded foot
        for angle in np.linspace(0, 2 * np.pi, 8):
            points.append([
                left_leg_end_x + limb_thickness * 1.3 * np.cos(angle),
                left_leg_end_y + limb_thickness * 0.8 * np.sin(angle)
            ])

        # Right leg
        right_leg_angle = np.radians(90 + self._pose.right_leg)
        right_leg_end_x = body_width * 0.4 + limb_length * np.cos(right_leg_angle)
        right_leg_end_y = leg_start_y - limb_length * np.sin(right_leg_angle)
        points.append([body_width * 0.4, leg_start_y])
        points.append([right_leg_end_x, right_leg_end_y])
        # Rounded foot
        for angle in np.linspace(0, 2 * np.pi, 8):
            points.append([
                right_leg_end_x + limb_thickness * 1.3 * np.cos(angle),
                right_leg_end_y + limb_thickness * 0.8 * np.sin(angle)
            ])

        self._points = np.array(points, dtype=np.float64)

        if self.facing == "left":
            self._points[:, 0] *= -1

    def get_render_data(self) -> dict[str, Any]:
        """Get data for rendering."""
        data = super().get_render_data()
        # Add chibi-specific render info
        data["hair_style"] = self.hair_style
        data["hair_color"] = self.hair_color
        data["skin_color"] = self.skin_color
        data["outfit_color"] = self.outfit_color
        data["blush"] = self.blush
        data["head_radius_ratio"] = 0.20  # 40% diameter
        data["body_height_ratio"] = 0.22
        data["body_width_ratio"] = 0.16
        data["limb_length_ratio"] = 0.12
        data["limb_thickness"] = self.character_height * 0.05
        return data


class Anime(Character):
    """Anime/manga style character with typical anime proportions.

    A character with distinctive anime/manga visual features:
    - Large expressive eyes with highlights (anime trademark)
    - Smaller nose and mouth
    - Natural body proportions (not super-deformed)
    - Distinct hair styles (ponytail, bob, flowing, short, spiky)
    - Visible neck and shoulders
    - Slender build with defined limbs

    Suitable for serious manga, shoujo/shounen styles, and dramatic scenes.
    """

    def __init__(
        self,
        name: str = "Anime",
        hair_style: str = "flowing",
        hair_color: str = "#2D1B12",
        skin_color: str = "#FFE0C4",
        outfit_color: str = "#3B82F6",
        eye_color: str = "#4A90D9",
        gender: str = "neutral",
        **kwargs: Any,
    ) -> None:
        """Initialize Anime character.

        Args:
            name: Character name
            hair_style: Hair style ("flowing", "ponytail", "short", "spiky", "bob", "twintails", "none")
            hair_color: Color for hair (default dark brown)
            skin_color: Skin tone color (default peach)
            outfit_color: Color for outfit (default blue)
            eye_color: Color for eyes (default blue)
            gender: Body type hint ("neutral", "masculine", "feminine")
            **kwargs: Additional Character parameters
        """
        kwargs.setdefault("style", "anime")
        kwargs.setdefault("color", "#333333")
        kwargs.setdefault("fill_color", skin_color)
        self.hair_style = hair_style
        self.hair_color = hair_color
        self.skin_color = skin_color
        self.outfit_color = outfit_color
        self.eye_color = eye_color
        self.gender = gender
        super().__init__(name=name, **kwargs)

    def generate_points(self) -> None:
        """Generate anime figure points.

        Structure:
        - Head: Slightly oval/tapered face shape
        - Neck: Visible thin neck
        - Body: Natural proportions with shoulders
        - Arms: Slender limbs with defined shape
        - Legs: Long slender legs
        """
        h = self.character_height

        # Anime proportions: head is ~1/7 of height (natural proportions)
        head_height = h * 0.14
        head_width = h * 0.10
        neck_height = h * 0.04
        neck_width = h * 0.03
        shoulder_width = h * 0.22
        body_height = h * 0.30
        body_width = h * 0.12
        arm_length = h * 0.26
        leg_length = h * 0.32
        limb_width = h * 0.025

        points = []

        # Calculate vertical positions
        head_top = h / 2
        head_center_y = head_top - head_height / 2
        head_bottom = head_top - head_height
        neck_bottom = head_bottom - neck_height
        shoulder_y = neck_bottom
        body_bottom = shoulder_y - body_height
        hip_y = body_bottom

        # Generate head shape (slightly tapered oval - anime face shape)
        # Top half is more rounded, bottom tapers to chin
        for i, angle in enumerate(np.linspace(0, 2 * np.pi, 32)):
            # Make the bottom half narrower (chin)
            width_mod = 1.0 if np.sin(angle) >= 0 else 0.8
            # Slightly taller than wide
            points.append([
                head_width * width_mod * np.cos(angle),
                head_center_y + head_height * 0.55 * np.sin(angle)
            ])

        # Neck points
        points.append([-neck_width, head_bottom])
        points.append([-neck_width, neck_bottom])
        points.append([neck_width, neck_bottom])
        points.append([neck_width, head_bottom])

        # Shoulders and body (torso trapezoid tapering down)
        waist_width = body_width * 0.8
        points.append([-shoulder_width / 2, shoulder_y])  # Left shoulder
        points.append([-waist_width, body_bottom])  # Left hip
        points.append([waist_width, body_bottom])  # Right hip
        points.append([shoulder_width / 2, shoulder_y])  # Right shoulder

        # Arms
        arm_y = shoulder_y - h * 0.02

        # Left arm
        left_arm_angle = np.radians(self._pose.left_arm)
        left_elbow_x = -shoulder_width / 2 - arm_length * 0.5 * np.cos(left_arm_angle)
        left_elbow_y = arm_y - arm_length * 0.5 * np.sin(left_arm_angle)
        left_hand_x = -shoulder_width / 2 - arm_length * np.cos(left_arm_angle)
        left_hand_y = arm_y - arm_length * np.sin(left_arm_angle)

        points.append([-shoulder_width / 2, arm_y])  # Shoulder
        points.append([left_elbow_x, left_elbow_y])  # Elbow
        points.append([left_hand_x, left_hand_y])  # Hand
        # Hand circle
        for angle in np.linspace(0, 2 * np.pi, 8):
            points.append([
                left_hand_x + limb_width * 1.5 * np.cos(angle),
                left_hand_y + limb_width * 1.5 * np.sin(angle)
            ])

        # Right arm
        right_arm_angle = np.radians(self._pose.right_arm)
        right_elbow_x = shoulder_width / 2 + arm_length * 0.5 * np.cos(right_arm_angle)
        right_elbow_y = arm_y - arm_length * 0.5 * np.sin(right_arm_angle)
        right_hand_x = shoulder_width / 2 + arm_length * np.cos(right_arm_angle)
        right_hand_y = arm_y - arm_length * np.sin(right_arm_angle)

        points.append([shoulder_width / 2, arm_y])  # Shoulder
        points.append([right_elbow_x, right_elbow_y])  # Elbow
        points.append([right_hand_x, right_hand_y])  # Hand
        # Hand circle
        for angle in np.linspace(0, 2 * np.pi, 8):
            points.append([
                right_hand_x + limb_width * 1.5 * np.cos(angle),
                right_hand_y + limb_width * 1.5 * np.sin(angle)
            ])

        # Legs
        leg_gap = body_width * 0.4

        # Left leg
        left_leg_angle = np.radians(90 + self._pose.left_leg)
        left_knee_x = -leg_gap - leg_length * 0.5 * np.cos(left_leg_angle)
        left_knee_y = hip_y - leg_length * 0.5 * np.sin(left_leg_angle)
        left_foot_x = -leg_gap - leg_length * np.cos(left_leg_angle)
        left_foot_y = hip_y - leg_length * np.sin(left_leg_angle)

        points.append([-leg_gap, hip_y])  # Hip
        points.append([left_knee_x, left_knee_y])  # Knee
        points.append([left_foot_x, left_foot_y])  # Foot
        # Foot shape (oval)
        for angle in np.linspace(0, 2 * np.pi, 8):
            points.append([
                left_foot_x + limb_width * 2 * np.cos(angle),
                left_foot_y + limb_width * np.sin(angle)
            ])

        # Right leg
        right_leg_angle = np.radians(90 + self._pose.right_leg)
        right_knee_x = leg_gap + leg_length * 0.5 * np.cos(right_leg_angle)
        right_knee_y = hip_y - leg_length * 0.5 * np.sin(right_leg_angle)
        right_foot_x = leg_gap + leg_length * np.cos(right_leg_angle)
        right_foot_y = hip_y - leg_length * np.sin(right_leg_angle)

        points.append([leg_gap, hip_y])  # Hip
        points.append([right_knee_x, right_knee_y])  # Knee
        points.append([right_foot_x, right_foot_y])  # Foot
        # Foot shape (oval)
        for angle in np.linspace(0, 2 * np.pi, 8):
            points.append([
                right_foot_x + limb_width * 2 * np.cos(angle),
                right_foot_y + limb_width * np.sin(angle)
            ])

        self._points = np.array(points, dtype=np.float64)

        if self.facing == "left":
            self._points[:, 0] *= -1

    def get_render_data(self) -> dict[str, Any]:
        """Get data for rendering."""
        data = super().get_render_data()
        # Add anime-specific render info
        data["hair_style"] = self.hair_style
        data["hair_color"] = self.hair_color
        data["skin_color"] = self.skin_color
        data["outfit_color"] = self.outfit_color
        data["eye_color"] = self.eye_color
        data["gender"] = self.gender
        data["head_height_ratio"] = 0.14
        data["head_width_ratio"] = 0.10
        data["shoulder_width_ratio"] = 0.22
        data["body_height_ratio"] = 0.30
        data["arm_length_ratio"] = 0.26
        data["leg_length_ratio"] = 0.32
        return data


class Cartoon(Character):
    """Classic Western cartoon character with exaggerated features.

    A character with classic cartoon aesthetics inspired by Tex Avery, Disney,
    and classic animation studios:
    - Large round head with exaggerated features
    - Pear-shaped or bean-shaped body
    - Big expressive eyes with thick outlines
    - Simple hands (mitten-style or 4-finger)
    - Squash-and-stretch friendly proportions
    - Bold, thick outlines characteristic of classic animation

    Suitable for comedy comics, children's content, and classic Western-style comics.
    """

    def __init__(
        self,
        name: str = "Cartoon",
        body_shape: str = "pear",  # "pear", "bean", "round"
        skin_color: str = "#FFDAB9",  # Peach puff
        outline_color: str = "#000000",
        outfit_color: str = "#4169E1",  # Royal blue
        hair_color: str = "#8B4513",  # Saddle brown
        nose_type: str = "round",  # "round", "triangle", "long"
        ear_size: str = "normal",  # "small", "normal", "large"
        gloves: bool = True,  # Classic cartoon gloves
        **kwargs: Any,
    ) -> None:
        """Initialize Cartoon character.

        Args:
            name: Character name
            body_shape: Body shape type ("pear", "bean", "round")
            skin_color: Skin/body color (default peach)
            outline_color: Outline color (default black)
            outfit_color: Color for outfit/clothes (default royal blue)
            hair_color: Color for hair
            nose_type: Nose shape ("round", "triangle", "long")
            ear_size: Ear size ("small", "normal", "large")
            gloves: Whether to draw classic white cartoon gloves
            **kwargs: Additional Character parameters
        """
        kwargs.setdefault("style", "cartoon")
        kwargs.setdefault("color", outline_color)
        kwargs.setdefault("fill_color", skin_color)
        self.body_shape = body_shape
        self.skin_color = skin_color
        self.outline_color = outline_color
        self.outfit_color = outfit_color
        self.hair_color = hair_color
        self.nose_type = nose_type
        self.ear_size = ear_size
        self.gloves = gloves
        super().__init__(name=name, **kwargs)

    def generate_points(self) -> None:
        """Generate cartoon figure points.

        Structure:
        - Head: Large circle (35% of height)
        - Body: Pear/bean/round shape based on body_shape
        - Arms: Simple curved limbs with mitten hands
        - Legs: Short stubby legs with rounded feet
        """
        h = self.character_height

        # Cartoon proportions: big head, small body
        head_radius = h * 0.175  # 35% diameter for head
        body_height = h * 0.32
        body_width_top = h * 0.12
        body_width_bottom = h * 0.16 if self.body_shape == "pear" else h * 0.12
        arm_length = h * 0.20
        hand_size = h * 0.05  # Mitten hand size
        leg_length = h * 0.18
        foot_width = h * 0.06
        foot_height = h * 0.03

        points = []

        # Calculate vertical positions
        head_top = h / 2
        head_center_y = head_top - head_radius
        head_bottom = head_top - head_radius * 2
        neck_y = head_bottom
        body_top = neck_y - h * 0.01  # Small gap
        body_bottom = body_top - body_height
        hip_y = body_bottom

        # Generate large head circle (32 points for smooth circle)
        for angle in np.linspace(0, 2 * np.pi, 32):
            points.append([
                head_radius * np.cos(angle),
                head_center_y + head_radius * np.sin(angle)
            ])

        # Generate body shape based on body_shape parameter
        body_center_y = (body_top + body_bottom) / 2

        if self.body_shape == "pear":
            # Pear shape: narrow top, wider bottom
            for i, angle in enumerate(np.linspace(0, 2 * np.pi, 20)):
                # Interpolate width from top to bottom
                t = (np.sin(angle) + 1) / 2  # 0 at top, 1 at bottom
                width = body_width_top + (body_width_bottom - body_width_top) * t
                points.append([
                    width * np.cos(angle),
                    body_center_y + (body_height / 2) * np.sin(angle)
                ])
        elif self.body_shape == "bean":
            # Bean shape: slight S-curve body
            for angle in np.linspace(0, 2 * np.pi, 20):
                width_mod = 1.0 + 0.1 * np.sin(2 * angle)
                avg_width = (body_width_top + body_width_bottom) / 2
                points.append([
                    avg_width * width_mod * np.cos(angle),
                    body_center_y + (body_height / 2) * np.sin(angle)
                ])
        else:  # round
            # Simple oval body
            avg_width = (body_width_top + body_width_bottom) / 2
            for angle in np.linspace(0, 2 * np.pi, 20):
                points.append([
                    avg_width * np.cos(angle),
                    body_center_y + (body_height / 2) * np.sin(angle)
                ])

        # Arms - cartoon style with rounded ends
        arm_y = body_top - body_height * 0.15
        shoulder_offset = body_width_top * 0.9

        # Left arm
        left_arm_angle = np.radians(self._pose.left_arm)
        left_elbow_x = -shoulder_offset - arm_length * 0.5 * np.cos(left_arm_angle)
        left_elbow_y = arm_y - arm_length * 0.5 * np.sin(left_arm_angle)
        left_hand_x = -shoulder_offset - arm_length * np.cos(left_arm_angle)
        left_hand_y = arm_y - arm_length * np.sin(left_arm_angle)

        points.append([-shoulder_offset, arm_y])  # Shoulder
        points.append([left_elbow_x, left_elbow_y])  # Elbow
        points.append([left_hand_x, left_hand_y])  # Hand position
        # Mitten hand shape (circle/oval)
        for angle in np.linspace(0, 2 * np.pi, 10):
            points.append([
                left_hand_x + hand_size * np.cos(angle),
                left_hand_y + hand_size * 0.8 * np.sin(angle)
            ])

        # Right arm
        right_arm_angle = np.radians(self._pose.right_arm)
        right_elbow_x = shoulder_offset + arm_length * 0.5 * np.cos(right_arm_angle)
        right_elbow_y = arm_y - arm_length * 0.5 * np.sin(right_arm_angle)
        right_hand_x = shoulder_offset + arm_length * np.cos(right_arm_angle)
        right_hand_y = arm_y - arm_length * np.sin(right_arm_angle)

        points.append([shoulder_offset, arm_y])  # Shoulder
        points.append([right_elbow_x, right_elbow_y])  # Elbow
        points.append([right_hand_x, right_hand_y])  # Hand position
        # Mitten hand shape
        for angle in np.linspace(0, 2 * np.pi, 10):
            points.append([
                right_hand_x + hand_size * np.cos(angle),
                right_hand_y + hand_size * 0.8 * np.sin(angle)
            ])

        # Legs - short and stubby, cartoon style
        leg_gap = body_width_bottom * 0.3

        # Left leg
        left_leg_angle = np.radians(90 + self._pose.left_leg)
        left_knee_x = -leg_gap - leg_length * 0.5 * np.cos(left_leg_angle)
        left_knee_y = hip_y - leg_length * 0.5 * np.sin(left_leg_angle)
        left_foot_x = -leg_gap - leg_length * np.cos(left_leg_angle)
        left_foot_y = hip_y - leg_length * np.sin(left_leg_angle)

        points.append([-leg_gap, hip_y])  # Hip
        points.append([left_knee_x, left_knee_y])  # Knee
        points.append([left_foot_x, left_foot_y])  # Foot position
        # Cartoon shoe/foot (oval)
        for angle in np.linspace(0, 2 * np.pi, 8):
            points.append([
                left_foot_x + foot_width * np.cos(angle),
                left_foot_y + foot_height * np.sin(angle)
            ])

        # Right leg
        right_leg_angle = np.radians(90 + self._pose.right_leg)
        right_knee_x = leg_gap + leg_length * 0.5 * np.cos(right_leg_angle)
        right_knee_y = hip_y - leg_length * 0.5 * np.sin(right_leg_angle)
        right_foot_x = leg_gap + leg_length * np.cos(right_leg_angle)
        right_foot_y = hip_y - leg_length * np.sin(right_leg_angle)

        points.append([leg_gap, hip_y])  # Hip
        points.append([right_knee_x, right_knee_y])  # Knee
        points.append([right_foot_x, right_foot_y])  # Foot position
        # Cartoon shoe/foot (oval)
        for angle in np.linspace(0, 2 * np.pi, 8):
            points.append([
                right_foot_x + foot_width * np.cos(angle),
                right_foot_y + foot_height * np.sin(angle)
            ])

        self._points = np.array(points, dtype=np.float64)

        if self.facing == "left":
            self._points[:, 0] *= -1

    def get_render_data(self) -> dict[str, Any]:
        """Get data for rendering."""
        data = super().get_render_data()
        # Add cartoon-specific render info
        data["body_shape"] = self.body_shape
        data["skin_color"] = self.skin_color
        data["outline_color"] = self.outline_color
        data["outfit_color"] = self.outfit_color
        data["hair_color"] = self.hair_color
        data["nose_type"] = self.nose_type
        data["ear_size"] = self.ear_size
        data["gloves"] = self.gloves
        data["head_radius_ratio"] = 0.175  # 35% diameter
        data["body_height_ratio"] = 0.32
        data["arm_length_ratio"] = 0.20
        data["leg_length_ratio"] = 0.18
        data["hand_size"] = self.character_height * 0.05
        return data


class Superhero(Character):
    """Superhero character with heroic proportions and costume details.

    A character designed for action comics with:
    - Heroic proportions (broad shoulders, narrow waist)
    - Muscular build with defined body shape
    - Customizable costume with cape option
    - Mask/helmet options for secret identity
    - Dynamic pose-ready structure
    - Emblem/logo placement on chest

    Suitable for superhero comics, action sequences, and dramatic heroic scenes.
    """

    def __init__(
        self,
        name: str = "Superhero",
        costume_primary: str = "#DC2626",  # Primary costume color (red)
        costume_secondary: str = "#1D4ED8",  # Secondary costume color (blue)
        skin_color: str = "#FBBF24",  # Skin tone (default gold/tan)
        cape: bool = True,
        cape_color: str = "#DC2626",
        mask: str = "domino",  # "domino", "full", "cowl", "none"
        emblem: str = "star",  # "star", "diamond", "circle", "shield", "none"
        emblem_color: str = "#FBBF24",  # Emblem color (default gold)
        boots: bool = True,
        gloves: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize Superhero character.

        Args:
            name: Character name
            costume_primary: Primary costume color (default red)
            costume_secondary: Secondary costume color (default blue)
            skin_color: Skin tone color
            cape: Whether to draw a cape
            cape_color: Color for the cape
            mask: Mask type ("domino", "full", "cowl", "none")
            emblem: Chest emblem type ("star", "diamond", "circle", "shield", "none")
            emblem_color: Color for the chest emblem
            boots: Whether to draw boots (different color from legs)
            gloves: Whether to draw gloves (different color from arms)
            **kwargs: Additional Character parameters
        """
        kwargs.setdefault("style", "superhero")
        kwargs.setdefault("color", "#1F2937")  # Dark gray outline
        kwargs.setdefault("fill_color", skin_color)
        self.costume_primary = costume_primary
        self.costume_secondary = costume_secondary
        self.skin_color = skin_color
        self.cape = cape
        self.cape_color = cape_color
        self.mask = mask
        self.emblem = emblem
        self.emblem_color = emblem_color
        self.boots = boots
        self.gloves = gloves
        super().__init__(name=name, **kwargs)

    def generate_points(self) -> None:
        """Generate superhero figure points.

        Structure:
        - Head: Slightly angular/heroic face shape
        - Neck: Thick muscular neck
        - Torso: Broad shoulders tapering to narrow waist (heroic V-shape)
        - Arms: Muscular with defined biceps
        - Legs: Strong legs with defined thighs
        - Cape: Optional flowing cape points
        """
        h = self.character_height

        # Heroic proportions: head is ~1/8 of height, broader shoulders
        head_height = h * 0.12
        head_width = h * 0.09
        neck_height = h * 0.04
        neck_width = h * 0.05  # Thicker neck
        shoulder_width = h * 0.28  # Broader shoulders
        chest_width = h * 0.24
        waist_width = h * 0.14  # Narrow waist for V-taper
        hip_width = h * 0.16
        body_height = h * 0.32
        arm_length = h * 0.26
        arm_width = h * 0.04  # Thicker arms
        leg_length = h * 0.34
        leg_width = h * 0.05  # Thicker legs

        points = []

        # Calculate vertical positions
        head_top = h / 2
        head_center_y = head_top - head_height / 2
        head_bottom = head_top - head_height
        neck_bottom = head_bottom - neck_height
        shoulder_y = neck_bottom
        chest_y = shoulder_y - body_height * 0.3
        waist_y = shoulder_y - body_height * 0.7
        hip_y = shoulder_y - body_height

        # Generate head shape (more angular/heroic jawline)
        for i, angle in enumerate(np.linspace(0, 2 * np.pi, 24)):
            # Make the jaw more defined (wider at cheeks, narrower at chin)
            if np.sin(angle) < -0.3:  # Lower face
                width_mod = 0.75 + 0.15 * (1 + np.sin(angle))
            else:
                width_mod = 1.0
            points.append([
                head_width * width_mod * np.cos(angle),
                head_center_y + head_height * 0.5 * np.sin(angle)
            ])

        # Neck points (thick muscular neck)
        points.append([-neck_width, head_bottom])
        points.append([-neck_width, neck_bottom])
        points.append([neck_width, neck_bottom])
        points.append([neck_width, head_bottom])

        # Torso - heroic V-shape (shoulders to waist)
        # Left shoulder to left hip
        points.append([-shoulder_width / 2, shoulder_y])
        points.append([-chest_width / 2, chest_y])
        points.append([-waist_width / 2, waist_y])
        points.append([-hip_width / 2, hip_y])
        # Right hip to right shoulder
        points.append([hip_width / 2, hip_y])
        points.append([waist_width / 2, waist_y])
        points.append([chest_width / 2, chest_y])
        points.append([shoulder_width / 2, shoulder_y])

        # Arms - muscular with bicep bulge
        arm_y = shoulder_y - h * 0.015

        # Left arm
        left_arm_angle = np.radians(self._pose.left_arm)
        # Upper arm (shoulder to elbow)
        left_elbow_x = -shoulder_width / 2 - arm_length * 0.45 * np.cos(left_arm_angle)
        left_elbow_y = arm_y - arm_length * 0.45 * np.sin(left_arm_angle)
        # Forearm (elbow to hand)
        left_hand_x = -shoulder_width / 2 - arm_length * np.cos(left_arm_angle)
        left_hand_y = arm_y - arm_length * np.sin(left_arm_angle)

        points.append([-shoulder_width / 2, arm_y])  # Shoulder
        points.append([left_elbow_x, left_elbow_y])  # Elbow
        points.append([left_hand_x, left_hand_y])  # Hand
        # Fist/hand (8 points for rectangular fist shape)
        fist_size = arm_width * 1.2
        for angle in np.linspace(0, 2 * np.pi, 8):
            points.append([
                left_hand_x + fist_size * np.cos(angle),
                left_hand_y + fist_size * 0.8 * np.sin(angle)
            ])

        # Right arm
        right_arm_angle = np.radians(self._pose.right_arm)
        right_elbow_x = shoulder_width / 2 + arm_length * 0.45 * np.cos(right_arm_angle)
        right_elbow_y = arm_y - arm_length * 0.45 * np.sin(right_arm_angle)
        right_hand_x = shoulder_width / 2 + arm_length * np.cos(right_arm_angle)
        right_hand_y = arm_y - arm_length * np.sin(right_arm_angle)

        points.append([shoulder_width / 2, arm_y])  # Shoulder
        points.append([right_elbow_x, right_elbow_y])  # Elbow
        points.append([right_hand_x, right_hand_y])  # Hand
        # Fist/hand
        for angle in np.linspace(0, 2 * np.pi, 8):
            points.append([
                right_hand_x + fist_size * np.cos(angle),
                right_hand_y + fist_size * 0.8 * np.sin(angle)
            ])

        # Legs - strong with defined thighs
        leg_gap = hip_width * 0.35

        # Left leg
        left_leg_angle = np.radians(90 + self._pose.left_leg)
        left_knee_x = -leg_gap - leg_length * 0.48 * np.cos(left_leg_angle)
        left_knee_y = hip_y - leg_length * 0.48 * np.sin(left_leg_angle)
        left_foot_x = -leg_gap - leg_length * np.cos(left_leg_angle)
        left_foot_y = hip_y - leg_length * np.sin(left_leg_angle)

        points.append([-leg_gap, hip_y])  # Hip
        points.append([left_knee_x, left_knee_y])  # Knee
        points.append([left_foot_x, left_foot_y])  # Foot
        # Boot/foot shape
        for angle in np.linspace(0, 2 * np.pi, 8):
            points.append([
                left_foot_x + leg_width * 1.5 * np.cos(angle),
                left_foot_y + leg_width * 0.8 * np.sin(angle)
            ])

        # Right leg
        right_leg_angle = np.radians(90 + self._pose.right_leg)
        right_knee_x = leg_gap + leg_length * 0.48 * np.cos(right_leg_angle)
        right_knee_y = hip_y - leg_length * 0.48 * np.sin(right_leg_angle)
        right_foot_x = leg_gap + leg_length * np.cos(right_leg_angle)
        right_foot_y = hip_y - leg_length * np.sin(right_leg_angle)

        points.append([leg_gap, hip_y])  # Hip
        points.append([right_knee_x, right_knee_y])  # Knee
        points.append([right_foot_x, right_foot_y])  # Foot
        # Boot/foot shape
        for angle in np.linspace(0, 2 * np.pi, 8):
            points.append([
                right_foot_x + leg_width * 1.5 * np.cos(angle),
                right_foot_y + leg_width * 0.8 * np.sin(angle)
            ])

        # Cape points (if enabled) - 6 points for flowing cape shape
        if self.cape:
            cape_attach_left = -shoulder_width / 2 + h * 0.02
            cape_attach_right = shoulder_width / 2 - h * 0.02
            cape_bottom = hip_y - h * 0.15  # Cape extends below hips
            cape_mid = (shoulder_y + cape_bottom) / 2
            cape_width = shoulder_width * 1.2

            # Cape flows outward slightly
            points.append([cape_attach_left, shoulder_y])  # Left attach
            points.append([-cape_width / 2, cape_mid])  # Left flow
            points.append([-cape_width / 2 * 0.8, cape_bottom])  # Left bottom
            points.append([cape_width / 2 * 0.8, cape_bottom])  # Right bottom
            points.append([cape_width / 2, cape_mid])  # Right flow
            points.append([cape_attach_right, shoulder_y])  # Right attach

        self._points = np.array(points, dtype=np.float64)

        if self.facing == "left":
            self._points[:, 0] *= -1

    def get_render_data(self) -> dict[str, Any]:
        """Get data for rendering."""
        data = super().get_render_data()
        # Add superhero-specific render info
        data["costume_primary"] = self.costume_primary
        data["costume_secondary"] = self.costume_secondary
        data["skin_color"] = self.skin_color
        data["cape"] = self.cape
        data["cape_color"] = self.cape_color
        data["mask"] = self.mask
        data["emblem"] = self.emblem
        data["emblem_color"] = self.emblem_color
        data["boots"] = self.boots
        data["gloves"] = self.gloves
        data["head_height_ratio"] = 0.12
        data["head_width_ratio"] = 0.09
        data["shoulder_width_ratio"] = 0.28
        data["waist_width_ratio"] = 0.14
        data["body_height_ratio"] = 0.32
        data["arm_length_ratio"] = 0.26
        data["leg_length_ratio"] = 0.34
        return data
