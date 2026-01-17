"""Animation system for comicode comics.

This module provides classes for animating CObjects and Effects over time,
enabling export to animated formats like GIF and video.

Example:
    from comix.animation import Timeline, EffectAnimation, ObjectAnimation

    # Create timeline
    timeline = Timeline(page)

    # Add effect animation
    timeline.add(
        EffectAnimation(shake_effect, pattern="pulse", duration=0.5)
    )

    # Add object animation
    timeline.then(
        ObjectAnimation(character, position=(400, 200), duration=1.0)
            .set_easing("ease_out_bounce")
    )

    # Render to GIF
    from comix.renderer.gif_renderer import GIFRenderer
    GIFRenderer(page).render("output.gif", timeline, fps=24, duration=2.0)
"""

from comix.animation.animation import (
    Animation,
    AnimationConfig,
    AnimationGroup,
    EffectAnimation,
    ObjectAnimation,
    PropertyAnimation,
)
from comix.animation.easing import (
    EASING_FUNCTIONS,
    EasingFunction,
    get_easing,
    register_easing,
)
from comix.animation.timeline import Timeline, TimelineEntry

__all__ = [
    # Core classes
    "Animation",
    "AnimationConfig",
    "AnimationGroup",
    "EffectAnimation",
    "ObjectAnimation",
    "PropertyAnimation",
    # Timeline
    "Timeline",
    "TimelineEntry",
    # Easing
    "EASING_FUNCTIONS",
    "EasingFunction",
    "get_easing",
    "register_easing",
]
