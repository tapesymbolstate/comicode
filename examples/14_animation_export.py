"""Animation export example - Creating animated GIFs from comic pages.

Demonstrates the animation system for exporting animated GIFs:
- Timeline for orchestrating animations
- EffectAnimation for animating visual effects
- ObjectAnimation for animating character movement
- AnimationGroup for parallel/sequential animations
- Various easing functions for smooth motion
"""
# Status: ✅ Working (v0.1.108)

from comix import Page, Panel, Stickman
from comix.effect import ImpactEffect, ZoomEffect, FocusLines
from comix.animation import (
    Timeline,
    EffectAnimation,
    ObjectAnimation,
    AnimationGroup,
)


# Example 1: Simple effect animation - Impact burst
print("Example 1: Simple effect animation...")
page1 = Page(width=400, height=400)
panel1 = Panel()
char1 = Stickman(name="Hero")
char1.move_to((200, 220))
char1.set_expression("surprised")
bubble1 = char1.say("POW!")
panel1.add_content(char1, bubble1)
page1.add(panel1)

impact = ImpactEffect(target=char1, seed=42)
impact.set_num_spikes(12).set_radii(inner=25.0, outer=70.0)
page1.add_effect(impact)

timeline1 = Timeline(page1)
timeline1.add(EffectAnimation(impact, pattern="grow", duration=0.3).set_easing("ease_out"))
timeline1.then(EffectAnimation(impact, pattern="fade_out", duration=0.5).set_easing("ease_in"))

page1.animate("examples/output/14_anim_impact.gif", timeline1, fps=24, duration=0.8)
print("Created examples/output/14_anim_impact.gif")


# Example 2: Character movement animation
print("\nExample 2: Character movement animation...")
page2 = Page(width=500, height=300)
panel2 = Panel()
runner = Stickman(name="Runner")
runner.move_to((100, 180))
runner.set_pose("running")
panel2.add_content(runner)
page2.add(panel2)

timeline2 = Timeline(page2)
timeline2.add(
    ObjectAnimation(runner, position=(400, 180), duration=1.0)
    .set_easing("ease_in_out")
)

page2.animate("examples/output/14_anim_movement.gif", timeline2, fps=24, duration=1.0)
print("Created examples/output/14_anim_movement.gif")


# Example 3: Focus lines with zoom effect
print("\nExample 3: Dramatic focus effect...")
page3 = Page(width=400, height=400)
panel3 = Panel()
char3 = Stickman(name="Focus")
char3.move_to((200, 220))
char3.set_expression("angry")
bubble3 = char3.shout("NOW!")
panel3.add_content(char3, bubble3)
page3.add(panel3)

focus = FocusLines(target=char3, seed=42)
focus.set_num_lines(36).set_inner_gap(70.0).set_outer_radius(180.0)
focus.set_opacity(0.0)  # Start invisible
page3.add_effect(focus)

timeline3 = Timeline(page3)
timeline3.add(
    EffectAnimation(focus, pattern="fade_in", duration=0.4)
    .set_easing("ease_out")
)
timeline3.then(
    EffectAnimation(focus, pattern="pulse", duration=0.6)
    .set_easing("linear")
)

page3.animate("examples/output/14_anim_focus.gif", timeline3, fps=24, duration=1.0)
print("Created examples/output/14_anim_focus.gif")


# Example 4: Parallel animations - Multiple effects at once
print("\nExample 4: Parallel animations...")
page4 = Page(width=500, height=400)
panel4 = Panel()
char4 = Stickman(name="Action")
char4.move_to((250, 220))
char4.set_expression("excited")
panel4.add_content(char4)
page4.add(panel4)

zoom = ZoomEffect(target=char4, seed=42)
zoom.set_num_lines(24).set_radii(inner=50.0, outer=150.0)
zoom.set_opacity(0.0)

impact2 = ImpactEffect(target=char4, seed=43)
impact2.set_num_spikes(8).set_radii(inner=20.0, outer=50.0)
impact2.set_opacity(0.0)

page4.add_effect(zoom, impact2)

timeline4 = Timeline(page4)
timeline4.add(
    AnimationGroup(
        EffectAnimation(zoom, pattern="fade_in", duration=0.5).set_easing("ease_out"),
        EffectAnimation(impact2, pattern="grow", duration=0.3).set_delay(0.2).set_easing("ease_out"),
        mode="parallel",
    )
)
timeline4.then(
    AnimationGroup(
        EffectAnimation(zoom, pattern="fade_out", duration=0.4),
        EffectAnimation(impact2, pattern="fade_out", duration=0.3),
        mode="parallel",
    )
)

page4.animate("examples/output/14_anim_parallel.gif", timeline4, fps=24, duration=1.0)
print("Created examples/output/14_anim_parallel.gif")


# Example 5: Sequential animations - Effects one after another
print("\nExample 5: Sequential animations...")
page5 = Page(width=500, height=400)
panel5 = Panel()

hero = Stickman(name="Hero")
hero.move_to((150, 240))
hero.set_expression("angry")
hero.set_pose("pointing")

villain = Stickman(name="Villain", color="#8B0000")
villain.move_to((350, 240))
villain.set_expression("neutral")

panel5.add_content(hero, villain)
page5.add(panel5)

zoom_hero = ZoomEffect(target=hero, seed=42)
zoom_hero.set_num_lines(20).set_opacity(0.0)

impact_villain = ImpactEffect(target=villain, seed=43)
impact_villain.set_num_spikes(10).set_opacity(0.0)

page5.add_effect(zoom_hero, impact_villain)

timeline5 = Timeline(page5)
# Hero powers up first
timeline5.add(
    EffectAnimation(zoom_hero, pattern="fade_in", duration=0.4)
    .set_easing("ease_out")
)
# Then impact on villain
timeline5.then(
    EffectAnimation(impact_villain, pattern="grow", duration=0.2)
    .set_easing("ease_out"),
    gap=0.1,
)
# Both fade out
timeline5.then(
    AnimationGroup(
        EffectAnimation(zoom_hero, pattern="fade_out", duration=0.3),
        EffectAnimation(impact_villain, pattern="fade_out", duration=0.3),
        mode="parallel",
    )
)

page5.animate("examples/output/14_anim_sequence.gif", timeline5, fps=24, duration=1.2)
print("Created examples/output/14_anim_sequence.gif")


# Example 6: Combined movement and effects
print("\nExample 6: Movement with effects...")
page6 = Page(width=600, height=400)
panel6 = Panel()

attacker = Stickman(name="Attacker")
attacker.move_to((150, 220))
attacker.set_pose("running")
attacker.set_expression("angry")

target = Stickman(name="Target", color="#666666")
target.move_to((450, 220))
target.set_expression("scared")

panel6.add_content(attacker, target)
page6.add(panel6)

attack_impact = ImpactEffect(position=(380, 200), seed=42)
attack_impact.set_num_spikes(14).set_radii(inner=20.0, outer=60.0)
attack_impact.set_opacity(0.0)

page6.add_effect(attack_impact)

timeline6 = Timeline(page6)
# Attacker rushes forward
timeline6.add(
    ObjectAnimation(attacker, position=(320, 220), duration=0.5)
    .set_easing("ease_in")
)
# Impact appears on hit
timeline6.at(0.4).add(
    EffectAnimation(attack_impact, pattern="grow", duration=0.15)
    .set_easing("ease_out")
)
# Impact fades and attacker stops
timeline6.at(0.55).add(
    EffectAnimation(attack_impact, pattern="fade_out", duration=0.25)
)

page6.animate("examples/output/14_anim_attack.gif", timeline6, fps=30, duration=0.8)
print("Created examples/output/14_anim_attack.gif")


# Example 7: Easing function showcase
print("\nExample 7: Easing function showcase...")
page7 = Page(width=500, height=400)
panel7 = Panel()
char7 = Stickman(name="Bounce")
char7.move_to((100, 200))
char7.set_expression("happy")
panel7.add_content(char7)
page7.add(panel7)

timeline7 = Timeline(page7)
# Move right with bounce easing
timeline7.add(
    ObjectAnimation(char7, position=(400, 200), duration=0.8)
    .set_easing("ease_out_bounce")
)
# Move back with elastic easing
timeline7.then(
    ObjectAnimation(char7, position=(100, 200), duration=0.8)
    .set_easing("ease_out_elastic")
)

page7.animate("examples/output/14_anim_easing.gif", timeline7, fps=30, duration=1.6)
print("Created examples/output/14_anim_easing.gif")


print("\nAll animation examples completed!")
print("Animation exports add motion and life to static comic panels.")
print("\nAvailable animation patterns:")
print("  - pulse: Pulsating intensity")
print("  - fade_in: Fade from transparent to opaque")
print("  - fade_out: Fade from opaque to transparent")
print("  - grow: Grow from nothing to full size")
print("  - shrink: Shrink from full size to nothing")
print("\nAvailable easing functions:")
print("  - linear, ease_in, ease_out, ease_in_out")
print("  - ease_out_bounce, ease_in_bounce")
print("  - ease_out_elastic, ease_in_elastic")
print("  - ease_out_back, ease_in_back")
print("  - ...and many more!")
