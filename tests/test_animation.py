"""Tests for the animation system."""

from __future__ import annotations

import math
from unittest.mock import MagicMock

import pytest

from comix.animation.easing import (
    EASING_FUNCTIONS,
    ease_in_bounce,
    ease_in_cubic,
    ease_in_elastic,
    ease_in_out_bounce,
    ease_in_out_cubic,
    ease_in_out_quad,
    ease_in_quad,
    ease_out_bounce,
    ease_out_cubic,
    ease_out_elastic,
    ease_out_quad,
    get_easing,
    linear,
    register_easing,
)
from comix.animation.animation import (
    AnimationConfig,
    AnimationGroup,
    EffectAnimation,
    ObjectAnimation,
    PropertyAnimation,
)
from comix.animation.timeline import Timeline, TimelineEntry
from comix.effect.effect import ShakeEffect
from comix.cobject.character.character import Stickman


class TestEasingFunctions:
    """Tests for easing functions."""

    def test_linear_at_boundaries(self) -> None:
        assert linear(0.0) == 0.0
        assert linear(1.0) == 1.0

    def test_linear_at_midpoint(self) -> None:
        assert linear(0.5) == 0.5

    def test_ease_in_quad_at_boundaries(self) -> None:
        assert ease_in_quad(0.0) == 0.0
        assert ease_in_quad(1.0) == 1.0

    def test_ease_in_quad_slow_start(self) -> None:
        # Should be slower than linear at start
        assert ease_in_quad(0.25) < 0.25

    def test_ease_out_quad_at_boundaries(self) -> None:
        assert ease_out_quad(0.0) == 0.0
        assert ease_out_quad(1.0) == 1.0

    def test_ease_out_quad_fast_start(self) -> None:
        # Should be faster than linear at start
        assert ease_out_quad(0.25) > 0.25

    def test_ease_in_out_quad_at_boundaries(self) -> None:
        assert ease_in_out_quad(0.0) == 0.0
        assert ease_in_out_quad(1.0) == 1.0

    def test_ease_in_out_quad_symmetric(self) -> None:
        assert abs(ease_in_out_quad(0.5) - 0.5) < 0.001

    def test_ease_in_cubic_slower_than_quad(self) -> None:
        # Cubic should be slower than quad at early progress
        assert ease_in_cubic(0.25) < ease_in_quad(0.25)

    def test_ease_out_cubic_faster_than_quad(self) -> None:
        # Cubic ease out should be faster than quad at early progress
        assert ease_out_cubic(0.25) > ease_out_quad(0.25)

    def test_ease_in_out_cubic_at_boundaries(self) -> None:
        assert ease_in_out_cubic(0.0) == 0.0
        assert ease_in_out_cubic(1.0) == 1.0

    def test_ease_in_elastic_at_boundaries(self) -> None:
        assert ease_in_elastic(0.0) == 0.0
        assert ease_in_elastic(1.0) == 1.0

    def test_ease_out_elastic_at_boundaries(self) -> None:
        assert ease_out_elastic(0.0) == 0.0
        assert ease_out_elastic(1.0) == 1.0

    def test_ease_out_bounce_at_boundaries(self) -> None:
        assert ease_out_bounce(0.0) == 0.0
        assert abs(ease_out_bounce(1.0) - 1.0) < 0.001

    def test_ease_in_bounce_at_boundaries(self) -> None:
        assert ease_in_bounce(0.0) == 0.0
        assert abs(ease_in_bounce(1.0) - 1.0) < 0.001

    def test_ease_in_out_bounce_at_boundaries(self) -> None:
        assert ease_in_out_bounce(0.0) == 0.0
        assert abs(ease_in_out_bounce(1.0) - 1.0) < 0.001

    def test_get_easing_returns_correct_function(self) -> None:
        assert get_easing("linear") == linear
        assert get_easing("ease_in") == ease_in_quad
        assert get_easing("ease_out") == ease_out_quad

    def test_get_easing_unknown_raises_error(self) -> None:
        with pytest.raises(ValueError, match="Unknown easing function"):
            get_easing("nonexistent")

    def test_register_easing_adds_function(self) -> None:
        def custom_easing(t: float) -> float:
            return t * t * t * t

        register_easing("custom_test", custom_easing)
        assert get_easing("custom_test") == custom_easing
        # Clean up
        del EASING_FUNCTIONS["custom_test"]

    def test_all_easing_functions_have_valid_boundaries(self) -> None:
        for name, func in EASING_FUNCTIONS.items():
            assert abs(func(0.0)) < 0.5, f"{name} should start near 0"
            assert abs(func(1.0) - 1.0) < 0.5, f"{name} should end near 1"


class TestAnimationConfig:
    """Tests for AnimationConfig."""

    def test_default_values(self) -> None:
        config = AnimationConfig()
        assert config.fps == 24
        assert config.duration == 1.0
        assert config.loop is True
        assert config.loop_count == 0
        assert config.quality == "medium"

    def test_custom_values(self) -> None:
        config = AnimationConfig(fps=30, duration=2.0, loop=False, loop_count=3)
        assert config.fps == 30
        assert config.duration == 2.0
        assert config.loop is False
        assert config.loop_count == 3

    def test_frame_count(self) -> None:
        config = AnimationConfig(fps=24, duration=2.0)
        assert config.frame_count == 48

    def test_frame_duration(self) -> None:
        config = AnimationConfig(fps=24)
        assert abs(config.frame_duration - 1 / 24) < 0.0001


class TestPropertyAnimation:
    """Tests for PropertyAnimation."""

    def test_init(self) -> None:
        target = MagicMock()
        target.value = 0.0
        anim = PropertyAnimation(target, "value", 0.0, 100.0, duration=1.0)
        assert anim.target == target
        assert anim.property_name == "value"
        assert anim.start_value == 0.0
        assert anim.end_value == 100.0
        assert anim.duration == 1.0

    def test_apply_at_progress_zero(self) -> None:
        target = MagicMock()
        target.value = 50.0
        anim = PropertyAnimation(target, "value", 0.0, 100.0)
        anim.apply(0.0)
        assert target.value == 0.0

    def test_apply_at_progress_half(self) -> None:
        target = MagicMock()
        target.value = 0.0
        anim = PropertyAnimation(target, "value", 0.0, 100.0)
        anim.apply(0.5)
        assert target.value == 50.0

    def test_apply_at_progress_one(self) -> None:
        target = MagicMock()
        target.value = 0.0
        anim = PropertyAnimation(target, "value", 0.0, 100.0)
        anim.apply(1.0)
        assert target.value == 100.0

    def test_reset_restores_initial_value(self) -> None:
        target = MagicMock()
        target.value = 50.0
        anim = PropertyAnimation(target, "value", 0.0, 100.0)
        anim.apply(1.0)
        anim.reset()
        assert target.value == 50.0

    def test_triggers_needs_generate_if_present(self) -> None:
        target = MagicMock()
        target.value = 0.0
        target._needs_generate = False
        anim = PropertyAnimation(target, "value", 0.0, 100.0)
        anim.apply(0.5)
        assert target._needs_generate is True

    def test_get_progress_before_delay(self) -> None:
        target = MagicMock()
        target.value = 0.0
        anim = PropertyAnimation(target, "value", 0.0, 100.0, delay=0.5)
        assert anim.get_progress(0.25) == 0.0

    def test_get_progress_after_delay(self) -> None:
        target = MagicMock()
        target.value = 0.0
        anim = PropertyAnimation(target, "value", 0.0, 100.0, duration=1.0, delay=0.5)
        progress = anim.get_progress(1.0)  # 0.5 seconds after delay
        assert abs(progress - 0.5) < 0.001


class TestEffectAnimation:
    """Tests for EffectAnimation."""

    def test_init_with_effect(self) -> None:
        effect = ShakeEffect(seed=42)
        anim = EffectAnimation(effect, pattern="pulse", duration=0.5)
        assert anim.effect == effect
        assert anim.pattern == "pulse"
        assert anim.duration == 0.5

    def test_fade_in_pattern(self) -> None:
        effect = ShakeEffect(seed=42)
        effect.set_opacity(1.0)
        anim = EffectAnimation(effect, pattern="fade_in")

        anim.apply(0.0)
        assert effect.opacity == 0.0

        anim.apply(0.5)
        assert abs(effect.opacity - 0.5) < 0.01

        anim.apply(1.0)
        assert abs(effect.opacity - 1.0) < 0.01

    def test_fade_out_pattern(self) -> None:
        effect = ShakeEffect(seed=42)
        effect.set_opacity(1.0)
        anim = EffectAnimation(effect, pattern="fade_out")

        anim.apply(0.0)
        assert abs(effect.opacity - 1.0) < 0.01

        anim.apply(0.5)
        assert abs(effect.opacity - 0.5) < 0.01

        anim.apply(1.0)
        assert effect.opacity == 0.0

    def test_grow_pattern(self) -> None:
        effect = ShakeEffect(seed=42)
        effect.set_intensity(1.0)
        anim = EffectAnimation(effect, pattern="grow")

        anim.apply(0.0)
        assert effect.intensity == 0.0

        anim.apply(1.0)
        assert abs(effect.intensity - 1.0) < 0.01

    def test_shrink_pattern(self) -> None:
        effect = ShakeEffect(seed=42)
        effect.set_intensity(1.0)
        anim = EffectAnimation(effect, pattern="shrink")

        anim.apply(0.0)
        assert abs(effect.intensity - 1.0) < 0.01

        anim.apply(1.0)
        assert effect.intensity == 0.0

    def test_reverse_option(self) -> None:
        effect = ShakeEffect(seed=42)
        effect.set_opacity(1.0)
        anim = EffectAnimation(effect, pattern="fade_in", reverse=True)

        # Reversed fade_in should start at 1.0 and end at 0.0
        anim.apply(0.0)
        assert abs(effect.opacity - 1.0) < 0.01

        anim.apply(1.0)
        assert effect.opacity == 0.0

    def test_reset_restores_values(self) -> None:
        effect = ShakeEffect(seed=42)
        effect.set_opacity(0.8)
        effect.set_intensity(0.7)
        anim = EffectAnimation(effect, pattern="fade_out")

        anim.apply(1.0)
        assert effect.opacity < 0.1

        anim.reset()
        assert abs(effect.opacity - 0.8) < 0.01

    def test_set_pattern_method_chaining(self) -> None:
        effect = ShakeEffect(seed=42)
        anim = EffectAnimation(effect)
        result = anim.set_pattern("grow")
        assert result is anim
        assert anim.pattern == "grow"

    def test_set_easing_method_chaining(self) -> None:
        effect = ShakeEffect(seed=42)
        anim = EffectAnimation(effect)
        result = anim.set_easing("ease_out_bounce")
        assert result is anim


class TestObjectAnimation:
    """Tests for ObjectAnimation."""

    def test_init_with_cobject(self) -> None:
        char = Stickman(height=100)
        char.move_to((100, 100))
        anim = ObjectAnimation(char, position=(200, 200), duration=1.0)
        assert anim.target == char
        assert anim.end_position == (200, 200)
        assert anim.duration == 1.0

    def test_animate_position(self) -> None:
        char = Stickman(height=100)
        char.move_to((100, 100))
        anim = ObjectAnimation(char, position=(200, 200), duration=1.0)

        anim.apply(0.0)
        pos = char.position
        assert abs(pos[0] - 100) < 0.1
        assert abs(pos[1] - 100) < 0.1

        anim.apply(0.5)
        pos = char.position
        assert abs(pos[0] - 150) < 0.1
        assert abs(pos[1] - 150) < 0.1

        anim.apply(1.0)
        pos = char.position
        assert abs(pos[0] - 200) < 0.1
        assert abs(pos[1] - 200) < 0.1

    def test_animate_scale(self) -> None:
        char = Stickman(height=100)
        char.set_scale(1.0)
        anim = ObjectAnimation(char, scale=2.0, duration=1.0)

        anim.apply(0.0)
        assert abs(char.scale - 1.0) < 0.01

        anim.apply(1.0)
        assert abs(char.scale - 2.0) < 0.01

    def test_animate_rotation(self) -> None:
        char = Stickman(height=100)
        char.set_rotation(0.0)
        anim = ObjectAnimation(char, rotation=math.pi, duration=1.0)

        anim.apply(0.0)
        assert abs(char.rotation) < 0.01

        anim.apply(1.0)
        assert abs(char.rotation - math.pi) < 0.01

    def test_animate_opacity(self) -> None:
        char = Stickman(height=100)
        char.set_opacity(1.0)
        anim = ObjectAnimation(char, opacity=0.0, duration=1.0)

        anim.apply(0.0)
        assert abs(char.opacity - 1.0) < 0.01

        anim.apply(1.0)
        assert abs(char.opacity) < 0.01

    def test_reset_restores_state(self) -> None:
        char = Stickman(height=100)
        char.move_to((100, 100))
        char.set_scale(1.0)
        anim = ObjectAnimation(char, position=(200, 200), scale=2.0)

        anim.apply(1.0)
        anim.reset()

        pos = char.position
        assert abs(pos[0] - 100) < 0.1
        assert abs(pos[1] - 100) < 0.1
        assert abs(char.scale - 1.0) < 0.01

    def test_to_position_method_chaining(self) -> None:
        char = Stickman(height=100)
        anim = ObjectAnimation(char)
        result = anim.to_position(300, 300)
        assert result is anim
        assert anim.end_position == (300, 300)

    def test_to_scale_method_chaining(self) -> None:
        char = Stickman(height=100)
        anim = ObjectAnimation(char)
        result = anim.to_scale(1.5)
        assert result is anim
        assert anim.end_scale == 1.5


class TestAnimationGroup:
    """Tests for AnimationGroup."""

    def test_parallel_mode_duration(self) -> None:
        effect1 = ShakeEffect(seed=42)
        effect2 = ShakeEffect(seed=43)
        anim1 = EffectAnimation(effect1, pattern="fade_in", duration=1.0)
        anim2 = EffectAnimation(effect2, pattern="grow", duration=2.0)

        group = AnimationGroup(anim1, anim2, mode="parallel")
        assert group.duration == 2.0

    def test_sequence_mode_duration(self) -> None:
        effect1 = ShakeEffect(seed=42)
        effect2 = ShakeEffect(seed=43)
        anim1 = EffectAnimation(effect1, pattern="fade_in", duration=1.0)
        anim2 = EffectAnimation(effect2, pattern="grow", duration=2.0)

        group = AnimationGroup(anim1, anim2, mode="sequence")
        assert group.duration == 3.0

    def test_parallel_applies_all_at_same_time(self) -> None:
        effect1 = ShakeEffect(seed=42)
        effect1.set_opacity(1.0)
        effect2 = ShakeEffect(seed=43)
        effect2.set_intensity(1.0)

        anim1 = EffectAnimation(effect1, pattern="fade_out", duration=1.0)
        anim2 = EffectAnimation(effect2, pattern="shrink", duration=1.0)

        group = AnimationGroup(anim1, anim2, mode="parallel")
        group.apply(0.5)

        assert effect1.opacity < 0.6
        assert effect2.intensity < 0.6

    def test_sequence_applies_one_after_another(self) -> None:
        effect1 = ShakeEffect(seed=42)
        effect1.set_opacity(1.0)
        effect2 = ShakeEffect(seed=43)
        effect2.set_intensity(1.0)

        anim1 = EffectAnimation(effect1, pattern="fade_out", duration=1.0)
        anim2 = EffectAnimation(effect2, pattern="shrink", duration=1.0)

        group = AnimationGroup(anim1, anim2, mode="sequence")

        # At t=0.25 (25% of total 2s = 0.5s into first animation)
        group.apply(0.25)
        assert effect1.opacity < 0.6  # First animation should be in progress
        # Second animation hasn't started, intensity should still be initial

    def test_add_animations(self) -> None:
        effect1 = ShakeEffect(seed=42)
        effect2 = ShakeEffect(seed=43)
        anim1 = EffectAnimation(effect1, pattern="fade_in", duration=1.0)
        anim2 = EffectAnimation(effect2, pattern="grow", duration=1.0)

        group = AnimationGroup(anim1, mode="parallel")
        result = group.add(anim2)

        assert result is group
        assert group.duration == 1.0  # Both are 1.0s in parallel

    def test_reset_resets_all(self) -> None:
        effect1 = ShakeEffect(seed=42)
        effect1.set_opacity(0.8)
        effect2 = ShakeEffect(seed=43)
        effect2.set_opacity(0.9)

        anim1 = EffectAnimation(effect1, pattern="fade_out", duration=1.0)
        anim2 = EffectAnimation(effect2, pattern="fade_out", duration=1.0)

        group = AnimationGroup(anim1, anim2, mode="parallel")
        group.apply(1.0)

        assert effect1.opacity < 0.1
        assert effect2.opacity < 0.1

        group.reset()

        assert abs(effect1.opacity - 0.8) < 0.01
        assert abs(effect2.opacity - 0.9) < 0.01


class TestTimeline:
    """Tests for Timeline."""

    def test_empty_timeline_duration(self) -> None:
        timeline = Timeline()
        assert timeline.duration == 0.0

    def test_add_animation(self) -> None:
        timeline = Timeline()
        effect = ShakeEffect(seed=42)
        anim = EffectAnimation(effect, pattern="pulse", duration=1.0)

        result = timeline.add(anim, start_time=0.5)

        assert result is timeline
        assert len(timeline.entries) == 1
        assert timeline.duration == 1.5

    def test_then_adds_after_previous(self) -> None:
        timeline = Timeline()
        effect1 = ShakeEffect(seed=42)
        effect2 = ShakeEffect(seed=43)
        anim1 = EffectAnimation(effect1, duration=1.0)
        anim2 = EffectAnimation(effect2, duration=0.5)

        timeline.add(anim1)
        timeline.then(anim2)

        assert len(timeline.entries) == 2
        assert timeline.entries[1].start_time == 1.0
        assert timeline.duration == 1.5

    def test_then_with_gap(self) -> None:
        timeline = Timeline()
        effect1 = ShakeEffect(seed=42)
        effect2 = ShakeEffect(seed=43)
        anim1 = EffectAnimation(effect1, duration=1.0)
        anim2 = EffectAnimation(effect2, duration=0.5)

        timeline.add(anim1)
        timeline.then(anim2, gap=0.5)

        assert timeline.entries[1].start_time == 1.5
        assert timeline.duration == 2.0

    def test_with_previous_starts_at_same_time(self) -> None:
        timeline = Timeline()
        effect1 = ShakeEffect(seed=42)
        effect2 = ShakeEffect(seed=43)
        anim1 = EffectAnimation(effect1, duration=1.0)
        anim2 = EffectAnimation(effect2, duration=0.5)

        timeline.add(anim1, start_time=0.5)
        timeline.with_previous(anim2)

        assert timeline.entries[0].start_time == 0.5
        assert timeline.entries[1].start_time == 0.5

    def test_at_builder(self) -> None:
        timeline = Timeline()
        effect = ShakeEffect(seed=42)
        anim = EffectAnimation(effect, duration=1.0)

        result = timeline.at(2.0).add(anim)

        assert result is timeline
        assert timeline.entries[0].start_time == 2.0

    def test_apply_at_time(self) -> None:
        timeline = Timeline()
        effect = ShakeEffect(seed=42)
        effect.set_opacity(1.0)
        anim = EffectAnimation(effect, pattern="fade_out", duration=1.0)

        timeline.add(anim, start_time=0.0)

        timeline.apply_at_time(0.0)
        assert abs(effect.opacity - 1.0) < 0.01

        timeline.apply_at_time(0.5)
        assert effect.opacity < 0.6

        timeline.apply_at_time(1.0)
        assert effect.opacity < 0.1

    def test_apply_respects_start_time(self) -> None:
        timeline = Timeline()
        effect = ShakeEffect(seed=42)
        effect.set_opacity(1.0)
        anim = EffectAnimation(effect, pattern="fade_out", duration=1.0)

        timeline.add(anim, start_time=0.5)

        # Before animation starts
        timeline.apply_at_time(0.25)
        assert abs(effect.opacity - 1.0) < 0.01  # Should not have changed

        # After animation starts
        timeline.apply_at_time(1.0)  # 0.5s into the animation
        assert effect.opacity < 0.6

    def test_reset_resets_all_animations(self) -> None:
        timeline = Timeline()
        effect = ShakeEffect(seed=42)
        effect.set_opacity(0.8)
        anim = EffectAnimation(effect, pattern="fade_out", duration=1.0)

        timeline.add(anim)
        timeline.apply_at_time(1.0)

        assert effect.opacity < 0.1

        timeline.reset()

        assert abs(effect.opacity - 0.8) < 0.01

    def test_clear_removes_all_entries(self) -> None:
        timeline = Timeline()
        effect = ShakeEffect(seed=42)
        anim = EffectAnimation(effect, duration=1.0)

        timeline.add(anim)
        result = timeline.clear()

        assert result is timeline
        assert len(timeline.entries) == 0
        assert timeline.duration == 0.0

    def test_get_active_animations(self) -> None:
        timeline = Timeline()
        effect1 = ShakeEffect(seed=42)
        effect2 = ShakeEffect(seed=43)
        anim1 = EffectAnimation(effect1, duration=1.0)
        anim2 = EffectAnimation(effect2, duration=1.0)

        timeline.add(anim1, start_time=0.0)
        timeline.add(anim2, start_time=0.5)

        # At t=0.25, only anim1 should be active
        active = timeline.get_active_animations(0.25)
        assert anim1 in active
        assert anim2 not in active

        # At t=0.75, both should be active
        active = timeline.get_active_animations(0.75)
        assert anim1 in active
        assert anim2 in active


class TestTimelineEntry:
    """Tests for TimelineEntry."""

    def test_end_time_calculation(self) -> None:
        effect = ShakeEffect(seed=42)
        anim = EffectAnimation(effect, duration=1.0, delay=0.5)
        entry = TimelineEntry(animation=anim, start_time=2.0)

        assert entry.end_time == 3.5  # 2.0 + 1.0 + 0.5


class TestAnimationMethodChaining:
    """Tests for method chaining on Animation classes."""

    def test_animation_set_duration(self) -> None:
        effect = ShakeEffect(seed=42)
        anim = EffectAnimation(effect)
        result = anim.set_duration(2.0)
        assert result is anim
        assert anim.duration == 2.0

    def test_animation_set_delay(self) -> None:
        effect = ShakeEffect(seed=42)
        anim = EffectAnimation(effect)
        result = anim.set_delay(0.5)
        assert result is anim
        assert anim.delay == 0.5

    def test_animation_chained_calls(self) -> None:
        effect = ShakeEffect(seed=42)
        anim = (
            EffectAnimation(effect)
            .set_duration(1.5)
            .set_delay(0.25)
            .set_easing("ease_out_bounce")
            .set_pattern("grow")
        )
        assert anim.duration == 1.5
        assert anim.delay == 0.25
        assert anim.pattern == "grow"


class TestAnimationProgress:
    """Tests for animation progress calculation."""

    def test_progress_before_start(self) -> None:
        effect = ShakeEffect(seed=42)
        anim = EffectAnimation(effect, duration=1.0, delay=1.0)
        assert anim.get_progress(0.5) == 0.0

    def test_progress_at_start(self) -> None:
        effect = ShakeEffect(seed=42)
        anim = EffectAnimation(effect, duration=1.0, delay=1.0)
        assert anim.get_progress(1.0) == 0.0

    def test_progress_during_animation(self) -> None:
        effect = ShakeEffect(seed=42)
        anim = EffectAnimation(effect, duration=1.0, delay=0.0, easing="linear")
        progress = anim.get_progress(0.5)
        assert abs(progress - 0.5) < 0.01

    def test_progress_at_end(self) -> None:
        effect = ShakeEffect(seed=42)
        anim = EffectAnimation(effect, duration=1.0, delay=0.0)
        assert anim.get_progress(1.0) == 1.0

    def test_progress_after_end(self) -> None:
        effect = ShakeEffect(seed=42)
        anim = EffectAnimation(effect, duration=1.0, delay=0.0)
        assert anim.get_progress(2.0) == 1.0

    def test_is_complete(self) -> None:
        effect = ShakeEffect(seed=42)
        anim = EffectAnimation(effect, duration=1.0, delay=0.5)

        assert not anim.is_complete(0.5)
        assert not anim.is_complete(1.0)
        assert anim.is_complete(1.5)
        assert anim.is_complete(2.0)

    def test_is_started(self) -> None:
        effect = ShakeEffect(seed=42)
        anim = EffectAnimation(effect, duration=1.0, delay=0.5)

        assert not anim.is_started(0.25)
        assert anim.is_started(0.5)
        assert anim.is_started(1.0)

    def test_total_duration(self) -> None:
        effect = ShakeEffect(seed=42)
        anim = EffectAnimation(effect, duration=1.0, delay=0.5)
        assert anim.total_duration == 1.5

    def test_zero_duration_animation(self) -> None:
        effect = ShakeEffect(seed=42)
        anim = EffectAnimation(effect, duration=0.0)
        assert anim.get_progress(0.0) == 1.0


class TestAnimationWithCustomEasing:
    """Tests for using custom easing functions."""

    def test_custom_callable_easing(self) -> None:
        def custom_easing(t: float) -> float:
            return t * t * t * t

        effect = ShakeEffect(seed=42)
        anim = EffectAnimation(effect, duration=1.0, easing=custom_easing)

        # At t=0.5 with quartic easing, progress should be 0.5^4 = 0.0625
        progress = anim.get_progress(0.5)
        assert abs(progress - 0.0625) < 0.01

    def test_easing_property_caches_function(self) -> None:
        effect = ShakeEffect(seed=42)
        anim = EffectAnimation(effect, easing="ease_in_cubic")

        # Access easing twice to test caching
        easing1 = anim.easing
        easing2 = anim.easing

        assert easing1 is easing2

    def test_set_easing_clears_cache(self) -> None:
        effect = ShakeEffect(seed=42)
        anim = EffectAnimation(effect, easing="linear")

        # Get initial easing
        _ = anim.easing

        # Change easing
        anim.set_easing("ease_out_bounce")

        # Verify cache was cleared by checking new function is different
        assert anim._easing_fn is None
