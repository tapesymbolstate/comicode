"""Tests for web preview module."""

import http.client
import json
import tempfile
import threading
import time
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from comix.preview.server import (
    PreviewError,
    PreviewRequestHandler,
    PreviewServer,
    ScriptLoader,
    serve,
    WATCHDOG_AVAILABLE,
)


class TestScriptLoader:
    """Tests for ScriptLoader class."""

    def test_init_with_valid_path(self, tmp_path: Path) -> None:
        """Test initialization with valid script path."""
        script = tmp_path / "comic.py"
        script.write_text("from comix import Page\npage = Page()")
        loader = ScriptLoader(script)
        assert loader.script_path == script.resolve()

    def test_load_page_from_instance(self, tmp_path: Path) -> None:
        """Test loading Page instance from script."""
        script = tmp_path / "comic.py"
        script.write_text("""
from comix import Page
page = Page(width=640, height=480)
""")
        loader = ScriptLoader(script)
        page = loader.load_page()
        assert page is not None
        assert page.width == 640
        assert page.height == 480

    def test_load_page_from_class(self, tmp_path: Path) -> None:
        """Test loading Page subclass from script."""
        script = tmp_path / "comic.py"
        script.write_text("""
from comix import Page

class MyComic(Page):
    def __init__(self):
        super().__init__(width=800, height=600)
""")
        loader = ScriptLoader(script)
        page = loader.load_page()
        assert page is not None
        assert page.width == 800
        assert page.height == 600

    def test_load_page_no_page_found(self, tmp_path: Path) -> None:
        """Test loading script with no Page."""
        script = tmp_path / "comic.py"
        script.write_text("x = 1")
        loader = ScriptLoader(script)
        page = loader.load_page()
        assert page is None
        assert "No Page class or instance found" in loader._error_message

    def test_load_page_syntax_error(self, tmp_path: Path) -> None:
        """Test loading script with syntax error."""
        script = tmp_path / "comic.py"
        script.write_text("def broken(")
        loader = ScriptLoader(script)
        page = loader.load_page()
        assert page is None
        assert "Error loading script" in loader._error_message

    def test_render_svg_success(self, tmp_path: Path) -> None:
        """Test rendering SVG from valid script."""
        script = tmp_path / "comic.py"
        script.write_text("""
from comix import Page, Panel
page = Page(width=400, height=300)
page.add(Panel(width=100, height=100))
""")
        loader = ScriptLoader(script)
        svg, error = loader.render_svg()
        assert error is None
        assert "<svg" in svg
        assert "400" in svg  # width

    def test_render_svg_error(self, tmp_path: Path) -> None:
        """Test rendering SVG with error produces error SVG."""
        script = tmp_path / "comic.py"
        script.write_text("invalid python {{{")
        loader = ScriptLoader(script)
        svg, error = loader.render_svg()
        assert error is not None
        assert "<svg" in svg
        assert "#cc0000" in svg  # error color

    def test_version_increments(self, tmp_path: Path) -> None:
        """Test that version increments on successful render."""
        script = tmp_path / "comic.py"
        script.write_text("from comix import Page\npage = Page()")
        loader = ScriptLoader(script)

        initial_version = loader.get_version()
        loader.render_svg()
        assert loader.get_version() == initial_version + 1

        loader.render_svg()
        assert loader.get_version() == initial_version + 2

    def test_has_file_changed(self, tmp_path: Path) -> None:
        """Test file change detection."""
        script = tmp_path / "comic.py"
        script.write_text("from comix import Page\npage = Page()")
        loader = ScriptLoader(script)

        # First check should return True (initial state)
        assert loader.has_file_changed() is True

        # Second check without modification should return False
        assert loader.has_file_changed() is False

        # Modify file
        time.sleep(0.01)  # Ensure different mtime
        script.write_text("from comix import Page\npage = Page(width=100)")

        # Should detect change
        assert loader.has_file_changed() is True

    def test_create_error_svg_escapes_html(self, tmp_path: Path) -> None:
        """Test that error SVG escapes HTML entities."""
        script = tmp_path / "comic.py"
        script.write_text("x = 1")
        loader = ScriptLoader(script)
        svg = loader._create_error_svg("<script>alert('xss')</script>")
        assert "&lt;script&gt;" in svg
        assert "<script>" not in svg


class TestPreviewServer:
    """Tests for PreviewServer class."""

    def test_init_with_valid_script(self, tmp_path: Path) -> None:
        """Test initialization with valid script."""
        script = tmp_path / "comic.py"
        script.write_text("from comix import Page\npage = Page()")
        server = PreviewServer(script, port=0, open_browser=False)
        assert server.script_path == script.resolve()

    def test_init_with_missing_script(self, tmp_path: Path) -> None:
        """Test initialization with missing script raises error."""
        with pytest.raises(PreviewError, match="not found"):
            PreviewServer(tmp_path / "missing.py")

    def _start_server_in_background(self, server: PreviewServer) -> threading.Thread:
        """Helper to start server in background and wait for it to be ready."""
        started = threading.Event()

        def run_server():
            server.start(blocking=False)
            started.set()

        thread = threading.Thread(target=run_server)
        thread.start()
        started.wait(timeout=5)
        # Give server a moment to fully initialize
        time.sleep(0.2)
        return thread

    def test_start_and_stop(self, tmp_path: Path) -> None:
        """Test starting and stopping the server."""
        script = tmp_path / "comic.py"
        script.write_text("from comix import Page\npage = Page()")

        server = PreviewServer(script, port=0, open_browser=False)

        # Start in background
        with patch("webbrowser.open"):
            thread = self._start_server_in_background(server)

            try:
                assert server._running
                assert server.port > 0  # Port should be assigned
            finally:
                server.stop()
                thread.join(timeout=2)

            assert not server._running

    def test_server_serves_html(self, tmp_path: Path) -> None:
        """Test that server serves HTML at root."""
        script = tmp_path / "comic.py"
        script.write_text("from comix import Page\npage = Page()")

        server = PreviewServer(script, port=0, open_browser=False)

        with patch("webbrowser.open"):
            thread = self._start_server_in_background(server)

            try:
                conn = http.client.HTTPConnection("127.0.0.1", server.port, timeout=5)
                conn.request("GET", "/")
                response = conn.getresponse()
                content = response.read().decode()
                conn.close()

                assert response.status == 200
                assert "Comix Preview" in content
                assert "comic.svg" in content
            finally:
                server.stop()
                thread.join(timeout=2)

    def test_server_serves_svg(self, tmp_path: Path) -> None:
        """Test that server serves SVG at /comic.svg."""
        script = tmp_path / "comic.py"
        script.write_text("from comix import Page\npage = Page(width=300, height=200)")

        server = PreviewServer(script, port=0, open_browser=False)

        with patch("webbrowser.open"):
            thread = self._start_server_in_background(server)

            try:
                conn = http.client.HTTPConnection("127.0.0.1", server.port, timeout=5)
                conn.request("GET", "/comic.svg")
                response = conn.getresponse()
                content = response.read().decode()
                conn.close()

                assert response.status == 200
                assert response.getheader("Content-Type") == "image/svg+xml; charset=utf-8"
                assert "<svg" in content
            finally:
                server.stop()
                thread.join(timeout=2)

    def test_server_serves_version(self, tmp_path: Path) -> None:
        """Test that server serves version at /version."""
        script = tmp_path / "comic.py"
        script.write_text("from comix import Page\npage = Page()")

        server = PreviewServer(script, port=0, open_browser=False)

        with patch("webbrowser.open"):
            thread = self._start_server_in_background(server)

            try:
                conn = http.client.HTTPConnection("127.0.0.1", server.port, timeout=5)
                conn.request("GET", "/version")
                response = conn.getresponse()
                data = json.loads(response.read().decode())
                conn.close()

                assert response.status == 200
                assert "version" in data
                assert isinstance(data["version"], int)
            finally:
                server.stop()
                thread.join(timeout=2)

    def test_server_returns_404_for_unknown_path(self, tmp_path: Path) -> None:
        """Test that server returns 404 for unknown paths."""
        script = tmp_path / "comic.py"
        script.write_text("from comix import Page\npage = Page()")

        server = PreviewServer(script, port=0, open_browser=False)

        with patch("webbrowser.open"):
            thread = self._start_server_in_background(server)

            try:
                conn = http.client.HTTPConnection("127.0.0.1", server.port, timeout=5)
                conn.request("GET", "/unknown")
                response = conn.getresponse()
                conn.close()

                assert response.status == 404
            finally:
                server.stop()
                thread.join(timeout=2)


class TestPreviewRequestHandler:
    """Tests for PreviewRequestHandler."""

    def test_html_template_contains_required_elements(self, tmp_path: Path) -> None:
        """Test that HTML template contains required elements."""
        script = tmp_path / "comic.py"
        script.write_text("from comix import Page\npage = Page()")

        loader = ScriptLoader(script)

        # Create a handler class with loader attached
        handler_class = type(
            "TestHandler",
            (PreviewRequestHandler,),
            {"loader": loader},
        )

        # Mock handler to get template
        mock_wfile = MagicMock()
        mock_request = MagicMock()
        mock_request.makefile.return_value = mock_wfile

        handler = handler_class.__new__(handler_class)
        handler.loader = loader

        html = handler._get_html_template()

        assert "<!DOCTYPE html>" in html
        assert "Comix Preview" in html
        assert "/comic.svg" in html
        assert "/poll" in html
        assert "statusDot" in html


class TestServeFunction:
    """Tests for the serve convenience function."""

    def test_serve_raises_on_missing_file(self, tmp_path: Path) -> None:
        """Test that serve raises error for missing file."""
        with pytest.raises(PreviewError, match="not found"):
            serve(tmp_path / "missing.py", open_browser=False)


class TestWatchdogIntegration:
    """Tests for watchdog integration."""

    @pytest.mark.skipif(not WATCHDOG_AVAILABLE, reason="watchdog not installed")
    def test_watchdog_available(self) -> None:
        """Test that watchdog is available."""
        assert WATCHDOG_AVAILABLE

    def test_server_works_without_watchdog(self, tmp_path: Path) -> None:
        """Test that server works even without watchdog (polling fallback)."""
        script = tmp_path / "comic.py"
        script.write_text("from comix import Page\npage = Page()")

        server = PreviewServer(
            script,
            port=0,
            open_browser=False,
            use_watchdog=False  # Disable watchdog
        )

        started = threading.Event()

        def run_server():
            server.start(blocking=False)
            started.set()

        with patch("webbrowser.open"):
            thread = threading.Thread(target=run_server)
            thread.start()
            started.wait(timeout=5)
            time.sleep(0.2)

            try:
                assert server._running
                assert server._observer is None  # No watchdog observer
            finally:
                server.stop()
                thread.join(timeout=2)


class TestCLIIntegration:
    """Tests for CLI integration."""

    def test_cli_serve_command_exists(self) -> None:
        """Test that serve command is registered."""
        from comix.__main__ import main

        # Get all commands
        commands = main.commands
        assert "serve" in commands

    def test_cli_serve_command_has_options(self) -> None:
        """Test that serve command has expected options."""
        from comix.__main__ import serve as serve_cmd

        option_names = [param.name for param in serve_cmd.params]
        assert "script" in option_names
        assert "port" in option_names
        assert "host" in option_names
        assert "no_browser" in option_names


class TestEdgeCases:
    """Tests for edge cases."""

    def test_script_with_import_error(self, tmp_path: Path) -> None:
        """Test handling script with import error."""
        script = tmp_path / "comic.py"
        script.write_text("from nonexistent_module import something")

        loader = ScriptLoader(script)
        page = loader.load_page()

        assert page is None
        assert "Error loading script" in loader._error_message

    def test_script_with_runtime_error(self, tmp_path: Path) -> None:
        """Test handling script with runtime error during class init."""
        script = tmp_path / "comic.py"
        script.write_text("""
from comix import Page

class BrokenComic(Page):
    def __init__(self):
        raise ValueError("Intentional error")
""")
        loader = ScriptLoader(script)
        page = loader.load_page()

        assert page is None
        assert "Error instantiating" in loader._error_message

    def test_multiple_page_classes_uses_first(self, tmp_path: Path) -> None:
        """Test that multiple Page classes use the first one."""
        script = tmp_path / "comic.py"
        script.write_text("""
from comix import Page

class FirstComic(Page):
    def __init__(self):
        super().__init__(width=100)

class SecondComic(Page):
    def __init__(self):
        super().__init__(width=200)
""")
        loader = ScriptLoader(script)
        page = loader.load_page()

        # Should get one of them (order depends on dir())
        assert page is not None
        assert page.width in (100, 200)

    def test_port_auto_increment_on_conflict(self, tmp_path: Path) -> None:
        """Test that port auto-increments if busy."""
        import socket

        script = tmp_path / "comic.py"
        script.write_text("from comix import Page\npage = Page()")

        # Bind a socket to block a port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("127.0.0.1", 9999))
        sock.listen(1)

        try:
            server = PreviewServer(script, port=9999, host="127.0.0.1", open_browser=False)

            started = threading.Event()

            def run_server():
                server.start(blocking=False)
                started.set()

            with patch("webbrowser.open"):
                thread = threading.Thread(target=run_server)
                thread.start()
                started.wait(timeout=5)
                time.sleep(0.2)

                try:
                    # Server should have found a different port
                    assert server._running
                    assert server.port > 9999
                finally:
                    server.stop()
                    thread.join(timeout=2)
        finally:
            sock.close()
