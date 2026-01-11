"""SVG Renderer - renders comic pages to SVG format."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

import svgwrite
from svgwrite import Drawing
from svgwrite.container import Group
from svgwrite.shapes import Circle as SVGCircle
from svgwrite.shapes import Line as SVGLine
from svgwrite.shapes import Polygon, Polyline, Rect
from svgwrite.text import Text as SVGText

if TYPE_CHECKING:
    from comix.page.page import Page


class SVGRenderer:
    """Renders a Page to SVG format."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self._dwg: Drawing | None = None

    def render(self, output_path: str) -> str:
        """Render the page to an SVG file.

        Args:
            output_path: Path to save the SVG file.

        Returns:
            Path to the rendered file.
        """
        self._dwg = svgwrite.Drawing(
            output_path,
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

        sorted_objects = sorted(
            self.page._cobjects, key=lambda obj: obj.z_index
        )

        for cobject in sorted_objects:
            self._render_cobject(cobject)

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        self._dwg.save()

        return output_path

    def _render_cobject(self, cobject: Any, parent_group: Group | None = None) -> None:
        """Render a CObject and its children."""
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
        else:
            self._render_generic(data, group)

        for child in cobject.submobjects:
            self._render_cobject(child, group)

        if parent_group is not None:
            parent_group.add(group)
        else:
            self._dwg.add(group)

    def _render_panel(self, data: dict, group: Group) -> None:
        """Render a panel."""
        pos = data.get("position", [0, 0])
        width = data.get("width", 100)
        height = data.get("height", 100)
        border = data.get("border", {})

        x = pos[0] - width / 2
        y = pos[1] - height / 2

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

    def _render_bubble(self, data: dict, group: Group) -> None:
        """Render a speech bubble."""
        pos = data.get("position", [0, 0])
        points = data.get("points", [])
        tail_points = data.get("tail_points", [])

        if points:
            translated_points = [
                (p[0] + pos[0], p[1] + pos[1]) for p in points
            ]

            stroke_dasharray = None
            if data.get("border_style") == "dashed":
                stroke_dasharray = "5,5"
            elif data.get("border_style") == "dotted":
                stroke_dasharray = "2,2"

            bubble_path = Polygon(
                points=translated_points,
                fill=data.get("fill_color", "#FFFFFF"),
                stroke=data.get("border_color", "#000000"),
                stroke_width=data.get("border_width", 2),
            )
            if stroke_dasharray:
                bubble_path["stroke-dasharray"] = stroke_dasharray

            group.add(bubble_path)

        if tail_points and len(tail_points) >= 3:
            translated_tail = [
                (p[0] + pos[0], p[1] + pos[1]) for p in tail_points
            ]
            tail = Polygon(
                points=translated_tail,
                fill=data.get("fill_color", "#FFFFFF"),
                stroke=data.get("border_color", "#000000"),
                stroke_width=data.get("border_width", 2),
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

    def _render_text(self, data: dict, group: Group) -> None:
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

    def _render_character(self, data: dict, group: Group) -> None:
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
        self, data: dict, group: Group, pos: list, points: list
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

    def _render_simple_face(self, data: dict, group: Group, pos: list) -> None:
        """Render a simple face character."""
        radius = data.get("face_radius", 30)
        color = data.get("color", "#000000")
        fill = data.get("fill_color") or "#FFEB3B"

        face = SVGCircle(
            center=(pos[0], pos[1]),
            r=radius,
            fill=fill,
            stroke=color,
            stroke_width=2,
        )
        group.add(face)

        eye_y = pos[1] - radius * 0.2
        eye_offset = radius * 0.3
        eye_radius = radius * 0.1

        left_eye = SVGCircle(
            center=(pos[0] - eye_offset, eye_y),
            r=eye_radius,
            fill=color,
        )
        right_eye = SVGCircle(
            center=(pos[0] + eye_offset, eye_y),
            r=eye_radius,
            fill=color,
        )
        group.add(left_eye)
        group.add(right_eye)

        expression = data.get("expression", {})
        mouth_type = expression.get("mouth", "normal")

        if mouth_type in ("smile", "happy"):
            mouth_y = pos[1] + radius * 0.3
            mouth_width = radius * 0.4
            mouth = Polyline(
                points=[
                    (pos[0] - mouth_width, mouth_y - 5),
                    (pos[0], mouth_y + 5),
                    (pos[0] + mouth_width, mouth_y - 5),
                ],
                fill="none",
                stroke=color,
                stroke_width=2,
            )
            group.add(mouth)
        else:
            mouth_y = pos[1] + radius * 0.3
            mouth = SVGLine(
                start=(pos[0] - radius * 0.3, mouth_y),
                end=(pos[0] + radius * 0.3, mouth_y),
                stroke=color,
                stroke_width=2,
            )
            group.add(mouth)

    def _render_rectangle(self, data: dict, group: Group) -> None:
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

    def _render_circle(self, data: dict, group: Group) -> None:
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

    def _render_line(self, data: dict, group: Group) -> None:
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

    def _render_generic(self, data: dict, group: Group) -> None:
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
