"""Tests for script loader utilities."""

from pathlib import Path

import pytest

from comix.utils.script_loader import (
    ScriptLoadError,
    load_script_module,
    find_page_in_module,
    load_page_from_script,
)


class TestLoadScriptModule:
    """Tests for load_script_module function."""

    def test_load_valid_script(self, tmp_path: Path) -> None:
        """Test loading a valid Python script."""
        script = tmp_path / "test_script.py"
        script.write_text("x = 42\n")

        module = load_script_module(script)
        assert hasattr(module, "x")
        assert module.x == 42

    def test_load_with_custom_module_name(self, tmp_path: Path) -> None:
        """Test loading with a custom module name."""
        script = tmp_path / "test_script.py"
        script.write_text("value = 'test'\n")

        module = load_script_module(script, "custom_name")
        assert module.__name__ == "custom_name"
        assert module.value == "test"

    def test_load_nonexistent_file_raises(self, tmp_path: Path) -> None:
        """Test that loading a nonexistent file raises ScriptLoadError."""
        script = tmp_path / "nonexistent.py"

        with pytest.raises(ScriptLoadError):
            load_script_module(script)

    def test_load_script_with_syntax_error(self, tmp_path: Path) -> None:
        """Test that a script with syntax error raises an exception."""
        script = tmp_path / "bad_syntax.py"
        script.write_text("def broken(\n")  # Invalid syntax

        with pytest.raises(SyntaxError):
            load_script_module(script)

    def test_load_script_with_import_error(self, tmp_path: Path) -> None:
        """Test that a script with import error raises an exception."""
        script = tmp_path / "bad_import.py"
        script.write_text("import nonexistent_module_xyz\n")

        with pytest.raises(ModuleNotFoundError):
            load_script_module(script)

    def test_load_script_clears_module_cache(self, tmp_path: Path) -> None:
        """Test that loading with the same module name works correctly."""
        script1 = tmp_path / "script1.py"
        script1.write_text("value = 1\n")

        script2 = tmp_path / "script2.py"
        script2.write_text("value = 2\n")

        # Load first script with a module name
        module1 = load_script_module(script1, "test_module_name")
        assert module1.value == 1

        # Load different script with same module name - should get new content
        module2 = load_script_module(script2, "test_module_name")
        assert module2.value == 2
        assert module1.__file__ != module2.__file__

    def test_load_script_from_string_path(self, tmp_path: Path) -> None:
        """Test loading using string path instead of Path object."""
        script = tmp_path / "string_path.py"
        script.write_text("data = [1, 2, 3]\n")

        module = load_script_module(str(script))
        assert module.data == [1, 2, 3]


class TestFindPageInModule:
    """Tests for find_page_in_module function."""

    def test_find_page_class(self, tmp_path: Path) -> None:
        """Test finding a Page subclass in a module."""
        script = tmp_path / "page_class.py"
        script.write_text(
            """
from comix.page.page import Page

class MyPage(Page):
    def __init__(self):
        super().__init__(width=100, height=100)
"""
        )

        module = load_script_module(script)
        page = find_page_in_module(module)

        assert page is not None
        assert page.width == 100
        assert page.height == 100

    def test_find_page_instance(self, tmp_path: Path) -> None:
        """Test finding a Page instance in a module."""
        script = tmp_path / "page_instance.py"
        script.write_text(
            """
from comix.page.page import Page

my_page = Page(width=200, height=300)
"""
        )

        module = load_script_module(script)
        page = find_page_in_module(module)

        assert page is not None
        assert page.width == 200
        assert page.height == 300

    def test_page_class_takes_precedence(self, tmp_path: Path) -> None:
        """Test that Page subclass is found before instance."""
        script = tmp_path / "both.py"
        script.write_text(
            """
from comix.page.page import Page

instance_page = Page(width=100, height=100)

class ClassPage(Page):
    def __init__(self):
        super().__init__(width=500, height=500)
"""
        )

        module = load_script_module(script)
        page = find_page_in_module(module)

        assert page is not None
        # Should get the class-based page (500x500), not the instance (100x100)
        assert page.width == 500
        assert page.height == 500

    def test_no_page_returns_none(self, tmp_path: Path) -> None:
        """Test that None is returned when no Page is found."""
        script = tmp_path / "no_page.py"
        script.write_text("x = 42\n")

        module = load_script_module(script)
        page = find_page_in_module(module)

        assert page is None

    def test_ignores_page_base_class(self, tmp_path: Path) -> None:
        """Test that the Page base class itself is not instantiated."""
        script = tmp_path / "only_base.py"
        script.write_text(
            """
from comix.page.page import Page
# Just importing Page, no subclass or instance
"""
        )

        module = load_script_module(script)
        page = find_page_in_module(module)

        assert page is None


class TestLoadPageFromScript:
    """Tests for load_page_from_script convenience function."""

    def test_load_page_success(self, tmp_path: Path) -> None:
        """Test successfully loading a page from script."""
        script = tmp_path / "comic.py"
        script.write_text(
            """
from comix.page.page import Page

class Comic(Page):
    def __init__(self):
        super().__init__(width=800, height=600)
"""
        )

        page = load_page_from_script(script)
        assert page.width == 800
        assert page.height == 600

    def test_load_page_not_found_raises(self, tmp_path: Path) -> None:
        """Test that ScriptLoadError is raised when no page found."""
        script = tmp_path / "empty.py"
        script.write_text("# No page here\n")

        with pytest.raises(ScriptLoadError, match="No Page class or instance"):
            load_page_from_script(script)

    def test_load_page_file_not_found_raises(self, tmp_path: Path) -> None:
        """Test that ScriptLoadError is raised for nonexistent file."""
        script = tmp_path / "missing.py"

        with pytest.raises(ScriptLoadError):
            load_page_from_script(script)

    def test_load_page_from_string_path(self, tmp_path: Path) -> None:
        """Test loading page using string path."""
        script = tmp_path / "string_comic.py"
        script.write_text(
            """
from comix import Page
page = Page(width=400, height=300)
"""
        )

        page = load_page_from_script(str(script))
        assert page.width == 400
        assert page.height == 300


class TestScriptLoadErrorExport:
    """Tests for ScriptLoadError export."""

    def test_exception_is_importable(self) -> None:
        """Test that ScriptLoadError can be imported from utils."""
        from comix.utils import ScriptLoadError

        assert issubclass(ScriptLoadError, Exception)

    def test_exception_message(self) -> None:
        """Test that ScriptLoadError preserves message."""
        error = ScriptLoadError("Test error message")
        assert str(error) == "Test error message"


class TestUtilityExports:
    """Tests for utility function exports."""

    def test_all_functions_exported_from_utils(self) -> None:
        """Test that all functions are available from comix.utils."""
        from comix.utils import (
            ScriptLoadError,
            load_script_module,
            find_page_in_module,
            load_page_from_script,
        )

        assert callable(load_script_module)
        assert callable(find_page_in_module)
        assert callable(load_page_from_script)
        assert issubclass(ScriptLoadError, Exception)
