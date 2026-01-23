"""Character - Comic character classes."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Self

import numpy as np

from comix.cobject.cobject import CObject

if TYPE_CHECKING:
    from comix.cobject.bubble.bubble import Bubble

logger = logging.getLogger(__name__)


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
        """Create expression from preset name.

        If the name is not found in presets, logs a warning and returns
        the default neutral expression.
        """
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
        if name not in presets:
            logger.warning(
                "Unknown expression '%s', falling back to 'neutral'. "
                "Valid expressions: %s",
                name,
                ", ".join(sorted(presets.keys())),
            )
            return cls()
        return presets[name]


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
        """Create pose from preset name.

        If the name is not found in presets, logs a warning and returns
        the default standing pose.
        """
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
        if name not in presets:
            logger.warning(
                "Unknown pose '%s', falling back to 'standing'. "
                "Valid poses: %s",
                name,
                ", ".join(sorted(presets.keys())),
            )
            return cls()
        return presets[name]


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

        # Validate height parameter
        if height <= 0:
            raise ValueError(f"Character height must be positive, got: {height}")

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
                "character_style": self.style,  # Changed from "style" to "character_style"
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


class ArmController:
    """Helper class for arm control via preset poses.

    Accessed via char.left_arm or char.right_arm for convenient preset application.

    Example:
        >>> char = Stickman(height=150)
        >>> char.left_arm.set_preset("waving")
        >>> char.right_arm.set_preset("pointing")
    """

    ARM_PRESETS: dict[str, dict[str, float | str]] = {
        "down": {"shoulder": 0, "elbow": 0},
        "forward": {"shoulder": 90, "elbow": 0},
        "up": {"shoulder": 180, "elbow": 0},
        "waving": {"shoulder": 180, "elbow": 30},
        "pointing": {"shoulder": 90, "elbow": 0, "hand": "point"},
        "relaxed": {"shoulder": 0, "elbow": 15},
        "thinking": {"shoulder": 120, "elbow": 90, "hand": "fist"},
        "raised": {"shoulder": 135, "elbow": 45},
        "back": {"shoulder": 270, "elbow": 0},
    }

    def __init__(self, character: "Stickman", side: str) -> None:
        self._character = character
        self._side = side

    def set_preset(self, preset: str) -> "Stickman":
        """Apply preset arm pose.

        Args:
            preset: One of "down", "forward", "up", "waving", "pointing",
                    "relaxed", "thinking", "raised", "back"

        Returns:
            The parent Stickman for method chaining.
        """
        if preset not in self.ARM_PRESETS:
            raise ValueError(
                f"Unknown arm preset: {preset}. "
                f"Valid presets: {', '.join(sorted(self.ARM_PRESETS.keys()))}"
            )

        config = self.ARM_PRESETS[preset]

        shoulder_angle = float(config["shoulder"])
        elbow_angle = float(config.get("elbow", 0))
        hand_gesture = str(config["hand"]) if "hand" in config else None

        if self._side == "left":
            self._character.set_arm_angles(
                left_shoulder=shoulder_angle,
                left_elbow=elbow_angle
            )
            if hand_gesture is not None:
                self._character.set_hands(left=hand_gesture)
        else:
            self._character.set_arm_angles(
                right_shoulder=shoulder_angle,
                right_elbow=elbow_angle
            )
            if hand_gesture is not None:
                self._character.set_hands(right=hand_gesture)

        return self._character


class LegController:
    """Helper class for leg control via preset poses.

    Accessed via char.left_leg_ctrl or char.right_leg_ctrl for convenient preset application.

    Example:
        >>> char = Stickman(height=150)
        >>> char.left_leg_ctrl.set_preset("walking")
        >>> char.right_leg_ctrl.set_preset("standing")
    """

    LEG_PRESETS: dict[str, dict[str, float]] = {
        "standing": {"hip": 0, "knee": 0},
        "walking": {"hip": 30, "knee": 15},
        "walking_back": {"hip": -20, "knee": 10},
        "sitting": {"hip": 90, "knee": 90},
        "kneeling": {"hip": 135, "knee": 135},
        "bent": {"hip": 0, "knee": 45},
        "high_kick": {"hip": 90, "knee": 0},
        "running": {"hip": 45, "knee": 45},
    }

    def __init__(self, character: "Stickman", side: str) -> None:
        self._character = character
        self._side = side

    def set_preset(self, preset: str) -> "Stickman":
        """Apply preset leg pose.

        Args:
            preset: One of "standing", "walking", "walking_back", "sitting",
                    "kneeling", "bent", "high_kick", "running"

        Returns:
            The parent Stickman for method chaining.
        """
        if preset not in self.LEG_PRESETS:
            raise ValueError(
                f"Unknown leg preset: {preset}. "
                f"Valid presets: {', '.join(sorted(self.LEG_PRESETS.keys()))}"
            )

        config = self.LEG_PRESETS[preset]

        if self._side == "left":
            self._character.set_leg_angles(
                left_hip=config["hip"],
                left_knee=config.get("knee", 0)
            )
        else:
            self._character.set_leg_angles(
                right_hip=config["hip"],
                right_knee=config.get("knee", 0)
            )

        return self._character


class Stickman(Character):
    """Simple stick figure character with reference-based proportions and joint articulation.

    Proportions are based on professional stick figure standards (xkcd, etc.)
    with configurable presets for different styles:

    - "classic": Standard ~7.5 head heights for adults
    - "xkcd": Minimalist style with slightly smaller head
    - "tall": Tall/elongated proportions (~8 head heights)
    - "realistic": Realistic/heroic proportions (8 heads, ideal figure drawing)
    - "child": Larger head ratio (~4 head heights)

    Joint Articulation:
        Stickman supports detailed joint-level control for creating custom poses:

        - Shoulder angles: 0° = down, 90° = forward, 180° = up, 270° = back
        - Elbow angles: 0° = straight, 90° = right angle, 180° = fully bent
        - Hip angles: 0° = standing, 45° = walking forward, 90° = sitting
        - Knee angles: 0° = straight, 90° = sitting bend, 180° = fully bent

        Hand gestures: "none", "fist", "open", "point", "peace", "thumbs_up", "relaxed"

    Args:
        name: Character name.
        proportion_style: Preset proportion style ("classic", "xkcd", "tall", "realistic", "child").
        head_ratio: Override head size as ratio of total height (0.0-1.0).
        torso_ratio: Override torso length as ratio of total height.
        arm_ratio: Override arm length as ratio of total height.
        leg_ratio: Override leg length as ratio of total height.
        head_squash: Head shape modifier (-1.0 to 1.0). Positive values flatten
            the head (wider than tall), negative values elongate it (taller than
            wide). Default 0.0 creates a perfect circle.
        **kwargs: Additional Character parameters.

    Example:
        >>> # Default classic proportions
        >>> char = Stickman(height=150)
        >>>
        >>> # xkcd-style minimalist
        >>> char = Stickman(height=150, proportion_style="xkcd")
        >>>
        >>> # Custom proportions
        >>> char = Stickman(height=150, head_ratio=0.2, leg_ratio=0.45)
        >>>
        >>> # Slightly flattened head for cute look
        >>> char = Stickman(height=150, head_squash=0.15)
        >>>
        >>> # Joint-level articulation
        >>> char = Stickman(height=150)
        >>> char.set_arm_angles(left_shoulder=90, left_elbow=45)
        >>> char.set_hands(left="point", right="fist")
        >>>
        >>> # Point at a target
        >>> char.point_at((500, 200), arm="right")
    """

    # Valid hand gesture options
    HAND_GESTURES: list[str] = ["none", "fist", "open", "point", "peace", "thumbs_up", "relaxed"]

    # Reference-based proportion presets
    PROPORTION_PRESETS: dict[str, dict[str, float]] = {
        "classic": {
            "head_ratio": 0.133,  # ~7.5 heads (100/7.5)
            "torso_ratio": 0.40,  # ~3 heads
            "arm_ratio": 0.38,    # Arms reach mid-thigh
            "leg_ratio": 0.53,    # ~4 heads
        },
        "xkcd": {
            "head_ratio": 0.12,   # Slightly smaller head
            "torso_ratio": 0.42,
            "arm_ratio": 0.40,
            "leg_ratio": 0.54,
        },
        "tall": {
            "head_ratio": 0.125,  # 8 heads
            "torso_ratio": 0.42,
            "arm_ratio": 0.40,
            "leg_ratio": 0.55,
        },
        "realistic": {
            "head_ratio": 0.125,  # 8 heads (ideal figure drawing proportions)
            "torso_ratio": 0.375,  # 3 heads for torso (more balanced)
            "arm_ratio": 0.375,   # Arms slightly shorter than tall style
            "leg_ratio": 0.50,    # 4 heads for legs (equal to half body)
        },
        "child": {
            "head_ratio": 0.25,   # 4 heads (larger head)
            "torso_ratio": 0.30,
            "arm_ratio": 0.28,
            "leg_ratio": 0.45,
        },
    }

    # Reference height for line width scaling (100px is the baseline)
    REFERENCE_HEIGHT: float = 100.0
    # Default line width at reference height
    DEFAULT_LINE_WIDTH: float = 2.0
    # Minimum line width regardless of scaling
    MIN_LINE_WIDTH: float = 0.5
    # Maximum line width regardless of scaling
    MAX_LINE_WIDTH: float = 6.0

    def __init__(
        self,
        name: str = "Stickman",
        proportion_style: str = "classic",
        head_ratio: float | None = None,
        torso_ratio: float | None = None,
        arm_ratio: float | None = None,
        leg_ratio: float | None = None,
        head_squash: float = 0.0,
        line_width: float | None = None,
        auto_line_width: bool = True,
        **kwargs: Any,
    ) -> None:
        # Get preset proportions
        if proportion_style not in self.PROPORTION_PRESETS:
            logger.warning(
                "Unknown proportion_style '%s', falling back to 'classic'. "
                "Valid styles: %s",
                proportion_style,
                ", ".join(sorted(self.PROPORTION_PRESETS.keys())),
            )
            proportion_style = "classic"

        preset = self.PROPORTION_PRESETS[proportion_style]

        # Use custom ratios if provided, otherwise use preset
        self.proportion_style = proportion_style
        self.head_ratio = head_ratio if head_ratio is not None else preset["head_ratio"]
        self.torso_ratio = torso_ratio if torso_ratio is not None else preset["torso_ratio"]
        self.arm_ratio = arm_ratio if arm_ratio is not None else preset["arm_ratio"]
        self.leg_ratio = leg_ratio if leg_ratio is not None else preset["leg_ratio"]

        # Clamp head_squash to valid range (-1.0 to 1.0)
        self.head_squash = max(-1.0, min(1.0, head_squash))

        # Line width configuration
        self.auto_line_width = auto_line_width
        self._explicit_line_width = line_width  # Store explicit value (may be None)

        # Joint angle articulation system
        # Shoulder angles: 0° = down, 90° = forward, 180° = up, 270° = back
        self._left_shoulder_angle: float = 0.0
        self._left_elbow_angle: float = 0.0
        self._right_shoulder_angle: float = 0.0
        self._right_elbow_angle: float = 0.0

        # Hip angles: 0° = standing, positive = forward, negative = back
        # Knee angles: 0° = straight, positive = bent
        self._left_hip_angle: float = 0.0
        self._left_knee_angle: float = 0.0
        self._right_hip_angle: float = 0.0
        self._right_knee_angle: float = 0.0

        # Hand gesture options: "none", "fist", "open", "point", "peace", "thumbs_up", "relaxed"
        self._left_hand: str = "none"
        self._right_hand: str = "none"

        # Track whether articulation system is being used
        self._use_articulation: bool = False

        # Curve settings for natural limb appearance
        self._auto_curve: bool = False  # Automatically add curves based on pose
        self._auto_curve_strength: float = 0.0  # Strength of auto curves
        self._left_upper_arm_curve: float = 0.0
        self._left_forearm_curve: float = 0.0
        self._right_upper_arm_curve: float = 0.0
        self._right_forearm_curve: float = 0.0
        self._left_upper_leg_curve: float = 0.0
        self._left_lower_leg_curve: float = 0.0
        self._right_upper_leg_curve: float = 0.0
        self._right_lower_leg_curve: float = 0.0
        self._spine_curve: float = 0.0

        # Arm and leg controllers for preset convenience
        self.left_arm = ArmController(self, "left")
        self.right_arm = ArmController(self, "right")
        self.left_leg_ctrl = LegController(self, "left")
        self.right_leg_ctrl = LegController(self, "right")

        kwargs.setdefault("style", "stickman")
        super().__init__(name=name, **kwargs)

    # Articulation methods for joint-level control

    @staticmethod
    def _normalize_angle(angle: float) -> float:
        """Normalize angle to 0-360 range."""
        while angle < 0:
            angle += 360
        while angle >= 360:
            angle -= 360
        return angle

    @staticmethod
    def _clamp_elbow(angle: float) -> float:
        """Clamp elbow bend to physically possible range (0-180)."""
        return max(0, min(180, angle))

    @staticmethod
    def _clamp_knee(angle: float) -> float:
        """Clamp knee bend to physically possible range (0-180)."""
        return max(0, min(180, angle))

    def set_arm_angles(
        self,
        left_shoulder: float | None = None,
        left_elbow: float | None = None,
        right_shoulder: float | None = None,
        right_elbow: float | None = None,
    ) -> Self:
        """Set arm joint angles in degrees.

        Shoulder angles are measured from the resting position:
        - 0° = arm hanging straight down (resting position)
        - 90° = arm extending forward/horizontally
        - 180° = arm raised straight up
        - 270° = arm extending backward

        Elbow angles represent bend amount:
        - 0° = straight arm (no bend)
        - 90° = right angle bend
        - 180° = fully bent (hand touches shoulder)

        Args:
            left_shoulder: Left arm shoulder angle in degrees (0-360).
            left_elbow: Left arm elbow bend angle in degrees (0-180).
            right_shoulder: Right arm shoulder angle in degrees (0-360).
            right_elbow: Right arm elbow bend angle in degrees (0-180).

        Returns:
            Self for method chaining.

        Example:
            >>> char = Stickman(height=150)
            >>> char.set_arm_angles(left_shoulder=90, left_elbow=45)
            >>> char.set_arm_angles(right_shoulder=180, right_elbow=30)
        """
        if left_shoulder is not None:
            self._left_shoulder_angle = self._normalize_angle(left_shoulder)
            self._use_articulation = True
        if left_elbow is not None:
            self._left_elbow_angle = self._clamp_elbow(left_elbow)
            self._use_articulation = True
        if right_shoulder is not None:
            self._right_shoulder_angle = self._normalize_angle(right_shoulder)
            self._use_articulation = True
        if right_elbow is not None:
            self._right_elbow_angle = self._clamp_elbow(right_elbow)
            self._use_articulation = True

        self.generate_points()
        return self

    def set_leg_angles(
        self,
        left_hip: float | None = None,
        left_knee: float | None = None,
        right_hip: float | None = None,
        right_knee: float | None = None,
    ) -> Self:
        """Set leg joint angles in degrees.

        Hip angles are measured from the standing position:
        - 0° = leg hanging straight down (standing position)
        - 45° = leg extended forward (walking)
        - 90° = leg extended horizontally (sitting or high kick)
        - -45° = leg extended backward (walking backward)

        Knee angles represent bend amount:
        - 0° = straight leg (standing, no bend)
        - 90° = sitting position bend
        - 180° = fully bent (heel touches buttocks)

        Args:
            left_hip: Left leg hip angle in degrees.
            left_knee: Left leg knee bend angle in degrees (0-180).
            right_hip: Right leg hip angle in degrees.
            right_knee: Right leg knee bend angle in degrees (0-180).

        Returns:
            Self for method chaining.

        Example:
            >>> char = Stickman(height=150)
            >>> char.set_leg_angles(left_hip=30, left_knee=15)  # Walking
            >>> char.set_leg_angles(right_hip=90, right_knee=90)  # Sitting
        """
        if left_hip is not None:
            self._left_hip_angle = left_hip
            self._use_articulation = True
        if left_knee is not None:
            self._left_knee_angle = self._clamp_knee(left_knee)
            self._use_articulation = True
        if right_hip is not None:
            self._right_hip_angle = right_hip
            self._use_articulation = True
        if right_knee is not None:
            self._right_knee_angle = self._clamp_knee(right_knee)
            self._use_articulation = True

        self.generate_points()
        return self

    def set_hands(
        self,
        left: str | None = None,
        right: str | None = None,
    ) -> Self:
        """Set hand gesture options.

        Hand gestures add visual detail to the hand endpoint:
        - "none": Hand is just the endpoint of arm line (default stick figure)
        - "fist": Small circle at hand position (closed hand)
        - "open": 5 short radiating lines from hand position (fingers spread)
        - "point": Single extended line (index finger pointing)
        - "peace": Two short lines (peace sign / victory)
        - "thumbs_up": Vertical line with small perpendicular line
        - "relaxed": 3-4 short parallel lines (relaxed fingers)

        Args:
            left: Left hand gesture option.
            right: Right hand gesture option.

        Returns:
            Self for method chaining.

        Raises:
            ValueError: If an invalid hand gesture option is provided.

        Example:
            >>> char = Stickman(height=150)
            >>> char.set_hands(left="open", right="point")
        """
        if left is not None:
            if left not in self.HAND_GESTURES:
                raise ValueError(
                    f"Invalid hand option: {left}. "
                    f"Must be one of {self.HAND_GESTURES}"
                )
            self._left_hand = left
            self._use_articulation = True
        if right is not None:
            if right not in self.HAND_GESTURES:
                raise ValueError(
                    f"Invalid hand option: {right}. "
                    f"Must be one of {self.HAND_GESTURES}"
                )
            self._right_hand = right
            self._use_articulation = True

        self.generate_points()
        return self

    def set_limb_curves(
        self,
        left_upper_arm: float | None = None,
        left_forearm: float | None = None,
        right_upper_arm: float | None = None,
        right_forearm: float | None = None,
        left_upper_leg: float | None = None,
        left_lower_leg: float | None = None,
        right_upper_leg: float | None = None,
        right_lower_leg: float | None = None,
        spine: float | None = None,
    ) -> Self:
        """Set manual curve amounts for limbs and spine.

        Curves add natural organic appearance to limbs. Positive values curve
        outward, negative values curve inward.

        Args:
            left_upper_arm: Curve amount for left upper arm (0.0-0.3 typical).
            left_forearm: Curve amount for left forearm (0.0-0.3 typical).
            right_upper_arm: Curve amount for right upper arm (0.0-0.3 typical).
            right_forearm: Curve amount for right forearm (0.0-0.3 typical).
            left_upper_leg: Curve amount for left upper leg (0.0-0.3 typical).
            left_lower_leg: Curve amount for left lower leg (0.0-0.3 typical).
            right_upper_leg: Curve amount for right upper leg (0.0-0.3 typical).
            right_lower_leg: Curve amount for right lower leg (0.0-0.3 typical).
            spine: Curve amount for spine/torso (0.0-0.3 typical).

        Returns:
            Self for method chaining.

        Example:
            >>> char = Stickman(height=150)
            >>> # Slight natural curve
            >>> char.set_limb_curves(right_upper_arm=0.1, right_forearm=0.1)
            >>> # Bent spine
            >>> char.set_limb_curves(spine=0.2)
        """
        if left_upper_arm is not None:
            self._left_upper_arm_curve = left_upper_arm
        if left_forearm is not None:
            self._left_forearm_curve = left_forearm
        if right_upper_arm is not None:
            self._right_upper_arm_curve = right_upper_arm
        if right_forearm is not None:
            self._right_forearm_curve = right_forearm
        if left_upper_leg is not None:
            self._left_upper_leg_curve = left_upper_leg
        if left_lower_leg is not None:
            self._left_lower_leg_curve = left_lower_leg
        if right_upper_leg is not None:
            self._right_upper_leg_curve = right_upper_leg
        if right_lower_leg is not None:
            self._right_lower_leg_curve = right_lower_leg
        if spine is not None:
            self._spine_curve = spine

        self.generate_points()
        return self

    def enable_auto_curves(self, enabled: bool = True, strength: float = 0.15) -> Self:
        """Enable automatic natural curves based on limb angles.

        When enabled, limbs will automatically curve based on their position
        to create a more organic, cartoon-like appearance.

        Args:
            enabled: Whether to enable auto curves.
            strength: Overall strength of auto curves (0.0-0.3 typical).

        Returns:
            Self for method chaining.

        Example:
            >>> char = Stickman(height=150)
            >>> char.enable_auto_curves(True, strength=0.15)
            >>> char.set_arm_angles(left_shoulder=135, right_shoulder=45)
        """
        self._auto_curve = enabled
        self._auto_curve_strength = strength if enabled else 0.0
        self.generate_points()
        return self

    def point_at(
        self,
        target: CObject | tuple[float, float],
        arm: str = "right",
        hand: str = "point",
        elbow_bend: float = 0.0,
    ) -> Self:
        """Automatically calculate arm angles to point at a target.

        This helper method calculates the shoulder angle needed for the
        specified arm to point at the target position.

        Args:
            target: Object to point at, or (x, y) coordinates.
            arm: Which arm to use - "left" or "right".
            hand: Hand gesture to use (default: "point").
            elbow_bend: Amount of elbow bend in degrees (0 = straight arm).

        Returns:
            Self for method chaining.

        Example:
            >>> char = Stickman(height=150)
            >>> char.move_to((100, 200))
            >>> char.point_at((500, 150), arm="right", hand="point")
        """
        # Get target position
        if isinstance(target, tuple):
            target_x, target_y = target
        else:
            center = target.get_center()
            target_x, target_y = center[0], center[1]

        # Get shoulder position (approximate based on character position)
        char_center = self.get_center()
        shoulder_y = char_center[1] - self.character_height * 0.5 + self.character_height * self.head_ratio * 2 + self.character_height * self.torso_ratio * 0.1

        # For left arm, shoulder is slightly to the left; for right, slightly right
        if arm == "left":
            shoulder_x = char_center[0] - 2  # Small offset
        else:
            shoulder_x = char_center[0] + 2

        # Calculate angle from shoulder to target
        dx = target_x - shoulder_x
        dy = target_y - shoulder_y

        # In graphics coordinates, Y increases downward
        # arctan2(dy, dx) gives angle from positive X axis
        angle_rad = np.arctan2(dy, dx)
        angle_deg = np.degrees(angle_rad)

        # Convert to our convention (0° = down, 90° = forward)
        # Our shoulder angle: 0° = down, 90° = forward (right), 180° = up
        # Standard math: 0° = right, 90° = down (in graphics coords)
        # So we need to map: target_angle -> our_convention
        # If dx > 0, dy > 0 (target is down-right): arctan2 gives positive angle
        # We want ~45° to point down-right

        # For right arm: arm extends in direction of angle
        # For left arm: need to mirror
        if arm == "left":
            # Mirror the angle for left arm
            shoulder_angle = 180 - angle_deg
        else:
            shoulder_angle = angle_deg

        # Normalize the angle
        shoulder_angle = self._normalize_angle(shoulder_angle)

        # Set arm angles and hand gesture
        if arm == "left":
            self.set_arm_angles(left_shoulder=shoulder_angle, left_elbow=elbow_bend)
            self.set_hands(left=hand)
        else:
            self.set_arm_angles(right_shoulder=shoulder_angle, right_elbow=elbow_bend)
            self.set_hands(right=hand)

        return self

    def _get_shoulder_position(self, arm: str) -> tuple[float, float]:
        """Get the shoulder position for the specified arm.

        Used internally for point_at calculations.

        Args:
            arm: "left" or "right"

        Returns:
            (x, y) coordinates of the shoulder.
        """
        center = self.get_center()
        h = self.character_height
        head_radius = h * self.head_ratio
        torso_length = h * self.torso_ratio

        # Shoulder is at neck + 10% into torso
        head_top = center[1] - h / 2
        neck_y = head_top + 2 * head_radius
        shoulder_y = neck_y + torso_length * 0.1

        return (center[0], shoulder_y)

    def _generate_hand_gesture(
        self,
        hand_x: float,
        hand_y: float,
        arm_angle: float,
        gesture: str,
    ) -> list[list[float]]:
        """Generate geometry points for hand gesture.

        Args:
            hand_x: X coordinate of hand position.
            hand_y: Y coordinate of hand position.
            arm_angle: Direction the arm is pointing in radians.
            gesture: One of HAND_GESTURES.

        Returns:
            List of [x, y] point pairs for drawing gesture lines.
        """
        points: list[list[float]] = []
        finger_length = self.character_height * 0.05

        if gesture == "fist":
            # Small circle at hand position (8 points)
            radius = finger_length * 0.5
            for angle in np.linspace(0, 2 * np.pi, 8, endpoint=False):
                points.append([
                    hand_x + radius * np.cos(angle),
                    hand_y + radius * np.sin(angle)
                ])

        elif gesture == "open":
            # 5 radiating lines (spread fingers)
            for finger_offset in [-40, -20, 0, 20, 40]:
                angle = arm_angle + np.radians(finger_offset)
                points.append([hand_x, hand_y])
                points.append([
                    hand_x + finger_length * np.cos(angle),
                    hand_y + finger_length * np.sin(angle)
                ])

        elif gesture == "point":
            # Single extended line (index finger)
            points.append([hand_x, hand_y])
            points.append([
                hand_x + finger_length * 1.5 * np.cos(arm_angle),
                hand_y + finger_length * 1.5 * np.sin(arm_angle)
            ])

        elif gesture == "peace":
            # Two lines (V sign)
            for finger_offset in [-15, 15]:
                angle = arm_angle + np.radians(finger_offset)
                points.append([hand_x, hand_y])
                points.append([
                    hand_x + finger_length * np.cos(angle),
                    hand_y + finger_length * np.sin(angle)
                ])

        elif gesture == "thumbs_up":
            # Vertical line with perpendicular thumb
            # Thumb goes up (perpendicular to arm direction)
            perp_angle = arm_angle - np.pi / 2  # 90° counterclockwise
            points.append([hand_x, hand_y])
            points.append([
                hand_x + finger_length * np.cos(perp_angle),
                hand_y + finger_length * np.sin(perp_angle)
            ])
            # Small fist base
            for angle in np.linspace(0, 2 * np.pi, 6, endpoint=False):
                radius = finger_length * 0.3
                points.append([
                    hand_x + radius * np.cos(angle),
                    hand_y + radius * np.sin(angle)
                ])

        elif gesture == "relaxed":
            # 3-4 parallel short lines (relaxed fingers)
            perp_angle = arm_angle + np.pi / 2
            for i in range(4):
                offset = (i - 1.5) * finger_length * 0.25
                base_x = hand_x + offset * np.cos(perp_angle)
                base_y = hand_y + offset * np.sin(perp_angle)
                points.append([base_x, base_y])
                points.append([
                    base_x + finger_length * 0.6 * np.cos(arm_angle),
                    base_y + finger_length * 0.6 * np.sin(arm_angle)
                ])

        return points

    def generate_points(self) -> None:
        """Generate stickman figure points with reference-based proportions.

        If articulation mode is active (set_arm_angles/set_leg_angles called),
        uses the joint angle system for precise limb positioning. Otherwise,
        falls back to the pose-based system for backward compatibility.
        """
        h = self.character_height

        # Calculate component sizes from ratios
        head_radius = h * self.head_ratio
        torso_length = h * self.torso_ratio
        arm_length = h * self.arm_ratio
        leg_length = h * self.leg_ratio

        # Upper and lower segment lengths
        upper_arm_length = arm_length * 0.5
        forearm_length = arm_length * 0.5
        upper_leg_length = leg_length * 0.5
        lower_leg_length = leg_length * 0.5

        points: list[list[float]] = []

        # Calculate vertical positions (top to bottom)
        # In graphics coordinates, Y increases downward
        head_top = -h / 2
        head_center_y = head_top + head_radius
        neck_y = head_top + 2 * head_radius
        hip_y = neck_y + torso_length

        # Head ellipse (16 points) - uses head_squash to modify shape
        squash_factor = 1.0 + abs(self.head_squash) * 0.3
        if self.head_squash >= 0:
            head_radius_x = head_radius * squash_factor
            head_radius_y = head_radius / squash_factor
        else:
            head_radius_x = head_radius / squash_factor
            head_radius_y = head_radius * squash_factor

        for angle in np.linspace(0, 2 * np.pi, 16):
            points.append([
                head_radius_x * np.cos(angle),
                head_center_y + head_radius_y * np.sin(angle)
            ])

        # Torso line (neck to hips) with optional curve
        from comix.utils.sketchy import create_curved_segment
        spine_curve = self._spine_curve
        if self._auto_curve and spine_curve == 0.0:
            # Auto curve based on overall posture
            spine_curve = 0.0  # Default no auto curve for spine

        if abs(spine_curve) > 0.001:
            spine_pts = create_curved_segment(
                (0, neck_y),
                (0, hip_y),
                curve_amount=spine_curve,
                num_points=6
            )
            for pt in spine_pts:
                points.append([pt[0], pt[1]])
        else:
            points.append([0, neck_y])
            points.append([0, hip_y])

        # Arm attachment point
        arm_y = neck_y + torso_length * 0.1

        # Store hand positions for gesture rendering
        left_hand_pos: tuple[float, float] = (0, 0)
        right_hand_pos: tuple[float, float] = (0, 0)
        left_arm_angle_rad: float = 0
        right_arm_angle_rad: float = 0

        if self._use_articulation:
            # Use articulation system with independent joint angles

            # Left arm with shoulder and elbow angles
            left_shoulder_rad = np.radians(self._left_shoulder_angle)
            left_elbow_rad = np.radians(self._left_elbow_angle)

            # Upper arm direction (from shoulder)
            # 0° = down, so we add 90° to convert to standard coords
            upper_left_angle = left_shoulder_rad - np.pi / 2

            # Elbow position
            elbow_left_x = -upper_arm_length * np.cos(upper_left_angle)
            elbow_left_y = arm_y - upper_arm_length * np.sin(upper_left_angle)

            # Forearm bends from the upper arm direction
            # Elbow bend is relative to upper arm (0° = straight continuation)
            # For left arm, positive elbow bend curves toward body
            forearm_left_angle = upper_left_angle - left_elbow_rad

            # Hand position
            hand_left_x = elbow_left_x - forearm_length * np.cos(forearm_left_angle)
            hand_left_y = elbow_left_y - forearm_length * np.sin(forearm_left_angle)

            # Calculate curve amounts (auto or manual)
            left_upper_curve = self._left_upper_arm_curve
            left_fore_curve = self._left_forearm_curve
            if self._auto_curve and (left_upper_curve == 0.0 or left_fore_curve == 0.0):
                # Auto curve based on shoulder angle
                # More extreme angles get more curve
                angle_factor = abs(np.sin(upper_left_angle)) * self._auto_curve_strength
                if left_upper_curve == 0.0:
                    left_upper_curve = angle_factor
                if left_fore_curve == 0.0:
                    left_fore_curve = angle_factor * 0.7

            # Generate curved segments
            from comix.utils.sketchy import create_curved_segment
            upper_arm_pts = create_curved_segment(
                (0, arm_y),
                (elbow_left_x, elbow_left_y),
                curve_amount=left_upper_curve,
                num_points=8
            )
            for pt in upper_arm_pts:
                points.append([pt[0], pt[1]])

            forearm_pts = create_curved_segment(
                (elbow_left_x, elbow_left_y),
                (hand_left_x, hand_left_y),
                curve_amount=left_fore_curve,
                num_points=8
            )
            for pt in forearm_pts[1:]:  # Skip first to avoid duplicate
                points.append([pt[0], pt[1]])

            left_hand_pos = (hand_left_x, hand_left_y)
            left_arm_angle_rad = forearm_left_angle

            # Right arm with shoulder and elbow angles
            right_shoulder_rad = np.radians(self._right_shoulder_angle)
            right_elbow_rad = np.radians(self._right_elbow_angle)

            # Upper arm direction
            upper_right_angle = right_shoulder_rad - np.pi / 2

            # Elbow position
            elbow_right_x = upper_arm_length * np.cos(upper_right_angle)
            elbow_right_y = arm_y - upper_arm_length * np.sin(upper_right_angle)

            # Forearm with elbow bend (for right arm, positive curves away from body)
            forearm_right_angle = upper_right_angle + right_elbow_rad

            # Hand position
            hand_right_x = elbow_right_x + forearm_length * np.cos(forearm_right_angle)
            hand_right_y = elbow_right_y - forearm_length * np.sin(forearm_right_angle)

            # Calculate curve amounts (auto or manual)
            right_upper_curve = self._right_upper_arm_curve
            right_fore_curve = self._right_forearm_curve
            if self._auto_curve and (right_upper_curve == 0.0 or right_fore_curve == 0.0):
                angle_factor = abs(np.sin(upper_right_angle)) * self._auto_curve_strength
                if right_upper_curve == 0.0:
                    right_upper_curve = -angle_factor  # Negative for right side
                if right_fore_curve == 0.0:
                    right_fore_curve = -angle_factor * 0.7

            # Generate curved segments
            upper_arm_pts = create_curved_segment(
                (0, arm_y),
                (elbow_right_x, elbow_right_y),
                curve_amount=right_upper_curve,
                num_points=8
            )
            for pt in upper_arm_pts:
                points.append([pt[0], pt[1]])

            forearm_pts = create_curved_segment(
                (elbow_right_x, elbow_right_y),
                (hand_right_x, hand_right_y),
                curve_amount=right_fore_curve,
                num_points=8
            )
            for pt in forearm_pts[1:]:
                points.append([pt[0], pt[1]])

            right_hand_pos = (hand_right_x, hand_right_y)
            right_arm_angle_rad = forearm_right_angle

            # Left leg with hip and knee angles
            left_hip_rad = np.radians(self._left_hip_angle)
            left_knee_rad = np.radians(self._left_knee_angle)

            # Upper leg direction (0° = down, so straight down means angle = pi/2 in standard)
            # Hip angle: 0 = down, positive = forward
            upper_left_leg_angle = np.pi / 2 + left_hip_rad

            # Knee position
            knee_left_x = -upper_leg_length * np.cos(upper_left_leg_angle)
            knee_left_y = hip_y + upper_leg_length * np.sin(upper_left_leg_angle)

            # Lower leg bends from upper leg direction
            lower_left_leg_angle = upper_left_leg_angle + left_knee_rad

            # Foot position
            foot_left_x = knee_left_x - lower_leg_length * np.cos(lower_left_leg_angle)
            foot_left_y = knee_left_y + lower_leg_length * np.sin(lower_left_leg_angle)

            # Calculate curve amounts (auto or manual)
            left_upper_leg_curve = self._left_upper_leg_curve
            left_lower_leg_curve = self._left_lower_leg_curve
            if self._auto_curve and (left_upper_leg_curve == 0.0 or left_lower_leg_curve == 0.0):
                angle_factor = abs(np.sin(upper_left_leg_angle - np.pi/2)) * self._auto_curve_strength
                if left_upper_leg_curve == 0.0:
                    left_upper_leg_curve = angle_factor * 0.6
                if left_lower_leg_curve == 0.0:
                    left_lower_leg_curve = angle_factor * 0.5

            # Generate curved segments
            upper_leg_pts = create_curved_segment(
                (0, hip_y),
                (knee_left_x, knee_left_y),
                curve_amount=left_upper_leg_curve,
                num_points=8
            )
            for pt in upper_leg_pts:
                points.append([pt[0], pt[1]])

            lower_leg_pts = create_curved_segment(
                (knee_left_x, knee_left_y),
                (foot_left_x, foot_left_y),
                curve_amount=left_lower_leg_curve,
                num_points=8
            )
            for pt in lower_leg_pts[1:]:
                points.append([pt[0], pt[1]])

            # Right leg with hip and knee angles
            right_hip_rad = np.radians(self._right_hip_angle)
            right_knee_rad = np.radians(self._right_knee_angle)

            # Upper leg direction
            upper_right_leg_angle = np.pi / 2 - right_hip_rad

            # Knee position
            knee_right_x = upper_leg_length * np.cos(upper_right_leg_angle)
            knee_right_y = hip_y + upper_leg_length * np.sin(upper_right_leg_angle)

            # Lower leg bends
            lower_right_leg_angle = upper_right_leg_angle - right_knee_rad

            # Foot position
            foot_right_x = knee_right_x + lower_leg_length * np.cos(lower_right_leg_angle)
            foot_right_y = knee_right_y + lower_leg_length * np.sin(lower_right_leg_angle)

            # Calculate curve amounts (auto or manual)
            right_upper_leg_curve = self._right_upper_leg_curve
            right_lower_leg_curve = self._right_lower_leg_curve
            if self._auto_curve and (right_upper_leg_curve == 0.0 or right_lower_leg_curve == 0.0):
                angle_factor = abs(np.sin(upper_right_leg_angle - np.pi/2)) * self._auto_curve_strength
                if right_upper_leg_curve == 0.0:
                    right_upper_leg_curve = -angle_factor * 0.6
                if right_lower_leg_curve == 0.0:
                    right_lower_leg_curve = -angle_factor * 0.5

            # Generate curved segments
            upper_leg_pts = create_curved_segment(
                (0, hip_y),
                (knee_right_x, knee_right_y),
                curve_amount=right_upper_leg_curve,
                num_points=8
            )
            for pt in upper_leg_pts:
                points.append([pt[0], pt[1]])

            lower_leg_pts = create_curved_segment(
                (knee_right_x, knee_right_y),
                (foot_right_x, foot_right_y),
                curve_amount=right_lower_leg_curve,
                num_points=8
            )
            for pt in lower_leg_pts[1:]:
                points.append([pt[0], pt[1]])

        else:
            # Use pose-based system (backward compatibility)
            left_arm_angle = np.radians(self._pose.left_arm)
            right_arm_angle = np.radians(self._pose.right_arm)

            # Left arm
            elbow_left_x = -arm_length * 0.5 * np.cos(left_arm_angle)
            elbow_left_y = arm_y + arm_length * 0.5 * np.sin(left_arm_angle)
            hand_left_x = -arm_length * np.cos(left_arm_angle)
            hand_left_y = arm_y + arm_length * np.sin(left_arm_angle)

            points.append([0, arm_y])
            points.append([elbow_left_x, elbow_left_y])
            points.append([elbow_left_x, elbow_left_y])
            points.append([hand_left_x, hand_left_y])

            left_hand_pos = (hand_left_x, hand_left_y)
            left_arm_angle_rad = left_arm_angle

            # Right arm
            elbow_right_x = arm_length * 0.5 * np.cos(right_arm_angle)
            elbow_right_y = arm_y + arm_length * 0.5 * np.sin(right_arm_angle)
            hand_right_x = arm_length * np.cos(right_arm_angle)
            hand_right_y = arm_y + arm_length * np.sin(right_arm_angle)

            points.append([0, arm_y])
            points.append([elbow_right_x, elbow_right_y])
            points.append([elbow_right_x, elbow_right_y])
            points.append([hand_right_x, hand_right_y])

            right_hand_pos = (hand_right_x, hand_right_y)
            right_arm_angle_rad = right_arm_angle

            # Legs
            left_leg_angle = np.radians(90 + self._pose.left_leg)
            right_leg_angle = np.radians(90 + self._pose.right_leg)

            # Left leg
            knee_left_x = -leg_length * 0.5 * np.cos(left_leg_angle)
            knee_left_y = hip_y + leg_length * 0.5 * np.sin(left_leg_angle)
            foot_left_x = -leg_length * np.cos(left_leg_angle)
            foot_left_y = hip_y + leg_length * np.sin(left_leg_angle)

            points.append([0, hip_y])
            points.append([knee_left_x, knee_left_y])
            points.append([knee_left_x, knee_left_y])
            points.append([foot_left_x, foot_left_y])

            # Right leg
            knee_right_x = leg_length * 0.5 * np.cos(right_leg_angle)
            knee_right_y = hip_y + leg_length * 0.5 * np.sin(right_leg_angle)
            foot_right_x = leg_length * np.cos(right_leg_angle)
            foot_right_y = hip_y + leg_length * np.sin(right_leg_angle)

            points.append([0, hip_y])
            points.append([knee_right_x, knee_right_y])
            points.append([knee_right_x, knee_right_y])
            points.append([foot_right_x, foot_right_y])

        # Add hand gesture geometry if needed
        if self._left_hand != "none":
            gesture_points = self._generate_hand_gesture(
                left_hand_pos[0], left_hand_pos[1],
                left_arm_angle_rad, self._left_hand
            )
            points.extend(gesture_points)

        if self._right_hand != "none":
            gesture_points = self._generate_hand_gesture(
                right_hand_pos[0], right_hand_pos[1],
                right_arm_angle_rad, self._right_hand
            )
            points.extend(gesture_points)

        self._points = np.array(points, dtype=np.float64)

        if self.facing == "left":
            self._points[:, 0] *= -1

    @property
    def line_width(self) -> float:
        """Get the effective line width for rendering.

        If an explicit line_width was provided, uses that value (clamped to min 0.5).
        If auto_line_width is True and no explicit value was given, calculates
        line width proportionally based on character height:
        - 100px height = 2.0 line width (reference)
        - 50px height = 1.0 line width
        - 200px height = 4.0 line width
        - Clamped between MIN_LINE_WIDTH (0.5) and MAX_LINE_WIDTH (6.0)
        """
        if self._explicit_line_width is not None:
            # User specified explicit value, use it (with minimum)
            return max(self.MIN_LINE_WIDTH, self._explicit_line_width)

        if self.auto_line_width:
            # Calculate proportional line width based on height
            scale = self.character_height / self.REFERENCE_HEIGHT
            calculated = self.DEFAULT_LINE_WIDTH * scale
            return max(self.MIN_LINE_WIDTH, min(self.MAX_LINE_WIDTH, calculated))

        # auto_line_width is False and no explicit value: use default
        return self.DEFAULT_LINE_WIDTH

    @line_width.setter
    def line_width(self, value: float) -> None:
        """Set an explicit line width value."""
        self._explicit_line_width = value

    def get_render_data(self) -> dict[str, Any]:
        """Get data for rendering."""
        data = super().get_render_data()
        data.update({
            "proportion_style": self.proportion_style,
            "head_ratio": self.head_ratio,
            "torso_ratio": self.torso_ratio,
            "arm_ratio": self.arm_ratio,
            "leg_ratio": self.leg_ratio,
            "head_squash": self.head_squash,
            "line_width": self.line_width,
            "auto_line_width": self.auto_line_width,
            # Articulation data
            "use_articulation": self._use_articulation,
            "left_shoulder_angle": self._left_shoulder_angle,
            "left_elbow_angle": self._left_elbow_angle,
            "right_shoulder_angle": self._right_shoulder_angle,
            "right_elbow_angle": self._right_elbow_angle,
            "left_hip_angle": self._left_hip_angle,
            "left_knee_angle": self._left_knee_angle,
            "right_hip_angle": self._right_hip_angle,
            "right_knee_angle": self._right_knee_angle,
            "left_hand": self._left_hand,
            "right_hand": self._right_hand,
        })
        return data


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


class AnimalStyle(Character):
    """Anthropomorphic animal character for furry/mascot-style comics.

    A character that combines animal features with humanoid body structure:
    - Animal head shape based on species (cat, dog, rabbit, fox, bear, bird, wolf)
    - Ears appropriate to species (pointed, floppy, tall)
    - Optional tail
    - Humanoid body proportions for standing/posing
    - Expressive animal-style face features

    Suitable for furry comics, mascot characters, children's comics, and anthropomorphic stories.
    """

    # Species presets with head shape and feature configuration
    SPECIES_PRESETS: dict[str, dict[str, Any]] = {
        "cat": {
            "head_shape": "round",
            "ear_type": "pointed",
            "ear_angle": 30,
            "muzzle_size": 0.3,
            "has_tail": True,
            "tail_length": 0.4,
            "tail_curve": 0.3,
        },
        "dog": {
            "head_shape": "round",
            "ear_type": "floppy",
            "ear_angle": 45,
            "muzzle_size": 0.4,
            "has_tail": True,
            "tail_length": 0.3,
            "tail_curve": 0.5,
        },
        "rabbit": {
            "head_shape": "oval",
            "ear_type": "tall",
            "ear_angle": 15,
            "muzzle_size": 0.2,
            "has_tail": True,
            "tail_length": 0.1,
            "tail_curve": 0.0,
        },
        "fox": {
            "head_shape": "pointed",
            "ear_type": "pointed",
            "ear_angle": 25,
            "muzzle_size": 0.45,
            "has_tail": True,
            "tail_length": 0.5,
            "tail_curve": 0.4,
        },
        "bear": {
            "head_shape": "round",
            "ear_type": "round",
            "ear_angle": 60,
            "muzzle_size": 0.35,
            "has_tail": False,
            "tail_length": 0.0,
            "tail_curve": 0.0,
        },
        "bird": {
            "head_shape": "round",
            "ear_type": "none",
            "ear_angle": 0,
            "muzzle_size": 0.5,
            "has_tail": True,
            "tail_length": 0.25,
            "tail_curve": 0.0,
        },
        "wolf": {
            "head_shape": "pointed",
            "ear_type": "pointed",
            "ear_angle": 20,
            "muzzle_size": 0.5,
            "has_tail": True,
            "tail_length": 0.45,
            "tail_curve": 0.2,
        },
    }

    def __init__(
        self,
        name: str = "AnimalCharacter",
        species: str = "cat",
        fur_color: str = "#D2691E",
        fur_secondary: str = "#FFFFFF",
        eye_color: str = "#4A90D9",
        nose_color: str = "#333333",
        outfit_color: str = "#4169E1",
        ear_type: str | None = None,
        has_tail: bool | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize AnimalStyle character.

        Args:
            name: Character name
            species: Animal species preset ("cat", "dog", "rabbit", "fox", "bear", "bird", "wolf")
            fur_color: Primary fur/feather color (default brown)
            fur_secondary: Secondary fur color for markings (default white)
            eye_color: Eye color (default blue)
            nose_color: Nose color (default dark gray)
            outfit_color: Color for simple outfit (default royal blue)
            ear_type: Override ear type ("pointed", "floppy", "tall", "round", "none")
            has_tail: Override whether character has a tail
            **kwargs: Additional Character parameters
        """
        kwargs.setdefault("style", "animal")
        kwargs.setdefault("color", "#333333")
        kwargs.setdefault("fill_color", fur_color)

        # Get species preset
        if species not in self.SPECIES_PRESETS:
            logger.warning(
                "Unknown species '%s', falling back to 'cat'. "
                "Valid species: %s",
                species,
                ", ".join(sorted(self.SPECIES_PRESETS.keys())),
            )
            species = "cat"

        self.species = species
        preset = self.SPECIES_PRESETS[species]

        self.fur_color = fur_color
        self.fur_secondary = fur_secondary
        self.eye_color = eye_color
        self.nose_color = nose_color
        self.outfit_color = outfit_color

        # Use preset values unless overridden
        self.head_shape = preset["head_shape"]
        self.ear_type = ear_type if ear_type is not None else preset["ear_type"]
        self.ear_angle = preset["ear_angle"]
        self.muzzle_size = preset["muzzle_size"]
        self._has_tail = has_tail if has_tail is not None else preset["has_tail"]
        self.tail_length = preset["tail_length"]
        self.tail_curve = preset["tail_curve"]

        super().__init__(name=name, **kwargs)

    def generate_points(self) -> None:
        """Generate anthropomorphic animal figure points.

        Structure:
        - Head: Species-specific shape with ears
        - Muzzle: Protruding snout/beak based on species
        - Body: Humanoid proportions
        - Arms: Humanoid arms with paw-like hands
        - Legs: Digitigrade or plantigrade legs
        - Tail: Optional tail based on species
        """
        h = self.character_height

        # Proportions for anthropomorphic character
        head_height = h * 0.18
        head_width = h * 0.14
        ear_height = h * 0.10
        ear_width = h * 0.05
        neck_height = h * 0.03
        body_height = h * 0.30
        body_width = h * 0.18
        arm_length = h * 0.24
        leg_length = h * 0.32
        paw_size = h * 0.04

        points = []

        # Calculate vertical positions
        head_top = h / 2
        head_center_y = head_top - head_height / 2
        head_bottom = head_top - head_height
        neck_bottom = head_bottom - neck_height
        shoulder_y = neck_bottom
        hip_y = shoulder_y - body_height

        # Generate head shape based on species
        if self.head_shape == "round":
            # Round head (cat, dog, bear)
            for angle in np.linspace(0, 2 * np.pi, 24):
                points.append([
                    head_width * np.cos(angle),
                    head_center_y + head_height * 0.5 * np.sin(angle)
                ])
        elif self.head_shape == "oval":
            # Oval head (rabbit) - taller than wide
            for angle in np.linspace(0, 2 * np.pi, 24):
                points.append([
                    head_width * 0.85 * np.cos(angle),
                    head_center_y + head_height * 0.55 * np.sin(angle)
                ])
        else:  # pointed (fox, wolf)
            # Pointed/angular head - narrower at bottom
            for angle in np.linspace(0, 2 * np.pi, 24):
                width_mod = 1.0 if np.sin(angle) >= 0 else 0.7
                points.append([
                    head_width * width_mod * np.cos(angle),
                    head_center_y + head_height * 0.5 * np.sin(angle)
                ])

        # Generate ears based on ear_type
        if self.ear_type == "pointed":
            # Pointed ears (cat, fox, wolf) - triangular
            ear_offset = head_width * 0.6
            ear_angle_rad = np.radians(self.ear_angle)

            # Left ear (3 points: base-outside, tip, base-inside)
            points.append([-ear_offset - ear_width * 0.3, head_top - head_height * 0.1])
            points.append([
                -ear_offset - ear_width * np.sin(ear_angle_rad),
                head_top + ear_height * np.cos(ear_angle_rad)
            ])
            points.append([-ear_offset + ear_width * 0.3, head_top - head_height * 0.1])

            # Right ear
            points.append([ear_offset - ear_width * 0.3, head_top - head_height * 0.1])
            points.append([
                ear_offset + ear_width * np.sin(ear_angle_rad),
                head_top + ear_height * np.cos(ear_angle_rad)
            ])
            points.append([ear_offset + ear_width * 0.3, head_top - head_height * 0.1])

        elif self.ear_type == "floppy":
            # Floppy ears (dog) - droop down
            ear_offset = head_width * 0.8
            # Left ear - curves down
            for t in np.linspace(0, 1, 8):
                points.append([
                    -ear_offset - ear_width * 0.5 * np.sin(t * np.pi),
                    head_center_y + head_height * 0.3 - t * ear_height * 1.5
                ])
            # Right ear
            for t in np.linspace(0, 1, 8):
                points.append([
                    ear_offset + ear_width * 0.5 * np.sin(t * np.pi),
                    head_center_y + head_height * 0.3 - t * ear_height * 1.5
                ])

        elif self.ear_type == "tall":
            # Tall ears (rabbit) - long upright
            ear_offset = head_width * 0.5
            tall_ear_height = ear_height * 2.5

            # Left ear (elongated oval)
            for angle in np.linspace(0, 2 * np.pi, 12):
                points.append([
                    -ear_offset + ear_width * 0.4 * np.cos(angle),
                    head_top + tall_ear_height * 0.5 + tall_ear_height * 0.5 * np.sin(angle)
                ])

            # Right ear
            for angle in np.linspace(0, 2 * np.pi, 12):
                points.append([
                    ear_offset + ear_width * 0.4 * np.cos(angle),
                    head_top + tall_ear_height * 0.5 + tall_ear_height * 0.5 * np.sin(angle)
                ])

        elif self.ear_type == "round":
            # Round ears (bear) - small semicircles
            ear_offset = head_width * 0.7
            small_ear_size = ear_height * 0.5

            # Left ear
            for angle in np.linspace(0, np.pi, 8):
                points.append([
                    -ear_offset + small_ear_size * np.cos(angle),
                    head_top - head_height * 0.1 + small_ear_size * np.sin(angle)
                ])

            # Right ear
            for angle in np.linspace(0, np.pi, 8):
                points.append([
                    ear_offset + small_ear_size * np.cos(angle),
                    head_top - head_height * 0.1 + small_ear_size * np.sin(angle)
                ])

        # Muzzle points (snout/beak)
        muzzle_length = head_height * self.muzzle_size
        muzzle_y = head_center_y - head_height * 0.2
        if self.species == "bird":
            # Beak shape (triangular)
            points.append([0, muzzle_y + muzzle_length * 0.3])  # Top
            points.append([muzzle_length * 0.8, muzzle_y - muzzle_length * 0.2])  # Tip
            points.append([0, muzzle_y - muzzle_length * 0.3])  # Bottom
        else:
            # Standard muzzle (rounded)
            for angle in np.linspace(-np.pi/2, np.pi/2, 8):
                points.append([
                    head_width * 0.3 + muzzle_length * np.cos(angle),
                    muzzle_y + muzzle_length * 0.5 * np.sin(angle)
                ])

        # Neck
        neck_width = h * 0.04
        points.append([-neck_width, head_bottom])
        points.append([-neck_width, neck_bottom])
        points.append([neck_width, neck_bottom])
        points.append([neck_width, head_bottom])

        # Body (humanoid torso)
        points.append([-body_width / 2, shoulder_y])  # Left shoulder
        points.append([-body_width * 0.4, hip_y])  # Left hip
        points.append([body_width * 0.4, hip_y])  # Right hip
        points.append([body_width / 2, shoulder_y])  # Right shoulder

        # Arms with paw hands
        arm_y = shoulder_y - h * 0.02

        # Left arm
        left_arm_angle = np.radians(self._pose.left_arm)
        left_elbow_x = -body_width / 2 - arm_length * 0.45 * np.cos(left_arm_angle)
        left_elbow_y = arm_y - arm_length * 0.45 * np.sin(left_arm_angle)
        left_paw_x = -body_width / 2 - arm_length * np.cos(left_arm_angle)
        left_paw_y = arm_y - arm_length * np.sin(left_arm_angle)

        points.append([-body_width / 2, arm_y])  # Shoulder
        points.append([left_elbow_x, left_elbow_y])  # Elbow
        points.append([left_paw_x, left_paw_y])  # Paw
        # Paw shape (rounded with slight indentations for digits)
        for angle in np.linspace(0, 2 * np.pi, 10):
            pad_mod = 1.0 + 0.15 * np.cos(4 * angle)  # Slight bumps for paw pads
            points.append([
                left_paw_x + paw_size * pad_mod * np.cos(angle),
                left_paw_y + paw_size * 0.8 * np.sin(angle)
            ])

        # Right arm
        right_arm_angle = np.radians(self._pose.right_arm)
        right_elbow_x = body_width / 2 + arm_length * 0.45 * np.cos(right_arm_angle)
        right_elbow_y = arm_y - arm_length * 0.45 * np.sin(right_arm_angle)
        right_paw_x = body_width / 2 + arm_length * np.cos(right_arm_angle)
        right_paw_y = arm_y - arm_length * np.sin(right_arm_angle)

        points.append([body_width / 2, arm_y])  # Shoulder
        points.append([right_elbow_x, right_elbow_y])  # Elbow
        points.append([right_paw_x, right_paw_y])  # Paw
        # Paw shape
        for angle in np.linspace(0, 2 * np.pi, 10):
            pad_mod = 1.0 + 0.15 * np.cos(4 * angle)
            points.append([
                right_paw_x + paw_size * pad_mod * np.cos(angle),
                right_paw_y + paw_size * 0.8 * np.sin(angle)
            ])

        # Legs
        leg_gap = body_width * 0.25

        # Left leg
        left_leg_angle = np.radians(90 + self._pose.left_leg)
        left_knee_x = -leg_gap - leg_length * 0.45 * np.cos(left_leg_angle)
        left_knee_y = hip_y - leg_length * 0.45 * np.sin(left_leg_angle)
        left_foot_x = -leg_gap - leg_length * np.cos(left_leg_angle)
        left_foot_y = hip_y - leg_length * np.sin(left_leg_angle)

        points.append([-leg_gap, hip_y])  # Hip
        points.append([left_knee_x, left_knee_y])  # Knee
        points.append([left_foot_x, left_foot_y])  # Foot
        # Paw foot (larger than hand paw)
        for angle in np.linspace(0, 2 * np.pi, 10):
            points.append([
                left_foot_x + paw_size * 1.3 * np.cos(angle),
                left_foot_y + paw_size * 0.6 * np.sin(angle)
            ])

        # Right leg
        right_leg_angle = np.radians(90 + self._pose.right_leg)
        right_knee_x = leg_gap + leg_length * 0.45 * np.cos(right_leg_angle)
        right_knee_y = hip_y - leg_length * 0.45 * np.sin(right_leg_angle)
        right_foot_x = leg_gap + leg_length * np.cos(right_leg_angle)
        right_foot_y = hip_y - leg_length * np.sin(right_leg_angle)

        points.append([leg_gap, hip_y])  # Hip
        points.append([right_knee_x, right_knee_y])  # Knee
        points.append([right_foot_x, right_foot_y])  # Foot
        # Paw foot
        for angle in np.linspace(0, 2 * np.pi, 10):
            points.append([
                right_foot_x + paw_size * 1.3 * np.cos(angle),
                right_foot_y + paw_size * 0.6 * np.sin(angle)
            ])

        # Tail (if species has one)
        if self._has_tail:
            tail_base_y = hip_y + body_height * 0.1
            tail_len = h * self.tail_length
            tail_segments = 8

            # Generate tail curve
            for i in range(tail_segments):
                t = i / (tail_segments - 1)
                # Tail curves based on tail_curve parameter
                curve = self.tail_curve * np.sin(t * np.pi)
                points.append([
                    -body_width * 0.3 - tail_len * t * 0.7 - curve * h * 0.1,
                    tail_base_y - tail_len * t * 0.5
                ])

        self._points = np.array(points, dtype=np.float64)

        if self.facing == "left":
            self._points[:, 0] *= -1

    def get_render_data(self) -> dict[str, Any]:
        """Get data for rendering."""
        data = super().get_render_data()
        # Add animal-specific render info
        data["species"] = self.species
        data["fur_color"] = self.fur_color
        data["fur_secondary"] = self.fur_secondary
        data["eye_color"] = self.eye_color
        data["nose_color"] = self.nose_color
        data["outfit_color"] = self.outfit_color
        data["head_shape"] = self.head_shape
        data["ear_type"] = self.ear_type
        data["ear_angle"] = self.ear_angle
        data["muzzle_size"] = self.muzzle_size
        data["has_tail"] = self._has_tail
        data["tail_length"] = self.tail_length
        data["tail_curve"] = self.tail_curve
        data["head_height_ratio"] = 0.18
        data["head_width_ratio"] = 0.14
        data["body_height_ratio"] = 0.30
        data["arm_length_ratio"] = 0.24
        data["leg_length_ratio"] = 0.32
        return data
