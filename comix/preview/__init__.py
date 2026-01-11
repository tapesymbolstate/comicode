"""Web preview module with hot reload support.

This module provides a live development server for previewing comics
with automatic refresh when the source script changes.

Example:
    >>> from comix.preview import serve
    >>> serve("my_comic.py")  # Opens browser with live preview
"""

from comix.preview.server import (
    PreviewError,
    PreviewServer,
    ScriptLoader,
    serve,
)

__all__ = [
    "PreviewError",
    "PreviewServer",
    "ScriptLoader",
    "serve",
]
