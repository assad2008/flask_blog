from __future__ import annotations

from datetime import date, datetime
from typing import Literal

import frontmatter
from markdown_it import MarkdownIt
from mdit_py_plugins.footnote import footnote_plugin

from blog.content.types import Post, Topic

MarkdownKind = Literal["post", "topic"]


def render_markdown(slug: str, raw: str, kind: MarkdownKind) -> Post | Topic:
    parsed = frontmatter.loads(raw)
    metadata = parsed.metadata
    html = _markdown().render(parsed.content)

    title = _metadata_value(metadata, "title", "Title") or slug
    summary = _metadata_value(metadata, "summary", "Summary") or ""
    authors = _metadata_authors(_metadata_value(metadata, "authors", "Authors"))
    published_date = _metadata_date(_metadata_value(metadata, "date", "Date"))

    if kind == "post":
        return Post(
            slug=slug,
            title=str(title),
            summary=str(summary),
            authors=authors,
            date=published_date,
            html=html,
        )

    return Topic(
        slug=slug,
        title=str(title),
        summary=str(summary),
        authors=authors,
        date=published_date,
        html=html,
    )


def _markdown() -> MarkdownIt:
    return (
        MarkdownIt("commonmark", {"html": True, "linkify": True, "typographer": True})
        .enable("table")
        .use(footnote_plugin)
    )


def _metadata_value(
    metadata: dict[str, object], lowercase_key: str, legacy_key: str
) -> object | None:
    if lowercase_key in metadata:
        return metadata[lowercase_key]
    return metadata.get(legacy_key)


def _metadata_authors(value: object | None) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,)
    if isinstance(value, list | tuple):
        return tuple(str(author) for author in value)
    return (str(value),)


def _metadata_date(value: object | None) -> date | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        return date.fromisoformat(value.strip())
    raise ValueError(f"Unsupported date metadata value: {value!r}")
