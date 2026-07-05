"""LLM 服务：调用 OpenAI 兼容的 Chat Completions 接口，
为发布文章自动生成 URL slug 与简介。

设计要点：
- 仅使用标准库 ``urllib``，不引入额外 HTTP 依赖，保持项目轻量；
- 失败时抛出 ``LLMError``，由路由层捕获并走兜底逻辑，保证发布不中断；
- slug 严格限定为小写字母、数字与连字符，对所有输入做防御性清洗。
"""

from __future__ import annotations

import json
import logging
import re
import secrets
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import date
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

# LLM 专用 logger；handler 在应用工厂创建时按天滚动配置
logger = logging.getLogger("blog.llm")


def init_llm_logger(log_dir: Path) -> None:
    """配置按天滚动的 LLM 请求文件日志。

    日志文件为 ``llm.log``，每天午夜滚动，历史文件为 ``llm.log.YYYY-MM-DD``，保留 30 天。
    多次调用安全（已配置 handler 时跳过）。
    """
    log_dir.mkdir(parents=True, exist_ok=True)
    if logger.handlers:
        return
    handler = TimedRotatingFileHandler(
        log_dir / "llm.log",
        when="midnight",
        backupCount=30,
        encoding="utf-8",
    )
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False

# 正文过长时截断到该长度，控制 LLM 调用成本
_MAX_BODY_CHARS = 4000

# 网页导入候选正文最大长度
_MAX_ARTICLE_CHARS = 100000

# slug 允许的字符集：小写字母、数字、连字符
_SLUG_ALLOWED = re.compile(r"[^a-z0-9-]")

# 支持「思考/推理」开关的供应商：DeepSeek、通义千问（DashScope）、OpenRouter 等。
# 标准的 OpenAI 兼容接口会被未知参数严格校验而可能返回 400，
# 因此仅在 base_url 命中下列关键词时才下发关闭推理的参数。
_THINKING_HOSTS = ("deepseek", "dashscope", "openrouter")
# DashScope 专用 header 的匹配关键词
_DASHSCOPE_HOST = "dashscope"


def _host_of(base_url: str) -> str:
    """从 base_url 提取小写主机名，解析失败返回空串。"""
    try:
        return (urllib.parse.urlparse(base_url).hostname or "").lower()
    except Exception:
        return ""


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
    usage: dict | None = None  # 包含 prompt_tokens / completion_tokens / total_tokens


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

# ---------------------------------------------------------------------------
# 文章格式化系统提示与用户提示模板
# ---------------------------------------------------------------------------
_REFORMAT_SYSTEM_PROMPT = "你是一个专业的文档编辑，擅长将原始内容整理为结构清晰的 Markdown 文档。"

_REFORMAT_USER_TEMPLATE = """\
请将下面的原始内容整理成一篇结构清晰的 Markdown 文档。

要求：
1. 保留原文核心信息，不改变原意。
2. 使用 Markdown 标题、列表、表格等格式进行排版。
3. 在文章开头生成目录。
4. 内容按主题或项目分段整理。
5. 如果有图片、视频、链接，请保留原始地址。
6. 如果有清单类内容，请尽量整理成表格。
7. 语言表达要清楚、自然、适合阅读。
8. 不要添加原文没有的信息。
9. 最后可以增加一个简短总结。

请严格只返回如下 JSON，不要包含解释或 markdown 代码围栏：
{{"body": "整理后的 Markdown 正文"}}

原始内容如下：

{content}"""


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
    usage = raw.get("usage")
    return ArticleMarkdown(body=body, usage=usage)


def reformat_markdown(
    raw_content: str,
    *,
    base_url: str,
    api_key: str,
    model: str,
    temperature: float = 0.3,
) -> str:
    """调用 LLM 将原始内容整理为结构清晰的 Markdown 文档。

    返回整理后的 Markdown 正文，用于发布页「格式化」按钮。
    """
    if not base_url or not api_key or not model:
        raise LLMError("LLM not configured (base_url/api_key/model missing)")
    if not raw_content.strip():
        raise LLMError("empty content to reformat")

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": _REFORMAT_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": _REFORMAT_USER_TEMPLATE.format(
                    content=raw_content[:_MAX_ARTICLE_CHARS],
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
        raise LLMError("LLM returned empty formatted body")
    return body


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


def _log_llm_call(url: str, payload: dict, result: dict) -> None:
    """记录 LLM 请求到日志：模型名、URL、token 用量、提示词（截 50 字）。"""
    model = payload.get("model", "?")
    messages = payload.get("messages", [])
    # 提取用户消息中的提示词文本，多条消息合并
    prompt_parts = []
    for msg in messages:
        if isinstance(msg, dict):
            content = msg.get("content", "")
            if isinstance(content, str):
                prompt_parts.append(content)
    prompt_text = " | ".join(prompt_parts)
    if len(prompt_text) > 50:
        prompt_text = prompt_text[:50] + "..."
    usage = result.get("usage", {})
    prompt_tokens = usage.get("prompt_tokens", 0)
    completion_tokens = usage.get("completion_tokens", 0)
    total_tokens = usage.get("total_tokens", 0)
    logger.info(
        "model=%s | url=%s | tokens=%d/%d/%d | prompt=%s",
        model,
        url,
        prompt_tokens,
        completion_tokens,
        total_tokens,
        prompt_text,
    )


def _post_json(url: str, api_key: str, payload: dict) -> dict:
    """向 OpenAI 兼容接口发起 POST，返回解析后的 JSON 响应。"""
    # 仅对支持「思考/推理」的供应商下发关闭推理的参数，
    # 避免对严格的 OpenAI 兼容接口因未知参数而返回 400。
    host = _host_of(url)
    if any(name in host for name in _THINKING_HOSTS):
        payload["thinking"] = {"type": "disabled"}
        payload["enable_thinking"] = False
        payload["disable_reasoning"] = True
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    # DashScope 专用 header，仅对 DashScope 接口下发
    if _DASHSCOPE_HOST in host:
        headers["X-DashScope-WorkRunnable"] = "false"
    req = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers=headers,
    )
    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            _log_llm_call(url, payload, result)
            return result
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
