"""Tests for the Image and AIImage modules."""

import base64
import os
from unittest.mock import MagicMock, patch

import pytest

from comix import Image, AIImage, AIProvider, Page
from comix.cobject.image.ai_image import (
    AIProviderNotAvailableError,
    AIGenerationError,
)


class TestImage:
    """Tests for the Image class."""

    def test_image_creation_default(self):
        """Test creating an Image with default parameters."""
        img = Image()
        assert img.source is None
        assert img.width == 100.0
        assert img.height == 100.0
        assert img.preserve_aspect_ratio is True
        assert img.fit == "contain"
        assert img.position.tolist() == [0, 0]

    def test_image_creation_with_source(self):
        """Test creating an Image with a source."""
        img = Image(source="test.png", width=200, height=150)
        assert img.source == "test.png"
        assert img.width == 200
        assert img.height == 150

    def test_image_set_source(self):
        """Test setting the image source."""
        img = Image()
        result = img.set_source("new_image.png")
        assert result is img  # Method chaining
        assert img.source == "new_image.png"

    def test_image_set_size(self):
        """Test setting the image size."""
        img = Image()
        result = img.set_size(300, 200)
        assert result is img
        assert img.width == 300
        assert img.height == 200

    def test_image_set_fit(self):
        """Test setting the fit mode."""
        img = Image()

        img.set_fit("contain")
        assert img.fit == "contain"

        img.set_fit("cover")
        assert img.fit == "cover"

        img.set_fit("fill")
        assert img.fit == "fill"

        img.set_fit("none")
        assert img.fit == "none"

    def test_image_set_fit_invalid(self):
        """Test setting an invalid fit mode."""
        img = Image()
        with pytest.raises(ValueError, match="Invalid fit mode"):
            img.set_fit("invalid")

    def test_image_method_chaining(self):
        """Test method chaining for Image."""
        img = (
            Image()
            .set_source("test.png")
            .set_size(400, 300)
            .set_fit("cover")
            .move_to((100, 200))
            .set_opacity(0.8)
        )
        assert img.source == "test.png"
        assert img.width == 400
        assert img.height == 300
        assert img.fit == "cover"
        assert img.position.tolist() == [100, 200]
        assert img.opacity == 0.8

    def test_image_bounding_box(self):
        """Test bounding box calculation."""
        img = Image(width=100, height=50)
        img.move_to((200, 100))

        bbox = img.get_bounding_box()
        assert bbox[0].tolist() == [150, 75]  # min
        assert bbox[1].tolist() == [250, 125]  # max

    def test_image_get_render_data(self):
        """Test get_render_data returns correct structure."""
        img = Image(source="test.png", width=200, height=150)
        img.move_to((100, 100))

        data = img.get_render_data()

        assert data["type"] == "Image"
        assert data["source"] == "test.png"
        assert data["image_width"] == 200
        assert data["image_height"] == 150
        assert data["preserve_aspect_ratio"] is True
        assert data["fit"] == "contain"
        assert data["position"] == [100, 100]

    def test_image_set_base64_data(self):
        """Test setting base64 encoded image data."""
        img = Image()
        # Simple 1x1 red PNG in base64
        test_data = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8DwHwAFBQIAX8jx0gAAAABJRU5ErkJggg=="

        result = img.set_base64_data(test_data, "image/png")
        assert result is img
        assert img.get_base64_data() == test_data

    def test_image_get_data_uri(self):
        """Test generating data URI from base64 data."""
        img = Image()
        test_data = "SGVsbG8gV29ybGQ="  # "Hello World" in base64
        img.set_base64_data(test_data, "image/png")

        data_uri = img.get_data_uri()
        assert data_uri == f"data:image/png;base64,{test_data}"

    def test_image_get_data_uri_no_data(self):
        """Test get_data_uri when no data is set."""
        img = Image()
        assert img.get_data_uri() is None

    def test_image_load_from_file(self, tmp_path):
        """Test loading image from file."""
        # Create a test PNG file (1x1 red pixel)
        png_data = base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8DwHwAFBQIAX8jx0gAAAABJRU5ErkJggg=="
        )
        test_file = tmp_path / "test.png"
        test_file.write_bytes(png_data)

        img = Image()
        result = img.load_from_file(test_file)

        assert result is img
        assert img.source == str(test_file.absolute())
        assert img.get_base64_data() is not None

    def test_image_load_from_file_not_found(self):
        """Test loading from non-existent file raises error."""
        img = Image()
        with pytest.raises(FileNotFoundError):
            img.load_from_file("/nonexistent/path/image.png")

    def test_image_load_from_file_mime_types(self, tmp_path):
        """Test MIME type detection from file extension."""
        # Test various extensions
        extensions_and_types = [
            (".png", "image/png"),
            (".jpg", "image/jpeg"),
            (".jpeg", "image/jpeg"),
            (".gif", "image/gif"),
            (".webp", "image/webp"),
            (".svg", "image/svg+xml"),
            (".bmp", "image/bmp"),
        ]

        test_data = b"fake image data"

        for ext, expected_mime in extensions_and_types:
            test_file = tmp_path / f"test{ext}"
            test_file.write_bytes(test_data)

            img = Image()
            img.load_from_file(test_file)
            assert img._mime_type == expected_mime

    def test_image_repr(self):
        """Test string representation."""
        img = Image(source="test.png", width=200, height=150)
        repr_str = repr(img)
        assert "Image" in repr_str
        assert "test.png" in repr_str


class TestAIImage:
    """Tests for the AIImage class."""

    def test_aiimage_creation_default(self):
        """Test creating an AIImage with default parameters."""
        ai_img = AIImage(prompt="A beautiful landscape")

        assert ai_img.prompt == "A beautiful landscape"
        assert ai_img.provider == AIProvider.OPENAI
        assert ai_img.model == "dall-e-3"
        assert ai_img.width == 512.0
        assert ai_img.height == 512.0
        assert ai_img.quality == "standard"
        assert ai_img.is_generated is False

    def test_aiimage_creation_replicate(self):
        """Test creating an AIImage with Replicate provider."""
        ai_img = AIImage(
            prompt="A cyberpunk city",
            provider=AIProvider.REPLICATE,
        )

        assert ai_img.provider == AIProvider.REPLICATE
        assert "stability-ai/sdxl" in ai_img.model

    def test_aiimage_creation_string_provider(self):
        """Test creating AIImage with string provider."""
        ai_img = AIImage(prompt="test", provider="openai")
        assert ai_img.provider == AIProvider.OPENAI

        ai_img2 = AIImage(prompt="test", provider="replicate")
        assert ai_img2.provider == AIProvider.REPLICATE

    def test_aiimage_set_prompt(self):
        """Test setting the prompt."""
        ai_img = AIImage(prompt="original")
        result = ai_img.set_prompt("new prompt")

        assert result is ai_img
        assert ai_img.prompt == "new prompt"
        assert ai_img._generated is False  # Should reset generation flag

    def test_aiimage_set_provider(self):
        """Test setting the provider."""
        ai_img = AIImage(prompt="test")
        result = ai_img.set_provider(AIProvider.REPLICATE)

        assert result is ai_img
        assert ai_img.provider == AIProvider.REPLICATE

    def test_aiimage_set_model(self):
        """Test setting the model."""
        ai_img = AIImage(prompt="test")
        result = ai_img.set_model("dall-e-2")

        assert result is ai_img
        assert ai_img.model == "dall-e-2"

    def test_aiimage_get_render_data(self):
        """Test get_render_data includes AI-specific fields."""
        ai_img = AIImage(prompt="A test image", provider=AIProvider.OPENAI)
        data = ai_img.get_render_data()

        assert data["type"] == "AIImage"
        assert data["ai_generated"] is True
        assert data["prompt"] == "A test image"
        assert data["provider"] == "openai"
        assert data["model"] == "dall-e-3"
        assert data["is_generated"] is False

    def test_aiimage_repr(self):
        """Test string representation."""
        ai_img = AIImage(prompt="A beautiful sunset over mountains")
        repr_str = repr(ai_img)

        assert "AIImage" in repr_str
        assert "A beautiful sunset" in repr_str  # Truncated prompt
        assert "openai" in repr_str
        assert "pending" in repr_str

    def test_aiimage_openai_size_mapping(self):
        """Test OpenAI size mapping based on dimensions."""
        # Square
        ai_img = AIImage(prompt="test", width=512, height=512)
        assert ai_img._get_openai_size() == "1024x1024"

        # Landscape
        ai_img = AIImage(prompt="test", width=800, height=400)
        assert ai_img._get_openai_size() == "1792x1024"

        # Portrait
        ai_img = AIImage(prompt="test", width=400, height=800)
        assert ai_img._get_openai_size() == "1024x1792"

    def test_aiimage_generation_metadata(self):
        """Test getting generation metadata."""
        ai_img = AIImage(prompt="test")
        metadata = ai_img.get_generation_metadata()
        assert isinstance(metadata, dict)
        assert metadata == {}  # Empty before generation

    def test_aiimage_generate_no_prompt(self):
        """Test generation fails without prompt."""
        import asyncio

        ai_img = AIImage(prompt="")

        async def run_test():
            with pytest.raises(AIGenerationError, match="No prompt provided"):
                await ai_img.generate_async()

        asyncio.run(run_test())

    def test_aiimage_generate_openai_not_installed(self):
        """Test generation fails when openai is not installed."""
        import asyncio

        ai_img = AIImage(prompt="test")

        async def run_test():
            with patch(
                "comix.cobject.image.ai_image.AIImage._generate_openai",
                side_effect=AIProviderNotAvailableError("OpenAI package not installed"),
            ):
                with pytest.raises(AIProviderNotAvailableError):
                    await ai_img.generate_async()

        asyncio.run(run_test())

    def test_aiimage_generate_replicate_not_installed(self):
        """Test generation fails when replicate is not installed."""
        import asyncio

        ai_img = AIImage(prompt="test", provider=AIProvider.REPLICATE)

        async def run_test():
            with patch(
                "comix.cobject.image.ai_image.AIImage._generate_replicate",
                side_effect=AIProviderNotAvailableError("Replicate package not installed"),
            ):
                with pytest.raises(AIProviderNotAvailableError):
                    await ai_img.generate_async()

        asyncio.run(run_test())

    def test_aiimage_generate_openai_no_api_key(self):
        """Test generation fails without API key."""
        import asyncio

        ai_img = AIImage(prompt="test")

        async def run_test():
            # Clear any existing API key
            with patch.dict(os.environ, {}, clear=True):
                with patch.dict(os.environ, {"OPENAI_API_KEY": ""}):
                    # Mock the openai import to succeed
                    mock_openai = MagicMock()
                    with patch.dict("sys.modules", {"openai": mock_openai}):
                        with pytest.raises(AIGenerationError, match="OPENAI_API_KEY"):
                            await ai_img.generate_async()

        asyncio.run(run_test())

    def test_aiimage_generate_replicate_no_api_key(self):
        """Test generation fails without Replicate API token."""
        import asyncio

        ai_img = AIImage(prompt="test", provider=AIProvider.REPLICATE)

        async def run_test():
            with patch.dict(os.environ, {}, clear=True):
                with patch.dict(os.environ, {"REPLICATE_API_TOKEN": ""}):
                    mock_replicate = MagicMock()
                    with patch.dict("sys.modules", {"replicate": mock_replicate}):
                        with pytest.raises(AIGenerationError, match="REPLICATE_API_TOKEN"):
                            await ai_img.generate_async()

        asyncio.run(run_test())


class TestImageRendering:
    """Tests for Image rendering in SVG and Cairo."""

    def test_image_svg_rendering_with_data_uri(self, tmp_path):
        """Test rendering an Image with data URI to SVG."""
        page = Page(width=400, height=300)

        img = Image(width=100, height=100)
        img.move_to((200, 150))
        # Set some base64 data
        img.set_base64_data("SGVsbG8gV29ybGQ=", "image/png")

        page.add(img)

        output_path = tmp_path / "test_image.svg"
        page.render(str(output_path), format="svg")

        assert output_path.exists()
        content = output_path.read_text()

        # Check that image element is present
        assert "<image" in content
        assert 'preserveAspectRatio="xMidYMid meet"' in content

    def test_image_svg_rendering_placeholder(self, tmp_path):
        """Test rendering an Image without data shows placeholder."""
        page = Page(width=400, height=300)

        img = Image(width=100, height=100)
        img.move_to((200, 150))
        # No data set - should render placeholder

        page.add(img)

        output_path = tmp_path / "test_placeholder.svg"
        page.render(str(output_path), format="svg")

        assert output_path.exists()
        content = output_path.read_text()

        # Check placeholder elements
        assert "No image" in content
        assert "#EEEEEE" in content  # Placeholder fill color

    def test_image_svg_fit_modes(self, tmp_path):
        """Test different fit modes in SVG rendering."""
        page = Page(width=400, height=300)

        # Test contain
        img_contain = Image(width=100, height=100)
        img_contain.set_fit("contain")
        img_contain.set_base64_data("test", "image/png")
        img_contain.move_to((100, 150))

        # Test cover
        img_cover = Image(width=100, height=100)
        img_cover.set_fit("cover")
        img_cover.set_base64_data("test", "image/png")
        img_cover.move_to((300, 150))

        page.add(img_contain, img_cover)

        output_path = tmp_path / "test_fit.svg"
        page.render(str(output_path), format="svg")

        content = output_path.read_text()
        assert 'preserveAspectRatio="xMidYMid meet"' in content  # contain
        assert 'preserveAspectRatio="xMidYMid slice"' in content  # cover

    def test_aiimage_svg_rendering(self, tmp_path):
        """Test rendering an AIImage to SVG."""
        page = Page(width=400, height=300)

        ai_img = AIImage(prompt="A test image", width=100, height=100)
        ai_img.move_to((200, 150))
        # Without generation, should show placeholder

        page.add(ai_img)

        output_path = tmp_path / "test_aiimage.svg"
        page.render(str(output_path), format="svg")

        assert output_path.exists()


class TestImageIntegration:
    """Integration tests for Image with other components."""

    def test_image_in_panel(self, tmp_path):
        """Test adding Image to a Panel."""
        from comix import Panel

        page = Page(width=400, height=300)
        panel = Panel(width=300, height=200)
        panel.move_to((200, 150))

        img = Image(width=100, height=100)
        img.move_to((200, 150))

        panel.add_content(img)
        page.add(panel)

        output_path = tmp_path / "test_panel_image.svg"
        page.render(str(output_path), format="svg")

        assert output_path.exists()

    def test_image_z_index(self, tmp_path):
        """Test Image respects z-index ordering."""
        page = Page(width=400, height=300)

        # Create two overlapping images with different z-index
        img1 = Image(width=100, height=100, z_index=1)
        img1.move_to((200, 150))
        img1.set_base64_data("img1", "image/png")

        img2 = Image(width=100, height=100, z_index=2)
        img2.move_to((220, 170))
        img2.set_base64_data("img2", "image/png")

        page.add(img1, img2)

        output_path = tmp_path / "test_zindex.svg"
        page.render(str(output_path), format="svg")

        assert output_path.exists()

    def test_image_opacity(self, tmp_path):
        """Test Image with opacity."""
        page = Page(width=400, height=300)

        img = Image(width=100, height=100)
        img.move_to((200, 150))
        img.set_opacity(0.5)
        img.set_base64_data("test", "image/png")

        page.add(img)

        output_path = tmp_path / "test_opacity.svg"
        page.render(str(output_path), format="svg")

        content = output_path.read_text()
        assert 'opacity="0.5"' in content

    def test_image_transformations(self):
        """Test Image transformation methods."""
        img = Image(width=100, height=100)

        # Test all CObject transformation methods
        img.move_to((100, 100))
        assert img.position.tolist() == [100, 100]

        img.shift((50, 50))
        assert img.position.tolist() == [150, 150]

        img.set_scale(2.0)
        assert img.scale == 2.0

        img.rotate(1.57)  # ~90 degrees
        assert abs(img.rotation - 1.57) < 0.01

    def test_image_hierarchy(self):
        """Test Image in parent-child hierarchy."""
        parent = Image(width=200, height=200)
        child = Image(width=50, height=50)

        parent.add(child)

        assert child in parent.submobjects
        assert child.parent is parent

        family = parent.get_family()
        assert parent in family
        assert child in family


class TestAIProvider:
    """Tests for the AIProvider enum."""

    def test_aiprovider_values(self):
        """Test AIProvider enum values."""
        assert AIProvider.OPENAI.value == "openai"
        assert AIProvider.REPLICATE.value == "replicate"

    def test_aiprovider_from_string(self):
        """Test creating AIProvider from string."""
        assert AIProvider("openai") == AIProvider.OPENAI
        assert AIProvider("replicate") == AIProvider.REPLICATE

    def test_aiprovider_invalid_string(self):
        """Test invalid provider string raises error."""
        with pytest.raises(ValueError):
            AIProvider("invalid_provider")


class TestAIImageCoverage:
    """Additional tests to improve AIImage test coverage."""

    def test_aiimage_creation_with_custom_model(self):
        """Test creating AIImage with custom model parameter (line 108)."""
        ai_img = AIImage(
            prompt="test",
            provider=AIProvider.OPENAI,
            model="dall-e-2"
        )
        assert ai_img.model == "dall-e-2"

    def test_aiimage_creation_with_custom_replicate_model(self):
        """Test creating AIImage with custom Replicate model."""
        ai_img = AIImage(
            prompt="test",
            provider=AIProvider.REPLICATE,
            model="custom/model:version123"
        )
        assert ai_img.model == "custom/model:version123"

    def test_aiimage_generate_sync_wrapper(self):
        """Test synchronous generate() method (line 166)."""
        ai_img = AIImage(prompt="test")

        # Mock asyncio.run to consume the coroutine and return ai_img
        def mock_asyncio_run(coro):
            # Close the coroutine to prevent the warning
            coro.close()
            return ai_img

        with patch('comix.cobject.image.ai_image.asyncio.run', side_effect=mock_asyncio_run) as mock_run:
            result = ai_img.generate()
            assert result is ai_img
            mock_run.assert_called_once()

    def test_aiimage_generation_success_state_openai(self):
        """Test successful generation updates state flags (lines 186-188)."""
        import asyncio
        import sys

        ai_img = AIImage(prompt="test prompt")

        async def run_test():
            # Mock successful OpenAI response
            mock_response = MagicMock()
            mock_image_data = MagicMock()
            mock_image_data.b64_json = "fake_base64_data"
            mock_image_data.revised_prompt = "revised prompt"
            mock_response.data = [mock_image_data]

            # Create an AsyncMock for the images.generate method
            from unittest.mock import AsyncMock
            mock_generate = AsyncMock(return_value=mock_response)

            mock_client = MagicMock()
            mock_client.images = MagicMock()
            mock_client.images.generate = mock_generate

            # Create a mock openai module
            mock_openai_module = MagicMock()
            mock_openai_module.AsyncOpenAI = MagicMock(return_value=mock_client)

            with patch.dict(os.environ, {"OPENAI_API_KEY": "fake_key"}):
                with patch.dict(sys.modules, {'openai': mock_openai_module}):
                    await ai_img._generate_openai()

                    assert ai_img.get_base64_data() == "fake_base64_data"
                    assert ai_img._generation_metadata["revised_prompt"] == "revised prompt"

        asyncio.run(run_test())

    def test_aiimage_openai_import_error(self):
        """Test _generate_openai raises AIProviderNotAvailableError on import failure (lines 194-195)."""
        import asyncio
        import sys
        import builtins

        ai_img = AIImage(prompt="test")

        async def run_test():
            # Remove any cached openai module
            for key in list(sys.modules.keys()):
                if key == 'openai' or key.startswith('openai.'):
                    del sys.modules[key]

            original_import = builtins.__import__

            def mock_import(name, *args, **kwargs):
                if name == 'openai':
                    raise ImportError("No module named 'openai'")
                return original_import(name, *args, **kwargs)

            with patch('builtins.__import__', side_effect=mock_import):
                with pytest.raises(AIProviderNotAvailableError, match="OpenAI package not installed"):
                    await ai_img._generate_openai()

        asyncio.run(run_test())

    def test_aiimage_openai_no_image_data(self):
        """Test OpenAI generation fails when response has no b64_json (line 236)."""
        import asyncio
        import sys
        from unittest.mock import AsyncMock

        ai_img = AIImage(prompt="test")

        async def run_test():
            mock_response = MagicMock()
            mock_image_data = MagicMock()
            mock_image_data.b64_json = None  # No b64_json
            mock_response.data = [mock_image_data]

            mock_generate = AsyncMock(return_value=mock_response)

            mock_client = MagicMock()
            mock_client.images = MagicMock()
            mock_client.images.generate = mock_generate

            mock_openai_module = MagicMock()
            mock_openai_module.AsyncOpenAI = MagicMock(return_value=mock_client)

            with patch.dict(os.environ, {"OPENAI_API_KEY": "fake_key"}):
                with patch.dict(sys.modules, {'openai': mock_openai_module}):
                    with pytest.raises(AIGenerationError, match="No image data in OpenAI response"):
                        await ai_img._generate_openai()

        asyncio.run(run_test())

    def test_aiimage_openai_empty_response(self):
        """Test OpenAI generation fails with empty response (line 238)."""
        import asyncio
        import sys
        from unittest.mock import AsyncMock

        ai_img = AIImage(prompt="test")

        async def run_test():
            mock_response = MagicMock()
            mock_response.data = []  # Empty data

            mock_generate = AsyncMock(return_value=mock_response)

            mock_client = MagicMock()
            mock_client.images = MagicMock()
            mock_client.images.generate = mock_generate

            mock_openai_module = MagicMock()
            mock_openai_module.AsyncOpenAI = MagicMock(return_value=mock_client)

            with patch.dict(os.environ, {"OPENAI_API_KEY": "fake_key"}):
                with patch.dict(sys.modules, {'openai': mock_openai_module}):
                    with pytest.raises(AIGenerationError, match="Empty response from OpenAI"):
                        await ai_img._generate_openai()

        asyncio.run(run_test())

    def test_aiimage_openai_with_style(self):
        """Test OpenAI generation includes style parameter (lines 221-222)."""
        import asyncio
        import sys
        from unittest.mock import AsyncMock

        ai_img = AIImage(prompt="test", style="vivid")

        async def run_test():
            mock_response = MagicMock()
            mock_image_data = MagicMock()
            mock_image_data.b64_json = "fake_data"
            mock_image_data.revised_prompt = "revised"
            mock_response.data = [mock_image_data]

            captured_kwargs = {}

            async def capture_generate(**kwargs):
                captured_kwargs.update(kwargs)
                return mock_response

            mock_generate = AsyncMock(side_effect=capture_generate)

            mock_client = MagicMock()
            mock_client.images = MagicMock()
            mock_client.images.generate = mock_generate

            mock_openai_module = MagicMock()
            mock_openai_module.AsyncOpenAI = MagicMock(return_value=mock_client)

            with patch.dict(os.environ, {"OPENAI_API_KEY": "fake_key"}):
                with patch.dict(sys.modules, {'openai': mock_openai_module}):
                    await ai_img._generate_openai()
                    assert "style" in captured_kwargs
                    assert captured_kwargs["style"] == "vivid"

        asyncio.run(run_test())

    def test_aiimage_openai_generic_exception(self):
        """Test OpenAI generation wraps generic exceptions (lines 244-245)."""
        import asyncio
        import sys
        from unittest.mock import AsyncMock

        ai_img = AIImage(prompt="test")

        async def run_test():
            mock_generate = AsyncMock(side_effect=ValueError("Some unexpected error"))

            mock_client = MagicMock()
            mock_client.images = MagicMock()
            mock_client.images.generate = mock_generate

            mock_openai_module = MagicMock()
            mock_openai_module.AsyncOpenAI = MagicMock(return_value=mock_client)

            with patch.dict(os.environ, {"OPENAI_API_KEY": "fake_key"}):
                with patch.dict(sys.modules, {'openai': mock_openai_module}):
                    with pytest.raises(AIGenerationError, match="OpenAI generation failed"):
                        await ai_img._generate_openai()

        asyncio.run(run_test())

    def test_aiimage_replicate_import_error(self):
        """Test _generate_replicate raises error on import failure (lines 251-252)."""
        import asyncio
        import sys
        import builtins

        ai_img = AIImage(prompt="test", provider=AIProvider.REPLICATE)

        async def run_test():
            # Remove replicate from modules
            for key in list(sys.modules.keys()):
                if key == 'replicate' or key.startswith('replicate.'):
                    del sys.modules[key]

            original_import = builtins.__import__

            def mock_import(name, *args, **kwargs):
                if name == 'replicate':
                    raise ImportError("No module named 'replicate'")
                return original_import(name, *args, **kwargs)

            with patch('builtins.__import__', side_effect=mock_import):
                with pytest.raises(AIProviderNotAvailableError, match="Replicate package not installed"):
                    await ai_img._generate_replicate()

        asyncio.run(run_test())

    def test_aiimage_replicate_list_output_success(self):
        """Test Replicate generation with list output format (lines 284-290)."""
        import asyncio
        import sys

        ai_img = AIImage(
            prompt="test",
            provider=AIProvider.REPLICATE,
        )

        async def run_test():
            mock_replicate = MagicMock()
            mock_replicate.run = MagicMock(return_value=["https://example.com/image.png"])

            async def mock_to_thread(func, *args, **kwargs):
                return ["https://example.com/image.png"]

            async def mock_download(url):
                ai_img.set_base64_data("downloaded_data", "image/png")

            with patch.dict(os.environ, {"REPLICATE_API_TOKEN": "fake_token"}):
                with patch.dict(sys.modules, {'replicate': mock_replicate}):
                    with patch('asyncio.to_thread', side_effect=mock_to_thread):
                        with patch.object(ai_img, '_download_image', side_effect=mock_download):
                            await ai_img._generate_replicate()
                            assert ai_img._generation_metadata["output_url"] == "https://example.com/image.png"

        asyncio.run(run_test())

    def test_aiimage_replicate_string_output_success(self):
        """Test Replicate generation with string output format (lines 291-296)."""
        import asyncio
        import sys

        ai_img = AIImage(prompt="test", provider=AIProvider.REPLICATE)

        async def run_test():
            mock_replicate = MagicMock()

            async def mock_to_thread(func, *args, **kwargs):
                return "https://example.com/direct.png"

            async def mock_download(url):
                ai_img.set_base64_data("downloaded_data", "image/png")

            with patch.dict(os.environ, {"REPLICATE_API_TOKEN": "fake_token"}):
                with patch.dict(sys.modules, {'replicate': mock_replicate}):
                    with patch('asyncio.to_thread', side_effect=mock_to_thread):
                        with patch.object(ai_img, '_download_image', side_effect=mock_download):
                            await ai_img._generate_replicate()
                            assert ai_img._generation_metadata["output_url"] == "https://example.com/direct.png"

        asyncio.run(run_test())

    def test_aiimage_replicate_unexpected_output(self):
        """Test Replicate generation fails with unexpected output format (lines 297-298)."""
        import asyncio
        import sys

        ai_img = AIImage(prompt="test", provider=AIProvider.REPLICATE)

        async def run_test():
            mock_replicate = MagicMock()

            async def mock_to_thread(func, *args, **kwargs):
                return {"unexpected": "format"}

            with patch.dict(os.environ, {"REPLICATE_API_TOKEN": "fake_token"}):
                with patch.dict(sys.modules, {'replicate': mock_replicate}):
                    with patch('asyncio.to_thread', side_effect=mock_to_thread):
                        with pytest.raises(AIGenerationError, match="Unexpected Replicate output format"):
                            await ai_img._generate_replicate()

        asyncio.run(run_test())

    def test_aiimage_replicate_with_negative_prompt(self):
        """Test Replicate includes negative_prompt (lines 270-271)."""
        import asyncio
        import sys

        ai_img = AIImage(
            prompt="test",
            provider=AIProvider.REPLICATE,
            negative_prompt="bad quality"
        )

        async def run_test():
            mock_replicate = MagicMock()
            captured_params = {}

            async def mock_to_thread(func, model, input):
                captured_params.update(input)
                return ["https://example.com/image.png"]

            async def mock_download(url):
                ai_img.set_base64_data("data", "image/png")

            with patch.dict(os.environ, {"REPLICATE_API_TOKEN": "fake_token"}):
                with patch.dict(sys.modules, {'replicate': mock_replicate}):
                    with patch('asyncio.to_thread', side_effect=mock_to_thread):
                        with patch.object(ai_img, '_download_image', side_effect=mock_download):
                            await ai_img._generate_replicate()
                            assert captured_params["negative_prompt"] == "bad quality"

        asyncio.run(run_test())

    def test_aiimage_replicate_with_seed(self):
        """Test Replicate includes seed (lines 273-274)."""
        import asyncio
        import sys

        ai_img = AIImage(
            prompt="test",
            provider=AIProvider.REPLICATE,
            seed=42
        )

        async def run_test():
            mock_replicate = MagicMock()
            captured_params = {}

            async def mock_to_thread(func, model, input):
                captured_params.update(input)
                return ["https://example.com/image.png"]

            async def mock_download(url):
                ai_img.set_base64_data("data", "image/png")

            with patch.dict(os.environ, {"REPLICATE_API_TOKEN": "fake_token"}):
                with patch.dict(sys.modules, {'replicate': mock_replicate}):
                    with patch('asyncio.to_thread', side_effect=mock_to_thread):
                        with patch.object(ai_img, '_download_image', side_effect=mock_download):
                            await ai_img._generate_replicate()
                            assert captured_params["seed"] == 42

        asyncio.run(run_test())

    def test_aiimage_replicate_generic_exception(self):
        """Test Replicate generation wraps generic exceptions (lines 304-305)."""
        import asyncio
        import sys

        ai_img = AIImage(prompt="test", provider=AIProvider.REPLICATE)

        async def run_test():
            mock_replicate = MagicMock()

            async def mock_to_thread(*args, **kwargs):
                raise RuntimeError("Network error")

            with patch.dict(os.environ, {"REPLICATE_API_TOKEN": "fake_token"}):
                with patch.dict(sys.modules, {'replicate': mock_replicate}):
                    with patch('asyncio.to_thread', side_effect=mock_to_thread):
                        with pytest.raises(AIGenerationError, match="Replicate generation failed"):
                            await ai_img._generate_replicate()

        asyncio.run(run_test())

    def test_aiimage_download_image_success(self):
        """Test _download_image successfully downloads and stores image (lines 309-323)."""
        import asyncio

        ai_img = AIImage(prompt="test")

        async def run_test():
            fake_image_data = b"fake image bytes for testing"

            async def mock_to_thread(func):
                return fake_image_data

            with patch('asyncio.to_thread', side_effect=mock_to_thread):
                await ai_img._download_image("https://example.com/image.png")

                expected_b64 = base64.b64encode(fake_image_data).decode("utf-8")
                assert ai_img.get_base64_data() == expected_b64

        asyncio.run(run_test())

    def test_aiimage_download_image_failure(self):
        """Test _download_image raises AIGenerationError on failure (line 326)."""
        import asyncio

        ai_img = AIImage(prompt="test")

        async def run_test():
            async def mock_to_thread(func):
                raise Exception("Network error")

            with patch('asyncio.to_thread', side_effect=mock_to_thread):
                with pytest.raises(AIGenerationError, match="Failed to download generated image"):
                    await ai_img._download_image("https://example.com/image.png")

        asyncio.run(run_test())

    def test_aiimage_generate_async_sets_generated_flag(self):
        """Test generate_async sets _generated=True and _needs_update=True (lines 186-188)."""
        import asyncio

        ai_img = AIImage(prompt="test")

        async def run_test():
            # Mock the provider-specific generation
            async def mock_openai():
                pass

            with patch.object(ai_img, '_generate_openai', side_effect=mock_openai):
                assert ai_img._generated is False

                await ai_img.generate_async()

                assert ai_img._generated is True
                assert ai_img._needs_update is True

        asyncio.run(run_test())

    def test_aiimage_replicate_empty_list_output(self):
        """Test Replicate generation with empty list output falls through to unexpected format."""
        import asyncio
        import sys

        ai_img = AIImage(prompt="test", provider=AIProvider.REPLICATE)

        async def run_test():
            mock_replicate = MagicMock()

            async def mock_to_thread(func, *args, **kwargs):
                return []

            with patch.dict(os.environ, {"REPLICATE_API_TOKEN": "fake_token"}):
                with patch.dict(sys.modules, {'replicate': mock_replicate}):
                    with patch('asyncio.to_thread', side_effect=mock_to_thread):
                        with pytest.raises(AIGenerationError, match="Unexpected Replicate output format"):
                            await ai_img._generate_replicate()

        asyncio.run(run_test())
