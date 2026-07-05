from __future__ import annotations

from datetime import date
from pathlib import Path

from blog.content.markdown import extract_post_meta, render_markdown
from blog.content.types import Post, Topic


class ContentRepository:
    def __init__(self, content_dir: Path) -> None:
        self.content_dir = Path(content_dir)
        self.posts_dir = self.content_dir / "posts"
        self.topics_dir = self.content_dir / "topics"

    def list_posts(self) -> list[Post]:
        posts = [self._read_post_meta(path) for path in sorted(self.posts_dir.glob("*.md"))]
        return sorted(
            posts,
            key=lambda post: (post.date is not None, post.date or date.min),
            reverse=True,
        )

    def _read_post_meta(self, path: Path) -> Post:
        """仅读取文章元数据，不渲染 Markdown 正文。用于列表页面。"""
        raw = path.read_text(encoding="utf-8")
        return extract_post_meta(slug=path.stem, raw=raw)

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
