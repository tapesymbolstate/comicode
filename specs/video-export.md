# Video Export

## What

Export comic pages with animations to MP4 and WebM video files, with support for quality settings, audio tracks, frame extraction, and progress tracking.

## Why

While GIFs work well for short loops, video formats are better for longer animations and professional output. Video export enables:

1. **High-quality output**: H.264 (MP4) and VP9 (WebM) offer superior compression and quality
2. **Audio integration**: Add background music or narration to animated comics
3. **Platform compatibility**: MP4 is universally supported; WebM is optimized for web
4. **Professional workflows**: Frame extraction enables post-processing in video editors
5. **Longer animations**: Videos handle extended durations better than GIFs

## Acceptance Criteria

### Must Have
- [x] VideoRenderer class for MP4 and WebM output
- [x] Quality settings: low (72 DPI), medium (96 DPI), high (150 DPI)
- [x] FPS configuration (1-60, default 30)
- [x] Duration configuration (minimum 0.1 seconds)
- [x] Timeline integration for animations
- [x] MP4 format with H.264 codec (libx264)
- [x] WebM format with VP9 codec (libvpx-vp9)
- [x] Automatic even dimension adjustment (required by video codecs)

### Should Have
- [x] Audio track support with automatic mixing
- [x] Progress callback for rendering status
- [x] Frame extraction to directory (PNG and JPG formats)
- [x] CRF-based quality control for optimal file size
- [x] Automatic directory creation for output files
- [x] Graceful dependency checking with helpful error messages

### Won't Have (This Iteration)
- [ ] Multiple audio tracks
- [ ] Audio volume control
- [ ] Video transitions between pages
- [ ] Hardware-accelerated encoding
- [ ] Streaming output
- [ ] Custom codec parameters

## Context

### User Flow

1. Create Page with content and optionally create Timeline with animations
2. Instantiate `VideoRenderer(page)`
3. Call `render("output.mp4", timeline, ...)` with desired options
4. Share or post-process the resulting video file

### Dependencies

Video export requires optional dependencies:
```bash
uv sync --extra video
```

This installs:
- **Pillow**: Image processing
- **pycairo**: Cairo rendering backend
- **imageio-ffmpeg**: FFmpeg-based video encoding

### Video Codec Details

| Format | Codec | Constant | Pixel Format |
|--------|-------|----------|--------------|
| MP4 | H.264 | libx264 | yuv420p |
| WebM | VP9 | libvpx-vp9 | yuv420p |

### Quality Settings

| Quality | DPI | CRF | Default Bitrate | Use Case |
|---------|-----|-----|-----------------|----------|
| low | 72 | 28 | 1M | Quick preview, small file |
| medium | 96 | 23 | 2M | Balanced (default) |
| high | 150 | 18 | 5M | High quality, larger file |

CRF (Constant Rate Factor) controls quality: lower = better quality, larger file.

### Dimension Handling

Video codecs require even dimensions. VideoRenderer automatically adjusts:
```python
if width % 2 != 0:
    width += 1
if height % 2 != 0:
    height += 1
```

Dimensions are also scaled based on DPI:
```python
scale = dpi / 72.0  # Base DPI is 72 (screen standard)
width = int(page.width * scale)
height = int(page.height * scale)
```

### Audio Mixing

When an audio file is provided:
1. Video is rendered to a temporary file
2. FFmpeg mixes audio with video using AAC codec
3. `-shortest` flag ensures output matches shorter of audio/video
4. Temporary file is cleaned up automatically

## Examples

### Example 1: Basic MP4 Export

```python
from comix import Page, Panel, Stickman
from comix.renderer.video_renderer import VideoRenderer

page = Page(width=800, height=600)
panel = Panel(width=760, height=560)
char = Stickman(name="Star", height=100)
char.move_to((380, 300))
panel.add_content(char)
page.add(panel)

renderer = VideoRenderer(page)
renderer.render("output.mp4", fps=30, duration=2.0)
```

### Example 2: Animated Video with Timeline

```python
from comix import Page, Panel, Stickman
from comix.animation import Timeline, ObjectAnimation
from comix.renderer.video_renderer import VideoRenderer

page = Page(width=800, height=600)
panel = Panel(width=760, height=560)
char = Stickman(name="Mover", height=80)
char.move_to((100, 300))
panel.add_content(char)
page.add(panel)

timeline = Timeline(page)
timeline.add(
    ObjectAnimation(char, duration=2.0)
    .to_position(700, 300)
    .set_easing("ease_in_out_cubic")
)

renderer = VideoRenderer(page)
renderer.render(
    "animated.mp4",
    timeline,
    fps=30,
    duration=2.0,
    quality="high"
)
```

### Example 3: Video with Audio Track

```python
from comix import Page, Panel, Stickman
from comix.animation import Timeline, EffectAnimation
from comix.effect.effect import ShakeEffect
from comix.renderer.video_renderer import VideoRenderer

page = Page(width=600, height=400)
panel = Panel(width=560, height=360)
char = Stickman(name="Dancer", height=80)
char.move_to((280, 200))
effect = ShakeEffect(target=char, intensity=0.5)
panel.add_content(char, effect)
page.add(panel)

timeline = Timeline(page)
timeline.add(EffectAnimation(effect, pattern="pulse", duration=3.0))

renderer = VideoRenderer(page)
renderer.render(
    "with_music.mp4",
    timeline,
    fps=30,
    duration=3.0,
    audio_path="background.mp3"
)
```

### Example 4: WebM Format Export

```python
from comix import Page, Panel, Stickman
from comix.renderer.video_renderer import VideoRenderer

page = Page(width=640, height=480)
panel = Panel(width=600, height=440)
char = Stickman(name="Web", height=80)
char.move_to((300, 240))
panel.add_content(char)
page.add(panel)

renderer = VideoRenderer(page)
renderer.render(
    "output.webm",
    fps=24,
    duration=1.0,
    format="webm",
    quality="medium"
)
```

### Example 5: Frame Extraction

```python
from comix import Page, Panel, Stickman
from comix.animation import Timeline, ObjectAnimation
from comix.renderer.video_renderer import VideoRenderer

page = Page(width=400, height=300)
panel = Panel(width=360, height=260)
char = Stickman(name="Spinner", height=60)
char.move_to((180, 150))
panel.add_content(char)
page.add(panel)

timeline = Timeline(page)
timeline.add(ObjectAnimation(char, duration=1.0).to_rotation(6.28))

renderer = VideoRenderer(page)
frame_paths = renderer.render_frames(
    "frames/",
    timeline,
    fps=24,
    duration=1.0,
    format="png"
)
print(f"Extracted {len(frame_paths)} frames")
```

### Example 6: Progress Tracking

```python
from comix import Page, Panel, Stickman
from comix.renderer.video_renderer import VideoRenderer

page = Page(width=800, height=600)
panel = Panel(width=760, height=560)
char = Stickman(name="Progress", height=100)
char.move_to((380, 300))
panel.add_content(char)
page.add(panel)

def on_progress(current: int, total: int) -> None:
    percent = (current / total) * 100
    print(f"Rendering: {current}/{total} ({percent:.1f}%)")

renderer = VideoRenderer(page)
renderer.render(
    "tracked.mp4",
    fps=30,
    duration=5.0,
    progress_callback=on_progress
)
```

### Example 7: High-Quality Production Export

```python
from comix import Page, Panel, Stickman
from comix.animation import Timeline, ObjectAnimation, EffectAnimation
from comix.effect.effect import ZoomEffect
from comix.renderer.video_renderer import VideoRenderer

page = Page(width=1920, height=1080)
panel = Panel(width=1880, height=1040)
char = Stickman(name="Hero", height=200)
char.move_to((960, 540))
effect = ZoomEffect(target=char, intensity=0.8)
panel.add_content(char, effect)
page.add(panel)

timeline = Timeline(page)
timeline.add(EffectAnimation(effect, pattern="zoom_burst", duration=2.0))

renderer = VideoRenderer(page)
renderer.render(
    "production.mp4",
    timeline,
    fps=60,
    duration=2.0,
    quality="high",
    audio_path="epic_music.mp3"
)
```

## API Reference

### VideoRenderer Constructor

```python
def __init__(self, page: Page) -> None
```

Raises `ImportError` if dependencies are not installed.

### render() Method

```python
def render(
    self,
    output_path: str,
    timeline: Timeline | None = None,
    *,
    fps: int = 30,
    duration: float = 1.0,
    format: Literal["mp4", "webm"] = "mp4",
    quality: Literal["low", "medium", "high"] = "medium",
    bitrate: str | None = None,
    audio_path: str | None = None,
    progress_callback: Callable[[int, int], None] | None = None,
) -> str
```

**Parameters:**
- `output_path`: Destination file path
- `timeline`: Optional animation timeline
- `fps`: Frames per second (1-60, clamped)
- `duration`: Video duration in seconds (min 0.1)
- `format`: "mp4" or "webm"
- `quality`: "low", "medium", or "high"
- `bitrate`: Override bitrate (e.g., "2M")
- `audio_path`: Path to audio file for mixing
- `progress_callback`: Called with (current_frame, total_frames)

**Returns:** Path to rendered video file

### render_frames() Method

```python
def render_frames(
    self,
    output_dir: str,
    timeline: Timeline | None = None,
    *,
    fps: int = 30,
    duration: float = 1.0,
    quality: Literal["low", "medium", "high"] = "medium",
    format: str = "png",
    progress_callback: Callable[[int, int], None] | None = None,
) -> list[str]
```

**Parameters:**
- `output_dir`: Directory for frame files
- `timeline`: Optional animation timeline
- `fps`: Frames per second (1-60, clamped)
- `duration`: Total duration in seconds (min 0.1)
- `quality`: "low", "medium", or "high"
- `format`: "png" or "jpg"/"jpeg"
- `progress_callback`: Called with (current_frame, total_frames)

**Returns:** List of paths to rendered frame files (frame_0000.ext, frame_0001.ext, ...)

## Related Specs

- [Animation Export](animation-export.md) - GIF export and animation system
- [Page Rendering](page-rendering.md) - Core rendering concepts
- [Effect System](effect-system.md) - Visual effects that can be animated

## Test Requirements

1. **VideoRenderer Initialization**:
   - Test: Constructor accepts Page object
   - Test: ImportError when dependencies missing
   - Test: DPI constants defined correctly

2. **Basic Rendering**:
   - Test: MP4 file created successfully
   - Test: WebM file created successfully
   - Test: Static video without timeline
   - Test: Animated video with timeline

3. **Quality Settings**:
   - Test: Low quality uses DPI_LOW (72)
   - Test: Medium quality uses DPI_MEDIUM (96)
   - Test: High quality uses DPI_HIGH (150)
   - Test: CRF values correct for each quality

4. **Parameter Clamping**:
   - Test: FPS < 1 clamped to 1
   - Test: FPS > 60 clamped to 60
   - Test: Duration < 0.1 clamped to 0.1

5. **Dimension Handling**:
   - Test: Odd dimensions adjusted to even
   - Test: Large dimensions render correctly

6. **Frame Extraction**:
   - Test: Creates directory if needed
   - Test: PNG format preserves alpha
   - Test: JPG format converts to RGB
   - Test: Frame naming is zero-padded

7. **Progress Callback**:
   - Test: Called for each frame
   - Test: Parameters are (current, total)
   - Test: Works for both render() and render_frames()

8. **Audio Support**:
   - Test: audio_path parameter accepted
   - Test: _add_audio_track method exists

## Implementation Status

Fully implemented in:
- `/comix/renderer/video_renderer.py` - VideoRenderer class

Tests in:
- `/tests/test_video_renderer.py` (25 tests)

Working example: `/examples/15_video_export.py`
