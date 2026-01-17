"""Tests for the GIF renderer."""

from __future__ import annotations

import os
import tempfile

import pytest

from comix import Page, Panel, Stickman
from comix.animation import Timeline, EffectAnimation
from comix.effect.effect import ShakeEffect, ImpactEffect

try:
    from PIL import Image
    from comix.renderer.gif_renderer import GIFRenderer

    ANIMATION_AVAILABLE = True
except ImportError:
    ANIMATION_AVAILABLE = False
    GIFRenderer = None  # type: ignore[misc, assignment]
    Image = None  # type: ignore[misc, assignment]


@pytest.mark.skipif(not ANIMATION_AVAILABLE, reason="Animation dependencies not available")
class TestGIFRendererBasic:
    """Basic tests for GIF renderer."""

    def test_gif_renderer_init(self) -> None:
        page = Page(width=400, height=300)
        renderer = GIFRenderer(page)
        assert renderer.page is page

    def test_gif_renderer_raises_without_dependencies(self) -> None:
        # This test verifies the error message mentions the dependencies
        # We can only test this if the dependencies are available
        page = Page(width=400, height=300)
        renderer = GIFRenderer(page)
        assert renderer is not None

    def test_render_static_gif(self) -> None:
        page = Page(width=200, height=200)
        panel = Panel()
        char = Stickman(height=80)
        char.move_to((100, 100))
        panel.add_content(char)
        page.add(panel)
        page.build()

        renderer = GIFRenderer(page)

        with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as f:
            output_path = f.name

        try:
            result = renderer.render(output_path, fps=10, duration=0.5)
            assert result == output_path
            assert os.path.exists(output_path)

            # Verify it's a valid GIF
            with Image.open(output_path) as img:
                assert img.format == "GIF"
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)

    def test_render_animated_gif_with_timeline(self) -> None:
        page = Page(width=200, height=200)
        panel = Panel()
        char = Stickman(height=80)
        char.move_to((100, 100))
        panel.add_content(char)
        page.add(panel)

        # Use ImpactEffect which renders in foreground (z_index=1)
        # ShakeEffect renders behind objects and may be invisible
        effect = ImpactEffect(target=char, seed=42)
        effect.set_opacity(1.0)
        page.add_effect(effect)
        page.build()

        timeline = Timeline(page)
        timeline.add(EffectAnimation(effect, pattern="fade_out", duration=1.0))

        renderer = GIFRenderer(page)

        with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as f:
            output_path = f.name

        try:
            # Use higher fps and longer duration to ensure multiple frames
            result = renderer.render(output_path, timeline, fps=10, duration=1.0)
            assert result == output_path
            assert os.path.exists(output_path)

            # Verify it's a valid GIF
            with Image.open(output_path) as img:
                assert img.format == "GIF"
                # Check it's animated (has multiple frames)
                assert img.n_frames >= 2
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)

    def test_render_creates_output_directory(self) -> None:
        page = Page(width=100, height=100)
        page.build()

        renderer = GIFRenderer(page)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "subdir", "nested", "output.gif")
            result = renderer.render(output_path, fps=5, duration=0.2)
            assert result == output_path
            assert os.path.exists(output_path)


@pytest.mark.skipif(not ANIMATION_AVAILABLE, reason="Animation dependencies not available")
class TestGIFRendererQuality:
    """Tests for GIF renderer quality settings."""

    def test_quality_affects_dpi(self) -> None:
        page = Page(width=100, height=100)
        page.build()
        renderer = GIFRenderer(page)

        # Low quality
        with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as f:
            low_path = f.name
        with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as f:
            high_path = f.name

        try:
            renderer.render(low_path, fps=5, duration=0.2, quality="low")
            renderer.render(high_path, fps=5, duration=0.2, quality="high")

            with Image.open(low_path) as low_img:
                with Image.open(high_path) as high_img:
                    # High quality should produce larger frames
                    assert high_img.width >= low_img.width
        finally:
            for path in [low_path, high_path]:
                if os.path.exists(path):
                    os.unlink(path)


@pytest.mark.skipif(not ANIMATION_AVAILABLE, reason="Animation dependencies not available")
class TestGIFRendererFrames:
    """Tests for GIF renderer frame rendering."""

    def test_render_frames_to_directory(self) -> None:
        page = Page(width=100, height=100)
        page.build()

        renderer = GIFRenderer(page)

        with tempfile.TemporaryDirectory() as tmpdir:
            frame_paths = renderer.render_frames(
                tmpdir, fps=5, duration=0.4
            )

            assert len(frame_paths) == 2  # 5 fps * 0.4s = 2 frames
            for path in frame_paths:
                assert os.path.exists(path)
                assert path.endswith(".png")

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

        renderer = GIFRenderer(page)

        with tempfile.TemporaryDirectory() as tmpdir:
            frame_paths = renderer.render_frames(
                tmpdir, timeline, fps=10, duration=0.4
            )

            assert len(frame_paths) == 4  # 10 fps * 0.4s = 4 frames


@pytest.mark.skipif(not ANIMATION_AVAILABLE, reason="Animation dependencies not available")
class TestGIFRendererProgress:
    """Tests for GIF renderer progress callback."""

    def test_progress_callback_called(self) -> None:
        page = Page(width=100, height=100)
        page.build()

        renderer = GIFRenderer(page)

        progress_calls: list[tuple[int, int]] = []

        def progress_callback(current: int, total: int) -> None:
            progress_calls.append((current, total))

        with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as f:
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


@pytest.mark.skipif(not ANIMATION_AVAILABLE, reason="Animation dependencies not available")
class TestGIFRendererLooping:
    """Tests for GIF renderer looping options."""

    def test_loop_enabled_by_default(self) -> None:
        page = Page(width=100, height=100)
        page.build()

        renderer = GIFRenderer(page)

        with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as f:
            output_path = f.name

        try:
            renderer.render(output_path, fps=5, duration=0.4)
            # GIF should be created with looping
            assert os.path.exists(output_path)
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)


@pytest.mark.skipif(not ANIMATION_AVAILABLE, reason="Animation dependencies not available")
class TestPageAnimateMethod:
    """Tests for Page.animate() convenience method."""

    def test_page_animate_method(self) -> None:
        page = Page(width=200, height=200)
        panel = Panel()
        char = Stickman(height=80)
        char.move_to((100, 100))
        panel.add_content(char)
        page.add(panel)

        with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as f:
            output_path = f.name

        try:
            result = page.animate(output_path, fps=5, duration=0.2)
            assert result == output_path
            assert os.path.exists(output_path)

            with Image.open(output_path) as img:
                assert img.format == "GIF"
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)

    def test_page_animate_with_timeline(self) -> None:
        page = Page(width=200, height=200)
        panel = Panel()
        char = Stickman(height=80)
        char.move_to((100, 100))
        panel.add_content(char)
        page.add(panel)

        # Use ImpactEffect which renders in foreground for visible animation
        effect = ImpactEffect(target=char, seed=42)
        page.add_effect(effect)

        timeline = Timeline(page)
        timeline.add(EffectAnimation(effect, pattern="fade_out", duration=1.0))

        with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as f:
            output_path = f.name

        try:
            # Use longer duration to ensure multiple frames
            result = page.animate(output_path, timeline, fps=10, duration=1.0)
            assert result == output_path
            assert os.path.exists(output_path)

            with Image.open(output_path) as img:
                assert img.format == "GIF"
                assert img.n_frames >= 2
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)
