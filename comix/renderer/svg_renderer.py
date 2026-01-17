"""SVG Renderer - renders comic pages to SVG format."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

import svgwrite  # type: ignore[import-untyped]
from svgwrite import Drawing
from svgwrite.container import Group  # type: ignore[import-untyped]
from svgwrite.shapes import Circle as SVGCircle  # type: ignore[import-untyped]
from svgwrite.shapes import Line as SVGLine
from svgwrite.shapes import Polygon, Polyline, Rect
from svgwrite.text import Text as SVGText  # type: ignore[import-untyped]

if TYPE_CHECKING:
    from comix.effect.effect import Effect
    from comix.page.page import Page


class SVGRenderer:
    """Renders a Page to SVG format."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self._dwg: Drawing | None = None

    def _prepare_drawing(self, filename: str | None = None) -> None:
        """Prepare the SVG drawing with all content.

        Args:
            filename: Optional filename for the drawing.
        """
        self._dwg = svgwrite.Drawing(
            filename=filename,
            size=(f"{self.page.width}px", f"{self.page.height}px"),
            profile="full",
        )

        self._dwg.add(
            Rect(
                insert=(0, 0),
                size=(self.page.width, self.page.height),
                fill=self.page.background_color,
            )
        )

        # Render effects with negative z_index (behind objects)
        background_effects = sorted(
            [e for e in self.page._effects if e.z_index < 0],
            key=lambda e: e.z_index,
        )
        for effect in background_effects:
            self._render_effect(effect)

        # Render cobjects
        sorted_objects = sorted(
            self.page._cobjects, key=lambda obj: obj.z_index
        )

        for cobject in sorted_objects:
            self._render_cobject(cobject)

        # Render effects with positive z_index (in front of objects)
        foreground_effects = sorted(
            [e for e in self.page._effects if e.z_index >= 0],
            key=lambda e: e.z_index,
        )
        for effect in foreground_effects:
            self._render_effect(effect)

    def render(self, output_path: str) -> str:
        """Render the page to an SVG file.

        Args:
            output_path: Path to save the SVG file.

        Returns:
            Path to the rendered file.
        """
        self._prepare_drawing(output_path)

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        assert self._dwg is not None
        self._dwg.save()

        return output_path

    def render_to_string(self) -> str:
        """Render the page to an SVG string.

        Returns:
            The SVG content as a string.
        """
        self._prepare_drawing()

        assert self._dwg is not None
        return self._dwg.tostring()  # type: ignore[no-any-return]

    def _render_effect(self, effect: Effect) -> None:
        """Render an effect to the SVG."""
        assert self._dwg is not None
        data = effect.get_render_data()
        group = self._dwg.g(opacity=data.get("opacity", 1.0))

        for element in data.get("elements", []):
            self._render_effect_element(element, group)

        self._dwg.add(group)

    def _render_effect_element(self, element: dict[str, Any], group: Group) -> None:
        """Render a single effect element."""
        element_type = element.get("element_type", "")
        points = element.get("points", [])
        stroke_color = element.get("stroke_color", "#000000")
        stroke_width = element.get("stroke_width", 2.0)
        fill_color = element.get("fill_color")
        opacity = element.get("opacity", 1.0)
        stroke_dasharray = element.get("stroke_dasharray")

        if element_type == "line" and len(points) >= 2:
            line = SVGLine(
                start=points[0],
                end=points[1],
                stroke=stroke_color if stroke_color != "none" else "none",
                stroke_width=stroke_width,
                opacity=opacity,
            )
            if stroke_dasharray:
                line["stroke-dasharray"] = stroke_dasharray
            group.add(line)

        elif element_type == "polyline" and len(points) >= 2:
            polyline = Polyline(
                points=points,
                stroke=stroke_color if stroke_color != "none" else "none",
                stroke_width=stroke_width,
                fill="none",
                opacity=opacity,
            )
            if stroke_dasharray:
                polyline["stroke-dasharray"] = stroke_dasharray
            group.add(polyline)

        elif element_type == "polygon" and len(points) >= 3:
            polygon = Polygon(
                points=points,
                stroke=stroke_color if stroke_color != "none" else "none",
                stroke_width=stroke_width,
                fill=fill_color if fill_color else "none",
                opacity=opacity,
            )
            if stroke_dasharray:
                polygon["stroke-dasharray"] = stroke_dasharray
            group.add(polygon)

        elif element_type == "circle" and len(points) >= 1:
            radius = element.get("radius", 10)
            circle = SVGCircle(
                center=points[0],
                r=radius,
                stroke=stroke_color if stroke_color != "none" else "none",
                stroke_width=stroke_width,
                fill=fill_color if fill_color else "none",
                opacity=opacity,
            )
            group.add(circle)

    def _render_cobject(self, cobject: Any, parent_group: Group | None = None) -> None:
        """Render a CObject and its children."""
        assert self._dwg is not None
        data = cobject.get_render_data()
        obj_type = data.get("type", "")

        group = self._dwg.g(opacity=data.get("opacity", 1.0))

        if obj_type == "Panel":
            self._render_panel(data, group)
        elif obj_type in ("Bubble", "SpeechBubble", "ThoughtBubble", "ShoutBubble", "WhisperBubble", "NarratorBubble"):
            self._render_bubble(data, group)
        elif obj_type in ("Text", "StyledText", "SFX"):
            self._render_text(data, group)
        elif obj_type in ("Stickman", "SimpleFace", "Character"):
            self._render_character(data, group)
        elif obj_type == "Rectangle":
            self._render_rectangle(data, group)
        elif obj_type == "Circle":
            self._render_circle(data, group)
        elif obj_type == "Line":
            self._render_line(data, group)
        elif obj_type in ("Image", "AIImage"):
            self._render_image(data, group)
        else:
            self._render_generic(data, group)

        for child in cobject.submobjects:
            self._render_cobject(child, group)

        if parent_group is not None:
            parent_group.add(group)
        else:
            self._dwg.add(group)

    def _render_panel(self, data: dict[str, Any], group: Group) -> None:
        """Render a panel."""
        pos = data.get("position", [0, 0])
        width = data.get("width", 100)
        height = data.get("height", 100)
        border = data.get("border", {})

        x = pos[0] - width / 2
        y = pos[1] - height / 2

        # Draw background color first
        rect = Rect(
            insert=(x, y),
            size=(width, height),
            fill=data.get("background_color", "#FFFFFF"),
            stroke=border.get("color", "#000000"),
            stroke_width=border.get("width", 2),
        )

        if border.get("radius", 0) > 0:
            rect["rx"] = border["radius"]
            rect["ry"] = border["radius"]

        if border.get("style") == "dashed":
            rect["stroke-dasharray"] = "5,5"
        elif border.get("style") == "dotted":
            rect["stroke-dasharray"] = "2,2"

        group.add(rect)

        # Render background image if present
        background_image = data.get("background_image")
        if background_image:
            self._render_panel_background_image(
                background_image, x, y, width, height, border.get("radius", 0), group
            )

    def _render_panel_background_image(
        self,
        image_path: str,
        x: float,
        y: float,
        width: float,
        height: float,
        radius: float,
        group: Group,
    ) -> None:
        """Render a background image for a panel.

        Args:
            image_path: Path to the image file.
            x: Left edge of the panel.
            y: Top edge of the panel.
            width: Panel width.
            height: Panel height.
            radius: Corner radius for clipping.
            group: SVG group to add the image to.
        """
        import base64
        from pathlib import Path

        assert self._dwg is not None

        # Try to load and encode the image
        href = None
        path = Path(image_path)
        if path.exists():
            # Load and encode as data URI for portability
            suffix = path.suffix.lower()
            mime_types = {
                ".png": "image/png",
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".gif": "image/gif",
                ".webp": "image/webp",
                ".svg": "image/svg+xml",
            }
            mime_type = mime_types.get(suffix, "image/png")

            try:
                with open(path, "rb") as f:
                    data = base64.b64encode(f.read()).decode("utf-8")
                href = f"data:{mime_type};base64,{data}"
            except OSError:
                # Fall back to file path reference
                href = str(path.absolute())
        else:
            # Use path directly (might be URL or relative path)
            href = image_path

        if href:
            # Create clip path for rounded corners if needed
            if radius > 0:
                clip_id = f"panel-clip-{id(group)}"
                clip_path = self._dwg.defs.add(self._dwg.clipPath(id=clip_id))
                clip_rect = Rect(insert=(x, y), size=(width, height))
                clip_rect["rx"] = radius
                clip_rect["ry"] = radius
                clip_path.add(clip_rect)

                # Create image with clip path
                image = self._dwg.image(
                    href=href,
                    insert=(x, y),
                    size=(width, height),
                )
                image["preserveAspectRatio"] = "xMidYMid slice"  # Cover behavior
                image["clip-path"] = f"url(#{clip_id})"
                group.add(image)
            else:
                # Simple image without clipping
                image = self._dwg.image(
                    href=href,
                    insert=(x, y),
                    size=(width, height),
                )
                image["preserveAspectRatio"] = "xMidYMid slice"  # Cover behavior
                group.add(image)

    def _render_bubble(self, data: dict[str, Any], group: Group) -> None:
        """Render a speech bubble."""
        pos = data.get("position", [0, 0])
        points = data.get("points", [])
        tail_points = data.get("tail_points", [])
        emphasis = data.get("emphasis", False)

        if points:
            translated_points = [
                (p[0] + pos[0], p[1] + pos[1]) for p in points
            ]

            stroke_dasharray = None
            if data.get("border_style") == "dashed":
                stroke_dasharray = "5,5"
            elif data.get("border_style") == "dotted":
                stroke_dasharray = "2,2"

            # Render emphasis shadow/glow if enabled
            if emphasis:
                shadow_offset = 3
                shadow_points = [
                    (p[0] + shadow_offset, p[1] + shadow_offset) for p in translated_points
                ]
                shadow_path = Polygon(
                    points=shadow_points,
                    fill="#000000",
                    fill_opacity=0.2,
                    stroke="none",
                )
                group.add(shadow_path)

            border_width = data.get("border_width", 2)
            if emphasis:
                # Thicker border for emphasis
                border_width = max(border_width * 1.5, border_width + 1)

            bubble_path = Polygon(
                points=translated_points,
                fill=data.get("fill_color", "#FFFFFF"),
                stroke=data.get("border_color", "#000000"),
                stroke_width=border_width,
            )
            if stroke_dasharray:
                bubble_path["stroke-dasharray"] = stroke_dasharray

            group.add(bubble_path)

        if tail_points and len(tail_points) >= 3:
            translated_tail = [
                (p[0] + pos[0], p[1] + pos[1]) for p in tail_points
            ]

            # Add shadow for tail if emphasis is enabled
            if emphasis:
                shadow_offset = 3
                shadow_tail_points = [
                    (p[0] + shadow_offset, p[1] + shadow_offset) for p in translated_tail
                ]
                shadow_tail = Polygon(
                    points=shadow_tail_points,
                    fill="#000000",
                    fill_opacity=0.2,
                    stroke="none",
                )
                group.add(shadow_tail)

            border_width = data.get("border_width", 2)
            if emphasis:
                border_width = max(border_width * 1.5, border_width + 1)

            tail = Polygon(
                points=translated_tail,
                fill=data.get("fill_color", "#FFFFFF"),
                stroke=data.get("border_color", "#000000"),
                stroke_width=border_width,
            )
            group.add(tail)

        text = data.get("text", "")
        if text:
            text_elem = SVGText(
                text,
                insert=(pos[0], pos[1]),
                text_anchor="middle",
                dominant_baseline="central",
                font_family=data.get("font_family", "sans-serif"),
                font_size=data.get("font_size", 16),
                fill=data.get("font_color", "#000000"),
            )
            group.add(text_elem)

    def _render_text(self, data: dict[str, Any], group: Group) -> None:
        """Render text element."""
        pos = data.get("position", [0, 0])
        text = data.get("text", "")

        if not text:
            return

        text_anchor_map = {
            "left": "start",
            "center": "middle",
            "right": "end",
        }

        if data.get("sfx"):
            if data.get("outline"):
                outline = SVGText(
                    text,
                    insert=(pos[0], pos[1]),
                    text_anchor="middle",
                    dominant_baseline="central",
                    font_family=data.get("font_family", "sans-serif"),
                    font_size=data.get("font_size", 32),
                    font_weight=data.get("font_weight", "bold"),
                    fill="none",
                    stroke=data.get("outline_color", "#FFFFFF"),
                    stroke_width=data.get("outline_width", 3),
                )
                group.add(outline)

        text_elem = SVGText(
            text,
            insert=(pos[0], pos[1]),
            text_anchor=text_anchor_map.get(data.get("align", "center"), "middle"),
            dominant_baseline="central",
            font_family=data.get("font_family", "sans-serif"),
            font_size=data.get("font_size", 16),
            font_weight=data.get("font_weight", "normal"),
            font_style=data.get("font_style", "normal"),
            fill=data.get("color", "#000000"),
        )
        group.add(text_elem)

    def _render_character(self, data: dict[str, Any], group: Group) -> None:
        """Render a character."""
        pos = data.get("position", [0, 0])
        points = data.get("points", [])
        style = data.get("style", "stickman")

        if style == "stickman":
            self._render_stickman(data, group, pos, points)
        elif style == "simple":
            self._render_simple_face(data, group, pos)
        else:
            self._render_generic(data, group)

    def _render_stickman(
        self, data: dict[str, Any], group: Group, pos: list[float], points: list[list[float]]
    ) -> None:
        """Render a stickman character."""
        color = data.get("color", "#000000")
        stroke_width = 2

        if len(points) < 2:
            return

        head_points = points[:16]
        if head_points:
            translated_head = [
                (p[0] + pos[0], p[1] + pos[1]) for p in head_points
            ]
            head = Polygon(
                points=translated_head,
                fill="none",
                stroke=color,
                stroke_width=stroke_width,
            )
            group.add(head)

        body_points = points[16:]
        if body_points:
            for i in range(0, len(body_points) - 1, 2):
                if i + 1 < len(body_points):
                    p1 = body_points[i]
                    p2 = body_points[i + 1]
                    line = SVGLine(
                        start=(p1[0] + pos[0], p1[1] + pos[1]),
                        end=(p2[0] + pos[0], p2[1] + pos[1]),
                        stroke=color,
                        stroke_width=stroke_width,
                    )
                    group.add(line)

    def _render_simple_face(self, data: dict[str, Any], group: Group, pos: list[float]) -> None:
        """Render a simple face character with expression-based features.

        Renders eyes, mouth, and eyebrows based on the expression data.
        Supports all expression types defined in Expression class:
        - Eyes: normal, curved, droopy, narrow, wide, uneven
        - Mouth: normal, smile, frown, open, wavy
        - Eyebrows: normal, raised, worried, furrowed
        """
        radius = data.get("face_radius", 30)
        color = data.get("color", "#000000")
        fill = data.get("fill_color") or "#FFEB3B"

        # Draw face circle
        face = SVGCircle(
            center=(pos[0], pos[1]),
            r=radius,
            fill=fill,
            stroke=color,
            stroke_width=2,
        )
        group.add(face)

        expression = data.get("expression", {})
        eye_type = expression.get("eyes", "normal")
        mouth_type = expression.get("mouth", "normal")
        eyebrow_type = expression.get("eyebrows", "normal")

        # Eye parameters
        eye_y = pos[1] - radius * 0.15
        eye_offset = radius * 0.3
        eye_radius = radius * 0.1

        # Render eyes based on type
        self._render_face_eyes(group, pos, radius, eye_y, eye_offset, eye_radius, eye_type, color)

        # Render eyebrows
        self._render_face_eyebrows(group, pos, radius, eye_y, eye_offset, eyebrow_type, color)

        # Render mouth
        self._render_face_mouth(group, pos, radius, mouth_type, color)

    def _render_face_eyes(
        self,
        group: Group,
        pos: list[float],
        radius: float,
        eye_y: float,
        eye_offset: float,
        eye_radius: float,
        eye_type: str,
        color: str,
    ) -> None:
        """Render eyes based on expression type."""
        left_x = pos[0] - eye_offset
        right_x = pos[0] + eye_offset

        if eye_type == "curved":
            # Happy curved eyes (^_^)
            curve_width = eye_radius * 1.5
            for x in [left_x, right_x]:
                eye = Polyline(
                    points=[
                        (x - curve_width, eye_y),
                        (x, eye_y - eye_radius),
                        (x + curve_width, eye_y),
                    ],
                    fill="none",
                    stroke=color,
                    stroke_width=2,
                )
                group.add(eye)
        elif eye_type == "droopy":
            # Sad droopy eyes
            for x in [left_x, right_x]:
                eye = SVGCircle(
                    center=(x, eye_y + eye_radius * 0.3),
                    r=eye_radius * 0.9,
                    fill=color,
                )
                group.add(eye)
        elif eye_type == "narrow":
            # Angry narrow eyes (horizontal lines)
            for x in [left_x, right_x]:
                eye = SVGLine(
                    start=(x - eye_radius * 1.2, eye_y),
                    end=(x + eye_radius * 1.2, eye_y),
                    stroke=color,
                    stroke_width=2.5,
                )
                group.add(eye)
        elif eye_type == "wide":
            # Surprised wide eyes
            for x in [left_x, right_x]:
                # Larger outer circle
                outer = SVGCircle(
                    center=(x, eye_y),
                    r=eye_radius * 1.5,
                    fill="white",
                    stroke=color,
                    stroke_width=1.5,
                )
                group.add(outer)
                # Inner pupil
                inner = SVGCircle(
                    center=(x, eye_y),
                    r=eye_radius * 0.6,
                    fill=color,
                )
                group.add(inner)
        elif eye_type == "uneven":
            # Confused uneven eyes (one bigger, one smaller)
            # Left eye - smaller
            left_eye = SVGCircle(
                center=(left_x, eye_y + eye_radius * 0.2),
                r=eye_radius * 0.8,
                fill=color,
            )
            group.add(left_eye)
            # Right eye - larger
            right_eye = SVGCircle(
                center=(right_x, eye_y - eye_radius * 0.2),
                r=eye_radius * 1.2,
                fill=color,
            )
            group.add(right_eye)
        elif eye_type == "closed":
            # Sleepy closed eyes (curved lines like happy but lower)
            curve_width = eye_radius * 1.2
            for x in [left_x, right_x]:
                eye = Polyline(
                    points=[
                        (x - curve_width, eye_y + eye_radius * 0.3),
                        (x, eye_y),
                        (x + curve_width, eye_y + eye_radius * 0.3),
                    ],
                    fill="none",
                    stroke=color,
                    stroke_width=2,
                )
                group.add(eye)
        elif eye_type == "stars":
            # Excited star eyes (sparkle effect)
            for x in [left_x, right_x]:
                # Draw a simple 4-point star
                star_size = eye_radius * 1.3
                # Vertical line
                v_line = SVGLine(
                    start=(x, eye_y - star_size),
                    end=(x, eye_y + star_size),
                    stroke=color,
                    stroke_width=2,
                )
                group.add(v_line)
                # Horizontal line
                h_line = SVGLine(
                    start=(x - star_size, eye_y),
                    end=(x + star_size, eye_y),
                    stroke=color,
                    stroke_width=2,
                )
                group.add(h_line)
                # Small center dot
                center_dot = SVGCircle(
                    center=(x, eye_y),
                    r=eye_radius * 0.3,
                    fill=color,
                )
                group.add(center_dot)
        elif eye_type == "tears":
            # Crying eyes with tear drops
            for x in [left_x, right_x]:
                # Normal eye base
                eye = SVGCircle(
                    center=(x, eye_y),
                    r=eye_radius * 0.9,
                    fill=color,
                )
                group.add(eye)
                # Tear drop (simple circle below eye)
                tear = SVGCircle(
                    center=(x + eye_radius * 0.3, eye_y + eye_radius * 1.8),
                    r=eye_radius * 0.4,
                    fill="#87CEEB",  # Light blue for tears
                )
                group.add(tear)
        else:
            # Normal round eyes
            for x in [left_x, right_x]:
                eye = SVGCircle(
                    center=(x, eye_y),
                    r=eye_radius,
                    fill=color,
                )
                group.add(eye)

    def _render_face_eyebrows(
        self,
        group: Group,
        pos: list[float],
        radius: float,
        eye_y: float,
        eye_offset: float,
        eyebrow_type: str,
        color: str,
    ) -> None:
        """Render eyebrows based on expression type."""
        brow_y = eye_y - radius * 0.18
        brow_width = radius * 0.18
        left_x = pos[0] - eye_offset
        right_x = pos[0] + eye_offset

        if eyebrow_type == "raised":
            # Raised eyebrows (surprised/questioning)
            raised_y = brow_y - radius * 0.08
            for x in [left_x, right_x]:
                brow = Polyline(
                    points=[
                        (x - brow_width, raised_y + radius * 0.03),
                        (x, raised_y - radius * 0.03),
                        (x + brow_width, raised_y + radius * 0.03),
                    ],
                    fill="none",
                    stroke=color,
                    stroke_width=2,
                )
                group.add(brow)
        elif eyebrow_type == "worried":
            # Worried eyebrows (angled up toward center)
            # Left eyebrow - slants up to the right
            left_brow = SVGLine(
                start=(left_x - brow_width, brow_y - radius * 0.04),
                end=(left_x + brow_width, brow_y + radius * 0.06),
                stroke=color,
                stroke_width=2,
            )
            group.add(left_brow)
            # Right eyebrow - slants up to the left
            right_brow = SVGLine(
                start=(right_x - brow_width, brow_y + radius * 0.06),
                end=(right_x + brow_width, brow_y - radius * 0.04),
                stroke=color,
                stroke_width=2,
            )
            group.add(right_brow)
        elif eyebrow_type == "furrowed":
            # Furrowed/angry eyebrows (angled down toward center)
            # Left eyebrow - slants down to the right
            left_brow = SVGLine(
                start=(left_x - brow_width, brow_y + radius * 0.04),
                end=(left_x + brow_width, brow_y - radius * 0.08),
                stroke=color,
                stroke_width=2.5,
            )
            group.add(left_brow)
            # Right eyebrow - slants down to the left
            right_brow = SVGLine(
                start=(right_x - brow_width, brow_y - radius * 0.08),
                end=(right_x + brow_width, brow_y + radius * 0.04),
                stroke=color,
                stroke_width=2.5,
            )
            group.add(right_brow)
        elif eyebrow_type == "relaxed":
            # Relaxed/sleepy eyebrows (slightly droopy, low position)
            relaxed_y = brow_y + radius * 0.02
            for x in [left_x, right_x]:
                brow = SVGLine(
                    start=(x - brow_width, relaxed_y - radius * 0.02),
                    end=(x + brow_width, relaxed_y + radius * 0.02),
                    stroke=color,
                    stroke_width=1.5,
                )
                group.add(brow)
        elif eyebrow_type == "asymmetric":
            # Asymmetric eyebrows (one raised, one normal - smirk/skeptical)
            # Left eyebrow - raised
            left_brow = Polyline(
                points=[
                    (left_x - brow_width, brow_y - radius * 0.03),
                    (left_x, brow_y - radius * 0.08),
                    (left_x + brow_width, brow_y - radius * 0.03),
                ],
                fill="none",
                stroke=color,
                stroke_width=2,
            )
            group.add(left_brow)
            # Right eyebrow - flat/normal
            right_brow = SVGLine(
                start=(right_x - brow_width, brow_y),
                end=(right_x + brow_width, brow_y),
                stroke=color,
                stroke_width=2,
            )
            group.add(right_brow)
        # "normal" eyebrows - no visible eyebrows for cleaner look

    def _render_face_mouth(
        self,
        group: Group,
        pos: list[float],
        radius: float,
        mouth_type: str,
        color: str,
    ) -> None:
        """Render mouth based on expression type."""
        mouth_y = pos[1] + radius * 0.35
        mouth_width = radius * 0.35

        if mouth_type in ("smile", "happy"):
            # Smiling mouth (upward curve)
            mouth = Polyline(
                points=[
                    (pos[0] - mouth_width, mouth_y - radius * 0.05),
                    (pos[0], mouth_y + radius * 0.1),
                    (pos[0] + mouth_width, mouth_y - radius * 0.05),
                ],
                fill="none",
                stroke=color,
                stroke_width=2,
            )
            group.add(mouth)
        elif mouth_type == "frown":
            # Frowning mouth (downward curve)
            mouth = Polyline(
                points=[
                    (pos[0] - mouth_width, mouth_y + radius * 0.05),
                    (pos[0], mouth_y - radius * 0.1),
                    (pos[0] + mouth_width, mouth_y + radius * 0.05),
                ],
                fill="none",
                stroke=color,
                stroke_width=2,
            )
            group.add(mouth)
        elif mouth_type == "open":
            # Open mouth (surprised O)
            mouth = SVGCircle(
                center=(pos[0], mouth_y),
                r=radius * 0.15,
                fill="none",
                stroke=color,
                stroke_width=2,
            )
            group.add(mouth)
        elif mouth_type == "wavy":
            # Wavy/uncertain mouth
            segment = mouth_width / 3
            mouth = Polyline(
                points=[
                    (pos[0] - mouth_width, mouth_y),
                    (pos[0] - segment, mouth_y - radius * 0.04),
                    (pos[0], mouth_y + radius * 0.04),
                    (pos[0] + segment, mouth_y - radius * 0.04),
                    (pos[0] + mouth_width, mouth_y),
                ],
                fill="none",
                stroke=color,
                stroke_width=2,
            )
            group.add(mouth)
        elif mouth_type == "grin":
            # Big grin (wide smile with teeth hint)
            grin_width = mouth_width * 1.3
            # Upper lip curve
            mouth = Polyline(
                points=[
                    (pos[0] - grin_width, mouth_y - radius * 0.02),
                    (pos[0] - grin_width * 0.5, mouth_y + radius * 0.08),
                    (pos[0], mouth_y + radius * 0.12),
                    (pos[0] + grin_width * 0.5, mouth_y + radius * 0.08),
                    (pos[0] + grin_width, mouth_y - radius * 0.02),
                ],
                fill="none",
                stroke=color,
                stroke_width=2.5,
            )
            group.add(mouth)
            # Teeth line
            teeth = SVGLine(
                start=(pos[0] - grin_width * 0.6, mouth_y + radius * 0.04),
                end=(pos[0] + grin_width * 0.6, mouth_y + radius * 0.04),
                stroke=color,
                stroke_width=1,
            )
            group.add(teeth)
        elif mouth_type == "gasp":
            # Gasping/scared mouth (oval open mouth)
            mouth = SVGCircle(
                center=(pos[0], mouth_y + radius * 0.05),
                r=radius * 0.18,
                fill="none",
                stroke=color,
                stroke_width=2,
            )
            group.add(mouth)
        elif mouth_type == "smirk":
            # Asymmetric smirk (one side up)
            mouth = Polyline(
                points=[
                    (pos[0] - mouth_width, mouth_y + radius * 0.02),
                    (pos[0], mouth_y),
                    (pos[0] + mouth_width, mouth_y - radius * 0.08),
                ],
                fill="none",
                stroke=color,
                stroke_width=2,
            )
            group.add(mouth)
        else:
            # Normal mouth (straight line)
            mouth = SVGLine(
                start=(pos[0] - mouth_width, mouth_y),
                end=(pos[0] + mouth_width, mouth_y),
                stroke=color,
                stroke_width=2,
            )
            group.add(mouth)

    def _render_rectangle(self, data: dict[str, Any], group: Group) -> None:
        """Render a rectangle."""
        pos = data.get("position", [0, 0])
        width = data.get("rect_width", 100)
        height = data.get("rect_height", 100)

        x = pos[0] - width / 2
        y = pos[1] - height / 2

        rect = Rect(
            insert=(x, y),
            size=(width, height),
            fill=data.get("fill_color", "#FFFFFF"),
            stroke=data.get("stroke_color", "#000000"),
            stroke_width=data.get("stroke_width", 2),
        )

        if data.get("corner_radius", 0) > 0:
            rect["rx"] = data["corner_radius"]
            rect["ry"] = data["corner_radius"]

        group.add(rect)

    def _render_circle(self, data: dict[str, Any], group: Group) -> None:
        """Render a circle."""
        pos = data.get("position", [0, 0])

        circle = SVGCircle(
            center=(pos[0], pos[1]),
            r=data.get("radius", 50),
            fill=data.get("fill_color", "#FFFFFF"),
            stroke=data.get("stroke_color", "#000000"),
            stroke_width=data.get("stroke_width", 2),
        )
        group.add(circle)

    def _render_line(self, data: dict[str, Any], group: Group) -> None:
        """Render a line."""
        pos = data.get("position", [0, 0])
        start = data.get("start", [0, 0])
        end = data.get("end", [100, 0])

        line = SVGLine(
            start=(start[0] + pos[0], start[1] + pos[1]),
            end=(end[0] + pos[0], end[1] + pos[1]),
            stroke=data.get("stroke_color", "#000000"),
            stroke_width=data.get("stroke_width", 2),
        )

        if data.get("stroke_style") == "dashed":
            line["stroke-dasharray"] = "5,5"
        elif data.get("stroke_style") == "dotted":
            line["stroke-dasharray"] = "2,2"

        group.add(line)

    def _render_image(self, data: dict[str, Any], group: Group) -> None:
        """Render an image element."""
        pos = data.get("position", [0, 0])
        width = data.get("image_width", 100)
        height = data.get("image_height", 100)
        data_uri = data.get("data_uri")
        source = data.get("source")
        preserve_aspect = data.get("preserve_aspect_ratio", True)

        # Calculate position (centered on position)
        x = pos[0] - width / 2
        y = pos[1] - height / 2

        # Determine image href
        href = None
        if data_uri:
            href = data_uri
        elif source:
            # Use source directly (file path or URL)
            href = source

        if href:
            # Map fit mode to SVG preserveAspectRatio
            fit = data.get("fit", "contain")
            if preserve_aspect:
                if fit == "contain":
                    aspect_ratio = "xMidYMid meet"
                elif fit == "cover":
                    aspect_ratio = "xMidYMid slice"
                else:
                    aspect_ratio = "xMidYMid meet"
            else:
                aspect_ratio = "none"

            assert self._dwg is not None
            image = self._dwg.image(
                href=href,
                insert=(x, y),
                size=(width, height),
            )
            image["preserveAspectRatio"] = aspect_ratio
            group.add(image)
        else:
            # No image data - render placeholder rectangle
            placeholder = Rect(
                insert=(x, y),
                size=(width, height),
                fill="#EEEEEE",
                stroke="#CCCCCC",
                stroke_width=1,
            )
            group.add(placeholder)

            # Add placeholder text
            text = SVGText(
                "No image",
                insert=(pos[0], pos[1]),
                text_anchor="middle",
                dominant_baseline="central",
                font_family="sans-serif",
                font_size=12,
                fill="#999999",
            )
            group.add(text)

    def _render_generic(self, data: dict[str, Any], group: Group) -> None:
        """Render a generic CObject using its points."""
        pos = data.get("position", [0, 0])
        points = data.get("points", [])

        if not points:
            return

        translated_points = [
            (p[0] + pos[0], p[1] + pos[1]) for p in points
        ]

        polyline = Polyline(
            points=translated_points,
            fill="none",
            stroke="#000000",
            stroke_width=2,
        )
        group.add(polyline)
