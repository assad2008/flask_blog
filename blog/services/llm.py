"""LLM 服务：调用 OpenAI 兼容的 Chat Completions 接口，
为发布文章自动生成 URL slug 与简介。

设计要点：
- 仅使用标准库 ``urllib``，不引入额外 HTTP 依赖，保持项目轻量；
- 失败时抛出 ``LLMError``，由路由层捕获并走兜底逻辑，保证发布不中断；
- slug 严格限定为小写字母、数字与连字符，对所有输入做防御性清洗。
"""

from __future__ import annotations

import json
import re
import secrets
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import date

# 正文过长时截断到该长度，控制 LLM 调用成本
_MAX_BODY_CHARS = 4000

# 网页导入候选正文最大长度
_MAX_ARTICLE_CHARS = 20000

# slug 允许的字符集：小写字母、数字、连字符
_SLUG_ALLOWED = re.compile(r"[^a-z0-9-]")


class LLMError(Exception):
    """LLM 调用失败或未配置时抛出，调用方应走兜底逻辑。"""


@dataclass(frozen=True)
class PostMetadata:
    """LLM 为一篇文章生成的元数据。"""

    title: str
    slug: str
    summary: str


@dataclass(frozen=True)
class ArticleMarkdown:
    """网页导入功能提取出的 Markdown 正文。"""

    body: str


# ---------------------------------------------------------------------------
# 系统提示与用户提示模板
# ---------------------------------------------------------------------------
_SYSTEM_PROMPT = "你是一个博客编辑助手。根据文章标题和正文，生成标题、URL slug 和一段简介。"

_USER_TEMPLATE = """\
title 要求：
- 用中文撰写（与正文语言一致）
- 简洁有吸引力，不超过 30 字
- 不要加书名号《》或引号

slug 要求：
- 仅包含小写英文字母 a-z、数字 0-9 和连字符 -
- 能用英文体现文章主题，不要使用中文或拼音
- 长度不超过 60 个字符

summary 要求：
- 用中文撰写
- 1-2 句话，80-150 字
- 概括文章核心内容，不要简单复述标题

请严格只返回如下 JSON，不要包含任何解释或 markdown 代码块：
{{"title": "...", "slug": "...", "summary": "..."}}

文章标题（可能为空，为空时请根据正文生成）：{title}

文章正文：
{body}"""

# ---------------------------------------------------------------------------
# 网页正文提取的系统提示与用户提示模板
# ---------------------------------------------------------------------------
_ARTICLE_SYSTEM_PROMPT = "你是一个严格的网页正文抽取器，只负责识别正文边界并输出 Markdown。"

_ARTICLE_USER_TEMPLATE = """\
请从下面的网页候选内容中提取真正的文章正文，并输出 Markdown。

硬性要求：
- 不要改写任何正文句子。
- 不要总结。
- 不要翻译。
- 不要润色。
- 不要添加原文没有的观点、解释或段落。
- 只删除导航、广告、推荐阅读、评论区、版权声明、登录提示等非正文噪音。
- 尽量保留原文的标题层级、段落、列表、引用、代码块和链接结构。
- 不要生成 title、slug 或 summary。

请严格只返回如下 JSON，不要包含解释或 markdown 代码围栏：
{{"body": "Markdown 正文"}}

来源 URL：{source_url}

网页候选内容：
{candidate_text}"""


def extract_article_markdown(
    source_url: str,
    candidate_text: str,
    *,
    base_url: str,
    api_key: str,
    model: str,
    temperature: float = 0.0,
) -> ArticleMarkdown:
    """调用 LLM 从网页候选内容中提取未改写的 Markdown 正文。"""
    if not base_url or not api_key or not model:
        raise LLMError("LLM not configured (base_url/api_key/model missing)")
    if not candidate_text.strip():
        raise LLMError("empty candidate article content")

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": _ARTICLE_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": _ARTICLE_USER_TEMPLATE.format(
                    source_url=source_url,
                    candidate_text=candidate_text[:_MAX_ARTICLE_CHARS],
                ),
            },
        ],
        "temperature": temperature,
    }

    try:
        raw = _post_json(f"{base_url.rstrip('/')}/chat/completions", api_key, payload)
        content = raw["choices"][0]["message"]["content"]
        parsed = _parse_llm_json(content)
    except LLMError:
        raise
    except Exception as exc:  # noqa: BLE001 - 统一转换为调用方可展示的错误
        raise LLMError(f"LLM request failed: {exc}") from exc

    body = str(parsed.get("body") or "").strip()
    if not body:
        raise LLMError("LLM returned empty article body")
    return ArticleMarkdown(body=body)


def extract_metadata(
    title: str,
    body: str,
    *,
    base_url: str,
    api_key: str,
    model: str,
    temperature: float = 0.3,
) -> PostMetadata:
    """调用 LLM 生成标题、slug 与 summary。

    任何环节（未配置、网络错误、解析失败）出错均抛出 ``LLMError``。
    ``temperature`` 越高输出越发散，生成候选时可调高以获得多样性。
    """
    if not base_url or not api_key or not model:
        raise LLMError("LLM not configured (base_url/api_key/model missing)")

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": _SYSTEM_PROMPT},
            {
                "role": "user",
                "content": _USER_TEMPLATE.format(title=title, body=body[:_MAX_BODY_CHARS]),
            },
        ],
        "temperature": temperature,
    }

    try:
        raw = _post_json(f"{base_url.rstrip('/')}/chat/completions", api_key, payload)
        content = raw["choices"][0]["message"]["content"]
        parsed = _parse_llm_json(content)
    except LLMError:
        raise
    except Exception as exc:  # noqa: BLE001 - 任何异常都降级为 LLMError
        raise LLMError(f"LLM request failed: {exc}") from exc

    gen_title = str(parsed.get("title") or "").strip()
    slug = sanitize_slug(parsed.get("slug", ""))
    summary = str(parsed.get("summary") or "").strip()
    if not slug:
        raise LLMError("LLM returned empty slug")
    return PostMetadata(title=gen_title, slug=slug, summary=summary)


def fallback_metadata(title: str) -> PostMetadata:
    """LLM 不可用时的兜底：保留传入标题，从标题生成 slug，简介留空。

    标题为中文等非 ASCII 文本时，清洗后 slug 可能为空，
    此时回退为 ``post-日期-随机串`` 以保证文件可写入。
    """
    return PostMetadata(title=title, slug=_fallback_slug_from_title(title), summary="")


def sanitize_slug(raw: str) -> str:
    """将任意字符串清洗为合法 slug：小写、仅保留 a-z0-9-。

    连续非法字符折叠为单个连字符，并去掉首尾连字符。
    """
    s = raw.lower()
    s = _SLUG_ALLOWED.sub("-", s)
    s = re.sub(r"-+", "-", s)
    return s.strip("-")


def _fallback_slug_from_title(title: str) -> str:
    """从标题生成兜底 slug；清洗后为空则用日期+随机串。"""
    s = sanitize_slug(title)
    if s:
        return s[:60]
    return f"post-{date.today().isoformat()}-{secrets.token_hex(3)}"


def _post_json(url: str, api_key: str, payload: dict) -> dict:
    """向 OpenAI 兼容接口发起 POST，返回解析后的 JSON 响应。"""
    # 关闭思考模式（DeepSeek V3 / 通义千问等兼容）
    payload["thinking"] = {"type": "disabled"}
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise LLMError(f"LLM HTTP {exc.code}: {exc.reason}") from exc
    except urllib.error.URLError as exc:
        raise LLMError(f"LLM network error: {exc.reason}") from exc


def _parse_llm_json(content: str) -> dict:
    """从 LLM 返回内容中解析 JSON，兼容带 ```json 代码围栏的输出。"""
    text = content.strip()
    # 去除可能的 markdown 代码围栏
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\n?", "", text)
        text = re.sub(r"\n?```$", "", text)
    # 提取首个 {...} 块，丢弃多余文本
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        text = match.group(0)
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise LLMError(f"LLM response is not valid JSON: {content!r}") from exc
