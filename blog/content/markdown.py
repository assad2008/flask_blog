from __future__ import annotations

import re
import unicodedata
from datetime import date, datetime
from typing import Literal

import frontmatter
from markdown_it import MarkdownIt
from markdown_it.renderer import RendererHTML
from markdown_it.rules_core import StateCore
from markdown_it.token import Token
from mdit_py_plugins import anchors
from mdit_py_plugins.footnote import footnote_plugin
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import TextLexer, get_lexer_by_name, guess_lexer
from pygments.util import ClassNotFound

from blog.content.types import Heading, Post, Topic

MarkdownKind = Literal["post", "topic"]

# Pygments 高亮样式：亮色用 default，暗色用 monokai
_HTML_FORMATTER = HtmlFormatter(linenos=False, cssclass="highlight")


def _slugify(text: str) -> str:
    """将标题文本转为 HTML id，保留中文字符和原有连字符。"""
    # 先把所有空白（含连续空格）统一替换为单个连字符
    text = unicodedata.normalize("NFKD", text).strip().lower()
    text = re.sub(r"\s+", "-", text)
    # 移除 HTML 特殊字符和非法 id 字符，保留字母、数字、连字符、中文
    text = re.sub(r"[^\w\-一-鿿]", "", text)
    return text or "heading"


def extract_headings(markdown_text: str) -> tuple[Heading, ...]:
    """从原始 Markdown 文本中提取标题列表（仅 h2-h6）。"""
    headings: list[Heading] = []
    for line in markdown_text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("#"):
            continue
        # 计算标题级别（连续 # 的数量）
        level = 0
        for ch in stripped:
            if ch == "#":
                level += 1
            else:
                break
        if level < 2 or level > 6:
            continue
        # 去掉 # 前缀和首尾空白，得到标题纯文本
        text = stripped[level:].strip()
        if not text:
            continue
        slug = _slugify(text)
        headings.append(Heading(level=level, text=text, slug=slug))
    return tuple(headings)


def _highlight_code(code: str, lang: str) -> str:
    """使用 Pygments 对代码块进行语法高亮，返回完整 HTML。"""
    try:
        if lang:
            lexer = get_lexer_by_name(lang, stripall=False)
        else:
            lexer = guess_lexer(code)
    except ClassNotFound:
        lexer = TextLexer()

    return highlight(code, lexer, _HTML_FORMATTER)


class HighlightRenderer(RendererHTML):
    """扩展的渲染器，为代码块添加 Pygments 语法高亮。"""

    def fence(
        self,
        tokens: list[Token],
        idx: int,
        options: dict,
        env: dict,
    ) -> str:
        token = tokens[idx]
        info = token.info.strip() if token.info else ""
        lang = info.split(maxsplit=1)[0] if info else ""

        code = token.content
        highlighted = _highlight_code(code, lang)

        # 如果高亮返回以 <pre 开头的内容，直接返回
        if highlighted.startswith("<pre"):
            return highlighted + "\n"

        # 否则将高亮后的 HTML 包裹在 <pre><code> 中
        return "<pre><code>" + highlighted + "</code></pre>\n"


def _unescape_fences(text: str) -> str:
    """将 markdown 中转义的反引号围栏还原为可被解析的代码围栏标记。

    markdown-it 的 escape 规则会消耗 ``\\` `` 中的反斜杠，导致
    `` \\`\\`\\`python `` 无法被识别为代码围栏。
    此函数在渲染前将 `` \\`\\`\\` `` 替换为 `` ``` ``，使围栏规则正常工作。
    """
    import re

    # 匹配行首的 \`\`\` 或 \`\`\`，后面跟语言标识符和换行
    # 替换为普通的 ``` 围栏标记
    text = re.sub(r"^\\`\\`\\`(\w*)\n", r"```\1\n", text, flags=re.MULTILINE)
    # 匹配行首的 \`\`\`\`\`\`（关闭围栏）
    text = re.sub(r"^\\`\\`\\`\s*$", "```", text, flags=re.MULTILINE)
    return text


def render_markdown(slug: str, raw: str, kind: MarkdownKind) -> Post | Topic:
    parsed = frontmatter.loads(raw)
    metadata = parsed.metadata
    # 预处理：将转义的反引号 \`\`\` 还原为代码围栏标记
    content = _unescape_fences(parsed.content)
    html = _markdown().render(content)
    headings = extract_headings(content)

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
            headings=headings,
        )

    return Topic(
        slug=slug,
        title=str(title),
        summary=str(summary),
        authors=authors,
        date=published_date,
        html=html,
        headings=headings,
    )


def _markdown() -> MarkdownIt:
    md = MarkdownIt(
        "commonmark",
        options_update={"html": True, "linkify": True, "typographer": True},
        renderer_cls=HighlightRenderer,
    )
    # 所有链接新窗口打开
    md.core.ruler.push("external_links", _add_blank_target)
    return (
        md.enable("table")
        .use(anchors.anchors_plugin, min_level=1, max_level=6, slug_func=_slugify)
        .use(footnote_plugin)
    )


def _add_blank_target(state: StateCore) -> None:
    """为外部链接添加 target=\"_blank\" 和 rel=\"noopener noreferrer\"，内部锚点链接保持不变。"""
    for token in state.tokens:
        if token.type == "inline" and token.children:
            for child in token.children:
                if child.type == "link_open":
                    href = (child.attrGet("href") or "").strip()
                    # 跳过内部锚点链接（如 #section-name）
                    if href.startswith("#"):
                        continue
                    child.attrSet("target", "_blank")
                    child.attrSet("rel", "noopener noreferrer")


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
