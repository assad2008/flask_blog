"""网页导入服务：抓取 URL，清洗 HTML，并交给 LLM 提取未改写的 Markdown 正文。"""

from __future__ import annotations

import re
import urllib.error
import urllib.parse
import urllib.request
from html import unescape
from html.parser import HTMLParser

from blog.services.llm import LLMError, extract_article_markdown

_MAX_HTML_BYTES = 1_500_000
_MAX_CANDIDATE_CHARS = 20000
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


def fetch_article_markdown(url: str, *, base_url: str, api_key: str, model: str) -> str:
    """抓取网页并返回由 LLM 提取的 Markdown 正文。"""
    normalized_url = _validate_url(url)
    html = _fetch_html(normalized_url)
    candidate_text = _html_to_candidate_markdown(html, source_url=normalized_url)
    if not candidate_text.strip():
        raise WebImportError("未提取到可供分析的网页正文")

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

    body = article.body.strip()
    if not body:
        raise WebImportError("未提取到正文")
    return body


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
        raise WebImportError("网页内容过大，已拒绝导入")
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
    return _normalize_blank_lines(parser.markdown())[:_MAX_CANDIDATE_CHARS]


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
