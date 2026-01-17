"""SVG Renderer - renders comic pages to SVG format."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

import svgwrite  # type: ignore[import-untyped]
from svgwrite import Drawing
from svgwrite.container import Group  # type: ignore[import-untyped]
from svgwrite.path import Path as SVGPath  # type: ignore[import-untyped]
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
        elif obj_type in ("Stickman", "SimpleFace", "ChubbyStickman", "Robot", "Chibi", "Cartoon", "Character"):
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
        elif style == "chubby":
            self._render_chubby_stickman(data, group, pos, points)
        elif style == "robot":
            self._render_robot(data, group, pos, points)
        elif style == "chibi":
            self._render_chibi(data, group, pos, points)
        elif style == "anime":
            self._render_anime(data, group, pos, points)
        elif style == "superhero":
            self._render_superhero(data, group, pos, points)
        elif style == "cartoon":
            self._render_cartoon(data, group, pos, points)
        else:
            self._render_generic(data, group)

    def _render_stickman(
        self, data: dict[str, Any], group: Group, pos: list[float], points: list[list[float]]
    ) -> None:
        """Render a stickman character with expression support.

        Renders a simple stick figure with:
        - Head circle (first 16 points)
        - Body lines (remaining points as pairs)
        - Face features (eyes, mouth, eyebrows) based on expression
        """
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
            self._render_face_eyes(group, head_pos, head_radius, eye_y, eye_offset, eye_radius, eye_type, color)
            self._render_face_eyebrows(group, head_pos, head_radius, eye_y, eye_offset, eyebrow_type, color)
            self._render_face_mouth(group, head_pos, head_radius, mouth_type, color)

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

    def _render_chubby_stickman(
        self, data: dict[str, Any], group: Group, pos: list[float], points: list[list[float]]
    ) -> None:
        """Render a chubby stickman character.

        Renders a rounded, friendlier stick figure with:
        - Larger filled head
        - Oval body
        - Thicker limbs with rounded ends
        """
        color = data.get("color", "#000000")
        fill_color = data.get("fill_color", "#FFFFFF")
        stroke_width = 3  # Slightly thicker for chubby appearance

        if len(points) < 24:
            return

        # Head points (first 24 points form the head circle)
        head_points = points[:24]
        translated_head = [(p[0] + pos[0], p[1] + pos[1]) for p in head_points]
        head = Polygon(
            points=translated_head,
            fill=fill_color,
            stroke=color,
            stroke_width=stroke_width,
        )
        group.add(head)

        # Body oval points (next 16 points)
        body_points = points[24:40]
        if body_points:
            translated_body = [(p[0] + pos[0], p[1] + pos[1]) for p in body_points]
            body = Polygon(
                points=translated_body,
                fill=fill_color,
                stroke=color,
                stroke_width=stroke_width,
            )
            group.add(body)

        # Limbs with rounded ends
        # Points structure after body: left_arm_start, left_arm_end, left_hand(8pts),
        # right_arm_start, right_arm_end, right_hand(8pts), etc.
        limb_start = 40

        # Helper to render a limb segment
        def render_limb(start_idx: int) -> None:
            if start_idx + 10 > len(points):
                return
            # Limb line
            p1 = points[start_idx]
            p2 = points[start_idx + 1]
            line = SVGLine(
                start=(p1[0] + pos[0], p1[1] + pos[1]),
                end=(p2[0] + pos[0], p2[1] + pos[1]),
                stroke=color,
                stroke_width=stroke_width,
            )
            group.add(line)
            # Rounded end (circle approximation from next 8 points)
            end_points = points[start_idx + 2 : start_idx + 10]
            if end_points:
                translated_end = [(p[0] + pos[0], p[1] + pos[1]) for p in end_points]
                end_shape = Polygon(
                    points=translated_end,
                    fill=fill_color,
                    stroke=color,
                    stroke_width=stroke_width - 1,
                )
                group.add(end_shape)

        # Render all 4 limbs
        # Left arm: starts at index 40
        render_limb(limb_start)
        # Right arm: starts at index 50
        render_limb(limb_start + 10)
        # Left leg: starts at index 60
        render_limb(limb_start + 20)
        # Right leg: starts at index 70
        render_limb(limb_start + 30)

        # Render simple face features on the head
        expression = data.get("expression", {})
        eye_type = expression.get("eyes", "normal")
        mouth_type = expression.get("mouth", "normal")
        eyebrow_type = expression.get("eyebrows", "normal")

        # Calculate head center (average of head points)
        head_center_x = sum(p[0] for p in head_points) / len(head_points)
        head_center_y = sum(p[1] for p in head_points) / len(head_points)
        head_pos = [head_center_x + pos[0], head_center_y + pos[1]]

        # Calculate head radius from data
        height = data.get("character_height", 100)
        head_radius = height * 0.22  # Same ratio as in ChubbyStickman class

        # Eye parameters (scaled for larger head)
        eye_y = head_pos[1] - head_radius * 0.15
        eye_offset = head_radius * 0.35
        eye_radius = head_radius * 0.12

        # Render eyes
        self._render_face_eyes(group, head_pos, head_radius, eye_y, eye_offset, eye_radius, eye_type, color)
        # Render eyebrows
        self._render_face_eyebrows(group, head_pos, head_radius, eye_y, eye_offset, eyebrow_type, color)
        # Render mouth
        self._render_face_mouth(group, head_pos, head_radius, mouth_type, color)

    def _render_robot(
        self, data: dict[str, Any], group: Group, pos: list[float], points: list[list[float]]
    ) -> None:
        """Render a robot character with mechanical/geometric design.

        Renders a mechanical robot figure with:
        - Optional antenna
        - Square head with screen face display
        - Rectangular body
        - Jointed limbs with circular joint indicators
        - LED-style eyes and digital display mouth
        """
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
            antenna_line = SVGLine(
                start=(antenna_tip[0] + pos[0], antenna_tip[1] + pos[1]),
                end=(antenna_base[0] + pos[0], antenna_base[1] + pos[1]),
                stroke=color,
                stroke_width=stroke_width,
            )
            group.add(antenna_line)
            # Antenna ball at tip
            antenna_ball = SVGCircle(
                center=(antenna_tip[0] + pos[0], antenna_tip[1] + pos[1]),
                r=data.get("character_height", 100) * 0.02,
                fill=led_color,
                stroke=color,
                stroke_width=1,
            )
            group.add(antenna_ball)

        # Head rectangle (4 points starting at offset)
        head_start = offset
        if len(points) > head_start + 3:
            head_pts = points[head_start:head_start + 4]
            translated_head = [(p[0] + pos[0], p[1] + pos[1]) for p in head_pts]
            # Main head
            head = Polygon(
                points=translated_head,
                fill=fill_color,
                stroke=color,
                stroke_width=stroke_width,
            )
            group.add(head)

            # Screen face area (slightly inset rectangle)
            head_center_x = sum(p[0] for p in head_pts) / 4 + pos[0]
            head_center_y = sum(p[1] for p in head_pts) / 4 + pos[1]
            head_width = abs(head_pts[1][0] - head_pts[0][0])
            head_height = abs(head_pts[0][1] - head_pts[3][1])

            screen_margin = head_width * 0.15
            screen_rect = Rect(
                insert=(head_center_x - head_width / 2 + screen_margin,
                        head_center_y - head_height / 2 + screen_margin),
                size=(head_width - screen_margin * 2, head_height - screen_margin * 2),
                fill=screen_color,
                stroke=color,
                stroke_width=1,
                rx=3,
                ry=3,
            )
            group.add(screen_rect)

            # Render robot face on the screen
            self._render_robot_face(group, data, head_center_x, head_center_y, head_width, led_color)

        # Body rectangle (4 points)
        body_start = offset + 4
        if len(points) > body_start + 3:
            body_pts = points[body_start:body_start + 4]
            translated_body = [(p[0] + pos[0], p[1] + pos[1]) for p in body_pts]
            # Main body
            body = Polygon(
                points=translated_body,
                fill=fill_color,
                stroke=color,
                stroke_width=stroke_width,
            )
            group.add(body)

            # Body panel detail (center line)
            body_center_x = (body_pts[0][0] + body_pts[1][0]) / 2 + pos[0]
            body_top_y = body_pts[0][1] + pos[1]
            body_bottom_y = body_pts[2][1] + pos[1]
            panel_line = SVGLine(
                start=(body_center_x, body_top_y + 5),
                end=(body_center_x, body_bottom_y - 5),
                stroke=panel_color,
                stroke_width=1,
            )
            group.add(panel_line)

            # Chest light/indicator
            chest_light = SVGCircle(
                center=(body_center_x, (body_top_y + body_bottom_y) / 2 - 5),
                r=data.get("character_height", 100) * 0.02,
                fill=led_color,
                stroke=color,
                stroke_width=1,
            )
            group.add(chest_light)

        # Limbs - each limb has: start, elbow/knee, end + 4 joint circle points
        limb_start = offset + 8

        def render_limb(start_idx: int) -> None:
            """Render a limb segment with joint."""
            if start_idx + 6 > len(points):
                return

            # Upper limb segment
            p1 = points[start_idx]
            p2 = points[start_idx + 1]
            upper_limb = SVGLine(
                start=(p1[0] + pos[0], p1[1] + pos[1]),
                end=(p2[0] + pos[0], p2[1] + pos[1]),
                stroke=color,
                stroke_width=stroke_width + 1,
            )
            group.add(upper_limb)

            # Lower limb segment
            p3 = points[start_idx + 2]
            lower_limb = SVGLine(
                start=(p2[0] + pos[0], p2[1] + pos[1]),
                end=(p3[0] + pos[0], p3[1] + pos[1]),
                stroke=color,
                stroke_width=stroke_width + 1,
            )
            group.add(lower_limb)

            # Joint circle at elbow/knee (uses the 4 points to get center)
            joint_pts = points[start_idx + 3:start_idx + 7]
            if len(joint_pts) >= 4:
                joint_center_x = sum(p[0] for p in joint_pts) / 4 + pos[0]
                joint_center_y = sum(p[1] for p in joint_pts) / 4 + pos[1]
                joint_radius = abs(joint_pts[0][0] - joint_pts[2][0]) / 2
                joint = SVGCircle(
                    center=(joint_center_x, joint_center_y),
                    r=joint_radius,
                    fill=panel_color,
                    stroke=color,
                    stroke_width=1,
                )
                group.add(joint)

            # End effector (hand/foot) - small rectangle
            end_x = p3[0] + pos[0]
            end_y = p3[1] + pos[1]
            effector_size = data.get("character_height", 100) * 0.035
            effector = Rect(
                insert=(end_x - effector_size, end_y - effector_size / 2),
                size=(effector_size * 2, effector_size),
                fill=fill_color,
                stroke=color,
                stroke_width=1,
            )
            group.add(effector)

        # Render all 4 limbs (7 points each: start, elbow, end, + 4 joint points)
        render_limb(limb_start)  # Left arm
        render_limb(limb_start + 7)  # Right arm
        render_limb(limb_start + 14)  # Left leg
        render_limb(limb_start + 21)  # Right leg

    def _render_robot_face(
        self,
        group: Group,
        data: dict[str, Any],
        center_x: float,
        center_y: float,
        head_width: float,
        led_color: str,
    ) -> None:
        """Render robot face with LED-style eyes and digital display mouth."""
        expression = data.get("expression", {})
        eye_type = expression.get("eyes", "normal")
        mouth_type = expression.get("mouth", "normal")

        eye_y = center_y - head_width * 0.1
        eye_offset = head_width * 0.2
        eye_size = head_width * 0.08

        # Robot eyes - LED style (rectangles or geometric shapes)
        left_x = center_x - eye_offset
        right_x = center_x + eye_offset

        if eye_type == "curved":
            # Happy: horizontal bars (upward slant)
            for x in [left_x, right_x]:
                eye = Rect(
                    insert=(x - eye_size, eye_y - eye_size / 4),
                    size=(eye_size * 2, eye_size / 2),
                    fill=led_color,
                    stroke="none",
                )
                group.add(eye)
        elif eye_type == "narrow":
            # Angry: narrow horizontal slits
            for x in [left_x, right_x]:
                eye = Rect(
                    insert=(x - eye_size, eye_y - eye_size / 6),
                    size=(eye_size * 2, eye_size / 3),
                    fill="#FF4444",  # Red for angry
                    stroke="none",
                )
                group.add(eye)
        elif eye_type == "wide":
            # Surprised: larger circles
            for x in [left_x, right_x]:
                eye = SVGCircle(
                    center=(x, eye_y),
                    r=eye_size * 1.2,
                    fill=led_color,
                    stroke="none",
                )
                group.add(eye)
        elif eye_type == "closed":
            # Sleepy: thin horizontal lines
            for x in [left_x, right_x]:
                eye = SVGLine(
                    start=(x - eye_size, eye_y),
                    end=(x + eye_size, eye_y),
                    stroke=led_color,
                    stroke_width=2,
                )
                group.add(eye)
        elif eye_type == "stars":
            # Excited: plus signs (cross pattern)
            for x in [left_x, right_x]:
                v_line = SVGLine(
                    start=(x, eye_y - eye_size),
                    end=(x, eye_y + eye_size),
                    stroke=led_color,
                    stroke_width=2,
                )
                group.add(v_line)
                h_line = SVGLine(
                    start=(x - eye_size, eye_y),
                    end=(x + eye_size, eye_y),
                    stroke=led_color,
                    stroke_width=2,
                )
                group.add(h_line)
        else:
            # Normal: square LED eyes
            for x in [left_x, right_x]:
                eye = Rect(
                    insert=(x - eye_size / 2, eye_y - eye_size / 2),
                    size=(eye_size, eye_size),
                    fill=led_color,
                    stroke="none",
                )
                group.add(eye)

        # Robot mouth - digital display style
        mouth_y = center_y + head_width * 0.15
        mouth_width = head_width * 0.3

        if mouth_type in ("smile", "grin"):
            # Happy: upward chevron or U shape
            mouth = Polyline(
                points=[
                    (center_x - mouth_width / 2, mouth_y - head_width * 0.03),
                    (center_x, mouth_y + head_width * 0.05),
                    (center_x + mouth_width / 2, mouth_y - head_width * 0.03),
                ],
                fill="none",
                stroke=led_color,
                stroke_width=2,
            )
            group.add(mouth)
        elif mouth_type == "frown":
            # Sad: downward chevron
            mouth = Polyline(
                points=[
                    (center_x - mouth_width / 2, mouth_y + head_width * 0.03),
                    (center_x, mouth_y - head_width * 0.05),
                    (center_x + mouth_width / 2, mouth_y + head_width * 0.03),
                ],
                fill="none",
                stroke=led_color,
                stroke_width=2,
            )
            group.add(mouth)
        elif mouth_type in ("open", "gasp"):
            # Surprised: circle
            mouth = SVGCircle(
                center=(center_x, mouth_y),
                r=head_width * 0.06,
                fill="none",
                stroke=led_color,
                stroke_width=2,
            )
            group.add(mouth)
        elif mouth_type == "wavy":
            # Uncertain: zigzag line
            segment = mouth_width / 4
            mouth = Polyline(
                points=[
                    (center_x - mouth_width / 2, mouth_y),
                    (center_x - segment, mouth_y - head_width * 0.02),
                    (center_x, mouth_y + head_width * 0.02),
                    (center_x + segment, mouth_y - head_width * 0.02),
                    (center_x + mouth_width / 2, mouth_y),
                ],
                fill="none",
                stroke=led_color,
                stroke_width=2,
            )
            group.add(mouth)
        else:
            # Normal: horizontal line
            mouth = SVGLine(
                start=(center_x - mouth_width / 2, mouth_y),
                end=(center_x + mouth_width / 2, mouth_y),
                stroke=led_color,
                stroke_width=2,
            )
            group.add(mouth)

    def _render_chibi(
        self, data: dict[str, Any], group: Group, pos: list[float], points: list[list[float]]
    ) -> None:
        """Render a chibi/super-deformed anime-style character.

        Renders a cute chibi figure with:
        - Very large head (40% of height)
        - Small bean-shaped body
        - Short stubby limbs
        - Large expressive eyes
        - Optional hair and blush
        """
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
        translated_head = [(p[0] + pos[0], p[1] + pos[1]) for p in head_points]

        # Calculate head center for features
        head_center_x = sum(p[0] for p in head_points) / len(head_points)
        head_center_y = sum(p[1] for p in head_points) / len(head_points)
        head_pos = [head_center_x + pos[0], head_center_y + pos[1]]
        height = data.get("character_height", 100)
        head_radius = height * 0.20

        # Render hair (behind head)
        self._render_chibi_hair(group, head_pos, head_radius, hair_style, hair_color)

        # Draw head circle with skin color
        head = Polygon(
            points=translated_head,
            fill=fill_color,
            stroke=color,
            stroke_width=stroke_width,
        )
        group.add(head)

        # Body oval points (next 20 points)
        body_points = points[32:52]
        if body_points:
            translated_body = [(p[0] + pos[0], p[1] + pos[1]) for p in body_points]
            # Body with outfit color
            body = Polygon(
                points=translated_body,
                fill=outfit_color,
                stroke=color,
                stroke_width=stroke_width,
            )
            group.add(body)

        # Limbs with rounded ends
        # Points structure: left_arm_start, left_arm_end, left_hand(8pts),
        # right_arm_start, right_arm_end, right_hand(8pts),
        # left_leg_start, left_leg_end, left_foot(8pts),
        # right_leg_start, right_leg_end, right_foot(8pts)
        limb_start = 52

        def render_limb(start_idx: int, is_leg: bool = False) -> None:
            if start_idx + 10 > len(points):
                return
            # Limb line
            p1 = points[start_idx]
            p2 = points[start_idx + 1]
            line = SVGLine(
                start=(p1[0] + pos[0], p1[1] + pos[1]),
                end=(p2[0] + pos[0], p2[1] + pos[1]),
                stroke=color,
                stroke_width=stroke_width + 2,  # Thicker for chibi style
            )
            group.add(line)
            # Rounded end (hand/foot)
            end_points = points[start_idx + 2 : start_idx + 10]
            if end_points:
                translated_end = [(p[0] + pos[0], p[1] + pos[1]) for p in end_points]
                limb_fill = outfit_color if is_leg else fill_color
                end_shape = Polygon(
                    points=translated_end,
                    fill=limb_fill,
                    stroke=color,
                    stroke_width=stroke_width,
                )
                group.add(end_shape)

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
        self._render_chibi_eyes(group, head_pos, head_radius, eye_y, eye_offset, eye_radius, eye_type, color)

        # Render eyebrows (smaller/cuter for chibi)
        self._render_face_eyebrows(group, head_pos, head_radius, eye_y - eye_radius * 0.8, eye_offset, eyebrow_type, color)

        # Render mouth (small and cute)
        self._render_chibi_mouth(group, head_pos, head_radius, mouth_type, color)

        # Render blush if enabled
        if blush:
            self._render_chibi_blush(group, head_pos, head_radius, eye_y, eye_offset)

    def _render_chibi_hair(
        self, group: Group, head_pos: list[float], head_radius: float, hair_style: str, hair_color: str
    ) -> None:
        """Render chibi hair based on style."""
        cx, cy = head_pos

        if hair_style == "none":
            return

        elif hair_style == "spiky":
            # Spiky anime-style hair with several pointed tufts
            spikes = [
                # (angle, length_multiplier)
                (-0.6, 1.3), (-0.3, 1.4), (0, 1.5), (0.3, 1.4), (0.6, 1.3),
            ]
            for angle, length in spikes:
                import math
                spike_base_x = cx + head_radius * 0.7 * math.sin(angle)
                spike_base_y = cy - head_radius * 0.6
                spike_tip_x = cx + head_radius * length * math.sin(angle)
                spike_tip_y = cy - head_radius * length
                # Draw triangle spike
                spike = Polygon(
                    points=[
                        (spike_base_x - head_radius * 0.15, spike_base_y),
                        (spike_tip_x, spike_tip_y),
                        (spike_base_x + head_radius * 0.15, spike_base_y),
                    ],
                    fill=hair_color,
                    stroke=hair_color,
                    stroke_width=1,
                )
                group.add(spike)

        elif hair_style == "long":
            # Long hair falling down sides
            # Left side
            left_hair = Polygon(
                points=[
                    (cx - head_radius * 0.8, cy - head_radius * 0.3),
                    (cx - head_radius * 1.0, cy + head_radius * 0.8),
                    (cx - head_radius * 0.5, cy + head_radius * 0.6),
                    (cx - head_radius * 0.4, cy),
                ],
                fill=hair_color,
                stroke=hair_color,
                stroke_width=1,
            )
            group.add(left_hair)
            # Right side
            right_hair = Polygon(
                points=[
                    (cx + head_radius * 0.8, cy - head_radius * 0.3),
                    (cx + head_radius * 1.0, cy + head_radius * 0.8),
                    (cx + head_radius * 0.5, cy + head_radius * 0.6),
                    (cx + head_radius * 0.4, cy),
                ],
                fill=hair_color,
                stroke=hair_color,
                stroke_width=1,
            )
            group.add(right_hair)
            # Top bangs
            bangs = Polygon(
                points=[
                    (cx - head_radius * 0.6, cy - head_radius * 0.5),
                    (cx - head_radius * 0.2, cy - head_radius * 0.2),
                    (cx, cy - head_radius * 0.4),
                    (cx + head_radius * 0.2, cy - head_radius * 0.2),
                    (cx + head_radius * 0.6, cy - head_radius * 0.5),
                    (cx, cy - head_radius * 1.1),
                ],
                fill=hair_color,
                stroke=hair_color,
                stroke_width=1,
            )
            group.add(bangs)

        elif hair_style == "short":
            # Simple short hair cap
            hair_cap = Polygon(
                points=[
                    (cx - head_radius * 0.85, cy - head_radius * 0.2),
                    (cx - head_radius * 0.75, cy - head_radius * 0.8),
                    (cx - head_radius * 0.3, cy - head_radius * 1.05),
                    (cx, cy - head_radius * 1.1),
                    (cx + head_radius * 0.3, cy - head_radius * 1.05),
                    (cx + head_radius * 0.75, cy - head_radius * 0.8),
                    (cx + head_radius * 0.85, cy - head_radius * 0.2),
                ],
                fill=hair_color,
                stroke=hair_color,
                stroke_width=1,
            )
            group.add(hair_cap)

        elif hair_style == "twintails":
            # Two pigtails
            # Top hair
            top_hair = Polygon(
                points=[
                    (cx - head_radius * 0.7, cy - head_radius * 0.6),
                    (cx, cy - head_radius * 1.15),
                    (cx + head_radius * 0.7, cy - head_radius * 0.6),
                ],
                fill=hair_color,
                stroke=hair_color,
                stroke_width=1,
            )
            group.add(top_hair)
            # Left twintail
            left_tail = Polygon(
                points=[
                    (cx - head_radius * 0.7, cy - head_radius * 0.4),
                    (cx - head_radius * 1.3, cy + head_radius * 0.3),
                    (cx - head_radius * 1.1, cy + head_radius * 0.8),
                    (cx - head_radius * 0.8, cy + head_radius * 0.4),
                    (cx - head_radius * 0.5, cy),
                ],
                fill=hair_color,
                stroke=hair_color,
                stroke_width=1,
            )
            group.add(left_tail)
            # Right twintail
            right_tail = Polygon(
                points=[
                    (cx + head_radius * 0.7, cy - head_radius * 0.4),
                    (cx + head_radius * 1.3, cy + head_radius * 0.3),
                    (cx + head_radius * 1.1, cy + head_radius * 0.8),
                    (cx + head_radius * 0.8, cy + head_radius * 0.4),
                    (cx + head_radius * 0.5, cy),
                ],
                fill=hair_color,
                stroke=hair_color,
                stroke_width=1,
            )
            group.add(right_tail)

    def _render_chibi_eyes(
        self, group: Group, head_pos: list[float], head_radius: float,
        eye_y: float, eye_offset: float, eye_radius: float, eye_type: str, color: str
    ) -> None:
        """Render large chibi-style eyes with highlights."""
        left_x = head_pos[0] - eye_offset
        right_x = head_pos[0] + eye_offset

        if eye_type == "closed" or eye_type == "curved":
            # Happy closed eyes (^_^)
            for x in [left_x, right_x]:
                # Draw arc-like closed eye
                eye = SVGPath(
                    d=f"M {x - eye_radius} {eye_y} Q {x} {eye_y - eye_radius} {x + eye_radius} {eye_y}",
                    fill="none",
                    stroke=color,
                    stroke_width=2,
                )
                group.add(eye)
        elif eye_type == "stars":
            # Sparkly star eyes
            for x in [left_x, right_x]:
                # Draw star shape
                import math
                star_points = []
                for i in range(10):
                    angle = math.pi / 2 + i * math.pi / 5
                    r = eye_radius if i % 2 == 0 else eye_radius * 0.5
                    star_points.append((x + r * math.cos(angle), eye_y - r * math.sin(angle)))
                star = Polygon(points=star_points, fill="#FFD700", stroke=color, stroke_width=1)
                group.add(star)
        elif eye_type == "tears":
            # Crying eyes with tear drops
            for x in [left_x, right_x]:
                # Large eye circle
                eye = SVGCircle(center=(x, eye_y), r=eye_radius, fill="white", stroke=color, stroke_width=2)
                group.add(eye)
                # Pupil
                pupil = SVGCircle(center=(x, eye_y), r=eye_radius * 0.5, fill=color, stroke="none")
                group.add(pupil)
                # Highlight
                highlight = SVGCircle(center=(x - eye_radius * 0.25, eye_y - eye_radius * 0.25), r=eye_radius * 0.2, fill="white", stroke="none")
                group.add(highlight)
                # Tear drop
                tear = SVGPath(
                    d=f"M {x + eye_radius * 0.3} {eye_y + eye_radius * 0.8} Q {x + eye_radius * 0.5} {eye_y + eye_radius * 1.5} {x + eye_radius * 0.3} {eye_y + eye_radius * 1.8}",
                    fill="#87CEEB",
                    stroke="#87CEEB",
                    stroke_width=3,
                )
                group.add(tear)
        elif eye_type == "wide":
            # Surprised wide eyes
            for x in [left_x, right_x]:
                eye = SVGCircle(center=(x, eye_y), r=eye_radius * 1.2, fill="white", stroke=color, stroke_width=2)
                group.add(eye)
                pupil = SVGCircle(center=(x, eye_y + eye_radius * 0.1), r=eye_radius * 0.4, fill=color, stroke="none")
                group.add(pupil)
                highlight = SVGCircle(center=(x - eye_radius * 0.3, eye_y - eye_radius * 0.3), r=eye_radius * 0.25, fill="white", stroke="none")
                group.add(highlight)
        elif eye_type == "narrow":
            # Angry narrow eyes
            for x in [left_x, right_x]:
                eye = Rect(
                    insert=(x - eye_radius, eye_y - eye_radius * 0.3),
                    size=(eye_radius * 2, eye_radius * 0.6),
                    fill="white",
                    stroke=color,
                    stroke_width=2,
                )
                group.add(eye)
                pupil = SVGCircle(center=(x, eye_y), r=eye_radius * 0.25, fill=color, stroke="none")
                group.add(pupil)
        else:
            # Normal large chibi eyes with shine
            for x in [left_x, right_x]:
                # Large eye oval
                eye = SVGCircle(center=(x, eye_y), r=eye_radius, fill="white", stroke=color, stroke_width=2)
                group.add(eye)
                # Large pupil
                pupil = SVGCircle(center=(x, eye_y + eye_radius * 0.1), r=eye_radius * 0.5, fill=color, stroke="none")
                group.add(pupil)
                # Large highlight (signature chibi shine)
                highlight = SVGCircle(center=(x - eye_radius * 0.25, eye_y - eye_radius * 0.25), r=eye_radius * 0.25, fill="white", stroke="none")
                group.add(highlight)
                # Small secondary highlight
                highlight2 = SVGCircle(center=(x + eye_radius * 0.2, eye_y + eye_radius * 0.1), r=eye_radius * 0.1, fill="white", stroke="none")
                group.add(highlight2)

    def _render_chibi_mouth(
        self, group: Group, head_pos: list[float], head_radius: float, mouth_type: str, color: str
    ) -> None:
        """Render small cute chibi mouth."""
        cx, cy = head_pos
        mouth_y = cy + head_radius * 0.35
        mouth_width = head_radius * 0.25

        if mouth_type == "smile" or mouth_type == "grin":
            # Wide happy smile (cat mouth shape)
            mouth = SVGPath(
                d=f"M {cx - mouth_width} {mouth_y} Q {cx} {mouth_y + mouth_width * 0.8} {cx + mouth_width} {mouth_y}",
                fill="none",
                stroke=color,
                stroke_width=2,
            )
            group.add(mouth)
        elif mouth_type == "open" or mouth_type == "gasp":
            # Open surprised mouth (small circle)
            mouth = SVGCircle(center=(cx, mouth_y), r=mouth_width * 0.6, fill="#FFB6C1", stroke=color, stroke_width=2)
            group.add(mouth)
        elif mouth_type == "frown":
            # Small sad mouth
            mouth = SVGPath(
                d=f"M {cx - mouth_width * 0.6} {mouth_y + mouth_width * 0.3} Q {cx} {mouth_y - mouth_width * 0.3} {cx + mouth_width * 0.6} {mouth_y + mouth_width * 0.3}",
                fill="none",
                stroke=color,
                stroke_width=2,
            )
            group.add(mouth)
        elif mouth_type == "smirk":
            # Asymmetric smirk
            mouth = SVGPath(
                d=f"M {cx - mouth_width * 0.5} {mouth_y} Q {cx} {mouth_y + mouth_width * 0.3} {cx + mouth_width * 0.7} {mouth_y - mouth_width * 0.2}",
                fill="none",
                stroke=color,
                stroke_width=2,
            )
            group.add(mouth)
        elif mouth_type == "wavy":
            # Nervous wavy mouth
            mouth = SVGPath(
                d=f"M {cx - mouth_width * 0.6} {mouth_y} Q {cx - mouth_width * 0.3} {mouth_y - mouth_width * 0.2} {cx} {mouth_y} Q {cx + mouth_width * 0.3} {mouth_y + mouth_width * 0.2} {cx + mouth_width * 0.6} {mouth_y}",
                fill="none",
                stroke=color,
                stroke_width=2,
            )
            group.add(mouth)
        else:
            # Normal small line or dot mouth
            mouth = SVGLine(
                start=(cx - mouth_width * 0.4, mouth_y),
                end=(cx + mouth_width * 0.4, mouth_y),
                stroke=color,
                stroke_width=2,
            )
            group.add(mouth)

    def _render_chibi_blush(
        self, group: Group, head_pos: list[float], head_radius: float, eye_y: float, eye_offset: float
    ) -> None:
        """Render cute blush marks on cheeks."""
        blush_y = eye_y + head_radius * 0.3
        blush_x_offset = eye_offset + head_radius * 0.15

        for x in [head_pos[0] - blush_x_offset, head_pos[0] + blush_x_offset]:
            # Pink oval blush
            blush = SVGCircle(
                center=(x, blush_y),
                r=head_radius * 0.12,
                fill="#FFB6C1",
                stroke="none",
                fill_opacity=0.6,
            )
            group.add(blush)

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

        stroke_style = data.get("stroke_style", "solid")
        if stroke_style == "dashed":
            rect["stroke-dasharray"] = "5,5"
        elif stroke_style == "dotted":
            rect["stroke-dasharray"] = "2,2"

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

        stroke_style = data.get("stroke_style", "solid")
        if stroke_style == "dashed":
            circle["stroke-dasharray"] = "5,5"
        elif stroke_style == "dotted":
            circle["stroke-dasharray"] = "2,2"

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

    def _render_anime(
        self, data: dict[str, Any], group: Group, pos: list[float], points: list[list[float]]
    ) -> None:
        """Render an anime/manga style character.

        Renders a character with typical anime proportions:
        - Tapered face shape with pointed chin
        - Large expressive eyes with highlights
        - Visible neck and shoulders
        - Natural body proportions
        - Various hair styles
        """
        color = data.get("color", "#333333")
        skin_color = data.get("skin_color", "#FFE0C4")
        fill_color = data.get("fill_color", skin_color)
        outfit_color = data.get("outfit_color", "#3B82F6")
        hair_color = data.get("hair_color", "#2D1B12")
        hair_style = data.get("hair_style", "flowing")
        eye_color = data.get("eye_color", "#4A90D9")
        stroke_width = 1.5

        if len(points) < 32:
            return

        height = data.get("character_height", 100)

        # Head points (first 32 points - tapered oval)
        head_points = points[:32]
        translated_head = [(p[0] + pos[0], p[1] + pos[1]) for p in head_points]

        # Calculate head center for features
        head_center_x = sum(p[0] for p in head_points) / len(head_points)
        head_center_y = sum(p[1] for p in head_points) / len(head_points)
        head_pos = [head_center_x + pos[0], head_center_y + pos[1]]
        head_height = height * 0.14
        head_width = height * 0.10

        # Render hair (behind head)
        self._render_anime_hair(group, head_pos, head_height, head_width, hair_style, hair_color)

        # Draw head with skin color
        head = Polygon(
            points=translated_head,
            fill=fill_color,
            stroke=color,
            stroke_width=stroke_width,
        )
        group.add(head)

        # Neck points (next 4 points)
        neck_points = points[32:36]
        if len(neck_points) == 4:
            translated_neck = [(p[0] + pos[0], p[1] + pos[1]) for p in neck_points]
            neck = Polygon(
                points=translated_neck,
                fill=fill_color,
                stroke=color,
                stroke_width=stroke_width,
            )
            group.add(neck)

        # Body/torso points (next 4 points)
        body_points = points[36:40]
        if len(body_points) == 4:
            translated_body = [(p[0] + pos[0], p[1] + pos[1]) for p in body_points]
            body = Polygon(
                points=translated_body,
                fill=outfit_color,
                stroke=color,
                stroke_width=stroke_width,
            )
            group.add(body)

        # Arms and legs - each limb has: start, elbow/knee, end, hand/foot circle (8 points)
        limb_start = 40

        def render_arm(start_idx: int) -> None:
            if start_idx + 11 > len(points):
                return
            # Arm segments
            p1 = points[start_idx]
            p2 = points[start_idx + 1]
            p3 = points[start_idx + 2]

            # Upper arm
            line1 = SVGLine(
                start=(p1[0] + pos[0], p1[1] + pos[1]),
                end=(p2[0] + pos[0], p2[1] + pos[1]),
                stroke=color,
                stroke_width=stroke_width + 1,
            )
            group.add(line1)

            # Forearm
            line2 = SVGLine(
                start=(p2[0] + pos[0], p2[1] + pos[1]),
                end=(p3[0] + pos[0], p3[1] + pos[1]),
                stroke=color,
                stroke_width=stroke_width + 1,
            )
            group.add(line2)

            # Hand circle
            hand_points = points[start_idx + 3 : start_idx + 11]
            if hand_points:
                translated_hand = [(p[0] + pos[0], p[1] + pos[1]) for p in hand_points]
                hand = Polygon(
                    points=translated_hand,
                    fill=fill_color,
                    stroke=color,
                    stroke_width=stroke_width,
                )
                group.add(hand)

        def render_leg(start_idx: int) -> None:
            if start_idx + 11 > len(points):
                return
            # Leg segments
            p1 = points[start_idx]
            p2 = points[start_idx + 1]
            p3 = points[start_idx + 2]

            # Upper leg
            line1 = SVGLine(
                start=(p1[0] + pos[0], p1[1] + pos[1]),
                end=(p2[0] + pos[0], p2[1] + pos[1]),
                stroke=outfit_color,
                stroke_width=stroke_width + 2,
            )
            group.add(line1)

            # Lower leg
            line2 = SVGLine(
                start=(p2[0] + pos[0], p2[1] + pos[1]),
                end=(p3[0] + pos[0], p3[1] + pos[1]),
                stroke=outfit_color,
                stroke_width=stroke_width + 2,
            )
            group.add(line2)

            # Foot oval
            foot_points = points[start_idx + 3 : start_idx + 11]
            if foot_points:
                translated_foot = [(p[0] + pos[0], p[1] + pos[1]) for p in foot_points]
                foot = Polygon(
                    points=translated_foot,
                    fill=outfit_color,
                    stroke=color,
                    stroke_width=stroke_width,
                )
                group.add(foot)

        # Render arms (skin color for hands)
        render_arm(limb_start)  # Left arm
        render_arm(limb_start + 11)  # Right arm

        # Render legs (outfit color)
        render_leg(limb_start + 22)  # Left leg
        render_leg(limb_start + 33)  # Right leg

        # Render face features
        expression = data.get("expression", {})
        eye_type = expression.get("eyes", "normal")
        mouth_type = expression.get("mouth", "normal")
        eyebrow_type = expression.get("eyebrows", "normal")

        # Anime eyes are large and positioned in upper part of face
        eye_y = head_pos[1] - head_height * 0.1
        eye_offset = head_width * 0.45
        eye_radius = head_height * 0.18  # Large anime eyes

        # Render anime-style eyes
        self._render_anime_eyes(group, head_pos, head_height, eye_y, eye_offset, eye_radius, eye_type, eye_color, color)

        # Render eyebrows
        self._render_face_eyebrows(group, head_pos, head_height, eye_y - eye_radius * 0.9, eye_offset, eyebrow_type, color)

        # Render mouth (small anime mouth)
        self._render_anime_mouth(group, head_pos, head_height, mouth_type, color)

        # Render hair in front (bangs)
        self._render_anime_bangs(group, head_pos, head_height, head_width, hair_style, hair_color)

    def _render_anime_hair(
        self, group: Group, head_pos: list[float], head_height: float, head_width: float,
        hair_style: str, hair_color: str
    ) -> None:
        """Render anime hair (back layer behind head)."""
        cx, cy = head_pos
        stroke_width = 1.5

        if hair_style == "none":
            return

        if hair_style == "flowing":
            # Long flowing hair
            hair_points = [
                (cx - head_width * 1.2, cy - head_height * 0.3),
                (cx - head_width * 1.4, cy + head_height * 0.8),
                (cx - head_width * 1.2, cy + head_height * 1.5),
                (cx - head_width * 0.8, cy + head_height * 1.8),
                (cx, cy + head_height * 1.6),
                (cx + head_width * 0.8, cy + head_height * 1.8),
                (cx + head_width * 1.2, cy + head_height * 1.5),
                (cx + head_width * 1.4, cy + head_height * 0.8),
                (cx + head_width * 1.2, cy - head_height * 0.3),
            ]
            hair = Polygon(
                points=hair_points,
                fill=hair_color,
                stroke=hair_color,
                stroke_width=stroke_width,
            )
            group.add(hair)

        elif hair_style == "ponytail":
            # Ponytail at the back
            ponytail_points = [
                (cx + head_width * 0.6, cy - head_height * 0.2),
                (cx + head_width * 1.8, cy),
                (cx + head_width * 2.0, cy + head_height * 0.8),
                (cx + head_width * 1.6, cy + head_height * 1.5),
                (cx + head_width * 1.0, cy + head_height * 1.2),
                (cx + head_width * 0.8, cy + head_height * 0.3),
            ]
            ponytail = Polygon(
                points=ponytail_points,
                fill=hair_color,
                stroke=hair_color,
                stroke_width=stroke_width,
            )
            group.add(ponytail)

        elif hair_style == "twintails":
            # Two side tails
            for side in [-1, 1]:
                tail_points = [
                    (cx + side * head_width * 0.8, cy),
                    (cx + side * head_width * 1.5, cy + head_height * 0.3),
                    (cx + side * head_width * 1.6, cy + head_height * 1.0),
                    (cx + side * head_width * 1.3, cy + head_height * 1.5),
                    (cx + side * head_width * 0.9, cy + head_height * 1.2),
                    (cx + side * head_width * 0.7, cy + head_height * 0.4),
                ]
                tail = Polygon(
                    points=tail_points,
                    fill=hair_color,
                    stroke=hair_color,
                    stroke_width=stroke_width,
                )
                group.add(tail)

        # Hair cap for most styles (short, spiky, bob also get base layer)
        if hair_style in ["short", "spiky", "bob", "flowing", "ponytail", "twintails"]:
            cap_points = [
                (cx - head_width * 1.1, cy - head_height * 0.2),
                (cx - head_width * 0.9, cy - head_height * 0.5),
                (cx, cy - head_height * 0.6),
                (cx + head_width * 0.9, cy - head_height * 0.5),
                (cx + head_width * 1.1, cy - head_height * 0.2),
            ]
            cap = Polygon(
                points=cap_points,
                fill=hair_color,
                stroke=hair_color,
                stroke_width=stroke_width,
            )
            group.add(cap)

    def _render_anime_bangs(
        self, group: Group, head_pos: list[float], head_height: float, head_width: float,
        hair_style: str, hair_color: str
    ) -> None:
        """Render anime hair bangs (front layer)."""
        cx, cy = head_pos
        stroke_width = 1.5

        if hair_style == "none":
            return

        if hair_style == "spiky":
            # Spiky bangs
            spikes = [
                [(cx - head_width * 0.8, cy - head_height * 0.3),
                 (cx - head_width * 0.5, cy - head_height * 0.6),
                 (cx - head_width * 0.3, cy - head_height * 0.25)],
                [(cx - head_width * 0.3, cy - head_height * 0.25),
                 (cx, cy - head_height * 0.7),
                 (cx + head_width * 0.2, cy - head_height * 0.3)],
                [(cx + head_width * 0.2, cy - head_height * 0.3),
                 (cx + head_width * 0.5, cy - head_height * 0.55),
                 (cx + head_width * 0.8, cy - head_height * 0.3)],
            ]
            for spike in spikes:
                bang = Polygon(points=spike, fill=hair_color, stroke=hair_color, stroke_width=stroke_width)
                group.add(bang)

        elif hair_style in ["flowing", "ponytail", "twintails"]:
            # Soft side-swept bangs
            left_bang = [
                (cx - head_width * 0.9, cy - head_height * 0.3),
                (cx - head_width * 0.6, cy - head_height * 0.5),
                (cx - head_width * 0.2, cy - head_height * 0.35),
                (cx - head_width * 0.3, cy - head_height * 0.15),
                (cx - head_width * 0.5, cy - head_height * 0.1),
            ]
            right_bang = [
                (cx + head_width * 0.9, cy - head_height * 0.3),
                (cx + head_width * 0.6, cy - head_height * 0.5),
                (cx + head_width * 0.2, cy - head_height * 0.35),
                (cx + head_width * 0.3, cy - head_height * 0.15),
                (cx + head_width * 0.5, cy - head_height * 0.1),
            ]
            group.add(Polygon(points=left_bang, fill=hair_color, stroke=hair_color, stroke_width=stroke_width))
            group.add(Polygon(points=right_bang, fill=hair_color, stroke=hair_color, stroke_width=stroke_width))

        elif hair_style == "bob":
            # Short bob bangs
            bang = [
                (cx - head_width * 0.8, cy - head_height * 0.25),
                (cx - head_width * 0.4, cy - head_height * 0.4),
                (cx, cy - head_height * 0.45),
                (cx + head_width * 0.4, cy - head_height * 0.4),
                (cx + head_width * 0.8, cy - head_height * 0.25),
                (cx + head_width * 0.6, cy - head_height * 0.1),
                (cx, cy - head_height * 0.2),
                (cx - head_width * 0.6, cy - head_height * 0.1),
            ]
            group.add(Polygon(points=bang, fill=hair_color, stroke=hair_color, stroke_width=stroke_width))

        elif hair_style == "short":
            # Short tousled bangs
            bangs = [
                (cx - head_width * 0.7, cy - head_height * 0.3),
                (cx - head_width * 0.35, cy - head_height * 0.5),
                (cx, cy - head_height * 0.4),
                (cx + head_width * 0.35, cy - head_height * 0.5),
                (cx + head_width * 0.7, cy - head_height * 0.3),
                (cx + head_width * 0.4, cy - head_height * 0.15),
                (cx, cy - head_height * 0.25),
                (cx - head_width * 0.4, cy - head_height * 0.15),
            ]
            group.add(Polygon(points=bangs, fill=hair_color, stroke=hair_color, stroke_width=stroke_width))

    def _render_anime_eyes(
        self, group: Group, head_pos: list[float], head_height: float,
        eye_y: float, eye_offset: float, eye_radius: float,
        eye_type: str, eye_color: str, outline_color: str
    ) -> None:
        """Render anime-style eyes with highlights."""
        left_x = head_pos[0] - eye_offset
        right_x = head_pos[0] + eye_offset

        if eye_type == "curved":
            # Happy curved eyes (^_^)
            curve_width = eye_radius * 1.2
            for x in [left_x, right_x]:
                eye = Polyline(
                    points=[
                        (x - curve_width, eye_y),
                        (x, eye_y - eye_radius * 0.5),
                        (x + curve_width, eye_y),
                    ],
                    fill="none",
                    stroke=outline_color,
                    stroke_width=2,
                    stroke_linecap="round",
                )
                group.add(eye)

        elif eye_type == "closed":
            # Closed/sleepy eyes (horizontal lines)
            for x in [left_x, right_x]:
                eye = SVGLine(
                    start=(x - eye_radius, eye_y),
                    end=(x + eye_radius, eye_y),
                    stroke=outline_color,
                    stroke_width=2,
                    stroke_linecap="round",
                )
                group.add(eye)

        elif eye_type == "stars":
            # Star/sparkle eyes (excited)
            for x in [left_x, right_x]:
                # Outer star shape
                star_size = eye_radius * 0.8
                for angle in [0, 45, 90, 135]:
                    import math
                    rad = math.radians(angle)
                    line = SVGLine(
                        start=(x - star_size * math.cos(rad), eye_y - star_size * math.sin(rad)),
                        end=(x + star_size * math.cos(rad), eye_y + star_size * math.sin(rad)),
                        stroke=eye_color,
                        stroke_width=2,
                    )
                    group.add(line)

        elif eye_type == "tears":
            # Crying eyes with tear drops
            for x in [left_x, right_x]:
                # Eye base
                eye = SVGCircle(
                    center=(x, eye_y),
                    r=eye_radius,
                    fill="white",
                    stroke=outline_color,
                    stroke_width=1.5,
                )
                group.add(eye)
                # Pupil
                pupil = SVGCircle(
                    center=(x, eye_y),
                    r=eye_radius * 0.5,
                    fill=eye_color,
                    stroke="none",
                )
                group.add(pupil)
                # Tear drop
                tear = SVGCircle(
                    center=(x, eye_y + eye_radius * 1.5),
                    r=eye_radius * 0.3,
                    fill="#87CEEB",
                    stroke="none",
                )
                group.add(tear)

        elif eye_type in ["wide", "surprised"]:
            # Wide surprised eyes
            for x in [left_x, right_x]:
                # Larger white of eye
                eye = SVGCircle(
                    center=(x, eye_y),
                    r=eye_radius * 1.2,
                    fill="white",
                    stroke=outline_color,
                    stroke_width=1.5,
                )
                group.add(eye)
                # Smaller pupil (surprised look)
                pupil = SVGCircle(
                    center=(x, eye_y),
                    r=eye_radius * 0.4,
                    fill=eye_color,
                    stroke="none",
                )
                group.add(pupil)
                # Highlight
                highlight = SVGCircle(
                    center=(x - eye_radius * 0.3, eye_y - eye_radius * 0.3),
                    r=eye_radius * 0.2,
                    fill="white",
                    stroke="none",
                )
                group.add(highlight)

        else:
            # Normal anime eyes with highlights
            for x in [left_x, right_x]:
                # White of eye (slightly taller)
                eye_white = SVGCircle(
                    center=(x, eye_y),
                    r=eye_radius,
                    fill="white",
                    stroke=outline_color,
                    stroke_width=1.5,
                )
                group.add(eye_white)

                # Iris/pupil (colored)
                iris = SVGCircle(
                    center=(x, eye_y + eye_radius * 0.1),
                    r=eye_radius * 0.7,
                    fill=eye_color,
                    stroke="none",
                )
                group.add(iris)

                # Inner pupil (dark)
                pupil = SVGCircle(
                    center=(x, eye_y + eye_radius * 0.15),
                    r=eye_radius * 0.35,
                    fill="#1a1a1a",
                    stroke="none",
                )
                group.add(pupil)

                # Large highlight (top-left)
                highlight1 = SVGCircle(
                    center=(x - eye_radius * 0.25, eye_y - eye_radius * 0.2),
                    r=eye_radius * 0.25,
                    fill="white",
                    stroke="none",
                )
                group.add(highlight1)

                # Small highlight (bottom-right)
                highlight2 = SVGCircle(
                    center=(x + eye_radius * 0.2, eye_y + eye_radius * 0.3),
                    r=eye_radius * 0.12,
                    fill="white",
                    stroke="none",
                )
                group.add(highlight2)

    def _render_anime_mouth(
        self, group: Group, head_pos: list[float], head_height: float, mouth_type: str, color: str
    ) -> None:
        """Render anime-style mouth (small and simple)."""
        cx = head_pos[0]
        mouth_y = head_pos[1] + head_height * 0.25
        mouth_width = head_height * 0.12

        if mouth_type == "smile":
            # Small upward curve
            mouth = Polyline(
                points=[
                    (cx - mouth_width, mouth_y),
                    (cx, mouth_y + mouth_width * 0.5),
                    (cx + mouth_width, mouth_y),
                ],
                fill="none",
                stroke=color,
                stroke_width=1.5,
                stroke_linecap="round",
            )
            group.add(mouth)

        elif mouth_type == "frown":
            # Small downward curve
            mouth = Polyline(
                points=[
                    (cx - mouth_width, mouth_y),
                    (cx, mouth_y - mouth_width * 0.5),
                    (cx + mouth_width, mouth_y),
                ],
                fill="none",
                stroke=color,
                stroke_width=1.5,
                stroke_linecap="round",
            )
            group.add(mouth)

        elif mouth_type == "open":
            # Small open mouth (circle)
            mouth = SVGCircle(
                center=(cx, mouth_y),
                r=mouth_width * 0.6,
                fill="#2a1a1a",
                stroke=color,
                stroke_width=1.5,
            )
            group.add(mouth)

        elif mouth_type == "grin":
            # Wide grin with teeth hint
            mouth = Polyline(
                points=[
                    (cx - mouth_width * 1.5, mouth_y),
                    (cx - mouth_width * 0.5, mouth_y + mouth_width * 0.6),
                    (cx + mouth_width * 0.5, mouth_y + mouth_width * 0.6),
                    (cx + mouth_width * 1.5, mouth_y),
                ],
                fill="none",
                stroke=color,
                stroke_width=1.5,
                stroke_linecap="round",
            )
            group.add(mouth)

        elif mouth_type == "gasp":
            # Larger open surprised mouth
            mouth = SVGCircle(
                center=(cx, mouth_y),
                r=mouth_width,
                fill="#2a1a1a",
                stroke=color,
                stroke_width=1.5,
            )
            group.add(mouth)

        elif mouth_type == "wavy":
            # Uncertain wavy line
            mouth = Polyline(
                points=[
                    (cx - mouth_width, mouth_y),
                    (cx - mouth_width * 0.5, mouth_y - mouth_width * 0.3),
                    (cx, mouth_y + mouth_width * 0.2),
                    (cx + mouth_width * 0.5, mouth_y - mouth_width * 0.3),
                    (cx + mouth_width, mouth_y),
                ],
                fill="none",
                stroke=color,
                stroke_width=1.5,
                stroke_linecap="round",
            )
            group.add(mouth)

        elif mouth_type == "smirk":
            # Asymmetric smirk
            mouth = Polyline(
                points=[
                    (cx - mouth_width, mouth_y + mouth_width * 0.2),
                    (cx, mouth_y),
                    (cx + mouth_width, mouth_y - mouth_width * 0.4),
                ],
                fill="none",
                stroke=color,
                stroke_width=1.5,
                stroke_linecap="round",
            )
            group.add(mouth)

        else:
            # Normal small line
            mouth = SVGLine(
                start=(cx - mouth_width * 0.7, mouth_y),
                end=(cx + mouth_width * 0.7, mouth_y),
                stroke=color,
                stroke_width=1.5,
                stroke_linecap="round",
            )
            group.add(mouth)

    def _render_superhero(
        self, data: dict[str, Any], group: Group, pos: list[float], points: list[list[float]]
    ) -> None:
        """Render a superhero character with heroic proportions and costume.

        Renders a muscular character with:
        - Heroic proportions (broad shoulders, narrow waist)
        - Customizable costume with primary/secondary colors
        - Optional cape
        - Mask options (domino, full, cowl, none)
        - Chest emblem (star, diamond, circle, shield, none)
        - Boots and gloves
        """
        color = data.get("color", "#1F2937")
        skin_color = data.get("skin_color", "#FBBF24")
        costume_primary = data.get("costume_primary", "#DC2626")
        costume_secondary = data.get("costume_secondary", "#1D4ED8")
        cape_enabled = data.get("cape", True)
        cape_color = data.get("cape_color", "#DC2626")
        mask = data.get("mask", "domino")
        emblem = data.get("emblem", "star")
        emblem_color = data.get("emblem_color", "#FBBF24")
        boots = data.get("boots", True)
        gloves = data.get("gloves", True)
        stroke_width = 2

        if len(points) < 24:
            return

        height = data.get("character_height", 100)

        # Calculate point indices based on structure
        head_end = 24  # Head points
        neck_end = head_end + 4  # Neck points
        torso_end = neck_end + 8  # Torso points
        # Each arm: shoulder, elbow, hand + 8 fist points = 11 points
        left_arm_end = torso_end + 11
        right_arm_end = left_arm_end + 11
        # Each leg: hip, knee, foot + 8 boot points = 11 points
        left_leg_end = right_arm_end + 11
        right_leg_end = left_leg_end + 11
        # Cape: 6 points if enabled

        # Render cape first (behind character)
        if cape_enabled and len(points) >= right_leg_end + 6:
            cape_points = points[right_leg_end:right_leg_end + 6]
            translated_cape = [(p[0] + pos[0], p[1] + pos[1]) for p in cape_points]
            cape = Polygon(
                points=translated_cape,
                fill=cape_color,
                stroke=color,
                stroke_width=stroke_width,
            )
            group.add(cape)

        # Head points (first 24 points - angular heroic face)
        head_points = points[:head_end]
        translated_head = [(p[0] + pos[0], p[1] + pos[1]) for p in head_points]

        # Calculate head center for features
        head_center_x = sum(p[0] for p in head_points) / len(head_points)
        head_center_y = sum(p[1] for p in head_points) / len(head_points)
        head_pos = [head_center_x + pos[0], head_center_y + pos[1]]
        head_height = height * 0.12
        head_width = height * 0.09

        # Draw head with skin or mask color
        head_fill = skin_color if mask == "none" else skin_color
        if mask == "full":
            head_fill = costume_primary
        head = Polygon(
            points=translated_head,
            fill=head_fill,
            stroke=color,
            stroke_width=stroke_width,
        )
        group.add(head)

        # Neck points
        if len(points) > neck_end:
            neck_points = points[head_end:neck_end]
            translated_neck = [(p[0] + pos[0], p[1] + pos[1]) for p in neck_points]
            neck = Polygon(
                points=translated_neck,
                fill=skin_color,
                stroke=color,
                stroke_width=stroke_width,
            )
            group.add(neck)

        # Torso - heroic V-shape
        if len(points) > torso_end:
            torso_points = points[neck_end:torso_end]
            translated_torso = [(p[0] + pos[0], p[1] + pos[1]) for p in torso_points]
            torso = Polygon(
                points=translated_torso,
                fill=costume_primary,
                stroke=color,
                stroke_width=stroke_width,
            )
            group.add(torso)

            # Render chest emblem
            if emblem != "none":
                torso_center_x = sum(p[0] for p in torso_points) / len(torso_points) + pos[0]
                torso_center_y = sum(p[1] for p in torso_points) / len(torso_points) + pos[1]
                emblem_y = torso_center_y - height * 0.05  # Upper chest
                emblem_size = height * 0.06
                self._render_superhero_emblem(group, torso_center_x, emblem_y, emblem_size, emblem, emblem_color, color)

        # Arms
        def render_arm(start_idx: int, is_left: bool) -> None:
            if start_idx + 11 > len(points):
                return
            # Arm segments
            p1 = points[start_idx]  # Shoulder
            p2 = points[start_idx + 1]  # Elbow
            p3 = points[start_idx + 2]  # Hand

            # Upper arm (shoulder to elbow)
            upper_arm = SVGLine(
                start=(p1[0] + pos[0], p1[1] + pos[1]),
                end=(p2[0] + pos[0], p2[1] + pos[1]),
                stroke=costume_primary,
                stroke_width=stroke_width + 3,
            )
            group.add(upper_arm)

            # Forearm (elbow to hand)
            forearm_color = costume_secondary if gloves else costume_primary
            forearm = SVGLine(
                start=(p2[0] + pos[0], p2[1] + pos[1]),
                end=(p3[0] + pos[0], p3[1] + pos[1]),
                stroke=forearm_color,
                stroke_width=stroke_width + 3,
            )
            group.add(forearm)

            # Fist/hand
            fist_points = points[start_idx + 3:start_idx + 11]
            if fist_points:
                translated_fist = [(p[0] + pos[0], p[1] + pos[1]) for p in fist_points]
                fist_fill = costume_secondary if gloves else skin_color
                fist = Polygon(
                    points=translated_fist,
                    fill=fist_fill,
                    stroke=color,
                    stroke_width=stroke_width,
                )
                group.add(fist)

        # Render arms
        render_arm(torso_end, is_left=True)  # Left arm
        render_arm(left_arm_end, is_left=False)  # Right arm

        # Legs
        def render_leg(start_idx: int) -> None:
            if start_idx + 11 > len(points):
                return
            # Leg segments
            p1 = points[start_idx]  # Hip
            p2 = points[start_idx + 1]  # Knee
            p3 = points[start_idx + 2]  # Foot

            # Upper leg (hip to knee)
            upper_leg = SVGLine(
                start=(p1[0] + pos[0], p1[1] + pos[1]),
                end=(p2[0] + pos[0], p2[1] + pos[1]),
                stroke=costume_secondary,
                stroke_width=stroke_width + 4,
            )
            group.add(upper_leg)

            # Lower leg (knee to foot)
            lower_color = costume_primary if boots else costume_secondary
            lower_leg = SVGLine(
                start=(p2[0] + pos[0], p2[1] + pos[1]),
                end=(p3[0] + pos[0], p3[1] + pos[1]),
                stroke=lower_color,
                stroke_width=stroke_width + 4,
            )
            group.add(lower_leg)

            # Boot/foot
            foot_points = points[start_idx + 3:start_idx + 11]
            if foot_points:
                translated_foot = [(p[0] + pos[0], p[1] + pos[1]) for p in foot_points]
                foot_fill = costume_primary if boots else costume_secondary
                foot = Polygon(
                    points=translated_foot,
                    fill=foot_fill,
                    stroke=color,
                    stroke_width=stroke_width,
                )
                group.add(foot)

        # Render legs
        render_leg(right_arm_end)  # Left leg
        render_leg(left_leg_end)  # Right leg

        # Render face features
        expression = data.get("expression", {})
        eye_type = expression.get("eyes", "normal")
        mouth_type = expression.get("mouth", "normal")
        eyebrow_type = expression.get("eyebrows", "normal")

        # Eye parameters
        eye_y = head_pos[1] - head_height * 0.1
        eye_offset = head_width * 0.4
        eye_radius = head_height * 0.12

        # Render mask first if applicable
        if mask == "domino":
            self._render_superhero_domino_mask(group, head_pos, head_width, eye_y, costume_primary, color)
        elif mask == "cowl":
            self._render_superhero_cowl(group, head_pos, head_height, head_width, costume_primary, color)

        # Render eyes (on top of mask)
        if mask != "full":
            self._render_face_eyes(group, head_pos, head_height, eye_y, eye_offset, eye_radius, eye_type, color)
            self._render_face_eyebrows(group, head_pos, head_height, eye_y - eye_radius, eye_offset, eyebrow_type, color)
            self._render_face_mouth(group, head_pos, head_height, mouth_type, color)

    def _render_superhero_emblem(
        self, group: Group, cx: float, cy: float, size: float,
        emblem_type: str, emblem_color: str, outline_color: str
    ) -> None:
        """Render chest emblem based on type."""
        if emblem_type == "star":
            # 5-pointed star
            import math
            star_points = []
            for i in range(10):
                angle = math.radians(-90 + i * 36)
                r = size if i % 2 == 0 else size * 0.4
                star_points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
            star = Polygon(
                points=star_points,
                fill=emblem_color,
                stroke=outline_color,
                stroke_width=1,
            )
            group.add(star)

        elif emblem_type == "diamond":
            # Diamond shape
            diamond_points = [
                (cx, cy - size),
                (cx + size * 0.7, cy),
                (cx, cy + size),
                (cx - size * 0.7, cy),
            ]
            diamond = Polygon(
                points=diamond_points,
                fill=emblem_color,
                stroke=outline_color,
                stroke_width=1,
            )
            group.add(diamond)

        elif emblem_type == "circle":
            # Circle emblem
            circle = SVGCircle(
                center=(cx, cy),
                r=size,
                fill=emblem_color,
                stroke=outline_color,
                stroke_width=1,
            )
            group.add(circle)

        elif emblem_type == "shield":
            # Shield shape
            shield_points = [
                (cx - size * 0.8, cy - size),
                (cx + size * 0.8, cy - size),
                (cx + size * 0.8, cy + size * 0.3),
                (cx, cy + size),
                (cx - size * 0.8, cy + size * 0.3),
            ]
            shield = Polygon(
                points=shield_points,
                fill=emblem_color,
                stroke=outline_color,
                stroke_width=1,
            )
            group.add(shield)

    def _render_superhero_domino_mask(
        self, group: Group, head_pos: list[float], head_width: float,
        eye_y: float, mask_color: str, outline_color: str
    ) -> None:
        """Render a domino mask (eye mask)."""
        cx, cy = head_pos
        mask_height = head_width * 0.35
        mask_width = head_width * 1.5

        # Domino mask shape (covering eyes area)
        mask_points = [
            (cx - mask_width, eye_y - mask_height * 0.3),
            (cx - mask_width * 0.6, eye_y - mask_height),
            (cx, eye_y - mask_height * 0.8),
            (cx + mask_width * 0.6, eye_y - mask_height),
            (cx + mask_width, eye_y - mask_height * 0.3),
            (cx + mask_width * 0.8, eye_y + mask_height * 0.6),
            (cx, eye_y + mask_height * 0.4),
            (cx - mask_width * 0.8, eye_y + mask_height * 0.6),
        ]
        mask = Polygon(
            points=mask_points,
            fill=mask_color,
            stroke=outline_color,
            stroke_width=1.5,
        )
        group.add(mask)

    def _render_superhero_cowl(
        self, group: Group, head_pos: list[float], head_height: float,
        head_width: float, cowl_color: str, outline_color: str
    ) -> None:
        """Render a cowl (head covering with face opening)."""
        cx, cy = head_pos

        # Cowl covers top and sides of head
        cowl_points = [
            (cx - head_width * 1.1, cy + head_height * 0.1),
            (cx - head_width * 1.2, cy - head_height * 0.3),
            (cx - head_width * 0.8, cy - head_height * 0.6),
            (cx, cy - head_height * 0.7),
            (cx + head_width * 0.8, cy - head_height * 0.6),
            (cx + head_width * 1.2, cy - head_height * 0.3),
            (cx + head_width * 1.1, cy + head_height * 0.1),
            (cx + head_width * 0.6, cy - head_height * 0.1),
            (cx, cy - head_height * 0.15),
            (cx - head_width * 0.6, cy - head_height * 0.1),
        ]
        cowl = Polygon(
            points=cowl_points,
            fill=cowl_color,
            stroke=outline_color,
            stroke_width=1.5,
        )
        group.add(cowl)

    def _render_cartoon(
        self, data: dict[str, Any], group: Group, pos: list[float], points: list[list[float]]
    ) -> None:
        """Render a classic Western cartoon character.

        Renders a character with cartoon aesthetics:
        - Large round head with exaggerated features
        - Pear/bean/round body shape
        - Big expressive eyes with thick outlines
        - Mitten-style hands (optional white gloves)
        - Bold thick outlines characteristic of classic animation
        """
        outline_color = data.get("outline_color", "#000000")
        skin_color = data.get("skin_color", "#FFDAB9")
        fill_color = data.get("fill_color", skin_color)
        outfit_color = data.get("outfit_color", "#4169E1")
        has_gloves = data.get("gloves", True)
        glove_color = "#FFFFFF" if has_gloves else fill_color
        stroke_width = 3  # Thick cartoon outlines

        if len(points) < 32:
            return

        height = data.get("character_height", 100)

        # Head points (first 32 points - large circle)
        head_points = points[:32]
        translated_head = [(p[0] + pos[0], p[1] + pos[1]) for p in head_points]

        # Calculate head center for features
        head_center_x = sum(p[0] for p in head_points) / len(head_points)
        head_center_y = sum(p[1] for p in head_points) / len(head_points)
        head_pos = [head_center_x + pos[0], head_center_y + pos[1]]
        head_radius = height * 0.175  # 35% diameter

        # Draw head with skin color
        head = Polygon(
            points=translated_head,
            fill=fill_color,
            stroke=outline_color,
            stroke_width=stroke_width,
        )
        group.add(head)

        # Render cartoon face features
        expression = data.get("expression", {})
        self._render_cartoon_face(
            group, head_pos, head_radius, expression,
            outline_color, fill_color
        )

        # Body points (next 20 points)
        body_start = 32
        body_end = body_start + 20
        if len(points) >= body_end:
            body_points = points[body_start:body_end]
            translated_body = [(p[0] + pos[0], p[1] + pos[1]) for p in body_points]
            body = Polygon(
                points=translated_body,
                fill=outfit_color,
                stroke=outline_color,
                stroke_width=stroke_width,
            )
            group.add(body)

        # Arms and hands
        # Left arm: 3 position points + 10 hand points = 13 points starting at 52
        arm_start = 52
        self._render_cartoon_limb(
            group, points, pos, arm_start, 13, 10,
            fill_color, glove_color, outline_color, stroke_width
        )

        # Right arm: 3 position points + 10 hand points = 13 points starting at 65
        arm_start_right = 65
        self._render_cartoon_limb(
            group, points, pos, arm_start_right, 13, 10,
            fill_color, glove_color, outline_color, stroke_width
        )

        # Legs and feet
        # Left leg: 3 position points + 8 foot points = 11 points starting at 78
        leg_start = 78
        self._render_cartoon_limb(
            group, points, pos, leg_start, 11, 8,
            outfit_color, outline_color, outline_color, stroke_width
        )

        # Right leg: 3 position points + 8 foot points = 11 points starting at 89
        leg_start_right = 89
        self._render_cartoon_limb(
            group, points, pos, leg_start_right, 11, 8,
            outfit_color, outline_color, outline_color, stroke_width
        )

    def _render_cartoon_face(
        self, group: Group, head_pos: list[float], head_radius: float,
        expression: dict[str, str], outline_color: str, fill_color: str
    ) -> None:
        """Render cartoon face features - big eyes, simple nose, expressive mouth."""
        cx, cy = head_pos
        eye_type = expression.get("eyes", "normal")
        mouth_type = expression.get("mouth", "normal")
        eyebrow_type = expression.get("eyebrows", "normal")

        # Cartoon eyes are bigger and more expressive
        eye_y = cy - head_radius * 0.1
        eye_offset = head_radius * 0.35
        eye_radius = head_radius * 0.18  # Bigger eyes for cartoon

        # Render eyes using the shared face feature methods
        self._render_face_eyes(
            group, head_pos, head_radius, eye_y, eye_offset,
            eye_radius, eye_type, outline_color
        )

        # Render eyebrows
        self._render_face_eyebrows(
            group, head_pos, head_radius, eye_y, eye_offset,
            eyebrow_type, outline_color
        )

        # Render mouth
        self._render_face_mouth(
            group, head_pos, head_radius, mouth_type, outline_color
        )

        # Add cartoon nose (simple round dot or triangle)
        nose_y = cy + head_radius * 0.1
        nose_radius = head_radius * 0.08
        nose = SVGCircle(
            center=(cx, nose_y),
            r=nose_radius,
            fill=outline_color,
            stroke="none",
        )
        group.add(nose)

    def _render_cartoon_limb(
        self, group: Group, points: list[list[float]], pos: list[float],
        start_idx: int, total_points: int, end_points: int,
        limb_color: str, end_color: str, outline_color: str, stroke_width: float
    ) -> None:
        """Render a cartoon limb (arm or leg) with rounded end (hand or foot)."""
        if start_idx + total_points > len(points):
            return

        # Draw limb segments (first 3 points: shoulder/hip, elbow/knee, hand/foot position)
        segment_points = 3
        for i in range(segment_points - 1):
            if start_idx + i + 1 < len(points):
                p1 = points[start_idx + i]
                p2 = points[start_idx + i + 1]
                line = SVGLine(
                    start=(p1[0] + pos[0], p1[1] + pos[1]),
                    end=(p2[0] + pos[0], p2[1] + pos[1]),
                    stroke=limb_color,
                    stroke_width=stroke_width + 2,  # Thicker limbs for cartoon
                )
                group.add(line)
                # Add outline
                outline_line = SVGLine(
                    start=(p1[0] + pos[0], p1[1] + pos[1]),
                    end=(p2[0] + pos[0], p2[1] + pos[1]),
                    stroke=outline_color,
                    stroke_width=stroke_width,
                )
                group.add(outline_line)

        # Draw rounded end (hand/foot) from remaining points
        end_start = start_idx + segment_points
        if end_start + end_points <= len(points):
            end_pts = points[end_start:end_start + end_points]
            translated_end = [(p[0] + pos[0], p[1] + pos[1]) for p in end_pts]
            end_shape = Polygon(
                points=translated_end,
                fill=end_color,
                stroke=outline_color,
                stroke_width=stroke_width,
            )
            group.add(end_shape)
