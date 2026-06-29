from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Post:
    slug: str
    title: str
    summary: str
    authors: tuple[str, ...]
    date: date | None
    html: str


@dataclass(frozen=True)
class Topic:
    slug: str
    title: str
    summary: str
    authors: tuple[str, ...]
    date: date | None
    html: str


@dataclass(frozen=True)
class Page:
    items: list[Post]
    current_page: int
    total_pages: int
    has_previous: bool
    has_next: bool
    previous_page: int | None
    next_page: int | None
