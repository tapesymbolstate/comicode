"""Page module - comic page composition."""

from comix.page.book import Book
from comix.page.page import Page, SinglePanel, Strip
from comix.page.templates import (
    FourKoma,
    SplashPage,
    TwoByTwo,
    WebComic,
    ThreeRowLayout,
    MangaPage,
    ActionPage,
)

__all__ = [
    "Book",
    "Page",
    "SinglePanel",
    "Strip",
    # Templates
    "FourKoma",
    "SplashPage",
    "TwoByTwo",
    "WebComic",
    "ThreeRowLayout",
    "MangaPage",
    "ActionPage",
]
