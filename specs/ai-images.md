# AI Image Generation - DALL-E and Replicate Integration

## What

Integration with AI image generation services (OpenAI DALL-E and Replicate) to create comic artwork from text prompts, enabling artists to generate backgrounds, characters, and other visual elements programmatically.

## Why

Creating comic artwork manually is time-consuming and requires artistic skill. AI image generation enables:

1. **Rapid prototyping**: Generate placeholder art for layout testing
2. **Background creation**: Create unique backgrounds without illustration skills
3. **Style exploration**: Experiment with different visual styles quickly
4. **Accessibility**: Enable non-artists to create visual comics
5. **Iteration**: Quickly regenerate images with different prompts

## Acceptance Criteria

### Must Have
- [x] `AIImage` class extending base `Image` class
- [x] OpenAI DALL-E provider support
- [x] Replicate provider support (Stable Diffusion)
- [x] Text prompt configuration
- [x] Synchronous generation (`generate()`)
- [x] Asynchronous generation (`generate_async()`)
- [x] Provider selection via enum or string
- [x] Generation metadata access
- [x] Integration with CObject hierarchy (positioning, opacity, etc.)

### Should Have
- [x] OpenAI quality setting (standard/hd)
- [x] OpenAI style setting (vivid/natural)
- [x] Replicate negative prompt support
- [x] Seed parameter for reproducibility
- [x] Custom model selection
- [x] Method chaining API
- [x] Detailed error messages for missing credentials

### Won't Have (This Iteration)
- [ ] Image caching across sessions
- [ ] Batch generation
- [ ] Image editing/inpainting
- [ ] Custom model fine-tuning
- [ ] Usage tracking/cost estimation

## Context

### Providers

| Provider | Model | Features | Requirements |
|----------|-------|----------|--------------|
| OpenAI | dall-e-3 | quality, style, revised prompts | OPENAI_API_KEY env var |
| Replicate | stability-ai/sdxl | negative prompts, seed, custom models | REPLICATE_API_TOKEN env var |

### OpenAI Size Mapping

DALL-E 3 supports fixed sizes. AIImage maps aspect ratios:
- Square (aspect ~1.0): 1024x1024
- Landscape (aspect > 1.5): 1792x1024
- Portrait (aspect < 0.67): 1024x1792

### Installation

```bash
# For OpenAI support
uv sync --extra ai  # or: pip install openai

# For Replicate support
uv sync --extra ai  # or: pip install replicate
```

### Environment Setup

```bash
export OPENAI_API_KEY="sk-..."
export REPLICATE_API_TOKEN="r8_..."
```

## Examples

### Example 1: Basic OpenAI Generation

```python
from comix.cobject.image import AIImage, AIProvider

ai_img = AIImage(
    prompt="A heroic samurai standing on a cliff at sunset",
    provider=AIProvider.OPENAI,
    width=512,
    height=512,
)
ai_img.generate()

# Use in a page
page.add(ai_img.move_to((400, 300)))
```

### Example 2: Replicate with Negative Prompt

```python
from comix.cobject.image import AIImage, AIProvider

ai_img = AIImage(
    prompt="A cute cartoon cat",
    provider=AIProvider.REPLICATE,
    negative_prompt="realistic, photo, ugly, deformed",
    seed=42,  # For reproducibility
)
ai_img.generate()
```

### Example 3: High-Quality OpenAI Generation

```python
ai_img = AIImage(
    prompt="An epic dragon flying over a medieval castle",
    provider=AIProvider.OPENAI,
    quality="hd",  # Higher quality
    style="vivid",  # More dramatic
)
ai_img.generate()

# Access revised prompt
metadata = ai_img.get_generation_metadata()
print(f"Model used: {metadata['model']}")
print(f"Revised prompt: {metadata.get('revised_prompt')}")
```

### Example 4: Method Chaining

```python
ai_img = (
    AIImage(prompt="initial prompt")
    .set_prompt("A serene mountain landscape at dawn")
    .set_provider(AIProvider.REPLICATE)
    .set_model("stability-ai/stable-diffusion-3")
)
ai_img.generate()
```

### Example 5: Panel Background Generation

```python
from comix import Page, Panel
from comix.cobject.image import AIImage

# Create page with AI-generated background
page = Page(width=800, height=600)
panel = Panel(width=700, height=500)

bg = AIImage(
    prompt="Futuristic cyberpunk city street at night, neon lights",
    provider="openai",
    quality="hd",
)
bg.generate()
panel.set_background(image=bg)

page.add(panel.move_to((400, 300)))
```

### Example 6: Async Generation

```python
import asyncio
from comix.cobject.image import AIImage

async def generate_images():
    images = [
        AIImage(prompt="A medieval knight"),
        AIImage(prompt="A futuristic robot"),
        AIImage(prompt="A magical wizard"),
    ]

    # Generate all images concurrently
    await asyncio.gather(*[img.generate_async() for img in images])
    return images

images = asyncio.run(generate_images())
```

## Open Questions

- [x] Support multiple providers simultaneously? **Decision**: Yes, per-image provider selection
- [x] Cache generated images? **Decision**: Images stored as base64 in memory, no persistent cache
- [x] Handle rate limiting? **Decision**: Let provider errors propagate, user handles retry
- [x] Support local models? **Decision**: Defer to future, focus on cloud APIs

## Test Requirements

1. **Provider Setup**:
   - Test: OpenAI provider requires OPENAI_API_KEY
   - Test: Replicate provider requires REPLICATE_API_TOKEN
   - Test: Clear error when package not installed
   - Test: Clear error when credentials missing

2. **Image Generation**:
   - Test: Basic generation produces image data
   - Test: is_generated flag updates correctly
   - Test: Metadata populated after generation
   - Test: Seed produces reproducible results (Replicate)

3. **Configuration**:
   - Test: Provider enum and string accepted
   - Test: Quality parameter passed to OpenAI
   - Test: Style parameter passed to OpenAI
   - Test: Negative prompt passed to Replicate
   - Test: Custom model selection works

4. **Integration**:
   - Test: AIImage renders in page
   - Test: Positioning methods work (move_to, etc.)
   - Test: Opacity and transformations apply

5. **Error Handling**:
   - Test: Missing prompt raises error
   - Test: Missing credentials raise AIGenerationError
   - Test: Network errors propagate appropriately

## Implementation Status

Fully implemented in `/comix/cobject/image/ai_image.py` with tests in `/tests/test_image.py`.

Optional dependency - requires `uv sync --extra ai` for OpenAI and Replicate packages.
