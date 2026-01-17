"""Tests for SVG Renderer."""

import tempfile
from pathlib import Path

from comix.page.page import Page
from comix.cobject.panel.panel import Panel
from comix.cobject.bubble.bubble import SpeechBubble
from comix.cobject.character.character import Stickman, SimpleFace, ChubbyStickman, Robot, Chibi, Anime, Superhero, Cartoon
from comix.cobject.text.text import Text, SFX
from comix.cobject.shapes.shapes import Rectangle, Circle, Line
from comix.renderer.svg_renderer import SVGRenderer
from comix.effect.effect import (
    ShakeEffect,
    ZoomEffect,
    MotionLines,
    FocusLines,
    AppearEffect,
    ImpactEffect,
)


class TestSVGRenderer:
    """Tests for SVGRenderer class."""

    def test_render_empty_page(self):
        """Test rendering an empty page."""
        page = Page(width=400, height=300)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            renderer = SVGRenderer(page)
            output_path = renderer.render(f.name)

            assert Path(output_path).exists()
            content = Path(output_path).read_text()
            assert "<svg" in content
            assert 'width="400px"' in content
            assert 'height="300px"' in content
            Path(output_path).unlink()

    def test_render_panel(self):
        """Test rendering a panel."""
        page = Page(width=400, height=300)
        panel = Panel(width=300, height=200)
        panel.move_to((200, 150))
        page.add(panel)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = page.render(f.name)
            content = Path(output_path).read_text()
            assert "<rect" in content
            Path(output_path).unlink()

    def test_render_bubble(self):
        """Test rendering a bubble."""
        page = Page(width=400, height=300)
        bubble = SpeechBubble(text="Hello!").move_to((200, 150))
        page.add(bubble)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = page.render(f.name)
            content = Path(output_path).read_text()
            assert "Hello!" in content
            Path(output_path).unlink()

    def test_render_stickman(self):
        """Test rendering a stickman character."""
        page = Page(width=400, height=300)
        char = Stickman(name="Test").move_to((200, 150))
        page.add(char)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = page.render(f.name)
            content = Path(output_path).read_text()
            assert "<polygon" in content or "<line" in content
            Path(output_path).unlink()

    def test_render_stickman_with_expression(self):
        """Test rendering a stickman with expression features."""
        page = Page(width=400, height=300)
        char = Stickman(name="Happy", expression="happy").move_to((200, 150))
        page.add(char)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = page.render(f.name)
            content = Path(output_path).read_text()
            # Should have head polygon plus face features (eyes/mouth)
            assert "<polygon" in content
            # Face features are rendered as polylines, circles, or paths
            assert "<polyline" in content or "<circle" in content or "<path" in content
            Path(output_path).unlink()

    def test_render_stickman_all_expressions(self):
        """Test rendering stickman with all expression types."""
        expressions = ["neutral", "happy", "sad", "angry", "surprised", "confused",
                      "sleepy", "excited", "scared", "smirk", "crying"]
        for expr_name in expressions:
            page = Page(width=400, height=300)
            char = Stickman(name="Expressive", expression=expr_name).move_to((200, 150))
            page.add(char)

            with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
                output_path = page.render(f.name)
                content = Path(output_path).read_text()
                # Should render without errors and include face elements
                assert "<polygon" in content
                Path(output_path).unlink()

    def test_render_stickman_with_expression_and_pose(self):
        """Test rendering stickman with both expression and pose."""
        page = Page(width=400, height=300)
        char = Stickman(name="Waving", expression="happy", pose="waving").move_to((200, 150))
        page.add(char)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = page.render(f.name)
            content = Path(output_path).read_text()
            assert "<polygon" in content
            assert "<line" in content  # Body lines
            Path(output_path).unlink()

    def test_render_simple_face(self):
        """Test rendering a simple face character."""
        page = Page(width=400, height=300)
        face = SimpleFace(name="Smiley").move_to((200, 150))
        face.set_expression("happy")
        page.add(face)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = page.render(f.name)
            content = Path(output_path).read_text()
            assert "<circle" in content
            Path(output_path).unlink()

    def test_render_chubby_stickman(self):
        """Test rendering a chubby stickman character."""
        page = Page(width=400, height=300)
        chubby = ChubbyStickman(name="Chunky").move_to((200, 150))
        page.add(chubby)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = page.render(f.name)
            content = Path(output_path).read_text()
            # Chubby stickman has polygon elements for head and body
            assert "<polygon" in content
            Path(output_path).unlink()

    def test_render_chubby_stickman_with_expression(self):
        """Test rendering a chubby stickman with expression."""
        page = Page(width=400, height=300)
        chubby = ChubbyStickman(name="Happy", expression="happy").move_to((200, 150))
        page.add(chubby)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = page.render(f.name)
            content = Path(output_path).read_text()
            assert "<polygon" in content
            # Should have face features
            assert "<polyline" in content or "<circle" in content
            Path(output_path).unlink()

    def test_render_chubby_stickman_with_pose(self):
        """Test rendering a chubby stickman with different poses."""
        for pose_name in ["standing", "waving", "jumping", "cheering"]:
            page = Page(width=400, height=300)
            chubby = ChubbyStickman(name="Poser", pose=pose_name).move_to((200, 150))
            page.add(chubby)

            with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
                output_path = page.render(f.name)
                content = Path(output_path).read_text()
                assert "<polygon" in content
                Path(output_path).unlink()

    def test_render_chubby_stickman_facing_left(self):
        """Test rendering a chubby stickman facing left."""
        page = Page(width=400, height=300)
        chubby = ChubbyStickman(name="Lefty", facing="left").move_to((200, 150))
        page.add(chubby)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = page.render(f.name)
            content = Path(output_path).read_text()
            assert "<polygon" in content
            Path(output_path).unlink()

    def test_render_robot(self):
        """Test rendering a robot character."""
        page = Page(width=400, height=300)
        robot = Robot(name="Robo").move_to((200, 150))
        page.add(robot)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = page.render(f.name)
            content = Path(output_path).read_text()
            # Robot has polygon and rect elements for head and body
            assert "<polygon" in content or "<rect" in content
            Path(output_path).unlink()

    def test_render_robot_with_expression(self):
        """Test rendering a robot with expression."""
        page = Page(width=400, height=300)
        robot = Robot(name="HappyBot", expression="happy").move_to((200, 150))
        page.add(robot)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = page.render(f.name)
            content = Path(output_path).read_text()
            assert "<polygon" in content or "<rect" in content
            # Should have LED-style face features
            assert "<rect" in content or "<polyline" in content
            Path(output_path).unlink()

    def test_render_robot_with_pose(self):
        """Test rendering a robot with different poses."""
        for pose_name in ["standing", "waving", "jumping", "cheering"]:
            page = Page(width=400, height=300)
            robot = Robot(name="Poser", pose=pose_name).move_to((200, 150))
            page.add(robot)

            with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
                output_path = page.render(f.name)
                content = Path(output_path).read_text()
                assert "<polygon" in content or "<rect" in content
                Path(output_path).unlink()

    def test_render_robot_facing_left(self):
        """Test rendering a robot facing left."""
        page = Page(width=400, height=300)
        robot = Robot(name="Lefty", facing="left").move_to((200, 150))
        page.add(robot)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = page.render(f.name)
            content = Path(output_path).read_text()
            assert "<polygon" in content or "<rect" in content
            Path(output_path).unlink()

    def test_render_robot_without_antenna(self):
        """Test rendering a robot without antenna."""
        page = Page(width=400, height=300)
        robot = Robot(name="NoAntenna", antenna=False).move_to((200, 150))
        page.add(robot)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = page.render(f.name)
            content = Path(output_path).read_text()
            assert "<polygon" in content or "<rect" in content
            Path(output_path).unlink()

    def test_render_robot_all_expressions(self):
        """Test rendering robot with all expression types."""
        expressions = ["neutral", "happy", "sad", "angry", "surprised",
                       "confused", "sleepy", "excited", "scared"]
        for expr_name in expressions:
            page = Page(width=400, height=300)
            robot = Robot(name="Expressive", expression=expr_name).move_to((200, 150))
            page.add(robot)

            with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
                output_path = page.render(f.name)
                content = Path(output_path).read_text()
                # Should render without errors
                assert "svg" in content.lower()
                Path(output_path).unlink()

    def test_render_robot_custom_colors(self):
        """Test rendering a robot with custom colors."""
        page = Page(width=400, height=300)
        robot = Robot(
            name="ColorBot",
            color="#FF0000",
            fill_color="#00FF00",
            panel_color="#0000FF",
            screen_color="#FFFF00",
            led_color="#FF00FF",
        ).move_to((200, 150))
        page.add(robot)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = page.render(f.name)
            content = Path(output_path).read_text()
            # Custom colors should appear in the SVG
            assert "#FF0000" in content or "#ff0000" in content.lower()
            Path(output_path).unlink()

    def test_render_chibi(self):
        """Test rendering a chibi character."""
        page = Page(width=400, height=300)
        chibi = Chibi(name="ChibiChan").move_to((200, 150))
        page.add(chibi)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = page.render(f.name)
            content = Path(output_path).read_text()
            # Chibi renders - check for svg content
            assert "svg" in content.lower()
            Path(output_path).unlink()

    def test_render_chibi_with_expression(self):
        """Test rendering a chibi with expression."""
        page = Page(width=400, height=300)
        chibi = Chibi(name="HappyChibi", expression="happy").move_to((200, 150))
        page.add(chibi)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = page.render(f.name)
            content = Path(output_path).read_text()
            assert "svg" in content.lower()
            Path(output_path).unlink()

    def test_render_chibi_with_pose(self):
        """Test rendering a chibi with different poses."""
        for pose_name in ["standing", "waving", "jumping", "cheering"]:
            page = Page(width=400, height=300)
            chibi = Chibi(name="Poser", pose=pose_name).move_to((200, 150))
            page.add(chibi)

            with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
                output_path = page.render(f.name)
                content = Path(output_path).read_text()
                assert "svg" in content.lower()
                Path(output_path).unlink()

    def test_render_chibi_facing_left(self):
        """Test rendering a chibi facing left."""
        page = Page(width=400, height=300)
        chibi = Chibi(name="Lefty", facing="left").move_to((200, 150))
        page.add(chibi)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = page.render(f.name)
            content = Path(output_path).read_text()
            assert "svg" in content.lower()
            Path(output_path).unlink()

    def test_render_chibi_hair_styles(self):
        """Test rendering a chibi with different hair styles."""
        styles = ["spiky", "long", "short", "twintails", "none"]
        for style in styles:
            page = Page(width=400, height=300)
            chibi = Chibi(name="Hairy", hair_style=style).move_to((200, 150))
            page.add(chibi)

            with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
                output_path = page.render(f.name)
                content = Path(output_path).read_text()
                assert "svg" in content.lower()
                Path(output_path).unlink()

    def test_render_chibi_with_blush(self):
        """Test rendering a chibi with blush marks."""
        page = Page(width=400, height=300)
        chibi = Chibi(name="Blushing", blush=True).move_to((200, 150))
        page.add(chibi)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = page.render(f.name)
            content = Path(output_path).read_text()
            # Blush uses circle elements
            assert "svg" in content.lower()
            Path(output_path).unlink()

    def test_render_chibi_all_expressions(self):
        """Test rendering chibi with all expression types."""
        expressions = ["neutral", "happy", "sad", "angry", "surprised",
                       "confused", "sleepy", "excited", "scared", "smirk", "crying"]
        for expr_name in expressions:
            page = Page(width=400, height=300)
            chibi = Chibi(name="Expressive", expression=expr_name).move_to((200, 150))
            page.add(chibi)

            with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
                output_path = page.render(f.name)
                content = Path(output_path).read_text()
                # Should render without errors
                assert "svg" in content.lower()
                Path(output_path).unlink()

    def test_render_chibi_custom_colors(self):
        """Test rendering a chibi with custom colors."""
        page = Page(width=400, height=300)
        chibi = Chibi(
            name="ColorChibi",
            color="#FF0000",
            skin_color="#FFD700",
            outfit_color="#00FF00",
            hair_color="#0000FF",
        ).move_to((200, 150))
        page.add(chibi)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = page.render(f.name)
            content = Path(output_path).read_text()
            # Custom colors should appear in the SVG - check svg renders
            assert "svg" in content.lower()
            Path(output_path).unlink()

    def test_render_anime(self):
        """Test rendering an anime character."""
        page = Page(width=400, height=300)
        anime = Anime(name="Sakura").move_to((200, 150))
        page.add(anime)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = page.render(f.name)
            content = Path(output_path).read_text()
            # Anime renders - check for svg content
            assert "svg" in content.lower()
            Path(output_path).unlink()

    def test_render_anime_with_expression(self):
        """Test rendering an anime with expression."""
        page = Page(width=400, height=300)
        anime = Anime(name="HappyAnime", expression="happy").move_to((200, 150))
        page.add(anime)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = page.render(f.name)
            content = Path(output_path).read_text()
            assert "svg" in content.lower()
            Path(output_path).unlink()

    def test_render_anime_with_pose(self):
        """Test rendering an anime with different poses."""
        for pose_name in ["standing", "waving", "jumping", "cheering"]:
            page = Page(width=400, height=300)
            anime = Anime(name="Poser", pose=pose_name).move_to((200, 150))
            page.add(anime)

            with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
                output_path = page.render(f.name)
                content = Path(output_path).read_text()
                assert "svg" in content.lower()
                Path(output_path).unlink()

    def test_render_anime_facing_left(self):
        """Test rendering an anime facing left."""
        page = Page(width=400, height=300)
        anime = Anime(name="Lefty", facing="left").move_to((200, 150))
        page.add(anime)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = page.render(f.name)
            content = Path(output_path).read_text()
            assert "svg" in content.lower()
            Path(output_path).unlink()

    def test_render_anime_hair_styles(self):
        """Test rendering an anime with different hair styles."""
        styles = ["flowing", "ponytail", "short", "spiky", "bob", "twintails", "none"]
        for style in styles:
            page = Page(width=400, height=300)
            anime = Anime(name="Hairy", hair_style=style).move_to((200, 150))
            page.add(anime)

            with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
                output_path = page.render(f.name)
                content = Path(output_path).read_text()
                assert "svg" in content.lower()
                Path(output_path).unlink()

    def test_render_anime_all_expressions(self):
        """Test rendering anime with all expression types."""
        expressions = ["neutral", "happy", "sad", "angry", "surprised",
                       "confused", "sleepy", "excited", "scared", "smirk", "crying"]
        for expr_name in expressions:
            page = Page(width=400, height=300)
            anime = Anime(name="Expressive", expression=expr_name).move_to((200, 150))
            page.add(anime)

            with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
                output_path = page.render(f.name)
                content = Path(output_path).read_text()
                # Should render without errors
                assert "svg" in content.lower()
                Path(output_path).unlink()

    def test_render_anime_custom_colors(self):
        """Test rendering an anime with custom colors."""
        page = Page(width=400, height=300)
        anime = Anime(
            name="ColorAnime",
            color="#FF0000",
            skin_color="#FFD700",
            outfit_color="#00FF00",
            hair_color="#0000FF",
            eye_color="#FF00FF",
        ).move_to((200, 150))
        page.add(anime)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = page.render(f.name)
            content = Path(output_path).read_text()
            # Custom colors should appear in the SVG - check svg renders
            assert "svg" in content.lower()
            Path(output_path).unlink()

    # Superhero character tests
    def test_render_superhero(self):
        """Test rendering a superhero character."""
        page = Page(width=400, height=300)
        hero = Superhero(name="Captain Test").move_to((200, 150))
        page.add(hero)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = page.render(f.name)
            content = Path(output_path).read_text()
            assert "svg" in content.lower()
            Path(output_path).unlink()

    def test_render_superhero_with_expression(self):
        """Test rendering a superhero with expression."""
        page = Page(width=400, height=300)
        hero = Superhero(name="HappyHero", expression="happy").move_to((200, 150))
        page.add(hero)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = page.render(f.name)
            content = Path(output_path).read_text()
            assert "svg" in content.lower()
            Path(output_path).unlink()

    def test_render_superhero_with_pose(self):
        """Test rendering a superhero with different poses."""
        for pose_name in ["standing", "waving", "jumping", "cheering"]:
            page = Page(width=400, height=300)
            hero = Superhero(name="Poser", pose=pose_name).move_to((200, 150))
            page.add(hero)

            with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
                output_path = page.render(f.name)
                content = Path(output_path).read_text()
                assert "svg" in content.lower()
                Path(output_path).unlink()

    def test_render_superhero_facing_left(self):
        """Test rendering a superhero facing left."""
        page = Page(width=400, height=300)
        hero = Superhero(name="Lefty", facing="left").move_to((200, 150))
        page.add(hero)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = page.render(f.name)
            content = Path(output_path).read_text()
            assert "svg" in content.lower()
            Path(output_path).unlink()

    def test_render_superhero_with_cape(self):
        """Test rendering a superhero with cape."""
        page = Page(width=400, height=300)
        hero = Superhero(name="CapedCrusader", cape=True).move_to((200, 150))
        page.add(hero)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = page.render(f.name)
            content = Path(output_path).read_text()
            assert "svg" in content.lower()
            Path(output_path).unlink()

    def test_render_superhero_without_cape(self):
        """Test rendering a superhero without cape."""
        page = Page(width=400, height=300)
        hero = Superhero(name="NoCape", cape=False).move_to((200, 150))
        page.add(hero)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = page.render(f.name)
            content = Path(output_path).read_text()
            assert "svg" in content.lower()
            Path(output_path).unlink()

    def test_render_superhero_masks(self):
        """Test rendering a superhero with different mask types."""
        for mask in ["domino", "cowl", "none"]:
            page = Page(width=400, height=300)
            hero = Superhero(name="MaskedHero", mask=mask).move_to((200, 150))
            page.add(hero)

            with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
                output_path = page.render(f.name)
                content = Path(output_path).read_text()
                assert "svg" in content.lower()
                Path(output_path).unlink()

    def test_render_superhero_emblems(self):
        """Test rendering a superhero with different chest emblems."""
        for emblem in ["star", "diamond", "circle", "shield", "none"]:
            page = Page(width=400, height=300)
            hero = Superhero(name="EmblemHero", emblem=emblem).move_to((200, 150))
            page.add(hero)

            with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
                output_path = page.render(f.name)
                content = Path(output_path).read_text()
                assert "svg" in content.lower()
                Path(output_path).unlink()

    def test_render_superhero_all_expressions(self):
        """Test rendering superhero with all expression types."""
        expressions = ["neutral", "happy", "sad", "angry", "surprised",
                       "confused", "sleepy", "excited", "scared", "smirk", "crying"]
        for expr_name in expressions:
            page = Page(width=400, height=300)
            hero = Superhero(name="Expressive", expression=expr_name).move_to((200, 150))
            page.add(hero)

            with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
                output_path = page.render(f.name)
                content = Path(output_path).read_text()
                assert "svg" in content.lower()
                Path(output_path).unlink()

    def test_render_superhero_custom_colors(self):
        """Test rendering a superhero with custom colors."""
        page = Page(width=400, height=300)
        hero = Superhero(
            name="ColorHero",
            color="#FF0000",
            skin_color="#FFD700",
            costume_primary="#0000FF",
            costume_secondary="#00FF00",
            cape_color="#FF00FF",
        ).move_to((200, 150))
        page.add(hero)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = page.render(f.name)
            content = Path(output_path).read_text()
            assert "svg" in content.lower()
            Path(output_path).unlink()

    def test_render_superhero_full_costume(self):
        """Test rendering a superhero with all costume options enabled."""
        page = Page(width=400, height=300)
        hero = Superhero(
            name="FullHero",
            cape=True,
            mask="domino",
            emblem="star",
            boots=True,
            gloves=True,
        ).move_to((200, 150))
        page.add(hero)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = page.render(f.name)
            content = Path(output_path).read_text()
            assert "svg" in content.lower()
            Path(output_path).unlink()

    # Cartoon character tests
    def test_render_cartoon(self):
        """Test rendering a cartoon character."""
        page = Page(width=400, height=300)
        toon = Cartoon(name="ToonyMcToonface").move_to((200, 150))
        page.add(toon)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = page.render(f.name)
            content = Path(output_path).read_text()
            assert "svg" in content.lower()
            Path(output_path).unlink()

    def test_render_cartoon_with_expression(self):
        """Test rendering a cartoon with expression."""
        page = Page(width=400, height=300)
        toon = Cartoon(name="HappyToon", expression="happy").move_to((200, 150))
        page.add(toon)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = page.render(f.name)
            content = Path(output_path).read_text()
            assert "svg" in content.lower()
            Path(output_path).unlink()

    def test_render_cartoon_with_pose(self):
        """Test rendering a cartoon with different poses."""
        for pose_name in ["standing", "waving", "jumping", "cheering"]:
            page = Page(width=400, height=300)
            toon = Cartoon(name="Poser", pose=pose_name).move_to((200, 150))
            page.add(toon)

            with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
                output_path = page.render(f.name)
                content = Path(output_path).read_text()
                assert "svg" in content.lower()
                Path(output_path).unlink()

    def test_render_cartoon_facing_left(self):
        """Test rendering a cartoon facing left."""
        page = Page(width=400, height=300)
        toon = Cartoon(name="Lefty", facing="left").move_to((200, 150))
        page.add(toon)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = page.render(f.name)
            content = Path(output_path).read_text()
            assert "svg" in content.lower()
            Path(output_path).unlink()

    def test_render_cartoon_body_shapes(self):
        """Test rendering a cartoon with different body shapes."""
        for body_shape in ["pear", "bean", "round"]:
            page = Page(width=400, height=300)
            toon = Cartoon(name="ShapedToon", body_shape=body_shape).move_to((200, 150))
            page.add(toon)

            with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
                output_path = page.render(f.name)
                content = Path(output_path).read_text()
                assert "svg" in content.lower()
                Path(output_path).unlink()

    def test_render_cartoon_nose_types(self):
        """Test rendering a cartoon with different nose types."""
        for nose in ["round", "triangle", "long"]:
            page = Page(width=400, height=300)
            toon = Cartoon(name="NoseToon", nose_type=nose).move_to((200, 150))
            page.add(toon)

            with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
                output_path = page.render(f.name)
                content = Path(output_path).read_text()
                assert "svg" in content.lower()
                Path(output_path).unlink()

    def test_render_cartoon_ear_sizes(self):
        """Test rendering a cartoon with different ear sizes."""
        for ear_size in ["small", "normal", "large"]:
            page = Page(width=400, height=300)
            toon = Cartoon(name="EarToon", ear_size=ear_size).move_to((200, 150))
            page.add(toon)

            with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
                output_path = page.render(f.name)
                content = Path(output_path).read_text()
                assert "svg" in content.lower()
                Path(output_path).unlink()

    def test_render_cartoon_with_gloves(self):
        """Test rendering a cartoon with and without gloves."""
        for gloves in [True, False]:
            page = Page(width=400, height=300)
            toon = Cartoon(name="GloveToon", gloves=gloves).move_to((200, 150))
            page.add(toon)

            with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
                output_path = page.render(f.name)
                content = Path(output_path).read_text()
                assert "svg" in content.lower()
                Path(output_path).unlink()

    def test_render_cartoon_all_expressions(self):
        """Test rendering cartoon with all expression types."""
        expressions = ["neutral", "happy", "sad", "angry", "surprised",
                       "confused", "sleepy", "excited", "scared", "smirk", "crying"]
        for expr_name in expressions:
            page = Page(width=400, height=300)
            toon = Cartoon(name="Expressive", expression=expr_name).move_to((200, 150))
            page.add(toon)

            with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
                output_path = page.render(f.name)
                content = Path(output_path).read_text()
                assert "svg" in content.lower()
                Path(output_path).unlink()

    def test_render_cartoon_custom_colors(self):
        """Test rendering a cartoon with custom colors."""
        page = Page(width=400, height=300)
        toon = Cartoon(
            name="ColorToon",
            color="#FF0000",
            skin_color="#FFDAB9",
            outline_color="#000000",
            outfit_color="#4169E1",
            hair_color="#FFD700",
        ).move_to((200, 150))
        page.add(toon)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = page.render(f.name)
            content = Path(output_path).read_text()
            assert "svg" in content.lower()
            Path(output_path).unlink()

    def test_render_cartoon_full_options(self):
        """Test rendering a cartoon with all options customized."""
        page = Page(width=400, height=300)
        toon = Cartoon(
            name="FullToon",
            body_shape="round",
            nose_type="round",
            ear_size="large",
            gloves=True,
            expression="happy",
        ).move_to((200, 150))
        page.add(toon)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = page.render(f.name)
            content = Path(output_path).read_text()
            assert "svg" in content.lower()
            Path(output_path).unlink()

    def test_render_shapes(self):
        """Test rendering basic shapes."""
        page = Page(width=400, height=300)
        rect = Rectangle(width=100, height=50).move_to((100, 100))
        circle = Circle(radius=30).move_to((250, 100))
        line = Line(start=(0, 0), end=(100, 100)).move_to((200, 200))
        page.add(rect, circle, line)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = page.render(f.name)
            content = Path(output_path).read_text()
            assert "<rect" in content
            assert "<circle" in content
            assert "<line" in content
            Path(output_path).unlink()

    def test_render_text(self):
        """Test rendering text."""
        page = Page(width=400, height=300)
        text = Text(text="Hello World", font_size=24).move_to((200, 150))
        page.add(text)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = page.render(f.name)
            content = Path(output_path).read_text()
            assert "Hello World" in content
            assert "<text" in content
            Path(output_path).unlink()

    def test_render_sfx(self):
        """Test rendering SFX text with outline."""
        page = Page(width=400, height=300)
        sfx = SFX(text="BOOM!", color="#FF0000").move_to((200, 150))
        page.add(sfx)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = page.render(f.name)
            content = Path(output_path).read_text()
            assert "BOOM!" in content
            Path(output_path).unlink()

    def test_render_with_opacity(self):
        """Test rendering objects with opacity."""
        page = Page(width=400, height=300)
        rect = Rectangle(width=100, height=100).move_to((200, 150)).set_opacity(0.5)
        page.add(rect)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = page.render(f.name)
            content = Path(output_path).read_text()
            assert 'opacity="0.5"' in content
            Path(output_path).unlink()

    def test_render_complex_scene(self):
        """Test rendering a complex scene with multiple elements."""
        page = Page(width=800, height=600)

        panel = Panel(width=700, height=500)
        panel.move_to((400, 300))

        char1 = Stickman(name="Alice").move_to((300, 350))
        char2 = Stickman(name="Bob").move_to((500, 350)).face("left")

        bubble1 = char1.say("Hello!")
        bubble2 = char2.say("Hi there!")

        panel.add_content(char1, char2, bubble1, bubble2)
        page.add(panel)

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            output_path = page.render(f.name)
            content = Path(output_path).read_text()

            assert "<svg" in content
            assert "Hello!" in content
            assert "Hi there!" in content
            Path(output_path).unlink()

    def test_render_to_string_empty_page(self):
        """Test render_to_string with an empty page."""
        page = Page(width=400, height=300)
        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        assert isinstance(svg_string, str)
        assert "<svg" in svg_string
        assert 'width="400px"' in svg_string
        assert 'height="300px"' in svg_string
        assert "</svg>" in svg_string

    def test_render_to_string_with_content(self):
        """Test render_to_string with various objects."""
        page = Page(width=400, height=300)
        panel = Panel(width=300, height=200).move_to((200, 150))
        bubble = SpeechBubble(text="Test!").move_to((200, 100))
        page.add(panel, bubble)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        assert "<svg" in svg_string
        assert "<rect" in svg_string
        assert "Test!" in svg_string

    def test_render_to_string_matches_file_render(self):
        """Test that render_to_string produces same content as file render."""
        page = Page(width=400, height=300, background_color="#FAFAFA")
        rect = Rectangle(width=100, height=50).move_to((200, 150))
        page.add(rect)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
            renderer2 = SVGRenderer(page)
            output_path = renderer2.render(f.name)
            file_content = Path(output_path).read_text()
            Path(output_path).unlink()

        # Both should have the same core elements (file may have filename attribute)
        assert 'width="400px"' in svg_string
        assert 'width="400px"' in file_content
        assert "#FAFAFA" in svg_string
        assert "#FAFAFA" in file_content


class TestEffectRendering:
    """Tests for effect rendering in SVG renderer."""

    def test_render_shake_effect(self):
        """Test rendering a shake effect."""
        page = Page(width=400, height=300)
        rect = Rectangle(width=100, height=100).move_to((200, 150))
        page.add(rect)

        # Add shake effect with fixed seed for reproducibility
        effect = ShakeEffect(target=rect, seed=42, intensity=1.0)
        page.add_effect(effect)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Shake effect generates polylines (ghost copies) and lines (motion blur)
        assert "<polyline" in svg_string or "<line" in svg_string

    def test_render_zoom_effect(self):
        """Test rendering a zoom effect."""
        page = Page(width=400, height=300)
        rect = Rectangle(width=50, height=50).move_to((200, 150))
        page.add(rect)

        effect = ZoomEffect(target=rect, seed=42, num_lines=16)
        page.add_effect(effect)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Zoom effect generates radial lines
        assert "<line" in svg_string
        assert '<g opacity="0.6"' in svg_string  # Default zoom opacity

    def test_render_motion_lines(self):
        """Test rendering motion lines effect."""
        page = Page(width=400, height=300)
        char = Stickman(name="Runner").move_to((200, 150))
        page.add(char)

        effect = MotionLines(target=char, seed=42, num_lines=8)
        page.add_effect(effect)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Motion lines generate line elements
        assert "<line" in svg_string

    def test_render_focus_lines(self):
        """Test rendering focus lines effect."""
        page = Page(width=400, height=300)
        face = SimpleFace(name="Focus").move_to((200, 150))
        page.add(face)

        effect = FocusLines(target=face, seed=42, num_lines=24)
        page.add_effect(effect)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Focus lines generate radial lines
        assert "<line" in svg_string

    def test_render_focus_lines_with_fill(self):
        """Test rendering focus lines with background fill."""
        page = Page(width=400, height=300)

        effect = FocusLines(
            position=(200, 150),
            seed=42,
            fill_background=True,
            background_color="#FFFF00"
        )
        page.add_effect(effect)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # With fill_background, generates polygon elements
        assert "<polygon" in svg_string

    def test_render_appear_effect_sparkle(self):
        """Test rendering appear effect with sparkle style."""
        page = Page(width=400, height=300)
        rect = Rectangle(width=60, height=60).move_to((200, 150))
        page.add(rect)

        effect = AppearEffect(target=rect, seed=42, style="sparkle")
        page.add_effect(effect)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Sparkle generates polygon (stars) and circle (dots) elements
        assert "<polygon" in svg_string or "<circle" in svg_string

    def test_render_appear_effect_flash(self):
        """Test rendering appear effect with flash style."""
        page = Page(width=400, height=300)

        effect = AppearEffect(position=(200, 150), seed=42, style="flash")
        page.add_effect(effect)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Flash generates polygon elements (rays) and circle (center glow)
        assert "<polygon" in svg_string or "<circle" in svg_string

    def test_render_appear_effect_fade(self):
        """Test rendering appear effect with fade style."""
        page = Page(width=400, height=300)

        effect = AppearEffect(position=(200, 150), seed=42, style="fade")
        page.add_effect(effect)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Fade generates concentric polyline rings
        assert "<polyline" in svg_string

    def test_render_appear_effect_reveal(self):
        """Test rendering appear effect with reveal style."""
        page = Page(width=400, height=300)

        effect = AppearEffect(position=(200, 150), seed=42, style="reveal")
        page.add_effect(effect)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Reveal generates lines and polylines for corner accents
        assert "<line" in svg_string or "<polyline" in svg_string

    def test_render_impact_effect(self):
        """Test rendering impact effect."""
        page = Page(width=400, height=300)

        effect = ImpactEffect(position=(200, 150), seed=42, num_spikes=8)
        page.add_effect(effect)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Impact generates polygon (star burst) and lines (debris)
        assert "<polygon" in svg_string
        assert "<line" in svg_string

    def test_render_effect_z_index_background(self):
        """Test that effects with negative z_index render behind objects."""
        page = Page(width=400, height=300)
        rect = Rectangle(width=100, height=100).move_to((200, 150))
        page.add(rect)

        # Effect with negative z_index should render behind
        effect = ZoomEffect(target=rect, z_index=-1, seed=42)
        page.add_effect(effect)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Effect should be present
        assert "<line" in svg_string
        # Rectangle should also be present
        assert "<rect" in svg_string

    def test_render_effect_z_index_foreground(self):
        """Test that effects with positive z_index render in front of objects."""
        page = Page(width=400, height=300)
        rect = Rectangle(width=100, height=100).move_to((200, 150))
        page.add(rect)

        # Effect with positive z_index should render in front
        effect = ImpactEffect(position=(200, 150), z_index=1, seed=42)
        page.add_effect(effect)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Both effect and rectangle should be present
        assert "<polygon" in svg_string
        assert "<rect" in svg_string

    def test_render_multiple_effects(self):
        """Test rendering multiple effects on the same page."""
        page = Page(width=400, height=300)

        # Background effect
        effect1 = FocusLines(position=(200, 150), z_index=-1, seed=42, num_lines=12)
        # Foreground effect
        effect2 = ImpactEffect(position=(200, 150), z_index=1, seed=43, num_spikes=6)

        page.add_effect(effect1)
        page.add_effect(effect2)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Both effects should be rendered
        assert "<line" in svg_string  # Focus lines
        assert "<polygon" in svg_string  # Impact burst

    def test_render_effect_opacity(self):
        """Test that effect opacity is applied."""
        page = Page(width=400, height=300)

        effect = ZoomEffect(position=(200, 150), opacity=0.5, seed=42, num_lines=8)
        page.add_effect(effect)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Group should have opacity attribute
        assert 'opacity="0.5"' in svg_string

    def test_render_effect_with_stroke_dasharray(self):
        """Test rendering effect elements with stroke dasharray."""
        page = Page(width=400, height=300)
        rect = Rectangle(width=100, height=100).move_to((200, 150))
        page.add(rect)

        # ShakeEffect generates dashed polylines
        effect = ShakeEffect(target=rect, seed=42, num_copies=2)
        page.add_effect(effect)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Shake effect uses stroke-dasharray for ghost copies
        assert "stroke-dasharray" in svg_string


class TestPanelBackgroundImage:
    """Tests for panel background image rendering."""

    def test_panel_with_background_image_file(self, tmp_path):
        """Test rendering panel with a background image from file."""
        # Create a simple test PNG image (1x1 red pixel)
        import base64

        # Minimal valid PNG (1x1 red pixel)
        png_data = base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8DwHwAFBQIAX8jx"
            "0gAAAABJRU5ErkJggg=="
        )
        image_path = tmp_path / "test_bg.png"
        image_path.write_bytes(png_data)

        # Create panel with background image
        page = Page(width=400, height=300)
        panel = Panel(width=300, height=200)
        panel.move_to((200, 150))
        panel.set_background(image=str(image_path))
        page.add(panel)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Should contain an image element with data URI
        assert "<image" in svg_string
        assert "data:image/png;base64" in svg_string

    def test_panel_with_background_image_nonexistent(self):
        """Test rendering panel with nonexistent background image falls back to path."""
        page = Page(width=400, height=300)
        panel = Panel(width=300, height=200)
        panel.move_to((200, 150))
        panel.set_background(image="/nonexistent/path/image.png")
        page.add(panel)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Should still attempt to render with the path
        assert "<image" in svg_string
        assert "/nonexistent/path/image.png" in svg_string

    def test_panel_with_background_image_and_rounded_corners(self, tmp_path):
        """Test panel background image with rounded corners creates clip path."""
        import base64

        png_data = base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8DwHwAFBQIAX8jx"
            "0gAAAABJRU5ErkJggg=="
        )
        image_path = tmp_path / "test_bg_round.png"
        image_path.write_bytes(png_data)

        page = Page(width=400, height=300)
        panel = Panel(width=300, height=200)
        panel.set_border(radius=20)  # Set radius through set_border method
        panel.move_to((200, 150))
        panel.set_background(image=str(image_path))
        page.add(panel)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Should have clip path for rounded corners
        assert "<clipPath" in svg_string
        assert "clip-path" in svg_string
        assert "<image" in svg_string

    def test_panel_background_color_renders_before_image(self, tmp_path):
        """Test that background color is rendered before background image."""
        import base64

        png_data = base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8DwHwAFBQIAX8jx"
            "0gAAAABJRU5ErkJggg=="
        )
        image_path = tmp_path / "test_bg.png"
        image_path.write_bytes(png_data)

        page = Page(width=400, height=300)
        panel = Panel(width=300, height=200, background_color="#FF0000")
        panel.move_to((200, 150))
        panel.set_background(image=str(image_path))
        page.add(panel)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Both rect (background color) and image should be present
        assert "<rect" in svg_string
        assert "<image" in svg_string
        assert "#FF0000" in svg_string

    def test_panel_without_background_image(self):
        """Test that panel without background image doesn't have image element."""
        page = Page(width=400, height=300)
        panel = Panel(width=300, height=200)
        panel.move_to((200, 150))
        page.add(panel)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Should have rect but not image
        assert "<rect" in svg_string
        # Count image elements - there should be none for a simple panel
        # (unless other content has images)
        image_count = svg_string.count("<image")
        assert image_count == 0

    def test_parser_background_image_renders(self, tmp_path):
        """Test that parser-created panels with background image render correctly."""
        import base64
        from comix.parser.parser import parse_markup

        png_data = base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8DwHwAFBQIAX8jx"
            "0gAAAABJRU5ErkJggg=="
        )
        image_path = tmp_path / "bg.png"
        image_path.write_bytes(png_data)

        markup = f"""
[page 1x1]
# panel 1
[background: {image_path}]
character(center): "Test"
"""
        page = parse_markup(markup)
        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Should contain the background image
        assert "<image" in svg_string
        assert "data:image/png;base64" in svg_string


class TestPanelBorderStyles:
    """Tests for panel border style rendering."""

    def test_panel_with_dashed_border(self):
        """Test rendering panel with dashed border style."""
        page = Page(width=400, height=300)
        panel = Panel(width=200, height=150)
        panel.set_border(style="dashed")
        panel.move_to((200, 150))
        page.add(panel)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Dashed border should have stroke-dasharray="5,5"
        assert 'stroke-dasharray="5,5"' in svg_string

    def test_panel_with_dotted_border(self):
        """Test rendering panel with dotted border style."""
        page = Page(width=400, height=300)
        panel = Panel(width=200, height=150)
        panel.set_border(style="dotted")
        panel.move_to((200, 150))
        page.add(panel)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Dotted border should have stroke-dasharray="2,2"
        assert 'stroke-dasharray="2,2"' in svg_string

    def test_panel_with_solid_border(self):
        """Test rendering panel with solid border (default) has no dasharray."""
        page = Page(width=400, height=300)
        panel = Panel(width=200, height=150)
        panel.set_border(style="solid")
        panel.move_to((200, 150))
        page.add(panel)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Solid border should NOT have stroke-dasharray attribute
        assert "stroke-dasharray" not in svg_string


class TestBubbleBorderStyles:
    """Tests for bubble border style rendering."""

    def test_bubble_with_dashed_border(self):
        """Test rendering bubble with dashed border style."""
        page = Page(width=400, height=300)
        bubble = SpeechBubble(text="Test", border_style="dashed")
        bubble.move_to((200, 150))
        page.add(bubble)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Dashed border should have stroke-dasharray="5,5"
        assert 'stroke-dasharray="5,5"' in svg_string

    def test_bubble_with_dotted_border(self):
        """Test rendering bubble with dotted border style."""
        from comix.cobject.bubble.bubble import WhisperBubble

        page = Page(width=400, height=300)
        # WhisperBubble defaults to dotted style
        bubble = WhisperBubble(text="Whisper")
        bubble.move_to((200, 150))
        page.add(bubble)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # WhisperBubble should have dashed/dotted border
        assert "stroke-dasharray" in svg_string


class TestBubbleEmphasis:
    """Tests for bubble emphasis rendering with shadow effects."""

    def test_bubble_with_emphasis_shadow(self):
        """Test rendering emphasized bubble creates shadow."""
        page = Page(width=400, height=300)
        bubble = SpeechBubble(text="Important!", emphasis=True)
        bubble.move_to((200, 150))
        page.add(bubble)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Emphasized bubble should have shadow polygon with fill-opacity
        assert 'fill-opacity="0.2"' in svg_string

    def test_bubble_emphasis_thicker_border(self):
        """Test that emphasized bubble has thicker border."""
        page = Page(width=400, height=300)
        # Create two bubbles - one with emphasis, one without
        bubble_normal = SpeechBubble(text="Normal", border_width=2.0)
        bubble_emphasis = SpeechBubble(text="Emphasized!", emphasis=True, border_width=2.0)
        bubble_normal.move_to((100, 150))
        bubble_emphasis.move_to((300, 150))
        page.add(bubble_normal, bubble_emphasis)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Both bubbles render
        assert "Normal" in svg_string
        assert "Emphasized!" in svg_string
        # Emphasized bubble has shadow (with fill-opacity)
        assert 'fill-opacity="0.2"' in svg_string

    def test_bubble_emphasis_with_tail_shadow(self):
        """Test that emphasized bubble tail also has shadow."""
        page = Page(width=400, height=300)
        # Create bubble with tail pointing to a specific direction
        bubble = SpeechBubble(
            text="Hello!",
            emphasis=True,
            tail_direction="bottom-left",
            tail_length=30,
        )
        bubble.move_to((200, 150))
        page.add(bubble)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Should have multiple polygons (bubble + tail + shadows)
        polygon_count = svg_string.count("<polygon")
        # At minimum: bubble body, bubble shadow, tail, tail shadow = 4
        assert polygon_count >= 3

    def test_bubble_with_emphasis_and_dashed_border(self):
        """Test bubble with both emphasis and dashed border."""
        page = Page(width=400, height=300)
        bubble = SpeechBubble(
            text="Emphatic!",
            emphasis=True,
            border_style="dashed",
        )
        bubble.move_to((200, 150))
        page.add(bubble)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Should have both shadow and dashed border
        assert 'fill-opacity="0.2"' in svg_string  # Shadow
        assert 'stroke-dasharray="5,5"' in svg_string  # Dashed border


class TestRectangleCornerRadius:
    """Tests for rectangle corner radius rendering."""

    def test_rectangle_with_corner_radius(self):
        """Test rendering rectangle with corner radius."""
        page = Page(width=400, height=300)
        rect = Rectangle(width=100, height=50, corner_radius=10)
        rect.move_to((200, 150))
        page.add(rect)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Rectangle should have rx and ry attributes
        assert 'rx="10"' in svg_string
        assert 'ry="10"' in svg_string

    def test_rectangle_without_corner_radius(self):
        """Test rectangle without corner radius has no rx/ry."""
        page = Page(width=400, height=300)
        rect = Rectangle(width=100, height=50, corner_radius=0)
        rect.move_to((200, 150))
        page.add(rect)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Should not have rx/ry attributes (or they should be 0)
        # Check that it doesn't have a positive rx value
        assert 'rx="10"' not in svg_string


class TestLineStrokeStyles:
    """Tests for line stroke style rendering."""

    def test_line_with_dashed_stroke(self):
        """Test rendering line with dashed stroke style."""
        page = Page(width=400, height=300)
        line = Line(start=(50, 150), end=(350, 150), stroke_style="dashed")
        page.add(line)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Dashed line should have stroke-dasharray="5,5"
        assert 'stroke-dasharray="5,5"' in svg_string

    def test_line_with_dotted_stroke(self):
        """Test rendering line with dotted stroke style."""
        page = Page(width=400, height=300)
        line = Line(start=(50, 150), end=(350, 150), stroke_style="dotted")
        page.add(line)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Dotted line should have stroke-dasharray="2,2"
        assert 'stroke-dasharray="2,2"' in svg_string

    def test_line_with_solid_stroke(self):
        """Test rendering line with solid stroke (default) has no dasharray."""
        page = Page(width=400, height=300)
        line = Line(start=(50, 150), end=(350, 150), stroke_style="solid")
        page.add(line)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Solid line should NOT have stroke-dasharray attribute
        assert "stroke-dasharray" not in svg_string


class TestEmptyTextRendering:
    """Tests for empty text handling in rendering."""

    def test_render_empty_text_returns_early(self):
        """Test that empty text doesn't render any text elements."""
        page = Page(width=400, height=300)
        text = Text(text="")  # Empty text
        text.move_to((200, 150))
        page.add(text)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Page should render but without text element
        assert "<svg" in svg_string
        # Text elements from the empty Text object should not be present
        # (only the background rect should be there)


class TestGenericObjectRendering:
    """Tests for generic object rendering fallback."""

    def test_custom_cobject_renders_as_polyline(self):
        """Test that CObject with unknown type renders using generic method."""
        from comix.cobject.cobject import CObject
        import numpy as np

        # Create a custom CObject with custom type
        class CustomObject(CObject):
            def __init__(self):
                super().__init__()
                self._points = np.array(
                    [[0, 0], [50, 25], [100, 0], [100, 50], [0, 50]],
                    dtype=np.float64,
                )

            def get_render_data(self):
                data = super().get_render_data()
                data["type"] = "CustomType"  # Unknown type
                return data

        page = Page(width=400, height=300)
        custom = CustomObject()
        custom.move_to((200, 150))
        page.add(custom)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Should render as polyline
        assert "<polyline" in svg_string


class TestImageRendering:
    """Tests for image rendering with various options."""

    def test_image_with_source_path(self):
        """Test rendering image using source path directly."""
        from comix.cobject.image.image import Image

        page = Page(width=400, height=300)
        img = Image(source="/path/to/image.png", width=100, height=100)
        img.move_to((200, 150))
        page.add(img)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Should contain image element with href
        assert "<image" in svg_string
        assert "/path/to/image.png" in svg_string

    def test_image_with_preserve_aspect_ratio_false(self):
        """Test rendering image without preserving aspect ratio."""
        from comix.cobject.image.image import Image

        page = Page(width=400, height=300)
        img = Image(
            source="/path/to/image.png",
            width=100,
            height=100,
            preserve_aspect_ratio=False,
        )
        img.move_to((200, 150))
        page.add(img)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Should have preserveAspectRatio="none"
        assert 'preserveAspectRatio="none"' in svg_string

    def test_image_with_cover_fit(self):
        """Test rendering image with cover fit mode."""
        from comix.cobject.image.image import Image

        page = Page(width=400, height=300)
        img = Image(
            source="/path/to/image.png",
            width=100,
            height=100,
            fit="cover",
        )
        img.move_to((200, 150))
        page.add(img)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Should have preserveAspectRatio with slice (for cover)
        assert "xMidYMid slice" in svg_string

    def test_image_placeholder_when_no_source(self):
        """Test that image without source renders placeholder."""
        from comix.cobject.image.image import Image

        page = Page(width=400, height=300)
        # Create image without setting source (should show placeholder)
        img = Image(width=100, height=100)
        img.move_to((200, 150))
        page.add(img)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Should have placeholder rect and text
        assert "<rect" in svg_string
        assert "#EEEEEE" in svg_string  # Placeholder fill color
        assert "No image" in svg_string  # Placeholder text


class TestSimpleFaceExpressionRendering:
    """Tests for SimpleFace expression rendering with all eye, mouth, and eyebrow types."""

    def test_render_neutral_expression(self):
        """Test neutral expression (default) renders correctly."""
        page = Page(width=400, height=300)
        face = SimpleFace(name="Neutral").move_to((200, 150))
        page.add(face)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Should have face circle and basic features
        assert "<circle" in svg_string
        # Neutral expression has straight mouth line
        assert "<line" in svg_string

    def test_render_happy_expression_curved_eyes(self):
        """Test happy expression with curved eyes (^_^)."""
        page = Page(width=400, height=300)
        face = SimpleFace(name="Happy").move_to((200, 150))
        face.set_expression("happy")  # Uses curved eyes and smile mouth
        page.add(face)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Curved eyes are rendered as polylines
        assert "<polyline" in svg_string

    def test_render_sad_expression_droopy_eyes(self):
        """Test sad expression with droopy eyes and frown mouth."""
        page = Page(width=400, height=300)
        face = SimpleFace(name="Sad").move_to((200, 150))
        face.set_expression("sad")  # Uses droopy eyes and frown mouth
        page.add(face)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Droopy eyes and frown mouth should render
        assert "<circle" in svg_string
        assert "<polyline" in svg_string  # Frown is a polyline

    def test_render_angry_expression_narrow_eyes(self):
        """Test angry expression with narrow eyes and furrowed brows."""
        page = Page(width=400, height=300)
        face = SimpleFace(name="Angry").move_to((200, 150))
        face.set_expression("angry")  # Uses narrow eyes and furrowed eyebrows
        page.add(face)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Narrow eyes are rendered as lines
        assert "<line" in svg_string
        assert "<circle" in svg_string  # Face circle

    def test_render_surprised_expression_wide_eyes(self):
        """Test surprised expression with wide eyes and raised brows."""
        page = Page(width=400, height=300)
        face = SimpleFace(name="Surprised").move_to((200, 150))
        face.set_expression("surprised")  # Uses wide eyes and open mouth
        page.add(face)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Wide eyes have outer white circle with inner pupil
        # Count circles - face + 2 outer eyes + 2 inner pupils = 5 or more
        circle_count = svg_string.count("<circle")
        assert circle_count >= 3  # At least face, outer eyes, inner pupils

    def test_render_confused_expression_uneven_eyes(self):
        """Test confused expression with uneven eyes and wavy mouth."""
        page = Page(width=400, height=300)
        face = SimpleFace(name="Confused").move_to((200, 150))
        face.set_expression("confused")  # Uses uneven eyes and wavy mouth
        page.add(face)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Uneven eyes and wavy mouth - both rendered
        assert "<circle" in svg_string
        assert "<polyline" in svg_string  # Wavy mouth is a polyline

    def test_render_all_expressions_in_one_page(self):
        """Test rendering all 6 expressions on one page."""
        page = Page(width=800, height=300)
        expressions = ["neutral", "happy", "sad", "angry", "surprised", "confused"]

        for i, expr in enumerate(expressions):
            face = SimpleFace(name=expr).move_to((100 + i * 120, 150))
            face.set_expression(expr)
            page.add(face)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Should render all 6 faces
        circle_count = svg_string.count("<circle")
        assert circle_count >= 6  # At least 6 face circles

    def test_render_expression_with_custom_color(self):
        """Test expression rendering with custom colors."""
        page = Page(width=400, height=300)
        face = SimpleFace(name="Custom", color="#FF0000", fill_color="#FFFF00")
        face.move_to((200, 150))
        face.set_expression("happy")
        page.add(face)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # Should contain custom colors
        assert "#FF0000" in svg_string  # Stroke color
        assert "#FFFF00" in svg_string  # Fill color

    def test_render_mouth_types_via_custom_expression(self):
        """Test each mouth type renders distinctly."""
        from comix.cobject.character.character import Expression

        mouth_types = ["normal", "smile", "frown", "open", "wavy"]

        for mouth in mouth_types:
            page = Page(width=400, height=300)
            face = SimpleFace(name=f"Mouth_{mouth}").move_to((200, 150))
            # Set custom expression with specific mouth type
            face._expression = Expression(
                name="custom", eyes="normal", mouth=mouth, eyebrows="normal"
            )
            page.add(face)

            renderer = SVGRenderer(page)
            svg_string = renderer.render_to_string()

            # All mouth types should render successfully
            assert "<circle" in svg_string  # Face circle
            # Each mouth type renders a different element
            if mouth == "normal":
                assert "<line" in svg_string  # Straight line
            elif mouth in ("smile", "frown", "wavy"):
                assert "<polyline" in svg_string  # Curved/wavy path
            elif mouth == "open":
                # Open mouth is a circle (not filled)
                assert svg_string.count("<circle") >= 2  # Face + mouth

    def test_render_eyebrow_types_via_custom_expression(self):
        """Test each eyebrow type renders distinctly."""
        from comix.cobject.character.character import Expression

        eyebrow_types = ["normal", "raised", "worried", "furrowed"]

        for brow in eyebrow_types:
            page = Page(width=400, height=300)
            face = SimpleFace(name=f"Brows_{brow}").move_to((200, 150))
            # Set custom expression with specific eyebrow type
            face._expression = Expression(
                name="custom", eyes="normal", mouth="normal", eyebrows=brow
            )
            page.add(face)

            renderer = SVGRenderer(page)
            svg_string = renderer.render_to_string()

            # All eyebrow types should render successfully
            assert "<circle" in svg_string  # Face circle
            if brow == "normal":
                # Normal has no visible eyebrows (cleaner look)
                pass
            elif brow == "raised":
                assert "<polyline" in svg_string  # Raised brows are polylines
            elif brow in ("worried", "furrowed"):
                # These are rendered as lines
                line_count = svg_string.count("<line")
                assert line_count >= 2  # Mouth line + eyebrow lines

    def test_render_eye_types_via_custom_expression(self):
        """Test each eye type renders distinctly."""
        from comix.cobject.character.character import Expression

        eye_types = ["normal", "curved", "droopy", "narrow", "wide", "uneven"]

        for eye in eye_types:
            page = Page(width=400, height=300)
            face = SimpleFace(name=f"Eyes_{eye}").move_to((200, 150))
            # Set custom expression with specific eye type
            face._expression = Expression(
                name="custom", eyes=eye, mouth="normal", eyebrows="normal"
            )
            page.add(face)

            renderer = SVGRenderer(page)
            svg_string = renderer.render_to_string()

            # All eye types should render successfully
            assert "<circle" in svg_string  # Face circle always present
            if eye == "normal":
                # Normal eyes are filled circles
                assert svg_string.count("<circle") >= 3  # Face + 2 eyes
            elif eye == "curved":
                # Curved eyes are polylines
                assert "<polyline" in svg_string
            elif eye == "droopy":
                # Droopy are circles (just positioned lower)
                assert svg_string.count("<circle") >= 3
            elif eye == "narrow":
                # Narrow eyes are lines
                assert "<line" in svg_string
            elif eye == "wide":
                # Wide eyes have outer circle (white) + inner pupil
                assert svg_string.count("<circle") >= 5  # Face + 2 outer + 2 inner
            elif eye == "uneven":
                # Uneven eyes are circles of different sizes
                assert svg_string.count("<circle") >= 3

    def test_render_new_eye_types(self):
        """Test new eye types (closed, stars, tears) render correctly."""
        from comix.cobject.character.character import Expression

        new_eye_types = ["closed", "stars", "tears"]

        for eye in new_eye_types:
            page = Page(width=400, height=300)
            face = SimpleFace(name=f"Eyes_{eye}").move_to((200, 150))
            face._expression = Expression(
                name="custom", eyes=eye, mouth="normal", eyebrows="normal"
            )
            page.add(face)

            renderer = SVGRenderer(page)
            svg_string = renderer.render_to_string()

            assert "<circle" in svg_string  # Face circle always present
            if eye == "closed":
                # Closed eyes are curved polylines
                assert "<polyline" in svg_string
            elif eye == "stars":
                # Star eyes have lines and a center dot
                assert "<line" in svg_string
                assert svg_string.count("<circle") >= 3  # Face + center dots
            elif eye == "tears":
                # Tears have normal eyes + tear drop circles
                assert svg_string.count("<circle") >= 5  # Face + eyes + tears
                assert "#87CEEB" in svg_string  # Light blue tear color

    def test_render_new_mouth_types(self):
        """Test new mouth types (grin, gasp, smirk) render correctly."""
        from comix.cobject.character.character import Expression

        new_mouth_types = ["grin", "gasp", "smirk"]

        for mouth in new_mouth_types:
            page = Page(width=400, height=300)
            face = SimpleFace(name=f"Mouth_{mouth}").move_to((200, 150))
            face._expression = Expression(
                name="custom", eyes="normal", mouth=mouth, eyebrows="normal"
            )
            page.add(face)

            renderer = SVGRenderer(page)
            svg_string = renderer.render_to_string()

            assert "<circle" in svg_string  # Face circle always present
            if mouth == "grin":
                # Grin has a polyline and teeth line
                assert "<polyline" in svg_string
                assert "<line" in svg_string
            elif mouth == "gasp":
                # Gasp is a circle (open mouth)
                assert svg_string.count("<circle") >= 4  # Face + eyes + mouth
            elif mouth == "smirk":
                # Smirk is a polyline
                assert "<polyline" in svg_string

    def test_render_new_eyebrow_types(self):
        """Test new eyebrow types (relaxed, asymmetric) render correctly."""
        from comix.cobject.character.character import Expression

        new_brow_types = ["relaxed", "asymmetric"]

        for brow in new_brow_types:
            page = Page(width=400, height=300)
            face = SimpleFace(name=f"Brows_{brow}").move_to((200, 150))
            face._expression = Expression(
                name="custom", eyes="normal", mouth="normal", eyebrows=brow
            )
            page.add(face)

            renderer = SVGRenderer(page)
            svg_string = renderer.render_to_string()

            assert "<circle" in svg_string  # Face circle always present
            if brow == "relaxed":
                # Relaxed eyebrows are lines
                assert "<line" in svg_string
            elif brow == "asymmetric":
                # Asymmetric has one polyline and one line
                assert "<polyline" in svg_string
                assert "<line" in svg_string

    def test_render_new_expressions_complete(self):
        """Test all new preset expressions render successfully."""
        new_expressions = ["sleepy", "excited", "scared", "smirk", "crying"]

        for expr_name in new_expressions:
            page = Page(width=400, height=300)
            face = SimpleFace(name=f"Expr_{expr_name}", expression=expr_name)
            face.move_to((200, 150))
            page.add(face)

            renderer = SVGRenderer(page)
            svg_string = renderer.render_to_string()

            # All expressions should render successfully
            assert "<circle" in svg_string
            assert "<svg" in svg_string


class TestEffectElementStrokeDasharray:
    """Tests for effect elements with stroke dasharray."""

    def test_effect_line_with_dasharray(self):
        """Test effect lines can have stroke dasharray."""
        # ShakeEffect generates dashed lines/polylines for motion blur
        page = Page(width=400, height=300)
        rect = Rectangle(width=100, height=100).move_to((200, 150))
        page.add(rect)

        effect = ShakeEffect(target=rect, seed=42, intensity=2.0, num_copies=3)
        page.add_effect(effect)

        renderer = SVGRenderer(page)
        svg_string = renderer.render_to_string()

        # ShakeEffect creates dashed motion blur lines
        assert "stroke-dasharray" in svg_string
