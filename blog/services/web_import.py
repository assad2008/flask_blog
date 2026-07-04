"""网页导入服务：抓取 URL，清洗 HTML，并交给 LLM 提取未改写的 Markdown 正文。"""

from __future__ import annotations

import re
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable
from html import unescape
from html.parser import HTMLParser
from typing import Any

from blog.services.llm import LLMError, extract_article_markdown

_MAX_HTML_BYTES = 10_000_000
_MAX_CANDIDATE_CHARS = 100000
_TIMEOUT_SECONDS = 20
_ALLOWED_SCHEMES = {"http", "https"}
_BLOCK_TAGS = {"p", "div", "section", "article"}
_HEADING_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6"}
_DROP_TAGS = {
    "script",
    "style",
    "noscript",
    "svg",
    "canvas",
    "nav",
    "footer",
    "header",
    "aside",
    "form",
    "button",
    "iframe",
}


class WebImportError(Exception):
    """网页抓取或正文导入失败。"""


def fetch_article_markdown(
    url: str,
    *,
    base_url: str,
    api_key: str,
    model: str,
    on_progress: Callable[[dict[str, Any]], None] | None = None,
) -> str:
    """抓取网页并返回由 LLM 提取的 Markdown 正文。

    ``on_progress`` 回调用于向前端流式输出进度信息，接收 dict 事件：
    ``{"type": "log", "message": "…"}`` 或 ``{"type": "preview", "text": "…"}``。
    """

    def _log(msg: str, **extra: Any) -> None:
        if on_progress:
            on_progress({"type": "log", "message": msg, **extra})

    _log("正在验证网址…")
    normalized_url = _validate_url(url)

    _log("正在访问网站…")
    html = _fetch_html(normalized_url)

    _log("正在解析信息…")
    candidate_text = _html_to_candidate_markdown(html, source_url=normalized_url)
    if not candidate_text.strip():
        raise WebImportError("未提取到可供分析的网页正文")

    # 把解析后的候选文本发给前端做预览（截断前 5000 字符）
    if on_progress:
        on_progress({"type": "preview", "text": candidate_text[:5000]})

    raw_chars = len(candidate_text)
    input_chars = min(raw_chars, _MAX_CANDIDATE_CHARS)
    if raw_chars > _MAX_CANDIDATE_CHARS:
        _log(
            f"网页内容过长（{raw_chars} > 限制 {_MAX_CANDIDATE_CHARS} 字符），"
            f"已截断前 {_MAX_CANDIDATE_CHARS} 字符提交大模型"
        )
    _log(f"正在使用大模型({model})提取内容，提交 {input_chars} 字符…")

    try:
        article = extract_article_markdown(
            normalized_url,
            candidate_text[:_MAX_CANDIDATE_CHARS],
            base_url=base_url,
            api_key=api_key,
            model=model,
            temperature=0.0,
        )
    except LLMError as exc:
        raise WebImportError(str(exc)) from exc

    # 记录大模型 token 用量
    if article.usage:
        u = article.usage
        _log(
            f"大模型调用完成，tokens：提示 {u.get('prompt_tokens', 0)} "
            f"+ 补全 {u.get('completion_tokens', 0)} "
            f"= 总计 {u.get('total_tokens', 0)}"
        )

    body = article.body.strip()
    if not body:
        raise WebImportError("未提取到正文")

    # 从 HTML 中提取文章标题，附加转载声明
    page_title = _extract_html_title(html)
    source_label = page_title or normalized_url
    body += f"\n\n> 本文转自 [{source_label}]({normalized_url})"

    word_count = _count_words(body)
    _log(f"内容提取成功，字数：{word_count}")
    return body


def _count_words(text: str) -> int:
    """统计文本字数（不含空白字符的字符总数）。"""
    return len(re.sub(r"\s+", "", text))


def _extract_html_title(html: str) -> str:
    """从 HTML 中提取 ``<title>`` 标签内的文本。"""
    match = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
    if not match:
        return ""
    title = re.sub(r"\s+", " ", match.group(1).strip())
    return title


def _validate_url(url: str) -> str:
    """只允许 http/https URL，避免读取本地文件或其它协议。"""
    normalized = (url or "").strip()
    parsed = urllib.parse.urlparse(normalized)
    if not normalized or parsed.scheme not in _ALLOWED_SCHEMES or not parsed.netloc:
        raise WebImportError("请输入有效的 http:// 或 https:// 网页地址")
    return normalized


def _fetch_html(url: str) -> str:
    """抓取网页 HTML，并限制响应大小。"""
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; flask-blog-web-import/1.0)",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=_TIMEOUT_SECONDS) as resp:
            content_type = resp.headers.get("Content-Type", "")
            if "text/html" not in content_type and "application/xhtml+xml" not in content_type:
                raise WebImportError("目标地址返回的不是 HTML 页面")
            data = resp.read(_MAX_HTML_BYTES + 1)
    except urllib.error.HTTPError as exc:
        raise WebImportError(f"网页抓取失败：HTTP {exc.code}") from exc
    except urllib.error.URLError as exc:
        raise WebImportError(f"网页抓取失败：{exc.reason}") from exc

    if len(data) > _MAX_HTML_BYTES:
        raise WebImportError(
            f"网页内容过大（{len(data)} > 限制 {_MAX_HTML_BYTES} 字节），已拒绝导入"
        )
    return data.decode(_detect_charset(content_type), errors="replace")


def _detect_charset(content_type: str) -> str:
    """从 Content-Type 头中提取字符集，默认 utf-8。"""
    match = re.search(r"charset=([^;]+)", content_type, re.I)
    return match.group(1).strip() if match else "utf-8"


def _html_to_candidate_markdown(html: str, *, source_url: str = "") -> str:
    """把 HTML 粗略转换成候选 Markdown，供 LLM 判断正文边界。

    ``source_url`` 用于将相对路径的图片 URL 解析为绝对地址。
    """
    parser = _CandidateMarkdownParser(source_url=source_url)
    parser.feed(html)
    parser.close()
    return _normalize_blank_lines(parser.markdown())


def _normalize_blank_lines(text: str) -> str:
    """清理多余空白行和行尾空格。"""
    text = unescape(text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


class _CandidateMarkdownParser(HTMLParser):
    """面向正文抽取的轻量 HTML 到 Markdown 转换器。"""

    def __init__(self, *, source_url: str = "") -> None:
        super().__init__(convert_charrefs=True)
        self._parts: list[str] = []
        self._drop_depth = 0
        self._link_stack: list[str] = []
        self._list_depth = 0
        self._in_pre = False
        self._source_url = source_url

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag in _DROP_TAGS:
            self._drop_depth += 1
            return
        if self._drop_depth:
            return
        attrs_dict = {k.lower(): v for k, v in attrs if v}
        if tag in _HEADING_TAGS:
            level = int(tag[1])
            self._newline(2)
            self._parts.append("#" * level + " ")
        elif tag in _BLOCK_TAGS:
            self._newline(2)
        elif tag == "br":
            self._newline(1)
        elif tag == "img":
            # 将图片转换为 Markdown 图片语法，相对路径解析为绝对地址
            src = attrs_dict.get("src", "")
            alt = attrs_dict.get("alt", "")
            if src:
                src = self._resolve_url(src)
                self._newline(2)
                self._parts.append(f"![{alt}]({src})")
                self._newline(2)
        elif tag in {"ul", "ol"}:
            self._list_depth += 1
            self._newline(1)
        elif tag == "li":
            self._newline(1)
            self._parts.append("  " * max(self._list_depth - 1, 0) + "- ")
        elif tag == "blockquote":
            self._newline(2)
            self._parts.append("> ")
        elif tag == "pre":
            self._newline(2)
            self._parts.append("```\n")
            self._in_pre = True
        elif tag == "a":
            self._link_stack.append(attrs_dict.get("href", ""))
            self._parts.append("[")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in _DROP_TAGS and self._drop_depth:
            self._drop_depth -= 1
            return
        if self._drop_depth:
            return
        if tag in _HEADING_TAGS or tag in _BLOCK_TAGS:
            self._newline(2)
        elif tag in {"ul", "ol"}:
            self._list_depth = max(0, self._list_depth - 1)
            self._newline(1)
        elif tag == "li":
            self._newline(1)
        elif tag == "blockquote":
            self._newline(2)
        elif tag == "pre":
            if not self._parts or not self._parts[-1].endswith("\n"):
                self._newline(1)
            self._parts.append("```")
            self._newline(2)
            self._in_pre = False
        elif tag == "a" and self._link_stack:
            href = self._link_stack.pop()
            self._parts.append(f"]({href})" if href else "]")

    def handle_data(self, data: str) -> None:
        if self._drop_depth:
            return
        if self._in_pre:
            self._parts.append(data)
            return
        text = re.sub(r"\s+", " ", data)
        if text.strip():
            self._parts.append(text)

    def markdown(self) -> str:
        return "".join(self._parts)

    def _newline(self, count: int) -> None:
        current = "".join(self._parts[-2:])
        existing = len(current) - len(current.rstrip("\n"))
        needed = max(0, count - existing)
        if needed:
            self._parts.append("\n" * needed)

    def _resolve_url(self, src: str) -> str:
        """将相对路径的图片 URL 解析为绝对地址。"""
        if not self._source_url or src.startswith(("http://", "https://", "//")):
            return src
        return urllib.parse.urljoin(self._source_url, src)
