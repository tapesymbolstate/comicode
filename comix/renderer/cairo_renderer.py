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
        elif obj_type in ("Stickman", "SimpleFace", "ChubbyStickman", "Robot", "Chibi", "Character"):
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
        elif style == "chubby":
            self._render_chubby_stickman(data, pos)
        elif style == "robot":
            self._render_robot(data, pos)
        elif style == "chibi":
            self._render_chibi(data, pos)
        else:
            self._render_generic(data)

    def _render_stickman(self, data: dict[str, Any], pos: list[float]) -> None:
        """Render a stickman character with expression support.

        Renders a simple stick figure with:
        - Head circle (first 16 points)
        - Body lines (remaining points as pairs)
        - Face features (eyes, mouth, eyebrows) based on expression
        """
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

            # Render face features on the head
            expression = data.get("expression", {})
            eye_type = expression.get("eyes", "normal")
            mouth_type = expression.get("mouth", "normal")
            eyebrow_type = expression.get("eyebrows", "normal")

            # Calculate head center from the head points
            head_center_x = sum(p[0] for p in head_points) / len(head_points)
            head_center_y = sum(p[1] for p in head_points) / len(head_points)
            head_pos = [head_center_x + pos[0], head_center_y + pos[1]]

            # Calculate head radius from character height
            height = data.get("character_height", 100)
            head_radius = height * 0.15  # Stickman head ratio

            # Eye parameters (scaled for stickman head)
            eye_y = head_pos[1] - head_radius * 0.15
            eye_offset = head_radius * 0.35
            eye_radius = head_radius * 0.12

            # Render face features
            self._render_face_eyes_cairo(head_pos, head_radius, eye_y, eye_offset, eye_radius, eye_type, color)
            self._render_face_eyebrows_cairo(head_pos, head_radius, eye_y, eye_offset, eyebrow_type, color)
            self._render_face_mouth_cairo(head_pos, head_radius, mouth_type, color)

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

    def _render_chubby_stickman(self, data: dict[str, Any], pos: list[float]) -> None:
        """Render a chubby stickman character.

        Renders a rounded, friendlier stick figure with:
        - Larger filled head
        - Oval body
        - Thicker limbs with rounded ends
        """
        ctx = self._ctx
        assert ctx is not None

        points = data.get("points", [])
        color = data.get("color", "#000000")
        fill_color = data.get("fill_color", "#FFFFFF")
        stroke_width = 3  # Slightly thicker for chubby appearance

        if len(points) < 24:
            return

        # Draw head (first 24 points form a circle)
        head_points = points[:24]
        if head_points:
            translated_head = [(p[0] + pos[0], p[1] + pos[1]) for p in head_points]
            self._polygon_path(translated_head)
            self._set_color(fill_color)
            ctx.fill_preserve()
            self._set_color(color)
            ctx.set_line_width(stroke_width)
            ctx.stroke()

        # Draw body oval (next 16 points)
        body_points = points[24:40]
        if body_points:
            translated_body = [(p[0] + pos[0], p[1] + pos[1]) for p in body_points]
            self._polygon_path(translated_body)
            self._set_color(fill_color)
            ctx.fill_preserve()
            self._set_color(color)
            ctx.set_line_width(stroke_width)
            ctx.stroke()

        # Render limbs with rounded ends
        limb_start = 40

        def render_limb(start_idx: int) -> None:
            if start_idx + 10 > len(points):
                return
            # Limb line
            p1 = points[start_idx]
            p2 = points[start_idx + 1]
            ctx.move_to(p1[0] + pos[0], p1[1] + pos[1])
            ctx.line_to(p2[0] + pos[0], p2[1] + pos[1])
            self._set_color(color)
            ctx.set_line_width(stroke_width)
            ctx.stroke()

            # Rounded end (circle approximation from next 8 points)
            end_points = points[start_idx + 2 : start_idx + 10]
            if end_points:
                translated_end = [(p[0] + pos[0], p[1] + pos[1]) for p in end_points]
                self._polygon_path(translated_end)
                self._set_color(fill_color)
                ctx.fill_preserve()
                self._set_color(color)
                ctx.set_line_width(stroke_width - 1)
                ctx.stroke()

        # Render all 4 limbs
        render_limb(limb_start)       # Left arm
        render_limb(limb_start + 10)  # Right arm
        render_limb(limb_start + 20)  # Left leg
        render_limb(limb_start + 30)  # Right leg

        # Render face features
        expression = data.get("expression", {})
        eye_type = expression.get("eyes", "normal")
        mouth_type = expression.get("mouth", "normal")
        eyebrow_type = expression.get("eyebrows", "normal")

        # Calculate head center
        head_center_x = sum(p[0] for p in head_points) / len(head_points)
        head_center_y = sum(p[1] for p in head_points) / len(head_points)
        head_pos = [head_center_x + pos[0], head_center_y + pos[1]]

        # Calculate head radius from character height
        height = data.get("character_height", 100)
        head_radius = height * 0.22  # Same ratio as in ChubbyStickman class

        # Eye parameters (scaled for larger head)
        eye_y = head_pos[1] - head_radius * 0.15
        eye_offset = head_radius * 0.35
        eye_radius = head_radius * 0.12

        # Render face features
        self._render_face_eyes_cairo(head_pos, head_radius, eye_y, eye_offset, eye_radius, eye_type, color)
        self._render_face_eyebrows_cairo(head_pos, head_radius, eye_y, eye_offset, eyebrow_type, color)
        self._render_face_mouth_cairo(head_pos, head_radius, mouth_type, color)

    def _render_robot(self, data: dict[str, Any], pos: list[float]) -> None:
        """Render a robot character with mechanical/geometric design.

        Renders a mechanical robot figure with:
        - Optional antenna
        - Square head with screen face display
        - Rectangular body
        - Jointed limbs with circular joint indicators
        - LED-style eyes and digital display mouth
        """
        ctx = self._ctx
        assert ctx is not None

        points = data.get("points", [])
        color = data.get("color", "#333333")
        fill_color = data.get("fill_color", "#6B7280")
        panel_color = data.get("panel_color", "#4A4A4A")
        screen_color = data.get("screen_color", "#1A1A2E")
        led_color = data.get("led_color", "#00FF88")
        has_antenna = data.get("antenna", True)
        stroke_width = 2

        if len(points) < 10:
            return

        # Point indices depend on whether antenna is present
        offset = 2 if has_antenna else 0

        # Render antenna if present
        if has_antenna and len(points) >= 2:
            antenna_tip = points[0]
            antenna_base = points[1]
            # Antenna line
            ctx.move_to(antenna_tip[0] + pos[0], antenna_tip[1] + pos[1])
            ctx.line_to(antenna_base[0] + pos[0], antenna_base[1] + pos[1])
            self._set_color(color)
            ctx.set_line_width(stroke_width)
            ctx.stroke()
            # Antenna ball at tip
            antenna_radius = data.get("character_height", 100) * 0.02
            ctx.arc(antenna_tip[0] + pos[0], antenna_tip[1] + pos[1], antenna_radius, 0, 2 * math.pi)
            self._set_color(led_color)
            ctx.fill_preserve()
            self._set_color(color)
            ctx.set_line_width(1)
            ctx.stroke()

        # Head rectangle (4 points starting at offset)
        head_start = offset
        if len(points) > head_start + 3:
            head_pts = points[head_start:head_start + 4]
            translated_head = [(p[0] + pos[0], p[1] + pos[1]) for p in head_pts]
            # Draw head rectangle
            self._polygon_path(translated_head)
            self._set_color(fill_color)
            ctx.fill_preserve()
            self._set_color(color)
            ctx.set_line_width(stroke_width)
            ctx.stroke()

            # Screen face area (slightly inset rectangle)
            head_center_x = sum(p[0] for p in head_pts) / 4 + pos[0]
            head_center_y = sum(p[1] for p in head_pts) / 4 + pos[1]
            head_width = abs(head_pts[1][0] - head_pts[0][0])
            head_height = abs(head_pts[0][1] - head_pts[3][1])

            screen_margin = head_width * 0.15
            screen_x = head_center_x - head_width / 2 + screen_margin
            screen_y = head_center_y - head_height / 2 + screen_margin
            screen_w = head_width - screen_margin * 2
            screen_h = head_height - screen_margin * 2

            # Draw rounded rectangle for screen
            self._rounded_rect_path(screen_x, screen_y, screen_w, screen_h, 3)
            self._set_color(screen_color)
            ctx.fill_preserve()
            self._set_color(color)
            ctx.set_line_width(1)
            ctx.stroke()

            # Render robot face on the screen
            self._render_robot_face_cairo(data, head_center_x, head_center_y, head_width, led_color)

        # Body rectangle (4 points)
        body_start = offset + 4
        if len(points) > body_start + 3:
            body_pts = points[body_start:body_start + 4]
            translated_body = [(p[0] + pos[0], p[1] + pos[1]) for p in body_pts]
            # Draw body rectangle
            self._polygon_path(translated_body)
            self._set_color(fill_color)
            ctx.fill_preserve()
            self._set_color(color)
            ctx.set_line_width(stroke_width)
            ctx.stroke()

            # Body panel detail (center line)
            body_center_x = (body_pts[0][0] + body_pts[1][0]) / 2 + pos[0]
            body_top_y = body_pts[0][1] + pos[1]
            body_bottom_y = body_pts[2][1] + pos[1]
            ctx.move_to(body_center_x, body_top_y + 5)
            ctx.line_to(body_center_x, body_bottom_y - 5)
            self._set_color(panel_color)
            ctx.set_line_width(1)
            ctx.stroke()

            # Chest light/indicator
            chest_light_radius = data.get("character_height", 100) * 0.02
            ctx.arc(body_center_x, (body_top_y + body_bottom_y) / 2 - 5, chest_light_radius, 0, 2 * math.pi)
            self._set_color(led_color)
            ctx.fill_preserve()
            self._set_color(color)
            ctx.set_line_width(1)
            ctx.stroke()

        # Limbs - each limb has: start, elbow/knee, end + 4 joint circle points
        limb_start = offset + 8

        def render_limb(start_idx: int) -> None:
            """Render a limb segment with joint."""
            if start_idx + 6 > len(points):
                return

            # Upper limb segment
            p1 = points[start_idx]
            p2 = points[start_idx + 1]
            ctx.move_to(p1[0] + pos[0], p1[1] + pos[1])
            ctx.line_to(p2[0] + pos[0], p2[1] + pos[1])
            self._set_color(color)
            ctx.set_line_width(stroke_width + 1)
            ctx.stroke()

            # Lower limb segment
            p3 = points[start_idx + 2]
            ctx.move_to(p2[0] + pos[0], p2[1] + pos[1])
            ctx.line_to(p3[0] + pos[0], p3[1] + pos[1])
            self._set_color(color)
            ctx.set_line_width(stroke_width + 1)
            ctx.stroke()

            # Joint circle at elbow/knee
            joint_pts = points[start_idx + 3:start_idx + 7]
            if len(joint_pts) >= 4:
                joint_center_x = sum(p[0] for p in joint_pts) / 4 + pos[0]
                joint_center_y = sum(p[1] for p in joint_pts) / 4 + pos[1]
                joint_radius = abs(joint_pts[0][0] - joint_pts[2][0]) / 2
                ctx.arc(joint_center_x, joint_center_y, joint_radius, 0, 2 * math.pi)
                self._set_color(panel_color)
                ctx.fill_preserve()
                self._set_color(color)
                ctx.set_line_width(1)
                ctx.stroke()

            # End effector (hand/foot) - small rectangle
            end_x = p3[0] + pos[0]
            end_y = p3[1] + pos[1]
            effector_size = data.get("character_height", 100) * 0.035
            ctx.rectangle(end_x - effector_size, end_y - effector_size / 2, effector_size * 2, effector_size)
            self._set_color(fill_color)
            ctx.fill_preserve()
            self._set_color(color)
            ctx.set_line_width(1)
            ctx.stroke()

        # Render all 4 limbs (7 points each: start, elbow, end, + 4 joint points)
        render_limb(limb_start)  # Left arm
        render_limb(limb_start + 7)  # Right arm
        render_limb(limb_start + 14)  # Left leg
        render_limb(limb_start + 21)  # Right leg

    def _render_robot_face_cairo(
        self,
        data: dict[str, Any],
        center_x: float,
        center_y: float,
        head_width: float,
        led_color: str,
    ) -> None:
        """Render robot face with LED-style eyes and digital display mouth."""
        ctx = self._ctx
        assert ctx is not None

        expression = data.get("expression", {})
        eye_type = expression.get("eyes", "normal")
        mouth_type = expression.get("mouth", "normal")

        eye_y = center_y - head_width * 0.1
        eye_offset = head_width * 0.2
        eye_size = head_width * 0.08

        left_x = center_x - eye_offset
        right_x = center_x + eye_offset

        # Robot eyes - LED style
        if eye_type == "curved":
            # Happy: horizontal bars
            for x in [left_x, right_x]:
                ctx.rectangle(x - eye_size, eye_y - eye_size / 4, eye_size * 2, eye_size / 2)
                self._set_color(led_color)
                ctx.fill()
        elif eye_type == "narrow":
            # Angry: narrow red slits
            for x in [left_x, right_x]:
                ctx.rectangle(x - eye_size, eye_y - eye_size / 6, eye_size * 2, eye_size / 3)
                self._set_color("#FF4444")
                ctx.fill()
        elif eye_type == "wide":
            # Surprised: larger circles
            for x in [left_x, right_x]:
                ctx.arc(x, eye_y, eye_size * 1.2, 0, 2 * math.pi)
                self._set_color(led_color)
                ctx.fill()
        elif eye_type == "closed":
            # Sleepy: thin horizontal lines
            for x in [left_x, right_x]:
                ctx.move_to(x - eye_size, eye_y)
                ctx.line_to(x + eye_size, eye_y)
                self._set_color(led_color)
                ctx.set_line_width(2)
                ctx.stroke()
        elif eye_type == "stars":
            # Excited: plus signs
            for x in [left_x, right_x]:
                ctx.move_to(x, eye_y - eye_size)
                ctx.line_to(x, eye_y + eye_size)
                ctx.move_to(x - eye_size, eye_y)
                ctx.line_to(x + eye_size, eye_y)
                self._set_color(led_color)
                ctx.set_line_width(2)
                ctx.stroke()
        else:
            # Normal: square LED eyes
            for x in [left_x, right_x]:
                ctx.rectangle(x - eye_size / 2, eye_y - eye_size / 2, eye_size, eye_size)
                self._set_color(led_color)
                ctx.fill()

        # Robot mouth - digital display style
        mouth_y = center_y + head_width * 0.15
        mouth_width = head_width * 0.3

        if mouth_type in ("smile", "grin"):
            # Happy: upward chevron
            ctx.move_to(center_x - mouth_width / 2, mouth_y - head_width * 0.03)
            ctx.line_to(center_x, mouth_y + head_width * 0.05)
            ctx.line_to(center_x + mouth_width / 2, mouth_y - head_width * 0.03)
            self._set_color(led_color)
            ctx.set_line_width(2)
            ctx.stroke()
        elif mouth_type == "frown":
            # Sad: downward chevron
            ctx.move_to(center_x - mouth_width / 2, mouth_y + head_width * 0.03)
            ctx.line_to(center_x, mouth_y - head_width * 0.05)
            ctx.line_to(center_x + mouth_width / 2, mouth_y + head_width * 0.03)
            self._set_color(led_color)
            ctx.set_line_width(2)
            ctx.stroke()
        elif mouth_type in ("open", "gasp"):
            # Surprised: circle
            ctx.arc(center_x, mouth_y, head_width * 0.06, 0, 2 * math.pi)
            self._set_color(led_color)
            ctx.set_line_width(2)
            ctx.stroke()
        elif mouth_type == "wavy":
            # Uncertain: zigzag line
            segment = mouth_width / 4
            ctx.move_to(center_x - mouth_width / 2, mouth_y)
            ctx.line_to(center_x - segment, mouth_y - head_width * 0.02)
            ctx.line_to(center_x, mouth_y + head_width * 0.02)
            ctx.line_to(center_x + segment, mouth_y - head_width * 0.02)
            ctx.line_to(center_x + mouth_width / 2, mouth_y)
            self._set_color(led_color)
            ctx.set_line_width(2)
            ctx.stroke()
        else:
            # Normal: horizontal line
            ctx.move_to(center_x - mouth_width / 2, mouth_y)
            ctx.line_to(center_x + mouth_width / 2, mouth_y)
            self._set_color(led_color)
            ctx.set_line_width(2)
            ctx.stroke()

    def _render_chibi(self, data: dict[str, Any], pos: list[float]) -> None:
        """Render a chibi/super-deformed anime-style character.

        Renders a cute chibi figure with:
        - Very large head (40% of height)
        - Small bean-shaped body
        - Short stubby limbs
        - Large expressive eyes
        - Optional hair and blush
        """
        ctx = self._ctx
        assert ctx is not None

        points = data.get("points", [])
        color = data.get("color", "#333333")
        skin_color = data.get("skin_color", "#FFE4C4")
        fill_color = data.get("fill_color", skin_color)
        outfit_color = data.get("outfit_color", "#4A90D9")
        hair_color = data.get("hair_color", "#333333")
        hair_style = data.get("hair_style", "spiky")
        blush = data.get("blush", False)
        stroke_width = 2

        if len(points) < 32:
            return

        # Head circle points (first 32 points)
        head_points = points[:32]

        # Calculate head center for features
        head_center_x = sum(p[0] for p in head_points) / len(head_points)
        head_center_y = sum(p[1] for p in head_points) / len(head_points)
        head_pos = [head_center_x + pos[0], head_center_y + pos[1]]
        height = data.get("character_height", 100)
        head_radius = height * 0.20

        # Render hair (behind head)
        self._render_chibi_hair_cairo(head_pos, head_radius, hair_style, hair_color)

        # Draw head circle with skin color
        ctx.new_path()
        for i, p in enumerate(head_points):
            x, y = p[0] + pos[0], p[1] + pos[1]
            if i == 0:
                ctx.move_to(x, y)
            else:
                ctx.line_to(x, y)
        ctx.close_path()
        self._set_color(fill_color)
        ctx.fill_preserve()
        self._set_color(color)
        ctx.set_line_width(stroke_width)
        ctx.stroke()

        # Body oval points (next 20 points)
        body_points = points[32:52]
        if body_points:
            ctx.new_path()
            for i, p in enumerate(body_points):
                x, y = p[0] + pos[0], p[1] + pos[1]
                if i == 0:
                    ctx.move_to(x, y)
                else:
                    ctx.line_to(x, y)
            ctx.close_path()
            self._set_color(outfit_color)
            ctx.fill_preserve()
            self._set_color(color)
            ctx.set_line_width(stroke_width)
            ctx.stroke()

        # Limbs with rounded ends
        limb_start = 52

        def render_limb(start_idx: int, is_leg: bool = False) -> None:
            if start_idx + 10 > len(points):
                return
            # Limb line
            p1 = points[start_idx]
            p2 = points[start_idx + 1]
            ctx.new_path()
            ctx.move_to(p1[0] + pos[0], p1[1] + pos[1])
            ctx.line_to(p2[0] + pos[0], p2[1] + pos[1])
            self._set_color(color)
            ctx.set_line_width(stroke_width + 2)  # Thicker for chibi style
            ctx.stroke()

            # Rounded end (hand/foot)
            end_points = points[start_idx + 2 : start_idx + 10]
            if end_points:
                ctx.new_path()
                for i, p in enumerate(end_points):
                    x, y = p[0] + pos[0], p[1] + pos[1]
                    if i == 0:
                        ctx.move_to(x, y)
                    else:
                        ctx.line_to(x, y)
                ctx.close_path()
                limb_fill = outfit_color if is_leg else fill_color
                self._set_color(limb_fill)
                ctx.fill_preserve()
                self._set_color(color)
                ctx.set_line_width(stroke_width)
                ctx.stroke()

        # Render arms (skin color for hands)
        render_limb(limb_start, is_leg=False)  # Left arm
        render_limb(limb_start + 10, is_leg=False)  # Right arm
        # Render legs (outfit color)
        render_limb(limb_start + 20, is_leg=True)  # Left leg
        render_limb(limb_start + 30, is_leg=True)  # Right leg

        # Render face features (large chibi eyes)
        expression = data.get("expression", {})
        eye_type = expression.get("eyes", "normal")
        mouth_type = expression.get("mouth", "normal")
        eyebrow_type = expression.get("eyebrows", "normal")

        # Chibi eyes are much larger and positioned higher
        eye_y = head_pos[1] - head_radius * 0.05
        eye_offset = head_radius * 0.40
        eye_radius = head_radius * 0.22  # Much larger eyes for chibi style

        # Render eyes (chibi-style large eyes)
        self._render_chibi_eyes_cairo(head_pos, head_radius, eye_y, eye_offset, eye_radius, eye_type, color)

        # Render eyebrows
        self._render_face_eyebrows_cairo(head_pos, head_radius, eye_y - eye_radius * 0.8, eye_offset, eyebrow_type, color)

        # Render mouth (small and cute)
        self._render_chibi_mouth_cairo(head_pos, head_radius, mouth_type, color)

        # Render blush if enabled
        if blush:
            self._render_chibi_blush_cairo(head_pos, head_radius, eye_y, eye_offset)

    def _render_chibi_hair_cairo(
        self, head_pos: list[float], head_radius: float, hair_style: str, hair_color: str
    ) -> None:
        """Render chibi hair based on style using Cairo."""
        ctx = self._ctx
        assert ctx is not None

        cx, cy = head_pos

        if hair_style == "none":
            return

        elif hair_style == "spiky":
            # Spiky anime-style hair with several pointed tufts
            import math
            spikes = [(-0.6, 1.3), (-0.3, 1.4), (0, 1.5), (0.3, 1.4), (0.6, 1.3)]
            for angle, length in spikes:
                spike_base_x = cx + head_radius * 0.7 * math.sin(angle)
                spike_base_y = cy - head_radius * 0.6
                spike_tip_x = cx + head_radius * length * math.sin(angle)
                spike_tip_y = cy - head_radius * length
                ctx.new_path()
                ctx.move_to(spike_base_x - head_radius * 0.15, spike_base_y)
                ctx.line_to(spike_tip_x, spike_tip_y)
                ctx.line_to(spike_base_x + head_radius * 0.15, spike_base_y)
                ctx.close_path()
                self._set_color(hair_color)
                ctx.fill()

        elif hair_style == "long":
            # Long hair falling down sides
            # Left side
            ctx.new_path()
            ctx.move_to(cx - head_radius * 0.8, cy - head_radius * 0.3)
            ctx.line_to(cx - head_radius * 1.0, cy + head_radius * 0.8)
            ctx.line_to(cx - head_radius * 0.5, cy + head_radius * 0.6)
            ctx.line_to(cx - head_radius * 0.4, cy)
            ctx.close_path()
            self._set_color(hair_color)
            ctx.fill()
            # Right side
            ctx.new_path()
            ctx.move_to(cx + head_radius * 0.8, cy - head_radius * 0.3)
            ctx.line_to(cx + head_radius * 1.0, cy + head_radius * 0.8)
            ctx.line_to(cx + head_radius * 0.5, cy + head_radius * 0.6)
            ctx.line_to(cx + head_radius * 0.4, cy)
            ctx.close_path()
            self._set_color(hair_color)
            ctx.fill()
            # Top bangs
            ctx.new_path()
            ctx.move_to(cx - head_radius * 0.6, cy - head_radius * 0.5)
            ctx.line_to(cx - head_radius * 0.2, cy - head_radius * 0.2)
            ctx.line_to(cx, cy - head_radius * 0.4)
            ctx.line_to(cx + head_radius * 0.2, cy - head_radius * 0.2)
            ctx.line_to(cx + head_radius * 0.6, cy - head_radius * 0.5)
            ctx.line_to(cx, cy - head_radius * 1.1)
            ctx.close_path()
            self._set_color(hair_color)
            ctx.fill()

        elif hair_style == "short":
            # Simple short hair cap
            ctx.new_path()
            ctx.move_to(cx - head_radius * 0.85, cy - head_radius * 0.2)
            ctx.line_to(cx - head_radius * 0.75, cy - head_radius * 0.8)
            ctx.line_to(cx - head_radius * 0.3, cy - head_radius * 1.05)
            ctx.line_to(cx, cy - head_radius * 1.1)
            ctx.line_to(cx + head_radius * 0.3, cy - head_radius * 1.05)
            ctx.line_to(cx + head_radius * 0.75, cy - head_radius * 0.8)
            ctx.line_to(cx + head_radius * 0.85, cy - head_radius * 0.2)
            ctx.close_path()
            self._set_color(hair_color)
            ctx.fill()

        elif hair_style == "twintails":
            # Two pigtails
            # Top hair
            ctx.new_path()
            ctx.move_to(cx - head_radius * 0.7, cy - head_radius * 0.6)
            ctx.line_to(cx, cy - head_radius * 1.15)
            ctx.line_to(cx + head_radius * 0.7, cy - head_radius * 0.6)
            ctx.close_path()
            self._set_color(hair_color)
            ctx.fill()
            # Left twintail
            ctx.new_path()
            ctx.move_to(cx - head_radius * 0.7, cy - head_radius * 0.4)
            ctx.line_to(cx - head_radius * 1.3, cy + head_radius * 0.3)
            ctx.line_to(cx - head_radius * 1.1, cy + head_radius * 0.8)
            ctx.line_to(cx - head_radius * 0.8, cy + head_radius * 0.4)
            ctx.line_to(cx - head_radius * 0.5, cy)
            ctx.close_path()
            self._set_color(hair_color)
            ctx.fill()
            # Right twintail
            ctx.new_path()
            ctx.move_to(cx + head_radius * 0.7, cy - head_radius * 0.4)
            ctx.line_to(cx + head_radius * 1.3, cy + head_radius * 0.3)
            ctx.line_to(cx + head_radius * 1.1, cy + head_radius * 0.8)
            ctx.line_to(cx + head_radius * 0.8, cy + head_radius * 0.4)
            ctx.line_to(cx + head_radius * 0.5, cy)
            ctx.close_path()
            self._set_color(hair_color)
            ctx.fill()

    def _render_chibi_eyes_cairo(
        self, head_pos: list[float], head_radius: float,
        eye_y: float, eye_offset: float, eye_radius: float, eye_type: str, color: str
    ) -> None:
        """Render large chibi-style eyes with highlights using Cairo."""
        ctx = self._ctx
        assert ctx is not None
        import math

        left_x = head_pos[0] - eye_offset
        right_x = head_pos[0] + eye_offset

        if eye_type == "closed" or eye_type == "curved":
            # Happy closed eyes (^_^)
            for x in [left_x, right_x]:
                ctx.new_path()
                ctx.move_to(x - eye_radius, eye_y)
                ctx.curve_to(
                    x - eye_radius * 0.5, eye_y - eye_radius,
                    x + eye_radius * 0.5, eye_y - eye_radius,
                    x + eye_radius, eye_y
                )
                self._set_color(color)
                ctx.set_line_width(2)
                ctx.stroke()

        elif eye_type == "stars":
            # Sparkly star eyes
            for x in [left_x, right_x]:
                ctx.new_path()
                for i in range(10):
                    angle = math.pi / 2 + i * math.pi / 5
                    r = eye_radius if i % 2 == 0 else eye_radius * 0.5
                    px = x + r * math.cos(angle)
                    py = eye_y - r * math.sin(angle)
                    if i == 0:
                        ctx.move_to(px, py)
                    else:
                        ctx.line_to(px, py)
                ctx.close_path()
                self._set_color("#FFD700")
                ctx.fill_preserve()
                self._set_color(color)
                ctx.set_line_width(1)
                ctx.stroke()

        elif eye_type == "tears":
            # Crying eyes with tear drops
            for x in [left_x, right_x]:
                # Large eye circle
                ctx.new_path()
                ctx.arc(x, eye_y, eye_radius, 0, 2 * math.pi)
                self._set_color("#FFFFFF")
                ctx.fill_preserve()
                self._set_color(color)
                ctx.set_line_width(2)
                ctx.stroke()
                # Pupil
                ctx.new_path()
                ctx.arc(x, eye_y, eye_radius * 0.5, 0, 2 * math.pi)
                self._set_color(color)
                ctx.fill()
                # Highlight
                ctx.new_path()
                ctx.arc(x - eye_radius * 0.25, eye_y - eye_radius * 0.25, eye_radius * 0.2, 0, 2 * math.pi)
                self._set_color("#FFFFFF")
                ctx.fill()
                # Tear drop
                ctx.new_path()
                ctx.move_to(x + eye_radius * 0.3, eye_y + eye_radius * 0.8)
                ctx.curve_to(
                    x + eye_radius * 0.5, eye_y + eye_radius * 1.2,
                    x + eye_radius * 0.5, eye_y + eye_radius * 1.5,
                    x + eye_radius * 0.3, eye_y + eye_radius * 1.8
                )
                self._set_color("#87CEEB")
                ctx.set_line_width(3)
                ctx.stroke()

        elif eye_type == "wide":
            # Surprised wide eyes
            for x in [left_x, right_x]:
                ctx.new_path()
                ctx.arc(x, eye_y, eye_radius * 1.2, 0, 2 * math.pi)
                self._set_color("#FFFFFF")
                ctx.fill_preserve()
                self._set_color(color)
                ctx.set_line_width(2)
                ctx.stroke()
                # Pupil
                ctx.new_path()
                ctx.arc(x, eye_y + eye_radius * 0.1, eye_radius * 0.4, 0, 2 * math.pi)
                self._set_color(color)
                ctx.fill()
                # Highlight
                ctx.new_path()
                ctx.arc(x - eye_radius * 0.3, eye_y - eye_radius * 0.3, eye_radius * 0.25, 0, 2 * math.pi)
                self._set_color("#FFFFFF")
                ctx.fill()

        elif eye_type == "narrow":
            # Angry narrow eyes
            for x in [left_x, right_x]:
                ctx.new_path()
                ctx.rectangle(x - eye_radius, eye_y - eye_radius * 0.3, eye_radius * 2, eye_radius * 0.6)
                self._set_color("#FFFFFF")
                ctx.fill_preserve()
                self._set_color(color)
                ctx.set_line_width(2)
                ctx.stroke()
                # Pupil
                ctx.new_path()
                ctx.arc(x, eye_y, eye_radius * 0.25, 0, 2 * math.pi)
                self._set_color(color)
                ctx.fill()

        else:
            # Normal large chibi eyes with shine
            for x in [left_x, right_x]:
                # Large eye oval
                ctx.new_path()
                ctx.arc(x, eye_y, eye_radius, 0, 2 * math.pi)
                self._set_color("#FFFFFF")
                ctx.fill_preserve()
                self._set_color(color)
                ctx.set_line_width(2)
                ctx.stroke()
                # Large pupil
                ctx.new_path()
                ctx.arc(x, eye_y + eye_radius * 0.1, eye_radius * 0.5, 0, 2 * math.pi)
                self._set_color(color)
                ctx.fill()
                # Large highlight (signature chibi shine)
                ctx.new_path()
                ctx.arc(x - eye_radius * 0.25, eye_y - eye_radius * 0.25, eye_radius * 0.25, 0, 2 * math.pi)
                self._set_color("#FFFFFF")
                ctx.fill()
                # Small secondary highlight
                ctx.new_path()
                ctx.arc(x + eye_radius * 0.2, eye_y + eye_radius * 0.1, eye_radius * 0.1, 0, 2 * math.pi)
                self._set_color("#FFFFFF")
                ctx.fill()

    def _render_chibi_mouth_cairo(
        self, head_pos: list[float], head_radius: float, mouth_type: str, color: str
    ) -> None:
        """Render small cute chibi mouth using Cairo."""
        ctx = self._ctx
        assert ctx is not None
        import math

        cx, cy = head_pos
        mouth_y = cy + head_radius * 0.35
        mouth_width = head_radius * 0.25

        if mouth_type == "smile" or mouth_type == "grin":
            # Wide happy smile (cat mouth shape)
            ctx.new_path()
            ctx.move_to(cx - mouth_width, mouth_y)
            ctx.curve_to(
                cx - mouth_width * 0.5, mouth_y + mouth_width * 0.8,
                cx + mouth_width * 0.5, mouth_y + mouth_width * 0.8,
                cx + mouth_width, mouth_y
            )
            self._set_color(color)
            ctx.set_line_width(2)
            ctx.stroke()

        elif mouth_type == "open" or mouth_type == "gasp":
            # Open surprised mouth (small circle)
            ctx.new_path()
            ctx.arc(cx, mouth_y, mouth_width * 0.6, 0, 2 * math.pi)
            self._set_color("#FFB6C1")
            ctx.fill_preserve()
            self._set_color(color)
            ctx.set_line_width(2)
            ctx.stroke()

        elif mouth_type == "frown":
            # Small sad mouth
            ctx.new_path()
            ctx.move_to(cx - mouth_width * 0.6, mouth_y + mouth_width * 0.3)
            ctx.curve_to(
                cx - mouth_width * 0.3, mouth_y - mouth_width * 0.3,
                cx + mouth_width * 0.3, mouth_y - mouth_width * 0.3,
                cx + mouth_width * 0.6, mouth_y + mouth_width * 0.3
            )
            self._set_color(color)
            ctx.set_line_width(2)
            ctx.stroke()

        elif mouth_type == "smirk":
            # Asymmetric smirk
            ctx.new_path()
            ctx.move_to(cx - mouth_width * 0.5, mouth_y)
            ctx.curve_to(
                cx - mouth_width * 0.2, mouth_y + mouth_width * 0.3,
                cx + mouth_width * 0.3, mouth_y,
                cx + mouth_width * 0.7, mouth_y - mouth_width * 0.2
            )
            self._set_color(color)
            ctx.set_line_width(2)
            ctx.stroke()

        elif mouth_type == "wavy":
            # Nervous wavy mouth
            ctx.new_path()
            ctx.move_to(cx - mouth_width * 0.6, mouth_y)
            ctx.curve_to(
                cx - mouth_width * 0.3, mouth_y - mouth_width * 0.2,
                cx - mouth_width * 0.1, mouth_y + mouth_width * 0.2,
                cx, mouth_y
            )
            ctx.curve_to(
                cx + mouth_width * 0.1, mouth_y - mouth_width * 0.2,
                cx + mouth_width * 0.3, mouth_y + mouth_width * 0.2,
                cx + mouth_width * 0.6, mouth_y
            )
            self._set_color(color)
            ctx.set_line_width(2)
            ctx.stroke()

        else:
            # Normal small line or dot mouth
            ctx.new_path()
            ctx.move_to(cx - mouth_width * 0.4, mouth_y)
            ctx.line_to(cx + mouth_width * 0.4, mouth_y)
            self._set_color(color)
            ctx.set_line_width(2)
            ctx.stroke()

    def _render_chibi_blush_cairo(
        self, head_pos: list[float], head_radius: float, eye_y: float, eye_offset: float
    ) -> None:
        """Render cute blush marks on cheeks using Cairo."""
        ctx = self._ctx
        assert ctx is not None
        import math

        blush_y = eye_y + head_radius * 0.3
        blush_x_offset = eye_offset + head_radius * 0.15

        for x in [head_pos[0] - blush_x_offset, head_pos[0] + blush_x_offset]:
            ctx.new_path()
            ctx.arc(x, blush_y, head_radius * 0.12, 0, 2 * math.pi)
            # Set pink color with transparency
            ctx.set_source_rgba(1.0, 0.71, 0.76, 0.6)  # #FFB6C1 with 0.6 opacity
            ctx.fill()

    def _render_simple_face(self, data: dict[str, Any], pos: list[float]) -> None:
        """Render a simple face character with expression-based features.

        Renders eyes, mouth, and eyebrows based on the expression data.
        Supports all expression types defined in Expression class:
        - Eyes: normal, curved, droopy, narrow, wide, uneven
        - Mouth: normal, smile, frown, open, wavy
        - Eyebrows: normal, raised, worried, furrowed
        """
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

        expression = data.get("expression", {})
        eye_type = expression.get("eyes", "normal")
        mouth_type = expression.get("mouth", "normal")
        eyebrow_type = expression.get("eyebrows", "normal")

        # Eye parameters
        eye_y = pos[1] - radius * 0.15
        eye_offset = radius * 0.3
        eye_radius = radius * 0.1

        # Render eyes based on type
        self._render_face_eyes_cairo(pos, radius, eye_y, eye_offset, eye_radius, eye_type, color)

        # Render eyebrows
        self._render_face_eyebrows_cairo(pos, radius, eye_y, eye_offset, eyebrow_type, color)

        # Render mouth
        self._render_face_mouth_cairo(pos, radius, mouth_type, color)

    def _render_face_eyes_cairo(
        self,
        pos: list[float],
        radius: float,
        eye_y: float,
        eye_offset: float,
        eye_radius: float,
        eye_type: str,
        color: str,
    ) -> None:
        """Render eyes based on expression type (Cairo)."""
        ctx = self._ctx
        assert ctx is not None

        left_x = pos[0] - eye_offset
        right_x = pos[0] + eye_offset

        self._set_color(color)

        if eye_type == "curved":
            # Happy curved eyes (^_^)
            curve_width = eye_radius * 1.5
            ctx.set_line_width(2)
            for x in [left_x, right_x]:
                ctx.move_to(x - curve_width, eye_y)
                ctx.line_to(x, eye_y - eye_radius)
                ctx.line_to(x + curve_width, eye_y)
                ctx.stroke()
        elif eye_type == "droopy":
            # Sad droopy eyes
            for x in [left_x, right_x]:
                ctx.arc(x, eye_y + eye_radius * 0.3, eye_radius * 0.9, 0, 2 * math.pi)
                ctx.fill()
        elif eye_type == "narrow":
            # Angry narrow eyes (horizontal lines)
            ctx.set_line_width(2.5)
            for x in [left_x, right_x]:
                ctx.move_to(x - eye_radius * 1.2, eye_y)
                ctx.line_to(x + eye_radius * 1.2, eye_y)
                ctx.stroke()
        elif eye_type == "wide":
            # Surprised wide eyes
            for x in [left_x, right_x]:
                # Larger outer circle (white fill)
                ctx.arc(x, eye_y, eye_radius * 1.5, 0, 2 * math.pi)
                self._set_color("#FFFFFF")
                ctx.fill_preserve()
                self._set_color(color)
                ctx.set_line_width(1.5)
                ctx.stroke()
                # Inner pupil
                ctx.arc(x, eye_y, eye_radius * 0.6, 0, 2 * math.pi)
                ctx.fill()
        elif eye_type == "uneven":
            # Confused uneven eyes (one bigger, one smaller)
            # Left eye - smaller
            ctx.arc(left_x, eye_y + eye_radius * 0.2, eye_radius * 0.8, 0, 2 * math.pi)
            ctx.fill()
            # Right eye - larger
            ctx.arc(right_x, eye_y - eye_radius * 0.2, eye_radius * 1.2, 0, 2 * math.pi)
            ctx.fill()
        elif eye_type == "closed":
            # Sleepy closed eyes (curved lines)
            curve_width = eye_radius * 1.2
            ctx.set_line_width(2)
            for x in [left_x, right_x]:
                ctx.move_to(x - curve_width, eye_y + eye_radius * 0.3)
                ctx.line_to(x, eye_y)
                ctx.line_to(x + curve_width, eye_y + eye_radius * 0.3)
                ctx.stroke()
        elif eye_type == "stars":
            # Excited star eyes (sparkle effect)
            star_size = eye_radius * 1.3
            ctx.set_line_width(2)
            for x in [left_x, right_x]:
                # Vertical line
                ctx.move_to(x, eye_y - star_size)
                ctx.line_to(x, eye_y + star_size)
                ctx.stroke()
                # Horizontal line
                ctx.move_to(x - star_size, eye_y)
                ctx.line_to(x + star_size, eye_y)
                ctx.stroke()
                # Small center dot
                ctx.arc(x, eye_y, eye_radius * 0.3, 0, 2 * math.pi)
                ctx.fill()
        elif eye_type == "tears":
            # Crying eyes with tear drops
            for x in [left_x, right_x]:
                # Normal eye base
                ctx.arc(x, eye_y, eye_radius * 0.9, 0, 2 * math.pi)
                ctx.fill()
                # Tear drop (light blue)
                self._set_color("#87CEEB")
                ctx.arc(x + eye_radius * 0.3, eye_y + eye_radius * 1.8, eye_radius * 0.4, 0, 2 * math.pi)
                ctx.fill()
                self._set_color(color)  # Restore color
        else:
            # Normal round eyes
            for x in [left_x, right_x]:
                ctx.arc(x, eye_y, eye_radius, 0, 2 * math.pi)
                ctx.fill()

    def _render_face_eyebrows_cairo(
        self,
        pos: list[float],
        radius: float,
        eye_y: float,
        eye_offset: float,
        eyebrow_type: str,
        color: str,
    ) -> None:
        """Render eyebrows based on expression type (Cairo)."""
        ctx = self._ctx
        assert ctx is not None

        brow_y = eye_y - radius * 0.18
        brow_width = radius * 0.18
        left_x = pos[0] - eye_offset
        right_x = pos[0] + eye_offset

        self._set_color(color)

        if eyebrow_type == "raised":
            # Raised eyebrows (surprised/questioning)
            raised_y = brow_y - radius * 0.08
            ctx.set_line_width(2)
            for x in [left_x, right_x]:
                ctx.move_to(x - brow_width, raised_y + radius * 0.03)
                ctx.line_to(x, raised_y - radius * 0.03)
                ctx.line_to(x + brow_width, raised_y + radius * 0.03)
                ctx.stroke()
        elif eyebrow_type == "worried":
            # Worried eyebrows (angled up toward center)
            ctx.set_line_width(2)
            # Left eyebrow - slants up to the right
            ctx.move_to(left_x - brow_width, brow_y - radius * 0.04)
            ctx.line_to(left_x + brow_width, brow_y + radius * 0.06)
            ctx.stroke()
            # Right eyebrow - slants up to the left
            ctx.move_to(right_x - brow_width, brow_y + radius * 0.06)
            ctx.line_to(right_x + brow_width, brow_y - radius * 0.04)
            ctx.stroke()
        elif eyebrow_type == "furrowed":
            # Furrowed/angry eyebrows (angled down toward center)
            ctx.set_line_width(2.5)
            # Left eyebrow - slants down to the right
            ctx.move_to(left_x - brow_width, brow_y + radius * 0.04)
            ctx.line_to(left_x + brow_width, brow_y - radius * 0.08)
            ctx.stroke()
            # Right eyebrow - slants down to the left
            ctx.move_to(right_x - brow_width, brow_y - radius * 0.08)
            ctx.line_to(right_x + brow_width, brow_y + radius * 0.04)
            ctx.stroke()
        elif eyebrow_type == "relaxed":
            # Relaxed/sleepy eyebrows (slightly droopy, low position)
            relaxed_y = brow_y + radius * 0.02
            ctx.set_line_width(1.5)
            for x in [left_x, right_x]:
                ctx.move_to(x - brow_width, relaxed_y - radius * 0.02)
                ctx.line_to(x + brow_width, relaxed_y + radius * 0.02)
                ctx.stroke()
        elif eyebrow_type == "asymmetric":
            # Asymmetric eyebrows (one raised, one normal - smirk/skeptical)
            ctx.set_line_width(2)
            # Left eyebrow - raised
            ctx.move_to(left_x - brow_width, brow_y - radius * 0.03)
            ctx.line_to(left_x, brow_y - radius * 0.08)
            ctx.line_to(left_x + brow_width, brow_y - radius * 0.03)
            ctx.stroke()
            # Right eyebrow - flat/normal
            ctx.move_to(right_x - brow_width, brow_y)
            ctx.line_to(right_x + brow_width, brow_y)
            ctx.stroke()
        # "normal" eyebrows - no visible eyebrows for cleaner look

    def _render_face_mouth_cairo(
        self,
        pos: list[float],
        radius: float,
        mouth_type: str,
        color: str,
    ) -> None:
        """Render mouth based on expression type (Cairo)."""
        ctx = self._ctx
        assert ctx is not None

        mouth_y = pos[1] + radius * 0.35
        mouth_width = radius * 0.35

        self._set_color(color)
        ctx.set_line_width(2)

        if mouth_type in ("smile", "happy"):
            # Smiling mouth (upward curve)
            ctx.move_to(pos[0] - mouth_width, mouth_y - radius * 0.05)
            ctx.line_to(pos[0], mouth_y + radius * 0.1)
            ctx.line_to(pos[0] + mouth_width, mouth_y - radius * 0.05)
            ctx.stroke()
        elif mouth_type == "frown":
            # Frowning mouth (downward curve)
            ctx.move_to(pos[0] - mouth_width, mouth_y + radius * 0.05)
            ctx.line_to(pos[0], mouth_y - radius * 0.1)
            ctx.line_to(pos[0] + mouth_width, mouth_y + radius * 0.05)
            ctx.stroke()
        elif mouth_type == "open":
            # Open mouth (surprised O)
            ctx.arc(pos[0], mouth_y, radius * 0.15, 0, 2 * math.pi)
            ctx.stroke()
        elif mouth_type == "wavy":
            # Wavy/uncertain mouth
            segment = mouth_width / 3
            ctx.move_to(pos[0] - mouth_width, mouth_y)
            ctx.line_to(pos[0] - segment, mouth_y - radius * 0.04)
            ctx.line_to(pos[0], mouth_y + radius * 0.04)
            ctx.line_to(pos[0] + segment, mouth_y - radius * 0.04)
            ctx.line_to(pos[0] + mouth_width, mouth_y)
            ctx.stroke()
        elif mouth_type == "grin":
            # Big grin (wide smile with teeth hint)
            grin_width = mouth_width * 1.3
            ctx.set_line_width(2.5)
            # Upper lip curve
            ctx.move_to(pos[0] - grin_width, mouth_y - radius * 0.02)
            ctx.line_to(pos[0] - grin_width * 0.5, mouth_y + radius * 0.08)
            ctx.line_to(pos[0], mouth_y + radius * 0.12)
            ctx.line_to(pos[0] + grin_width * 0.5, mouth_y + radius * 0.08)
            ctx.line_to(pos[0] + grin_width, mouth_y - radius * 0.02)
            ctx.stroke()
            # Teeth line
            ctx.set_line_width(1)
            ctx.move_to(pos[0] - grin_width * 0.6, mouth_y + radius * 0.04)
            ctx.line_to(pos[0] + grin_width * 0.6, mouth_y + radius * 0.04)
            ctx.stroke()
        elif mouth_type == "gasp":
            # Gasping/scared mouth (oval open mouth)
            ctx.arc(pos[0], mouth_y + radius * 0.05, radius * 0.18, 0, 2 * math.pi)
            ctx.stroke()
        elif mouth_type == "smirk":
            # Asymmetric smirk (one side up)
            ctx.move_to(pos[0] - mouth_width, mouth_y + radius * 0.02)
            ctx.line_to(pos[0], mouth_y)
            ctx.line_to(pos[0] + mouth_width, mouth_y - radius * 0.08)
            ctx.stroke()
        else:
            # Normal mouth (straight line)
            ctx.move_to(pos[0] - mouth_width, mouth_y)
            ctx.line_to(pos[0] + mouth_width, mouth_y)
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
