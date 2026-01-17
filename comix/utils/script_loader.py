"""Script loading utilities for Comix.

Provides shared functions for loading Python scripts and finding Page objects,
used by CLI commands and the preview server.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from comix.page.page import Page


class ScriptLoadError(Exception):
    """Error loading a comic script."""

    pass


def load_script_module(script_path: str | Path, module_name: str | None = None) -> ModuleType:
    """Load a Python script as a module.

    Args:
        script_path: Path to the Python script file.
        module_name: Optional module name. If None, generates a unique name.

    Returns:
        The loaded module.

    Raises:
        ScriptLoadError: If the script cannot be loaded (file not found, etc.).
    """
    path = Path(script_path).resolve()

    # Check if file exists
    if not path.exists():
        raise ScriptLoadError(f"Script file not found: {path}")

    if module_name is None:
        module_name = f"comic_script_{id(path)}"

    # Remove any previously imported module from cache
    if module_name in sys.modules:
        del sys.modules[module_name]

    # Invalidate import caches to ensure fresh load
    importlib.invalidate_caches()

    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ScriptLoadError(f"Could not load script: {path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    return module


def find_page_in_module(module: ModuleType) -> Page | None:
    """Find a Page class or instance in a module.

    First looks for Page subclasses (and instantiates them),
    then looks for existing Page instances.

    Args:
        module: The module to search.

    Returns:
        A Page instance, or None if not found.
    """
    from comix.page.page import Page

    # First try to find Page subclasses
    for name in dir(module):
        obj = getattr(module, name)
        if isinstance(obj, type) and issubclass(obj, Page) and obj is not Page:
            return obj()

    # Then look for Page instances
    for name in dir(module):
        obj = getattr(module, name)
        if isinstance(obj, Page):
            return obj

    return None


def load_page_from_script(script_path: str | Path) -> Page:
    """Load a Page from a comic script file.

    This is a convenience function that combines load_script_module
    and find_page_in_module.

    Args:
        script_path: Path to the Python script file.

    Returns:
        A Page instance.

    Raises:
        ScriptLoadError: If the script cannot be loaded or no Page is found.
    """
    module = load_script_module(script_path)
    page = find_page_in_module(module)
    if page is None:
        raise ScriptLoadError("No Page class or instance found in script")
    return page
