from datetime import date

from blog.content.pagination import paginate_posts
from blog.content.types import Post


def make_post(index: int) -> Post:
    return Post(
        slug=f"post-{index}",
        title=f"Post {index}",
        summary="",
        authors=(),
        date=date(2024, 1, index),
        html="<p>Body</p>",
    )


def test_paginate_posts_returns_first_page():
    posts = [make_post(index) for index in range(1, 6)]

    page = paginate_posts(posts, current_page=1, per_page=2)

    assert [post.slug for post in page.items] == ["post-1", "post-2"]
    assert page.current_page == 1
    assert page.total_pages == 3
    assert page.has_previous is False
    assert page.has_next is True
    assert page.previous_page is None
    assert page.next_page == 2


def test_paginate_posts_returns_middle_page():
    posts = [make_post(index) for index in range(1, 6)]

    page = paginate_posts(posts, current_page=2, per_page=2)

    assert [post.slug for post in page.items] == ["post-3", "post-4"]
    assert page.current_page == 2
    assert page.total_pages == 3
    assert page.has_previous is True
    assert page.has_next is True
    assert page.previous_page == 1
    assert page.next_page == 3


def test_paginate_posts_clamps_page_above_range():
    posts = [make_post(index) for index in range(1, 4)]

    page = paginate_posts(posts, current_page=99, per_page=2)

    assert [post.slug for post in page.items] == ["post-3"]
    assert page.current_page == 2
    assert page.total_pages == 2


def test_paginate_posts_handles_empty_list():
    page = paginate_posts([], current_page=1, per_page=20)

    assert page.items == []
    assert page.current_page == 1
    assert page.total_pages == 1
    assert page.has_previous is False
    assert page.has_next is False
