"""Book - Multi-page comic compilation for PDF export."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, Iterator, Literal, Self

if TYPE_CHECKING:
    from comix.page.page import Page


class Book:
    """A collection of comic pages for multi-page PDF export.

    The Book class manages multiple Page objects and provides functionality
    to render them into a single multi-page PDF document.

    Example:
        >>> from comix import Book, Page, Panel
        >>>
        >>> # Create pages
        >>> page1 = Page()
        >>> page1.add(Panel(name="Cover"))
        >>>
        >>> page2 = Page()
        >>> page2.add(Panel(name="Chapter 1"))
        >>>
        >>> # Create book and add pages
        >>> book = Book(title="My Comic")
        >>> book.add_page(page1, page2)
        >>> book.render("my_comic.pdf")
    """

    def __init__(
        self,
        title: str = "Untitled Book",
        author: str = "",
        description: str = "",
    ) -> None:
        """Initialize a Book.

        Args:
            title: Title of the book (used in PDF metadata).
            author: Author name (used in PDF metadata).
            description: Description of the book.
        """
        self.title = title
        self.author = author
        self.description = description
        self._pages: list[Page] = []

    def add_page(self, *pages: Page) -> Self:
        """Add one or more pages to the book.

        Args:
            *pages: Page objects to add.

        Returns:
            Self for method chaining.
        """
        for page in pages:
            if page not in self._pages:
                self._pages.append(page)
        return self

    def insert_page(self, index: int, page: Page) -> Self:
        """Insert a page at a specific index.

        Args:
            index: Position to insert the page.
            page: Page to insert.

        Returns:
            Self for method chaining.
        """
        if page not in self._pages:
            self._pages.insert(index, page)
        return self

    def remove_page(self, page: Page) -> Self:
        """Remove a page from the book.

        Args:
            page: Page to remove.

        Returns:
            Self for method chaining.
        """
        if page in self._pages:
            self._pages.remove(page)
        return self

    def get_page(self, index: int) -> Page:
        """Get a page by index.

        Args:
            index: Index of the page (0-based).

        Returns:
            The Page at the specified index.

        Raises:
            IndexError: If index is out of range.
        """
        return self._pages[index]

    @property
    def pages(self) -> list[Page]:
        """Get all pages in the book."""
        return list(self._pages)

    @property
    def page_count(self) -> int:
        """Get the number of pages in the book."""
        return len(self._pages)

    def clear(self) -> Self:
        """Remove all pages from the book.

        Returns:
            Self for method chaining.
        """
        self._pages.clear()
        return self

    def render(
        self,
        output_path: str = "book.pdf",
        quality: Literal["low", "medium", "high"] = "medium",
    ) -> str:
        """Render the book to a multi-page PDF.

        Args:
            output_path: Path to save the PDF file.
            quality: Rendering quality ("low", "medium", "high").
                    Affects DPI for any rasterized content.

        Returns:
            Path to the rendered PDF file.

        Raises:
            ValueError: If the book has no pages.
            ImportError: If Cairo is not installed.
        """
        if not self._pages:
            raise ValueError("Cannot render an empty book. Add pages first.")

        # Ensure output path has .pdf extension
        output_path_obj = Path(output_path)
        if output_path_obj.suffix.lower() != ".pdf":
            output_path = str(output_path_obj.with_suffix(".pdf"))

        # Build all pages first
        for page in self._pages:
            page.build()
            page.auto_layout()

        # Use Cairo renderer for multi-page PDF
        from comix.renderer.cairo_renderer import CairoRenderer

        # Create a renderer with the first page to initialize
        renderer = CairoRenderer(self._pages[0])
        return renderer.render_book(self._pages, output_path, quality=quality)

    def get_metadata(self) -> dict[str, Any]:
        """Get book metadata.

        Returns:
            Dictionary with book metadata.
        """
        return {
            "title": self.title,
            "author": self.author,
            "description": self.description,
            "page_count": self.page_count,
        }

    def __len__(self) -> int:
        """Return the number of pages in the book."""
        return len(self._pages)

    def __iter__(self) -> Iterator[Page]:
        """Iterate over pages in the book."""
        return iter(self._pages)

    def __getitem__(self, index: int) -> Page:
        """Get a page by index."""
        return self._pages[index]
