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
        posts = [self._read_post_meta(path) for path in self.posts_dir.glob("*.md")]
        # glob 返回顺序不确定，需自行排序：
        # 1) 先按 slug 升序，作为同日期的稳定 tie-break；
        # 2) 再按日期降序（无日期排末尾），利用 Python 稳定排序保留 1) 的顺序。
        posts.sort(key=lambda p: p.slug)
        posts.sort(key=lambda p: (p.date is not None, p.date or date.min), reverse=True)
        return posts

    def get_post_raw(self, slug: str) -> str | None:
        """返回文章原始 Markdown 文本（含 front matter），用于编辑场景。"""
        path = self.posts_dir / f"{slug}.md"
        if not path.is_file():
            return None
        return path.read_text(encoding="utf-8")

    def delete_post(self, slug: str) -> bool:
        """删除文章文件，返回是否成功。"""
        path = self.posts_dir / f"{slug}.md"
        if not path.is_file():
            return False
        try:
            path.unlink()
            return True
        except OSError:
            return False

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
