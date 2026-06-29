from datetime import date

from blog.content.markdown import extract_headings, render_markdown
from blog.content.types import Heading, Post, Topic


def test_render_post_supports_legacy_metadata_keys():
    raw = """---
Title: Legacy Title
Summary: Legacy summary
Authors: Alice
Date: 2020-01-02
---

## Heading

Body text.
"""

    post = render_markdown(slug="legacy-post", raw=raw, kind="post")

    assert isinstance(post, Post)
    assert post.slug == "legacy-post"
    assert post.title == "Legacy Title"
    assert post.summary == "Legacy summary"
    assert post.authors == ("Alice",)
    assert post.date == date(2020, 1, 2)
    assert "<h2" in post.html
    assert "Heading" in post.html


def test_render_post_prefers_lowercase_metadata_keys():
    raw = """---
Title: Legacy Title
title: Modern Title
Summary: Legacy summary
summary: Modern summary
Authors: Alice
authors:
  - Bob
  - Carol
Date: 2020-01-02
date: 2021-03-04
---

Content.
"""

    post = render_markdown(slug="modern-post", raw=raw, kind="post")

    assert post.title == "Modern Title"
    assert post.summary == "Modern summary"
    assert post.authors == ("Bob", "Carol")
    assert post.date == date(2021, 3, 4)


def test_render_post_falls_back_to_slug_when_title_missing():
    post = render_markdown(slug="missing-title", raw="Plain **content**.", kind="post")

    assert post.title == "missing-title"
    assert "<strong>content</strong>" in post.html


def test_render_topic_returns_topic_object():
    raw = """---
title: About
summary: About this site
date: 2022-05-06
---

Welcome.
"""

    topic = render_markdown(slug="about", raw=raw, kind="topic")

    assert isinstance(topic, Topic)
    assert topic.title == "About"
    assert topic.summary == "About this site"
    assert topic.date == date(2022, 5, 6)
    assert "Welcome" in topic.html


def test_extract_headings_filters_and_slugifies():
    raw = """---
title: Test
---

# H1 ignored

## Section A

Some text.

### Sub A1

More text.

#### Sub A1a

Even more.

##### H5

###### H6

# Another H1 ignored

## Section--B

Text."""

    headings = extract_headings(raw)

    assert len(headings) == 6
    assert headings[0] == Heading(level=2, text="Section A", slug="section-a")
    assert headings[1] == Heading(level=3, text="Sub A1", slug="sub-a1")
    assert headings[2] == Heading(level=4, text="Sub A1a", slug="sub-a1a")
    assert headings[3] == Heading(level=5, text="H5", slug="h5")
    assert headings[4] == Heading(level=6, text="H6", slug="h6")
    assert headings[5] == Heading(level=2, text="Section--B", slug="section--b")


def test_render_post_includes_headings():
    raw = """---
title: Test
summary: Test
date: 2024-01-01
---

## First

Body.

## Second

More body.
"""

    post = render_markdown("test", raw, "post")

    assert isinstance(post, Post)
    assert len(post.headings) == 2
    assert post.headings[0] == Heading(level=2, text="First", slug="first")
    assert post.headings[0].level == 2
    assert post.headings[1] == Heading(level=2, text="Second", slug="second")
