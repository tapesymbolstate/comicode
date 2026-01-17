"""Cairo Renderer - renders comic pages to PNG/PDF format."""

from __future__ import annotations

import math
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal, Sequence

try:
    import cairo
except ImportError:
    cairo = None  # type: ignore[assignment]

if TYPE_CHECKING:
    from comix.effect.effect import Effect
    from comix.page.page import Page


class CairoRenderer:
    """Renders a Page to PNG or PDF format using Cairo.

    Requires optional 'cairo' dependencies:
        uv sync --extra cairo
    """

    # DPI settings for quality levels
    DPI_LOW = 72
    DPI_MEDIUM = 150
    DPI_HIGH = 300

    def __init__(self, page: Page) -> None:
        if cairo is None:
            raise ImportError(
                "Cairo is not installed. Install with: uv sync --extra cairo"
            )
        self.page = page
        self._surface: cairo.Surface | None = None
        self._ctx: cairo.Context | None = None  # type: ignore[type-arg]
        self._dpi: int = self.DPI_MEDIUM

    def render(
        self,
        output_path: str,
        format: str | None = None,
        quality: Literal["low", "medium", "high"] = "medium",
    ) -> str:
        """Render the page to a PNG or PDF file.

        Args:
            output_path: Path to save the output file.
            format: Output format ("png" or "pdf"). Auto-detected from path if None.
            quality: Rendering quality ("low", "medium", "high").

        Returns:
            Path to the rendered file.
        """
        if format is None:
            format = Path(output_path).suffix.lstrip(".") or "png"

        # Set DPI based on quality
        if quality == "low":
            self._dpi = self.DPI_LOW
        elif quality == "high":
            self._dpi = self.DPI_HIGH
        else:
            self._dpi = self.DPI_MEDIUM

        # Create output directory if needed
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        if format == "pdf":
            return self._render_pdf(output_path)
        else:
            return self._render_png(output_path)

    def _render_pdf(self, output_path: str) -> str:
        """Render to PDF format."""
        # PDF uses points (72 per inch), so use page dimensions directly
        self._surface = cairo.PDFSurface(
            output_path, self.page.width, self.page.height
        )
        self._ctx = cairo.Context(self._surface)

        self._draw_page()

        self._surface.finish()
        return output_path

    def render_book(
        self,
        pages: Sequence[Page],
        output_path: str,
        quality: Literal["low", "medium", "high"] = "medium",
    ) -> str:
        """Render multiple pages to a single multi-page PDF.

        Args:
            pages: Sequence of Page objects to render.
            output_path: Path to save the PDF file.
            quality: Rendering quality (affects any rasterized content).

        Returns:
            Path to the rendered PDF file.

        Raises:
            ValueError: If pages is empty.
        """
        if not pages:
            raise ValueError("Cannot render an empty book. Provide at least one page.")

        # Set DPI based on quality (for any rasterized content like images)
        if quality == "low":
            self._dpi = self.DPI_LOW
        elif quality == "high":
            self._dpi = self.DPI_HIGH
        else:
            self._dpi = self.DPI_MEDIUM

        # Create output directory if needed
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        # Use the first page's dimensions for the PDF surface
        # Cairo PDFSurface allows different page sizes via set_size() per page
        first_page = pages[0]
        self._surface = cairo.PDFSurface(
            output_path, first_page.width, first_page.height
        )
        self._ctx = cairo.Context(self._surface)

        # Render each page
        for i, page in enumerate(pages):
            # Update the current page reference
            self.page = page

            # Set the page size for this page (allows different sizes per page)
            assert self._surface is not None
            self._surface.set_size(page.width, page.height)

            # Draw the page content
            self._draw_page()

            # Show the page (creates a new page in the PDF)
            # Don't show_page after the last page
            if i < len(pages) - 1:
                assert self._ctx is not None
                self._ctx.show_page()

        # Finalize the PDF
        self._surface.finish()
        return output_path

    def _render_png(self, output_path: str) -> str:
        """Render to PNG format."""
        # Scale dimensions based on DPI
        scale = self._dpi / 72.0
        width = int(self.page.width * scale)
        height = int(self.page.height * scale)

        self._surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        self._ctx = cairo.Context(self._surface)

        # Scale context to match DPI
        self._ctx.scale(scale, scale)

        self._draw_page()

        self._surface.write_to_png(output_path)
        return output_path

    def _draw_page(self) -> None:
        """Draw the entire page content."""
        ctx = self._ctx
        assert ctx is not None

        # Draw background
        self._set_color(self.page.background_color)
        ctx.rectangle(0, 0, self.page.width, self.page.height)
        ctx.fill()

        # Render effects with negative z_index (behind objects)
        background_effects = sorted(
            [e for e in self.page._effects if e.z_index < 0],
            key=lambda e: e.z_index,
        )
        for effect in background_effects:
            self._render_effect(effect)

        # Sort objects by z-index
        sorted_objects = sorted(self.page._cobjects, key=lambda obj: obj.z_index)

        # Render each object
        for cobject in sorted_objects:
            self._render_cobject(cobject)

        # Render effects with positive z_index (in front of objects)
        foreground_effects = sorted(
            [e for e in self.page._effects if e.z_index >= 0],
            key=lambda e: e.z_index,
        )
        for effect in foreground_effects:
            self._render_effect(effect)

    def _render_cobject(self, cobject: Any) -> None:
        """Render a CObject and its children."""
        ctx = self._ctx
        assert ctx is not None

        data = cobject.get_render_data()
        obj_type = data.get("type", "")
        opacity = data.get("opacity", 1.0)

        ctx.save()

        # Apply global opacity via push_group/pop_group for full alpha support
        if opacity < 1.0:
            ctx.push_group()

        if obj_type == "Panel":
            self._render_panel(data)
        elif obj_type in (
            "Bubble",
            "SpeechBubble",
            "ThoughtBubble",
            "ShoutBubble",
            "WhisperBubble",
            "NarratorBubble",
        ):
            self._render_bubble(data)
        elif obj_type in ("Text", "StyledText", "SFX"):
            self._render_text(data)
        elif obj_type in ("Stickman", "SimpleFace", "Character"):
            self._render_character(data)
        elif obj_type == "Rectangle":
            self._render_rectangle(data)
        elif obj_type == "Circle":
            self._render_circle(data)
        elif obj_type == "Line":
            self._render_line(data)
        elif obj_type in ("Image", "AIImage"):
            self._render_image(data)
        else:
            self._render_generic(data)

        # Render children
        for child in cobject.submobjects:
            self._render_cobject(child)

        if opacity < 1.0:
            ctx.pop_group_to_source()
            ctx.paint_with_alpha(opacity)

        ctx.restore()

    def _render_panel(self, data: dict[str, Any]) -> None:
        """Render a panel."""
        ctx = self._ctx
        assert ctx is not None

        pos = data.get("position", [0, 0])
        width = data.get("width", 100)
        height = data.get("height", 100)
        border = data.get("border", {})

        x = pos[0] - width / 2
        y = pos[1] - height / 2
        radius = border.get("radius", 0)

        # Draw rounded rectangle path
        self._rounded_rect_path(x, y, width, height, radius)

        # Fill background color
        self._set_color(data.get("background_color", "#FFFFFF"))
        ctx.fill_preserve()

        # Render background image if present
        background_image = data.get("background_image")
        if background_image:
            self._render_panel_background_image(
                background_image, x, y, width, height, radius
            )

        # Stroke border
        self._set_color(border.get("color", "#000000"))
        ctx.set_line_width(border.get("width", 2))
        self._set_dash_style(border.get("style", "solid"))
        ctx.stroke()

    def _render_panel_background_image(
        self,
        image_path: str,
        x: float,
        y: float,
        width: float,
        height: float,
        radius: float,
    ) -> None:
        """Render a background image for a panel.

        Args:
            image_path: Path to the image file.
            x: Left edge of the panel.
            y: Top edge of the panel.
            width: Panel width.
            height: Panel height.
            radius: Corner radius for clipping.
        """
        ctx = self._ctx
        assert ctx is not None

        from pathlib import Path

        path = Path(image_path)
        if not path.exists():
            return  # Skip if file doesn't exist

        try:
            from PIL import Image as PILImage
        except ImportError:
            return  # Pillow not available

        try:
            pil_image = PILImage.open(path)

            # Calculate scaling to cover the panel (similar to CSS background-size: cover)
            orig_w, orig_h = pil_image.size
            scale_w = width / orig_w
            scale_h = height / orig_h
            scale = max(scale_w, scale_h)  # Cover behavior

            new_w = int(orig_w * scale)
            new_h = int(orig_h * scale)

            # Center the image within the panel bounds
            offset_x = (width - new_w) / 2
            offset_y = (height - new_h) / 2

            # Resize image
            pil_image = pil_image.resize(  # type: ignore[assignment]
                (new_w, new_h), PILImage.Resampling.LANCZOS
            )

            # Convert to RGBA if needed
            if pil_image.mode != "RGBA":
                pil_image = pil_image.convert("RGBA")  # type: ignore[assignment]

            # Create Cairo surface from PIL image
            img_width, img_height = pil_image.size
            img_data = pil_image.tobytes("raw", "BGRa")

            surface = cairo.ImageSurface.create_for_data(
                bytearray(img_data),
                cairo.FORMAT_ARGB32,
                img_width,
                img_height,
            )

            # Save context and apply clip path for rounded corners
            ctx.save()

            # Create clip path using panel bounds
            self._rounded_rect_path(x, y, width, height, radius)
            ctx.clip()

            # Draw the image
            ctx.translate(x + offset_x, y + offset_y)
            ctx.set_source_surface(surface, 0, 0)
            ctx.paint()

            ctx.restore()

        except Exception:
            pass  # Silently skip on errors

    def _render_bubble(self, data: dict[str, Any]) -> None:
        """Render a speech bubble."""
        ctx = self._ctx
        assert ctx is not None

        pos = data.get("position", [0, 0])
        points = data.get("points", [])
        tail_points = data.get("tail_points", [])
        emphasis = data.get("emphasis", False)

        if not points:
            return

        # Translate points
        translated_points = [(p[0] + pos[0], p[1] + pos[1]) for p in points]

        border_width = data.get("border_width", 2)
        if emphasis:
            border_width = max(border_width * 1.5, border_width + 1)

        # Draw emphasis shadow
        if emphasis:
            shadow_offset = 3
            shadow_points = [
                (p[0] + shadow_offset, p[1] + shadow_offset)
                for p in translated_points
            ]
            self._polygon_path(shadow_points)
            self._set_color("#000000", 0.2)
            ctx.fill()

        # Draw bubble body
        self._polygon_path(translated_points)

        # Fill
        self._set_color(data.get("fill_color", "#FFFFFF"))
        ctx.fill_preserve()

        # Stroke
        self._set_color(data.get("border_color", "#000000"))
        ctx.set_line_width(border_width)
        self._set_dash_style(data.get("border_style", "solid"))
        ctx.stroke()

        # Draw tail
        if tail_points and len(tail_points) >= 3:
            translated_tail = [(p[0] + pos[0], p[1] + pos[1]) for p in tail_points]

            # Draw tail shadow if emphasis
            if emphasis:
                shadow_tail = [
                    (p[0] + shadow_offset, p[1] + shadow_offset)
                    for p in translated_tail
                ]
                self._polygon_path(shadow_tail)
                self._set_color("#000000", 0.2)
                ctx.fill()

            self._polygon_path(translated_tail)
            self._set_color(data.get("fill_color", "#FFFFFF"))
            ctx.fill_preserve()
            self._set_color(data.get("border_color", "#000000"))
            ctx.set_line_width(border_width)
            ctx.stroke()

        # Draw text
        text = data.get("text", "")
        if text:
            self._draw_text(
                text,
                pos[0],
                pos[1],
                font_family=data.get("font_family", "sans-serif"),
                font_size=data.get("font_size", 16),
                color=data.get("font_color", "#000000"),
                align="center",
            )

    def _render_text(self, data: dict[str, Any]) -> None:
        """Render text element."""
        ctx = self._ctx
        assert ctx is not None

        pos = data.get("position", [0, 0])
        text = data.get("text", "")

        if not text:
            return

        # Handle SFX with outline
        if data.get("sfx") and data.get("outline"):
            self._draw_text(
                text,
                pos[0],
                pos[1],
                font_family=data.get("font_family", "sans-serif"),
                font_size=data.get("font_size", 32),
                font_weight=data.get("font_weight", "bold"),
                color=None,  # No fill for outline
                stroke_color=data.get("outline_color", "#FFFFFF"),
                stroke_width=data.get("outline_width", 3),
                align="center",
            )

        # Draw main text
        self._draw_text(
            text,
            pos[0],
            pos[1],
            font_family=data.get("font_family", "sans-serif"),
            font_size=data.get("font_size", 16),
            font_weight=data.get("font_weight", "normal"),
            font_style=data.get("font_style", "normal"),
            color=data.get("color", "#000000"),
            align=data.get("align", "center"),
        )

    def _render_character(self, data: dict[str, Any]) -> None:
        """Render a character."""
        pos = data.get("position", [0, 0])
        style = data.get("style", "stickman")

        if style == "stickman":
            self._render_stickman(data, pos)
        elif style == "simple":
            self._render_simple_face(data, pos)
        else:
            self._render_generic(data)

    def _render_stickman(self, data: dict[str, Any], pos: list[float]) -> None:
        """Render a stickman character."""
        ctx = self._ctx
        assert ctx is not None

        points = data.get("points", [])
        color = data.get("color", "#000000")
        stroke_width = 2

        if len(points) < 2:
            return

        # Draw head (first 16 points form a circle-ish shape)
        head_points = points[:16]
        if head_points:
            translated_head = [(p[0] + pos[0], p[1] + pos[1]) for p in head_points]
            self._polygon_path(translated_head)
            self._set_color(color)
            ctx.set_line_width(stroke_width)
            ctx.stroke()

        # Draw body lines (remaining points as pairs)
        body_points = points[16:]
        if body_points:
            for i in range(0, len(body_points) - 1, 2):
                if i + 1 < len(body_points):
                    p1 = body_points[i]
                    p2 = body_points[i + 1]
                    ctx.move_to(p1[0] + pos[0], p1[1] + pos[1])
                    ctx.line_to(p2[0] + pos[0], p2[1] + pos[1])
                    self._set_color(color)
                    ctx.set_line_width(stroke_width)
                    ctx.stroke()

    def _render_simple_face(self, data: dict[str, Any], pos: list[float]) -> None:
        """Render a simple face character."""
        ctx = self._ctx
        assert ctx is not None

        radius = data.get("face_radius", 30)
        color = data.get("color", "#000000")
        fill = data.get("fill_color") or "#FFEB3B"

        # Draw face circle
        ctx.arc(pos[0], pos[1], radius, 0, 2 * math.pi)
        self._set_color(fill)
        ctx.fill_preserve()
        self._set_color(color)
        ctx.set_line_width(2)
        ctx.stroke()

        # Draw eyes
        eye_y = pos[1] - radius * 0.2
        eye_offset = radius * 0.3
        eye_radius = radius * 0.1

        # Left eye
        ctx.arc(pos[0] - eye_offset, eye_y, eye_radius, 0, 2 * math.pi)
        self._set_color(color)
        ctx.fill()

        # Right eye
        ctx.arc(pos[0] + eye_offset, eye_y, eye_radius, 0, 2 * math.pi)
        self._set_color(color)
        ctx.fill()

        # Draw mouth based on expression
        expression = data.get("expression", {})
        mouth_type = expression.get("mouth", "normal")
        mouth_y = pos[1] + radius * 0.3

        self._set_color(color)
        ctx.set_line_width(2)

        if mouth_type in ("smile", "happy"):
            # Smiling mouth (arc)
            mouth_width = radius * 0.4
            ctx.move_to(pos[0] - mouth_width, mouth_y - 5)
            ctx.line_to(pos[0], mouth_y + 5)
            ctx.line_to(pos[0] + mouth_width, mouth_y - 5)
            ctx.stroke()
        else:
            # Neutral mouth (line)
            ctx.move_to(pos[0] - radius * 0.3, mouth_y)
            ctx.line_to(pos[0] + radius * 0.3, mouth_y)
            ctx.stroke()

    def _render_rectangle(self, data: dict[str, Any]) -> None:
        """Render a rectangle."""
        ctx = self._ctx
        assert ctx is not None

        pos = data.get("position", [0, 0])
        width = data.get("rect_width", 100)
        height = data.get("rect_height", 100)
        radius = data.get("corner_radius", 0)

        x = pos[0] - width / 2
        y = pos[1] - height / 2

        self._rounded_rect_path(x, y, width, height, radius)

        # Fill
        self._set_color(data.get("fill_color", "#FFFFFF"))
        ctx.fill_preserve()

        # Stroke
        self._set_color(data.get("stroke_color", "#000000"))
        ctx.set_line_width(data.get("stroke_width", 2))
        ctx.stroke()

    def _render_circle(self, data: dict[str, Any]) -> None:
        """Render a circle."""
        ctx = self._ctx
        assert ctx is not None

        pos = data.get("position", [0, 0])
        radius = data.get("radius", 50)

        ctx.arc(pos[0], pos[1], radius, 0, 2 * math.pi)

        # Fill
        self._set_color(data.get("fill_color", "#FFFFFF"))
        ctx.fill_preserve()

        # Stroke
        self._set_color(data.get("stroke_color", "#000000"))
        ctx.set_line_width(data.get("stroke_width", 2))
        ctx.stroke()

    def _render_line(self, data: dict[str, Any]) -> None:
        """Render a line."""
        ctx = self._ctx
        assert ctx is not None

        pos = data.get("position", [0, 0])
        start = data.get("start", [0, 0])
        end = data.get("end", [100, 0])

        ctx.move_to(start[0] + pos[0], start[1] + pos[1])
        ctx.line_to(end[0] + pos[0], end[1] + pos[1])

        self._set_color(data.get("stroke_color", "#000000"))
        ctx.set_line_width(data.get("stroke_width", 2))
        self._set_dash_style(data.get("stroke_style", "solid"))
        ctx.stroke()

    def _render_image(self, data: dict[str, Any]) -> None:
        """Render an image element."""
        ctx = self._ctx
        assert ctx is not None

        pos = data.get("position", [0, 0])
        width = data.get("image_width", 100)
        height = data.get("image_height", 100)
        base64_data = data.get("base64_data")

        # Calculate position (centered on position)
        x = pos[0] - width / 2
        y = pos[1] - height / 2

        if base64_data:
            try:
                import base64
                import io

                try:
                    from PIL import Image as PILImage
                except ImportError:
                    # Pillow not available, render placeholder
                    self._render_image_placeholder(x, y, width, height, "PIL not available")
                    return

                # Decode base64 to image
                image_data = base64.b64decode(base64_data)
                pil_image = PILImage.open(io.BytesIO(image_data))

                # Handle aspect ratio
                fit = data.get("fit", "contain")
                preserve_aspect = data.get("preserve_aspect_ratio", True)

                if preserve_aspect and fit in ("contain", "cover"):
                    # Calculate scaled dimensions
                    orig_w, orig_h = pil_image.size
                    scale_w = width / orig_w
                    scale_h = height / orig_h

                    if fit == "contain":
                        scale = min(scale_w, scale_h)
                    else:  # cover
                        scale = max(scale_w, scale_h)

                    new_w = int(orig_w * scale)
                    new_h = int(orig_h * scale)

                    # Center within bounds
                    offset_x = (width - new_w) / 2
                    offset_y = (height - new_h) / 2

                    # Resize image
                    pil_image = pil_image.resize(  # type: ignore[assignment]
                        (new_w, new_h), PILImage.Resampling.LANCZOS
                    )
                    draw_x = x + offset_x
                    draw_y = y + offset_y
                    draw_w = new_w
                    draw_h = new_h
                else:
                    # Fill mode - resize to exact dimensions
                    pil_image = pil_image.resize(  # type: ignore[assignment]
                        (int(width), int(height)), PILImage.Resampling.LANCZOS
                    )
                    draw_x = x
                    draw_y = y
                    draw_w = width
                    draw_h = height

                # Convert to RGBA if needed
                if pil_image.mode != "RGBA":
                    pil_image = pil_image.convert("RGBA")  # type: ignore[assignment]

                # Create Cairo surface from PIL image
                img_width, img_height = pil_image.size
                img_data = pil_image.tobytes("raw", "BGRa")

                surface = cairo.ImageSurface.create_for_data(
                    bytearray(img_data),
                    cairo.FORMAT_ARGB32,
                    img_width,
                    img_height,
                )

                # Draw image
                ctx.save()
                ctx.translate(draw_x, draw_y)
                ctx.set_source_surface(surface, 0, 0)
                ctx.rectangle(0, 0, draw_w, draw_h)
                ctx.fill()
                ctx.restore()

            except Exception as e:
                # On error, render placeholder with error message
                self._render_image_placeholder(x, y, width, height, f"Error: {str(e)[:20]}")
        else:
            # No image data - render placeholder
            self._render_image_placeholder(x, y, width, height, "No image")

    def _render_image_placeholder(
        self, x: float, y: float, width: float, height: float, text: str
    ) -> None:
        """Render a placeholder rectangle for images without data."""
        ctx = self._ctx
        assert ctx is not None

        # Draw placeholder rectangle
        ctx.rectangle(x, y, width, height)
        self._set_color("#EEEEEE")
        ctx.fill_preserve()
        self._set_color("#CCCCCC")
        ctx.set_line_width(1)
        ctx.stroke()

        # Draw placeholder text
        self._draw_text(
            text,
            x + width / 2,
            y + height / 2,
            font_family="sans-serif",
            font_size=12,
            color="#999999",
            align="center",
        )

    def _render_generic(self, data: dict[str, Any]) -> None:
        """Render a generic CObject using its points."""
        ctx = self._ctx
        assert ctx is not None

        pos = data.get("position", [0, 0])
        points = data.get("points", [])

        if not points:
            return

        translated_points = [(p[0] + pos[0], p[1] + pos[1]) for p in points]

        ctx.move_to(translated_points[0][0], translated_points[0][1])
        for p in translated_points[1:]:
            ctx.line_to(p[0], p[1])

        self._set_color("#000000")
        ctx.set_line_width(2)
        ctx.stroke()

    # Helper methods

    def _set_color(self, color: str | None, alpha: float = 1.0) -> None:
        """Set the current drawing color."""
        ctx = self._ctx
        assert ctx is not None

        if color is None:
            return

        # Parse hex color
        color = color.lstrip("#")
        if len(color) == 6:
            r = int(color[0:2], 16) / 255.0
            g = int(color[2:4], 16) / 255.0
            b = int(color[4:6], 16) / 255.0
        elif len(color) == 8:
            # RGBA format
            r = int(color[0:2], 16) / 255.0
            g = int(color[2:4], 16) / 255.0
            b = int(color[4:6], 16) / 255.0
            alpha = int(color[6:8], 16) / 255.0
        else:
            # Default to black
            r, g, b = 0, 0, 0

        ctx.set_source_rgba(r, g, b, alpha)

    def _set_dash_style(self, style: str) -> None:
        """Set line dash style."""
        ctx = self._ctx
        assert ctx is not None

        if style == "dashed":
            ctx.set_dash([5, 5])
        elif style == "dotted":
            ctx.set_dash([2, 2])
        else:
            ctx.set_dash([])

    def _rounded_rect_path(
        self, x: float, y: float, width: float, height: float, radius: float
    ) -> None:
        """Create a rounded rectangle path."""
        ctx = self._ctx
        assert ctx is not None

        if radius <= 0:
            ctx.rectangle(x, y, width, height)
            return

        # Clamp radius to half of smallest dimension
        radius = min(radius, width / 2, height / 2)

        ctx.new_path()
        ctx.arc(x + radius, y + radius, radius, math.pi, 1.5 * math.pi)
        ctx.arc(x + width - radius, y + radius, radius, 1.5 * math.pi, 2 * math.pi)
        ctx.arc(x + width - radius, y + height - radius, radius, 0, 0.5 * math.pi)
        ctx.arc(x + radius, y + height - radius, radius, 0.5 * math.pi, math.pi)
        ctx.close_path()

    def _polygon_path(self, points: list[tuple[float, float]]) -> None:
        """Create a polygon path from points."""
        ctx = self._ctx
        assert ctx is not None

        if not points:
            return

        ctx.new_path()
        ctx.move_to(points[0][0], points[0][1])
        for p in points[1:]:
            ctx.line_to(p[0], p[1])
        ctx.close_path()

    def _draw_text(
        self,
        text: str,
        x: float,
        y: float,
        font_family: str = "sans-serif",
        font_size: float = 16,
        font_weight: str = "normal",
        font_style: str = "normal",
        color: str | None = "#000000",
        align: str = "center",
        stroke_color: str | None = None,
        stroke_width: float = 0,
    ) -> None:
        """Draw text at the specified position."""
        ctx = self._ctx
        assert ctx is not None

        # Map font weight to Cairo slant/weight
        slant = cairo.FONT_SLANT_ITALIC if font_style == "italic" else cairo.FONT_SLANT_NORMAL
        weight = cairo.FONT_WEIGHT_BOLD if font_weight == "bold" else cairo.FONT_WEIGHT_NORMAL

        ctx.select_font_face(font_family, slant, weight)
        ctx.set_font_size(font_size)

        # Get text extents for alignment
        extents = ctx.text_extents(text)

        # Calculate position based on alignment
        if align == "left":
            text_x = x
        elif align == "right":
            text_x = x - extents.width
        else:  # center
            text_x = x - extents.width / 2

        # Center vertically
        text_y = y + extents.height / 2 - extents.y_bearing - extents.height

        ctx.move_to(text_x, text_y)

        # Draw stroke first if specified
        if stroke_color and stroke_width > 0:
            self._set_color(stroke_color)
            ctx.set_line_width(stroke_width)
            ctx.text_path(text)
            ctx.stroke()
            ctx.move_to(text_x, text_y)

        # Draw fill
        if color:
            self._set_color(color)
            ctx.show_text(text)

    def _render_effect(self, effect: Effect) -> None:
        """Render an effect."""
        ctx = self._ctx
        assert ctx is not None

        data = effect.get_render_data()
        effect_opacity = data.get("opacity", 1.0)

        ctx.save()

        # Apply global opacity via push_group if needed
        if effect_opacity < 1.0:
            ctx.push_group()

        for element in data.get("elements", []):
            self._render_effect_element(element)

        if effect_opacity < 1.0:
            ctx.pop_group_to_source()
            ctx.paint_with_alpha(effect_opacity)

        ctx.restore()

    def _render_effect_element(self, element: dict[str, Any]) -> None:
        """Render a single effect element."""
        ctx = self._ctx
        assert ctx is not None

        element_type = element.get("element_type", "")
        points = element.get("points", [])
        stroke_color = element.get("stroke_color", "#000000")
        stroke_width = element.get("stroke_width", 2.0)
        fill_color = element.get("fill_color")
        opacity = element.get("opacity", 1.0)
        stroke_dasharray = element.get("stroke_dasharray")

        ctx.save()

        # Set dash pattern if specified
        if stroke_dasharray:
            dashes = [float(x) for x in stroke_dasharray.split(",")]
            ctx.set_dash(dashes)

        if element_type == "line" and len(points) >= 2:
            ctx.move_to(points[0][0], points[0][1])
            ctx.line_to(points[1][0], points[1][1])

            if stroke_color != "none":
                self._set_color(stroke_color, opacity)
                ctx.set_line_width(stroke_width)
                ctx.stroke()

        elif element_type == "polyline" and len(points) >= 2:
            ctx.move_to(points[0][0], points[0][1])
            for p in points[1:]:
                ctx.line_to(p[0], p[1])

            if stroke_color != "none":
                self._set_color(stroke_color, opacity)
                ctx.set_line_width(stroke_width)
                ctx.stroke()

        elif element_type == "polygon" and len(points) >= 3:
            ctx.move_to(points[0][0], points[0][1])
            for p in points[1:]:
                ctx.line_to(p[0], p[1])
            ctx.close_path()

            if fill_color:
                self._set_color(fill_color, opacity)
                ctx.fill_preserve()

            if stroke_color != "none":
                self._set_color(stroke_color, opacity)
                ctx.set_line_width(stroke_width)
                ctx.stroke()
            else:
                ctx.new_path()

        elif element_type == "circle" and len(points) >= 1:
            radius = element.get("radius", 10)
            ctx.arc(points[0][0], points[0][1], radius, 0, 2 * math.pi)

            if fill_color:
                self._set_color(fill_color, opacity)
                ctx.fill_preserve()

            if stroke_color != "none":
                self._set_color(stroke_color, opacity)
                ctx.set_line_width(stroke_width)
                ctx.stroke()
            else:
                ctx.new_path()

        ctx.restore()
