"""GIF Renderer - exports animated GIFs from comicode pages.

Requires optional 'animation' dependencies:
    uv sync --extra animation
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Callable, Literal

try:
    from PIL import Image
except ImportError:
    Image = None  # type: ignore[assignment]

try:
    import cairo
except ImportError:
    cairo = None  # type: ignore[assignment]

if TYPE_CHECKING:
    from comix.animation.timeline import Timeline
    from comix.page.page import Page


class GIFRenderer:
    """Renders animated GIF from a Page with animations.

    Requires optional 'animation' dependencies:
        uv sync --extra animation

    Example:
        from comix.animation import Timeline, EffectAnimation
        from comix.renderer.gif_renderer import GIFRenderer

        timeline = Timeline(page)
        timeline.add(EffectAnimation(effect, pattern="pulse", duration=0.5))

        renderer = GIFRenderer(page)
        renderer.render("output.gif", timeline, fps=24, duration=1.0)
    """

    DPI_LOW = 72
    DPI_MEDIUM = 96
    DPI_HIGH = 150

    def __init__(self, page: Page) -> None:
        """Initialize GIF renderer.

        Args:
            page: Page to render.

        Raises:
            ImportError: If required dependencies are not installed.
        """
        if Image is None:
            raise ImportError(
                "Pillow is not installed. Install with: uv sync --extra animation"
            )
        if cairo is None:
            raise ImportError(
                "Cairo is not installed. Install with: uv sync --extra cairo"
            )
        self.page = page
        self._dpi: int = self.DPI_MEDIUM

    def render(
        self,
        output_path: str,
        timeline: Timeline | None = None,
        *,
        fps: int = 24,
        duration: float = 1.0,
        loop: bool = True,
        loop_count: int = 0,
        quality: Literal["low", "medium", "high"] = "medium",
        optimize: bool = True,
        progress_callback: Callable[[int, int], None] | None = None,
    ) -> str:
        """Render the page with animations to an animated GIF.

        Args:
            output_path: Path to save the GIF file.
            timeline: Animation timeline to use. If None, renders a static GIF.
            fps: Frames per second (1-60).
            duration: Total animation duration in seconds.
            loop: Whether the GIF should loop.
            loop_count: Number of loops (0 = infinite).
            quality: Rendering quality ("low", "medium", "high").
            optimize: Whether to optimize the GIF for smaller file size.
            progress_callback: Called with (current_frame, total_frames) after each frame.

        Returns:
            Path to the rendered file.
        """
        fps = max(1, min(60, fps))
        duration = max(0.1, duration)

        if quality == "low":
            self._dpi = self.DPI_LOW
        elif quality == "high":
            self._dpi = self.DPI_HIGH
        else:
            self._dpi = self.DPI_MEDIUM

        frame_count = max(1, int(fps * duration))
        frames: list[Image.Image] = []

        for i in range(frame_count):
            if frame_count > 1:
                t = i / (frame_count - 1)
            else:
                t = 0.0
            time = t * duration

            if timeline is not None:
                timeline.apply_at_time(time)

            frame = self._render_frame()
            frames.append(frame)

            if progress_callback is not None:
                progress_callback(i + 1, frame_count)

        if timeline is not None:
            timeline.reset()

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        frame_duration_ms = int(1000 / fps)

        if len(frames) == 1:
            frames[0].save(output_path, format="GIF")
        else:
            frames[0].save(
                output_path,
                save_all=True,
                append_images=frames[1:],
                duration=frame_duration_ms,
                loop=0 if loop and loop_count == 0 else loop_count,
                optimize=optimize,
            )

        return output_path

    def _render_frame(self) -> Image.Image:
        """Render a single frame to a PIL Image in RGBA mode."""
        scale = self._dpi / 72.0
        width = int(self.page.width * scale)
        height = int(self.page.height * scale)

        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        ctx = cairo.Context(surface)
        ctx.scale(scale, scale)

        from comix.renderer.cairo_renderer import CairoRenderer

        renderer = CairoRenderer.__new__(CairoRenderer)
        renderer.page = self.page
        renderer._surface = surface
        renderer._ctx = ctx
        renderer._dpi = self._dpi
        renderer._draw_page()

        data = bytes(surface.get_data())
        image = Image.frombuffer(
            "RGBA", (width, height), data, "raw", "BGRA", 0, 1
        )

        return image.copy()

    def render_frames(
        self,
        output_dir: str,
        timeline: Timeline | None = None,
        *,
        fps: int = 24,
        duration: float = 1.0,
        quality: Literal["low", "medium", "high"] = "medium",
        format: str = "png",
        progress_callback: Callable[[int, int], None] | None = None,
    ) -> list[str]:
        """Render animation frames to individual image files.

        Useful for post-processing or when you need individual frames.

        Args:
            output_dir: Directory to save frame images.
            timeline: Animation timeline to use.
            fps: Frames per second.
            duration: Total animation duration in seconds.
            quality: Rendering quality.
            format: Image format ("png" or "gif").
            progress_callback: Called with (current_frame, total_frames).

        Returns:
            List of paths to rendered frame files.
        """
        fps = max(1, min(60, fps))
        duration = max(0.1, duration)

        if quality == "low":
            self._dpi = self.DPI_LOW
        elif quality == "high":
            self._dpi = self.DPI_HIGH
        else:
            self._dpi = self.DPI_MEDIUM

        frame_count = max(1, int(fps * duration))
        output_dir_path = Path(output_dir)
        output_dir_path.mkdir(parents=True, exist_ok=True)

        frame_paths: list[str] = []

        for i in range(frame_count):
            if frame_count > 1:
                t = i / (frame_count - 1)
            else:
                t = 0.0
            time = t * duration

            if timeline is not None:
                timeline.apply_at_time(time)

            frame = self._render_frame_rgba()

            frame_path = str(output_dir_path / f"frame_{i:04d}.{format}")
            frame.save(frame_path)
            frame_paths.append(frame_path)

            if progress_callback is not None:
                progress_callback(i + 1, frame_count)

        if timeline is not None:
            timeline.reset()

        return frame_paths

    def _render_frame_rgba(self) -> Image.Image:
        """Render a single frame to a PIL Image in RGBA format."""
        scale = self._dpi / 72.0
        width = int(self.page.width * scale)
        height = int(self.page.height * scale)

        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        ctx = cairo.Context(surface)
        ctx.scale(scale, scale)

        from comix.renderer.cairo_renderer import CairoRenderer

        renderer = CairoRenderer.__new__(CairoRenderer)
        renderer.page = self.page
        renderer._surface = surface
        renderer._ctx = ctx
        renderer._dpi = self._dpi
        renderer._draw_page()

        data = bytes(surface.get_data())
        image = Image.frombuffer(
            "RGBA", (width, height), data, "raw", "BGRA", 0, 1
        )

        return image
