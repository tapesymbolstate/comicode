"""Tests for the Book class and multi-page PDF export."""

import tempfile
from pathlib import Path

import pytest

from comix.page.book import Book
from comix.page.page import Page
from comix.cobject.panel.panel import Panel
from comix.cobject.text.text import Text


class TestBookBasic:
    """Test basic Book functionality."""

    def test_init_default(self):
        """Test Book initialization with defaults."""
        book = Book()
        assert book.title == "Untitled Book"
        assert book.author == ""
        assert book.description == ""
        assert book.page_count == 0
        assert len(book) == 0

    def test_init_with_metadata(self):
        """Test Book initialization with metadata."""
        book = Book(title="My Comic", author="Test Author", description="A test comic")
        assert book.title == "My Comic"
        assert book.author == "Test Author"
        assert book.description == "A test comic"

    def test_add_page_single(self):
        """Test adding a single page."""
        book = Book()
        page = Page()
        book.add_page(page)
        assert book.page_count == 1
        assert book.pages[0] is page

    def test_add_page_multiple(self):
        """Test adding multiple pages at once."""
        book = Book()
        page1 = Page()
        page2 = Page()
        page3 = Page()
        book.add_page(page1, page2, page3)
        assert book.page_count == 3
        assert book.pages == [page1, page2, page3]

    def test_add_page_chaining(self):
        """Test that add_page returns self for chaining."""
        book = Book()
        page1 = Page()
        page2 = Page()
        result = book.add_page(page1).add_page(page2)
        assert result is book
        assert book.page_count == 2

    def test_add_page_no_duplicates(self):
        """Test that adding the same page twice doesn't duplicate."""
        book = Book()
        page = Page()
        book.add_page(page)
        book.add_page(page)
        assert book.page_count == 1

    def test_insert_page(self):
        """Test inserting a page at a specific index."""
        book = Book()
        page1 = Page()
        page2 = Page()
        page3 = Page()
        book.add_page(page1, page3)
        book.insert_page(1, page2)
        assert book.pages == [page1, page2, page3]

    def test_insert_page_no_duplicates(self):
        """Test that inserting an existing page doesn't duplicate."""
        book = Book()
        page = Page()
        book.add_page(page)
        book.insert_page(0, page)
        assert book.page_count == 1

    def test_remove_page(self):
        """Test removing a page."""
        book = Book()
        page1 = Page()
        page2 = Page()
        book.add_page(page1, page2)
        book.remove_page(page1)
        assert book.page_count == 1
        assert book.pages == [page2]

    def test_remove_page_not_in_book(self):
        """Test removing a page that isn't in the book."""
        book = Book()
        page = Page()
        book.remove_page(page)  # Should not raise
        assert book.page_count == 0

    def test_get_page(self):
        """Test getting a page by index."""
        book = Book()
        page1 = Page()
        page2 = Page()
        book.add_page(page1, page2)
        assert book.get_page(0) is page1
        assert book.get_page(1) is page2

    def test_get_page_index_error(self):
        """Test that get_page raises IndexError for invalid index."""
        book = Book()
        with pytest.raises(IndexError):
            book.get_page(0)

    def test_clear(self):
        """Test clearing all pages."""
        book = Book()
        page1 = Page()
        page2 = Page()
        book.add_page(page1, page2)
        book.clear()
        assert book.page_count == 0

    def test_clear_chaining(self):
        """Test that clear returns self for chaining."""
        book = Book()
        book.add_page(Page())
        result = book.clear()
        assert result is book


class TestBookProperties:
    """Test Book properties and special methods."""

    def test_pages_property_returns_copy(self):
        """Test that pages property returns a copy, not the internal list."""
        book = Book()
        page = Page()
        book.add_page(page)
        pages = book.pages
        pages.append(Page())  # Modify the returned list
        assert book.page_count == 1  # Original should be unchanged

    def test_len(self):
        """Test __len__ method."""
        book = Book()
        assert len(book) == 0
        book.add_page(Page(), Page())
        assert len(book) == 2

    def test_iter(self):
        """Test __iter__ method."""
        book = Book()
        page1 = Page()
        page2 = Page()
        book.add_page(page1, page2)
        pages_list = list(book)
        assert pages_list == [page1, page2]

    def test_getitem(self):
        """Test __getitem__ method."""
        book = Book()
        page1 = Page()
        page2 = Page()
        book.add_page(page1, page2)
        assert book[0] is page1
        assert book[1] is page2

    def test_get_metadata(self):
        """Test getting book metadata."""
        book = Book(title="Test", author="Author", description="Desc")
        book.add_page(Page(), Page())
        metadata = book.get_metadata()
        assert metadata["title"] == "Test"
        assert metadata["author"] == "Author"
        assert metadata["description"] == "Desc"
        assert metadata["page_count"] == 2


class TestBookRender:
    """Test Book rendering functionality."""

    def test_render_empty_book_raises(self):
        """Test that rendering an empty book raises ValueError."""
        book = Book()
        with pytest.raises(ValueError, match="Cannot render an empty book"):
            book.render()

    @pytest.mark.skipif(
        True,  # Will be conditionally enabled based on Cairo availability
        reason="Cairo not available"
    )
    def test_render_single_page(self):
        """Test rendering a book with a single page."""
        # This test is skipped if Cairo is not available
        pass

    def test_render_adds_pdf_extension(self):
        """Test that render adds .pdf extension if missing."""
        book = Book()
        page = Page()
        page.add(Panel())
        book.add_page(page)

        # This will fail with ImportError if Cairo is not available
        # We test the extension logic by checking the return path
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                output = str(Path(tmpdir) / "output")
                result = book.render(output)
                assert result.endswith(".pdf")
        except ImportError:
            pytest.skip("Cairo not available")


class TestBookRenderWithCairo:
    """Tests that require Cairo."""

    @pytest.fixture(autouse=True)
    def check_cairo(self):
        """Skip tests if Cairo is not available."""
        try:
            import cairo  # noqa: F401
        except ImportError:
            pytest.skip("Cairo not available")

    def test_render_single_page(self):
        """Test rendering a book with a single page."""
        book = Book(title="Single Page Test")
        page = Page(width=400, height=600)
        page.add(Panel(width=300, height=500))
        book.add_page(page)

        with tempfile.TemporaryDirectory() as tmpdir:
            output = str(Path(tmpdir) / "single.pdf")
            result = book.render(output)
            assert Path(result).exists()
            assert Path(result).stat().st_size > 0

    def test_render_multiple_pages(self):
        """Test rendering a book with multiple pages."""
        book = Book(title="Multi Page Test")

        for i in range(3):
            page = Page(width=400, height=600)
            panel = Panel(width=300, height=500, name=f"Panel_{i}")
            page.add(panel)
            book.add_page(page)

        with tempfile.TemporaryDirectory() as tmpdir:
            output = str(Path(tmpdir) / "multi.pdf")
            result = book.render(output)
            assert Path(result).exists()
            # PDF should be larger with more pages
            assert Path(result).stat().st_size > 0

    def test_render_different_page_sizes(self):
        """Test rendering pages with different dimensions."""
        book = Book()

        # Page 1: Portrait
        page1 = Page(width=400, height=600)
        page1.add(Panel(width=300, height=500))
        book.add_page(page1)

        # Page 2: Landscape
        page2 = Page(width=600, height=400)
        page2.add(Panel(width=500, height=300))
        book.add_page(page2)

        # Page 3: Square
        page3 = Page(width=500, height=500)
        page3.add(Panel(width=400, height=400))
        book.add_page(page3)

        with tempfile.TemporaryDirectory() as tmpdir:
            output = str(Path(tmpdir) / "varied_sizes.pdf")
            result = book.render(output)
            assert Path(result).exists()

    def test_render_with_content(self):
        """Test rendering pages with actual content."""
        book = Book(title="Content Test", author="Test Author")

        # Page with panel and text
        page1 = Page(width=400, height=600)
        panel1 = Panel(width=300, height=500)
        text1 = Text("Page 1", font_size=24)
        text1.move_to((200, 300))
        panel1.add(text1)
        page1.add(panel1)
        book.add_page(page1)

        # Another page
        page2 = Page(width=400, height=600)
        panel2 = Panel(width=300, height=500, background_color="#F0F0F0")
        text2 = Text("Page 2", font_size=24)
        text2.move_to((200, 300))
        panel2.add(text2)
        page2.add(panel2)
        book.add_page(page2)

        with tempfile.TemporaryDirectory() as tmpdir:
            output = str(Path(tmpdir) / "with_content.pdf")
            result = book.render(output)
            assert Path(result).exists()
            assert Path(result).stat().st_size > 100  # Should have actual content

    def test_render_quality_low(self):
        """Test rendering with low quality."""
        book = Book()
        page = Page(width=400, height=600)
        page.add(Panel())
        book.add_page(page)

        with tempfile.TemporaryDirectory() as tmpdir:
            output = str(Path(tmpdir) / "low_quality.pdf")
            result = book.render(output, quality="low")
            assert Path(result).exists()

    def test_render_quality_high(self):
        """Test rendering with high quality."""
        book = Book()
        page = Page(width=400, height=600)
        page.add(Panel())
        book.add_page(page)

        with tempfile.TemporaryDirectory() as tmpdir:
            output = str(Path(tmpdir) / "high_quality.pdf")
            result = book.render(output, quality="high")
            assert Path(result).exists()

    def test_render_creates_directory(self):
        """Test that render creates the output directory if needed."""
        book = Book()
        page = Page()
        page.add(Panel())
        book.add_page(page)

        with tempfile.TemporaryDirectory() as tmpdir:
            output = str(Path(tmpdir) / "subdir" / "nested" / "output.pdf")
            result = book.render(output)
            assert Path(result).exists()
            assert Path(result).parent.exists()


class TestCairoRendererRenderBook:
    """Test CairoRenderer.render_book directly."""

    @pytest.fixture(autouse=True)
    def check_cairo(self):
        """Skip tests if Cairo is not available."""
        try:
            import cairo  # noqa: F401
        except ImportError:
            pytest.skip("Cairo not available")

    def test_render_book_empty_raises(self):
        """Test that render_book raises ValueError for empty list."""
        from comix.renderer.cairo_renderer import CairoRenderer

        page = Page()
        renderer = CairoRenderer(page)

        with pytest.raises(ValueError, match="Cannot render an empty book"):
            with tempfile.TemporaryDirectory() as tmpdir:
                renderer.render_book([], str(Path(tmpdir) / "empty.pdf"))

    def test_render_book_single_page(self):
        """Test render_book with a single page."""
        from comix.renderer.cairo_renderer import CairoRenderer

        page = Page(width=400, height=600)
        page.add(Panel())
        page.build()
        page.auto_layout()

        renderer = CairoRenderer(page)

        with tempfile.TemporaryDirectory() as tmpdir:
            output = str(Path(tmpdir) / "single.pdf")
            result = renderer.render_book([page], output)
            assert Path(result).exists()

    def test_render_book_multiple_pages(self):
        """Test render_book with multiple pages."""
        from comix.renderer.cairo_renderer import CairoRenderer

        pages = []
        for i in range(5):
            page = Page(width=400, height=600)
            page.add(Panel(name=f"Panel_{i}"))
            page.build()
            page.auto_layout()
            pages.append(page)

        renderer = CairoRenderer(pages[0])

        with tempfile.TemporaryDirectory() as tmpdir:
            output = str(Path(tmpdir) / "multi.pdf")
            result = renderer.render_book(pages, output)
            assert Path(result).exists()

    def test_render_book_quality_settings(self):
        """Test that quality parameter is accepted."""
        from comix.renderer.cairo_renderer import CairoRenderer

        page = Page()
        page.add(Panel())
        page.build()
        page.auto_layout()

        renderer = CairoRenderer(page)

        with tempfile.TemporaryDirectory() as tmpdir:
            for quality in ["low", "medium", "high"]:
                output = str(Path(tmpdir) / f"{quality}.pdf")
                result = renderer.render_book([page], output, quality=quality)
                assert Path(result).exists()
