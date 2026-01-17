"""Timeline for orchestrating complex animation sequences.

Provides precise control over when animations start and how they overlap.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Self

if TYPE_CHECKING:
    from comix.animation.animation import Animation
    from comix.page.page import Page


@dataclass
class TimelineEntry:
    """Entry in the animation timeline."""

    animation: Animation
    start_time: float

    @property
    def end_time(self) -> float:
        """Get the time when this animation ends."""
        return self.start_time + self.animation.total_duration


class Timeline:
    """Orchestrates multiple animations over time.

    Provides precise control over when animations start and how they overlap.
    Use this for complex animation sequences with specific timing requirements.
    """

    def __init__(self, page: Page | None = None) -> None:
        """Initialize timeline.

        Args:
            page: Optional page reference for convenience methods.
        """
        self.page = page
        self._entries: list[TimelineEntry] = []
        self._current_time: float = 0.0

    @property
    def duration(self) -> float:
        """Get total timeline duration."""
        if not self._entries:
            return 0.0
        return max(entry.end_time for entry in self._entries)

    @property
    def entries(self) -> list[TimelineEntry]:
        """Get all timeline entries."""
        return self._entries.copy()

    def at(self, time: float) -> _TimelineBuilder:
        """Start adding animations at a specific time.

        Args:
            time: Time in seconds to add animations at.

        Returns:
            Builder for adding animations at the specified time.

        Example:
            timeline.at(0.5).add(fade_animation)
        """
        return _TimelineBuilder(self, time)

    def add(self, animation: Animation, start_time: float = 0.0) -> Self:
        """Add an animation at a specific start time.

        Args:
            animation: Animation to add.
            start_time: Time in seconds when animation should start.

        Returns:
            Self for method chaining.
        """
        self._entries.append(TimelineEntry(animation, start_time))
        return self

    def then(self, animation: Animation, gap: float = 0.0) -> Self:
        """Add an animation after all current animations complete.

        Args:
            animation: Animation to add.
            gap: Time gap after previous animations end.

        Returns:
            Self for method chaining.
        """
        start_time = self.duration + gap
        return self.add(animation, start_time)

    def with_previous(self, animation: Animation, offset: float = 0.0) -> Self:
        """Add an animation starting at the same time as the previous one.

        Args:
            animation: Animation to add.
            offset: Offset from previous animation's start time.

        Returns:
            Self for method chaining.
        """
        if self._entries:
            start_time = self._entries[-1].start_time + offset
        else:
            start_time = offset
        return self.add(animation, start_time)

    def apply_at_time(self, time: float) -> None:
        """Apply all animations at the given time.

        Args:
            time: Current time in seconds.
        """
        for entry in self._entries:
            if time < entry.start_time:
                continue
            local_time = time - entry.start_time
            progress = entry.animation.get_progress(local_time)
            entry.animation.apply(progress)

    def reset(self) -> None:
        """Reset all animations to their initial state."""
        for entry in self._entries:
            entry.animation.reset()

    def clear(self) -> Self:
        """Remove all animations from timeline."""
        self._entries.clear()
        return self

    def get_active_animations(self, time: float) -> list[Animation]:
        """Get animations that are active at a given time.

        Args:
            time: Time in seconds.

        Returns:
            List of active animations.
        """
        active = []
        for entry in self._entries:
            if entry.start_time <= time < entry.end_time:
                active.append(entry.animation)
        return active


class _TimelineBuilder:
    """Fluent builder for adding animations at a specific time."""

    def __init__(self, timeline: Timeline, time: float) -> None:
        self._timeline = timeline
        self._time = time

    def add(self, animation: Animation) -> Timeline:
        """Add the animation at the specified time.

        Args:
            animation: Animation to add.

        Returns:
            The parent timeline for continued chaining.
        """
        return self._timeline.add(animation, self._time)
