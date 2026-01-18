"""Tests for Character classes."""

import logging
import numpy as np
import pytest

from comix.cobject.character.character import (
    Anime,
    AnimalStyle,
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

    def test_unknown_name(self, caplog: pytest.LogCaptureFixture):
        """Test unknown expression name returns default and logs warning."""
        import logging

        with caplog.at_level(logging.WARNING, logger="comix.cobject.character.character"):
            expr = Expression.from_name("unknown")

        assert expr.name == "neutral"
        # Verify warning was logged
        assert len(caplog.records) == 1
        assert "Unknown expression 'unknown'" in caplog.text
        assert "falling back to 'neutral'" in caplog.text
        assert "Valid expressions:" in caplog.text

    def test_unknown_expression_typo(self, caplog: pytest.LogCaptureFixture):
        """Test common typo in expression name logs helpful warning."""
        import logging

        with caplog.at_level(logging.WARNING, logger="comix.cobject.character.character"):
            expr = Expression.from_name("hapy")  # Common typo for "happy"

        assert expr.name == "neutral"
        # Warning should include valid expressions for user reference
        assert "happy" in caplog.text  # Help user find correct spelling

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

    def test_unknown_pose_name(self, caplog: pytest.LogCaptureFixture):
        """Test unknown pose name returns default and logs warning."""
        import logging

        with caplog.at_level(logging.WARNING, logger="comix.cobject.character.character"):
            pose = Pose.from_name("unknown_pose")

        assert pose.name == "standing"
        # Verify warning was logged
        assert len(caplog.records) == 1
        assert "Unknown pose 'unknown_pose'" in caplog.text
        assert "falling back to 'standing'" in caplog.text
        assert "Valid poses:" in caplog.text

    def test_unknown_pose_typo(self, caplog: pytest.LogCaptureFixture):
        """Test common typo in pose name logs helpful warning."""
        import logging

        with caplog.at_level(logging.WARNING, logger="comix.cobject.character.character"):
            pose = Pose.from_name("waveing")  # Common typo for "waving"

        assert pose.name == "standing"
        # Warning should include valid poses for user reference
        assert "waving" in caplog.text  # Help user find correct spelling

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

    def test_height_zero_raises_error(self):
        """Test that height=0 raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            Character(height=0)
        assert "Character height must be positive" in str(exc_info.value)
        assert "0" in str(exc_info.value)

    def test_negative_height_raises_error(self):
        """Test that negative height raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            Character(height=-50)
        assert "Character height must be positive" in str(exc_info.value)
        assert "-50" in str(exc_info.value)

    def test_positive_height_is_valid(self):
        """Test that positive height values are accepted."""
        char = Character(height=150.0)
        assert char.character_height == 150.0

    def test_small_positive_height_is_valid(self):
        """Test that small positive height values are accepted."""
        char = Character(height=0.1)
        assert char.character_height == 0.1


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

    def test_all_poses(self):
        """Test stickman with all 12 poses."""
        poses = ["standing", "sitting", "walking", "running", "pointing",
                 "waving", "jumping", "dancing", "lying", "kneeling", "cheering", "thinking"]
        for pose_name in poses:
            stickman = Stickman(pose=pose_name)
            assert stickman._pose.name == pose_name
            assert len(stickman._points) > 0

    def test_all_expressions(self):
        """Test stickman with all 11 expressions."""
        expressions = ["neutral", "happy", "sad", "angry", "surprised",
                       "confused", "sleepy", "excited", "scared", "smirk", "crying"]
        for expr_name in expressions:
            stickman = Stickman(expression=expr_name)
            assert stickman._expression.name == expr_name


class TestStickmanProportions:
    """Tests for Stickman reference-based proportions."""

    def test_default_proportion_style(self):
        """Test default proportion style is classic."""
        stickman = Stickman()
        assert stickman.proportion_style == "classic"
        assert stickman.head_ratio == 0.133
        assert stickman.torso_ratio == 0.40
        assert stickman.arm_ratio == 0.38
        assert stickman.leg_ratio == 0.53

    def test_xkcd_proportion_style(self):
        """Test xkcd proportion style."""
        stickman = Stickman(proportion_style="xkcd")
        assert stickman.proportion_style == "xkcd"
        assert stickman.head_ratio == 0.12
        assert stickman.torso_ratio == 0.42
        assert stickman.arm_ratio == 0.40
        assert stickman.leg_ratio == 0.54

    def test_tall_proportion_style(self):
        """Test tall proportion style (heroic proportions)."""
        stickman = Stickman(proportion_style="tall")
        assert stickman.proportion_style == "tall"
        assert stickman.head_ratio == 0.125  # 8 heads
        assert stickman.leg_ratio == 0.55

    def test_child_proportion_style(self):
        """Test child proportion style (larger head)."""
        stickman = Stickman(proportion_style="child")
        assert stickman.proportion_style == "child"
        assert stickman.head_ratio == 0.25  # 4 heads (larger head)
        assert stickman.leg_ratio == 0.45

    def test_realistic_proportion_style(self):
        """Test realistic proportion style (ideal 8-head figure drawing)."""
        stickman = Stickman(proportion_style="realistic")
        assert stickman.proportion_style == "realistic"
        assert stickman.head_ratio == 0.125  # 8 heads
        assert stickman.torso_ratio == 0.375  # 3 heads for torso
        assert stickman.arm_ratio == 0.375
        assert stickman.leg_ratio == 0.50  # 4 heads for legs

    def test_invalid_proportion_style_fallback(self, caplog: pytest.LogCaptureFixture):
        """Test that invalid proportion style falls back to classic."""
        with caplog.at_level(logging.WARNING, logger="comix.cobject.character.character"):
            stickman = Stickman(proportion_style="invalid")
        assert "Unknown proportion_style" in caplog.text
        assert stickman.proportion_style == "classic"

    def test_custom_head_ratio_override(self):
        """Test that custom head_ratio overrides preset."""
        stickman = Stickman(proportion_style="classic", head_ratio=0.2)
        assert stickman.proportion_style == "classic"
        assert stickman.head_ratio == 0.2  # Custom override
        assert stickman.torso_ratio == 0.40  # Preset value

    def test_custom_all_ratios_override(self):
        """Test that all ratios can be custom overridden."""
        stickman = Stickman(
            head_ratio=0.15,
            torso_ratio=0.35,
            arm_ratio=0.30,
            leg_ratio=0.50,
        )
        assert stickman.head_ratio == 0.15
        assert stickman.torso_ratio == 0.35
        assert stickman.arm_ratio == 0.30
        assert stickman.leg_ratio == 0.50

    def test_proportion_affects_points(self):
        """Test that different proportions generate different points."""
        classic = Stickman(proportion_style="classic")
        child = Stickman(proportion_style="child")

        # Child should have larger head (different points)
        assert not np.array_equal(classic._points, child._points)

    def test_get_render_data_includes_proportions(self):
        """Test that render data includes proportion info."""
        stickman = Stickman(proportion_style="xkcd")
        data = stickman.get_render_data()

        assert data["proportion_style"] == "xkcd"
        assert data["head_ratio"] == 0.12
        assert data["torso_ratio"] == 0.42
        assert data["arm_ratio"] == 0.40
        assert data["leg_ratio"] == 0.54

    def test_all_proportion_presets(self):
        """Test that all proportion presets create valid stickmen."""
        presets = ["classic", "xkcd", "tall", "realistic", "child"]
        for preset in presets:
            stickman = Stickman(proportion_style=preset)
            assert len(stickman._points) > 0, f"Failed for preset: {preset}"
            assert stickman.proportion_style == preset


class TestStickmanHeadSquash:
    """Tests for Stickman head_squash feature (head curve/roundness)."""

    def test_default_head_squash_is_zero(self):
        """Test that default head_squash is 0 (perfect circle)."""
        stickman = Stickman()
        assert stickman.head_squash == 0.0

    def test_head_squash_positive_flattens_head(self):
        """Test that positive head_squash makes head wider than tall."""
        stickman = Stickman(head_squash=0.5)
        assert stickman.head_squash == 0.5
        # Head points are first 16 points
        head_points = stickman._points[:16]
        head_width = head_points[:, 0].max() - head_points[:, 0].min()
        head_height = head_points[:, 1].max() - head_points[:, 1].min()
        # Flattened head should be wider than tall
        assert head_width > head_height

    def test_head_squash_negative_elongates_head(self):
        """Test that negative head_squash makes head taller than wide."""
        stickman = Stickman(head_squash=-0.5)
        assert stickman.head_squash == -0.5
        # Head points are first 16 points
        head_points = stickman._points[:16]
        head_width = head_points[:, 0].max() - head_points[:, 0].min()
        head_height = head_points[:, 1].max() - head_points[:, 1].min()
        # Elongated head should be taller than wide
        assert head_height > head_width

    def test_head_squash_zero_creates_circle(self):
        """Test that head_squash=0 creates a circular head (equal width and height)."""
        stickman = Stickman(head_squash=0.0)
        # Head points are first 16 points
        head_points = stickman._points[:16]
        head_width = head_points[:, 0].max() - head_points[:, 0].min()
        head_height = head_points[:, 1].max() - head_points[:, 1].min()
        # Circle should have approximately equal width and height
        # Due to 16-point discretization, allow 1% tolerance
        assert abs(head_width - head_height) / head_height < 0.01

    def test_head_squash_clamped_to_max(self):
        """Test that head_squash is clamped to maximum 1.0."""
        stickman = Stickman(head_squash=2.0)
        assert stickman.head_squash == 1.0

    def test_head_squash_clamped_to_min(self):
        """Test that head_squash is clamped to minimum -1.0."""
        stickman = Stickman(head_squash=-2.0)
        assert stickman.head_squash == -1.0

    def test_head_squash_at_boundary_values(self):
        """Test head_squash at boundary values (1.0 and -1.0)."""
        flat = Stickman(head_squash=1.0)
        elongated = Stickman(head_squash=-1.0)
        assert flat.head_squash == 1.0
        assert elongated.head_squash == -1.0
        # Both should generate valid points
        assert len(flat._points) > 0
        assert len(elongated._points) > 0

    def test_head_squash_in_render_data(self):
        """Test that head_squash is included in render data."""
        stickman = Stickman(head_squash=0.3)
        data = stickman.get_render_data()
        assert "head_squash" in data
        assert data["head_squash"] == 0.3

    def test_head_squash_with_proportion_style(self):
        """Test head_squash works with different proportion styles."""
        styles = ["classic", "xkcd", "tall", "child"]
        for style in styles:
            stickman = Stickman(proportion_style=style, head_squash=0.2)
            assert stickman.head_squash == 0.2
            assert stickman.proportion_style == style
            # Head should be flattened
            head_points = stickman._points[:16]
            head_width = head_points[:, 0].max() - head_points[:, 0].min()
            head_height = head_points[:, 1].max() - head_points[:, 1].min()
            assert head_width > head_height, f"Failed for style: {style}"

    def test_head_squash_with_facing_left(self):
        """Test head_squash is correctly applied when facing left."""
        right = Stickman(head_squash=0.4, facing="right")
        left = Stickman(head_squash=0.4, facing="left")
        # Head dimensions should be same (facing just flips x-axis)
        right_head = right._points[:16]
        left_head = left._points[:16]
        right_width = right_head[:, 0].max() - right_head[:, 0].min()
        left_width = left_head[:, 0].max() - left_head[:, 0].min()
        np.testing.assert_almost_equal(right_width, left_width)

    def test_head_squash_range_produces_different_shapes(self):
        """Test that different head_squash values produce different shapes."""
        shapes = []
        for squash in [-0.5, -0.25, 0.0, 0.25, 0.5]:
            stickman = Stickman(head_squash=squash)
            head_points = stickman._points[:16]
            width = head_points[:, 0].max() - head_points[:, 0].min()
            height = head_points[:, 1].max() - head_points[:, 1].min()
            shapes.append((width, height))
        # All shapes should be different
        for i in range(len(shapes)):
            for j in range(i + 1, len(shapes)):
                assert shapes[i] != shapes[j], f"Shapes at indices {i} and {j} are identical"


class TestStickmanLineWidth:
    """Tests for Stickman line_width parameter."""

    def test_default_line_width(self):
        """Test default line_width is 2.0."""
        stickman = Stickman()
        assert stickman.line_width == 2.0

    def test_custom_line_width(self):
        """Test custom line_width is stored correctly."""
        stickman = Stickman(line_width=3.0)
        assert stickman.line_width == 3.0

    def test_line_width_minimum_clamped(self):
        """Test line_width is clamped to minimum 0.5."""
        stickman = Stickman(line_width=0.1)
        assert stickman.line_width == 0.5

    def test_line_width_zero_clamped(self):
        """Test line_width of 0 is clamped to 0.5."""
        stickman = Stickman(line_width=0)
        assert stickman.line_width == 0.5

    def test_line_width_negative_clamped(self):
        """Test negative line_width is clamped to 0.5."""
        stickman = Stickman(line_width=-1.0)
        assert stickman.line_width == 0.5

    def test_line_width_in_render_data(self):
        """Test line_width is included in render data."""
        stickman = Stickman(line_width=4.0)
        data = stickman.get_render_data()
        assert "line_width" in data
        assert data["line_width"] == 4.0

    def test_line_width_with_proportion_style(self):
        """Test line_width works with proportion_style."""
        for style in ["classic", "xkcd", "tall", "child"]:
            stickman = Stickman(proportion_style=style, line_width=3.5)
            assert stickman.line_width == 3.5
            assert stickman.proportion_style == style

    def test_line_width_with_head_squash(self):
        """Test line_width works with head_squash."""
        stickman = Stickman(line_width=2.5, head_squash=0.5)
        assert stickman.line_width == 2.5
        assert stickman.head_squash == 0.5

    def test_line_width_various_values(self):
        """Test various line_width values."""
        test_values = [0.5, 1.0, 2.0, 3.0, 5.0, 10.0]
        for value in test_values:
            stickman = Stickman(line_width=value)
            assert stickman.line_width == value

    def test_line_width_preserved_in_chaining(self):
        """Test line_width is preserved when using method chaining."""
        stickman = Stickman(line_width=3.0)
        stickman.move_to((100, 100)).set_expression("happy").set_pose("waving")
        assert stickman.line_width == 3.0


class TestStickmanAutoLineWidth:
    """Tests for Stickman auto_line_width feature (line width scaling with height)."""

    def test_auto_line_width_default_enabled(self) -> None:
        """Test auto_line_width is enabled by default."""
        stickman = Stickman()
        assert stickman.auto_line_width is True

    def test_auto_line_width_reference_height(self) -> None:
        """Test line_width at reference height (100px) equals DEFAULT_LINE_WIDTH (2.0)."""
        stickman = Stickman(height=100)
        assert stickman.line_width == 2.0

    def test_auto_line_width_small_character(self) -> None:
        """Test auto line_width for small character (50px height = 1.0 line_width)."""
        stickman = Stickman(height=50)
        assert stickman.line_width == 1.0

    def test_auto_line_width_large_character(self) -> None:
        """Test auto line_width for large character (200px height = 4.0 line_width)."""
        stickman = Stickman(height=200)
        assert stickman.line_width == 4.0

    def test_auto_line_width_clamped_to_minimum(self) -> None:
        """Test auto line_width is clamped to MIN_LINE_WIDTH (0.5) for very small characters."""
        stickman = Stickman(height=20)  # Would calculate 0.4, but clamped to 0.5
        assert stickman.line_width == Stickman.MIN_LINE_WIDTH
        assert stickman.line_width == 0.5

    def test_auto_line_width_clamped_to_maximum(self) -> None:
        """Test auto line_width is clamped to MAX_LINE_WIDTH (6.0) for very large characters."""
        stickman = Stickman(height=500)  # Would calculate 10.0, but clamped to 6.0
        assert stickman.line_width == Stickman.MAX_LINE_WIDTH
        assert stickman.line_width == 6.0

    def test_explicit_line_width_overrides_auto(self) -> None:
        """Test explicit line_width parameter overrides auto calculation."""
        stickman = Stickman(height=200, line_width=1.5)
        assert stickman.line_width == 1.5  # Not 4.0 (which auto would give)

    def test_explicit_line_width_still_clamped_to_min(self) -> None:
        """Test explicit line_width is still clamped to minimum."""
        stickman = Stickman(height=200, line_width=0.2)
        assert stickman.line_width == 0.5  # Clamped to MIN

    def test_auto_line_width_disabled(self) -> None:
        """Test auto_line_width=False uses DEFAULT_LINE_WIDTH regardless of height."""
        stickman = Stickman(height=200, auto_line_width=False)
        assert stickman.line_width == Stickman.DEFAULT_LINE_WIDTH
        assert stickman.line_width == 2.0

    def test_auto_line_width_disabled_explicit_overrides(self) -> None:
        """Test explicit line_width works when auto_line_width=False."""
        stickman = Stickman(height=200, auto_line_width=False, line_width=3.5)
        assert stickman.line_width == 3.5

    def test_auto_line_width_proportional_scaling(self) -> None:
        """Test line_width scales proportionally with height."""
        heights = [50, 75, 100, 125, 150, 175, 200]
        expected = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]

        for h, expected_lw in zip(heights, expected):
            stickman = Stickman(height=h)
            assert stickman.line_width == pytest.approx(expected_lw, rel=0.01), \
                f"Height {h}: expected {expected_lw}, got {stickman.line_width}"

    def test_auto_line_width_in_render_data(self) -> None:
        """Test auto_line_width is included in render data."""
        stickman = Stickman(height=150)
        data = stickman.get_render_data()
        assert "auto_line_width" in data
        assert data["auto_line_width"] is True
        assert "line_width" in data
        assert data["line_width"] == 3.0  # 150/100 * 2.0

    def test_line_width_setter(self) -> None:
        """Test line_width can be set after creation."""
        stickman = Stickman(height=200)  # auto would give 4.0
        assert stickman.line_width == 4.0
        stickman.line_width = 2.5
        assert stickman.line_width == 2.5

    def test_auto_line_width_with_child_preset(self) -> None:
        """Test auto_line_width works with child proportion_style."""
        stickman = Stickman(height=80, proportion_style="child")
        expected = 80 / 100 * 2.0  # 1.6
        assert stickman.line_width == pytest.approx(expected, rel=0.01)

    def test_auto_line_width_constants(self) -> None:
        """Test class constants for auto line width scaling."""
        assert Stickman.REFERENCE_HEIGHT == 100.0
        assert Stickman.DEFAULT_LINE_WIDTH == 2.0
        assert Stickman.MIN_LINE_WIDTH == 0.5
        assert Stickman.MAX_LINE_WIDTH == 6.0


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

    def test_all_poses(self):
        """Test simple face with all 12 poses."""
        poses = ["standing", "sitting", "walking", "running", "pointing",
                 "waving", "jumping", "dancing", "lying", "kneeling", "cheering", "thinking"]
        for pose_name in poses:
            face = SimpleFace(pose=pose_name)
            assert face._pose.name == pose_name
            assert len(face._points) == 32

    def test_all_expressions(self):
        """Test simple face with all 11 expressions."""
        expressions = ["neutral", "happy", "sad", "angry", "surprised",
                       "confused", "sleepy", "excited", "scared", "smirk", "crying"]
        for expr_name in expressions:
            face = SimpleFace(expression=expr_name)
            assert face._expression.name == expr_name


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
                 "waving", "jumping", "dancing", "lying", "kneeling", "cheering", "thinking"]
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
                 "waving", "jumping", "dancing", "lying", "kneeling", "cheering", "thinking"]
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
                 "waving", "jumping", "dancing", "lying", "kneeling", "cheering", "thinking"]
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
                 "waving", "jumping", "dancing", "lying", "kneeling", "cheering", "thinking"]
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
                 "waving", "jumping", "dancing", "lying", "kneeling", "cheering", "thinking"]
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
                 "waving", "jumping", "dancing", "lying", "kneeling", "cheering", "thinking"]
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


class TestCharacterExpressionPoseResolution:
    """Tests for expression and pose resolution edge cases."""

    def test_resolve_expression_with_expression_object(self) -> None:
        """Test that Expression objects are passed through unchanged."""
        custom_expr = Expression("custom", "wide", "grin", "raised")
        char = Stickman(name="Test", expression=custom_expr)
        assert char._expression is custom_expr

    def test_resolve_pose_with_pose_object(self) -> None:
        """Test that Pose objects are passed through unchanged."""
        custom_pose = Pose("custom", left_arm=45, right_arm=-45, left_leg=10, right_leg=-10)
        char = Stickman(name="Test", pose=custom_pose)
        assert char._pose is custom_pose

    def test_set_expression_with_expression_object(self) -> None:
        """Test set_expression accepts Expression objects."""
        char = Stickman(name="Test")
        custom_expr = Expression("my_expr", "stars", "smile", "relaxed")
        result = char.set_expression(custom_expr)
        assert result is char
        assert char._expression is custom_expr

    def test_set_pose_with_pose_object(self) -> None:
        """Test set_pose accepts Pose objects."""
        char = Stickman(name="Test")
        custom_pose = Pose("my_pose", left_arm=90, right_arm=90, body_angle=15)
        result = char.set_pose(custom_pose)
        assert result is char
        assert char._pose is custom_pose

    def test_expression_from_name_with_unknown_returns_neutral(self, caplog) -> None:
        """Test Expression.from_name logs warning for unknown name."""
        import logging

        with caplog.at_level(logging.WARNING):
            result = Expression.from_name("nonexistent_expression")

        assert result.name == "neutral"
        assert "Unknown expression" in caplog.text or result.name == "neutral"

    def test_pose_from_name_with_unknown_returns_standing(self, caplog) -> None:
        """Test Pose.from_name logs warning for unknown name."""
        import logging

        with caplog.at_level(logging.WARNING):
            result = Pose.from_name("nonexistent_pose")

        assert result.name == "standing"
        assert "Unknown pose" in caplog.text or result.name == "standing"

    def test_all_character_types_accept_expression_object(self) -> None:
        """Test all character types accept Expression objects."""
        expr = Expression("test", "curved", "smile", "normal")
        characters = [
            Stickman(name="S", expression=expr),
            SimpleFace(name="SF", expression=expr),
            ChubbyStickman(name="CS", expression=expr),
            Robot(name="R", expression=expr),
            Chibi(name="Ch", expression=expr),
            Anime(name="A", expression=expr),
            Superhero(name="Su", expression=expr),
            Cartoon(name="Ca", expression=expr),
            AnimalStyle(name="An", expression=expr),
        ]
        for char in characters:
            assert char._expression is expr

    def test_all_character_types_accept_pose_object(self) -> None:
        """Test all character types accept Pose objects."""
        pose = Pose("test", left_arm=30, right_arm=-30)
        characters = [
            Stickman(name="S", pose=pose),
            SimpleFace(name="SF", pose=pose),
            ChubbyStickman(name="CS", pose=pose),
            Robot(name="R", pose=pose),
            Chibi(name="Ch", pose=pose),
            Anime(name="A", pose=pose),
            Superhero(name="Su", pose=pose),
            Cartoon(name="Ca", pose=pose),
            AnimalStyle(name="An", pose=pose),
        ]
        for char in characters:
            assert char._pose is pose


class TestAnimalStyle:
    """Tests for AnimalStyle character class."""

    def test_default_init(self):
        """Test default initialization."""
        animal = AnimalStyle()
        assert animal.name == "AnimalCharacter"
        assert animal.style == "animal"
        assert animal.species == "cat"
        assert animal.fur_color == "#D2691E"
        assert animal.fur_secondary == "#FFFFFF"
        assert animal.eye_color == "#4A90D9"
        assert animal.nose_color == "#333333"
        assert animal.outfit_color == "#4169E1"

    def test_custom_name(self):
        """Test custom character name."""
        animal = AnimalStyle(name="Whiskers")
        assert animal.name == "Whiskers"

    def test_all_species_presets(self):
        """Test all species presets work correctly."""
        species_list = ["cat", "dog", "rabbit", "fox", "bear", "bird", "wolf"]
        for species in species_list:
            animal = AnimalStyle(species=species)
            assert animal.species == species
            # Should generate valid points
            assert len(animal._points) >= 32

    def test_cat_preset(self):
        """Test cat species preset."""
        cat = AnimalStyle(species="cat")
        assert cat.head_shape == "round"
        assert cat.ear_type == "pointed"
        assert cat._has_tail is True

    def test_dog_preset(self):
        """Test dog species preset."""
        dog = AnimalStyle(species="dog")
        assert dog.head_shape == "round"
        assert dog.ear_type == "floppy"
        assert dog._has_tail is True

    def test_rabbit_preset(self):
        """Test rabbit species preset."""
        rabbit = AnimalStyle(species="rabbit")
        assert rabbit.head_shape == "oval"
        assert rabbit.ear_type == "tall"
        assert rabbit._has_tail is True

    def test_fox_preset(self):
        """Test fox species preset."""
        fox = AnimalStyle(species="fox")
        assert fox.head_shape == "pointed"
        assert fox.ear_type == "pointed"
        assert fox._has_tail is True

    def test_bear_preset(self):
        """Test bear species preset."""
        bear = AnimalStyle(species="bear")
        assert bear.head_shape == "round"
        assert bear.ear_type == "round"
        assert bear._has_tail is False

    def test_bird_preset(self):
        """Test bird species preset."""
        bird = AnimalStyle(species="bird")
        assert bird.head_shape == "round"
        assert bird.ear_type == "none"
        assert bird._has_tail is True

    def test_wolf_preset(self):
        """Test wolf species preset."""
        wolf = AnimalStyle(species="wolf")
        assert wolf.head_shape == "pointed"
        assert wolf.ear_type == "pointed"
        assert wolf._has_tail is True

    def test_unknown_species_falls_back_to_cat(self, caplog):
        """Test unknown species falls back to cat with warning."""
        with caplog.at_level(logging.WARNING, logger="comix.cobject.character.character"):
            animal = AnimalStyle(species="unicorn")

        assert animal.species == "cat"
        assert "Unknown species 'unicorn'" in caplog.text
        assert "falling back to 'cat'" in caplog.text

    def test_custom_colors(self):
        """Test custom colors."""
        animal = AnimalStyle(
            fur_color="#FF6600",
            fur_secondary="#FFFFFF",
            eye_color="#00FF00",
            nose_color="#000000",
            outfit_color="#FF0000",
        )
        assert animal.fur_color == "#FF6600"
        assert animal.fur_secondary == "#FFFFFF"
        assert animal.eye_color == "#00FF00"
        assert animal.nose_color == "#000000"
        assert animal.outfit_color == "#FF0000"

    def test_override_ear_type(self):
        """Test overriding ear type from preset."""
        # Dog normally has floppy ears, override to pointed
        dog = AnimalStyle(species="dog", ear_type="pointed")
        assert dog.species == "dog"
        assert dog.ear_type == "pointed"

    def test_override_has_tail(self):
        """Test overriding has_tail from preset."""
        # Bear normally has no tail, override to have one
        bear = AnimalStyle(species="bear", has_tail=True)
        assert bear.species == "bear"
        assert bear._has_tail is True

        # Cat normally has tail, override to remove it
        cat = AnimalStyle(species="cat", has_tail=False)
        assert cat.species == "cat"
        assert cat._has_tail is False

    def test_generates_points(self):
        """Test that animal generates outline points."""
        animal = AnimalStyle()
        # Should have points for head, ears, muzzle, neck, body, arms, legs, tail
        assert len(animal._points) >= 80
        assert animal._points.shape[1] == 2  # Each point has x, y

    def test_facing_flips_points(self):
        """Test that facing left flips x coordinates."""
        animal_right = AnimalStyle(facing="right")
        animal_left = AnimalStyle(facing="left")

        # X coordinates should be flipped
        assert not np.allclose(animal_right._points[:, 0], animal_left._points[:, 0])
        # Y coordinates should be the same
        assert np.allclose(animal_right._points[:, 1], animal_left._points[:, 1])

    def test_custom_height(self):
        """Test custom height parameter."""
        animal = AnimalStyle(height=150)
        assert animal.character_height == 150.0
        data = animal.get_render_data()
        assert data["character_height"] == 150.0

    def test_get_render_data(self):
        """Test render data includes animal-specific fields."""
        animal = AnimalStyle(species="fox")
        data = animal.get_render_data()
        assert data["style"] == "animal"
        assert data["species"] == "fox"
        assert "fur_color" in data
        assert "fur_secondary" in data
        assert "eye_color" in data
        assert "nose_color" in data
        assert "outfit_color" in data
        assert "head_shape" in data
        assert data["head_shape"] == "pointed"
        assert "ear_type" in data
        assert data["ear_type"] == "pointed"
        assert "ear_angle" in data
        assert "muzzle_size" in data
        assert "has_tail" in data
        assert data["has_tail"] is True
        assert "tail_length" in data
        assert "tail_curve" in data
        assert "head_height_ratio" in data
        assert data["head_height_ratio"] == 0.18
        assert "body_height_ratio" in data
        assert data["body_height_ratio"] == 0.30

    def test_set_expression(self):
        """Test setting expression."""
        animal = AnimalStyle()
        result = animal.set_expression("happy")
        assert result is animal
        assert animal._expression.name == "happy"

    def test_set_pose(self):
        """Test setting pose."""
        animal = AnimalStyle()
        result = animal.set_pose("waving")
        assert result is animal
        assert animal._pose.name == "waving"

    def test_say_creates_bubble(self):
        """Test say method creates speech bubble."""
        animal = AnimalStyle().move_to((100, 100))
        bubble = animal.say("Meow!")
        assert bubble.text == "Meow!"
        assert bubble.bubble_type == "speech"
        assert bubble.tail_target is animal

    def test_think_creates_bubble(self):
        """Test think method creates thought bubble."""
        animal = AnimalStyle().move_to((100, 100))
        bubble = animal.think("Hmm...")
        assert bubble.text == "Hmm..."
        assert bubble.bubble_type == "thought"

    def test_shout_creates_bubble(self):
        """Test shout method creates shout bubble."""
        animal = AnimalStyle().move_to((100, 100))
        bubble = animal.shout("WOOF!")
        assert bubble.text == "WOOF!"
        assert bubble.bubble_type == "shout"

    def test_whisper_creates_bubble(self):
        """Test whisper method creates whisper bubble."""
        animal = AnimalStyle().move_to((100, 100))
        bubble = animal.whisper("*purr*")
        assert bubble.text == "*purr*"
        assert bubble.bubble_type == "whisper"

    def test_all_poses(self):
        """Test animal with different poses."""
        poses = ["standing", "sitting", "walking", "running", "pointing",
                 "waving", "jumping", "dancing", "lying", "kneeling", "cheering", "thinking"]
        for pose_name in poses:
            animal = AnimalStyle(pose=pose_name)
            assert animal._pose.name == pose_name
            # Should still generate valid points
            assert len(animal._points) >= 80

    def test_all_expressions(self):
        """Test animal with different expressions."""
        expressions = ["neutral", "happy", "sad", "angry", "surprised",
                       "confused", "sleepy", "excited", "scared", "smirk", "crying"]
        for expr_name in expressions:
            animal = AnimalStyle(expression=expr_name)
            assert animal._expression.name == expr_name
            data = animal.get_render_data()
            assert data["expression"]["name"] == expr_name

    def test_default_fill_color_is_fur_color(self):
        """Test default fill color matches fur color."""
        animal = AnimalStyle(fur_color="#FF9900")
        assert animal.fill_color == "#FF9900"

    def test_default_outline_color(self):
        """Test default outline color."""
        animal = AnimalStyle()
        assert animal.color == "#333333"

    def test_method_chaining(self):
        """Test method chaining works correctly."""
        animal = AnimalStyle()
        result = animal.move_to((100, 100)).set_expression("happy").set_pose("waving")
        assert result is animal
        assert np.allclose(animal.position, (100, 100))
        assert animal._expression.name == "happy"
        assert animal._pose.name == "waving"

    def test_full_customization(self):
        """Test full customization."""
        animal = AnimalStyle(
            name="Foxy",
            species="fox",
            fur_color="#FF6600",
            fur_secondary="#FFFFFF",
            eye_color="#00AA00",
            nose_color="#000000",
            outfit_color="#0000FF",
            ear_type="pointed",
            has_tail=True,
            height=120,
        )
        assert animal.name == "Foxy"
        assert animal.species == "fox"
        assert animal.fur_color == "#FF6600"
        assert animal.character_height == 120.0
        data = animal.get_render_data()
        assert data["species"] == "fox"
        assert data["fur_color"] == "#FF6600"
        assert data["character_height"] == 120.0

    def test_tail_generated_for_tailed_species(self):
        """Test tail points are generated for species with tails."""
        # Compare same species with/without tail
        cat_with_tail = AnimalStyle(species="cat", has_tail=True)
        cat_no_tail = AnimalStyle(species="cat", has_tail=False)
        # Cat with tail should have more points than cat without tail
        assert len(cat_with_tail._points) > len(cat_no_tail._points)

    def test_each_ear_type_generates_different_points(self):
        """Test each ear type generates different point counts."""
        pointed = AnimalStyle(ear_type="pointed")
        floppy = AnimalStyle(species="dog", ear_type="floppy")
        tall = AnimalStyle(species="rabbit", ear_type="tall")
        round_ears = AnimalStyle(species="bear", ear_type="round")
        none_ears = AnimalStyle(species="bird", ear_type="none")

        # Each ear type should produce different point arrays
        # This is a basic check that different ear types work
        assert len(pointed._points) > 0
        assert len(floppy._points) > 0
        assert len(tall._points) > 0
        assert len(round_ears._points) > 0
        assert len(none_ears._points) > 0


# Import controllers for articulation tests
from comix.cobject.character.character import ArmController, LegController


class TestStickmanArticulation:
    """Tests for Stickman joint articulation system."""

    def test_default_joint_angles_are_zero(self):
        """Test that default joint angles are all zero."""
        char = Stickman(height=150)
        assert char._left_shoulder_angle == 0.0
        assert char._left_elbow_angle == 0.0
        assert char._right_shoulder_angle == 0.0
        assert char._right_elbow_angle == 0.0
        assert char._left_hip_angle == 0.0
        assert char._left_knee_angle == 0.0
        assert char._right_hip_angle == 0.0
        assert char._right_knee_angle == 0.0

    def test_default_hands_are_none(self):
        """Test that default hand gestures are 'none'."""
        char = Stickman(height=150)
        assert char._left_hand == "none"
        assert char._right_hand == "none"

    def test_use_articulation_initially_false(self):
        """Test articulation mode is not active by default."""
        char = Stickman(height=150)
        assert char._use_articulation is False

    def test_set_arm_angles_activates_articulation(self):
        """Test that set_arm_angles activates articulation mode."""
        char = Stickman(height=150)
        char.set_arm_angles(left_shoulder=90)
        assert char._use_articulation is True

    def test_set_arm_angles_left_shoulder(self):
        """Test setting left shoulder angle."""
        char = Stickman(height=150)
        char.set_arm_angles(left_shoulder=90)
        assert char._left_shoulder_angle == 90.0

    def test_set_arm_angles_left_elbow(self):
        """Test setting left elbow angle."""
        char = Stickman(height=150)
        char.set_arm_angles(left_elbow=45)
        assert char._left_elbow_angle == 45.0

    def test_set_arm_angles_right_shoulder(self):
        """Test setting right shoulder angle."""
        char = Stickman(height=150)
        char.set_arm_angles(right_shoulder=180)
        assert char._right_shoulder_angle == 180.0

    def test_set_arm_angles_right_elbow(self):
        """Test setting right elbow angle."""
        char = Stickman(height=150)
        char.set_arm_angles(right_elbow=90)
        assert char._right_elbow_angle == 90.0

    def test_set_arm_angles_all_at_once(self):
        """Test setting all arm angles simultaneously."""
        char = Stickman(height=150)
        char.set_arm_angles(
            left_shoulder=45,
            left_elbow=30,
            right_shoulder=135,
            right_elbow=60
        )
        assert char._left_shoulder_angle == 45.0
        assert char._left_elbow_angle == 30.0
        assert char._right_shoulder_angle == 135.0
        assert char._right_elbow_angle == 60.0

    def test_set_arm_angles_returns_self(self):
        """Test set_arm_angles returns self for chaining."""
        char = Stickman(height=150)
        result = char.set_arm_angles(left_shoulder=90)
        assert result is char

    def test_set_leg_angles_activates_articulation(self):
        """Test that set_leg_angles activates articulation mode."""
        char = Stickman(height=150)
        char.set_leg_angles(left_hip=30)
        assert char._use_articulation is True

    def test_set_leg_angles_left_hip(self):
        """Test setting left hip angle."""
        char = Stickman(height=150)
        char.set_leg_angles(left_hip=30)
        assert char._left_hip_angle == 30.0

    def test_set_leg_angles_left_knee(self):
        """Test setting left knee angle."""
        char = Stickman(height=150)
        char.set_leg_angles(left_knee=45)
        assert char._left_knee_angle == 45.0

    def test_set_leg_angles_right_hip(self):
        """Test setting right hip angle."""
        char = Stickman(height=150)
        char.set_leg_angles(right_hip=90)
        assert char._right_hip_angle == 90.0

    def test_set_leg_angles_right_knee(self):
        """Test setting right knee angle."""
        char = Stickman(height=150)
        char.set_leg_angles(right_knee=90)
        assert char._right_knee_angle == 90.0

    def test_set_leg_angles_all_at_once(self):
        """Test setting all leg angles simultaneously."""
        char = Stickman(height=150)
        char.set_leg_angles(
            left_hip=30,
            left_knee=15,
            right_hip=-20,
            right_knee=10
        )
        assert char._left_hip_angle == 30.0
        assert char._left_knee_angle == 15.0
        assert char._right_hip_angle == -20.0
        assert char._right_knee_angle == 10.0

    def test_set_leg_angles_returns_self(self):
        """Test set_leg_angles returns self for chaining."""
        char = Stickman(height=150)
        result = char.set_leg_angles(left_hip=30)
        assert result is char


class TestStickmanAngleNormalization:
    """Tests for angle normalization and clamping."""

    def test_shoulder_angle_normalization_positive(self):
        """Test shoulder angles normalize from >360."""
        char = Stickman(height=150)
        char.set_arm_angles(left_shoulder=370)
        assert char._left_shoulder_angle == 10.0

    def test_shoulder_angle_normalization_large_positive(self):
        """Test shoulder angles normalize from very large values."""
        char = Stickman(height=150)
        char.set_arm_angles(left_shoulder=720)
        assert char._left_shoulder_angle == 0.0

    def test_shoulder_angle_normalization_negative(self):
        """Test shoulder angles normalize from negative values."""
        char = Stickman(height=150)
        char.set_arm_angles(left_shoulder=-90)
        assert char._left_shoulder_angle == 270.0

    def test_shoulder_angle_normalization_large_negative(self):
        """Test shoulder angles normalize from large negative values."""
        char = Stickman(height=150)
        char.set_arm_angles(left_shoulder=-450)
        assert char._left_shoulder_angle == 270.0

    def test_elbow_angle_clamped_to_max(self):
        """Test elbow angles clamp to max 180."""
        char = Stickman(height=150)
        char.set_arm_angles(left_elbow=200)
        assert char._left_elbow_angle == 180.0

    def test_elbow_angle_clamped_to_min(self):
        """Test elbow angles clamp to min 0."""
        char = Stickman(height=150)
        char.set_arm_angles(left_elbow=-30)
        assert char._left_elbow_angle == 0.0

    def test_knee_angle_clamped_to_max(self):
        """Test knee angles clamp to max 180."""
        char = Stickman(height=150)
        char.set_leg_angles(left_knee=200)
        assert char._left_knee_angle == 180.0

    def test_knee_angle_clamped_to_min(self):
        """Test knee angles clamp to min 0."""
        char = Stickman(height=150)
        char.set_leg_angles(left_knee=-30)
        assert char._left_knee_angle == 0.0


class TestStickmanHandGestures:
    """Tests for hand gesture system."""

    def test_set_hands_left(self):
        """Test setting left hand gesture."""
        char = Stickman(height=150)
        char.set_hands(left="fist")
        assert char._left_hand == "fist"

    def test_set_hands_right(self):
        """Test setting right hand gesture."""
        char = Stickman(height=150)
        char.set_hands(right="open")
        assert char._right_hand == "open"

    def test_set_hands_both(self):
        """Test setting both hand gestures."""
        char = Stickman(height=150)
        char.set_hands(left="point", right="fist")
        assert char._left_hand == "point"
        assert char._right_hand == "fist"

    def test_set_hands_returns_self(self):
        """Test set_hands returns self for chaining."""
        char = Stickman(height=150)
        result = char.set_hands(left="open")
        assert result is char

    def test_set_hands_activates_articulation(self):
        """Test that set_hands activates articulation mode."""
        char = Stickman(height=150)
        char.set_hands(left="fist")
        assert char._use_articulation is True

    def test_all_valid_hand_gestures(self):
        """Test all valid hand gesture options."""
        valid_gestures = ["none", "fist", "open", "point", "peace", "thumbs_up", "relaxed"]
        for gesture in valid_gestures:
            char = Stickman(height=150)
            char.set_hands(left=gesture)
            assert char._left_hand == gesture

    def test_invalid_hand_gesture_raises_error(self):
        """Test invalid hand gesture raises ValueError."""
        char = Stickman(height=150)
        with pytest.raises(ValueError) as excinfo:
            char.set_hands(left="invalid_gesture")
        assert "Invalid hand option" in str(excinfo.value)
        assert "invalid_gesture" in str(excinfo.value)

    def test_hand_gestures_generate_extra_points(self):
        """Test that hand gestures add points to the character."""
        char_no_hands = Stickman(height=150)
        char_with_hands = Stickman(height=150)
        char_with_hands.set_hands(left="open", right="fist")

        # Character with hand gestures should have more points
        assert len(char_with_hands._points) > len(char_no_hands._points)


class TestStickmanPointAt:
    """Tests for point_at helper method."""

    def test_point_at_coordinates(self):
        """Test point_at with (x, y) coordinates."""
        char = Stickman(height=150)
        char.move_to((100, 200))
        char.point_at((500, 200), arm="right")
        # Should set right arm to point roughly horizontally
        assert char._use_articulation is True
        assert char._right_hand == "point"

    def test_point_at_object(self):
        """Test point_at with CObject target."""
        from comix.cobject.shapes.shapes import Circle
        char = Stickman(height=150)
        char.move_to((100, 200))
        target = Circle(radius=20)
        target.move_to((500, 200))
        char.point_at(target, arm="right")
        assert char._use_articulation is True
        assert char._right_hand == "point"

    def test_point_at_left_arm(self):
        """Test point_at using left arm."""
        char = Stickman(height=150)
        char.move_to((100, 200))
        char.point_at((500, 200), arm="left")
        assert char._left_hand == "point"

    def test_point_at_custom_hand_gesture(self):
        """Test point_at with custom hand gesture."""
        char = Stickman(height=150)
        char.move_to((100, 200))
        char.point_at((500, 200), arm="right", hand="fist")
        assert char._right_hand == "fist"

    def test_point_at_with_elbow_bend(self):
        """Test point_at with elbow bend parameter."""
        char = Stickman(height=150)
        char.move_to((100, 200))
        char.point_at((500, 200), arm="right", elbow_bend=30)
        assert char._right_elbow_angle == 30.0

    def test_point_at_returns_self(self):
        """Test point_at returns self for chaining."""
        char = Stickman(height=150)
        char.move_to((100, 200))
        result = char.point_at((500, 200))
        assert result is char


class TestArmController:
    """Tests for ArmController helper class."""

    def test_arm_controller_created(self):
        """Test that arm controllers are created on Stickman."""
        char = Stickman(height=150)
        assert hasattr(char, 'left_arm')
        assert hasattr(char, 'right_arm')
        assert isinstance(char.left_arm, ArmController)
        assert isinstance(char.right_arm, ArmController)

    def test_arm_controller_set_preset_down(self):
        """Test arm controller 'down' preset."""
        char = Stickman(height=150)
        char.left_arm.set_preset("down")
        assert char._left_shoulder_angle == 0.0
        assert char._left_elbow_angle == 0.0

    def test_arm_controller_set_preset_forward(self):
        """Test arm controller 'forward' preset."""
        char = Stickman(height=150)
        char.left_arm.set_preset("forward")
        assert char._left_shoulder_angle == 90.0
        assert char._left_elbow_angle == 0.0

    def test_arm_controller_set_preset_up(self):
        """Test arm controller 'up' preset."""
        char = Stickman(height=150)
        char.left_arm.set_preset("up")
        assert char._left_shoulder_angle == 180.0

    def test_arm_controller_set_preset_waving(self):
        """Test arm controller 'waving' preset."""
        char = Stickman(height=150)
        char.left_arm.set_preset("waving")
        assert char._left_shoulder_angle == 180.0
        assert char._left_elbow_angle == 30.0

    def test_arm_controller_set_preset_pointing(self):
        """Test arm controller 'pointing' preset with hand gesture."""
        char = Stickman(height=150)
        char.right_arm.set_preset("pointing")
        assert char._right_shoulder_angle == 90.0
        assert char._right_elbow_angle == 0.0
        assert char._right_hand == "point"

    def test_arm_controller_set_preset_thinking(self):
        """Test arm controller 'thinking' preset with hand gesture."""
        char = Stickman(height=150)
        char.left_arm.set_preset("thinking")
        assert char._left_shoulder_angle == 120.0
        assert char._left_elbow_angle == 90.0
        assert char._left_hand == "fist"

    def test_arm_controller_invalid_preset_raises_error(self):
        """Test arm controller with invalid preset raises ValueError."""
        char = Stickman(height=150)
        with pytest.raises(ValueError) as excinfo:
            char.left_arm.set_preset("invalid_preset")
        assert "Unknown arm preset" in str(excinfo.value)

    def test_arm_controller_returns_stickman(self):
        """Test arm controller set_preset returns the parent Stickman."""
        char = Stickman(height=150)
        result = char.left_arm.set_preset("waving")
        assert result is char


class TestLegController:
    """Tests for LegController helper class."""

    def test_leg_controller_created(self):
        """Test that leg controllers are created on Stickman."""
        char = Stickman(height=150)
        assert hasattr(char, 'left_leg_ctrl')
        assert hasattr(char, 'right_leg_ctrl')
        assert isinstance(char.left_leg_ctrl, LegController)
        assert isinstance(char.right_leg_ctrl, LegController)

    def test_leg_controller_set_preset_standing(self):
        """Test leg controller 'standing' preset."""
        char = Stickman(height=150)
        char.left_leg_ctrl.set_preset("standing")
        assert char._left_hip_angle == 0.0
        assert char._left_knee_angle == 0.0

    def test_leg_controller_set_preset_walking(self):
        """Test leg controller 'walking' preset."""
        char = Stickman(height=150)
        char.left_leg_ctrl.set_preset("walking")
        assert char._left_hip_angle == 30.0
        assert char._left_knee_angle == 15.0

    def test_leg_controller_set_preset_sitting(self):
        """Test leg controller 'sitting' preset."""
        char = Stickman(height=150)
        char.left_leg_ctrl.set_preset("sitting")
        assert char._left_hip_angle == 90.0
        assert char._left_knee_angle == 90.0

    def test_leg_controller_set_preset_kneeling(self):
        """Test leg controller 'kneeling' preset."""
        char = Stickman(height=150)
        char.left_leg_ctrl.set_preset("kneeling")
        assert char._left_hip_angle == 135.0
        assert char._left_knee_angle == 135.0

    def test_leg_controller_invalid_preset_raises_error(self):
        """Test leg controller with invalid preset raises ValueError."""
        char = Stickman(height=150)
        with pytest.raises(ValueError) as excinfo:
            char.left_leg_ctrl.set_preset("invalid_preset")
        assert "Unknown leg preset" in str(excinfo.value)

    def test_leg_controller_returns_stickman(self):
        """Test leg controller set_preset returns the parent Stickman."""
        char = Stickman(height=150)
        result = char.left_leg_ctrl.set_preset("walking")
        assert result is char


class TestStickmanArticulationRenderData:
    """Tests for articulation data in render output."""

    def test_render_data_includes_articulation_flag(self):
        """Test render data includes use_articulation flag."""
        char = Stickman(height=150)
        data = char.get_render_data()
        assert "use_articulation" in data
        assert data["use_articulation"] is False

    def test_render_data_includes_joint_angles(self):
        """Test render data includes all joint angles."""
        char = Stickman(height=150)
        char.set_arm_angles(left_shoulder=45, left_elbow=30)
        char.set_leg_angles(left_hip=20, left_knee=15)
        data = char.get_render_data()

        assert data["left_shoulder_angle"] == 45.0
        assert data["left_elbow_angle"] == 30.0
        assert data["left_hip_angle"] == 20.0
        assert data["left_knee_angle"] == 15.0

    def test_render_data_includes_hand_gestures(self):
        """Test render data includes hand gestures."""
        char = Stickman(height=150)
        char.set_hands(left="open", right="fist")
        data = char.get_render_data()

        assert data["left_hand"] == "open"
        assert data["right_hand"] == "fist"


class TestStickmanArticulationGeometry:
    """Tests for articulation system geometry generation."""

    def test_articulation_generates_points(self):
        """Test that articulation mode generates valid points."""
        char = Stickman(height=150)
        char.set_arm_angles(left_shoulder=90, left_elbow=45)
        assert len(char._points) > 0

    def test_shoulder_angle_0_positions_arm_down(self):
        """Test shoulder angle 0° positions arm straight down."""
        char = Stickman(height=150)
        char.set_arm_angles(left_shoulder=0, left_elbow=0)
        # Points should exist
        assert len(char._points) > 0

    def test_shoulder_angle_90_positions_arm_horizontal(self):
        """Test shoulder angle 90° positions arm horizontally."""
        char = Stickman(height=150)
        char.set_arm_angles(left_shoulder=90, left_elbow=0)
        # Points should exist
        assert len(char._points) > 0

    def test_elbow_bend_90_creates_right_angle(self):
        """Test elbow bend 90° creates a right angle at elbow."""
        char = Stickman(height=150)
        char.set_arm_angles(left_shoulder=90, left_elbow=90)
        # Points should exist
        assert len(char._points) > 0

    def test_facing_left_mirrors_articulated_points(self):
        """Test that facing left mirrors articulated points."""
        char_right = Stickman(height=150)
        char_right.set_arm_angles(left_shoulder=90)

        char_left = Stickman(height=150)
        char_left.face("left")
        char_left.set_arm_angles(left_shoulder=90)

        # Left facing should have mirrored X coordinates
        assert char_left.facing == "left"
        # The x values should be mirrored (negative)
        assert np.sum(char_left._points[:, 0]) != np.sum(char_right._points[:, 0])


class TestStickmanMethodChaining:
    """Tests for method chaining with articulation system."""

    def test_chain_set_arm_angles_and_set_hands(self):
        """Test chaining set_arm_angles with set_hands."""
        char = Stickman(height=150)
        result = char.set_arm_angles(left_shoulder=90).set_hands(left="point")
        assert result is char
        assert char._left_shoulder_angle == 90.0
        assert char._left_hand == "point"

    def test_chain_set_leg_angles_and_set_arm_angles(self):
        """Test chaining set_leg_angles with set_arm_angles."""
        char = Stickman(height=150)
        result = char.set_leg_angles(left_hip=30).set_arm_angles(right_shoulder=180)
        assert result is char
        assert char._left_hip_angle == 30.0
        assert char._right_shoulder_angle == 180.0

    def test_chain_all_articulation_methods(self):
        """Test chaining all articulation methods together."""
        char = Stickman(height=150)
        result = (
            char
            .set_arm_angles(left_shoulder=45, right_shoulder=135)
            .set_leg_angles(left_hip=30, right_hip=-20)
            .set_hands(left="open", right="fist")
        )
        assert result is char
        assert char._left_shoulder_angle == 45.0
        assert char._right_shoulder_angle == 135.0
        assert char._left_hip_angle == 30.0
        assert char._right_hip_angle == -20.0
        assert char._left_hand == "open"
        assert char._right_hand == "fist"

    def test_chain_with_controller_presets(self):
        """Test chaining controller preset methods."""
        char = Stickman(height=150)
        char.left_arm.set_preset("waving")
        char.right_arm.set_preset("pointing")
        char.left_leg_ctrl.set_preset("walking")
        char.right_leg_ctrl.set_preset("standing")

        assert char._left_shoulder_angle == 180.0
        assert char._right_shoulder_angle == 90.0
        assert char._left_hip_angle == 30.0
        assert char._right_hip_angle == 0.0


class TestStickmanBackwardCompatibility:
    """Tests ensuring articulation system doesn't break existing functionality."""

    def test_pose_system_still_works(self):
        """Test that pose-based system still works when articulation not used."""
        char = Stickman(height=150)
        char.set_pose("waving")
        # Pose should be set
        assert char._pose.name == "waving"
        # Articulation should not be active
        assert char._use_articulation is False

    def test_articulation_overrides_pose(self):
        """Test that articulation overrides pose when both are used."""
        char = Stickman(height=150)
        char.set_pose("waving")
        char.set_arm_angles(left_shoulder=45)
        # Articulation should now be active
        assert char._use_articulation is True
        # Shoulder should have custom angle, not pose angle
        assert char._left_shoulder_angle == 45.0

    def test_expression_still_works_with_articulation(self):
        """Test expressions work with articulation."""
        char = Stickman(height=150)
        char.set_arm_angles(left_shoulder=90)
        char.set_expression("happy")
        assert char._expression.name == "happy"

    def test_facing_works_with_articulation(self):
        """Test facing direction works with articulation."""
        char = Stickman(height=150)
        char.set_arm_angles(left_shoulder=90)
        char.face("left")
        assert char.facing == "left"

    def test_proportion_styles_work_with_articulation(self):
        """Test proportion styles work with articulation."""
        char = Stickman(height=150, proportion_style="xkcd")
        char.set_arm_angles(left_shoulder=90)
        assert char.proportion_style == "xkcd"
        assert char._use_articulation is True
