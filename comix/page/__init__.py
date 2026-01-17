"""Page module - comic page composition."""

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
