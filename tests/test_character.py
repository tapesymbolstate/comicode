"""Tests for Character classes."""

import numpy as np

from comix.cobject.character.character import (
    Anime,
    Cartoon,
    Character,
    Chibi,
    ChubbyStickman,
    Expression,
    Pose,
    Robot,
    SimpleFace,
    Stickman,
    Superhero,
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


class TestAnime:
    """Tests for Anime character class."""

    def test_default_init(self):
        """Test default initialization."""
        anime = Anime()
        assert anime.name == "Anime"
        assert anime.style == "anime"
        assert anime.hair_style == "flowing"
        assert anime.hair_color == "#2D1B12"
        assert anime.skin_color == "#FFE0C4"
        assert anime.outfit_color == "#3B82F6"
        assert anime.eye_color == "#4A90D9"
        assert anime.gender == "neutral"

    def test_custom_name(self):
        """Test custom character name."""
        anime = Anime(name="Sakura")
        assert anime.name == "Sakura"

    def test_custom_hair_style(self):
        """Test custom hair style."""
        for hair_style in ["flowing", "ponytail", "short", "spiky", "bob", "twintails", "none"]:
            anime = Anime(hair_style=hair_style)
            assert anime.hair_style == hair_style

    def test_custom_colors(self):
        """Test custom colors."""
        anime = Anime(
            hair_color="#FF0000",
            skin_color="#FFE0BD",
            outfit_color="#00FF00",
            eye_color="#0000FF",
        )
        assert anime.hair_color == "#FF0000"
        assert anime.skin_color == "#FFE0BD"
        assert anime.outfit_color == "#00FF00"
        assert anime.eye_color == "#0000FF"

    def test_gender_option(self):
        """Test gender option."""
        for gender in ["neutral", "masculine", "feminine"]:
            anime = Anime(gender=gender)
            assert anime.gender == gender

    def test_generates_points(self):
        """Test that anime generates outline points."""
        anime = Anime()
        assert len(anime._points) >= 32  # At least head points
        assert anime._points.shape[1] == 2  # Each point has x, y

    def test_facing_flips_points(self):
        """Test that facing left flips x coordinates."""
        anime_right = Anime(facing="right")
        anime_left = Anime(facing="left")

        # X coordinates should be flipped
        assert not np.allclose(anime_right._points[:, 0], anime_left._points[:, 0])
        # Y coordinates should be the same
        assert np.allclose(anime_right._points[:, 1], anime_left._points[:, 1])

    def test_custom_height(self):
        """Test custom height parameter."""
        anime = Anime(height=150)
        assert anime.character_height == 150.0
        data = anime.get_render_data()
        assert data["character_height"] == 150.0

    def test_get_render_data(self):
        """Test render data includes anime-specific fields."""
        anime = Anime()
        data = anime.get_render_data()
        assert data["style"] == "anime"
        assert "hair_style" in data
        assert data["hair_style"] == "flowing"
        assert "hair_color" in data
        assert data["hair_color"] == "#2D1B12"
        assert "skin_color" in data
        assert "outfit_color" in data
        assert "eye_color" in data
        assert "gender" in data
        assert "head_height_ratio" in data
        assert "shoulder_width_ratio" in data

    def test_set_expression(self):
        """Test setting expression."""
        anime = Anime()
        anime.set_expression("happy")
        assert anime._expression.name == "happy"
        assert anime._expression.mouth == "smile"

    def test_set_pose(self):
        """Test setting pose."""
        anime = Anime()
        anime.set_pose("walking")
        assert anime._pose.name == "walking"
        assert anime._pose.left_arm == 30

    def test_say_creates_bubble(self):
        """Test say method creates speech bubble."""
        anime = Anime().move_to((100, 100))
        bubble = anime.say("Hello!")
        assert bubble.text == "Hello!"
        assert bubble.bubble_type == "speech"

    def test_think_creates_bubble(self):
        """Test think method creates thought bubble."""
        anime = Anime().move_to((100, 100))
        bubble = anime.think("I wonder...")
        assert bubble.text == "I wonder..."
        assert bubble.bubble_type == "thought"

    def test_shout_creates_bubble(self):
        """Test shout method creates shout bubble."""
        anime = Anime().move_to((100, 100))
        bubble = anime.shout("YAMETE!")
        assert bubble.text == "YAMETE!"
        assert bubble.bubble_type == "shout"

    def test_whisper_creates_bubble(self):
        """Test whisper method creates whisper bubble."""
        anime = Anime().move_to((100, 100))
        bubble = anime.whisper("*psst*")
        assert bubble.text == "*psst*"
        assert bubble.bubble_type == "whisper"

    def test_all_poses(self):
        """Test anime with different poses."""
        poses = ["standing", "sitting", "walking", "running", "pointing",
                 "waving", "jumping", "dancing", "kneeling", "cheering", "thinking"]
        for pose_name in poses:
            anime = Anime(pose=pose_name)
            assert anime._pose.name == pose_name
            # Should still generate valid points
            assert len(anime._points) >= 32

    def test_all_expressions(self):
        """Test anime with different expressions."""
        expressions = ["neutral", "happy", "sad", "angry", "surprised",
                       "confused", "sleepy", "excited", "scared", "smirk", "crying"]
        for expr_name in expressions:
            anime = Anime(expression=expr_name)
            assert anime._expression.name == expr_name
            data = anime.get_render_data()
            assert data["expression"]["name"] == expr_name

    def test_default_fill_color_is_skin_color(self):
        """Test default fill color matches skin color."""
        anime = Anime()
        assert anime.fill_color == "#FFE0C4"  # Default peach skin tone

    def test_default_outline_color(self):
        """Test default outline color."""
        anime = Anime()
        assert anime.color == "#333333"

    def test_proportions(self):
        """Test anime character has natural proportions."""
        anime = Anime(height=100)
        data = anime.get_render_data()
        # Anime proportions: head is ~1/7 of height
        assert data["head_height_ratio"] == 0.14
        # Shoulders are wider than head
        assert data["shoulder_width_ratio"] > data["head_width_ratio"]


class TestSuperhero:
    """Tests for Superhero character class."""

    def test_default_init(self):
        """Test default initialization."""
        hero = Superhero()
        assert hero.name == "Superhero"
        assert hero.style == "superhero"
        assert hero.costume_primary == "#DC2626"
        assert hero.costume_secondary == "#1D4ED8"
        assert hero.skin_color == "#FBBF24"
        assert hero.cape is True
        assert hero.cape_color == "#DC2626"
        assert hero.mask == "domino"
        assert hero.emblem == "star"
        assert hero.emblem_color == "#FBBF24"
        assert hero.boots is True
        assert hero.gloves is True

    def test_custom_name(self):
        """Test custom character name."""
        hero = Superhero(name="Captain Amazing")
        assert hero.name == "Captain Amazing"

    def test_custom_costume_colors(self):
        """Test custom costume colors."""
        hero = Superhero(
            costume_primary="#00FF00",
            costume_secondary="#FF00FF",
        )
        assert hero.costume_primary == "#00FF00"
        assert hero.costume_secondary == "#FF00FF"

    def test_custom_skin_color(self):
        """Test custom skin color."""
        hero = Superhero(skin_color="#8B4513")
        assert hero.skin_color == "#8B4513"

    def test_cape_disabled(self):
        """Test disabling cape."""
        hero = Superhero(cape=False)
        assert hero.cape is False

    def test_custom_cape_color(self):
        """Test custom cape color."""
        hero = Superhero(cape_color="#000000")
        assert hero.cape_color == "#000000"

    def test_mask_options(self):
        """Test different mask options."""
        for mask_type in ["domino", "full", "cowl", "none"]:
            hero = Superhero(mask=mask_type)
            assert hero.mask == mask_type

    def test_emblem_options(self):
        """Test different emblem options."""
        for emblem_type in ["star", "diamond", "circle", "shield", "none"]:
            hero = Superhero(emblem=emblem_type)
            assert hero.emblem == emblem_type

    def test_custom_emblem_color(self):
        """Test custom emblem color."""
        hero = Superhero(emblem_color="#FFFFFF")
        assert hero.emblem_color == "#FFFFFF"

    def test_boots_option(self):
        """Test boots option."""
        hero_no_boots = Superhero(boots=False)
        assert hero_no_boots.boots is False

        hero_with_boots = Superhero(boots=True)
        assert hero_with_boots.boots is True

    def test_gloves_option(self):
        """Test gloves option."""
        hero_no_gloves = Superhero(gloves=False)
        assert hero_no_gloves.gloves is False

        hero_with_gloves = Superhero(gloves=True)
        assert hero_with_gloves.gloves is True

    def test_generates_points(self):
        """Test that superhero generates outline points."""
        hero = Superhero()
        assert len(hero._points) >= 24  # At least head points
        assert hero._points.shape[1] == 2  # Each point has x, y

    def test_generates_cape_points_when_enabled(self):
        """Test that superhero generates cape points when enabled."""
        hero_with_cape = Superhero(cape=True)
        hero_no_cape = Superhero(cape=False)
        # Hero with cape should have more points
        assert len(hero_with_cape._points) > len(hero_no_cape._points)

    def test_facing_flips_points(self):
        """Test that facing left flips x coordinates."""
        hero_right = Superhero(facing="right")
        hero_left = Superhero(facing="left")

        # X coordinates should be flipped
        assert not np.allclose(hero_right._points[:, 0], hero_left._points[:, 0])
        # Y coordinates should be the same
        assert np.allclose(hero_right._points[:, 1], hero_left._points[:, 1])

    def test_custom_height(self):
        """Test custom height parameter."""
        hero = Superhero(height=200)
        assert hero.character_height == 200.0
        data = hero.get_render_data()
        assert data["character_height"] == 200.0

    def test_get_render_data(self):
        """Test render data includes superhero-specific fields."""
        hero = Superhero()
        data = hero.get_render_data()
        assert data["style"] == "superhero"
        assert "costume_primary" in data
        assert data["costume_primary"] == "#DC2626"
        assert "costume_secondary" in data
        assert data["costume_secondary"] == "#1D4ED8"
        assert "skin_color" in data
        assert "cape" in data
        assert data["cape"] is True
        assert "cape_color" in data
        assert "mask" in data
        assert data["mask"] == "domino"
        assert "emblem" in data
        assert data["emblem"] == "star"
        assert "emblem_color" in data
        assert "boots" in data
        assert "gloves" in data
        assert "head_height_ratio" in data
        assert "shoulder_width_ratio" in data
        assert "waist_width_ratio" in data

    def test_set_expression(self):
        """Test setting expression."""
        hero = Superhero()
        hero.set_expression("happy")
        assert hero._expression.name == "happy"
        assert hero._expression.mouth == "smile"

    def test_set_pose(self):
        """Test setting pose."""
        hero = Superhero()
        hero.set_pose("cheering")
        assert hero._pose.name == "cheering"

    def test_say_creates_bubble(self):
        """Test say method creates speech bubble."""
        hero = Superhero().move_to((100, 100))
        bubble = hero.say("Fear not, citizen!")
        assert bubble.text == "Fear not, citizen!"
        assert bubble.bubble_type == "speech"

    def test_think_creates_bubble(self):
        """Test think method creates thought bubble."""
        hero = Superhero().move_to((100, 100))
        bubble = hero.think("I must save them...")
        assert bubble.text == "I must save them..."
        assert bubble.bubble_type == "thought"

    def test_shout_creates_bubble(self):
        """Test shout method creates shout bubble."""
        hero = Superhero().move_to((100, 100))
        bubble = hero.shout("STOP RIGHT THERE!")
        assert bubble.text == "STOP RIGHT THERE!"
        assert bubble.bubble_type == "shout"

    def test_whisper_creates_bubble(self):
        """Test whisper method creates whisper bubble."""
        hero = Superhero().move_to((100, 100))
        bubble = hero.whisper("*secret identity*")
        assert bubble.text == "*secret identity*"
        assert bubble.bubble_type == "whisper"

    def test_all_poses(self):
        """Test superhero with different poses."""
        poses = ["standing", "sitting", "walking", "running", "pointing",
                 "waving", "jumping", "dancing", "kneeling", "cheering", "thinking"]
        for pose_name in poses:
            hero = Superhero(pose=pose_name)
            assert hero._pose.name == pose_name
            # Should still generate valid points
            assert len(hero._points) >= 24

    def test_all_expressions(self):
        """Test superhero with different expressions."""
        expressions = ["neutral", "happy", "sad", "angry", "surprised",
                       "confused", "sleepy", "excited", "scared", "smirk", "crying"]
        for expr_name in expressions:
            hero = Superhero(expression=expr_name)
            assert hero._expression.name == expr_name
            data = hero.get_render_data()
            assert data["expression"]["name"] == expr_name

    def test_default_fill_color_is_skin_color(self):
        """Test default fill color matches skin color."""
        hero = Superhero()
        assert hero.fill_color == "#FBBF24"  # Default gold skin tone

    def test_default_outline_color(self):
        """Test default outline color."""
        hero = Superhero()
        assert hero.color == "#1F2937"  # Dark gray

    def test_heroic_proportions(self):
        """Test superhero has heroic proportions (V-taper)."""
        hero = Superhero(height=100)
        data = hero.get_render_data()
        # Heroic proportions: broad shoulders, narrow waist
        assert data["shoulder_width_ratio"] == 0.28
        assert data["waist_width_ratio"] == 0.14
        # Shoulders should be twice as wide as waist
        assert data["shoulder_width_ratio"] == 2 * data["waist_width_ratio"]

    def test_method_chaining(self):
        """Test method chaining works correctly."""
        hero = Superhero()
        result = hero.move_to((100, 100)).set_expression("angry").set_pose("pointing")
        assert result is hero
        assert np.allclose(hero.position, (100, 100))
        assert hero._expression.name == "angry"
        assert hero._pose.name == "pointing"

    def test_full_costume_customization(self):
        """Test full costume customization."""
        hero = Superhero(
            name="Dark Knight",
            costume_primary="#1A1A1A",
            costume_secondary="#2D2D2D",
            skin_color="#FFE4C4",
            cape=True,
            cape_color="#1A1A1A",
            mask="cowl",
            emblem="shield",
            emblem_color="#FBBF24",
            boots=True,
            gloves=True,
        )
        assert hero.costume_primary == "#1A1A1A"
        assert hero.costume_secondary == "#2D2D2D"
        assert hero.mask == "cowl"
        assert hero.emblem == "shield"
        data = hero.get_render_data()
        assert data["costume_primary"] == "#1A1A1A"
        assert data["mask"] == "cowl"
        assert data["emblem"] == "shield"


class TestCartoon:
    """Tests for Cartoon character class."""

    def test_default_init(self):
        """Test default initialization."""
        cartoon = Cartoon()
        assert cartoon.name == "Cartoon"
        assert cartoon.style == "cartoon"
        assert cartoon.body_shape == "pear"
        assert cartoon.skin_color == "#FFDAB9"
        assert cartoon.outline_color == "#000000"
        assert cartoon.outfit_color == "#4169E1"
        assert cartoon.hair_color == "#8B4513"
        assert cartoon.nose_type == "round"
        assert cartoon.ear_size == "normal"
        assert cartoon.gloves is True

    def test_custom_name(self):
        """Test custom character name."""
        cartoon = Cartoon(name="ToonBoy")
        assert cartoon.name == "ToonBoy"

    def test_body_shapes(self):
        """Test different body shapes."""
        for body_shape in ["pear", "bean", "round"]:
            cartoon = Cartoon(body_shape=body_shape)
            assert cartoon.body_shape == body_shape
            data = cartoon.get_render_data()
            assert data["body_shape"] == body_shape

    def test_custom_colors(self):
        """Test custom colors."""
        cartoon = Cartoon(
            skin_color="#FFD700",
            outline_color="#333333",
            outfit_color="#FF6347",
            hair_color="#000000",
        )
        assert cartoon.skin_color == "#FFD700"
        assert cartoon.outline_color == "#333333"
        assert cartoon.outfit_color == "#FF6347"
        assert cartoon.hair_color == "#000000"

    def test_nose_options(self):
        """Test different nose options."""
        for nose_type in ["round", "triangle", "long"]:
            cartoon = Cartoon(nose_type=nose_type)
            assert cartoon.nose_type == nose_type

    def test_ear_size_options(self):
        """Test different ear size options."""
        for ear_size in ["small", "normal", "large"]:
            cartoon = Cartoon(ear_size=ear_size)
            assert cartoon.ear_size == ear_size

    def test_gloves_option(self):
        """Test gloves option."""
        cartoon_with_gloves = Cartoon(gloves=True)
        assert cartoon_with_gloves.gloves is True

        cartoon_no_gloves = Cartoon(gloves=False)
        assert cartoon_no_gloves.gloves is False

    def test_generates_points(self):
        """Test that cartoon generates outline points."""
        cartoon = Cartoon()
        # Should have: head(32) + body(20) + arms(26) + legs(22) = 100 points
        assert len(cartoon._points) >= 32
        assert cartoon._points.shape[1] == 2  # Each point has x, y

    def test_facing_flips_points(self):
        """Test that facing left flips x coordinates."""
        cartoon_right = Cartoon(facing="right")
        cartoon_left = Cartoon(facing="left")

        # X coordinates should be flipped
        assert not np.allclose(cartoon_right._points[:, 0], cartoon_left._points[:, 0])
        # Y coordinates should be the same
        assert np.allclose(cartoon_right._points[:, 1], cartoon_left._points[:, 1])

    def test_custom_height(self):
        """Test custom height parameter."""
        cartoon = Cartoon(height=150)
        assert cartoon.character_height == 150.0
        data = cartoon.get_render_data()
        assert data["character_height"] == 150.0

    def test_get_render_data(self):
        """Test render data includes cartoon-specific fields."""
        cartoon = Cartoon()
        data = cartoon.get_render_data()
        assert data["style"] == "cartoon"
        assert "body_shape" in data
        assert data["body_shape"] == "pear"
        assert "skin_color" in data
        assert data["skin_color"] == "#FFDAB9"
        assert "outline_color" in data
        assert "outfit_color" in data
        assert "hair_color" in data
        assert "nose_type" in data
        assert "ear_size" in data
        assert "gloves" in data
        assert data["gloves"] is True
        assert "head_radius_ratio" in data
        assert "body_height_ratio" in data
        assert "hand_size" in data

    def test_set_expression(self):
        """Test setting expression."""
        cartoon = Cartoon()
        cartoon.set_expression("happy")
        assert cartoon._expression.name == "happy"
        assert cartoon._expression.mouth == "smile"

    def test_set_pose(self):
        """Test setting pose."""
        cartoon = Cartoon()
        cartoon.set_pose("waving")
        assert cartoon._pose.name == "waving"

    def test_say_creates_bubble(self):
        """Test say method creates speech bubble."""
        cartoon = Cartoon().move_to((100, 100))
        bubble = cartoon.say("Zoinks!")
        assert bubble.text == "Zoinks!"
        assert bubble.bubble_type == "speech"

    def test_think_creates_bubble(self):
        """Test think method creates thought bubble."""
        cartoon = Cartoon().move_to((100, 100))
        bubble = cartoon.think("Hmm...")
        assert bubble.text == "Hmm..."
        assert bubble.bubble_type == "thought"

    def test_shout_creates_bubble(self):
        """Test shout method creates shout bubble."""
        cartoon = Cartoon().move_to((100, 100))
        bubble = cartoon.shout("BONK!")
        assert bubble.text == "BONK!"
        assert bubble.bubble_type == "shout"

    def test_whisper_creates_bubble(self):
        """Test whisper method creates whisper bubble."""
        cartoon = Cartoon().move_to((100, 100))
        bubble = cartoon.whisper("*psst*")
        assert bubble.text == "*psst*"
        assert bubble.bubble_type == "whisper"

    def test_all_poses(self):
        """Test cartoon with different poses."""
        poses = ["standing", "sitting", "walking", "running", "pointing",
                 "waving", "jumping", "dancing", "kneeling", "cheering", "thinking"]
        for pose_name in poses:
            cartoon = Cartoon(pose=pose_name)
            assert cartoon._pose.name == pose_name
            # Should still generate valid points
            assert len(cartoon._points) >= 32

    def test_all_expressions(self):
        """Test cartoon with different expressions."""
        expressions = ["neutral", "happy", "sad", "angry", "surprised",
                       "confused", "sleepy", "excited", "scared", "smirk", "crying"]
        for expr_name in expressions:
            cartoon = Cartoon(expression=expr_name)
            assert cartoon._expression.name == expr_name
            data = cartoon.get_render_data()
            assert data["expression"]["name"] == expr_name

    def test_default_fill_color_is_skin_color(self):
        """Test default fill color matches skin color."""
        cartoon = Cartoon()
        assert cartoon.fill_color == "#FFDAB9"  # Default peach puff

    def test_default_outline_color(self):
        """Test default outline color."""
        cartoon = Cartoon()
        assert cartoon.color == "#000000"  # Black

    def test_cartoon_proportions(self):
        """Test cartoon character has correct proportions."""
        cartoon = Cartoon(height=100)
        data = cartoon.get_render_data()
        # Large head for cartoon style (35% diameter = 0.175 radius ratio)
        assert data["head_radius_ratio"] == 0.175
        # Shorter limbs for cartoon style
        assert data["arm_length_ratio"] == 0.20
        assert data["leg_length_ratio"] == 0.18

    def test_method_chaining(self):
        """Test method chaining works correctly."""
        cartoon = Cartoon()
        result = cartoon.move_to((100, 100)).set_expression("happy").set_pose("waving")
        assert result is cartoon
        assert np.allclose(cartoon.position, (100, 100))
        assert cartoon._expression.name == "happy"
        assert cartoon._pose.name == "waving"

    def test_full_customization(self):
        """Test full customization."""
        cartoon = Cartoon(
            name="MickeyLike",
            body_shape="round",
            skin_color="#FFE4B5",
            outline_color="#000000",
            outfit_color="#FF0000",
            hair_color="#000000",
            nose_type="round",
            ear_size="large",
            gloves=True,
        )
        assert cartoon.body_shape == "round"
        assert cartoon.outfit_color == "#FF0000"
        assert cartoon.ear_size == "large"
        data = cartoon.get_render_data()
        assert data["body_shape"] == "round"
        assert data["outfit_color"] == "#FF0000"
        assert data["ear_size"] == "large"
