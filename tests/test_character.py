"""Tests for Character classes."""

import numpy as np

from comix.cobject.character.character import (
    Character,
    Chibi,
    ChubbyStickman,
    Expression,
    Pose,
    Robot,
    SimpleFace,
    Stickman,
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


class TestChubbyStickman:
    """Tests for ChubbyStickman class."""

    def test_default_init(self):
        """Test default initialization."""
        chubby = ChubbyStickman()
        assert chubby.name == "ChubbyStickman"
        assert chubby.style == "chubby"
        assert chubby.fill_color == "#FFFFFF"

    def test_custom_name(self):
        """Test custom name."""
        chubby = ChubbyStickman(name="Bubbles")
        assert chubby.name == "Bubbles"

    def test_generates_points(self):
        """Test that chubby stickman generates points."""
        chubby = ChubbyStickman()
        # Should have enough points for head (24), body (16), and limbs (4 * 10)
        assert len(chubby._points) >= 80

    def test_facing_flips_points(self):
        """Test that facing left flips x coordinates."""
        right = ChubbyStickman(facing="right")
        left = ChubbyStickman(facing="left")

        right_x = right._points[:, 0]
        left_x = left._points[:, 0]

        np.allclose(right_x, -left_x)

    def test_custom_height(self):
        """Test custom height."""
        chubby = ChubbyStickman(height=150.0)
        assert chubby.character_height == 150.0
        # Points should scale with height
        data = chubby.get_render_data()
        assert data["character_height"] == 150.0

    def test_custom_colors(self):
        """Test custom colors."""
        chubby = ChubbyStickman(color="#FF0000", fill_color="#FFAAAA")
        assert chubby.color == "#FF0000"
        assert chubby.fill_color == "#FFAAAA"

    def test_get_render_data(self):
        """Test render data includes chubby-specific fields."""
        chubby = ChubbyStickman()
        data = chubby.get_render_data()
        assert "head_ratio" in data
        assert data["head_ratio"] == 0.22
        assert "body_width_ratio" in data
        assert data["body_width_ratio"] == 0.18
        assert "limb_thickness" in data
        assert data["limb_thickness"] == 100.0 * 0.04  # Default height * ratio

    def test_set_expression(self):
        """Test setting expression on chubby stickman."""
        chubby = ChubbyStickman()
        result = chubby.set_expression("happy")
        assert result is chubby
        assert chubby._expression.name == "happy"

    def test_set_pose(self):
        """Test setting pose on chubby stickman."""
        chubby = ChubbyStickman()
        result = chubby.set_pose("waving")
        assert result is chubby
        assert chubby._pose.name == "waving"

    def test_say_creates_bubble(self):
        """Test say method creates speech bubble."""
        chubby = ChubbyStickman().move_to((100, 100))
        bubble = chubby.say("Hello!")
        assert bubble.text == "Hello!"
        assert bubble.bubble_type == "speech"
        assert bubble.tail_target is chubby

    def test_think_creates_bubble(self):
        """Test think method creates thought bubble."""
        chubby = ChubbyStickman().move_to((100, 100))
        bubble = chubby.think("Hmm...")
        assert bubble.text == "Hmm..."
        assert bubble.bubble_type == "thought"

    def test_shout_creates_bubble(self):
        """Test shout method creates shout bubble."""
        chubby = ChubbyStickman().move_to((100, 100))
        bubble = chubby.shout("WOW!")
        assert bubble.text == "WOW!"
        assert bubble.bubble_type == "shout"

    def test_whisper_creates_bubble(self):
        """Test whisper method creates whisper bubble."""
        chubby = ChubbyStickman().move_to((100, 100))
        bubble = chubby.whisper("secret...")
        assert bubble.text == "secret..."
        assert bubble.bubble_type == "whisper"

    def test_all_poses(self):
        """Test chubby stickman with different poses."""
        poses = ["standing", "sitting", "walking", "running", "pointing",
                 "waving", "jumping", "dancing", "kneeling", "cheering", "thinking"]
        for pose_name in poses:
            chubby = ChubbyStickman(pose=pose_name)
            assert chubby._pose.name == pose_name
            # Should still generate valid points
            assert len(chubby._points) >= 80

    def test_all_expressions(self):
        """Test chubby stickman with different expressions."""
        expressions = ["neutral", "happy", "sad", "angry", "surprised",
                       "confused", "sleepy", "excited", "scared", "smirk", "crying"]
        for expr_name in expressions:
            chubby = ChubbyStickman(expression=expr_name)
            assert chubby._expression.name == expr_name
            data = chubby.get_render_data()
            assert data["expression"]["name"] == expr_name


class TestRobot:
    """Tests for Robot character class."""

    def test_default_init(self):
        """Test default initialization."""
        robot = Robot()
        assert robot.name == "Robot"
        assert robot.style == "robot"
        assert robot.antenna is True
        assert robot.panel_color == "#4A4A4A"
        assert robot.screen_color == "#1A1A2E"
        assert robot.led_color == "#00FF88"

    def test_custom_name(self):
        """Test custom name."""
        robot = Robot(name="RoboHelper")
        assert robot.name == "RoboHelper"

    def test_no_antenna(self):
        """Test robot without antenna."""
        robot = Robot(antenna=False)
        assert robot.antenna is False
        # Should generate fewer points without antenna
        with_antenna = Robot(antenna=True)
        assert len(robot._points) < len(with_antenna._points)

    def test_generates_points(self):
        """Test that robot generates points."""
        robot = Robot()
        # Should have points for: antenna (2), head (4), body (4), limbs (7 * 4)
        assert len(robot._points) >= 38  # Minimum expected points

    def test_facing_flips_points(self):
        """Test that facing left flips x coordinates."""
        right = Robot(facing="right")
        left = Robot(facing="left")

        right_x = right._points[:, 0]
        left_x = left._points[:, 0]

        np.allclose(right_x, -left_x)

    def test_custom_height(self):
        """Test custom height."""
        robot = Robot(height=150.0)
        assert robot.character_height == 150.0
        data = robot.get_render_data()
        assert data["character_height"] == 150.0

    def test_custom_colors(self):
        """Test custom colors."""
        robot = Robot(
            color="#FF0000",
            fill_color="#FFAAAA",
            panel_color="#222222",
            screen_color="#000066",
            led_color="#00FFFF",
        )
        assert robot.color == "#FF0000"
        assert robot.fill_color == "#FFAAAA"
        assert robot.panel_color == "#222222"
        assert robot.screen_color == "#000066"
        assert robot.led_color == "#00FFFF"

    def test_get_render_data(self):
        """Test render data includes robot-specific fields."""
        robot = Robot()
        data = robot.get_render_data()
        assert data["style"] == "robot"
        assert "antenna" in data
        assert data["antenna"] is True
        assert "panel_color" in data
        assert data["panel_color"] == "#4A4A4A"
        assert "screen_color" in data
        assert data["screen_color"] == "#1A1A2E"
        assert "led_color" in data
        assert data["led_color"] == "#00FF88"
        assert "head_height_ratio" in data
        assert data["head_height_ratio"] == 0.25
        assert "head_width_ratio" in data
        assert data["head_width_ratio"] == 0.22
        assert "body_height_ratio" in data
        assert data["body_height_ratio"] == 0.30
        assert "body_width_ratio" in data
        assert data["body_width_ratio"] == 0.26
        assert "joint_size" in data
        assert data["joint_size"] == 100.0 * 0.03  # Default height * ratio

    def test_set_expression(self):
        """Test setting expression on robot."""
        robot = Robot()
        result = robot.set_expression("happy")
        assert result is robot
        assert robot._expression.name == "happy"

    def test_set_pose(self):
        """Test setting pose on robot."""
        robot = Robot()
        result = robot.set_pose("waving")
        assert result is robot
        assert robot._pose.name == "waving"

    def test_say_creates_bubble(self):
        """Test say method creates speech bubble."""
        robot = Robot().move_to((100, 100))
        bubble = robot.say("Beep boop!")
        assert bubble.text == "Beep boop!"
        assert bubble.bubble_type == "speech"
        assert bubble.tail_target is robot

    def test_think_creates_bubble(self):
        """Test think method creates thought bubble."""
        robot = Robot().move_to((100, 100))
        bubble = robot.think("Computing...")
        assert bubble.text == "Computing..."
        assert bubble.bubble_type == "thought"

    def test_shout_creates_bubble(self):
        """Test shout method creates shout bubble."""
        robot = Robot().move_to((100, 100))
        bubble = robot.shout("ALERT!")
        assert bubble.text == "ALERT!"
        assert bubble.bubble_type == "shout"

    def test_whisper_creates_bubble(self):
        """Test whisper method creates whisper bubble."""
        robot = Robot().move_to((100, 100))
        bubble = robot.whisper("*beep*")
        assert bubble.text == "*beep*"
        assert bubble.bubble_type == "whisper"

    def test_all_poses(self):
        """Test robot with different poses."""
        poses = ["standing", "sitting", "walking", "running", "pointing",
                 "waving", "jumping", "dancing", "kneeling", "cheering", "thinking"]
        for pose_name in poses:
            robot = Robot(pose=pose_name)
            assert robot._pose.name == pose_name
            # Should still generate valid points
            assert len(robot._points) >= 38

    def test_all_expressions(self):
        """Test robot with different expressions."""
        expressions = ["neutral", "happy", "sad", "angry", "surprised",
                       "confused", "sleepy", "excited", "scared", "smirk", "crying"]
        for expr_name in expressions:
            robot = Robot(expression=expr_name)
            assert robot._expression.name == expr_name
            data = robot.get_render_data()
            assert data["expression"]["name"] == expr_name

    def test_default_fill_color(self):
        """Test default fill color is metal gray."""
        robot = Robot()
        assert robot.fill_color == "#6B7280"

    def test_default_outline_color(self):
        """Test default outline color."""
        robot = Robot()
        assert robot.color == "#333333"


class TestChibi:
    """Tests for Chibi character class."""

    def test_default_init(self):
        """Test default chibi initialization."""
        chibi = Chibi()
        assert chibi.name == "Chibi"
        assert chibi.style == "chibi"
        assert chibi.character_height == 100.0

    def test_custom_name(self):
        """Test chibi with custom name."""
        chibi = Chibi("Miku")
        assert chibi.name == "Miku"

    def test_custom_hair_style(self):
        """Test chibi with different hair styles."""
        styles = ["spiky", "long", "short", "twintails", "none"]
        for style in styles:
            chibi = Chibi(hair_style=style)
            assert chibi.hair_style == style

    def test_custom_colors(self):
        """Test chibi with custom colors."""
        chibi = Chibi(
            hair_color="#FF00FF",
            skin_color="#FFD700",
            outfit_color="#00FF00"
        )
        assert chibi.hair_color == "#FF00FF"
        assert chibi.skin_color == "#FFD700"
        assert chibi.outfit_color == "#00FF00"

    def test_blush_option(self):
        """Test chibi with blush enabled."""
        chibi = Chibi(blush=True)
        assert chibi.blush is True
        data = chibi.get_render_data()
        assert data["blush"] is True

    def test_generates_points(self):
        """Test chibi generates valid points."""
        chibi = Chibi()
        # Should generate head (32) + body (20) + 4 limbs (10 each)
        # = 32 + 20 + 40 = 92+ points
        assert len(chibi._points) >= 80

    def test_facing_flips_points(self):
        """Test facing direction flips points correctly."""
        chibi_right = Chibi(facing="right")
        chibi_left = Chibi(facing="left")
        # X coordinates should be flipped
        x_right = chibi_right._points[:, 0]
        x_left = chibi_left._points[:, 0]
        # The flipped version should have opposite signs
        assert not np.allclose(x_right, x_left)

    def test_custom_height(self):
        """Test chibi with custom height."""
        chibi = Chibi(height=150.0)
        assert chibi.character_height == 150.0

    def test_get_render_data(self):
        """Test render data contains chibi-specific properties."""
        chibi = Chibi(
            hair_style="twintails",
            hair_color="#FF69B4",
            skin_color="#FFE4C4",
            outfit_color="#4A90D9",
            blush=True
        )
        data = chibi.get_render_data()
        assert data["style"] == "chibi"
        assert data["hair_style"] == "twintails"
        assert data["hair_color"] == "#FF69B4"
        assert data["skin_color"] == "#FFE4C4"
        assert data["outfit_color"] == "#4A90D9"
        assert data["blush"] is True
        assert data["head_radius_ratio"] == 0.20
        assert data["body_height_ratio"] == 0.22
        assert data["body_width_ratio"] == 0.16

    def test_set_expression(self):
        """Test setting expression on chibi."""
        chibi = Chibi()
        result = chibi.set_expression("happy")
        assert result is chibi
        assert chibi._expression.name == "happy"

    def test_set_pose(self):
        """Test setting pose on chibi."""
        chibi = Chibi()
        result = chibi.set_pose("waving")
        assert result is chibi
        assert chibi._pose.name == "waving"

    def test_say_creates_bubble(self):
        """Test say method creates speech bubble."""
        chibi = Chibi().move_to((100, 100))
        bubble = chibi.say("Kawaii!")
        assert bubble.text == "Kawaii!"
        assert bubble.bubble_type == "speech"
        assert bubble.tail_target is chibi

    def test_think_creates_bubble(self):
        """Test think method creates thought bubble."""
        chibi = Chibi().move_to((100, 100))
        bubble = chibi.think("Hmm...")
        assert bubble.text == "Hmm..."
        assert bubble.bubble_type == "thought"

    def test_shout_creates_bubble(self):
        """Test shout method creates shout bubble."""
        chibi = Chibi().move_to((100, 100))
        bubble = chibi.shout("SUGOI!")
        assert bubble.text == "SUGOI!"
        assert bubble.bubble_type == "shout"

    def test_whisper_creates_bubble(self):
        """Test whisper method creates whisper bubble."""
        chibi = Chibi().move_to((100, 100))
        bubble = chibi.whisper("*shhh*")
        assert bubble.text == "*shhh*"
        assert bubble.bubble_type == "whisper"

    def test_all_poses(self):
        """Test chibi with different poses."""
        poses = ["standing", "sitting", "walking", "running", "pointing",
                 "waving", "jumping", "dancing", "kneeling", "cheering", "thinking"]
        for pose_name in poses:
            chibi = Chibi(pose=pose_name)
            assert chibi._pose.name == pose_name
            # Should still generate valid points
            assert len(chibi._points) >= 80

    def test_all_expressions(self):
        """Test chibi with different expressions."""
        expressions = ["neutral", "happy", "sad", "angry", "surprised",
                       "confused", "sleepy", "excited", "scared", "smirk", "crying"]
        for expr_name in expressions:
            chibi = Chibi(expression=expr_name)
            assert chibi._expression.name == expr_name
            data = chibi.get_render_data()
            assert data["expression"]["name"] == expr_name

    def test_default_fill_color_is_skin_color(self):
        """Test default fill color matches skin color."""
        chibi = Chibi()
        assert chibi.fill_color == "#FFE4C4"  # Default bisque skin tone

    def test_default_outline_color(self):
        """Test default outline color."""
        chibi = Chibi()
        assert chibi.color == "#333333"

    def test_limb_thickness(self):
        """Test limb thickness is calculated correctly."""
        chibi = Chibi(height=100)
        data = chibi.get_render_data()
        assert data["limb_thickness"] == 5.0  # height * 0.05
