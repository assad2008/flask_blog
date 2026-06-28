# Flask Blog Modernization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Modernize the legacy Flask blog into a Python 3.12+ / Flask 3.x application that serves local Git-managed Markdown content without Tornado, OSS, Redis, or other legacy runtime dependencies.

**Architecture:** Keep Flask and server-side rendering, but split responsibilities into focused modules: app factory/config, routes, content repository, Markdown rendering, and pagination. Content lives in `content/posts/` and `content/topics/`; routes call repository functions and render Jinja templates with normalized `Post` / `Topic` objects.

**Tech Stack:** Python 3.12+, Flask 3.x, Jinja2, local Markdown files, `python-frontmatter`, `markdown-it-py`, `mdit-py-plugins`, `pygments`, `python-dotenv`, `pytest`, `ruff`, Gunicorn, Waitress.

## Global Constraints

- Do not execute or require any `git` commands; the user explicitly requested no git commands.
- Preserve existing public URL structure: `/`, `/page/<int:page>.html`, `/archives.html`, `/posts/<slug>.html`, `/topic/<slug>.html`.
- Remove Tornado from the runtime path.
- Remove Alibaba Cloud OSS from the content path.
- Remove Redis as a required runtime dependency.
- Use local Markdown files under `content/posts/` and `content/topics/`.
- Support legacy metadata keys `Title`, `Summary`, `Authors`, `Date`.
- Support new metadata keys `title`, `summary`, `authors`, `date`, with lowercase keys taking precedence when both forms exist.
- First-stage implementation must not introduce a database, admin system, full frontend framework, Docker requirement, RSS, sitemap, search, tags, or categories.
- Use `pytest` for tests and `ruff` for lint/format.

---

## File Structure Map

### Create

- `pyproject.toml` — package metadata, dependencies, optional dependency groups, pytest config, ruff config.
- `blog/config.py` — configuration object loaded from environment variables with safe defaults.
- `blog/routes/__init__.py` — route package marker.
- `blog/routes/index.py` — homepage, pagination, archives routes.
- `blog/routes/posts.py` — post detail route.
- `blog/routes/topics.py` — topic detail route.
- `blog/content/__init__.py` — public exports for content layer.
- `blog/content/types.py` — `Post`, `Topic`, and `Page` dataclasses.
- `blog/content/markdown.py` — front matter parsing and Markdown-to-HTML rendering.
- `blog/content/pagination.py` — pure pagination function.
- `blog/content/repository.py` — local filesystem repository for posts and topics.
- `blog/templates/light/base.html` — shared HTML shell.
- `blog/templates/light/index.html` — homepage post list.
- `blog/templates/light/archives.html` — archives page.
- `blog/templates/light/post.html` — post detail page.
- `blog/templates/light/topic.html` — topic detail page.
- `blog/templates/light/page.html` — pagination component.
- `blog/templates/light/404.html` — 404 page.
- `content/posts/awesome-php.md` — migrated sample post from root `awesome-php.md`.
- `content/topics/about.md` — small example topic page.
- `tests/conftest.py` — shared pytest fixtures.
- `tests/test_markdown.py` — Markdown parsing tests.
- `tests/test_pagination.py` — pagination tests.
- `tests/test_repository.py` — local content repository tests.
- `tests/test_routes.py` — Flask route tests.

### Modify

- `blog/__init__.py` — replace legacy factory with modern app factory and blueprint registration.
- `app.py` — replace legacy Flask-Script import path with lightweight development entry point.
- `README.md` — update installation, content editing, run, test, and deployment instructions.
- `CLAUDE.md` — update commands and architecture guidance after implementation.

### Delete or stop using

- `server.py` — no longer used after Tornado removal. Delete once replacement run commands pass.
- `blog/models/post.py` — replaced by `blog/content/repository.py` and `blog/content/markdown.py`.
- `blog/models/topic.py` — replaced by `blog/content/repository.py`.
- `blog/utils/rediscache.py` — Redis no longer required.
- `requirements.txt` — replaced by `pyproject.toml` after all commands use editable install.

---

## Task 1: Packaging and Configuration Baseline

**Files:**
- Create: `pyproject.toml`
- Create: `blog/config.py`
- Test: no test file in this task; verification is package metadata validation and import check.

**Interfaces:**
- Consumes: existing repository root and `blog/` package.
- Produces: `Settings.from_env() -> Settings`, with fields `content_dir: Path`, `posts_per_page: int`, `theme: str`, `secret_key: str`.

- [ ] **Step 1: Create `pyproject.toml`**

Write this complete file:

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "flask-blog"
version = "0.1.0"
description = "A modern Flask blog backed by local Markdown files"
requires-python = ">=3.12"
dependencies = [
  "Flask>=3.0",
  "python-frontmatter>=1.0",
  "markdown-it-py>=3.0",
  "mdit-py-plugins>=0.4",
  "pygments>=2.17",
  "python-dotenv>=1.0",
]

[project.optional-dependencies]
server = [
  "gunicorn>=22; platform_system != 'Windows'",
  "waitress>=3.0",
]
dev = [
  "pytest>=8.0",
  "ruff>=0.5",
]

[tool.setuptools.packages.find]
include = ["blog*"]

[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
line-ending = "auto"
```

- [ ] **Step 2: Create `blog/config.py`**

```python
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class Settings:
    content_dir: Path
    posts_per_page: int
    theme: str
    secret_key: str

    @classmethod
    def from_env(cls) -> "Settings":
        content_dir = Path(os.environ.get("BLOG_CONTENT_DIR", BASE_DIR / "content"))
        posts_per_page = int(os.environ.get("BLOG_POSTS_PER_PAGE", "20"))
        theme = os.environ.get("BLOG_THEME", "light")
        secret_key = os.environ.get("BLOG_SECRET_KEY", "dev-secret-key")
        return cls(
            content_dir=content_dir,
            posts_per_page=posts_per_page,
            theme=theme,
            secret_key=secret_key,
        )
```

- [ ] **Step 3: Install editable development dependencies**

Run:

```bash
pip install -e ".[dev,server]"
```

Expected: command exits 0 and installs Flask, pytest, ruff, Markdown dependencies, and WSGI server dependencies.

- [ ] **Step 4: Verify configuration imports**

Run:

```bash
python -c "from blog.config import Settings; s = Settings.from_env(); print(s.theme, s.posts_per_page, s.content_dir.name)"
```

Expected output contains:

```text
light 20 content
```

- [ ] **Step 5: Manual review checkpoint**

Review changed files manually. Do not run git commands.

---

## Task 2: Content Types and Markdown Renderer

**Files:**
- Create: `blog/content/__init__.py`
- Create: `blog/content/types.py`
- Create: `blog/content/markdown.py`
- Create: `tests/test_markdown.py`

**Interfaces:**
- Consumes: `python-frontmatter`, `markdown-it-py`.
- Produces: `render_markdown(slug: str, raw: str, kind: Literal["post", "topic"]) -> Post | Topic`.
- Produces: `Post` dataclass with `slug: str`, `title: str`, `summary: str`, `authors: tuple[str, ...]`, `date: date | None`, `html: str`.
- Produces: `Topic` dataclass with `slug: str`, `title: str`, `summary: str`, `authors: tuple[str, ...]`, `date: date | None`, `html: str`.

- [ ] **Step 1: Write failing Markdown tests**

Create `tests/test_markdown.py`:

```python
from datetime import date

from blog.content.markdown import render_markdown
from blog.content.types import Post, Topic


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
```

- [ ] **Step 2: Run tests and verify failure**

Run:

```bash
pytest tests/test_markdown.py -v
```

Expected: FAIL because `blog.content.markdown` and related types do not exist yet.

- [ ] **Step 3: Create `blog/content/types.py`**

```python
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
```

- [ ] **Step 4: Create `blog/content/markdown.py`**

```python
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


def _metadata_value(metadata: dict[str, object], lowercase_key: str, legacy_key: str) -> object | None:
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
```

- [ ] **Step 5: Create `blog/content/__init__.py`**

```python
from blog.content.markdown import render_markdown
from blog.content.types import Page, Post, Topic

__all__ = ["Page", "Post", "Topic", "render_markdown"]
```

- [ ] **Step 6: Run Markdown tests and verify pass**

Run:

```bash
pytest tests/test_markdown.py -v
```

Expected: 4 passed.

- [ ] **Step 7: Manual review checkpoint**

Review changed files manually. Do not run git commands.

---

## Task 3: Pagination

**Files:**
- Create: `blog/content/pagination.py`
- Create: `tests/test_pagination.py`

**Interfaces:**
- Consumes: `Post` from `blog.content.types`.
- Produces: `paginate_posts(posts: list[Post], current_page: int, per_page: int) -> Page`.

- [ ] **Step 1: Write failing pagination tests**

Create `tests/test_pagination.py`:

```python
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
```

- [ ] **Step 2: Run tests and verify failure**

Run:

```bash
pytest tests/test_pagination.py -v
```

Expected: FAIL because `blog.content.pagination` does not exist yet.

- [ ] **Step 3: Create `blog/content/pagination.py`**

```python
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
```

- [ ] **Step 4: Export pagination function**

Modify `blog/content/__init__.py` to this complete content:

```python
from blog.content.markdown import render_markdown
from blog.content.pagination import paginate_posts
from blog.content.types import Page, Post, Topic

__all__ = ["Page", "Post", "Topic", "paginate_posts", "render_markdown"]
```

- [ ] **Step 5: Run pagination tests and verify pass**

Run:

```bash
pytest tests/test_pagination.py -v
```

Expected: 4 passed.

- [ ] **Step 6: Manual review checkpoint**

Review changed files manually. Do not run git commands.

---

## Task 4: Local Content Repository

**Files:**
- Create: `blog/content/repository.py`
- Create: `tests/test_repository.py`

**Interfaces:**
- Consumes: `render_markdown(slug, raw, kind)` from Task 2.
- Produces: `ContentRepository(content_dir: Path)`.
- Produces: `ContentRepository.list_posts() -> list[Post]` sorted by date descending, with undated posts last.
- Produces: `ContentRepository.get_post(slug: str) -> Post | None`.
- Produces: `ContentRepository.get_topic(slug: str) -> Topic | None`.

- [ ] **Step 1: Write failing repository tests**

Create `tests/test_repository.py`:

```python
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
```

- [ ] **Step 2: Run tests and verify failure**

Run:

```bash
pytest tests/test_repository.py -v
```

Expected: FAIL because `blog.content.repository` does not exist yet.

- [ ] **Step 3: Create `blog/content/repository.py`**

```python
from __future__ import annotations

from pathlib import Path

from blog.content.markdown import render_markdown
from blog.content.types import Post, Topic


class ContentRepository:
    def __init__(self, content_dir: Path) -> None:
        self.content_dir = Path(content_dir)
        self.posts_dir = self.content_dir / "posts"
        self.topics_dir = self.content_dir / "topics"

    def list_posts(self) -> list[Post]:
        posts = [self._read_post(path) for path in sorted(self.posts_dir.glob("*.md"))]
        return sorted(posts, key=lambda post: post.date is not None and post.date, reverse=True)

    def get_post(self, slug: str) -> Post | None:
        path = self.posts_dir / f"{slug}.md"
        if not path.is_file():
            return None
        return self._read_post(path)

    def get_topic(self, slug: str) -> Topic | None:
        path = self.topics_dir / f"{slug}.md"
        if not path.is_file():
            return None
        raw = path.read_text(encoding="utf-8")
        return render_markdown(slug=slug, raw=raw, kind="topic")

    def _read_post(self, path: Path) -> Post:
        raw = path.read_text(encoding="utf-8")
        rendered = render_markdown(slug=path.stem, raw=raw, kind="post")
        if not isinstance(rendered, Post):
            raise TypeError(f"Expected Post for {path}")
        return rendered
```

- [ ] **Step 4: Export repository**

Modify `blog/content/__init__.py` to this complete content:

```python
from blog.content.markdown import render_markdown
from blog.content.pagination import paginate_posts
from blog.content.repository import ContentRepository
from blog.content.types import Page, Post, Topic

__all__ = ["ContentRepository", "Page", "Post", "Topic", "paginate_posts", "render_markdown"]
```

- [ ] **Step 5: Run repository tests and verify pass**

Run:

```bash
pytest tests/test_repository.py -v
```

Expected: 5 passed.

- [ ] **Step 6: Run content-layer tests together**

Run:

```bash
pytest tests/test_markdown.py tests/test_pagination.py tests/test_repository.py -v
```

Expected: 13 passed.

- [ ] **Step 7: Manual review checkpoint**

Review changed files manually. Do not run git commands.

---

## Task 5: Modern Flask App Factory and Routes

**Files:**
- Modify: `blog/__init__.py`
- Modify: `app.py`
- Create: `blog/routes/__init__.py`
- Create: `blog/routes/index.py`
- Create: `blog/routes/posts.py`
- Create: `blog/routes/topics.py`
- Create: `tests/conftest.py`
- Create: `tests/test_routes.py`

**Interfaces:**
- Consumes: `Settings.from_env()`, `ContentRepository`, `paginate_posts`.
- Produces: `create_app(settings: Settings | None = None) -> Flask`.
- Produces: Flask config keys `SETTINGS`, `CONTENT_REPOSITORY`, `POSTS_PER_PAGE`, `THEME`.

- [ ] **Step 1: Write failing route tests**

Create `tests/conftest.py`:

```python
import pytest

from blog import create_app
from blog.config import Settings


@pytest.fixture
def app(tmp_path):
    posts_dir = tmp_path / "posts"
    topics_dir = tmp_path / "topics"
    posts_dir.mkdir()
    topics_dir.mkdir()

    (posts_dir / "hello.md").write_text(
        """---
title: Hello
date: 2024-01-02
summary: Hello summary
---

Hello **world**.
""",
        encoding="utf-8",
    )
    (topics_dir / "about.md").write_text(
        """---
title: About
summary: About summary
---

About page.
""",
        encoding="utf-8",
    )

    settings = Settings(
        content_dir=tmp_path,
        posts_per_page=1,
        theme="light",
        secret_key="test-secret",
    )
    flask_app = create_app(settings=settings)
    flask_app.config.update(TESTING=True)
    return flask_app


@pytest.fixture
def client(app):
    return app.test_client()
```

Create `tests/test_routes.py`:

```python
def test_homepage_returns_post_list(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Hello" in response.data
    assert b"Hello summary" in response.data


def test_archives_returns_post_list(client):
    response = client.get("/archives.html")

    assert response.status_code == 200
    assert b"Hello" in response.data


def test_post_detail_returns_existing_post(client):
    response = client.get("/posts/hello.html")

    assert response.status_code == 200
    assert b"Hello" in response.data
    assert b"<strong>world</strong>" in response.data


def test_post_detail_returns_404_for_missing_post(client):
    response = client.get("/posts/missing.html")

    assert response.status_code == 404


def test_topic_detail_returns_existing_topic(client):
    response = client.get("/topic/about.html")

    assert response.status_code == 200
    assert b"About" in response.data
    assert b"About page" in response.data


def test_topic_detail_returns_404_for_missing_topic(client):
    response = client.get("/topic/missing.html")

    assert response.status_code == 404


def test_page_route_returns_200(client):
    response = client.get("/page/1.html")

    assert response.status_code == 200
    assert b"Hello" in response.data
```

- [ ] **Step 2: Run route tests and verify failure**

Run:

```bash
pytest tests/test_routes.py -v
```

Expected: FAIL because routes and templates have not been modernized yet.

- [ ] **Step 3: Replace `blog/__init__.py`**

```python
from __future__ import annotations

from flask import Flask, render_template

from blog.config import Settings
from blog.content import ContentRepository


def create_app(settings: Settings | None = None) -> Flask:
    settings = settings or Settings.from_env()
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=settings.secret_key,
        SETTINGS=settings,
        CONTENT_REPOSITORY=ContentRepository(settings.content_dir),
        POSTS_PER_PAGE=settings.posts_per_page,
        THEME=settings.theme,
    )

    from blog.routes.index import index_bp
    from blog.routes.posts import posts_bp
    from blog.routes.topics import topics_bp

    app.register_blueprint(index_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(topics_bp)
    register_error_handlers(app)
    return app


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("light/404.html"), 404
```

- [ ] **Step 4: Replace `app.py`**

```python
from blog import create_app

app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
```

- [ ] **Step 5: Create `blog/routes/__init__.py`**

```python
"""Route blueprints for the Flask blog."""
```

- [ ] **Step 6: Create `blog/routes/index.py`**

```python
from __future__ import annotations

from flask import Blueprint, current_app, render_template

from blog.content import ContentRepository, paginate_posts

index_bp = Blueprint("index", __name__)


@index_bp.route("/")
@index_bp.route("/page/<int:page>.html")
def index(page: int = 1):
    repository: ContentRepository = current_app.config["CONTENT_REPOSITORY"]
    posts = repository.list_posts()
    paginated = paginate_posts(
        posts,
        current_page=page,
        per_page=current_app.config["POSTS_PER_PAGE"],
    )
    return render_template("light/index.html", page=paginated)


@index_bp.route("/archives.html")
def archives():
    repository: ContentRepository = current_app.config["CONTENT_REPOSITORY"]
    posts = repository.list_posts()
    return render_template("light/archives.html", posts=posts)
```

- [ ] **Step 7: Create `blog/routes/posts.py`**

```python
from __future__ import annotations

from flask import Blueprint, abort, current_app, render_template

from blog.content import ContentRepository

posts_bp = Blueprint("posts", __name__)


@posts_bp.route("/posts/<slug>.html")
def detail(slug: str):
    repository: ContentRepository = current_app.config["CONTENT_REPOSITORY"]
    post = repository.get_post(slug)
    if post is None:
        abort(404)
    return render_template("light/post.html", post=post)
```

- [ ] **Step 8: Create `blog/routes/topics.py`**

```python
from __future__ import annotations

from flask import Blueprint, abort, current_app, render_template

from blog.content import ContentRepository

topics_bp = Blueprint("topics", __name__)


@topics_bp.route("/topic/<slug>.html")
def detail(slug: str):
    repository: ContentRepository = current_app.config["CONTENT_REPOSITORY"]
    topic = repository.get_topic(slug)
    if topic is None:
        abort(404)
    return render_template("light/topic.html", topic=topic)
```

- [ ] **Step 9: Run route tests and verify template failure**

Run:

```bash
pytest tests/test_routes.py -v
```

Expected: FAIL with template-not-found errors for `light/*.html`. Task 6 creates templates.

- [ ] **Step 10: Manual review checkpoint**

Review changed files manually. Do not run git commands.

---

## Task 6: Modern Jinja Templates

**Files:**
- Create: `blog/templates/light/base.html`
- Create: `blog/templates/light/index.html`
- Create: `blog/templates/light/archives.html`
- Create: `blog/templates/light/post.html`
- Create: `blog/templates/light/topic.html`
- Create: `blog/templates/light/page.html`
- Create: `blog/templates/light/404.html`

**Interfaces:**
- Consumes: route context variables `page`, `posts`, `post`, `topic`.
- Produces: rendered HTML for all preserved routes.

- [ ] **Step 1: Create `blog/templates/light/base.html`**

```html
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{% block title %}随笔记录{% endblock %}</title>
    <style>
      body { margin: 0 auto; max-width: 900px; padding: 2rem; font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; line-height: 1.7; color: #222; }
      nav { margin-bottom: 2rem; display: flex; gap: 1rem; }
      a { color: #0b5cad; text-decoration: none; }
      a:hover { text-decoration: underline; }
      article { margin-bottom: 2rem; }
      time { color: #666; font-size: 0.9rem; }
      .summary { color: #444; }
      .pagination { display: flex; gap: 1rem; margin-top: 2rem; }
      pre { overflow-x: auto; padding: 1rem; background: #f6f8fa; }
      code { background: #f6f8fa; padding: 0.1rem 0.25rem; }
    </style>
  </head>
  <body>
    <nav>
      <a href="/">首页</a>
      <a href="/archives.html">归档</a>
      <a href="/topic/about.html">关于</a>
    </nav>
    <main>
      {% block content %}{% endblock %}
    </main>
  </body>
</html>
```

- [ ] **Step 2: Create `blog/templates/light/index.html`**

```html
{% extends "light/base.html" %}

{% block title %}首页 - 随笔记录{% endblock %}

{% block content %}
  <h1>随笔记录</h1>
  {% if page.items %}
    {% for post in page.items %}
      <article>
        {% if post.date %}<time datetime="{{ post.date.isoformat() }}">{{ post.date.isoformat() }}</time>{% endif %}
        <h2><a href="/posts/{{ post.slug }}.html">{{ post.title }}</a></h2>
        {% if post.summary %}<p class="summary">{{ post.summary }}</p>{% endif %}
        <p><a href="/posts/{{ post.slug }}.html">阅读全文</a></p>
      </article>
    {% endfor %}
    {% include "light/page.html" %}
  {% else %}
    <p>暂无文章。</p>
  {% endif %}
{% endblock %}
```

- [ ] **Step 3: Create `blog/templates/light/archives.html`**

```html
{% extends "light/base.html" %}

{% block title %}归档 - 随笔记录{% endblock %}

{% block content %}
  <h1>归档</h1>
  {% if posts %}
    <ul>
      {% for post in posts %}
        <li>
          {% if post.date %}<time datetime="{{ post.date.isoformat() }}">{{ post.date.isoformat() }}</time>{% endif %}
          <a href="/posts/{{ post.slug }}.html">{{ post.title }}</a>
        </li>
      {% endfor %}
    </ul>
  {% else %}
    <p>暂无文章。</p>
  {% endif %}
{% endblock %}
```

- [ ] **Step 4: Create `blog/templates/light/post.html`**

```html
{% extends "light/base.html" %}

{% block title %}{{ post.title }} - 随笔记录{% endblock %}

{% block content %}
  <article>
    <header>
      {% if post.date %}<time datetime="{{ post.date.isoformat() }}">{{ post.date.isoformat() }}</time>{% endif %}
      <h1>{{ post.title }}</h1>
      {% if post.authors %}<p>作者：{{ post.authors | join(", ") }}</p>{% endif %}
    </header>
    <div>
      {{ post.html | safe }}
    </div>
  </article>
{% endblock %}
```

- [ ] **Step 5: Create `blog/templates/light/topic.html`**

```html
{% extends "light/base.html" %}

{% block title %}{{ topic.title }} - 随笔记录{% endblock %}

{% block content %}
  <article>
    <header>
      {% if topic.date %}<time datetime="{{ topic.date.isoformat() }}">{{ topic.date.isoformat() }}</time>{% endif %}
      <h1>{{ topic.title }}</h1>
    </header>
    <div>
      {{ topic.html | safe }}
    </div>
  </article>
{% endblock %}
```

- [ ] **Step 6: Create `blog/templates/light/page.html`**

```html
<nav class="pagination" aria-label="分页">
  {% if page.has_previous %}
    <a href="{% if page.previous_page == 1 %}/{% else %}/page/{{ page.previous_page }}.html{% endif %}">上一页</a>
  {% endif %}
  <span>第 {{ page.current_page }} / {{ page.total_pages }} 页</span>
  {% if page.has_next %}
    <a href="/page/{{ page.next_page }}.html">下一页</a>
  {% endif %}
</nav>
```

- [ ] **Step 7: Create `blog/templates/light/404.html`**

```html
{% extends "light/base.html" %}

{% block title %}页面不存在 - 随笔记录{% endblock %}

{% block content %}
  <h1>页面不存在</h1>
  <p>你访问的内容不存在，或已经移动。</p>
  <p><a href="/">返回首页</a></p>
{% endblock %}
```

- [ ] **Step 8: Run route tests and verify pass**

Run:

```bash
pytest tests/test_routes.py -v
```

Expected: 7 passed.

- [ ] **Step 9: Run all tests added so far**

Run:

```bash
pytest -v
```

Expected: 20 passed.

- [ ] **Step 10: Manual review checkpoint**

Review changed files manually. Do not run git commands.

---

## Task 7: Migrate Local Content

**Files:**
- Create: `content/posts/awesome-php.md`
- Create: `content/topics/about.md`
- Modify: no Python files unless tests expose path issues.

**Interfaces:**
- Consumes: `ContentRepository` reading `content/posts` and `content/topics`.
- Produces: real local content for development runs.

- [ ] **Step 1: Create content directories**

Create directories:

```text
content/posts
content/topics
```

- [ ] **Step 2: Move sample post content into `content/posts/awesome-php.md`**

Copy the full content from root `awesome-php.md` into `content/posts/awesome-php.md` without changing its front matter.

The beginning of `content/posts/awesome-php.md` must remain:

```markdown
---
Title:  Github上的PHP资源汇总大全
Summary: 一个PHP资源列表，内容包括：库、框架、模板、安全、代码分析、日志、第三方库、配置工具、Web 工具、书籍、电子书、经典博文等等
Authors: Django Wong
Date:    2015-01-08
---
```

- [ ] **Step 3: Create `content/topics/about.md`**

```markdown
---
title: 关于
summary: 关于本站
date: 2026-06-28
---

这是一个使用 Flask 和本地 Markdown 文件构建的博客。
```

- [ ] **Step 4: Verify repository can read real content**

Run:

```bash
python -c "from pathlib import Path; from blog.content import ContentRepository; r=ContentRepository(Path('content')); print(r.list_posts()[0].slug); print(r.get_topic('about').title)"
```

Expected output:

```text
awesome-php
关于
```

- [ ] **Step 5: Manual review checkpoint**

Review content files manually. Do not run git commands.

---

## Task 8: Remove Legacy Runtime Paths

**Files:**
- Delete: `server.py`
- Delete: `blog/models/post.py`
- Delete: `blog/models/topic.py`
- Delete: `blog/utils/rediscache.py`
- Modify: `requirements.txt` or remove it after confirming `pyproject.toml` is the installation source.

**Interfaces:**
- Consumes: all modern code from Tasks 1-7.
- Produces: codebase without Tornado, OSS, Redis, Flask-Script runtime imports.

- [ ] **Step 1: Search for legacy imports**

Run:

```bash
python -c "from pathlib import Path; needles=['tornado','oss2','redis','rc','flask.ext','Flask-Script','Flask-Cache']; hits=[]\nfor p in Path('.').rglob('*'):\n    if p.is_file() and p.suffix in {'.py','.txt','.md','.toml'} and '.git' not in p.parts:\n        text=p.read_text(encoding='utf-8', errors='ignore')\n        for n in needles:\n            if n in text:\n                hits.append((str(p), n))\nprint(hits)" 
```

Expected before deletion: hits include legacy files and docs. After this task, hits in runtime Python files must be empty.

- [ ] **Step 2: Delete `server.py`**

Remove `server.py` because Tornado is no longer the entry point.

- [ ] **Step 3: Delete legacy OSS/Redis model files**

Remove:

```text
blog/models/post.py
blog/models/topic.py
blog/utils/rediscache.py
```

- [ ] **Step 4: Remove or replace `requirements.txt`**

Preferred first-stage action: replace `requirements.txt` with a short compatibility note so old install commands do not silently install legacy dependencies:

```text
# This project now uses pyproject.toml.
# Install with:
#   pip install -e ".[dev,server]"
```

- [ ] **Step 5: Verify legacy runtime imports are gone from Python files**

Run:

```bash
python -c "from pathlib import Path; needles=['tornado','oss2','redis','rc','flask.ext']; hits=[]\nfor p in Path('.').rglob('*.py'):\n    if '.git' in p.parts:\n        continue\n    text=p.read_text(encoding='utf-8', errors='ignore')\n    for n in needles:\n        if n in text:\n            hits.append((str(p), n))\nprint(hits); raise SystemExit(1 if hits else 0)"
```

Expected output:

```text
[]
```

- [ ] **Step 6: Run all tests**

Run:

```bash
pytest -v
```

Expected: 20 passed.

- [ ] **Step 7: Manual review checkpoint**

Review deleted/replaced files manually. Do not run git commands.

---

## Task 9: Documentation Updates

**Files:**
- Modify: `README.md`
- Modify: `CLAUDE.md`

**Interfaces:**
- Consumes: final run/test commands and architecture from Tasks 1-8.
- Produces: accurate human and Claude Code documentation.

- [ ] **Step 1: Replace README with modern project documentation**

Use this structure and keep the content specific:

```markdown
# flask_blog

一个使用 Flask 和本地 Markdown 文件构建的博客系统。内容保存在 `content/posts/` 和 `content/topics/` 中，并通过 Git 管理。

## 技术栈

- Python 3.12+
- Flask 3.x
- Jinja2
- 本地 Markdown 文件
- python-frontmatter
- markdown-it-py
- pytest
- ruff

## 安装

```bash
pip install -e ".[dev,server]"
```

## 启动开发服务器

```bash
flask --app blog:create_app --debug run
```

也可以运行：

```bash
python app.py
```

## 生产运行

Linux：

```bash
gunicorn "blog:create_app()" --bind 0.0.0.0:8080
```

Windows 或简单部署：

```bash
waitress-serve --listen=0.0.0.0:8080 --call blog:create_app
```

## 内容目录

```text
content/posts/   文章 Markdown
content/topics/  独立页面 Markdown
```

文章文件示例：

```markdown
---
title: Example title
summary: Example summary
authors:
  - Author name
date: 2026-06-28
---

Markdown content...
```

兼容旧字段：`Title`、`Summary`、`Authors`、`Date`。

## URL

- `/`
- `/page/<page>.html`
- `/archives.html`
- `/posts/<slug>.html`
- `/topic/<slug>.html`

## 测试和格式化

```bash
pytest
ruff check .
ruff format .
```
```

- [ ] **Step 2: Update `CLAUDE.md`**

Replace the old OSS/Tornado/Redis guidance with the current architecture and commands. The top of the file must remain exactly:

```markdown
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.
```

Include these command blocks:

```bash
pip install -e ".[dev,server]"
flask --app blog:create_app --debug run
python app.py
gunicorn "blog:create_app()" --bind 0.0.0.0:8080
waitress-serve --listen=0.0.0.0:8080 --call blog:create_app
pytest
pytest tests/test_repository.py
pytest tests/test_repository.py::test_list_posts_reads_markdown_and_sorts_by_date_desc
ruff check .
ruff format .
```

- [ ] **Step 3: Verify docs no longer describe OSS/Tornado/Redis as required runtime dependencies**

Run:

```bash
python -c "from pathlib import Path; docs=[Path('README.md'), Path('CLAUDE.md')]; bad=[]\nfor p in docs:\n    text=p.read_text(encoding='utf-8')\n    for phrase in ['OSS 作为内容存储', 'Tornado WSGI', 'Redis 做缓存']:\n        if phrase in text:\n            bad.append((str(p), phrase))\nprint(bad); raise SystemExit(1 if bad else 0)"
```

Expected output:

```text
[]
```

- [ ] **Step 4: Manual review checkpoint**

Review README and CLAUDE.md manually. Do not run git commands.

---

## Task 10: Final Verification

**Files:**
- Modify only if verification exposes issues.

**Interfaces:**
- Consumes: complete implementation from Tasks 1-9.
- Produces: verified first-stage modernization deliverable.

- [ ] **Step 1: Run full test suite**

Run:

```bash
pytest -v
```

Expected: all tests pass. Expected count after this plan is 20 tests unless extra tests were added during implementation.

- [ ] **Step 2: Run ruff lint**

Run:

```bash
ruff check .
```

Expected: exits 0 with no lint errors.

- [ ] **Step 3: Run ruff format check**

Run:

```bash
ruff format --check .
```

Expected: exits 0 and reports files are already formatted.

- [ ] **Step 4: Verify Flask app imports**

Run:

```bash
python -c "from blog import create_app; app=create_app(); print(app.name); print(sorted(rule.rule for rule in app.url_map.iter_rules()))"
```

Expected output includes:

```text
blog
/
/archives.html
/page/<int:page>.html
/posts/<slug>.html
/topic/<slug>.html
```

- [ ] **Step 5: Verify local content route through Flask test client**

Run:

```bash
python -c "from blog import create_app; app=create_app(); c=app.test_client(); r=c.get('/posts/awesome-php.html'); print(r.status_code); print('Github' in r.get_data(as_text=True))"
```

Expected output:

```text
200
True
```

- [ ] **Step 6: Verify legacy runtime imports remain absent**

Run:

```bash
python -c "from pathlib import Path; needles=['tornado','oss2','redis','rc','flask.ext']; hits=[]\nfor p in Path('.').rglob('*.py'):\n    if '.git' in p.parts:\n        continue\n    text=p.read_text(encoding='utf-8', errors='ignore')\n    for n in needles:\n        if n in text:\n            hits.append((str(p), n))\nprint(hits); raise SystemExit(1 if hits else 0)"
```

Expected output:

```text
[]
```

- [ ] **Step 7: Final manual review checkpoint**

Review the final changed tree manually through file inspection. Do not run git commands.

---

## Execution Notes

- This plan intentionally replaces commit steps with manual review checkpoints because the user instructed that no git commands be executed.
- If an implementation agent uses subagents, each task should be implemented in order and verified before the next task begins.
- If a task fails because a dependency behaves differently than expected, stop at that task, report the exact command and output, and revise the plan or implementation before continuing.
- Do not skip tests because the project originally had no test suite; this modernization relies on tests to preserve URL and content behavior while removing OSS, Redis, and Tornado.
