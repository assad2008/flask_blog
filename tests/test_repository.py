from pathlib import Path

from blog.content.repository import ContentRepository


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_list_posts_reads_markdown_and_sorts_by_date_desc(tmp_path):
    write_file(
        tmp_path / "posts" / "older.md",
        """---
title: Older
date: 2020-01-01
summary: Old summary
---

Older body.
""",
    )
    write_file(
        tmp_path / "posts" / "newer.md",
        """---
title: Newer
date: 2022-01-01
summary: New summary
---

Newer body.
""",
    )
    write_file(tmp_path / "posts" / "ignored.txt", "not markdown")

    repository = ContentRepository(tmp_path)

    posts = repository.list_posts()

    assert [post.slug for post in posts] == ["newer", "older"]
    assert posts[0].title == "Newer"
    assert posts[1].title == "Older"


def test_get_post_returns_post_for_existing_slug(tmp_path):
    write_file(
        tmp_path / "posts" / "hello.md",
        """---
title: Hello
date: 2021-02-03
---

Hello **world**.
""",
    )

    repository = ContentRepository(tmp_path)

    post = repository.get_post("hello")

    assert post is not None
    assert post.slug == "hello"
    assert post.title == "Hello"
    assert "<strong>world</strong>" in post.html


def test_get_post_returns_none_for_missing_slug(tmp_path):
    repository = ContentRepository(tmp_path)

    assert repository.get_post("missing") is None


def test_get_topic_returns_topic_for_existing_slug(tmp_path):
    write_file(
        tmp_path / "topics" / "about.md",
        """---
title: About
summary: About this site
---

Welcome.
""",
    )

    repository = ContentRepository(tmp_path)

    topic = repository.get_topic("about")

    assert topic is not None
    assert topic.slug == "about"
    assert topic.title == "About"
    assert "Welcome" in topic.html


def test_get_topic_returns_none_for_missing_slug(tmp_path):
    repository = ContentRepository(tmp_path)

    assert repository.get_topic("missing") is None
