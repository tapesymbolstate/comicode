"""Animation system for comicode effects and objects.

Provides classes for animating CObjects and Effects over time,
enabling export to animated formats like GIF and video.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Callable, Self

if TYPE_CHECKING:
    from comix.cobject.cobject import CObject
    from comix.effect.effect import Effect


@dataclass
class AnimationConfig:
    """Configuration for animation export."""

    fps: int = 24
    duration: float = 1.0
    loop: bool = True
    loop_count: int = 0
    quality: str = "medium"

    @property
    def frame_count(self) -> int:
        """Total number of frames."""
        return max(1, int(self.fps * self.duration))

    @property
    def frame_duration(self) -> float:
        """Duration of each frame in seconds."""
        return 1.0 / self.fps if self.fps > 0 else 0.0


class Animation(ABC):
    """Base class for all animations.

    Animations define how properties change over time from t=0.0 to t=1.0.
    They can be applied to Effects, CObjects, or arbitrary property setters.
    """

    def __init__(
        self,
        duration: float = 1.0,
        delay: float = 0.0,
        easing: str | Callable[[float], float] = "linear",
    ) -> None:
        """Initialize animation.

        Args:
            duration: Animation duration in seconds.
            delay: Delay before animation starts in seconds.
            easing: Easing function name or callable.
        """
        self.duration = max(0.0, duration)
        self.delay = max(0.0, delay)
        self._easing = easing
        self._easing_fn: Callable[[float], float] | None = None

    @property
    def easing(self) -> Callable[[float], float]:
        """Get the easing function."""
        if self._easing_fn is None:
            if callable(self._easing):
                self._easing_fn = self._easing
            else:
                from comix.animation.easing import get_easing

                self._easing_fn = get_easing(self._easing)
        return self._easing_fn

    @property
    def total_duration(self) -> float:
        """Total duration including delay."""
        return self.delay + self.duration

    def set_duration(self, duration: float) -> Self:
        """Set animation duration."""
        self.duration = max(0.0, duration)
        return self

    def set_delay(self, delay: float) -> Self:
        """Set animation delay."""
        self.delay = max(0.0, delay)
        return self

    def set_easing(self, easing: str | Callable[[float], float]) -> Self:
        """Set easing function."""
        self._easing = easing
        self._easing_fn = None
        return self

    def get_progress(self, time: float) -> float:
        """Get animation progress (0.0 to 1.0) for given time.

        Args:
            time: Current time in seconds.

        Returns:
            Progress value from 0.0 to 1.0 with easing applied.
        """
        if time < self.delay:
            return 0.0
        elapsed = time - self.delay
        if self.duration <= 0:
            return 1.0
        if elapsed >= self.duration:
            return 1.0
        raw_progress = elapsed / self.duration
        return self.easing(raw_progress)

    def is_complete(self, time: float) -> bool:
        """Check if animation is complete at given time."""
        return time >= self.total_duration

    def is_started(self, time: float) -> bool:
        """Check if animation has started at given time."""
        return time >= self.delay

    @abstractmethod
    def apply(self, progress: float) -> None:
        """Apply the animation at given progress (0.0 to 1.0).

        Args:
            progress: Animation progress with easing applied.
        """
        pass

    @abstractmethod
    def reset(self) -> None:
        """Reset to initial state."""
        pass


class PropertyAnimation(Animation):
    """Animates a single property from start to end value."""

    def __init__(
        self,
        target: Any,
        property_name: str,
        start_value: float,
        end_value: float,
        duration: float = 1.0,
        delay: float = 0.0,
        easing: str | Callable[[float], float] = "linear",
    ) -> None:
        """Initialize property animation.

        Args:
            target: Object to animate.
            property_name: Name of the property to animate.
            start_value: Starting value.
            end_value: Ending value.
            duration: Animation duration.
            delay: Delay before start.
            easing: Easing function.
        """
        super().__init__(duration, delay, easing)
        self.target = target
        self.property_name = property_name
        self.start_value = start_value
        self.end_value = end_value
        self._initial_value: float | None = None

    def apply(self, progress: float) -> None:
        """Apply interpolated value to target property."""
        if self._initial_value is None:
            self._initial_value = getattr(self.target, self.property_name, self.start_value)

        value = self.start_value + (self.end_value - self.start_value) * progress
        setattr(self.target, self.property_name, value)

        if hasattr(self.target, "_needs_generate"):
            self.target._needs_generate = True

    def reset(self) -> None:
        """Reset property to initial value."""
        if self._initial_value is not None:
            setattr(self.target, self.property_name, self._initial_value)
            if hasattr(self.target, "_needs_generate"):
                self.target._needs_generate = True


class EffectAnimation(Animation):
    """Animates an Effect with predefined animation patterns."""

    PATTERNS: dict[str, list[str]] = {
        "pulse": ["intensity"],
        "fade_in": ["opacity"],
        "fade_out": ["opacity"],
        "grow": ["intensity"],
        "shrink": ["intensity"],
        "shake_intensify": ["intensity", "shake_distance"],
        "zoom_burst": ["intensity", "inner_radius", "outer_radius"],
    }

    def __init__(
        self,
        effect: Effect,
        pattern: str = "pulse",
        duration: float = 1.0,
        delay: float = 0.0,
        easing: str | Callable[[float], float] = "ease_in_out",
        reverse: bool = False,
    ) -> None:
        """Initialize effect animation.

        Args:
            effect: Effect to animate.
            pattern: Animation pattern name.
            duration: Animation duration.
            delay: Delay before start.
            easing: Easing function.
            reverse: Whether to reverse the animation.
        """
        super().__init__(duration, delay, easing)
        self.effect = effect
        self.pattern = pattern
        self.reverse = reverse
        self._initial_values: dict[str, Any] = {}

    def set_pattern(self, pattern: str) -> Self:
        """Set animation pattern."""
        self.pattern = pattern
        return self

    def set_reverse(self, reverse: bool) -> Self:
        """Set whether animation should reverse."""
        self.reverse = reverse
        return self

    def apply(self, progress: float) -> None:
        """Apply pattern-based animation to effect."""
        if self.reverse:
            progress = 1.0 - progress

        if not self._initial_values:
            self._capture_initial_values()

        self._apply_pattern(progress)
        self.effect._needs_generate = True

    def _capture_initial_values(self) -> None:
        """Capture initial property values for reset."""
        properties = self.PATTERNS.get(self.pattern, ["intensity"])
        for prop in properties:
            if hasattr(self.effect, prop):
                self._initial_values[prop] = getattr(self.effect, prop)

        if "opacity" not in self._initial_values:
            self._initial_values["opacity"] = self.effect.opacity
        if "intensity" not in self._initial_values:
            self._initial_values["intensity"] = self.effect.intensity

    def _apply_pattern(self, progress: float) -> None:
        """Apply the animation pattern at current progress."""
        if self.pattern == "pulse":
            pulse_value = 0.5 + 0.5 * (1 - abs(2 * progress - 1))
            base = self._initial_values.get("intensity", 1.0)
            self.effect.intensity = base * pulse_value

        elif self.pattern == "fade_in":
            self.effect.opacity = progress * self._initial_values.get("opacity", 1.0)

        elif self.pattern == "fade_out":
            self.effect.opacity = (1.0 - progress) * self._initial_values.get("opacity", 1.0)

        elif self.pattern == "grow":
            self.effect.intensity = progress * self._initial_values.get("intensity", 1.0)

        elif self.pattern == "shrink":
            self.effect.intensity = (1.0 - progress) * self._initial_values.get("intensity", 1.0)

        elif self.pattern == "shake_intensify":
            base_intensity = self._initial_values.get("intensity", 1.0)
            self.effect.intensity = base_intensity * (0.3 + 0.7 * progress)
            if hasattr(self.effect, "shake_distance"):
                base_distance = self._initial_values.get("shake_distance", 5.0)
                self.effect.shake_distance = base_distance * (0.5 + 1.5 * progress)

        elif self.pattern == "zoom_burst":
            if hasattr(self.effect, "inner_radius") and hasattr(self.effect, "outer_radius"):
                base_inner = self._initial_values.get("inner_radius", 50.0)
                base_outer = self._initial_values.get("outer_radius", 150.0)
                self.effect.inner_radius = base_inner * (1.0 + 0.5 * progress)
                self.effect.outer_radius = base_outer * (1.0 + progress)
                self.effect.intensity = self._initial_values.get("intensity", 1.0) * (1.0 - 0.3 * progress)

    def reset(self) -> None:
        """Reset effect to initial values."""
        for prop, value in self._initial_values.items():
            if hasattr(self.effect, prop):
                setattr(self.effect, prop, value)
        self.effect._needs_generate = True


class ObjectAnimation(Animation):
    """Animates a CObject's transform properties."""

    def __init__(
        self,
        target: CObject,
        duration: float = 1.0,
        delay: float = 0.0,
        easing: str | Callable[[float], float] = "ease_in_out",
        position: tuple[float, float] | None = None,
        scale: float | None = None,
        rotation: float | None = None,
        opacity: float | None = None,
    ) -> None:
        """Initialize object animation.

        Args:
            target: CObject to animate.
            duration: Animation duration.
            delay: Delay before start.
            easing: Easing function.
            position: Target position (x, y).
            scale: Target scale factor.
            rotation: Target rotation in radians.
            opacity: Target opacity (0.0-1.0).
        """
        super().__init__(duration, delay, easing)
        self.target = target
        self.end_position = position
        self.end_scale = scale
        self.end_rotation = rotation
        self.end_opacity = opacity

        self._start_position: tuple[float, float] | None = None
        self._start_scale: float | None = None
        self._start_rotation: float | None = None
        self._start_opacity: float | None = None
        self._captured = False

    def to_position(self, x: float, y: float) -> Self:
        """Set target position."""
        self.end_position = (x, y)
        return self

    def to_scale(self, scale: float) -> Self:
        """Set target scale."""
        self.end_scale = scale
        return self

    def to_rotation(self, rotation: float) -> Self:
        """Set target rotation in radians."""
        self.end_rotation = rotation
        return self

    def to_opacity(self, opacity: float) -> Self:
        """Set target opacity."""
        self.end_opacity = max(0.0, min(1.0, opacity))
        return self

    def apply(self, progress: float) -> None:
        """Apply interpolated transforms to target."""
        if not self._captured:
            self._capture_initial_state()

        if self.end_position is not None and self._start_position is not None:
            x = self._start_position[0] + (self.end_position[0] - self._start_position[0]) * progress
            y = self._start_position[1] + (self.end_position[1] - self._start_position[1]) * progress
            self.target.move_to((x, y))

        if self.end_scale is not None and self._start_scale is not None:
            scale = self._start_scale + (self.end_scale - self._start_scale) * progress
            self.target.set_scale(scale)

        if self.end_rotation is not None and self._start_rotation is not None:
            rotation = self._start_rotation + (self.end_rotation - self._start_rotation) * progress
            self.target.set_rotation(rotation)

        if self.end_opacity is not None and self._start_opacity is not None:
            opacity = self._start_opacity + (self.end_opacity - self._start_opacity) * progress
            self.target.set_opacity(opacity)

    def _capture_initial_state(self) -> None:
        """Capture initial transform state."""
        pos = self.target.position
        self._start_position = (float(pos[0]), float(pos[1]))
        self._start_scale = float(self.target.scale)
        self._start_rotation = float(self.target.rotation)
        self._start_opacity = float(self.target.opacity)
        self._captured = True

    def reset(self) -> None:
        """Reset target to initial state."""
        if self._start_position is not None:
            self.target.move_to(self._start_position)
        if self._start_scale is not None:
            self.target.set_scale(self._start_scale)
        if self._start_rotation is not None:
            self.target.set_rotation(self._start_rotation)
        if self._start_opacity is not None:
            self.target.set_opacity(self._start_opacity)
        self._captured = False


class AnimationGroup(Animation):
    """Groups multiple animations to play together or in sequence."""

    def __init__(
        self,
        *animations: Animation,
        mode: str = "parallel",
    ) -> None:
        """Initialize animation group.

        Args:
            animations: Animations to group.
            mode: "parallel" to play together, "sequence" to play one after another.
        """
        self._animations = list(animations)
        self.mode = mode

        super().__init__(duration=self._calculate_duration())

    def _calculate_duration(self) -> float:
        """Calculate total duration based on mode."""
        if not self._animations:
            return 0.0
        if self.mode == "sequence":
            return sum(a.total_duration for a in self._animations)
        return max(a.total_duration for a in self._animations)

    def add(self, *animations: Animation) -> Self:
        """Add animations to the group."""
        self._animations.extend(animations)
        self.duration = self._calculate_duration()
        return self

    def apply(self, progress: float) -> None:
        """Apply all animations at given progress."""
        if self.duration <= 0:
            return

        current_time = progress * self.duration

        if self.mode == "parallel":
            for anim in self._animations:
                anim_progress = anim.get_progress(current_time)
                anim.apply(anim_progress)
        else:  # sequence
            elapsed = 0.0
            for anim in self._animations:
                anim_total = anim.total_duration
                if current_time < elapsed + anim_total:
                    local_time = current_time - elapsed
                    anim_progress = anim.get_progress(local_time)
                    anim.apply(anim_progress)
                    break
                else:
                    anim.apply(1.0)
                elapsed += anim_total

    def reset(self) -> None:
        """Reset all animations."""
        for anim in self._animations:
            anim.reset()
