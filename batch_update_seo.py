"""批量更新已有文章的 SEO 元数据（seo_description / seo_keywords）。

从 .env 读取 LLM 配置，遍历 content/posts/*.md，跳过已有 seo_description
的文章，调用 LLM 生成 SEO 描述与关键词并写入 frontmatter。
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import frontmatter
from dotenv import load_dotenv

from blog.config import Settings
from blog.services.llm import LLMError, extract_seo_metadata

# 每篇文章之间延迟秒数，避免触发 API 限流
_DELAY_SECONDS = 3


def _load_settings() -> Settings:
    """从项目根目录 .env 加载 LLM 配置。"""
    base = Path(__file__).resolve().parent
    load_dotenv(base / ".env")
    return Settings.from_env()


def _needs_update(path: Path) -> bool:
    """判断文章是否需要 SEO 更新（检查 frontmatter 中是否已有 seo_description）。"""
    raw = path.read_text(encoding="utf-8")
    post = frontmatter.loads(raw)
    desc = post.metadata.get("seo_description") or post.metadata.get("Seo_Description") or ""
    return not desc.strip()


def _update_post(path: Path, settings: Settings) -> bool:
    """对单篇文章调用 LLM 生成 SEO 元数据并写回 frontmatter。返回是否成功。"""
    raw = path.read_text(encoding="utf-8")
    post = frontmatter.loads(raw)

    title = (post.metadata.get("title") or post.metadata.get("Title") or path.stem)
    summary = (post.metadata.get("summary") or post.metadata.get("Summary") or "")
    body = post.content or ""

    print(f"  [{path.name}] 标题: {title}")
    print(f"  [{path.name}] 正文 {len(body)} 字符, 调用 LLM…", end=" ", flush=True)

    try:
        seo_desc, seo_kw = extract_seo_metadata(
            str(title),
            str(summary),
            body,
            base_url=settings.llm_base_url,
            api_key=settings.llm_api_key,
            model=settings.llm_model,
        )
    except LLMError as exc:
        print(f"失败: {exc}")
        return False

    post["seo_description"] = seo_desc
    post["seo_keywords"] = seo_kw
    path.write_text(frontmatter.dumps(post), encoding="utf-8")
    print(f"OK (desc={len(seo_desc)}字, kw={seo_kw})")
    return True


def main() -> None:
    settings = _load_settings()
    if not settings.llm_base_url or not settings.llm_api_key or not settings.llm_model:
        print("错误: .env 中未配置 BLOG_LLM_*，请先设置 LLM 接口信息。")
        sys.exit(1)

    posts_dir = settings.content_dir / "posts"
    if not posts_dir.is_dir():
        print(f"错误: 文章目录不存在: {posts_dir}")
        sys.exit(1)

    md_files = sorted(posts_dir.glob("*.md"))
    total = len(md_files)
    print(f"文章目录: {posts_dir}")
    print(f"共发现 {total} 个 .md 文件\n")

    # 统计需要更新的文件
    pending = [f for f in md_files if _needs_update(f)]
    skip = total - len(pending)
    print(f"已有 SEO 数据: {skip} 篇 | 需要更新: {len(pending)} 篇\n")

    if not pending:
        print("所有文章已有 SEO 数据，无需更新。")
        return

    ok = 0
    fail = 0
    for i, path in enumerate(pending, 1):
        print(f"[{i}/{len(pending)}]", end=" ")
        if _update_post(path, settings):
            ok += 1
        else:
            fail += 1
        if i < len(pending):
            time.sleep(_DELAY_SECONDS)

    print(f"\n完成: 成功 {ok} 篇, 失败 {fail} 篇")


if __name__ == "__main__":
    main()
