"""HTML Renderer - renders comic pages to interactive HTML format."""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import TYPE_CHECKING

from comix.renderer.svg_renderer import SVGRenderer

if TYPE_CHECKING:
    from comix.page.book import Book
    from comix.page.page import Page


class HTMLRenderer:
    """Renders a Page or Book to interactive HTML format.

    Features:
    - Embedded SVG for crisp scaling
    - Zoom controls (mouse wheel, buttons)
    - Pan with mouse drag
    - Hover effects on panels
    - Keyboard navigation
    - Dark/light theme toggle
    - Fullscreen mode
    - Multi-page navigation for books
    """

    def __init__(
        self,
        page: Page | None = None,
        *,
        title: str = "Comic",
        theme: str = "light",
        enable_zoom: bool = True,
        enable_pan: bool = True,
        enable_hover: bool = True,
        enable_fullscreen: bool = True,
        min_zoom: float = 0.5,
        max_zoom: float = 4.0,
    ) -> None:
        """Initialize HTML renderer.

        Args:
            page: The page to render (can also use render_book for multiple pages).
            title: HTML document title.
            theme: Initial theme ("light" or "dark").
            enable_zoom: Enable zoom functionality.
            enable_pan: Enable pan functionality.
            enable_hover: Enable hover effects on panels.
            enable_fullscreen: Enable fullscreen mode.
            min_zoom: Minimum zoom level.
            max_zoom: Maximum zoom level.
        """
        self.page = page
        self.title = title
        self.theme = theme
        self.enable_zoom = enable_zoom
        self.enable_pan = enable_pan
        self.enable_hover = enable_hover
        self.enable_fullscreen = enable_fullscreen
        self.min_zoom = min_zoom
        self.max_zoom = max_zoom

    def render(self, output_path: str) -> str:
        """Render single page to HTML file.

        Args:
            output_path: Path to save the HTML file.

        Returns:
            Path to the rendered file.
        """
        if self.page is None:
            raise ValueError("No page to render. Set page in constructor or use render_book().")

        svg_content = self._get_svg_content(self.page)
        html_content = self._generate_html([svg_content])

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path).write_text(html_content, encoding="utf-8")

        return output_path

    def render_to_string(self) -> str:
        """Render single page to HTML string.

        Returns:
            The HTML content as a string.
        """
        if self.page is None:
            raise ValueError("No page to render. Set page in constructor or use render_book().")

        svg_content = self._get_svg_content(self.page)
        return self._generate_html([svg_content])

    def render_book(self, book: Book, output_path: str) -> str:
        """Render multiple pages (book) to HTML with navigation.

        Args:
            book: The Book object containing pages.
            output_path: Path to save the HTML file.

        Returns:
            Path to the rendered file.
        """
        svg_contents = []
        for page in book.pages:
            svg_contents.append(self._get_svg_content(page))

        html_content = self._generate_html(svg_contents, is_book=True, book_title=book.title)

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path).write_text(html_content, encoding="utf-8")

        return output_path

    def _get_svg_content(self, page: Page) -> str:
        """Get SVG content for a page."""
        page.build()
        page.auto_layout()
        svg_renderer = SVGRenderer(page)
        return svg_renderer.render_to_string()

    def _generate_html(
        self,
        svg_contents: list[str],
        *,
        is_book: bool = False,
        book_title: str | None = None,
    ) -> str:
        """Generate the complete HTML document.

        Args:
            svg_contents: List of SVG strings (one per page).
            is_book: Whether this is a multi-page book.
            book_title: Title for book mode.

        Returns:
            Complete HTML document as string.
        """
        title = book_title or self.title
        escaped_title = html.escape(title)

        svg_data_json = json.dumps(svg_contents)

        config = {
            "enableZoom": self.enable_zoom,
            "enablePan": self.enable_pan,
            "enableHover": self.enable_hover,
            "enableFullscreen": self.enable_fullscreen,
            "minZoom": self.min_zoom,
            "maxZoom": self.max_zoom,
            "theme": self.theme,
            "isBook": is_book,
            "pageCount": len(svg_contents),
        }
        config_json = json.dumps(config)

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escaped_title}</title>
    <meta name="generator" content="Comix - Python Comic Creation Library">
    <style>
{self._get_css()}
    </style>
</head>
<body class="theme-{self.theme}">
    <div class="comic-viewer" id="viewer">
        <header class="toolbar">
            <div class="toolbar-left">
                <span class="title">{escaped_title}</span>
                {self._get_page_indicator_html(is_book)}
            </div>
            <div class="toolbar-right">
                {self._get_zoom_controls_html()}
                {self._get_theme_toggle_html()}
                {self._get_fullscreen_button_html()}
            </div>
        </header>

        <main class="canvas-container" id="canvasContainer">
            <div class="canvas" id="canvas">
                <div class="svg-container" id="svgContainer">
                    <!-- SVG will be inserted here -->
                </div>
            </div>
        </main>

        {self._get_navigation_html(is_book)}

        <footer class="status-bar">
            <span id="zoomLevel">100%</span>
            <span class="separator">|</span>
            <span id="instructions">Scroll to zoom • Drag to pan • Double-click to reset</span>
        </footer>
    </div>

    <script>
        const svgPages = {svg_data_json};
        const config = {config_json};
{self._get_javascript()}
    </script>
</body>
</html>"""

    def _get_css(self) -> str:
        """Get CSS styles for the HTML document."""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --bg-primary: #ffffff;
            --bg-secondary: #f5f5f5;
            --bg-tertiary: #e5e5e5;
            --text-primary: #1a1a1a;
            --text-secondary: #666666;
            --accent: #3b82f6;
            --accent-hover: #2563eb;
            --border: #d4d4d4;
            --shadow: rgba(0, 0, 0, 0.1);
        }

        .theme-dark {
            --bg-primary: #1a1a1a;
            --bg-secondary: #2d2d2d;
            --bg-tertiary: #404040;
            --text-primary: #ffffff;
            --text-secondary: #a0a0a0;
            --accent: #60a5fa;
            --accent-hover: #93c5fd;
            --border: #404040;
            --shadow: rgba(0, 0, 0, 0.3);
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: var(--bg-secondary);
            color: var(--text-primary);
            overflow: hidden;
            height: 100vh;
            width: 100vw;
        }

        .comic-viewer {
            display: flex;
            flex-direction: column;
            height: 100vh;
            width: 100vw;
        }

        .toolbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 16px;
            background: var(--bg-primary);
            border-bottom: 1px solid var(--border);
            z-index: 100;
            flex-shrink: 0;
        }

        .toolbar-left, .toolbar-right {
            display: flex;
            align-items: center;
            gap: 16px;
        }

        .title {
            font-weight: 600;
            font-size: 16px;
        }

        .page-indicator {
            font-size: 14px;
            color: var(--text-secondary);
        }

        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 6px 12px;
            border: 1px solid var(--border);
            border-radius: 6px;
            background: var(--bg-primary);
            color: var(--text-primary);
            font-size: 14px;
            cursor: pointer;
            transition: all 0.15s ease;
            min-width: 36px;
            height: 36px;
        }

        .btn:hover {
            background: var(--bg-tertiary);
            border-color: var(--accent);
        }

        .btn:active {
            transform: scale(0.95);
        }

        .btn-icon {
            padding: 6px;
        }

        .btn-group {
            display: flex;
            gap: 4px;
        }

        .zoom-display {
            min-width: 60px;
            text-align: center;
            font-variant-numeric: tabular-nums;
        }

        .canvas-container {
            flex: 1;
            overflow: hidden;
            position: relative;
            background: var(--bg-tertiary);
            cursor: grab;
        }

        .canvas-container:active {
            cursor: grabbing;
        }

        .canvas {
            position: absolute;
            transform-origin: 0 0;
            transition: none;
        }

        .canvas.animating {
            transition: transform 0.3s ease-out;
        }

        .svg-container {
            background: white;
            box-shadow: 0 4px 20px var(--shadow);
            border-radius: 4px;
            overflow: hidden;
        }

        .svg-container svg {
            display: block;
        }

        /* Hover effects for panels */
        .svg-container.hover-enabled svg g[data-panel] {
            transition: filter 0.2s ease, transform 0.2s ease;
            transform-origin: center;
        }

        .svg-container.hover-enabled svg g[data-panel]:hover {
            filter: brightness(1.02);
            cursor: pointer;
        }

        .navigation {
            position: fixed;
            bottom: 50%;
            transform: translateY(50%);
            z-index: 50;
        }

        .navigation.prev {
            left: 16px;
        }

        .navigation.next {
            right: 16px;
        }

        .nav-btn {
            width: 48px;
            height: 48px;
            border-radius: 50%;
            background: var(--bg-primary);
            border: 1px solid var(--border);
            color: var(--text-primary);
            font-size: 20px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 2px 8px var(--shadow);
            transition: all 0.15s ease;
        }

        .nav-btn:hover {
            background: var(--accent);
            color: white;
            border-color: var(--accent);
        }

        .nav-btn:disabled {
            opacity: 0.3;
            cursor: not-allowed;
        }

        .nav-btn:disabled:hover {
            background: var(--bg-primary);
            color: var(--text-primary);
            border-color: var(--border);
        }

        .status-bar {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 6px 16px;
            background: var(--bg-primary);
            border-top: 1px solid var(--border);
            font-size: 12px;
            color: var(--text-secondary);
            flex-shrink: 0;
        }

        .separator {
            color: var(--border);
        }

        /* Fullscreen mode */
        .comic-viewer:fullscreen {
            background: var(--bg-secondary);
        }

        .comic-viewer:fullscreen .toolbar {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            opacity: 0;
            transition: opacity 0.3s ease;
        }

        .comic-viewer:fullscreen:hover .toolbar {
            opacity: 1;
        }

        .comic-viewer:fullscreen .status-bar {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            opacity: 0;
            transition: opacity 0.3s ease;
        }

        .comic-viewer:fullscreen:hover .status-bar {
            opacity: 1;
        }

        /* Hide elements based on config */
        .hidden {
            display: none !important;
        }

        /* Responsive adjustments */
        @media (max-width: 768px) {
            .toolbar {
                padding: 8px 12px;
            }

            .toolbar-left, .toolbar-right {
                gap: 8px;
            }

            .title {
                font-size: 14px;
            }

            .btn {
                min-width: 32px;
                height: 32px;
                padding: 4px 8px;
            }

            .nav-btn {
                width: 40px;
                height: 40px;
            }

            .navigation.prev {
                left: 8px;
            }

            .navigation.next {
                right: 8px;
            }
        }
"""

    def _get_zoom_controls_html(self) -> str:
        """Get HTML for zoom controls."""
        if not self.enable_zoom:
            return ""
        return """
                <div class="btn-group zoom-controls">
                    <button class="btn btn-icon" id="zoomOut" title="Zoom out (-)">−</button>
                    <span class="btn zoom-display" id="zoomDisplay">100%</span>
                    <button class="btn btn-icon" id="zoomIn" title="Zoom in (+)">+</button>
                    <button class="btn" id="zoomFit" title="Fit to screen (0)">Fit</button>
                </div>"""

    def _get_theme_toggle_html(self) -> str:
        """Get HTML for theme toggle button."""
        return """
                <button class="btn btn-icon" id="themeToggle" title="Toggle theme (T)">
                    <span id="themeIcon">☀️</span>
                </button>"""

    def _get_fullscreen_button_html(self) -> str:
        """Get HTML for fullscreen button."""
        if not self.enable_fullscreen:
            return ""
        return """
                <button class="btn btn-icon" id="fullscreenBtn" title="Fullscreen (F)">⛶</button>"""

    def _get_page_indicator_html(self, is_book: bool) -> str:
        """Get HTML for page indicator."""
        if not is_book:
            return ""
        return """
                <span class="page-indicator">
                    Page <span id="currentPage">1</span> of <span id="totalPages">1</span>
                </span>"""

    def _get_navigation_html(self, is_book: bool) -> str:
        """Get HTML for page navigation."""
        if not is_book:
            return ""
        return """
        <div class="navigation prev">
            <button class="nav-btn" id="prevPage" title="Previous page (←)">‹</button>
        </div>
        <div class="navigation next">
            <button class="nav-btn" id="nextPage" title="Next page (→)">›</button>
        </div>"""

    def _get_javascript(self) -> str:
        """Get JavaScript code for interactivity."""
        return """
        // State
        let currentPage = 0;
        let zoom = 1;
        let panX = 0;
        let panY = 0;
        let isPanning = false;
        let startX = 0;
        let startY = 0;
        let startPanX = 0;
        let startPanY = 0;

        // Elements
        const viewer = document.getElementById('viewer');
        const container = document.getElementById('canvasContainer');
        const canvas = document.getElementById('canvas');
        const svgContainer = document.getElementById('svgContainer');
        const zoomDisplay = document.getElementById('zoomDisplay');
        const zoomLevel = document.getElementById('zoomLevel');

        // Initialize
        function init() {
            loadPage(0);
            updateZoomDisplay();
            centerCanvas();
            setupEventListeners();
            updateThemeIcon();

            if (config.enableHover) {
                svgContainer.classList.add('hover-enabled');
            }

            // Update page count
            const totalPagesEl = document.getElementById('totalPages');
            if (totalPagesEl) {
                totalPagesEl.textContent = config.pageCount;
            }
        }

        function loadPage(index) {
            if (index < 0 || index >= svgPages.length) return;
            currentPage = index;
            svgContainer.innerHTML = svgPages[index];

            // Update page indicator
            const currentPageEl = document.getElementById('currentPage');
            if (currentPageEl) {
                currentPageEl.textContent = index + 1;
            }

            // Update nav buttons
            const prevBtn = document.getElementById('prevPage');
            const nextBtn = document.getElementById('nextPage');
            if (prevBtn) prevBtn.disabled = index === 0;
            if (nextBtn) nextBtn.disabled = index === svgPages.length - 1;

            // Add data attributes to panels for hover effects
            const panels = svgContainer.querySelectorAll('g');
            panels.forEach((g, i) => {
                if (g.querySelector('rect')) {
                    g.setAttribute('data-panel', i);
                }
            });

            centerCanvas();
        }

        function updateZoomDisplay() {
            const percent = Math.round(zoom * 100) + '%';
            if (zoomDisplay) zoomDisplay.textContent = percent;
            if (zoomLevel) zoomLevel.textContent = percent;
        }

        function setZoom(newZoom, centerX, centerY) {
            if (!config.enableZoom) return;

            const oldZoom = zoom;
            zoom = Math.max(config.minZoom, Math.min(config.maxZoom, newZoom));

            if (centerX !== undefined && centerY !== undefined) {
                // Zoom toward cursor position
                const rect = container.getBoundingClientRect();
                const mouseX = centerX - rect.left;
                const mouseY = centerY - rect.top;

                panX = mouseX - (mouseX - panX) * (zoom / oldZoom);
                panY = mouseY - (mouseY - panY) * (zoom / oldZoom);
            }

            updateTransform();
            updateZoomDisplay();
        }

        function updateTransform() {
            canvas.style.transform = `translate(${panX}px, ${panY}px) scale(${zoom})`;
        }

        function centerCanvas() {
            const containerRect = container.getBoundingClientRect();
            const svg = svgContainer.querySelector('svg');
            if (!svg) return;

            const svgWidth = parseFloat(svg.getAttribute('width') || svg.viewBox?.baseVal?.width || 800);
            const svgHeight = parseFloat(svg.getAttribute('height') || svg.viewBox?.baseVal?.height || 600);

            // Calculate zoom to fit
            const fitZoom = Math.min(
                (containerRect.width - 40) / svgWidth,
                (containerRect.height - 40) / svgHeight,
                1
            );

            zoom = fitZoom;
            panX = (containerRect.width - svgWidth * zoom) / 2;
            panY = (containerRect.height - svgHeight * zoom) / 2;

            canvas.classList.add('animating');
            updateTransform();
            updateZoomDisplay();

            setTimeout(() => canvas.classList.remove('animating'), 300);
        }

        function setupEventListeners() {
            // Zoom controls
            const zoomInBtn = document.getElementById('zoomIn');
            const zoomOutBtn = document.getElementById('zoomOut');
            const zoomFitBtn = document.getElementById('zoomFit');

            if (zoomInBtn) zoomInBtn.addEventListener('click', () => setZoom(zoom * 1.25));
            if (zoomOutBtn) zoomOutBtn.addEventListener('click', () => setZoom(zoom / 1.25));
            if (zoomFitBtn) zoomFitBtn.addEventListener('click', centerCanvas);

            // Mouse wheel zoom
            if (config.enableZoom) {
                container.addEventListener('wheel', (e) => {
                    e.preventDefault();
                    const delta = e.deltaY > 0 ? 0.9 : 1.1;
                    setZoom(zoom * delta, e.clientX, e.clientY);
                }, { passive: false });
            }

            // Pan
            if (config.enablePan) {
                container.addEventListener('mousedown', (e) => {
                    if (e.button !== 0) return;
                    isPanning = true;
                    startX = e.clientX;
                    startY = e.clientY;
                    startPanX = panX;
                    startPanY = panY;
                    container.style.cursor = 'grabbing';
                });

                document.addEventListener('mousemove', (e) => {
                    if (!isPanning) return;
                    panX = startPanX + (e.clientX - startX);
                    panY = startPanY + (e.clientY - startY);
                    updateTransform();
                });

                document.addEventListener('mouseup', () => {
                    isPanning = false;
                    container.style.cursor = 'grab';
                });
            }

            // Double-click to reset
            container.addEventListener('dblclick', centerCanvas);

            // Theme toggle
            const themeToggle = document.getElementById('themeToggle');
            if (themeToggle) {
                themeToggle.addEventListener('click', toggleTheme);
            }

            // Fullscreen
            const fullscreenBtn = document.getElementById('fullscreenBtn');
            if (fullscreenBtn && config.enableFullscreen) {
                fullscreenBtn.addEventListener('click', toggleFullscreen);
            }

            // Page navigation
            const prevBtn = document.getElementById('prevPage');
            const nextBtn = document.getElementById('nextPage');
            if (prevBtn) prevBtn.addEventListener('click', () => loadPage(currentPage - 1));
            if (nextBtn) nextBtn.addEventListener('click', () => loadPage(currentPage + 1));

            // Keyboard shortcuts
            document.addEventListener('keydown', (e) => {
                if (e.target.tagName === 'INPUT') return;

                switch (e.key) {
                    case '+':
                    case '=':
                        if (config.enableZoom) setZoom(zoom * 1.25);
                        break;
                    case '-':
                        if (config.enableZoom) setZoom(zoom / 1.25);
                        break;
                    case '0':
                        centerCanvas();
                        break;
                    case 'f':
                    case 'F':
                        if (config.enableFullscreen) toggleFullscreen();
                        break;
                    case 't':
                    case 'T':
                        toggleTheme();
                        break;
                    case 'ArrowLeft':
                        if (config.isBook) loadPage(currentPage - 1);
                        break;
                    case 'ArrowRight':
                        if (config.isBook) loadPage(currentPage + 1);
                        break;
                    case 'Home':
                        if (config.isBook) loadPage(0);
                        break;
                    case 'End':
                        if (config.isBook) loadPage(svgPages.length - 1);
                        break;
                }
            });

            // Window resize
            window.addEventListener('resize', () => {
                centerCanvas();
            });

            // Touch support for mobile
            let touchStartX = 0;
            let touchStartY = 0;
            let touchStartPanX = 0;
            let touchStartPanY = 0;
            let lastTouchDistance = 0;

            container.addEventListener('touchstart', (e) => {
                if (e.touches.length === 1) {
                    touchStartX = e.touches[0].clientX;
                    touchStartY = e.touches[0].clientY;
                    touchStartPanX = panX;
                    touchStartPanY = panY;
                } else if (e.touches.length === 2) {
                    lastTouchDistance = Math.hypot(
                        e.touches[0].clientX - e.touches[1].clientX,
                        e.touches[0].clientY - e.touches[1].clientY
                    );
                }
            }, { passive: true });

            container.addEventListener('touchmove', (e) => {
                if (e.touches.length === 1 && config.enablePan) {
                    panX = touchStartPanX + (e.touches[0].clientX - touchStartX);
                    panY = touchStartPanY + (e.touches[0].clientY - touchStartY);
                    updateTransform();
                } else if (e.touches.length === 2 && config.enableZoom) {
                    const distance = Math.hypot(
                        e.touches[0].clientX - e.touches[1].clientX,
                        e.touches[0].clientY - e.touches[1].clientY
                    );
                    const delta = distance / lastTouchDistance;
                    lastTouchDistance = distance;

                    const centerX = (e.touches[0].clientX + e.touches[1].clientX) / 2;
                    const centerY = (e.touches[0].clientY + e.touches[1].clientY) / 2;
                    setZoom(zoom * delta, centerX, centerY);
                }
            }, { passive: true });
        }

        function toggleTheme() {
            const body = document.body;
            const isDark = body.classList.contains('theme-dark');
            body.classList.remove('theme-dark', 'theme-light');
            body.classList.add(isDark ? 'theme-light' : 'theme-dark');
            updateThemeIcon();
        }

        function updateThemeIcon() {
            const icon = document.getElementById('themeIcon');
            if (icon) {
                const isDark = document.body.classList.contains('theme-dark');
                icon.textContent = isDark ? '🌙' : '☀️';
            }
        }

        function toggleFullscreen() {
            if (!document.fullscreenElement) {
                viewer.requestFullscreen().catch(() => {});
            } else {
                document.exitFullscreen().catch(() => {});
            }
        }

        // Start
        init();
"""
