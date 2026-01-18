"""Visual effects example - Manga-style dramatic effects.

Demonstrates the 6 effect types available in the effects system:
ShakeEffect, ZoomEffect, MotionLines, FocusLines, AppearEffect, ImpactEffect
"""
# Status: ✅ Working (v0.1.108)

import math
from comix import Page, Panel, Stickman
from comix.effect import (
    ShakeEffect,
    ZoomEffect,
    MotionLines,
    FocusLines,
    AppearEffect,
    ImpactEffect,
)

# Example 1: ShakeEffect - Character trembling with fear
page1 = Page(width=400, height=400)
panel1 = Panel()
char1 = Stickman(name="Scared")
char1.move_to((200, 220))
char1.set_expression("scared")
bubble1 = char1.say("I'm so scared!")
panel1.add_content(char1, bubble1)
page1.add(panel1)

shake = ShakeEffect(target=char1, seed=42)
shake.set_intensity(0.8).set_shake_distance(8.0).set_num_copies(4)
page1.add_effect(shake)
page1.render("examples/output/13_effect_shake.png")
print("Created examples/output/13_effect_shake.png")


# Example 2: ZoomEffect - Radial speed lines for emphasis
page2 = Page(width=400, height=400)
panel2 = Panel()
char2 = Stickman(name="Focused")
char2.move_to((200, 220))
char2.set_expression("surprised")
bubble2 = char2.say("WHAT?!")
panel2.add_content(char2, bubble2)
page2.add(panel2)

zoom = ZoomEffect(target=char2, seed=42)
zoom.set_num_lines(32).set_radii(inner=60.0, outer=180.0)
page2.add_effect(zoom)
page2.render("examples/output/13_effect_zoom.png")
print("Created examples/output/13_effect_zoom.png")


# Example 3: MotionLines - Character moving fast
page3 = Page(width=500, height=400)
panel3 = Panel()
char3 = Stickman(name="Runner")
char3.move_to((300, 220))
char3.set_pose("running")
panel3.add_content(char3)
page3.add(panel3)

motion = MotionLines(target=char3, seed=42)
motion.set_direction(math.pi)  # Moving left
motion.set_num_lines(16).set_line_length(120.0).set_spread(60.0)
page3.add_effect(motion)
page3.render("examples/output/13_effect_motion.png")
print("Created examples/output/13_effect_motion.png")


# Example 4: FocusLines - Dramatic focus effect
page4 = Page(width=500, height=500)
panel4 = Panel()
char4 = Stickman(name="Hero")
char4.move_to((250, 280))
char4.set_expression("angry")
char4.set_pose("pointing")
bubble4 = char4.shout("I WILL STOP YOU!")
panel4.add_content(char4, bubble4)
page4.add(panel4)

focus = FocusLines(target=char4, seed=42)
focus.set_num_lines(48).set_inner_gap(90.0).set_outer_radius(280.0)
focus.set_fill_background(True, "#FFFFFF")
page4.add_effect(focus)
page4.render("examples/output/13_effect_focus.png")
print("Created examples/output/13_effect_focus.png")


# Example 5: AppearEffect styles - Character materialization
page5 = Page(width=800, height=400)
page5.set_layout(rows=1, cols=4)

styles = ["sparkle", "fade", "flash", "reveal"]
for i, style in enumerate(styles):
    panel = Panel()
    char = Stickman(name=style.capitalize())
    char.move_to((100, 200))
    char.set_expression("excited")
    panel.add_content(char)
    page5.add(panel)

page5.auto_layout()

# Add effects after layout so positions are correct
for i, style in enumerate(styles):
    effect = AppearEffect(position=(100 + i * 200, 200), style=style, seed=42)
    effect.set_intensity(0.9).set_radius(70.0)
    if style == "sparkle":
        effect.set_glow_color("#FFD700")  # Gold sparkles
    page5.add_effect(effect)

page5.render("examples/output/13_effect_appear.png")
print("Created examples/output/13_effect_appear.png")


# Example 6: ImpactEffect - Explosion/collision burst
page6 = Page(width=400, height=400)
panel6 = Panel()
# Position the impact point
page6.add(panel6)

impact = ImpactEffect(position=(200, 200), seed=42)
impact.set_num_spikes(16).set_radii(inner=30.0, outer=80.0)
impact.set_color("#FF0000")
page6.add_effect(impact)
page6.render("examples/output/13_effect_impact.png")
print("Created examples/output/13_effect_impact.png")


# Example 7: Combined effects - Action scene
page7 = Page(width=600, height=500)
panel7 = Panel()

# Hero character with focus lines
hero = Stickman(name="Hero")
hero.move_to((200, 280))
hero.set_expression("angry")
hero.set_pose("pointing")

# Villain character with shake effect
villain = Stickman(name="Villain", color="#8B0000")
villain.move_to((450, 280))
villain.set_expression("scared")

bubble_hero = hero.shout("Take this!")
bubble_villain = villain.say("No...!")

panel7.add_content(hero, villain, bubble_hero, bubble_villain)
page7.add(panel7)

# Add multiple effects
focus_effect = FocusLines(target=hero, seed=42)
focus_effect.set_num_lines(24).set_inner_gap(80.0).set_outer_radius(150.0)
focus_effect.set_opacity(0.4)

shake_effect = ShakeEffect(target=villain, seed=42)
shake_effect.set_intensity(0.7).set_shake_distance(6.0)

impact_effect = ImpactEffect(position=(330, 250), seed=42)
impact_effect.set_num_spikes(12).set_radii(inner=15.0, outer=45.0)

page7.add_effect(focus_effect, shake_effect, impact_effect)
page7.render("examples/output/13_effect_combined.png")
print("Created examples/output/13_effect_combined.png")


print("\nAll effect examples completed!")
print("Effects add manga-style drama and motion to static comic panels.")
