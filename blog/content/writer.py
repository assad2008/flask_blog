"""内容写入层：将发布页提交的文章写成带 front matter 的 Markdown 文件。

与只读的 ``ContentRepository`` 分离，把写入相关副作用集中在此处，便于测试。
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import frontmatter


def resolve_unique_slug(slug: str, posts_dir: Path) -> str:
    """解决 slug 冲突：若 ``<slug>.md`` 已存在，依次追加 ``-2``、``-3`` 后缀。"""
    candidate = slug
    counter = 2
    while (posts_dir / f"{candidate}.md").exists():
        candidate = f"{slug}-{counter}"
        counter += 1
    return candidate


def update_post_title_and_body(
    posts_dir: Path,
    slug: str,
    *,
    title: str,
    body: str,
) -> Path:
    """更新已有文章的标题与正文，保留其他 front matter 字段不变。
    读取原文件，修改 title 和正文后写回。
    """
    path = posts_dir / f"{slug}.md"
    raw = path.read_text(encoding="utf-8")
    parsed = frontmatter.loads(raw)
    parsed["title"] = title
    # 移除旧的 uppercase 兼容字段，避免前端冲突
    if "Title" in parsed.metadata:
        del parsed["Title"]
    parsed.content = body
    path.write_text(frontmatter.dumps(parsed), encoding="utf-8")
    return path


def write_markdown_post(
    posts_dir: Path,
    slug: str,
    *,
    title: str,
    summary: str,
    authors: list[str],
    date_str: str,
    body: str,
    seo_description: str = "",
    seo_keywords: str = "",
) -> Path:
    """将文章写入 ``posts_dir/<slug>.md``，包含 front matter。

    - ``authors`` 为空时不写 authors 字段；
    - ``date_str`` 形如 ``YYYY-MM-DD``；
    - ``seo_description`` / ``seo_keywords`` 为空时不写对应字段。
    """
    post = frontmatter.Post(body)
    post["title"] = title
    post["summary"] = summary
    if authors:
        post["authors"] = authors
    post["date"] = date_str
    if seo_description:
        post["seo_description"] = seo_description
    if seo_keywords:
        post["seo_keywords"] = seo_keywords

    posts_dir.mkdir(parents=True, exist_ok=True)
    path = posts_dir / f"{slug}.md"
    path.write_text(frontmatter.dumps(post), encoding="utf-8")
    return path


def today_iso() -> str:
    """返回当天日期的 ISO 字符串（``YYYY-MM-DD``）。"""
    return date.today().isoformat()
