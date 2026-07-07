from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Heading:
    """文章目录中的一级标题。"""

    level: int  # 2-6（对应 <h2>~<h6>）
    text: str  # 纯文本标题
    slug: str  # 锚点 id


@dataclass(frozen=True)
class Post:
    slug: str
    title: str
    summary: str
    authors: tuple[str, ...]
    date: date | None
    html: str
    headings: tuple[Heading, ...] = ()
    seo_description: str = ""
    seo_keywords: str = ""


@dataclass(frozen=True)
class Topic:
    slug: str
    title: str
    summary: str
    authors: tuple[str, ...]
    date: date | None
    html: str
    headings: tuple[Heading, ...] = ()
    seo_description: str = ""
    seo_keywords: str = ""


@dataclass(frozen=True)
class Page:
    items: list[Post]
    current_page: int
    total_pages: int
    has_previous: bool
    has_next: bool
    previous_page: int | None
    next_page: int | None
