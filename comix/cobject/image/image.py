"""Image - CObject for displaying images in comics."""

from __future__ import annotations

import base64
from pathlib import Path
from typing import Any, Self

import numpy as np

from comix.cobject.cobject import CObject


class Image(CObject):
    """Image element for displaying images in comics.

    Images can be loaded from file paths, URLs, or base64-encoded data.
    They support the full CObject transformation methods (move_to, scale, etc.).

    Example:
        >>> img = Image("character.png", width=200, height=200)
        >>> img.move_to((100, 100)).set_opacity(0.8)
    """

    def __init__(
        self,
        source: str | None = None,
        width: float = 100.0,
        height: float = 100.0,
        preserve_aspect_ratio: bool = True,
        fit: str = "contain",  # "contain", "cover", "fill", "none"
        **kwargs: Any,
    ) -> None:
        """Initialize an Image.

        Args:
            source: Path to image file, URL, or base64-encoded data.
            width: Display width of the image.
            height: Display height of the image.
            preserve_aspect_ratio: Whether to preserve the original aspect ratio.
            fit: How to fit the image within bounds:
                - "contain": Scale to fit within bounds, preserving aspect ratio
                - "cover": Scale to cover bounds, preserving aspect ratio
                - "fill": Stretch to fill bounds exactly
                - "none": Use original size
            **kwargs: Additional CObject parameters.
        """
        super().__init__(**kwargs)
        self._source = source
        self.width = width
        self.height = height
        self.preserve_aspect_ratio = preserve_aspect_ratio
        self.fit = fit

        # Cached base64 data for rendering
        self._base64_data: str | None = None
        self._mime_type: str = "image/png"

        # Original dimensions (if known)
        self._original_width: float | None = None
        self._original_height: float | None = None

        self.generate_points()

    @property
    def source(self) -> str | None:
        """Get the image source."""
        return self._source

    def set_source(self, source: str) -> Self:
        """Set the image source.

        Args:
            source: Path to image file, URL, or base64-encoded data.

        Returns:
            Self for method chaining.
        """
        self._source = source
        self._base64_data = None  # Clear cached data
        self._needs_update = True
        return self

    def set_size(self, width: float, height: float) -> Self:
        """Set the display size.

        Args:
            width: Display width.
            height: Display height.

        Returns:
            Self for method chaining.
        """
        self.width = width
        self.height = height
        self._needs_update = True
        self.generate_points()
        return self

    def set_fit(self, fit: str) -> Self:
        """Set the fit mode.

        Args:
            fit: One of "contain", "cover", "fill", "none".

        Returns:
            Self for method chaining.
        """
        if fit not in ("contain", "cover", "fill", "none"):
            raise ValueError(f"Invalid fit mode: {fit}")
        self.fit = fit
        self._needs_update = True
        return self

    def generate_points(self) -> None:
        """Generate bounding box points for the image."""
        half_w = self.width / 2
        half_h = self.height / 2

        self._points = np.array(
            [
                [-half_w, -half_h],
                [half_w, -half_h],
                [half_w, half_h],
                [-half_w, half_h],
                [-half_w, -half_h],  # Close the path
            ],
            dtype=np.float64,
        )

    def load_from_file(self, path: str | Path) -> Self:
        """Load image from a file path.

        Args:
            path: Path to the image file.

        Returns:
            Self for method chaining.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        file_path = Path(path)
        if not file_path.exists():
            raise FileNotFoundError(f"Image file not found: {path}")

        self._source = str(file_path.absolute())

        # Detect MIME type from extension
        suffix = file_path.suffix.lower()
        mime_types = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".gif": "image/gif",
            ".webp": "image/webp",
            ".svg": "image/svg+xml",
            ".bmp": "image/bmp",
        }
        self._mime_type = mime_types.get(suffix, "image/png")

        # Read and encode as base64
        with open(file_path, "rb") as f:
            self._base64_data = base64.b64encode(f.read()).decode("utf-8")

        self._needs_update = True
        return self

    def set_base64_data(self, data: str, mime_type: str = "image/png") -> Self:
        """Set image from base64-encoded data.

        Args:
            data: Base64-encoded image data.
            mime_type: MIME type of the image.

        Returns:
            Self for method chaining.
        """
        self._base64_data = data
        self._mime_type = mime_type
        self._source = f"data:{mime_type};base64,..."  # Placeholder source indicator
        self._needs_update = True
        return self

    def get_base64_data(self) -> str | None:
        """Get the base64-encoded image data.

        Returns:
            Base64-encoded data if available, None otherwise.
        """
        if self._base64_data:
            return self._base64_data

        # Try to load from source if it's a file path
        if self._source and not self._source.startswith(("http://", "https://", "data:")):
            try:
                self.load_from_file(self._source)
                return self._base64_data
            except FileNotFoundError:
                pass

        return None

    def get_data_uri(self) -> str | None:
        """Get the image as a data URI.

        Returns:
            Data URI string if data is available, None otherwise.
        """
        data = self.get_base64_data()
        if data:
            return f"data:{self._mime_type};base64,{data}"
        return None

    def get_render_data(self) -> dict[str, Any]:
        """Get data for rendering."""
        data = super().get_render_data()
        data.update(
            {
                "source": self._source,
                "image_width": self.width,
                "image_height": self.height,
                "preserve_aspect_ratio": self.preserve_aspect_ratio,
                "fit": self.fit,
                "base64_data": self.get_base64_data(),
                "mime_type": self._mime_type,
                "data_uri": self.get_data_uri(),
            }
        )
        return data

    def __repr__(self) -> str:
        source_str = self._source[:50] + "..." if self._source and len(self._source) > 50 else self._source
        return f"Image(source={source_str!r}, width={self.width}, height={self.height})"
