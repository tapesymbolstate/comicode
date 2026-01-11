"""Web preview server with hot reload support.

Provides a live development server that automatically re-renders and refreshes
the browser when the comic script changes.
"""

from __future__ import annotations

import http.server
import importlib.util
import json
import socketserver
import sys
import threading
import time
import webbrowser
from pathlib import Path
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from comix.page.page import Page

# Check for optional watchdog dependency
try:
    from watchdog.events import FileSystemEventHandler
    from watchdog.observers import Observer

    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False
    Observer = None  # type: ignore[assignment]  # Placeholder when watchdog not installed
    FileSystemEventHandler = object  # type: ignore[misc, assignment]  # Placeholder when watchdog not installed


class PreviewError(Exception):
    """Error during preview server operation."""

    pass


class ScriptLoader:
    """Loads and reloads comic scripts."""

    def __init__(self, script_path: str | Path) -> None:
        self.script_path = Path(script_path).resolve()
        self._last_modified: float = 0.0
        self._cached_svg: str = ""
        self._error_message: str | None = None
        self._version: int = 0

    def load_page(self) -> Page | None:
        """Load the Page from the script file."""
        from comix.page.page import Page

        # Remove any previously imported module from cache
        module_name = f"comic_script_{id(self)}"
        if module_name in sys.modules:
            del sys.modules[module_name]

        spec = importlib.util.spec_from_file_location(module_name, self.script_path)
        if spec is None or spec.loader is None:
            raise PreviewError(f"Could not load script: {self.script_path}")

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module

        try:
            spec.loader.exec_module(module)
        except Exception as e:
            self._error_message = f"Error loading script: {e}"
            return None

        # Look for Page subclass first
        for name in dir(module):
            obj = getattr(module, name)
            if isinstance(obj, type) and issubclass(obj, Page) and obj is not Page:
                try:
                    return obj()
                except Exception as e:
                    self._error_message = f"Error instantiating {name}: {e}"
                    return None

        # Then look for Page instance
        for name in dir(module):
            obj = getattr(module, name)
            if isinstance(obj, Page):
                return obj

        self._error_message = "No Page class or instance found in script"
        return None

    def render_svg(self) -> tuple[str, str | None]:
        """Render the page to SVG string.

        Returns:
            Tuple of (svg_content, error_message).
            If error_message is not None, svg_content will be error placeholder.
        """
        try:
            self._error_message = None
            page = self.load_page()

            if page is None:
                return self._create_error_svg(self._error_message or "Unknown error"), self._error_message

            # Render to in-memory SVG
            page.build()
            page.auto_layout()

            from comix.renderer.svg_renderer import SVGRenderer

            renderer = SVGRenderer(page)
            svg_content = renderer.render_to_string()
            self._cached_svg = svg_content
            self._version += 1
            return svg_content, None

        except Exception as e:
            error_msg = f"Render error: {e}"
            self._error_message = error_msg
            return self._create_error_svg(error_msg), error_msg

    def _create_error_svg(self, message: str) -> str:
        """Create an SVG showing an error message."""
        escaped_message = message.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        return f"""<?xml version="1.0" encoding="utf-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600">
  <rect width="100%" height="100%" fill="#fff0f0"/>
  <text x="50%" y="50%" text-anchor="middle" font-family="monospace" font-size="14" fill="#cc0000">
    {escaped_message}
  </text>
</svg>"""

    def get_version(self) -> int:
        """Get current render version (increments on each successful render)."""
        return self._version

    def has_file_changed(self) -> bool:
        """Check if the script file has been modified."""
        try:
            mtime = self.script_path.stat().st_mtime
            if mtime > self._last_modified:
                self._last_modified = mtime
                return True
            return False
        except OSError:
            return False


class PreviewRequestHandler(http.server.BaseHTTPRequestHandler):
    """HTTP request handler for preview server."""

    loader: ScriptLoader
    on_change_callback: Callable[[], None] | None = None

    def log_message(self, format: str, *args: object) -> None:
        """Suppress default logging."""
        pass

    def do_GET(self) -> None:
        """Handle GET requests."""
        if self.path == "/" or self.path == "/index.html":
            self._serve_html()
        elif self.path == "/comic.svg":
            self._serve_svg()
        elif self.path == "/version":
            self._serve_version()
        elif self.path == "/poll":
            self._serve_poll()
        else:
            self.send_error(404, "Not Found")

    def _serve_html(self) -> None:
        """Serve the HTML wrapper page."""
        html = self._get_html_template()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(html)))
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def _serve_svg(self) -> None:
        """Serve the rendered SVG."""
        svg_content, _ = self.loader.render_svg()
        self.send_response(200)
        self.send_header("Content-Type", "image/svg+xml; charset=utf-8")
        self.send_header("Content-Length", str(len(svg_content)))
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.end_headers()
        self.wfile.write(svg_content.encode("utf-8"))

    def _serve_version(self) -> None:
        """Serve current version number for polling."""
        version = self.loader.get_version()
        data = json.dumps({"version": version})
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.end_headers()
        self.wfile.write(data.encode("utf-8"))

    def _serve_poll(self) -> None:
        """Long-polling endpoint for file changes."""
        initial_version = self.loader.get_version()
        start_time = time.time()
        timeout = 30  # 30 second timeout

        while time.time() - start_time < timeout:
            if self.loader.has_file_changed():
                # Re-render and get new version
                self.loader.render_svg()
                break
            time.sleep(0.2)

        version = self.loader.get_version()
        changed = version != initial_version
        data = json.dumps({"version": version, "changed": changed})

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.end_headers()
        self.wfile.write(data.encode("utf-8"))

    def _get_html_template(self) -> str:
        """Get the HTML template with auto-refresh JavaScript."""
        script_name = self.loader.script_path.name
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comix Preview - {script_name}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: #1a1a2e;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }}
        header {{
            background: #16213e;
            padding: 12px 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 1px solid #0f3460;
        }}
        .logo {{
            color: #e94560;
            font-weight: bold;
            font-size: 18px;
        }}
        .status {{
            display: flex;
            align-items: center;
            gap: 8px;
            color: #a0a0a0;
            font-size: 13px;
        }}
        .status-dot {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #4ade80;
            animation: pulse 2s infinite;
        }}
        .status-dot.error {{
            background: #ef4444;
            animation: none;
        }}
        .status-dot.loading {{
            background: #fbbf24;
        }}
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
        }}
        .script-name {{
            color: #64748b;
            font-size: 13px;
        }}
        main {{
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
            overflow: auto;
        }}
        .comic-container {{
            background: white;
            border-radius: 8px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            max-width: 100%;
            max-height: 100%;
            overflow: hidden;
        }}
        .comic-container img {{
            display: block;
            max-width: 100%;
            max-height: calc(100vh - 100px);
            object-fit: contain;
        }}
        footer {{
            background: #16213e;
            padding: 8px 20px;
            text-align: center;
            color: #64748b;
            font-size: 12px;
            border-top: 1px solid #0f3460;
        }}
        kbd {{
            background: #0f3460;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: monospace;
        }}
    </style>
</head>
<body>
    <header>
        <span class="logo">Comix Preview</span>
        <span class="script-name">{script_name}</span>
        <div class="status">
            <span class="status-dot" id="statusDot"></span>
            <span id="statusText">Watching for changes...</span>
        </div>
    </header>
    <main>
        <div class="comic-container">
            <img id="comicImg" src="/comic.svg" alt="Comic Preview">
        </div>
    </main>
    <footer>
        <kbd>Ctrl+C</kbd> to stop server | Hot reload enabled
    </footer>
    <script>
        const img = document.getElementById('comicImg');
        const statusDot = document.getElementById('statusDot');
        const statusText = document.getElementById('statusText');
        let currentVersion = 0;
        let pollActive = true;

        async function poll() {{
            if (!pollActive) return;

            try {{
                statusDot.className = 'status-dot';
                const response = await fetch('/poll');
                const data = await response.json();

                if (data.changed && data.version !== currentVersion) {{
                    currentVersion = data.version;
                    statusDot.className = 'status-dot loading';
                    statusText.textContent = 'Reloading...';

                    // Add cache-busting timestamp
                    img.src = '/comic.svg?t=' + Date.now();

                    setTimeout(() => {{
                        statusDot.className = 'status-dot';
                        statusText.textContent = 'Watching for changes...';
                    }}, 500);
                }}
            }} catch (e) {{
                statusDot.className = 'status-dot error';
                statusText.textContent = 'Connection lost. Retrying...';
            }}

            // Continue polling
            setTimeout(poll, 100);
        }}

        // Handle image load errors
        img.onerror = function() {{
            statusDot.className = 'status-dot error';
            statusText.textContent = 'Render error';
        }};

        img.onload = function() {{
            statusDot.className = 'status-dot';
        }};

        // Get initial version
        fetch('/version')
            .then(r => r.json())
            .then(data => {{
                currentVersion = data.version;
                poll();
            }})
            .catch(() => poll());
    </script>
</body>
</html>"""


class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    """HTTP server that handles requests in separate threads."""

    allow_reuse_address = True
    daemon_threads = True


if WATCHDOG_AVAILABLE:

    class ScriptChangeHandler(FileSystemEventHandler):
        """Watchdog handler for script file changes."""

        def __init__(self, loader: ScriptLoader, callback: Callable[[], None] | None = None) -> None:
            self.loader = loader
            self.callback = callback
            self._last_event_time: float = 0.0

        def on_modified(self, event: object) -> None:
            """Handle file modification events."""
            # Debounce rapid events
            current_time = time.time()
            if current_time - self._last_event_time < 0.1:
                return
            self._last_event_time = current_time

            # Check if it's our script file
            if hasattr(event, "src_path"):
                src_path = Path(getattr(event, "src_path"))
                if src_path.resolve() == self.loader.script_path:
                    if self.callback:
                        self.callback()


class PreviewServer:
    """Live preview server with hot reload support.

    Starts an HTTP server that serves the rendered comic and automatically
    refreshes when the source script changes.

    Example:
        >>> server = PreviewServer("my_comic.py", port=8080)
        >>> server.start()  # Opens browser and watches for changes

    Args:
        script_path: Path to the comic script file.
        port: Port to run the server on (default: 8000).
        host: Host to bind to (default: localhost).
        open_browser: Whether to open the browser automatically (default: True).
        use_watchdog: Whether to use watchdog for file watching (default: True if available).
    """

    def __init__(
        self,
        script_path: str | Path,
        port: int = 8000,
        host: str = "localhost",
        open_browser: bool = True,
        use_watchdog: bool = True,
    ) -> None:
        self.script_path = Path(script_path).resolve()
        if not self.script_path.exists():
            raise PreviewError(f"Script file not found: {self.script_path}")

        self.port = port
        self.host = host
        self.open_browser = open_browser
        self.use_watchdog = use_watchdog and WATCHDOG_AVAILABLE

        self.loader = ScriptLoader(self.script_path)
        self._server: ThreadedHTTPServer | None = None
        self._observer: Observer | None = None  # type: ignore[valid-type]
        self._running = False

    def start(self, blocking: bool = True) -> None:
        """Start the preview server.

        Args:
            blocking: If True, blocks until the server is stopped (Ctrl+C).
                     If False, runs in background thread.
        """
        if self._running:
            return

        # Create handler class with loader attached
        handler_class = type(
            "PreviewHandler",
            (PreviewRequestHandler,),
            {"loader": self.loader},
        )

        # Find available port
        port = self.port
        for attempt in range(10):
            try:
                self._server = ThreadedHTTPServer((self.host, port), handler_class)
                break
            except OSError:
                if port == 0:
                    # Port 0 failed - this shouldn't happen
                    raise PreviewError("Could not bind to an available port")
                port += 1
        else:
            raise PreviewError(f"Could not find available port starting from {self.port}")

        # Get the actual assigned port (important when port=0 is used)
        self.port = self._server.server_address[1]
        self._running = True

        # Initial render
        self.loader.render_svg()

        # Setup watchdog observer if available
        if self.use_watchdog and WATCHDOG_AVAILABLE:
            self._setup_watchdog()

        # Start server in thread
        server_thread = threading.Thread(target=self._server.serve_forever)
        server_thread.daemon = True
        server_thread.start()

        url = f"http://{self.host}:{self.port}"
        print(f"Preview server running at {url}")
        print(f"Watching: {self.script_path}")
        print("Press Ctrl+C to stop")

        if self.open_browser:
            webbrowser.open(url)

        if blocking:
            try:
                while self._running:
                    time.sleep(0.5)
            except KeyboardInterrupt:
                print("\nShutting down...")
                self.stop()

    def _setup_watchdog(self) -> None:
        """Setup watchdog file observer."""
        if not WATCHDOG_AVAILABLE or Observer is None:
            return

        def on_change() -> None:
            # The loader will detect the change via polling
            pass

        handler = ScriptChangeHandler(self.loader, on_change)
        self._observer = Observer()
        self._observer.schedule(handler, str(self.script_path.parent), recursive=False)
        self._observer.start()

    def stop(self) -> None:
        """Stop the preview server."""
        self._running = False

        if self._observer is not None:
            self._observer.stop()
            self._observer.join(timeout=1)
            self._observer = None

        if self._server is not None:
            self._server.shutdown()
            self._server = None


def serve(
    script_path: str | Path,
    port: int = 8000,
    host: str = "localhost",
    open_browser: bool = True,
) -> PreviewServer:
    """Start a live preview server for a comic script.

    This is a convenience function that creates and starts a PreviewServer.

    Args:
        script_path: Path to the comic script file.
        port: Port to run the server on (default: 8000).
        host: Host to bind to (default: localhost).
        open_browser: Whether to open the browser automatically (default: True).

    Returns:
        The PreviewServer instance.

    Example:
        >>> serve("my_comic.py")  # Opens browser with live preview
        Preview server running at http://localhost:8000
        Watching: /path/to/my_comic.py
        Press Ctrl+C to stop
    """
    server = PreviewServer(script_path, port, host, open_browser)
    server.start(blocking=True)
    return server
