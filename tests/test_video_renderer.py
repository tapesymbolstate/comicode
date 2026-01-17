"""Tests for the Video renderer."""

from __future__ import annotations

import os
import tempfile

import pytest

from comix import Page, Panel, Stickman

try:
    from comix.animation import Timeline, EffectAnimation
    from comix.effect.effect import ShakeEffect, ImpactEffect

    ANIMATION_AVAILABLE = True
except ImportError:
    ANIMATION_AVAILABLE = False
    Timeline = None  # type: ignore[misc, assignment]
    EffectAnimation = None  # type: ignore[misc, assignment]
    ShakeEffect = None  # type: ignore[misc, assignment]
    ImpactEffect = None  # type: ignore[misc, assignment]

try:
    from comix.renderer.video_renderer import VideoRenderer, _IMAGEIO_AVAILABLE

    VIDEO_AVAILABLE = _IMAGEIO_AVAILABLE and ANIMATION_AVAILABLE
except ImportError:
    VIDEO_AVAILABLE = False
    VideoRenderer = None  # type: ignore[misc, assignment]


@pytest.mark.skipif(not VIDEO_AVAILABLE, reason="Video dependencies not available")
class TestVideoRendererBasic:
    """Basic tests for Video renderer."""

    def test_video_renderer_init(self) -> None:
        page = Page(width=400, height=300)
        renderer = VideoRenderer(page)
        assert renderer.page is page

    def test_video_renderer_dpi_constants(self) -> None:
        assert VideoRenderer.DPI_LOW == 72
        assert VideoRenderer.DPI_MEDIUM == 96
        assert VideoRenderer.DPI_HIGH == 150

    def test_video_renderer_codec_constants(self) -> None:
        assert VideoRenderer.CODEC_MP4 == "libx264"
        assert VideoRenderer.CODEC_WEBM == "libvpx-vp9"

    def test_render_static_mp4(self) -> None:
        page = Page(width=200, height=200)
        panel = Panel()
        char = Stickman(height=80)
        char.move_to((100, 100))
        panel.add_content(char)
        page.add(panel)
        page.build()

        renderer = VideoRenderer(page)

        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
            output_path = f.name

        try:
            result = renderer.render(output_path, fps=10, duration=0.5)
            assert result == output_path
            assert os.path.exists(output_path)
            assert os.path.getsize(output_path) > 0
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)

    def test_render_static_webm(self) -> None:
        page = Page(width=200, height=200)
        panel = Panel()
        char = Stickman(height=80)
        char.move_to((100, 100))
        panel.add_content(char)
        page.add(panel)
        page.build()

        renderer = VideoRenderer(page)

        with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as f:
            output_path = f.name

        try:
            result = renderer.render(output_path, format="webm", fps=10, duration=0.5)
            assert result == output_path
            assert os.path.exists(output_path)
            assert os.path.getsize(output_path) > 0
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)

    def test_render_animated_video_with_timeline(self) -> None:
        page = Page(width=200, height=200)
        panel = Panel()
        char = Stickman(height=80)
        char.move_to((100, 100))
        panel.add_content(char)
        page.add(panel)

        effect = ImpactEffect(target=char, seed=42)
        effect.set_opacity(1.0)
        page.add_effect(effect)
        page.build()

        timeline = Timeline(page)
        timeline.add(EffectAnimation(effect, pattern="fade_out", duration=1.0))

        renderer = VideoRenderer(page)

        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
            output_path = f.name

        try:
            result = renderer.render(output_path, timeline, fps=10, duration=1.0)
            assert result == output_path
            assert os.path.exists(output_path)
            assert os.path.getsize(output_path) > 0
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)

    def test_render_creates_output_directory(self) -> None:
        page = Page(width=100, height=100)
        page.build()

        renderer = VideoRenderer(page)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "subdir", "nested", "output.mp4")
            result = renderer.render(output_path, fps=5, duration=0.2)
            assert result == output_path
            assert os.path.exists(output_path)


@pytest.mark.skipif(not VIDEO_AVAILABLE, reason="Video dependencies not available")
class TestVideoRendererQuality:
    """Tests for Video renderer quality settings."""

    def test_quality_low(self) -> None:
        page = Page(width=100, height=100)
        page.build()
        renderer = VideoRenderer(page)

        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
            output_path = f.name

        try:
            renderer.render(output_path, fps=5, duration=0.2, quality="low")
            assert os.path.exists(output_path)
            assert os.path.getsize(output_path) > 0
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)

    def test_quality_medium(self) -> None:
        page = Page(width=100, height=100)
        page.build()
        renderer = VideoRenderer(page)

        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
            output_path = f.name

        try:
            renderer.render(output_path, fps=5, duration=0.2, quality="medium")
            assert os.path.exists(output_path)
            assert os.path.getsize(output_path) > 0
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)

    def test_quality_high(self) -> None:
        page = Page(width=100, height=100)
        page.build()
        renderer = VideoRenderer(page)

        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
            output_path = f.name

        try:
            renderer.render(output_path, fps=5, duration=0.2, quality="high")
            assert os.path.exists(output_path)
            assert os.path.getsize(output_path) > 0
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)

    def test_crf_for_quality(self) -> None:
        page = Page(width=100, height=100)
        renderer = VideoRenderer(page)

        assert renderer._get_crf_for_quality("low") == "28"
        assert renderer._get_crf_for_quality("medium") == "23"
        assert renderer._get_crf_for_quality("high") == "18"


@pytest.mark.skipif(not VIDEO_AVAILABLE, reason="Video dependencies not available")
class TestVideoRendererFrames:
    """Tests for Video renderer frame rendering."""

    def test_render_frames_to_directory(self) -> None:
        page = Page(width=100, height=100)
        page.build()

        renderer = VideoRenderer(page)

        with tempfile.TemporaryDirectory() as tmpdir:
            frame_paths = renderer.render_frames(
                tmpdir, fps=5, duration=0.4
            )

            assert len(frame_paths) == 2  # 5 fps * 0.4s = 2 frames
            for path in frame_paths:
                assert os.path.exists(path)
                assert path.endswith(".png")

    def test_render_frames_jpg_format(self) -> None:
        page = Page(width=100, height=100)
        page.build()

        renderer = VideoRenderer(page)

        with tempfile.TemporaryDirectory() as tmpdir:
            frame_paths = renderer.render_frames(
                tmpdir, fps=5, duration=0.4, format="jpg"
            )

            assert len(frame_paths) == 2
            for path in frame_paths:
                assert os.path.exists(path)
                assert path.endswith(".jpg")

    def test_render_frames_with_timeline(self) -> None:
        page = Page(width=100, height=100)
        panel = Panel()
        char = Stickman(height=50)
        char.move_to((50, 50))
        panel.add_content(char)
        page.add(panel)

        effect = ShakeEffect(target=char, seed=42)
        page.add_effect(effect)
        page.build()

        timeline = Timeline(page)
        timeline.add(EffectAnimation(effect, pattern="pulse", duration=0.4))

        renderer = VideoRenderer(page)

        with tempfile.TemporaryDirectory() as tmpdir:
            frame_paths = renderer.render_frames(
                tmpdir, timeline, fps=10, duration=0.4
            )

            assert len(frame_paths) == 4  # 10 fps * 0.4s = 4 frames


@pytest.mark.skipif(not VIDEO_AVAILABLE, reason="Video dependencies not available")
class TestVideoRendererProgress:
    """Tests for Video renderer progress callback."""

    def test_progress_callback_called(self) -> None:
        page = Page(width=100, height=100)
        page.build()

        renderer = VideoRenderer(page)

        progress_calls: list[tuple[int, int]] = []

        def progress_callback(current: int, total: int) -> None:
            progress_calls.append((current, total))

        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
            output_path = f.name

        try:
            renderer.render(
                output_path,
                fps=5,
                duration=0.4,
                progress_callback=progress_callback,
            )

            assert len(progress_calls) == 2  # 5 fps * 0.4s = 2 frames
            assert progress_calls[0] == (1, 2)
            assert progress_calls[1] == (2, 2)
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)

    def test_progress_callback_for_frames(self) -> None:
        page = Page(width=100, height=100)
        page.build()

        renderer = VideoRenderer(page)

        progress_calls: list[tuple[int, int]] = []

        def progress_callback(current: int, total: int) -> None:
            progress_calls.append((current, total))

        with tempfile.TemporaryDirectory() as tmpdir:
            renderer.render_frames(
                tmpdir,
                fps=5,
                duration=0.4,
                progress_callback=progress_callback,
            )

            assert len(progress_calls) == 2
            assert progress_calls[0] == (1, 2)
            assert progress_calls[1] == (2, 2)


@pytest.mark.skipif(not VIDEO_AVAILABLE, reason="Video dependencies not available")
class TestVideoRendererEdgeCases:
    """Tests for Video renderer edge cases."""

    def test_fps_clamped_min(self) -> None:
        page = Page(width=100, height=100)
        page.build()
        renderer = VideoRenderer(page)

        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
            output_path = f.name

        try:
            # fps below 1 should be clamped to 1
            renderer.render(output_path, fps=0, duration=0.5)
            assert os.path.exists(output_path)
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)

    def test_fps_clamped_max(self) -> None:
        page = Page(width=100, height=100)
        page.build()
        renderer = VideoRenderer(page)

        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
            output_path = f.name

        try:
            # fps above 60 should be clamped to 60
            renderer.render(output_path, fps=100, duration=0.1)
            assert os.path.exists(output_path)
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)

    def test_duration_clamped_min(self) -> None:
        page = Page(width=100, height=100)
        page.build()
        renderer = VideoRenderer(page)

        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
            output_path = f.name

        try:
            # duration below 0.1 should be clamped to 0.1
            renderer.render(output_path, fps=10, duration=0.01)
            assert os.path.exists(output_path)
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)

    def test_single_frame_video(self) -> None:
        page = Page(width=100, height=100)
        page.build()
        renderer = VideoRenderer(page)

        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
            output_path = f.name

        try:
            # Very short duration = single frame
            renderer.render(output_path, fps=1, duration=0.5)
            assert os.path.exists(output_path)
            assert os.path.getsize(output_path) > 0
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)


@pytest.mark.skipif(not VIDEO_AVAILABLE, reason="Video dependencies not available")
class TestVideoRendererFormats:
    """Tests for different video formats."""

    def test_mp4_format(self) -> None:
        page = Page(width=100, height=100)
        page.build()
        renderer = VideoRenderer(page)

        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
            output_path = f.name

        try:
            renderer.render(output_path, format="mp4", fps=5, duration=0.2)
            assert os.path.exists(output_path)
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)

    def test_webm_format(self) -> None:
        page = Page(width=100, height=100)
        page.build()
        renderer = VideoRenderer(page)

        with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as f:
            output_path = f.name

        try:
            renderer.render(output_path, format="webm", fps=5, duration=0.2)
            assert os.path.exists(output_path)
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)


@pytest.mark.skipif(not VIDEO_AVAILABLE, reason="Video dependencies not available")
class TestVideoRendererDimensions:
    """Tests for video dimension handling."""

    def test_odd_dimensions_adjusted(self) -> None:
        # Video codecs require even dimensions
        page = Page(width=101, height=103)  # Odd dimensions
        page.build()
        renderer = VideoRenderer(page)

        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
            output_path = f.name

        try:
            renderer.render(output_path, fps=5, duration=0.2)
            assert os.path.exists(output_path)
            assert os.path.getsize(output_path) > 0
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)

    def test_large_dimensions(self) -> None:
        page = Page(width=800, height=1200)
        page.build()
        renderer = VideoRenderer(page)

        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
            output_path = f.name

        try:
            renderer.render(output_path, fps=5, duration=0.2, quality="low")
            assert os.path.exists(output_path)
            assert os.path.getsize(output_path) > 0
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)


class TestVideoRendererWithoutDependencies:
    """Tests for VideoRenderer without dependencies."""

    def test_import_check(self) -> None:
        if not VIDEO_AVAILABLE:
            # If dependencies are not available, import should still work
            # but VideoRenderer should be None or raise ImportError on init
            from comix import VideoRenderer as VR

            if VR is not None:
                page = Page(width=100, height=100)
                with pytest.raises(ImportError):
                    VR(page)
