from __future__ import annotations

from math import ceil

from blog.content.types import Page, Post


def paginate_posts(posts: list[Post], current_page: int, per_page: int) -> Page:
    if per_page < 1:
        raise ValueError("per_page must be at least 1")

    total_pages = max(1, ceil(len(posts) / per_page))
    normalized_page = min(max(current_page, 1), total_pages)
    start = (normalized_page - 1) * per_page
    end = start + per_page
    items = posts[start:end]

    has_previous = normalized_page > 1
    has_next = normalized_page < total_pages

    return Page(
        items=items,
        current_page=normalized_page,
        total_pages=total_pages,
        has_previous=has_previous,
        has_next=has_next,
        previous_page=normalized_page - 1 if has_previous else None,
        next_page=normalized_page + 1 if has_next else None,
    )
