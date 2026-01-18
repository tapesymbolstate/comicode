"""AI image generation example - Creating images with DALL-E and Replicate.

Demonstrates the AI image generation system for comic artwork:
- AIImage class for generating images from text prompts
- OpenAI DALL-E provider with quality and style settings
- Replicate provider with negative prompts and seed control
- Integration with pages and panels as backgrounds
- Method chaining API

Requires: uv sync --extra ai
Environment: OPENAI_API_KEY and/or REPLICATE_API_TOKEN
"""
# Status: ✅ Working (v0.1.108)

import os
from pathlib import Path

from comix import Page, Panel, Stickman
from comix.cobject.image import AIImage, AIProvider

output_dir = Path("examples/output")
output_dir.mkdir(parents=True, exist_ok=True)

openai_available = bool(os.environ.get("OPENAI_API_KEY"))
replicate_available = bool(os.environ.get("REPLICATE_API_TOKEN"))

if not openai_available and not replicate_available:
    print("AI Image Generation Examples")
    print("=" * 50)
    print()
    print("This example requires API credentials to generate images.")
    print("Set one or both environment variables:")
    print("  - OPENAI_API_KEY: For OpenAI DALL-E generation")
    print("  - REPLICATE_API_TOKEN: For Replicate/Stable Diffusion generation")
    print()
    print("Install dependencies with: uv sync --extra ai")
    print()
    print("Below are code examples showing how to use the AI image features:")
    print()


print("Example 1: Basic AIImage setup (no generation)")
print("-" * 50)
ai_img = AIImage(
    prompt="A heroic samurai standing on a cliff at sunset",
    provider=AIProvider.OPENAI,
    width=512,
    height=512,
)
print(f"  Created AIImage with prompt: '{ai_img.prompt[:40]}...'")
print(f"  Provider: {ai_img.provider}")
print(f"  Size: {ai_img.width}x{ai_img.height}")
print(f"  Is generated: {ai_img.is_generated}")
print()


print("Example 2: Replicate configuration with negative prompt")
print("-" * 50)
ai_img_replicate = AIImage(
    prompt="A cute cartoon cat sitting on a windowsill",
    provider=AIProvider.REPLICATE,
    negative_prompt="realistic, photo, ugly, deformed, blurry",
    seed=42,
    width=512,
    height=512,
)
print(f"  Prompt: '{ai_img_replicate.prompt}'")
print(f"  Negative prompt: '{ai_img_replicate.negative_prompt}'")
print(f"  Seed: {ai_img_replicate.seed}")
print()


print("Example 3: Method chaining API")
print("-" * 50)
ai_img_chained = (
    AIImage(prompt="initial prompt", seed=123)
    .set_prompt("A serene mountain landscape at dawn with mist")
    .set_provider(AIProvider.REPLICATE)
)
print(f"  Final prompt: '{ai_img_chained.prompt}'")
print(f"  Provider: {ai_img_chained.provider}")
print(f"  Seed: {ai_img_chained.seed}")
print()


print("Example 4: OpenAI quality and style settings")
print("-" * 50)
ai_img_hq = AIImage(
    prompt="An epic dragon flying over a medieval castle at night",
    provider=AIProvider.OPENAI,
    quality="hd",
    style="vivid",
    width=1024,
    height=1024,
)
print(f"  Quality: {ai_img_hq.quality}")
print(f"  Style: {ai_img_hq.image_style}")
print(f"  Size: {ai_img_hq.width}x{ai_img_hq.height}")
print()


print("Example 5: Integration with Page and Panel")
print("-" * 50)
page = Page(width=800, height=600)
panel = Panel()

char = Stickman(name="Hero")
char.move_to((200, 350))
char.set_expression("excited")
bubble = char.say("Look at this view!")

background = AIImage(
    prompt="Futuristic cyberpunk city street at night, neon lights, rain",
    provider=AIProvider.OPENAI,
    quality="hd",
    width=800,
    height=600,
)
background.move_to((400, 300))

panel.add_content(char, bubble)
page.add(panel)
print("  Created page with character ready for AI background")
print("  Background prompt: 'Futuristic cyberpunk city...'")
print()


if openai_available:
    print("Example 6: Actual OpenAI generation")
    print("-" * 50)
    print("  Generating image with DALL-E (this may take a moment)...")

    try:
        live_img = AIImage(
            prompt="A simple cartoon sun with a happy face, minimal style",
            provider=AIProvider.OPENAI,
            quality="standard",
            style="natural",
            width=256,
            height=256,
        )
        live_img.generate()

        print("  Generation successful!")
        print(f"  Is generated: {live_img.is_generated}")

        metadata = live_img.get_generation_metadata()
        print(f"  Model: {metadata.get('model', 'N/A')}")
        if metadata.get('revised_prompt'):
            print(f"  Revised prompt: '{metadata['revised_prompt'][:50]}...'")

        live_page = Page(width=300, height=300)
        live_panel = Panel()
        live_img.move_to((150, 150))
        live_panel.add_content(live_img)
        live_page.add(live_panel)
        live_page.render("examples/output/17_ai_openai_generated.png")
        print("  Saved to examples/output/17_ai_openai_generated.png")
    except Exception as e:
        print(f"  Generation failed: {e}")
    print()


if replicate_available:
    print("Example 7: Actual Replicate generation")
    print("-" * 50)
    print("  Generating image with Stable Diffusion (this may take a moment)...")

    try:
        rep_img = AIImage(
            prompt="A pixel art style robot character, 8-bit retro game style",
            provider=AIProvider.REPLICATE,
            negative_prompt="realistic, 3d, complex, detailed",
            seed=42,
            width=512,
            height=512,
        )
        rep_img.generate()

        print("  Generation successful!")
        print(f"  Is generated: {rep_img.is_generated}")

        rep_page = Page(width=560, height=560)
        rep_panel = Panel()
        rep_img.move_to((280, 280))
        rep_panel.add_content(rep_img)
        rep_page.add(rep_panel)
        rep_page.render("examples/output/17_ai_replicate_generated.png")
        print("  Saved to examples/output/17_ai_replicate_generated.png")
    except Exception as e:
        print(f"  Generation failed: {e}")
    print()


print("=" * 50)
print("AI Image Generation Examples Complete")
print("=" * 50)
print()
print("AI Image features:")
print("  - OpenAI DALL-E: quality (standard/hd), style (vivid/natural)")
print("  - Replicate: negative_prompt, seed for reproducibility")
print("  - Method chaining: set_prompt(), set_provider(), set_seed()")
print("  - CObject integration: move_to(), set_opacity(), etc.")
print("  - Async support: generate_async() for concurrent generation")
print()
print("Setup:")
print("  1. Install: uv sync --extra ai")
print("  2. Set OPENAI_API_KEY for DALL-E")
print("  3. Set REPLICATE_API_TOKEN for Stable Diffusion")
