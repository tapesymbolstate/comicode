"""Tests for CLI commands using Click's CliRunner."""

from pathlib import Path
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from comix.__main__ import main


@pytest.fixture
def runner() -> CliRunner:
    """Create a CLI runner."""
    return CliRunner()


@pytest.fixture
def sample_script(tmp_path: Path) -> Path:
    """Create a sample comic script for testing."""
    script = tmp_path / "comic.py"
    script.write_text("""
from comix import Page, Panel, Text

page = Page(width=400, height=300)
panel = Panel(width=200, height=150)
panel.add(Text("Hello"))
page.add(panel)
""")
    return script


@pytest.fixture
def sample_class_script(tmp_path: Path) -> Path:
    """Create a sample script with a Page subclass."""
    script = tmp_path / "comic_class.py"
    script.write_text("""
from comix import Page, Panel, Text

class MyComic(Page):
    def __init__(self):
        super().__init__(width=500, height=400)
        self.add(Panel(width=200, height=150))
""")
    return script


class TestInfoCommand:
    """Tests for the info command."""

    def test_info_command_runs(self, runner: CliRunner) -> None:
        """Test that info command runs successfully."""
        result = runner.invoke(main, ["info"])
        assert result.exit_code == 0

    def test_info_displays_framework_name(self, runner: CliRunner) -> None:
        """Test that info displays framework name."""
        result = runner.invoke(main, ["info"])
        assert "Comix" in result.output

    def test_info_displays_version(self, runner: CliRunner) -> None:
        """Test that info displays version."""
        result = runner.invoke(main, ["info"])
        assert "Version: 0.1.0" in result.output

    def test_info_displays_core_components(self, runner: CliRunner) -> None:
        """Test that info displays core components."""
        result = runner.invoke(main, ["info"])
        assert "CObject" in result.output
        assert "Panel" in result.output
        assert "Bubble" in result.output
        assert "Character" in result.output
        assert "Page" in result.output

    def test_info_displays_usage_examples(self, runner: CliRunner) -> None:
        """Test that info displays usage examples."""
        result = runner.invoke(main, ["info"])
        assert "comix render" in result.output
        assert "comix preview" in result.output
        assert "comix serve" in result.output

    def test_info_mentions_manim_inspiration(self, runner: CliRunner) -> None:
        """Test that info mentions Manim inspiration."""
        result = runner.invoke(main, ["info"])
        assert "Manim" in result.output


class TestVersionOption:
    """Tests for the version option."""

    def test_version_option(self, runner: CliRunner) -> None:
        """Test that --version displays version."""
        result = runner.invoke(main, ["--version"])
        assert result.exit_code == 0
        assert "0.1.0" in result.output

    def test_version_short_option(self, runner: CliRunner) -> None:
        """Test that -V works (if supported)."""
        # Click's version_option doesn't support -V by default
        result = runner.invoke(main, ["--version"])
        assert result.exit_code == 0


class TestRenderCommand:
    """Tests for the render command."""

    def test_render_requires_script(self, runner: CliRunner) -> None:
        """Test that render command requires a script argument."""
        result = runner.invoke(main, ["render"])
        assert result.exit_code != 0
        assert "Missing argument" in result.output

    def test_render_with_nonexistent_script(self, runner: CliRunner) -> None:
        """Test that render fails with nonexistent script."""
        result = runner.invoke(main, ["render", "nonexistent.py"])
        assert result.exit_code != 0

    def test_render_svg_with_instance(
        self, runner: CliRunner, sample_script: Path, tmp_path: Path
    ) -> None:
        """Test rendering SVG with Page instance script."""
        output = tmp_path / "output.svg"
        result = runner.invoke(
            main, ["render", str(sample_script), "-o", str(output), "-f", "svg"]
        )
        assert result.exit_code == 0
        assert output.exists()
        assert "Rendered to:" in result.output

    def test_render_svg_with_class(
        self, runner: CliRunner, sample_class_script: Path, tmp_path: Path
    ) -> None:
        """Test rendering SVG with Page subclass script."""
        output = tmp_path / "output.svg"
        result = runner.invoke(
            main, ["render", str(sample_class_script), "-o", str(output), "-f", "svg"]
        )
        assert result.exit_code == 0
        assert output.exists()

    def test_render_default_output(
        self, runner: CliRunner, sample_script: Path
    ) -> None:
        """Test that render uses default output path."""
        # Use isolated filesystem to avoid polluting cwd
        with runner.isolated_filesystem():
            # Copy script to isolated dir
            script = Path("comic.py")
            script.write_text(sample_script.read_text())

            result = runner.invoke(main, ["render", str(script)])
            assert result.exit_code == 0
            assert Path("output.svg").exists()

    def test_render_format_options(self, runner: CliRunner) -> None:
        """Test that format option accepts valid choices."""
        result = runner.invoke(main, ["render", "--help"])
        assert "svg" in result.output
        assert "png" in result.output
        assert "pdf" in result.output

    def test_render_quality_options(self, runner: CliRunner) -> None:
        """Test that quality option accepts valid choices."""
        result = runner.invoke(main, ["render", "--help"])
        assert "low" in result.output
        assert "medium" in result.output
        assert "high" in result.output
        assert "72dpi" in result.output
        assert "150dpi" in result.output
        assert "300dpi" in result.output

    def test_render_invalid_format(
        self, runner: CliRunner, sample_script: Path
    ) -> None:
        """Test that render rejects invalid format."""
        result = runner.invoke(
            main, ["render", str(sample_script), "-f", "invalid"]
        )
        assert result.exit_code != 0
        assert "Invalid value" in result.output

    def test_render_invalid_quality(
        self, runner: CliRunner, sample_script: Path
    ) -> None:
        """Test that render rejects invalid quality."""
        result = runner.invoke(
            main, ["render", str(sample_script), "-q", "ultra"]
        )
        assert result.exit_code != 0
        assert "Invalid value" in result.output

    def test_render_no_page_found(
        self, runner: CliRunner, tmp_path: Path
    ) -> None:
        """Test that render fails when no Page is found in script."""
        script = tmp_path / "empty.py"
        script.write_text("x = 1")
        result = runner.invoke(main, ["render", str(script)])
        assert result.exit_code != 0
        assert "No Page class or instance found" in result.output


class TestPreviewCommand:
    """Tests for the preview command."""

    def test_preview_requires_script(self, runner: CliRunner) -> None:
        """Test that preview command requires a script argument."""
        result = runner.invoke(main, ["preview"])
        assert result.exit_code != 0
        assert "Missing argument" in result.output

    def test_preview_with_nonexistent_script(self, runner: CliRunner) -> None:
        """Test that preview fails with nonexistent script."""
        result = runner.invoke(main, ["preview", "nonexistent.py"])
        assert result.exit_code != 0

    def test_preview_no_page_found(
        self, runner: CliRunner, tmp_path: Path
    ) -> None:
        """Test that preview fails when no Page is found."""
        script = tmp_path / "empty.py"
        script.write_text("x = 1")
        result = runner.invoke(main, ["preview", str(script)])
        assert result.exit_code != 0
        assert "No Page class or instance found" in result.output

    def test_preview_opens_browser(
        self, runner: CliRunner, sample_script: Path
    ) -> None:
        """Test that preview opens browser with page.show()."""
        with patch("webbrowser.open") as mock_open:
            result = runner.invoke(main, ["preview", str(sample_script)])
            # Should succeed and call webbrowser.open
            assert result.exit_code == 0
            mock_open.assert_called_once()


class TestServeCommand:
    """Tests for the serve command."""

    def test_serve_requires_script(self, runner: CliRunner) -> None:
        """Test that serve command requires a script argument."""
        result = runner.invoke(main, ["serve"])
        assert result.exit_code != 0
        assert "Missing argument" in result.output

    def test_serve_with_nonexistent_script(self, runner: CliRunner) -> None:
        """Test that serve fails with nonexistent script."""
        result = runner.invoke(main, ["serve", "nonexistent.py"])
        assert result.exit_code != 0

    def test_serve_has_port_option(self, runner: CliRunner) -> None:
        """Test that serve has port option."""
        result = runner.invoke(main, ["serve", "--help"])
        assert "--port" in result.output
        assert "-p" in result.output
        assert "8000" in result.output  # default value

    def test_serve_has_host_option(self, runner: CliRunner) -> None:
        """Test that serve has host option."""
        result = runner.invoke(main, ["serve", "--help"])
        assert "--host" in result.output
        assert "-H" in result.output
        assert "localhost" in result.output  # default value

    def test_serve_has_no_browser_flag(self, runner: CliRunner) -> None:
        """Test that serve has no-browser flag."""
        result = runner.invoke(main, ["serve", "--help"])
        assert "--no-browser" in result.output


class TestHelpOutput:
    """Tests for help output."""

    def test_main_help(self, runner: CliRunner) -> None:
        """Test main help output."""
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "Comix" in result.output
        assert "render" in result.output
        assert "preview" in result.output
        assert "serve" in result.output
        assert "info" in result.output

    def test_render_help(self, runner: CliRunner) -> None:
        """Test render command help."""
        result = runner.invoke(main, ["render", "--help"])
        assert result.exit_code == 0
        assert "Render a comic script" in result.output
        assert "--output" in result.output
        assert "--format" in result.output
        assert "--quality" in result.output

    def test_preview_help(self, runner: CliRunner) -> None:
        """Test preview command help."""
        result = runner.invoke(main, ["preview", "--help"])
        assert result.exit_code == 0
        assert "Preview" in result.output

    def test_serve_help(self, runner: CliRunner) -> None:
        """Test serve command help."""
        result = runner.invoke(main, ["serve", "--help"])
        assert result.exit_code == 0
        assert "live preview" in result.output
        assert "hot reload" in result.output


class TestCommandRegistration:
    """Tests for command registration."""

    def test_all_commands_registered(self, runner: CliRunner) -> None:
        """Test that all expected commands are registered."""
        commands = main.commands
        assert "render" in commands
        assert "preview" in commands
        assert "serve" in commands
        assert "info" in commands

    def test_render_command_params(self) -> None:
        """Test render command has expected parameters."""
        from comix.__main__ import render

        param_names = [p.name for p in render.params]
        assert "script" in param_names
        assert "output" in param_names
        assert "format" in param_names
        assert "quality" in param_names

    def test_preview_command_params(self) -> None:
        """Test preview command has expected parameters."""
        from comix.__main__ import preview

        param_names = [p.name for p in preview.params]
        assert "script" in param_names

    def test_serve_command_params(self) -> None:
        """Test serve command has expected parameters."""
        from comix.__main__ import serve

        param_names = [p.name for p in serve.params]
        assert "script" in param_names
        assert "port" in param_names
        assert "host" in param_names
        assert "no_browser" in param_names


class TestErrorHandling:
    """Tests for error handling in CLI commands."""

    def test_render_syntax_error_in_script(
        self, runner: CliRunner, tmp_path: Path
    ) -> None:
        """Test that render handles syntax errors in scripts."""
        script = tmp_path / "broken.py"
        script.write_text("def broken(")
        result = runner.invoke(main, ["render", str(script)])
        assert result.exit_code != 0

    def test_preview_syntax_error_in_script(
        self, runner: CliRunner, tmp_path: Path
    ) -> None:
        """Test that preview handles syntax errors in scripts."""
        script = tmp_path / "broken.py"
        script.write_text("def broken(")
        result = runner.invoke(main, ["preview", str(script)])
        assert result.exit_code != 0

    def test_render_import_error_in_script(
        self, runner: CliRunner, tmp_path: Path
    ) -> None:
        """Test that render handles import errors in scripts."""
        script = tmp_path / "bad_import.py"
        script.write_text("from nonexistent_module import something")
        result = runner.invoke(main, ["render", str(script)])
        assert result.exit_code != 0


class TestCompileCommand:
    """Tests for the compile command."""

    def test_compile_requires_scripts(self, runner: CliRunner) -> None:
        """Test that compile command requires script arguments."""
        result = runner.invoke(main, ["compile"])
        assert result.exit_code != 0
        assert "Missing argument" in result.output

    def test_compile_with_nonexistent_script(self, runner: CliRunner) -> None:
        """Test that compile fails with nonexistent script."""
        result = runner.invoke(main, ["compile", "nonexistent.py"])
        assert result.exit_code != 0

    def test_compile_help(self, runner: CliRunner) -> None:
        """Test compile command help."""
        result = runner.invoke(main, ["compile", "--help"])
        assert result.exit_code == 0
        assert "Compile multiple comic scripts" in result.output
        assert "--output" in result.output
        assert "--quality" in result.output
        assert "--title" in result.output
        assert "--author" in result.output

    def test_compile_has_quality_choices(self, runner: CliRunner) -> None:
        """Test that compile has quality choices."""
        result = runner.invoke(main, ["compile", "--help"])
        assert "low" in result.output
        assert "medium" in result.output
        assert "high" in result.output

    def test_compile_no_page_found(
        self, runner: CliRunner, tmp_path: Path
    ) -> None:
        """Test that compile handles script without Page gracefully."""
        script = tmp_path / "empty.py"
        script.write_text("x = 1")
        result = runner.invoke(main, ["compile", str(script)])
        assert result.exit_code != 0
        assert "No pages were loaded" in result.output

    @pytest.fixture
    def check_cairo(self):
        """Skip tests if Cairo is not available."""
        try:
            import cairo  # noqa: F401
        except ImportError:
            pytest.skip("Cairo not available")

    def test_compile_single_script(
        self,
        runner: CliRunner,
        tmp_path: Path,
        sample_script: Path,
        check_cairo,
    ) -> None:
        """Test compiling a single script."""
        output_path = tmp_path / "output.pdf"
        result = runner.invoke(
            main, ["compile", str(sample_script), "-o", str(output_path)]
        )
        assert result.exit_code == 0
        assert "Compiled 1 page" in result.output
        assert output_path.exists()

    def test_compile_multiple_scripts(
        self,
        runner: CliRunner,
        tmp_path: Path,
        check_cairo,
    ) -> None:
        """Test compiling multiple scripts."""
        # Create multiple script files
        script1 = tmp_path / "page1.py"
        script1.write_text("""
from comix import Page, Panel
page = Page()
page.add(Panel(name="Page1"))
""")
        script2 = tmp_path / "page2.py"
        script2.write_text("""
from comix import Page, Panel
page = Page()
page.add(Panel(name="Page2"))
""")

        output_path = tmp_path / "book.pdf"
        result = runner.invoke(
            main,
            ["compile", str(script1), str(script2), "-o", str(output_path)],
        )
        assert result.exit_code == 0
        assert "Compiled 2 page" in result.output
        assert output_path.exists()

    def test_compile_with_title_and_author(
        self,
        runner: CliRunner,
        tmp_path: Path,
        sample_script: Path,
        check_cairo,
    ) -> None:
        """Test compile with title and author metadata."""
        output_path = tmp_path / "book.pdf"
        result = runner.invoke(
            main,
            [
                "compile",
                str(sample_script),
                "-o",
                str(output_path),
                "-t",
                "My Comic",
                "-a",
                "Test Author",
            ],
        )
        assert result.exit_code == 0
        assert output_path.exists()

    def test_compile_skips_bad_scripts(
        self,
        runner: CliRunner,
        tmp_path: Path,
        sample_script: Path,
        check_cairo,
    ) -> None:
        """Test that compile skips scripts without Page but continues."""
        # Create a script without Page
        empty_script = tmp_path / "empty.py"
        empty_script.write_text("x = 1")

        output_path = tmp_path / "book.pdf"
        result = runner.invoke(
            main,
            [
                "compile",
                str(sample_script),
                str(empty_script),
                "-o",
                str(output_path),
            ],
        )
        # Should succeed because at least one valid page was found
        assert result.exit_code == 0
        assert "Warning:" in result.output
        assert "Compiled 1 page" in result.output

    def test_compile_class_based_script(
        self,
        runner: CliRunner,
        tmp_path: Path,
        sample_class_script: Path,
        check_cairo,
    ) -> None:
        """Test compiling a script with Page subclass."""
        output_path = tmp_path / "class_based.pdf"
        result = runner.invoke(
            main, ["compile", str(sample_class_script), "-o", str(output_path)]
        )
        assert result.exit_code == 0
        assert output_path.exists()


class TestCompileCommandParams:
    """Tests for compile command parameters."""

    def test_compile_command_registered(self, runner: CliRunner) -> None:
        """Test that compile command is registered."""
        commands = main.commands
        assert "compile" in commands

    def test_compile_command_params(self) -> None:
        """Test compile command has expected parameters."""
        from comix.__main__ import compile

        param_names = [p.name for p in compile.params]
        assert "scripts" in param_names
        assert "output" in param_names
        assert "quality" in param_names
        assert "title" in param_names
        assert "author" in param_names

    def test_main_help_shows_compile(self, runner: CliRunner) -> None:
        """Test that main help shows compile command."""
        result = runner.invoke(main, ["--help"])
        assert "compile" in result.output
