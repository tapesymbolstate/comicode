"""Preview Server for live development workflow.

The Preview Server provides hot-reload capability for comic development.
When you modify your script, the browser automatically refreshes to show
your changes - no manual re-rendering needed!

This example demonstrates:
- How to use the preview server via CLI
- How to use PreviewServer programmatically
- Creating a preview-friendly comic script

## Usage Methods

### Method 1: CLI Command (Recommended)

The easiest way to use the preview server is via the `comix serve` command:

    uv run comix serve examples/23_preview_server.py

This will:
1. Start a local web server (default port 8000)
2. Open your default browser to view the comic
3. Watch the file for changes
4. Auto-refresh when you save the file

Options:
    --port / -p    : Specify port (default: 8000)
    --no-browser   : Don't auto-open browser

### Method 2: CLI One-shot Preview

For a quick preview without hot-reload:

    uv run comix preview examples/23_preview_server.py

This renders once and opens in browser.

### Method 3: Python API

You can also start the server programmatically:

    from comix.preview.server import PreviewServer

    server = PreviewServer("my_comic.py", port=8080)
    server.start()  # Blocks until Ctrl+C

## Creating Preview-Friendly Scripts

For the preview server to work, your script must:
1. Define a Page instance at module level, OR
2. Define a Page subclass that gets instantiated

The script below demonstrates a preview-friendly comic.
"""
# Status: ✅ Working (v0.1.108)

from comix import Page, Panel, Stickman


def create_preview_demo() -> Page:
    """Create a demo page for preview server.

    This function demonstrates the structure of a preview-friendly script.
    The page returned will be rendered when the preview server loads this file.
    """
    page = Page(width=600, height=500, background_color="#FAFAFA")
    page.set_layout(rows=2, cols=2)

    # Panel 1: Introduction
    panel1 = Panel()
    char1 = Stickman(height=70, color="#1976D2")
    char1.move_to((150, 130))
    char1.set_expression("happy")
    bubble1 = char1.say("Welcome to\nthe Preview!")
    panel1.add_content(char1, bubble1)

    # Panel 2: Explanation
    panel2 = Panel()
    char2 = Stickman(height=70, color="#E91E63")
    char2.move_to((150, 130))
    char2.set_expression("excited")
    bubble2 = char2.say("Edit this file\nand save!")
    panel2.add_content(char2, bubble2)

    # Panel 3: Hot reload
    panel3 = Panel()
    char3 = Stickman(height=70, color="#4CAF50")
    char3.move_to((150, 130))
    char3.set_expression("surprised")
    bubble3 = char3.say("Browser updates\nautomatically!")
    panel3.add_content(char3, bubble3)

    # Panel 4: Call to action
    panel4 = Panel()
    char4 = Stickman(height=70, color="#FF9800")
    char4.move_to((150, 130))
    char4.set_expression("happy")
    char4.set_pose("cheering")
    bubble4 = char4.say("Try it now!")
    panel4.add_content(char4, bubble4)

    page.add(panel1, panel2, panel3, panel4)
    page.auto_layout()

    return page


# Module-level Page instance - required for preview server to find it
page = create_preview_demo()


def print_usage_guide() -> None:
    """Print usage guide for the preview server."""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                    PREVIEW SERVER USAGE GUIDE                     ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  1. Start the preview server:                                     ║
║                                                                   ║
║     uv run comix serve examples/23_preview_server.py              ║
║                                                                   ║
║  2. The browser will open automatically                           ║
║                                                                   ║
║  3. Edit this file and save - the browser refreshes!              ║
║                                                                   ║
║  4. Press Ctrl+C in the terminal to stop the server               ║
║                                                                   ║
╠══════════════════════════════════════════════════════════════════╣
║  CLI OPTIONS:                                                     ║
║                                                                   ║
║    --port 8080      Use a specific port                           ║
║    --no-browser     Don't auto-open browser                       ║
║                                                                   ║
╠══════════════════════════════════════════════════════════════════╣
║  ONE-SHOT PREVIEW (no hot-reload):                                ║
║                                                                   ║
║    uv run comix preview examples/23_preview_server.py             ║
║                                                                   ║
╚══════════════════════════════════════════════════════════════════╝
""")


if __name__ == "__main__":
    # When run directly, just save a static render and print usage guide
    page.render("examples/output/23_preview_demo.png")
    print("Created examples/output/23_preview_demo.png")
    print_usage_guide()
