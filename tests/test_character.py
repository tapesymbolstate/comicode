"""Tests for Character classes."""

import numpy as np
import pytest

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
        assert bubble.style == "speech"
        assert bubble.tail_target is char

    def test_think(self):
        """Test think method creates thought bubble."""
        char = Character().move_to((100, 100))
        bubble = char.think("Hmm...")
        assert bubble.text == "Hmm..."
        assert bubble.style == "thought"

    def test_shout(self):
        """Test shout method creates shout bubble."""
        char = Character().move_to((100, 100))
        bubble = char.shout("HEY!")
        assert bubble.text == "HEY!"
        assert bubble.style == "shout"


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
