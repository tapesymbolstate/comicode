"""Video export example - Creating MP4/WebM videos from comic pages.

Demonstrates the video export system for creating video files:
- VideoRenderer for rendering MP4 and WebM videos
- Timeline integration for animated content
- Quality settings and format options
- Frame extraction for post-processing

Requires: uv sync --extra video
"""

from pathlib import Path

# Check if video dependencies are available
try:
    from comix.renderer.video_renderer import VideoRenderer, _IMAGEIO_AVAILABLE
    if not _IMAGEIO_AVAILABLE:
        raise ImportError("Video dependencies not available")
except ImportError:
    print("Video export requires additional dependencies.")
    print("Install with: uv sync --extra video")
    exit(1)

from comix import Page, Panel, Stickman
from comix.effect import ImpactEffect, ZoomEffect, FocusLines
from comix.animation import (
    Timeline,
    EffectAnimation,
    ObjectAnimation,
)


# Create output directory
output_dir = Path("examples/output")
output_dir.mkdir(parents=True, exist_ok=True)


# Example 1: Simple MP4 video - Impact burst
print("Example 1: Simple MP4 video...")
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

renderer1 = VideoRenderer(page1)
renderer1.render(
    "examples/output/15_video_impact.mp4",
    timeline1,
    fps=30,
    duration=0.8,
    format="mp4",
    quality="medium"
)
print("Created examples/output/15_video_impact.mp4")


# Example 2: WebM format video
print("\nExample 2: WebM format video...")
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

renderer2 = VideoRenderer(page2)
renderer2.render(
    "examples/output/15_video_movement.webm",
    timeline2,
    fps=30,
    duration=1.0,
    format="webm",
    quality="medium"
)
print("Created examples/output/15_video_movement.webm")


# Example 3: High quality video
print("\nExample 3: High quality video...")
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
focus.set_opacity(0.0)
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

renderer3 = VideoRenderer(page3)
renderer3.render(
    "examples/output/15_video_focus_hq.mp4",
    timeline3,
    fps=30,
    duration=1.0,
    format="mp4",
    quality="high"
)
print("Created examples/output/15_video_focus_hq.mp4")


# Example 4: Complex animation video
print("\nExample 4: Complex animation video...")
page4 = Page(width=600, height=400)
panel4 = Panel()

attacker = Stickman(name="Attacker")
attacker.move_to((150, 220))
attacker.set_pose("running")
attacker.set_expression("angry")

target = Stickman(name="Target", color="#666666")
target.move_to((450, 220))
target.set_expression("scared")

panel4.add_content(attacker, target)
page4.add(panel4)

attack_impact = ImpactEffect(position=(380, 200), seed=42)
attack_impact.set_num_spikes(14).set_radii(inner=20.0, outer=60.0)
attack_impact.set_opacity(0.0)

page4.add_effect(attack_impact)

timeline4 = Timeline(page4)
timeline4.add(
    ObjectAnimation(attacker, position=(320, 220), duration=0.5)
    .set_easing("ease_in")
)
timeline4.at(0.4).add(
    EffectAnimation(attack_impact, pattern="grow", duration=0.15)
    .set_easing("ease_out")
)
timeline4.at(0.55).add(
    EffectAnimation(attack_impact, pattern="fade_out", duration=0.25)
)

renderer4 = VideoRenderer(page4)
renderer4.render(
    "examples/output/15_video_attack.mp4",
    timeline4,
    fps=30,
    duration=0.8,
    format="mp4",
    quality="medium"
)
print("Created examples/output/15_video_attack.mp4")


# Example 5: Progress callback
print("\nExample 5: Video with progress tracking...")

def show_progress(current: int, total: int) -> None:
    percent = (current / total) * 100
    print(f"  Rendering frame {current}/{total} ({percent:.0f}%)", end="\r")

page5 = Page(width=400, height=400)
panel5 = Panel()
char5 = Stickman(name="Bounce")
char5.move_to((100, 200))
char5.set_expression("happy")
panel5.add_content(char5)
page5.add(panel5)

timeline5 = Timeline(page5)
timeline5.add(
    ObjectAnimation(char5, position=(300, 200), duration=0.6)
    .set_easing("ease_out_bounce")
)
timeline5.then(
    ObjectAnimation(char5, position=(100, 200), duration=0.6)
    .set_easing("ease_out_elastic")
)

renderer5 = VideoRenderer(page5)
renderer5.render(
    "examples/output/15_video_bounce.mp4",
    timeline5,
    fps=30,
    duration=1.2,
    progress_callback=show_progress
)
print("\nCreated examples/output/15_video_bounce.mp4")


# Example 6: Extract frames for post-processing
print("\nExample 6: Frame extraction...")
page6 = Page(width=300, height=300)
panel6 = Panel()
char6 = Stickman(name="Spin")
char6.move_to((150, 170))
char6.set_expression("excited")
panel6.add_content(char6)
page6.add(panel6)

zoom_effect = ZoomEffect(target=char6, seed=42)
zoom_effect.set_num_lines(20).set_opacity(0.0)
page6.add_effect(zoom_effect)

timeline6 = Timeline(page6)
timeline6.add(
    EffectAnimation(zoom_effect, pattern="fade_in", duration=0.5)
)

renderer6 = VideoRenderer(page6)
frame_paths = renderer6.render_frames(
    "examples/output/15_video_frames",
    timeline6,
    fps=10,
    duration=0.5,
    quality="medium",
    format="png"
)
print(f"Extracted {len(frame_paths)} frames to examples/output/15_video_frames/")


print("\n" + "="*50)
print("All video export examples completed!")
print("="*50)
print("\nVideo export features:")
print("  - MP4 format: Widely compatible, good compression")
print("  - WebM format: Web-optimized, open source codec")
print("  - Quality levels: low (72 DPI), medium (96 DPI), high (150 DPI)")
print("  - Progress callback: Track rendering progress")
print("  - Frame extraction: Export individual frames for post-processing")
print("\nInstall video dependencies with: uv sync --extra video")
