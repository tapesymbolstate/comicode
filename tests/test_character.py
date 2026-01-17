"""Tests for Character classes."""

import numpy as np

from comix.cobject.character.character import (
    Character,
    Stickman,
    SimpleFace,
    Expression,
    Pose,
)


class TestExpression:
    """Tests for Expression class."""

    def test_default_expression(self):
        """Test default expression."""
        expr = Expression()
        assert expr.name == "neutral"
        assert expr.eyes == "normal"
        assert expr.mouth == "normal"

    def test_from_name(self):
        """Test creating expression from preset name."""
        expr = Expression.from_name("happy")
        assert expr.name == "happy"
        assert expr.mouth == "smile"

    def test_unknown_name(self):
        """Test unknown expression name returns default."""
        expr = Expression.from_name("unknown")
        assert expr.name == "neutral"

    def test_sleepy_expression(self):
        """Test sleepy expression preset."""
        expr = Expression.from_name("sleepy")
        assert expr.name == "sleepy"
        assert expr.eyes == "closed"
        assert expr.mouth == "normal"
        assert expr.eyebrows == "relaxed"

    def test_excited_expression(self):
        """Test excited expression preset."""
        expr = Expression.from_name("excited")
        assert expr.name == "excited"
        assert expr.eyes == "stars"
        assert expr.mouth == "grin"
        assert expr.eyebrows == "raised"

    def test_scared_expression(self):
        """Test scared expression preset."""
        expr = Expression.from_name("scared")
        assert expr.name == "scared"
        assert expr.eyes == "wide"
        assert expr.mouth == "gasp"
        assert expr.eyebrows == "worried"

    def test_smirk_expression(self):
        """Test smirk expression preset."""
        expr = Expression.from_name("smirk")
        assert expr.name == "smirk"
        assert expr.eyes == "normal"
        assert expr.mouth == "smirk"
        assert expr.eyebrows == "asymmetric"

    def test_crying_expression(self):
        """Test crying expression preset."""
        expr = Expression.from_name("crying")
        assert expr.name == "crying"
        assert expr.eyes == "tears"
        assert expr.mouth == "frown"
        assert expr.eyebrows == "worried"

    def test_expression_class_constants(self):
        """Test expression class constants are defined."""
        assert Expression.SLEEPY == "sleepy"
        assert Expression.EXCITED == "excited"
        assert Expression.SCARED == "scared"
        assert Expression.SMIRK == "smirk"
        assert Expression.CRYING == "crying"


class TestPose:
    """Tests for Pose class."""

    def test_default_pose(self):
        """Test default pose."""
        pose = Pose()
        assert pose.name == "standing"

    def test_from_name(self):
        """Test creating pose from preset name."""
        pose = Pose.from_name("waving")
        assert pose.name == "waving"
        assert pose.left_arm == -135

    def test_jumping_pose(self):
        """Test jumping pose preset."""
        pose = Pose.from_name("jumping")
        assert pose.name == "jumping"
        assert pose.left_arm == -45
        assert pose.right_arm == 45
        assert pose.left_leg == -30
        assert pose.right_leg == -30
        assert pose.body_angle == -5

    def test_dancing_pose(self):
        """Test dancing pose preset."""
        pose = Pose.from_name("dancing")
        assert pose.name == "dancing"
        assert pose.left_arm == -120
        assert pose.right_arm == 45
        assert pose.body_angle == 5

    def test_lying_pose(self):
        """Test lying pose preset."""
        pose = Pose.from_name("lying")
        assert pose.name == "lying"
        assert pose.body_angle == 90

    def test_kneeling_pose(self):
        """Test kneeling pose preset."""
        pose = Pose.from_name("kneeling")
        assert pose.name == "kneeling"
        assert pose.left_leg == 90
        assert pose.right_leg == 120

    def test_cheering_pose(self):
        """Test cheering pose preset."""
        pose = Pose.from_name("cheering")
        assert pose.name == "cheering"
        assert pose.left_arm == -150
        assert pose.right_arm == -150
        assert pose.body_angle == -5

    def test_thinking_pose(self):
        """Test thinking pose preset."""
        pose = Pose.from_name("thinking")
        assert pose.name == "thinking"
        assert pose.left_arm == 60
        assert pose.right_arm == 15

    def test_pose_class_constants(self):
        """Test pose class constants are defined."""
        assert Pose.JUMPING == "jumping"
        assert Pose.DANCING == "dancing"
        assert Pose.LYING == "lying"
        assert Pose.KNEELING == "kneeling"
        assert Pose.CHEERING == "cheering"
        assert Pose.THINKING == "thinking"


class TestCharacter:
    """Tests for Character base class."""

    def test_default_init(self):
        """Test default initialization."""
        char = Character()
        assert char.name == "Character"
        assert char.style == "stickman"
        assert char.color == "#000000"
        assert char.character_height == 100.0
        assert char.facing == "right"

    def test_set_expression(self):
        """Test setting expression."""
        char = Character()
        result = char.set_expression("happy")
        assert result is char
        assert char._expression.name == "happy"

    def test_set_pose(self):
        """Test setting pose."""
        char = Character()
        result = char.set_pose("waving")
        assert result is char
        assert char._pose.name == "waving"

    def test_face(self):
        """Test facing direction."""
        char = Character()
        result = char.face("left")
        assert result is char
        assert char.facing == "left"

    def test_say(self):
        """Test say method creates speech bubble."""
        char = Character().move_to((100, 100))
        bubble = char.say("Hello!")
        assert bubble.text == "Hello!"
        assert bubble.bubble_type == "speech"
        assert bubble.tail_target is char

    def test_think(self):
        """Test think method creates thought bubble."""
        char = Character().move_to((100, 100))
        bubble = char.think("Hmm...")
        assert bubble.text == "Hmm..."
        assert bubble.bubble_type == "thought"

    def test_shout(self):
        """Test shout method creates shout bubble."""
        char = Character().move_to((100, 100))
        bubble = char.shout("HEY!")
        assert bubble.text == "HEY!"
        assert bubble.bubble_type == "shout"

    def test_whisper(self):
        """Test whisper method creates whisper bubble."""
        char = Character().move_to((100, 100))
        bubble = char.whisper("psst...")
        assert bubble.text == "psst..."
        assert bubble.bubble_type == "whisper"
        assert bubble.tail_target is char


class TestStickman:
    """Tests for Stickman class."""

    def test_default_init(self):
        """Test default initialization."""
        stickman = Stickman()
        assert stickman.name == "Stickman"
        assert stickman.style == "stickman"

    def test_custom_name(self):
        """Test custom name."""
        stickman = Stickman(name="Bob")
        assert stickman.name == "Bob"

    def test_generates_points(self):
        """Test that stickman generates points."""
        stickman = Stickman()
        assert len(stickman._points) > 0

    def test_facing_flips_points(self):
        """Test that facing left flips x coordinates."""
        right = Stickman(facing="right")
        left = Stickman(facing="left")

        right_x = right._points[:, 0]
        left_x = left._points[:, 0]

        np.allclose(right_x, -left_x)


class TestSimpleFace:
    """Tests for SimpleFace class."""

    def test_default_init(self):
        """Test default initialization."""
        face = SimpleFace()
        assert face.name == "Face"
        assert face.style == "simple"
        assert face.character_height == 60.0

    def test_generates_circle_points(self):
        """Test that face generates circle points."""
        face = SimpleFace()
        assert len(face._points) == 32

    def test_get_render_data(self):
        """Test render data includes face_radius."""
        face = SimpleFace()
        data = face.get_render_data()
        assert "face_radius" in data
        assert data["face_radius"] == 30.0
