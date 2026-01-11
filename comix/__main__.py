"""CLI entry point for Comix."""

import click


@click.group()
@click.version_option(version="0.1.0", prog_name="comix")
def main() -> None:
    """Comix - Code-based comic creation framework."""
    pass


@main.command()
@click.argument("script", type=click.Path(exists=True))
@click.option("-o", "--output", default="output.svg", help="Output file path (default: output.svg)")
@click.option(
    "-f",
    "--format",
    type=click.Choice(["svg", "png", "pdf"]),
    default="svg",
    help="Output format (default: svg)",
)
@click.option(
    "-q",
    "--quality",
    type=click.Choice(["low", "medium", "high"]),
    default="medium",
    help="Render quality: low=72dpi, medium=150dpi, high=300dpi (default: medium)",
)
def render(script: str, output: str, format: str, quality: str) -> None:
    """Render a comic script to an output file."""
    import importlib.util
    from pathlib import Path

    script_path = Path(script)
    spec = importlib.util.spec_from_file_location("comic_script", script_path)
    if spec is None or spec.loader is None:
        click.echo(f"Error: Could not load script {script}", err=True)
        raise SystemExit(1)

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    from comix.page.page import Page

    page = None
    for name in dir(module):
        obj = getattr(module, name)
        if isinstance(obj, type) and issubclass(obj, Page) and obj is not Page:
            page = obj()
            break

    if page is None:
        for name in dir(module):
            obj = getattr(module, name)
            if isinstance(obj, Page):
                page = obj
                break

    if page is None:
        click.echo("Error: No Page class or instance found in script", err=True)
        raise SystemExit(1)

    output_path = page.render(output, format=format, quality=quality)
    click.echo(f"Rendered to: {output_path}")


@main.command()
@click.argument("script", type=click.Path(exists=True))
def preview(script: str) -> None:
    """Preview a comic script in the browser."""
    import importlib.util
    from pathlib import Path

    script_path = Path(script)
    spec = importlib.util.spec_from_file_location("comic_script", script_path)
    if spec is None or spec.loader is None:
        click.echo(f"Error: Could not load script {script}", err=True)
        raise SystemExit(1)

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    from comix.page.page import Page

    page = None
    for name in dir(module):
        obj = getattr(module, name)
        if isinstance(obj, type) and issubclass(obj, Page) and obj is not Page:
            page = obj()
            break

    if page is None:
        for name in dir(module):
            obj = getattr(module, name)
            if isinstance(obj, Page):
                page = obj
                break

    if page is None:
        click.echo("Error: No Page class or instance found in script", err=True)
        raise SystemExit(1)

    page.show()


@main.command()
@click.argument("script", type=click.Path(exists=True))
@click.option("-p", "--port", default=8000, help="Port to run the server on (default: 8000)")
@click.option("-H", "--host", default="localhost", help="Host to bind to (default: localhost)")
@click.option("--no-browser", is_flag=True, help="Don't open browser automatically")
def serve(script: str, port: int, host: str, no_browser: bool) -> None:
    """Start a live preview server with hot reload.

    Watches the script file for changes and automatically refreshes
    the browser preview.

    Requires: uv sync --extra web
    """
    try:
        from comix.preview import serve as start_server
    except ImportError:
        click.echo(
            "Error: Web preview requires watchdog. Install with: uv sync --extra web",
            err=True,
        )
        raise SystemExit(1)

    try:
        start_server(script, port=port, host=host, open_browser=not no_browser)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@main.command()
def info() -> None:
    """Display information about Comix."""
    click.echo("Comix - Code-based comic creation framework")
    click.echo("Version: 0.1.0")
    click.echo("")
    click.echo("Inspired by Manim's architecture for creating comics programmatically.")
    click.echo("")
    click.echo("Core components:")
    click.echo("  - CObject: Base class for all visual elements")
    click.echo("  - Panel: Comic panel container")
    click.echo("  - Bubble: Speech bubbles (Speech, Thought, Shout, Whisper, Narrator)")
    click.echo("  - Character: Character types (Stickman, SimpleFace)")
    click.echo("  - Page: Main composition class")
    click.echo("")
    click.echo("Usage:")
    click.echo("  comix render script.py -o output.svg")
    click.echo("  comix preview script.py")
    click.echo("  comix serve script.py    # Live preview with hot reload")


if __name__ == "__main__":
    main()
