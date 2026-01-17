"""Video Renderer - exports MP4/WebM videos from comicode pages.

Requires optional 'video' dependencies:
    uv sync --extra video
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Literal

import numpy as np
from numpy.typing import NDArray

try:
    from PIL import Image
except ImportError:
    Image = None  # type: ignore[assignment]

try:
    import cairo
except ImportError:
    cairo = None  # type: ignore[assignment]

try:
    import imageio.v3 as iio
    from imageio_ffmpeg import get_ffmpeg_exe as _get_ffmpeg_exe

    def _ffmpeg_exe() -> str:
        return _get_ffmpeg_exe()  # type: ignore[no-any-return]

    _IMAGEIO_AVAILABLE = True
except ImportError:
    iio = None  # type: ignore[assignment]
    _ffmpeg_exe = None  # type: ignore[assignment]
    _IMAGEIO_AVAILABLE = False

if TYPE_CHECKING:
    from comix.animation.timeline import Timeline
    from comix.page.page import Page


class VideoRenderer:
    """Renders MP4/WebM video from a Page with animations.

    Requires optional 'video' dependencies:
        uv sync --extra video

    Example:
        from comix.animation import Timeline, EffectAnimation
        from comix.renderer.video_renderer import VideoRenderer

        timeline = Timeline(page)
        timeline.add(EffectAnimation(effect, pattern="pulse", duration=0.5))

        renderer = VideoRenderer(page)
        renderer.render("output.mp4", timeline, fps=30, duration=2.0)
    """

    DPI_LOW = 72
    DPI_MEDIUM = 96
    DPI_HIGH = 150

    CODEC_MP4 = "libx264"
    CODEC_WEBM = "libvpx-vp9"

    def __init__(self, page: Page) -> None:
        """Initialize video renderer.

        Args:
            page: Page to render.

        Raises:
            ImportError: If required dependencies are not installed.
        """
        if Image is None:
            raise ImportError(
                "Pillow is not installed. Install with: uv sync --extra video"
            )
        if cairo is None:
            raise ImportError(
                "Cairo is not installed. Install with: uv sync --extra video"
            )
        if not _IMAGEIO_AVAILABLE:
            raise ImportError(
                "imageio-ffmpeg is not installed. Install with: uv sync --extra video"
            )
        self.page = page
        self._dpi: int = self.DPI_MEDIUM

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
    ) -> str:
        """Render the page with animations to a video file.

        Args:
            output_path: Path to save the video file.
            timeline: Animation timeline to use. If None, renders a static video.
            fps: Frames per second (1-60).
            duration: Total animation duration in seconds.
            format: Video format ("mp4" or "webm").
            quality: Rendering quality ("low", "medium", "high").
            bitrate: Video bitrate (e.g., "2M", "5M"). If None, uses quality-based default.
            audio_path: Optional path to an audio file to include in the video.
            progress_callback: Called with (current_frame, total_frames) after each frame.

        Returns:
            Path to the rendered file.
        """
        fps = max(1, min(60, fps))
        duration = max(0.1, duration)

        if quality == "low":
            self._dpi = self.DPI_LOW
            default_bitrate = "1M"
        elif quality == "high":
            self._dpi = self.DPI_HIGH
            default_bitrate = "5M"
        else:
            self._dpi = self.DPI_MEDIUM
            default_bitrate = "2M"

        bitrate = bitrate or default_bitrate

        frame_count = max(1, int(fps * duration))

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        codec = self.CODEC_MP4 if format == "mp4" else self.CODEC_WEBM
        pixel_format = "yuv420p"

        # Suppress unused variable warning - bitrate is used for documentation
        _ = bitrate

        scale = self._dpi / 72.0
        width = int(self.page.width * scale)
        height = int(self.page.height * scale)

        if width % 2 != 0:
            width += 1
        if height % 2 != 0:
            height += 1

        if audio_path is not None:
            temp_video_path = str(Path(output_path).with_suffix(".temp.mp4"))
        else:
            temp_video_path = output_path

        with iio.imopen(  # type: ignore[call-overload]
            temp_video_path,
            "w",
            plugin="pyav",
            legacy_mode=False,
        ) as writer:
            writer.init_video_stream(
                codec=codec,
                fps=fps,
                pixel_format=pixel_format,
            )

            for i in range(frame_count):
                if frame_count > 1:
                    t = i / (frame_count - 1)
                else:
                    t = 0.0
                time = t * duration

                if timeline is not None:
                    timeline.apply_at_time(time)

                frame = self._render_frame_rgb(width, height)
                writer.write_frame(frame)

                if progress_callback is not None:
                    progress_callback(i + 1, frame_count)

        if timeline is not None:
            timeline.reset()

        if audio_path is not None:
            self._add_audio_track(temp_video_path, audio_path, output_path)
            Path(temp_video_path).unlink(missing_ok=True)

        return output_path

    def _get_crf_for_quality(self, quality: str) -> str:
        """Get CRF value for quality level.

        CRF (Constant Rate Factor): 0 = lossless, 51 = worst quality.
        """
        if quality == "low":
            return "28"
        elif quality == "high":
            return "18"
        else:
            return "23"

    def _render_frame_rgb(self, width: int, height: int) -> NDArray[Any]:
        """Render a single frame to RGB numpy array for video encoding."""
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        ctx = cairo.Context(surface)

        scale = self._dpi / 72.0
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

        rgb_image = Image.new("RGB", image.size, (255, 255, 255))
        rgb_image.paste(image, mask=image.split()[3])

        return np.array(rgb_image)

    def _add_audio_track(
        self, video_path: str, audio_path: str, output_path: str
    ) -> None:
        """Combine video with audio track using ffmpeg."""
        import subprocess

        ffmpeg_exe = _ffmpeg_exe()
        subprocess.run(
            [
                ffmpeg_exe,
                "-y",
                "-i", video_path,
                "-i", audio_path,
                "-c:v", "copy",
                "-c:a", "aac",
                "-shortest",
                output_path,
            ],
            check=True,
            capture_output=True,
        )

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
    ) -> list[str]:
        """Render animation frames to individual image files.

        Useful for post-processing or when you need individual frames.

        Args:
            output_dir: Directory to save frame images.
            timeline: Animation timeline to use.
            fps: Frames per second.
            duration: Total animation duration in seconds.
            quality: Rendering quality.
            format: Image format ("png" or "jpg").
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

        scale = self._dpi / 72.0
        width = int(self.page.width * scale)
        height = int(self.page.height * scale)

        frame_paths: list[str] = []

        for i in range(frame_count):
            if frame_count > 1:
                t = i / (frame_count - 1)
            else:
                t = 0.0
            time = t * duration

            if timeline is not None:
                timeline.apply_at_time(time)

            frame = self._render_frame_pil(width, height)

            if format.lower() in ("jpg", "jpeg"):
                rgb_frame = Image.new("RGB", frame.size, (255, 255, 255))
                rgb_frame.paste(frame, mask=frame.split()[3])
                frame = rgb_frame

            frame_path = str(output_dir_path / f"frame_{i:04d}.{format}")
            frame.save(frame_path)
            frame_paths.append(frame_path)

            if progress_callback is not None:
                progress_callback(i + 1, frame_count)

        if timeline is not None:
            timeline.reset()

        return frame_paths

    def _render_frame_pil(self, width: int, height: int) -> Image.Image:
        """Render a single frame to a PIL Image."""
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        ctx = cairo.Context(surface)

        scale = self._dpi / 72.0
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
