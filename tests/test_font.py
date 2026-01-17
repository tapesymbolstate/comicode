"""Tests for font management system."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from comix.style.font import (
    FontInfo,
    FontMetrics,
    FontRegistry,
    get_font_registry,
    get_default_metrics,
    estimate_text_width,
    estimate_text_height,
    is_fullwidth_char,
    calculate_text_width_with_cjk,
    _extract_font_metrics,
    _get_default_metrics,
    init_font_system,
)


class TestFontInfo:
    """Tests for FontInfo dataclass."""

    def test_default_init(self) -> None:
        """Test creating FontInfo with minimal parameters."""
        info = FontInfo(family="Arial", path=Path("/fonts/arial.ttf"))
        assert info.family == "Arial"
        assert info.path == Path("/fonts/arial.ttf")
        assert info.weight == "normal"
        assert info.style == "normal"
        assert info.full_name == "Arial"

    def test_custom_init(self) -> None:
        """Test creating FontInfo with all parameters."""
        info = FontInfo(
            family="Arial",
            path=Path("/fonts/arial-bold.ttf"),
            weight="bold",
            style="italic",
            full_name="Arial Bold Italic",
        )
        assert info.family == "Arial"
        assert info.weight == "bold"
        assert info.style == "italic"
        assert info.full_name == "Arial Bold Italic"


class TestFontMetrics:
    """Tests for FontMetrics dataclass."""

    def test_init(self) -> None:
        """Test creating FontMetrics."""
        metrics = FontMetrics(
            units_per_em=1000,
            ascender=800,
            descender=-200,
            x_height=500,
            cap_height=700,
            line_gap=0,
            avg_char_width=500,
        )
        assert metrics.units_per_em == 1000
        assert metrics.ascender == 800
        assert metrics.descender == -200

    def test_get_line_height(self) -> None:
        """Test calculating line height."""
        metrics = FontMetrics(
            units_per_em=1000,
            ascender=800,
            descender=-200,
            x_height=500,
            cap_height=700,
            line_gap=100,
            avg_char_width=500,
        )
        # line_height = (800 - (-200) + 100) / 1000 * 16 = 1100/1000 * 16 = 17.6
        line_height = metrics.get_line_height(16.0)
        assert line_height == pytest.approx(17.6)

    def test_get_text_height(self) -> None:
        """Test calculating text height."""
        metrics = FontMetrics(
            units_per_em=1000,
            ascender=800,
            descender=-200,
            x_height=500,
            cap_height=700,
            line_gap=0,
            avg_char_width=500,
        )
        # text_height = (800 - (-200)) / 1000 * 16 = 1000/1000 * 16 = 16
        text_height = metrics.get_text_height(16.0)
        assert text_height == pytest.approx(16.0)

    def test_get_char_width(self) -> None:
        """Test calculating character width."""
        metrics = FontMetrics(
            units_per_em=1000,
            ascender=800,
            descender=-200,
            x_height=500,
            cap_height=700,
            line_gap=0,
            avg_char_width=500,
        )
        # char_width = 500 / 1000 * 16 = 8
        char_width = metrics.get_char_width(16.0)
        assert char_width == pytest.approx(8.0)


class TestFontRegistry:
    """Tests for FontRegistry."""

    def test_init(self) -> None:
        """Test creating FontRegistry."""
        registry = FontRegistry()
        assert registry._fonts == {}
        assert "sans-serif" in registry._fallback_chains
        assert "serif" in registry._fallback_chains

    def test_register_font(self) -> None:
        """Test registering a font."""
        registry = FontRegistry()
        info = FontInfo(family="CustomFont", path=Path("/fonts/custom.ttf"))
        registry.register_font(info)

        assert "customfont:normal:normal" in registry._fonts
        assert "customfont" in registry._fonts

    def test_get_font_exact_match(self) -> None:
        """Test getting a font with exact match."""
        registry = FontRegistry()
        info = FontInfo(
            family="Arial",
            path=Path("/fonts/arial.ttf"),
            weight="normal",
            style="normal",
        )
        registry.register_font(info)

        result = registry.get_font("Arial", "normal", "normal")
        assert result == info

    def test_get_font_case_insensitive(self) -> None:
        """Test getting a font is case insensitive."""
        registry = FontRegistry()
        info = FontInfo(family="Arial", path=Path("/fonts/arial.ttf"))
        registry.register_font(info)

        result = registry.get_font("arial")
        assert result == info

        result = registry.get_font("ARIAL")
        assert result == info

    def test_get_font_not_found(self) -> None:
        """Test getting a font that doesn't exist."""
        registry = FontRegistry()
        result = registry.get_font("NonExistent")
        assert result is None

    def test_fallback_chain(self) -> None:
        """Test that fallback chain works."""
        registry = FontRegistry()
        # Register Arial as fallback for sans-serif
        info = FontInfo(family="Arial", path=Path("/fonts/arial.ttf"))
        registry.register_font(info)

        # Request sans-serif which should fallback to Arial
        result = registry.get_font("sans-serif")
        assert result == info

    def test_set_custom_fallback(self) -> None:
        """Test setting custom fallback chain."""
        registry = FontRegistry()

        # Register custom font
        custom = FontInfo(family="MyFont", path=Path("/fonts/myfont.ttf"))
        registry.register_font(custom)

        # Set MyFont as fallback for "comic"
        registry.set_fallback_chain("custom-family", ["MyFont"])

        result = registry.get_font("custom-family")
        assert result == custom


class TestGlobalRegistry:
    """Tests for global registry functions."""

    def test_get_font_registry(self) -> None:
        """Test getting global font registry."""
        registry = get_font_registry()
        assert isinstance(registry, FontRegistry)

        # Should return same instance
        registry2 = get_font_registry()
        assert registry is registry2

    def test_get_default_metrics(self) -> None:
        """Test getting default font metrics."""
        metrics = get_default_metrics()
        assert isinstance(metrics, FontMetrics)
        assert metrics.units_per_em == 1000
        assert metrics.ascender == 800
        assert metrics.descender == -200


class TestTextMeasurement:
    """Tests for text measurement functions."""

    def test_estimate_text_width(self) -> None:
        """Test estimating text width."""
        width = estimate_text_width("Hello", 16.0)
        # Using default metrics: 500/1000 * 16 = 8 per char, 5 chars = 40
        assert width == pytest.approx(40.0)

    def test_estimate_text_width_empty(self) -> None:
        """Test estimating width of empty text."""
        width = estimate_text_width("", 16.0)
        assert width == 0.0

    def test_estimate_text_height(self) -> None:
        """Test estimating text height."""
        height = estimate_text_height(16.0, line_height=1.0, num_lines=1)
        # Using default metrics: (800 - (-200))/1000 * 16 * 1.0 * 1 = 16
        assert height == pytest.approx(16.0)

    def test_estimate_text_height_multiline(self) -> None:
        """Test estimating height for multiple lines."""
        height = estimate_text_height(16.0, line_height=1.4, num_lines=3)
        # 16 * 1.4 * 3 = 67.2
        assert height == pytest.approx(67.2)


class TestFontDiscovery:
    """Tests for font discovery functionality."""

    def test_discover_system_fonts(self) -> None:
        """Test that font discovery runs without error."""
        registry = FontRegistry()
        # Just verify it runs - actual font count depends on system
        fonts_found = registry.discover_system_fonts()
        # Should find at least 0 fonts (may be more on systems with fonts)
        assert fonts_found >= 0

    def test_default_fallbacks_exist(self) -> None:
        """Test that default fallback chains are initialized."""
        registry = FontRegistry()
        assert "sans-serif" in registry._fallback_chains
        assert "serif" in registry._fallback_chains
        assert "monospace" in registry._fallback_chains
        assert "comic" in registry._fallback_chains


class TestCJKFullwidthDetection:
    """Tests for CJK full-width character detection."""

    def test_cjk_unified_ideographs(self) -> None:
        """Test detection of CJK Unified Ideographs (Chinese/Kanji)."""
        # Common Chinese/Kanji characters
        assert is_fullwidth_char("中") is True
        assert is_fullwidth_char("文") is True
        assert is_fullwidth_char("字") is True
        assert is_fullwidth_char("漢") is True

    def test_korean_hangul(self) -> None:
        """Test detection of Korean Hangul characters."""
        # Korean syllables
        assert is_fullwidth_char("가") is True
        assert is_fullwidth_char("한") is True
        assert is_fullwidth_char("글") is True
        assert is_fullwidth_char("철") is True
        assert is_fullwidth_char("수") is True
        # Hangul Jamo
        assert is_fullwidth_char("ㄱ") is True
        assert is_fullwidth_char("ㅏ") is True

    def test_japanese_hiragana(self) -> None:
        """Test detection of Japanese Hiragana."""
        assert is_fullwidth_char("あ") is True
        assert is_fullwidth_char("い") is True
        assert is_fullwidth_char("う") is True

    def test_japanese_katakana(self) -> None:
        """Test detection of Japanese Katakana."""
        assert is_fullwidth_char("ア") is True
        assert is_fullwidth_char("イ") is True
        assert is_fullwidth_char("ウ") is True

    def test_cjk_punctuation(self) -> None:
        """Test detection of CJK punctuation."""
        assert is_fullwidth_char("。") is True  # CJK full stop
        assert is_fullwidth_char("、") is True  # CJK comma
        assert is_fullwidth_char("「") is True  # CJK quote

    def test_fullwidth_ascii(self) -> None:
        """Test detection of fullwidth ASCII characters."""
        assert is_fullwidth_char("Ａ") is True  # Fullwidth A
        assert is_fullwidth_char("１") is True  # Fullwidth 1

    def test_halfwidth_ascii(self) -> None:
        """Test that regular ASCII is half-width."""
        assert is_fullwidth_char("A") is False
        assert is_fullwidth_char("Z") is False
        assert is_fullwidth_char("a") is False
        assert is_fullwidth_char("z") is False
        assert is_fullwidth_char("0") is False
        assert is_fullwidth_char("9") is False
        assert is_fullwidth_char(" ") is False
        assert is_fullwidth_char("!") is False
        assert is_fullwidth_char(".") is False

    def test_empty_string(self) -> None:
        """Test that empty string returns False."""
        assert is_fullwidth_char("") is False


class TestCJKTextWidthCalculation:
    """Tests for CJK-aware text width calculation."""

    def test_ascii_only(self) -> None:
        """Test width calculation for ASCII-only text."""
        # 5 chars * 0.5 * 16 = 40
        width = calculate_text_width_with_cjk("Hello", 16.0)
        assert width == pytest.approx(40.0)

    def test_cjk_only(self) -> None:
        """Test width calculation for CJK-only text."""
        # 2 chars * 1.0 * 16 = 32
        width = calculate_text_width_with_cjk("한글", 16.0)
        assert width == pytest.approx(32.0)

    def test_mixed_text(self) -> None:
        """Test width calculation for mixed ASCII and CJK text."""
        # "안녕 Hello" = 2 CJK + 1 space + 5 ASCII = 2*1.0 + 6*0.5 = 5.0 em
        # 5.0 * 16 = 80
        width = calculate_text_width_with_cjk("안녕 Hello", 16.0)
        assert width == pytest.approx(80.0)

    def test_korean_dialogue(self) -> None:
        """Test width calculation for typical Korean comic dialogue."""
        # "뭐라고?!" = 3 Korean + 2 ASCII = 3*1.0 + 2*0.5 = 4.0 em
        # 4.0 * 16 = 64
        width = calculate_text_width_with_cjk("뭐라고?!", 16.0)
        assert width == pytest.approx(64.0)

    def test_japanese_text(self) -> None:
        """Test width calculation for Japanese text."""
        # "こんにちは" = 5 hiragana * 1.0 * 16 = 80
        width = calculate_text_width_with_cjk("こんにちは", 16.0)
        assert width == pytest.approx(80.0)

    def test_chinese_text(self) -> None:
        """Test width calculation for Chinese text."""
        # "你好" = 2 characters * 1.0 * 16 = 32
        width = calculate_text_width_with_cjk("你好", 16.0)
        assert width == pytest.approx(32.0)

    def test_empty_text(self) -> None:
        """Test width calculation for empty text."""
        width = calculate_text_width_with_cjk("", 16.0)
        assert width == 0.0

    def test_custom_ratios(self) -> None:
        """Test width calculation with custom ratios."""
        # "A한" = 1 ASCII + 1 Korean
        # 1*0.6 + 1*0.9 = 1.5 em * 10 = 15
        width = calculate_text_width_with_cjk(
            "A한", 10.0, halfwidth_ratio=0.6, fullwidth_ratio=0.9
        )
        assert width == pytest.approx(15.0)


class TestEstimateTextWidthCJK:
    """Tests for estimate_text_width with CJK support."""

    def test_korean_text_wider_than_ascii(self) -> None:
        """Test that Korean text is measured wider than equivalent ASCII."""
        korean_width = estimate_text_width("한글", 16.0)  # 2 chars
        ascii_width = estimate_text_width("AB", 16.0)  # 2 chars
        # Korean should be approximately 2x wider (1.0 vs 0.5 em per char)
        assert korean_width > ascii_width

    def test_mixed_text(self) -> None:
        """Test that mixed text is measured correctly."""
        # "Hi 안녕" = 3 ASCII/space + 2 Korean
        width = estimate_text_width("Hi 안녕", 16.0)
        # With default metrics (0.5em for halfwidth), this should be:
        # 3 * 0.5 + 2 * 1.0 = 3.5 em * 16 = 56 (approximately)
        assert width > 0


class TestFontMetricsExtraction:
    """Tests for _extract_font_metrics and edge cases."""

    def test_get_default_metrics_values(self) -> None:
        """Test that default metrics have expected values."""
        metrics = _get_default_metrics()
        assert metrics.units_per_em == 1000
        assert metrics.ascender == 800
        assert metrics.descender == -200
        assert metrics.x_height == 500
        assert metrics.cap_height == 700
        assert metrics.line_gap == 0
        assert metrics.avg_char_width == 500

    def test_extract_metrics_nonexistent_file(self) -> None:
        """Test extracting metrics from nonexistent file returns defaults."""
        metrics = _extract_font_metrics(Path("/nonexistent/font.ttf"))
        default = _get_default_metrics()
        assert metrics.units_per_em == default.units_per_em
        assert metrics.ascender == default.ascender

    def test_extract_metrics_with_full_tables(self) -> None:
        """Test extracting metrics when all tables present."""
        mock_font = MagicMock()

        # Mock head table
        mock_head = MagicMock()
        mock_head.unitsPerEm = 2048

        # Mock OS/2 table
        mock_os2 = MagicMock()
        mock_os2.sTypoAscender = 1800
        mock_os2.sTypoDescender = -400
        mock_os2.sTypoLineGap = 90
        mock_os2.sxHeight = 1024
        mock_os2.sCapHeight = 1400
        mock_os2.xAvgCharWidth = 1024

        def mock_get(table_name: str) -> MagicMock | None:
            if table_name == "head":
                return mock_head
            elif table_name == "OS/2":
                return mock_os2
            return None

        mock_font.get = mock_get
        mock_font.close = MagicMock()

        with patch("comix.style.font.TTFont", return_value=mock_font):
            metrics = _extract_font_metrics(Path("/test/font.ttf"))

        assert metrics.units_per_em == 2048
        assert metrics.ascender == 1800
        assert metrics.descender == -400
        assert metrics.line_gap == 90
        assert metrics.x_height == 1024
        assert metrics.cap_height == 1400
        assert metrics.avg_char_width == 1024

    def test_extract_metrics_no_head_table(self) -> None:
        """Test extracting metrics when head table is missing."""
        mock_font = MagicMock()

        mock_os2 = MagicMock()
        mock_os2.sTypoAscender = 800
        mock_os2.sTypoDescender = -200
        mock_os2.sTypoLineGap = 0
        mock_os2.sxHeight = 500
        mock_os2.sCapHeight = 700
        mock_os2.xAvgCharWidth = 500

        def mock_get(table_name: str) -> MagicMock | None:
            if table_name == "OS/2":
                return mock_os2
            return None  # No head table

        mock_font.get = mock_get
        mock_font.close = MagicMock()

        with patch("comix.style.font.TTFont", return_value=mock_font):
            metrics = _extract_font_metrics(Path("/test/font.ttf"))

        # Should use default units_per_em of 1000
        assert metrics.units_per_em == 1000

    def test_extract_metrics_no_os2_uses_hhea(self) -> None:
        """Test extracting metrics falls back to hhea when OS/2 is missing."""
        mock_font = MagicMock()

        mock_head = MagicMock()
        mock_head.unitsPerEm = 1000

        mock_hhea = MagicMock()
        mock_hhea.ascent = 900
        mock_hhea.descent = -300
        mock_hhea.lineGap = 50

        def mock_get(table_name: str) -> MagicMock | None:
            if table_name == "head":
                return mock_head
            elif table_name == "hhea":
                return mock_hhea
            return None  # No OS/2 table

        mock_font.get = mock_get
        mock_font.close = MagicMock()

        with patch("comix.style.font.TTFont", return_value=mock_font):
            metrics = _extract_font_metrics(Path("/test/font.ttf"))

        assert metrics.ascender == 900
        assert metrics.descender == -300
        assert metrics.line_gap == 50
        # x_height and cap_height should be derived from units_per_em
        assert metrics.x_height == 500  # 1000 * 0.5
        assert metrics.cap_height == 700  # 1000 * 0.7

    def test_extract_metrics_no_os2_no_hhea(self) -> None:
        """Test extracting metrics when both OS/2 and hhea are missing."""
        mock_font = MagicMock()

        mock_head = MagicMock()
        mock_head.unitsPerEm = 2000

        def mock_get(table_name: str) -> MagicMock | None:
            if table_name == "head":
                return mock_head
            return None  # No OS/2 or hhea

        mock_font.get = mock_get
        mock_font.close = MagicMock()

        with patch("comix.style.font.TTFont", return_value=mock_font):
            metrics = _extract_font_metrics(Path("/test/font.ttf"))

        # Should use fallback values based on units_per_em
        assert metrics.units_per_em == 2000
        assert metrics.ascender == 1600  # 2000 * 0.8
        assert metrics.descender == -400  # 2000 * -0.2
        assert metrics.line_gap == 0

    def test_extract_metrics_os2_missing_sxheight(self) -> None:
        """Test extracting metrics when OS/2 lacks sxHeight attribute."""
        mock_font = MagicMock()

        mock_head = MagicMock()
        mock_head.unitsPerEm = 1000

        mock_os2 = MagicMock(spec=["sTypoAscender", "sTypoDescender", "sTypoLineGap", "xAvgCharWidth"])
        mock_os2.sTypoAscender = 800
        mock_os2.sTypoDescender = -200
        mock_os2.sTypoLineGap = 0
        mock_os2.xAvgCharWidth = 500
        # sxHeight and sCapHeight are missing

        def mock_get(table_name: str) -> MagicMock | None:
            if table_name == "head":
                return mock_head
            elif table_name == "OS/2":
                return mock_os2
            return None

        mock_font.get = mock_get
        mock_font.close = MagicMock()

        with patch("comix.style.font.TTFont", return_value=mock_font):
            metrics = _extract_font_metrics(Path("/test/font.ttf"))

        # Should fall back to calculated values
        assert metrics.x_height == 500  # 1000 * 0.5
        assert metrics.cap_height == 700  # 1000 * 0.7


class TestFontInfoLoading:
    """Tests for _load_font_info with mock fonts."""

    def test_load_font_with_no_name_table(self) -> None:
        """Test loading font when name table is missing."""
        mock_font = MagicMock()
        mock_font.get.return_value = None  # No name table
        mock_font.close = MagicMock()

        registry = FontRegistry()
        with patch("comix.style.font.TTFont", return_value=mock_font):
            result = registry._load_font_info(Path("/test/font.ttf"))

        assert result is None

    def test_load_font_with_no_family_uses_stem(self) -> None:
        """Test loading font uses filename when family name is missing."""
        mock_font = MagicMock()

        # Mock name table with no family name
        mock_name_table = MagicMock()
        mock_name_table.names = []  # Empty names

        mock_os2 = MagicMock()
        mock_os2.usWeightClass = 400
        mock_os2.fsSelection = 0

        def mock_get(table_name: str) -> MagicMock | None:
            if table_name == "name":
                return mock_name_table
            elif table_name == "OS/2":
                return mock_os2
            return None

        mock_font.get = mock_get
        mock_font.close = MagicMock()

        registry = FontRegistry()
        with patch("comix.style.font.TTFont", return_value=mock_font):
            result = registry._load_font_info(Path("/test/MyCustomFont.ttf"))

        assert result is not None
        assert result.family == "MyCustomFont"  # Uses stem of filename

    def test_load_font_detect_bold_weight(self) -> None:
        """Test loading font detects bold weight from OS/2 table."""
        mock_font = MagicMock()

        mock_name_record = MagicMock()
        mock_name_record.nameID = 1
        mock_name_record.toUnicode.return_value = "Arial"

        mock_name_table = MagicMock()
        mock_name_table.names = [mock_name_record]

        mock_os2 = MagicMock()
        mock_os2.usWeightClass = 700  # Bold
        mock_os2.fsSelection = 0

        def mock_get(table_name: str) -> MagicMock | None:
            if table_name == "name":
                return mock_name_table
            elif table_name == "OS/2":
                return mock_os2
            return None

        mock_font.get = mock_get
        mock_font.close = MagicMock()

        registry = FontRegistry()
        with patch("comix.style.font.TTFont", return_value=mock_font):
            result = registry._load_font_info(Path("/test/arial-bold.ttf"))

        assert result is not None
        assert result.weight == "bold"

    def test_load_font_detect_light_weight(self) -> None:
        """Test loading font detects light weight from OS/2 table."""
        mock_font = MagicMock()

        mock_name_record = MagicMock()
        mock_name_record.nameID = 1
        mock_name_record.toUnicode.return_value = "Helvetica"

        mock_name_table = MagicMock()
        mock_name_table.names = [mock_name_record]

        mock_os2 = MagicMock()
        mock_os2.usWeightClass = 300  # Light
        mock_os2.fsSelection = 0

        def mock_get(table_name: str) -> MagicMock | None:
            if table_name == "name":
                return mock_name_table
            elif table_name == "OS/2":
                return mock_os2
            return None

        mock_font.get = mock_get
        mock_font.close = MagicMock()

        registry = FontRegistry()
        with patch("comix.style.font.TTFont", return_value=mock_font):
            result = registry._load_font_info(Path("/test/helvetica-light.ttf"))

        assert result is not None
        assert result.weight == "light"

    def test_load_font_detect_italic_style(self) -> None:
        """Test loading font detects italic style from OS/2 table."""
        mock_font = MagicMock()

        mock_name_record = MagicMock()
        mock_name_record.nameID = 1
        mock_name_record.toUnicode.return_value = "Times"

        mock_name_table = MagicMock()
        mock_name_table.names = [mock_name_record]

        mock_os2 = MagicMock()
        mock_os2.usWeightClass = 400
        mock_os2.fsSelection = 1  # Italic bit set

        def mock_get(table_name: str) -> MagicMock | None:
            if table_name == "name":
                return mock_name_table
            elif table_name == "OS/2":
                return mock_os2
            return None

        mock_font.get = mock_get
        mock_font.close = MagicMock()

        registry = FontRegistry()
        with patch("comix.style.font.TTFont", return_value=mock_font):
            result = registry._load_font_info(Path("/test/times-italic.ttf"))

        assert result is not None
        assert result.style == "italic"

    def test_load_font_no_os2_table(self) -> None:
        """Test loading font when OS/2 table is missing."""
        mock_font = MagicMock()

        mock_name_record = MagicMock()
        mock_name_record.nameID = 1
        mock_name_record.toUnicode.return_value = "SimpleFont"

        mock_name_table = MagicMock()
        mock_name_table.names = [mock_name_record]

        def mock_get(table_name: str) -> MagicMock | None:
            if table_name == "name":
                return mock_name_table
            return None  # No OS/2 table

        mock_font.get = mock_get
        mock_font.close = MagicMock()

        registry = FontRegistry()
        with patch("comix.style.font.TTFont", return_value=mock_font):
            result = registry._load_font_info(Path("/test/simple.ttf"))

        assert result is not None
        assert result.weight == "normal"
        assert result.style == "normal"

    def test_load_font_exception_returns_none(self) -> None:
        """Test loading font returns None on exception."""
        registry = FontRegistry()
        with patch("comix.style.font.TTFont", side_effect=Exception("Font error")):
            result = registry._load_font_info(Path("/test/corrupt.ttf"))

        assert result is None

    def test_load_font_with_full_name(self) -> None:
        """Test loading font extracts full name from name table."""
        mock_font = MagicMock()

        mock_family_record = MagicMock()
        mock_family_record.nameID = 1
        mock_family_record.toUnicode.return_value = "Arial"

        mock_fullname_record = MagicMock()
        mock_fullname_record.nameID = 4
        mock_fullname_record.toUnicode.return_value = "Arial Bold Italic"

        mock_name_table = MagicMock()
        mock_name_table.names = [mock_family_record, mock_fullname_record]

        mock_os2 = MagicMock()
        mock_os2.usWeightClass = 700
        mock_os2.fsSelection = 1

        def mock_get(table_name: str) -> MagicMock | None:
            if table_name == "name":
                return mock_name_table
            elif table_name == "OS/2":
                return mock_os2
            return None

        mock_font.get = mock_get
        mock_font.close = MagicMock()

        registry = FontRegistry()
        with patch("comix.style.font.TTFont", return_value=mock_font):
            result = registry._load_font_info(Path("/test/arial-bolditalic.ttf"))

        assert result is not None
        assert result.full_name == "Arial Bold Italic"


class TestFontDirectoryScanning:
    """Tests for _scan_font_directory."""

    def test_scan_directory_empty(self, tmp_path: Path) -> None:
        """Test scanning empty directory."""
        registry = FontRegistry()
        fonts_found = registry._scan_font_directory(tmp_path)
        assert fonts_found == 0

    def test_scan_directory_ignores_non_fonts(self, tmp_path: Path) -> None:
        """Test scanning directory ignores non-font files."""
        # Create non-font files
        (tmp_path / "readme.txt").write_text("test")
        (tmp_path / "image.png").write_bytes(b"\x89PNG")
        (tmp_path / "script.py").write_text("print('hello')")

        registry = FontRegistry()
        fonts_found = registry._scan_font_directory(tmp_path)
        assert fonts_found == 0

    def test_scan_directory_with_font_extensions(self, tmp_path: Path) -> None:
        """Test scanning recognizes all font extensions."""
        # Create dummy font files - they won't parse but we can test extension detection
        registry = FontRegistry()

        # Create files with valid extensions
        font_extensions = [".ttf", ".otf", ".ttc", ".woff", ".woff2"]
        for ext in font_extensions:
            (tmp_path / f"font{ext}").write_bytes(b"dummy")

        # Mock _load_font_info to return None (simulating invalid fonts)
        with patch.object(registry, "_load_font_info", return_value=None):
            fonts_found = registry._scan_font_directory(tmp_path)

        # No fonts found since _load_font_info returns None
        assert fonts_found == 0

    def test_scan_directory_recursive(self, tmp_path: Path) -> None:
        """Test scanning recurses into subdirectories."""
        # Create nested directory structure
        subdir = tmp_path / "subdir" / "nested"
        subdir.mkdir(parents=True)

        registry = FontRegistry()

        # Create a font that can be "loaded"
        mock_info = FontInfo(family="NestedFont", path=subdir / "nested.ttf")

        with patch.object(registry, "_load_font_info", return_value=mock_info):
            # Create the file
            (subdir / "nested.ttf").write_bytes(b"dummy")
            fonts_found = registry._scan_font_directory(tmp_path)

        assert fonts_found == 1

    def test_scan_directory_counts_valid_fonts(self, tmp_path: Path) -> None:
        """Test scanning counts only valid fonts."""
        registry = FontRegistry()

        # Create font files
        (tmp_path / "font1.ttf").write_bytes(b"dummy")
        (tmp_path / "font2.otf").write_bytes(b"dummy")
        (tmp_path / "font3.ttf").write_bytes(b"dummy")

        call_count = 0

        def mock_load(path: Path) -> FontInfo | None:
            nonlocal call_count
            call_count += 1
            # Return valid info for first two, None for third
            if call_count <= 2:
                return FontInfo(family=f"Font{call_count}", path=path)
            return None

        with patch.object(registry, "_load_font_info", side_effect=mock_load):
            fonts_found = registry._scan_font_directory(tmp_path)

        assert fonts_found == 2


class TestPlatformFontDiscovery:
    """Tests for platform-specific font discovery methods."""

    def test_discover_macos_fonts_all_dirs(self) -> None:
        """Test macOS font discovery scans all font directories."""
        registry = FontRegistry()

        scanned_dirs: list[Path] = []

        def mock_scan(directory: Path) -> int:
            scanned_dirs.append(directory)
            return 5

        with patch.object(registry, "_scan_font_directory", side_effect=mock_scan):
            with patch("pathlib.Path.exists", return_value=True):
                fonts_found = registry._discover_macos_fonts()

        # Should scan 3 directories
        assert len(scanned_dirs) == 3
        assert fonts_found == 15  # 5 * 3

    def test_discover_macos_fonts_missing_dirs(self) -> None:
        """Test macOS font discovery handles missing directories."""
        registry = FontRegistry()

        def mock_exists(self: Path) -> bool:
            # Only /Library/Fonts exists
            return str(self) == "/Library/Fonts"

        with patch.object(registry, "_scan_font_directory", return_value=10):
            with patch.object(Path, "exists", mock_exists):
                fonts_found = registry._discover_macos_fonts()

        assert fonts_found == 10  # Only one directory scanned

    def test_discover_linux_with_fc_list(self) -> None:
        """Test Linux font discovery uses fc-list successfully."""
        registry = FontRegistry()

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "/usr/share/fonts/font1.ttf\n/usr/share/fonts/font2.ttf\n"

        mock_info = FontInfo(family="TestFont", path=Path("/test.ttf"))

        with patch("subprocess.run", return_value=mock_result):
            with patch("pathlib.Path.exists", return_value=True):
                with patch.object(registry, "_load_font_info", return_value=mock_info):
                    fonts_found = registry._discover_linux_fonts()

        assert fonts_found == 2

    def test_discover_linux_fc_list_timeout(self) -> None:
        """Test Linux font discovery falls back on fc-list timeout."""
        registry = FontRegistry()

        import subprocess
        with patch("subprocess.run", side_effect=subprocess.TimeoutExpired("fc-list", 10)):
            with patch("pathlib.Path.exists", return_value=False):
                fonts_found = registry._discover_linux_fonts()

        # Falls back to scanning directories, but none exist
        assert fonts_found == 0

    def test_discover_linux_fc_list_not_found(self) -> None:
        """Test Linux font discovery falls back when fc-list not found."""
        registry = FontRegistry()

        with patch("subprocess.run", side_effect=FileNotFoundError()):
            with patch.object(registry, "_scan_font_directory", return_value=3):
                with patch("pathlib.Path.exists", return_value=True):
                    fonts_found = registry._discover_linux_fonts()

        # Falls back to scanning 4 directories
        assert fonts_found == 12  # 3 * 4

    def test_discover_linux_fallback_dirs(self) -> None:
        """Test Linux font discovery scans correct fallback directories."""
        registry = FontRegistry()

        scanned_dirs: list[Path] = []

        def mock_scan(directory: Path) -> int:
            scanned_dirs.append(directory)
            return 1

        with patch("subprocess.run", side_effect=FileNotFoundError()):
            with patch.object(registry, "_scan_font_directory", side_effect=mock_scan):
                with patch("pathlib.Path.exists", return_value=True):
                    registry._discover_linux_fonts()

        # Check expected directories
        dir_strs = [str(d) for d in scanned_dirs]
        assert any("/usr/share/fonts" in d for d in dir_strs)
        assert any("/usr/local/share/fonts" in d for d in dir_strs)

    def test_discover_windows_fonts(self) -> None:
        """Test Windows font discovery."""
        registry = FontRegistry()

        with patch.dict("os.environ", {"WINDIR": "C:\\Windows"}):
            with patch("pathlib.Path.exists", return_value=True):
                with patch.object(registry, "_scan_font_directory", return_value=50):
                    fonts_found = registry._discover_windows_fonts()

        assert fonts_found == 50

    def test_discover_windows_custom_windir(self) -> None:
        """Test Windows font discovery with custom WINDIR."""
        registry = FontRegistry()

        scanned_dir: Path | None = None

        def mock_scan(directory: Path) -> int:
            nonlocal scanned_dir
            scanned_dir = directory
            return 10

        with patch.dict("os.environ", {"WINDIR": "D:\\CustomWindows"}):
            with patch("pathlib.Path.exists", return_value=True):
                with patch.object(registry, "_scan_font_directory", side_effect=mock_scan):
                    registry._discover_windows_fonts()

        assert scanned_dir is not None
        assert "CustomWindows" in str(scanned_dir)

    def test_discover_windows_dir_not_exists(self) -> None:
        """Test Windows font discovery when fonts directory doesn't exist."""
        registry = FontRegistry()

        with patch("pathlib.Path.exists", return_value=False):
            fonts_found = registry._discover_windows_fonts()

        assert fonts_found == 0

    def test_discover_system_fonts_dispatches_by_platform(self) -> None:
        """Test discover_system_fonts calls correct platform method."""
        registry = FontRegistry()

        with patch("platform.system", return_value="Darwin"):
            with patch.object(registry, "_discover_macos_fonts", return_value=100) as mock_mac:
                fonts_found = registry.discover_system_fonts()
                mock_mac.assert_called_once()
                assert fonts_found == 100

        with patch("platform.system", return_value="Linux"):
            with patch.object(registry, "_discover_linux_fonts", return_value=50) as mock_linux:
                fonts_found = registry.discover_system_fonts()
                mock_linux.assert_called_once()
                assert fonts_found == 50

        with patch("platform.system", return_value="Windows"):
            with patch.object(registry, "_discover_windows_fonts", return_value=75) as mock_win:
                fonts_found = registry.discover_system_fonts()
                mock_win.assert_called_once()
                assert fonts_found == 75


class TestFontMetricsCaching:
    """Tests for metrics caching behavior."""

    def test_get_metrics_cache_miss(self) -> None:
        """Test getting metrics for uncached font."""
        registry = FontRegistry()
        font_info = FontInfo(family="TestFont", path=Path("/test/font.ttf"))

        expected_metrics = FontMetrics(
            units_per_em=2000,
            ascender=1600,
            descender=-400,
            x_height=1000,
            cap_height=1400,
            line_gap=50,
            avg_char_width=1000,
        )

        with patch("comix.style.font._extract_font_metrics", return_value=expected_metrics):
            metrics = registry.get_metrics(font_info)

        assert metrics == expected_metrics
        assert str(font_info.path) in registry._metrics_cache

    def test_get_metrics_cache_hit(self) -> None:
        """Test getting metrics uses cache on second call."""
        registry = FontRegistry()
        font_info = FontInfo(family="TestFont", path=Path("/test/font.ttf"))

        expected_metrics = FontMetrics(
            units_per_em=2000,
            ascender=1600,
            descender=-400,
            x_height=1000,
            cap_height=1400,
            line_gap=50,
            avg_char_width=1000,
        )

        with patch("comix.style.font._extract_font_metrics", return_value=expected_metrics) as mock_extract:
            # First call - cache miss
            metrics1 = registry.get_metrics(font_info)
            # Second call - should hit cache
            metrics2 = registry.get_metrics(font_info)

        # _extract_font_metrics should only be called once
        mock_extract.assert_called_once()
        assert metrics1 == metrics2

    def test_get_metrics_for_family_font_exists(self) -> None:
        """Test getting metrics for a registered font family."""
        registry = FontRegistry()
        font_info = FontInfo(family="Arial", path=Path("/test/arial.ttf"))
        registry.register_font(font_info)

        expected_metrics = FontMetrics(
            units_per_em=1000,
            ascender=800,
            descender=-200,
            x_height=500,
            cap_height=700,
            line_gap=0,
            avg_char_width=500,
        )

        with patch("comix.style.font._extract_font_metrics", return_value=expected_metrics):
            metrics = registry.get_metrics_for_family("Arial")

        assert metrics == expected_metrics

    def test_get_metrics_for_family_font_not_found(self) -> None:
        """Test getting metrics for unregistered font returns None."""
        registry = FontRegistry()
        metrics = registry.get_metrics_for_family("NonExistentFont")
        assert metrics is None


class TestFontSystemInit:
    """Tests for init_font_system."""

    def test_init_with_discovery(self) -> None:
        """Test init_font_system with font discovery enabled."""
        # Reset global registry
        import comix.style.font as font_module
        font_module._global_registry = None

        with patch.object(FontRegistry, "discover_system_fonts", return_value=100) as mock_discover:
            registry = init_font_system(discover_system_fonts=True)
            mock_discover.assert_called_once()

        assert isinstance(registry, FontRegistry)

    def test_init_without_discovery(self) -> None:
        """Test init_font_system without font discovery."""
        # Reset global registry
        import comix.style.font as font_module
        font_module._global_registry = None

        with patch.object(FontRegistry, "discover_system_fonts") as mock_discover:
            registry = init_font_system(discover_system_fonts=False)
            mock_discover.assert_not_called()

        assert isinstance(registry, FontRegistry)

    def test_init_returns_global_registry(self) -> None:
        """Test init_font_system returns the global registry."""
        # Reset global registry
        import comix.style.font as font_module
        font_module._global_registry = None

        registry1 = init_font_system(discover_system_fonts=False)
        registry2 = get_font_registry()

        assert registry1 is registry2


class TestCJKExtendedRanges:
    """Tests for all CJK Unicode ranges."""

    def test_cjk_extension_a(self) -> None:
        """Test CJK Extension A range (0x3400-0x4DBF)."""
        # First and last characters of Extension A
        assert is_fullwidth_char("\u3400") is True  # CJK Extension A start
        assert is_fullwidth_char("\u4DBF") is True  # CJK Extension A end
        # Middle of range
        assert is_fullwidth_char("\u4000") is True

    def test_cjk_extension_b_and_beyond(self) -> None:
        """Test CJK Extension B-F range (0x20000-0x2EBEF)."""
        # These are surrogate pairs in UTF-16 but Python handles them
        assert is_fullwidth_char("\U00020000") is True  # Extension B start
        assert is_fullwidth_char("\U0002A6DF") is True  # Extension B end
        # Extension C, D, E, F
        assert is_fullwidth_char("\U0002A700") is True  # Extension C
        assert is_fullwidth_char("\U0002B820") is True  # Extension E

    def test_hangul_jamo(self) -> None:
        """Test Korean Hangul Jamo range (0x1100-0x11FF)."""
        assert is_fullwidth_char("\u1100") is True  # Hangul Jamo start
        assert is_fullwidth_char("\u11FF") is True  # Hangul Jamo end
        assert is_fullwidth_char("\u1150") is True  # Middle

    def test_hangul_compatibility_jamo(self) -> None:
        """Test Korean Hangul Compatibility Jamo (0x3130-0x318F)."""
        assert is_fullwidth_char("\u3130") is True  # Start (reserved)
        assert is_fullwidth_char("\u318F") is True  # End
        assert is_fullwidth_char("\u3131") is True  # ㄱ (kiyeok)
        assert is_fullwidth_char("\u314F") is True  # ㅏ (a)

    def test_katakana_phonetic_extensions(self) -> None:
        """Test Katakana Phonetic Extensions (0x31F0-0x31FF)."""
        assert is_fullwidth_char("\u31F0") is True  # Start
        assert is_fullwidth_char("\u31FF") is True  # End

    def test_cjk_compatibility_forms(self) -> None:
        """Test CJK Compatibility Forms (0xFE30-0xFE4F)."""
        assert is_fullwidth_char("\uFE30") is True  # Start (vertical two-dot leader)
        assert is_fullwidth_char("\uFE4F") is True  # End
        assert is_fullwidth_char("\uFE35") is True  # Vertical left parenthesis

    def test_fullwidth_forms_range(self) -> None:
        """Test Fullwidth ASCII and Punctuation (0xFF00-0xFFEF)."""
        assert is_fullwidth_char("\uFF01") is True  # Fullwidth exclamation
        assert is_fullwidth_char("\uFF21") is True  # Fullwidth A
        assert is_fullwidth_char("\uFF41") is True  # Fullwidth a
        assert is_fullwidth_char("\uFF10") is True  # Fullwidth 0

    def test_cjk_symbols_and_punctuation(self) -> None:
        """Test CJK Symbols and Punctuation (0x3000-0x303F)."""
        assert is_fullwidth_char("\u3000") is True  # Ideographic space
        assert is_fullwidth_char("\u3001") is True  # Ideographic comma
        assert is_fullwidth_char("\u3002") is True  # Ideographic full stop
        assert is_fullwidth_char("\u300C") is True  # Left corner bracket
        assert is_fullwidth_char("\u300D") is True  # Right corner bracket


class TestFallbackChainAdvanced:
    """Tests for fallback with weight/style."""

    def test_fallback_with_weight_and_style(self) -> None:
        """Test fallback chain considers weight and style."""
        registry = FontRegistry()

        # Register Arial Bold
        arial_bold = FontInfo(
            family="Arial",
            path=Path("/fonts/arial-bold.ttf"),
            weight="bold",
            style="normal",
        )
        registry.register_font(arial_bold)

        # Request sans-serif bold - should find Arial Bold
        result = registry.get_font("sans-serif", "bold", "normal")
        assert result == arial_bold

    def test_fallback_multiple_attempts(self) -> None:
        """Test fallback tries multiple fonts in chain."""
        registry = FontRegistry()

        # Don't register Arial (first in sans-serif chain)
        # Register Helvetica (second in chain)
        helvetica = FontInfo(
            family="Helvetica Neue",
            path=Path("/fonts/helvetica-neue.ttf"),
        )
        registry.register_font(helvetica)

        # Request sans-serif - should skip Arial and find Helvetica
        result = registry.get_font("sans-serif")
        assert result == helvetica

    def test_fallback_exact_match_in_chain(self) -> None:
        """Test fallback finds exact weight/style match in chain."""
        registry = FontRegistry()

        # Register Arial normal
        arial_normal = FontInfo(
            family="Arial",
            path=Path("/fonts/arial.ttf"),
            weight="normal",
            style="normal",
        )
        # Register Arial italic
        arial_italic = FontInfo(
            family="Arial",
            path=Path("/fonts/arial-italic.ttf"),
            weight="normal",
            style="italic",
        )
        registry.register_font(arial_normal)
        registry.register_font(arial_italic)

        # Request sans-serif italic - should find Arial italic via fallback
        result = registry.get_font("sans-serif", "normal", "italic")
        assert result == arial_italic


class TestEdgeCases:
    """Tests for edge cases and error conditions."""

    def test_estimate_text_width_zero_font_size(self) -> None:
        """Test estimate_text_width handles zero font size."""
        width = estimate_text_width("Hello", 0.0)
        assert width == 0.0

    def test_calculate_text_width_with_zero_size(self) -> None:
        """Test calculate_text_width_with_cjk handles zero font size."""
        width = calculate_text_width_with_cjk("Hello", 0.0)
        assert width == 0.0

    def test_font_metrics_methods_with_zero_size(self) -> None:
        """Test FontMetrics methods handle zero font size."""
        metrics = FontMetrics(
            units_per_em=1000,
            ascender=800,
            descender=-200,
            x_height=500,
            cap_height=700,
            line_gap=0,
            avg_char_width=500,
        )
        assert metrics.get_line_height(0.0) == 0.0
        assert metrics.get_text_height(0.0) == 0.0
        assert metrics.get_char_width(0.0) == 0.0

    def test_make_key_lowercase_family(self) -> None:
        """Test _make_key normalizes family to lowercase."""
        # _make_key only lowercases the family name, preserves weight/style
        key1 = FontRegistry._make_key("Arial", "normal", "normal")
        key2 = FontRegistry._make_key("arial", "normal", "normal")
        key3 = FontRegistry._make_key("ARIAL", "normal", "normal")

        assert key1 == key2 == key3
        assert key1 == "arial:normal:normal"

    def test_estimate_text_height_zero_lines(self) -> None:
        """Test estimate_text_height with zero lines."""
        height = estimate_text_height(16.0, num_lines=0)
        assert height == 0.0

    def test_is_fullwidth_char_requires_single_char(self) -> None:
        """Test is_fullwidth_char requires single character input."""
        # Function uses ord() which requires a single character
        # Verify it raises TypeError for multi-char strings
        with pytest.raises(TypeError):
            is_fullwidth_char("AB")  # Two ASCII chars

        with pytest.raises(TypeError):
            is_fullwidth_char("한글")  # Two Korean chars

        # But single chars should work
        assert is_fullwidth_char("A") is False
        assert is_fullwidth_char("한") is True
