"""Tests for the Comix markup parser."""

import pytest

from comix.parser import parse_markup, MarkupParser
from comix.parser.parser import (
    CharacterAction,
    SFXAction,
    NarratorAction,
    BackgroundDirective,
    ParseError,
    _parse_modifiers,
)
from comix.page.page import Page
from comix.cobject.bubble.bubble import NarratorBubble


class TestParseModifiers:
    """Tests for the modifier parsing function."""

    def test_empty_modifiers(self):
        """Test parsing empty modifier string."""
        result = _parse_modifiers("")
        assert result["expression"] == "neutral"
        assert result["position"] == "center"
        assert result["facing"] == "right"
        assert result["bubble_type"] == "speech"

    def test_single_position(self):
        """Test parsing single position modifier."""
        result = _parse_modifiers("left")
        assert result["position"] == "left"
        # Position left should set facing to right
        assert result["facing"] == "right"

    def test_single_expression(self):
        """Test parsing single expression modifier."""
        result = _parse_modifiers("happy")
        assert result["expression"] == "happy"

    def test_position_and_expression(self):
        """Test parsing position and expression together."""
        result = _parse_modifiers("left, surprised")
        assert result["position"] == "left"
        assert result["expression"] == "surprised"
        assert result["facing"] == "right"

    def test_right_position_facing(self):
        """Test that right position sets facing to left."""
        result = _parse_modifiers("right")
        assert result["position"] == "right"
        assert result["facing"] == "left"

    def test_bubble_type_thought(self):
        """Test parsing thought bubble type."""
        result = _parse_modifiers("thought")
        assert result["bubble_type"] == "thought"

    def test_bubble_type_think(self):
        """Test that 'think' is normalized to 'thought'."""
        result = _parse_modifiers("think")
        assert result["bubble_type"] == "thought"

    def test_bubble_type_shout(self):
        """Test parsing shout bubble type."""
        result = _parse_modifiers("shout")
        assert result["bubble_type"] == "shout"

    def test_bubble_type_whisper(self):
        """Test parsing whisper bubble type."""
        result = _parse_modifiers("left, whisper")
        assert result["position"] == "left"
        assert result["bubble_type"] == "whisper"

    def test_all_modifiers(self):
        """Test parsing multiple modifiers together."""
        result = _parse_modifiers("right, angry, thought")
        assert result["position"] == "right"
        assert result["expression"] == "angry"
        assert result["bubble_type"] == "thought"
        assert result["facing"] == "left"

    def test_closeup_position(self):
        """Test parsing closeup position."""
        result = _parse_modifiers("closeup")
        assert result["position"] == "closeup"

    def test_case_insensitivity(self):
        """Test that modifiers are case insensitive."""
        result = _parse_modifiers("LEFT, HAPPY")
        assert result["position"] == "left"
        assert result["expression"] == "happy"

    def test_smirk_expression(self):
        """Test parsing 'smirk' expression modifier."""
        result = _parse_modifiers("right, smirk")
        assert result["expression"] == "smirk"
        assert result["position"] == "right"

    def test_explicit_facing_front(self):
        """Test explicit facing direction 'front'."""
        result = _parse_modifiers("center, happy, front")
        assert result["position"] == "center"
        assert result["expression"] == "happy"
        assert result["facing"] == "front"

    def test_explicit_facing_back(self):
        """Test explicit facing direction 'back'."""
        result = _parse_modifiers("center, back")
        assert result["position"] == "center"
        assert result["facing"] == "back"

    def test_explicit_facing_front_with_left_position(self):
        """Test explicit facing 'front' with left position."""
        # Position 'left' normally sets facing to 'right'
        # But explicit 'front' facing should override
        result = _parse_modifiers("left, front")
        assert result["position"] == "left"
        assert result["facing"] == "front"

    def test_explicit_facing_back_with_right_position(self):
        """Test explicit facing 'back' with right position."""
        # Position 'right' normally sets facing to 'left'
        # But explicit 'back' facing should override
        result = _parse_modifiers("right, back")
        assert result["position"] == "right"
        assert result["facing"] == "back"

    def test_front_and_back_directions(self):
        """Test front and back direction values (not left/right which are positions)."""
        # Note: 'left' and 'right' are treated as positions, not explicit facing directions
        # Only 'front' and 'back' work as explicit facing direction modifiers
        for direction in ["front", "back"]:
            result = _parse_modifiers(f"center, {direction}")
            assert result["facing"] == direction


class TestMarkupParser:
    """Tests for the MarkupParser class."""

    def test_parse_empty(self):
        """Test parsing empty markup."""
        parser = MarkupParser("")
        spec = parser.parse()
        assert spec.rows == 1
        assert spec.cols == 1

    def test_parse_page_declaration(self):
        """Test parsing page declaration."""
        parser = MarkupParser("[page 2x3]")
        spec = parser.parse()
        assert spec.rows == 2
        assert spec.cols == 3

    def test_parse_page_with_size(self):
        """Test parsing page declaration with custom size."""
        parser = MarkupParser("[page 2x2 1000x1500]")
        spec = parser.parse()
        assert spec.rows == 2
        assert spec.cols == 2
        assert spec.width == 1000.0
        assert spec.height == 1500.0

    def test_parse_panel_marker(self):
        """Test parsing panel markers."""
        markup = """
        [page 2x2]

        # panel 1

        # panel 2
        """
        parser = MarkupParser(markup)
        spec = parser.parse()
        assert len(spec.panels) >= 2
        assert spec.panels[0].number == 1
        assert spec.panels[1].number == 2

    def test_parse_character_action(self):
        """Test parsing character dialogue."""
        markup = """
        # panel 1
        Alice(left, happy): "Hello!"
        """
        parser = MarkupParser(markup)
        spec = parser.parse()

        assert len(spec.panels) >= 1
        actions = spec.panels[0].actions
        assert len(actions) == 1
        assert isinstance(actions[0], CharacterAction)
        assert actions[0].name == "Alice"
        assert actions[0].text == "Hello!"
        assert actions[0].position == "left"
        assert actions[0].expression == "happy"

    def test_parse_korean_character(self):
        """Test parsing Korean character names and dialogue."""
        markup = """
        # panel 1
        철수(left, surprised): "뭐라고?!"
        영희(right): "응, 진짜야"
        """
        parser = MarkupParser(markup)
        spec = parser.parse()

        actions = spec.panels[0].actions
        assert len(actions) == 2
        assert actions[0].name == "철수"
        assert actions[0].text == "뭐라고?!"
        assert actions[0].expression == "surprised"
        assert actions[1].name == "영희"
        assert actions[1].text == "응, 진짜야"

    def test_parse_sfx(self):
        """Test parsing sound effects."""
        markup = """
        # panel 1
        sfx: BOOM
        """
        parser = MarkupParser(markup)
        spec = parser.parse()

        actions = spec.panels[0].actions
        assert len(actions) == 1
        assert isinstance(actions[0], SFXAction)
        assert actions[0].text == "BOOM"

    def test_parse_narrator(self):
        """Test parsing narrator boxes."""
        markup = """
        # panel 1
        narrator: "Meanwhile, in another dimension..."
        """
        parser = MarkupParser(markup)
        spec = parser.parse()

        actions = spec.panels[0].actions
        assert len(actions) == 1
        assert isinstance(actions[0], NarratorAction)
        assert actions[0].text == "Meanwhile, in another dimension..."

    def test_parse_background(self):
        """Test parsing background directives."""
        markup = """
        # panel 1
        [background: A beautiful sunset]
        """
        parser = MarkupParser(markup)
        spec = parser.parse()

        actions = spec.panels[0].actions
        assert len(actions) == 1
        assert isinstance(actions[0], BackgroundDirective)
        assert actions[0].description == "A beautiful sunset"
        assert spec.panels[0].background == "A beautiful sunset"

    def test_parse_complete_panel(self):
        """Test parsing a complete panel with multiple elements."""
        markup = """
        [page 2x2]

        # panel 1
        [background: City street]
        Alice(left, surprised): "What?!"
        Bob(right, smug): "Yep."
        sfx: 충격
        narrator: "It was a shocking revelation."
        """
        parser = MarkupParser(markup)
        spec = parser.parse()

        assert spec.rows == 2
        assert spec.cols == 2

        actions = spec.panels[0].actions
        assert len(actions) == 5

        assert isinstance(actions[0], BackgroundDirective)
        assert isinstance(actions[1], CharacterAction)
        assert isinstance(actions[2], CharacterAction)
        assert isinstance(actions[3], SFXAction)
        assert isinstance(actions[4], NarratorAction)

    def test_parse_thought_bubble(self):
        """Test parsing thought bubble type."""
        markup = """
        # panel 1
        Alice(thought): "I wonder..."
        """
        parser = MarkupParser(markup)
        spec = parser.parse()

        action = spec.panels[0].actions[0]
        assert isinstance(action, CharacterAction)
        assert action.bubble_type == "thought"

    def test_parse_shout_bubble(self):
        """Test parsing shout bubble type."""
        markup = """
        # panel 1
        Alice(shout): "NOOO!"
        """
        parser = MarkupParser(markup)
        spec = parser.parse()

        action = spec.panels[0].actions[0]
        assert isinstance(action, CharacterAction)
        assert action.bubble_type == "shout"

    def test_skip_comments(self):
        """Test that // comments are skipped."""
        markup = """
        # panel 1
        // This is a comment
        Alice(left): "Hello"
        """
        parser = MarkupParser(markup)
        spec = parser.parse()

        actions = spec.panels[0].actions
        assert len(actions) == 1
        assert isinstance(actions[0], CharacterAction)

    def test_skip_shebang(self):
        """Test that #! lines are skipped."""
        markup = """
        #! This is a shebang-like comment
        # panel 1
        Alice(left): "Hello"
        """
        parser = MarkupParser(markup)
        spec = parser.parse()

        actions = spec.panels[0].actions
        assert len(actions) == 1

    def test_panels_without_explicit_markers(self):
        """Test that content before any panel marker goes to panel 1."""
        markup = """
        Alice(left): "No panel marker here"
        """
        parser = MarkupParser(markup)
        spec = parser.parse()

        assert len(spec.panels) >= 1
        actions = spec.panels[0].actions
        assert len(actions) == 1

    def test_fill_missing_panels(self):
        """Test that missing panels are filled for grid."""
        markup = """
        [page 2x2]

        # panel 1
        Alice(left): "Hello"
        """
        parser = MarkupParser(markup)
        spec = parser.parse()

        # 2x2 grid needs 4 panels
        assert len(spec.panels) == 4


class TestToPage:
    """Tests for converting parsed markup to Page objects."""

    def test_to_page_basic(self):
        """Test basic page conversion."""
        markup = """
        [page 2x2]

        # panel 1
        Alice(left): "Hello!"
        """
        parser = MarkupParser(markup)
        page = parser.to_page()

        assert isinstance(page, Page)
        assert page.width == 800.0
        assert page.height == 1200.0

    def test_to_page_with_characters(self):
        """Test page conversion creates characters."""
        markup = """
        # panel 1
        Alice(left, happy): "Hello!"
        """
        parser = MarkupParser(markup)
        page = parser.to_page()

        # Check that panels were created
        assert len(page._panels) >= 1

        # Check panel has content
        panel = page._panels[0]
        assert len(panel.submobjects) >= 1

    def test_to_page_creates_correct_bubble_types(self):
        """Test that correct bubble types are created."""
        markup = """
        # panel 1
        Alice(thought): "Thinking..."
        Bob(shout): "LOUD!"
        Charlie(whisper): "quiet..."
        Dana(left): "Normal speech"
        """
        parser = MarkupParser(markup)
        page = parser.to_page()

        # Get all objects from the panel
        panel = page._panels[0]
        bubbles = [obj for obj in panel.submobjects if hasattr(obj, 'bubble_type')]

        bubble_types = [b.bubble_type for b in bubbles]
        assert "thought" in bubble_types
        assert "shout" in bubble_types
        assert "whisper" in bubble_types
        assert "speech" in bubble_types

    def test_to_page_creates_sfx(self):
        """Test that SFX objects are created."""
        markup = """
        # panel 1
        sfx: KABOOM
        """
        parser = MarkupParser(markup)
        page = parser.to_page()

        panel = page._panels[0]
        from comix.cobject.text.text import SFX

        sfx_objects = [obj for obj in panel.submobjects if isinstance(obj, SFX)]
        assert len(sfx_objects) == 1

    def test_to_page_creates_narrator(self):
        """Test that narrator bubbles are created."""
        markup = """
        # panel 1
        narrator: "Once upon a time..."
        """
        parser = MarkupParser(markup)
        page = parser.to_page()

        panel = page._panels[0]
        narrator_bubbles = [obj for obj in panel.submobjects if isinstance(obj, NarratorBubble)]
        assert len(narrator_bubbles) == 1
        assert narrator_bubbles[0].text == "Once upon a time..."

    def test_to_page_handles_background_color(self):
        """Test that color backgrounds are applied to panels."""
        markup = """
        # panel 1
        [background: #ff5500]
        """
        parser = MarkupParser(markup)
        page = parser.to_page()

        panel = page._panels[0]
        assert panel.background_color == "#ff5500"

    def test_to_page_handles_background_named_color(self):
        """Test that named color backgrounds are applied to panels."""
        markup = """
        # panel 1
        [background: blue]
        """
        parser = MarkupParser(markup)
        page = parser.to_page()

        panel = page._panels[0]
        assert panel.background_color == "blue"

    def test_to_page_handles_background_image(self):
        """Test that image path backgrounds are applied to panels."""
        markup = """
        # panel 1
        [background: /path/to/image.png]
        """
        parser = MarkupParser(markup)
        page = parser.to_page()

        panel = page._panels[0]
        assert panel.background_image == "/path/to/image.png"

    def test_to_page_handles_background_description(self):
        """Test that text descriptions are stored for AI generation."""
        markup = """
        # panel 1
        [background: A sunny beach with palm trees]
        """
        parser = MarkupParser(markup)
        page = parser.to_page()

        panel = page._panels[0]
        assert panel.background_description == "A sunny beach with palm trees"


class TestParseMarkupFunction:
    """Tests for the top-level parse_markup function."""

    def test_parse_markup_returns_page(self):
        """Test that parse_markup returns a Page object."""
        page = parse_markup("[page 2x2]")
        assert isinstance(page, Page)

    def test_parse_markup_full_example(self):
        """Test parse_markup with a complete example."""
        markup = """
        [page 2x2]

        # panel 1
        철수(left, surprised): "뭐라고?!"
        영희(right, smug): "응, 진짜야"

        # panel 2
        철수(closeup): "..."
        sfx: 충격

        # panel 3
        [background: 카페 전경]
        narrator: "그날 이후..."

        # panel 4
        철수(center): "믿을 수 없어"
        """
        page = parse_markup(markup)

        assert isinstance(page, Page)
        assert len(page._panels) == 4

    def test_parse_markup_can_render(self):
        """Test that parsed markup can be rendered."""
        import tempfile
        import os

        markup = """
        [page 1x1]

        # panel 1
        Alice(left): "Hello!"
        """
        page = parse_markup(markup)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "test.svg")
            result = page.render(output_path)
            assert os.path.exists(result)


class TestEdgeCases:
    """Tests for edge cases and special scenarios."""

    def test_single_quotes_in_dialogue(self):
        """Test that single quotes work for dialogue."""
        markup = """
        # panel 1
        Alice(left): 'Hello world!'
        """
        parser = MarkupParser(markup)
        spec = parser.parse()

        action = spec.panels[0].actions[0]
        assert action.text == "Hello world!"

    def test_whitespace_handling(self):
        """Test handling of various whitespace."""
        markup = """

        [page 2x2]


        # panel 1

        Alice( left , happy ): "Hello!"

        """
        parser = MarkupParser(markup)
        spec = parser.parse()

        assert spec.rows == 2
        assert spec.cols == 2
        assert len(spec.panels) >= 1

    def test_multiple_characters_same_name(self):
        """Test that same character can speak multiple times."""
        markup = """
        # panel 1
        Alice(left): "First line"
        Bob(right): "Response"
        Alice(left): "Second line"
        """
        parser = MarkupParser(markup)
        spec = parser.parse()

        actions = spec.panels[0].actions
        assert len(actions) == 3
        assert actions[0].name == "Alice"
        assert actions[1].name == "Bob"
        assert actions[2].name == "Alice"

    def test_expression_names_are_valid(self):
        """Test all documented expression names."""
        expressions = ["neutral", "happy", "sad", "angry", "surprised", "confused",
                       "sleepy", "excited", "scared", "smirk", "crying"]
        for expr in expressions:
            markup = f"""
            # panel 1
            Alice({expr}): "Hello"
            """
            parser = MarkupParser(markup)
            spec = parser.parse()
            action = spec.panels[0].actions[0]
            assert action.expression == expr

    def test_position_names_are_valid(self):
        """Test all documented position names."""
        positions = ["left", "right", "center", "closeup", "top", "bottom"]
        for pos in positions:
            markup = f"""
            # panel 1
            Alice({pos}): "Hello"
            """
            parser = MarkupParser(markup)
            spec = parser.parse()
            action = spec.panels[0].actions[0]
            assert action.position == pos


class TestRenderIntegration:
    """Integration tests for rendering parsed markup."""

    def test_render_to_svg(self):
        """Test rendering parsed markup to SVG."""
        import tempfile
        import os

        markup = """
        [page 2x1]

        # panel 1
        Alice(left, happy): "Hello!"
        Bob(right): "Hi there!"

        # panel 2
        sfx: POW
        narrator: "The story continues..."
        """
        page = parse_markup(markup)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "comic.svg")
            result = page.render(output_path, format="svg")

            assert os.path.exists(result)
            with open(result, "r") as f:
                content = f.read()
                assert "<svg" in content
                assert "</svg>" in content


class TestParseError:
    """Tests for the ParseError exception class."""

    def test_parse_error_with_line_info(self):
        """Test ParseError includes line number and content."""
        error = ParseError("Test error", line_number=5, line="bad content")
        assert error.line_number == 5
        assert error.line == "bad content"
        assert "Line 5" in str(error)
        assert "Test error" in str(error)
        assert "bad content" in str(error)

    def test_parse_error_default_values(self):
        """Test ParseError with default values."""
        error = ParseError("Simple error")
        assert error.line_number == 0
        assert error.line == ""

    def test_parse_error_is_exception(self):
        """Test ParseError is a proper exception."""
        with pytest.raises(ParseError):
            raise ParseError("Test")


class TestParserExplicitFacingInMarkup:
    """Tests for explicit facing direction in markup."""

    def test_character_with_explicit_front_facing(self):
        """Test character with explicit front facing direction."""
        markup = """
        # panel 1
        Alice(center, happy, front): "Looking at you!"
        """
        parser = MarkupParser(markup)
        spec = parser.parse()

        action = spec.panels[0].actions[0]
        assert isinstance(action, CharacterAction)
        assert action.facing == "front"
        assert action.position == "center"
        assert action.expression == "happy"

    def test_character_with_explicit_back_facing(self):
        """Test character with explicit back facing direction."""
        markup = """
        # panel 1
        Alice(right, back): "Walking away..."
        """
        parser = MarkupParser(markup)
        spec = parser.parse()

        action = spec.panels[0].actions[0]
        assert isinstance(action, CharacterAction)
        assert action.facing == "back"
        # Position right normally defaults facing to left, but explicit back overrides
        assert action.position == "right"

    def test_smirk_expression_in_markup(self):
        """Test smirk expression is correctly parsed in full markup."""
        markup = """
        # panel 1
        Bob(right, smirk): "I told you so"
        """
        parser = MarkupParser(markup)
        spec = parser.parse()

        action = spec.panels[0].actions[0]
        assert isinstance(action, CharacterAction)
        assert action.expression == "smirk"
        assert action.name == "Bob"


class TestParserEdgeCases:
    """Tests for parser edge cases and uncovered code paths."""

    def test_unrecognized_hash_comments_ignored(self):
        """Test that unrecognized # lines are treated as comments (lines 193-194)."""
        markup = """
        # panel 1
        Alice(left): "Hello"
        # This is a comment, not a panel marker
        ## Another comment style
        ### Triple hash
        #not-a-panel
        Bob(right): "Hi"
        """
        parser = MarkupParser(markup)
        spec = parser.parse()

        # Should have 1 panel with 2 character actions
        assert len(spec.panels) >= 1
        assert len(spec.panels[0].actions) == 2
        assert spec.panels[0].actions[0].name == "Alice"
        assert spec.panels[0].actions[1].name == "Bob"

    def test_background_without_panel_marker(self):
        """Test background directive creates panel if none exists (lines 252-254)."""
        markup = """
        [background: A forest scene]
        """
        parser = MarkupParser(markup)
        spec = parser.parse()

        assert spec.rows == 1
        assert spec.cols == 1
        assert len(spec.panels) >= 1
        assert spec.panels[0].background == "A forest scene"

    def test_narrator_without_panel_marker(self):
        """Test narrator creates panel if none exists (lines 269-271)."""
        markup = """
        narrator: "Long ago, in a distant land..."
        """
        parser = MarkupParser(markup)
        spec = parser.parse()

        assert spec.rows == 1
        assert spec.cols == 1
        assert len(spec.panels) >= 1
        assert isinstance(spec.panels[0].actions[0], NarratorAction)
        assert spec.panels[0].actions[0].text == "Long ago, in a distant land..."

    def test_sfx_without_panel_marker(self):
        """Test SFX creates panel if none exists (lines 285-287)."""
        markup = """
        sfx: BOOM
        """
        parser = MarkupParser(markup)
        spec = parser.parse()

        assert spec.rows == 1
        assert spec.cols == 1
        assert len(spec.panels) >= 1
        assert isinstance(spec.panels[0].actions[0], SFXAction)
        assert spec.panels[0].actions[0].text == "BOOM"

    def test_character_without_panel_marker(self):
        """Test character dialogue creates panel if none exists."""
        markup = """
        Alice(left): "Hello world"
        """
        parser = MarkupParser(markup)
        spec = parser.parse()

        assert spec.rows == 1
        assert spec.cols == 1
        assert len(spec.panels) >= 1
        assert isinstance(spec.panels[0].actions[0], CharacterAction)

    def test_invalid_character_syntax_returns_false(self):
        """Test that malformed character syntax is ignored (line 319)."""
        markup = """
        # panel 1
        Alice(left): "Valid dialogue"
        This is not a valid character line
        Bob(right): "Also valid"
        """
        parser = MarkupParser(markup)
        spec = parser.parse()

        # Should have 2 valid actions, ignoring the invalid line
        assert len(spec.panels[0].actions) == 2
        assert spec.panels[0].actions[0].name == "Alice"
        assert spec.panels[0].actions[1].name == "Bob"

    def test_same_character_multiple_times_updates_expression(self):
        """Test that same character speaking multiple times reuses character and updates expression (lines 372-373)."""
        markup = """
        # panel 1
        Alice(left, happy): "First line"
        Alice(left, angry): "Second line - now angry!"
        """
        parser = MarkupParser(markup)
        page = parser.to_page()

        # Get the panel
        panel = page._panels[0]

        # Count characters and bubbles
        from comix.cobject.character.character import Stickman
        from comix.cobject.bubble.bubble import Bubble

        characters = [obj for obj in panel.submobjects if isinstance(obj, Stickman)]
        bubbles = [obj for obj in panel.submobjects if isinstance(obj, Bubble)]

        # Should have 1 character (reused) and 2 bubbles
        assert len(characters) == 1, "Character should be reused, not duplicated"
        assert len(bubbles) == 2, "Should have two speech bubbles"

        # The character should have the last expression set (angry)
        assert characters[0]._expression.name == "angry"

    def test_multiple_hash_comment_variations(self):
        """Test various hash comment formats are ignored."""
        markup = """
        # panel 1
        Alice(left): "Line 1"
        #this-looks-like-tag
        # random comment
        #123
        Bob(right): "Line 2"
        """
        parser = MarkupParser(markup)
        spec = parser.parse()

        # All non-standard # lines should be ignored
        assert len(spec.panels[0].actions) == 2

    def test_multiple_elements_without_page_declaration(self):
        """Test parsing multiple element types without page declaration."""
        markup = """
        narrator: "The story begins..."
        sfx: WHOOSH
        [background: dark alley]
        Alice(left): "Who's there?"
        """
        parser = MarkupParser(markup)
        spec = parser.parse()

        # Should create default 1x1 page and panel
        assert spec.rows == 1
        assert spec.cols == 1
        assert len(spec.panels) >= 1

        # All actions should be in the first panel
        actions = spec.panels[0].actions
        assert len(actions) == 4
        assert isinstance(actions[0], NarratorAction)
        assert isinstance(actions[1], SFXAction)
        assert isinstance(actions[2], BackgroundDirective)
        assert isinstance(actions[3], CharacterAction)


class TestBookMarkupParser:
    """Tests for multi-page book parsing functionality."""

    def test_basic_book_parsing(self):
        """Test parsing basic multi-page book markup."""
        from comix.parser import parse_book_markup

        markup = """
        [page 2x2]
        # panel 1
        Alice(left): "Page 1!"

        ===

        [page 1x2]
        # panel 1
        Bob(right): "Page 2!"
        """
        book = parse_book_markup(markup)

        assert book.page_count == 2
        assert len(book.pages[0]._panels) >= 1
        assert len(book.pages[1]._panels) >= 1

    def test_book_with_metadata_inline(self):
        """Test parsing book with metadata mixed in first section."""
        from comix.parser import parse_book_markup

        markup = """
        [book: My Comic]
        title: Test Comic
        author: Test Author

        [page 2x1]
        # panel 1
        Alice(left): "Hello!"

        ===

        [page 1x1]
        # panel 1
        Bob(right): "Bye!"
        """
        book = parse_book_markup(markup)

        assert book.title == "Test Comic"
        assert book.author == "Test Author"
        assert book.page_count == 2

    def test_book_with_separate_metadata_section(self):
        """Test parsing book with metadata in separate section."""
        from comix.parser import parse_book_markup

        markup = """
        [book]
        title: Separate Section Comic
        author: Author Name

        ===

        [page 2x2]
        # panel 1
        Alice(left): "First page!"

        ---

        [page 1x2]
        # panel 1
        Bob(right): "Second page!"
        """
        book = parse_book_markup(markup)

        assert book.title == "Separate Section Comic"
        assert book.author == "Author Name"
        assert book.page_count == 2

    def test_book_title_in_bracket(self):
        """Test parsing book title in bracket syntax."""
        from comix.parser import parse_book_markup

        markup = """
        [book: Inline Title]

        [page 1x1]
        # panel 1
        Alice(left): "Hello!"
        """
        book = parse_book_markup(markup)

        assert book.title == "Inline Title"
        assert book.page_count == 1

    def test_dash_separator(self):
        """Test parsing pages with --- separator."""
        from comix.parser import parse_book_markup

        markup = """
        [page 1x1]
        # panel 1
        Alice(left): "Page 1"

        ---

        [page 1x1]
        # panel 1
        Bob(right): "Page 2"

        ---

        [page 1x1]
        # panel 1
        Charlie(center): "Page 3"
        """
        book = parse_book_markup(markup)

        assert book.page_count == 3

    def test_equals_separator(self):
        """Test parsing pages with === separator."""
        from comix.parser import parse_book_markup

        markup = """
        [page 1x1]
        # panel 1
        Alice(left): "Page 1"

        ======

        [page 1x1]
        # panel 1
        Bob(right): "Page 2"
        """
        book = parse_book_markup(markup)

        assert book.page_count == 2

    def test_mixed_separators(self):
        """Test parsing pages with mixed === and --- separators."""
        from comix.parser import parse_book_markup

        markup = """
        [page 1x1]
        # panel 1
        Alice(left): "Page 1"

        ===

        [page 1x1]
        # panel 1
        Bob(right): "Page 2"

        ---

        [page 1x1]
        # panel 1
        Charlie(center): "Page 3"
        """
        book = parse_book_markup(markup)

        assert book.page_count == 3

    def test_single_page_no_separator(self):
        """Test parsing single page (no separators)."""
        from comix.parser import parse_book_markup

        markup = """
        [page 2x2]
        # panel 1
        Alice(left): "Hello!"
        # panel 2
        Bob(right): "Hi!"
        """
        book = parse_book_markup(markup)

        assert book.page_count == 1
        assert len(book.pages[0]._panels) >= 2

    def test_empty_sections_skipped(self):
        """Test that empty sections between separators are skipped."""
        from comix.parser import parse_book_markup

        markup = """
        [page 1x1]
        # panel 1
        Alice(left): "Page 1"

        ===

        ===

        [page 1x1]
        # panel 1
        Bob(right): "Page 2"
        """
        book = parse_book_markup(markup)

        assert book.page_count == 2

    def test_book_spec_dataclass(self):
        """Test BookSpec dataclass creation."""
        from comix.parser.parser import BookSpec, PageSpec

        spec = BookSpec(
            title="Test",
            author="Author",
            pages=[PageSpec(rows=1, cols=1), PageSpec(rows=2, cols=2)]
        )

        assert spec.title == "Test"
        assert spec.author == "Author"
        assert len(spec.pages) == 2

    def test_book_markup_parser_class(self):
        """Test BookMarkupParser class directly."""
        from comix.parser import BookMarkupParser

        markup = """
        [book: Direct Parser Test]
        author: Direct Author

        [page 1x1]
        # panel 1
        Alice(left): "Test"
        """
        parser = BookMarkupParser(markup)
        spec = parser.parse()

        assert spec.title == "Direct Parser Test"
        assert spec.author == "Direct Author"
        assert len(spec.pages) == 1

    def test_book_with_expressions_and_modifiers(self):
        """Test multi-page book with various expressions and modifiers."""
        from comix.parser import parse_book_markup

        markup = """
        [page 2x1]
        # panel 1
        Alice(left, happy): "I'm happy!"
        Bob(right, sad, thought): "I'm thinking..."

        ===

        [page 1x1]
        # panel 1
        Charlie(center, angry, shout): "I'M ANGRY!"
        """
        book = parse_book_markup(markup)

        assert book.page_count == 2

    def test_book_with_sfx_and_narrator(self):
        """Test multi-page book with SFX and narrator elements."""
        from comix.parser import parse_book_markup

        markup = """
        [page 1x1]
        # panel 1
        sfx: BOOM
        Alice(left): "What was that?"

        ===

        [page 1x1]
        # panel 1
        narrator: "The next day..."
        Bob(right): "All is calm now."
        """
        book = parse_book_markup(markup)

        assert book.page_count == 2

    def test_book_default_values(self):
        """Test book with no explicit title or author."""
        from comix.parser import parse_book_markup

        markup = """
        [page 1x1]
        # panel 1
        Alice(left): "No metadata"
        """
        book = parse_book_markup(markup)

        # BookSpec default is "Untitled", Book uses it as-is
        assert book.title == "Untitled"
        assert book.author == ""
        assert book.page_count == 1

    def test_book_korean_content(self):
        """Test multi-page book with Korean content."""
        from comix.parser import parse_book_markup

        markup = """
        [book: 한국어 만화]
        title: 나의 만화
        author: 김작가

        [page 2x1]
        # panel 1
        철수(left, happy): "안녕하세요!"

        ===

        [page 1x1]
        # panel 1
        영희(right, surprised): "오랜만이에요!"
        """
        book = parse_book_markup(markup)

        assert book.title == "나의 만화"
        assert book.author == "김작가"
        assert book.page_count == 2
