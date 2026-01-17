"""AIImage - AI-generated images for comics using OpenAI or Replicate."""

from __future__ import annotations

import asyncio
import base64
import os
from enum import Enum
from typing import Any, Self

from comix.cobject.image.image import Image


class AIProvider(Enum):
    """Supported AI image generation providers."""

    OPENAI = "openai"
    REPLICATE = "replicate"


class AIImageError(Exception):
    """Base exception for AI image generation errors."""

    pass


class AIProviderNotAvailableError(AIImageError):
    """Raised when the required AI provider package is not installed."""

    pass


class AIGenerationError(AIImageError):
    """Raised when image generation fails."""

    pass


class AIImage(Image):
    """AI-generated image element for comics.

    Generates images using AI services (OpenAI DALL-E or Replicate)
    based on text prompts. The generated image is automatically loaded
    and can be rendered like any other Image.

    Example:
        >>> ai_img = AIImage(
        ...     prompt="A heroic samurai standing on a cliff at sunset",
        ...     provider=AIProvider.OPENAI,
        ...     width=512,
        ...     height=512,
        ... )
        >>> ai_img.generate()  # Synchronous generation
        >>> # or
        >>> await ai_img.generate_async()  # Async generation

    Note:
        Requires API keys:
        - OpenAI: Set OPENAI_API_KEY environment variable
        - Replicate: Set REPLICATE_API_TOKEN environment variable
    """

    def __init__(
        self,
        prompt: str = "",
        provider: AIProvider | str = AIProvider.OPENAI,
        model: str | None = None,
        width: float = 512.0,
        height: float = 512.0,
        quality: str = "standard",  # "standard" or "hd" (OpenAI)
        style: str | None = None,  # "vivid" or "natural" (OpenAI)
        negative_prompt: str | None = None,  # For Replicate models
        seed: int | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize an AIImage.

        Args:
            prompt: Text description of the image to generate.
            provider: AI provider to use (AIProvider.OPENAI or AIProvider.REPLICATE).
            model: Specific model to use. Defaults:
                - OpenAI: "dall-e-3"
                - Replicate: "stability-ai/sdxl"
            width: Image width (may be adjusted by provider).
            height: Image height (may be adjusted by provider).
            quality: Image quality ("standard" or "hd" for OpenAI).
            style: Image style ("vivid" or "natural" for OpenAI).
            negative_prompt: What to avoid in the image (Replicate).
            seed: Random seed for reproducibility (if supported).
            **kwargs: Additional CObject/Image parameters.
        """
        super().__init__(source=None, width=width, height=height, **kwargs)

        self.prompt = prompt
        self.provider = AIProvider(provider) if isinstance(provider, str) else provider
        self.quality = quality
        self.image_style = style  # 'style' is used by CObject
        self.negative_prompt = negative_prompt
        self.seed = seed

        # Set default model based on provider
        if model is None:
            if self.provider == AIProvider.OPENAI:
                self.model = "dall-e-3"
            else:
                self.model = "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b"
        else:
            self.model = model

        # Generation state
        self._generated = False
        self._generation_metadata: dict[str, Any] = {}

    @property
    def is_generated(self) -> bool:
        """Check if the image has been generated."""
        return self._generated

    def set_prompt(self, prompt: str) -> Self:
        """Set the generation prompt.

        Args:
            prompt: Text description of the image.

        Returns:
            Self for method chaining.
        """
        self.prompt = prompt
        self._generated = False  # Mark as needing regeneration
        return self

    def set_provider(self, provider: AIProvider | str) -> Self:
        """Set the AI provider.

        Args:
            provider: AIProvider enum or string.

        Returns:
            Self for method chaining.
        """
        self.provider = AIProvider(provider) if isinstance(provider, str) else provider
        return self

    def set_model(self, model: str) -> Self:
        """Set the model to use.

        Args:
            model: Model identifier.

        Returns:
            Self for method chaining.
        """
        self.model = model
        return self

    def generate(self) -> Self:
        """Generate the image synchronously.

        Returns:
            Self for method chaining.

        Raises:
            AIProviderNotAvailableError: If the provider package is not installed.
            AIGenerationError: If generation fails.
        """
        return asyncio.run(self.generate_async())

    async def generate_async(self) -> Self:
        """Generate the image asynchronously.

        Returns:
            Self for method chaining.

        Raises:
            AIProviderNotAvailableError: If the provider package is not installed.
            AIGenerationError: If generation fails.
        """
        if not self.prompt:
            raise AIGenerationError("No prompt provided for image generation")

        if self.provider == AIProvider.OPENAI:
            await self._generate_openai()
        elif self.provider == AIProvider.REPLICATE:
            await self._generate_replicate()

        self._generated = True
        self._needs_update = True
        return self

    async def _generate_openai(self) -> None:
        """Generate image using OpenAI DALL-E."""
        try:
            from openai import AsyncOpenAI
        except ImportError as e:
            raise AIProviderNotAvailableError(
                "OpenAI package not installed. Install with: pip install openai"
            ) from e

        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise AIGenerationError(
                "OPENAI_API_KEY environment variable not set"
            )

        client = AsyncOpenAI(api_key=api_key)

        # Map dimensions to supported sizes for DALL-E 3
        # DALL-E 3 supports: 1024x1024, 1792x1024, 1024x1792
        size = self._get_openai_size()

        try:
            kwargs: dict[str, Any] = {
                "model": self.model,
                "prompt": self.prompt,
                "size": size,
                "quality": self.quality,
                "response_format": "b64_json",
                "n": 1,
            }

            if self.image_style:
                kwargs["style"] = self.image_style

            response = await client.images.generate(**kwargs)

            if response.data and len(response.data) > 0:
                image_data = response.data[0]
                if image_data.b64_json:
                    self.set_base64_data(image_data.b64_json, "image/png")
                    self._generation_metadata = {
                        "model": self.model,
                        "revised_prompt": image_data.revised_prompt,
                        "size": size,
                    }
                else:
                    raise AIGenerationError("No image data in OpenAI response")
            else:
                raise AIGenerationError("Empty response from OpenAI")

        except ImportError:
            raise
        except AIGenerationError:
            raise
        except Exception as e:
            raise AIGenerationError(f"OpenAI generation failed: {e}") from e

    async def _generate_replicate(self) -> None:
        """Generate image using Replicate."""
        try:
            import replicate
        except ImportError as e:
            raise AIProviderNotAvailableError(
                "Replicate package not installed. Install with: pip install replicate"
            ) from e

        api_token = os.environ.get("REPLICATE_API_TOKEN")
        if not api_token:
            raise AIGenerationError(
                "REPLICATE_API_TOKEN environment variable not set"
            )

        try:
            # Build input parameters
            input_params: dict[str, Any] = {
                "prompt": self.prompt,
                "width": int(self.width),
                "height": int(self.height),
            }

            if self.negative_prompt:
                input_params["negative_prompt"] = self.negative_prompt

            if self.seed is not None:
                input_params["seed"] = self.seed

            # Run the model
            output = await asyncio.to_thread(
                replicate.run,
                self.model,
                input=input_params,
            )

            # Output format varies by model, usually a list of URLs
            if isinstance(output, list) and len(output) > 0:
                image_url = output[0]
                await self._download_image(str(image_url))
                self._generation_metadata = {
                    "model": self.model,
                    "output_url": str(image_url),
                }
            elif isinstance(output, str):
                await self._download_image(output)
                self._generation_metadata = {
                    "model": self.model,
                    "output_url": output,
                }
            else:
                raise AIGenerationError(f"Unexpected Replicate output format: {type(output)}")

        except ImportError:
            raise
        except AIGenerationError:
            raise
        except Exception as e:
            raise AIGenerationError(f"Replicate generation failed: {e}") from e

    async def _download_image(self, url: str) -> None:
        """Download an image from URL and store as base64."""
        try:
            import urllib.request
            import ssl

            ctx = ssl.create_default_context()

            def fetch() -> bytes:
                with urllib.request.urlopen(url, context=ctx) as response:
                    return response.read()  # type: ignore[no-any-return]

            data = await asyncio.to_thread(fetch)
            self.set_base64_data(base64.b64encode(data).decode("utf-8"), "image/png")

        except Exception as e:
            raise AIGenerationError(f"Failed to download generated image: {e}") from e

    def _get_openai_size(self) -> str:
        """Map dimensions to supported OpenAI sizes."""
        # DALL-E 3 supported sizes: 1024x1024, 1792x1024, 1024x1792
        aspect_ratio = self.width / self.height if self.height > 0 else 1.0

        if aspect_ratio > 1.5:
            return "1792x1024"  # Landscape
        elif aspect_ratio < 0.67:
            return "1024x1792"  # Portrait
        else:
            return "1024x1024"  # Square

    def get_generation_metadata(self) -> dict[str, Any]:
        """Get metadata about the generation.

        Returns:
            Dictionary with generation details (model, revised prompt, etc.)
        """
        return self._generation_metadata.copy()

    def get_render_data(self) -> dict[str, Any]:
        """Get data for rendering."""
        data = super().get_render_data()
        data.update(
            {
                "ai_generated": True,
                "prompt": self.prompt,
                "provider": self.provider.value,
                "model": self.model,
                "is_generated": self._generated,
                "generation_metadata": self._generation_metadata,
            }
        )
        return data

    def __repr__(self) -> str:
        prompt_str = self.prompt[:30] + "..." if len(self.prompt) > 30 else self.prompt
        status = "generated" if self._generated else "pending"
        return f"AIImage(prompt={prompt_str!r}, provider={self.provider.value}, status={status})"
