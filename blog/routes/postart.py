"""文章发布页面：在单一 ``/postart`` 路由内完成登录与发布。

- 未登录时显示登录表单（密码 + 数学验证码）；
- 登录通过后显示发布表单（标题 + 正文）；
- 提交发布时调用 LLM 生成 slug 与简介，写入 ``content/posts/<slug>.md``。

所有写文件的副作用集中在 ``blog/content/writer.py``，
LLM 调用集中在 ``blog/services/llm.py``，路由只负责编排。
"""

from __future__ import annotations

import hmac
import json as _sse_json
import queue as _sse_queue
import random
import threading as _sse_threading
import time as _sse_time
from pathlib import Path

import frontmatter
from flask import (
    Blueprint,
    Response,
    abort,
    current_app,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    stream_with_context,
    url_for,
)

from blog.config import Settings
from blog.content.writer import (
    resolve_unique_slug,
    today_iso,
    update_post_title_and_body,
    write_markdown_post,
)
from blog.services.git import commit_paths
from blog.services.llm import (
    LLMError,
    extract_metadata,
    reformat_markdown,
    sanitize_slug,
)
from blog.services.web_import import WebImportError, fetch_article_markdown

postart_bp = Blueprint("postart", __name__)

# session 中存放登录状态与验证码答案的键名
_SESSION_AUTHED = "postart_authed"
_SESSION_CAPTCHA = "postart_captcha_answer"


def _settings() -> Settings:
    return current_app.config["SETTINGS"]


def _is_authed() -> bool:
    return bool(session.get(_SESSION_AUTHED))


def _llm_ready(settings: Settings) -> bool:
    """LLM 三项配置是否齐全（缺一则走兜底）。"""
    return bool(settings.llm_base_url and settings.llm_api_key and settings.llm_model)


def _new_captcha() -> tuple[str, str]:
    """生成一道简单数学验证码，返回 (题目文本, 答案字符串)。"""
    a = random.randint(1, 9)
    b = random.randint(1, 9)
    if random.choice(["+", "-"]) == "+":
        return f"{a} + {b}", str(a + b)
    # 减法保证非负
    x, y = (a, b) if a >= b else (b, a)
    return f"{x} - {y}", str(x - y)


def _parse_authors(raw: str) -> list[str]:
    """将 .env 中的默认作者按逗号拆分为列表。"""
    return [name.strip() for name in raw.split(",") if name.strip()]


@postart_bp.route("/postart", methods=["GET", "POST"])
def postart():
    settings = _settings()
    # 未配置密码时禁用发布入口，避免暴露未授权入口（与 webhook 一致）
    if not settings.postart_password:
        abort(404)

    if request.method == "POST":
        action = request.form.get("action", "")
        if action == "login":
            return _handle_login(settings)
        if action == "logout":
            session.clear()
            return redirect(url_for("postart.postart"))
        if action == "publish":
            # 发布前必须已登录
            if not _is_authed():
                abort(403)
            return _handle_publish(settings)
        if action == "generate":
            # AI 生成标题/slug/简介（AJAX，仅返回 JSON）
            if not _is_authed():
                abort(403)
            return _handle_generate(settings)
        if action == "import_url":
            # 抓取网页正文并填入编辑区（AJAX，仅返回 JSON）
            if not _is_authed():
                abort(403)
            return _handle_import_url(settings)
        if action == "reformat":
            # 调用大模型整理文章格式（AJAX，仅返回 JSON）
            if not _is_authed():
                abort(403)
            return _handle_reformat(settings)
        if action in ("manage_list", "manage_get", "manage_delete", "manage_update"):
            # 文章管理（AJAX）
            if not _is_authed():
                abort(403)
            return _handle_manage(settings, action)
        # 未知 action 视为非法请求
        abort(400)

    # GET：按登录状态渲染登录表单或发布表单
    if not _is_authed():
        question, answer = _new_captcha()
        session[_SESSION_CAPTCHA] = answer
        return render_template("light/postart.html", mode="login", captcha=question)
    return render_template(
        "light/postart.html",
        mode="publish",
        llm_ready=_llm_ready(settings),
    )


def _handle_login(settings: Settings):
    """处理登录表单提交：校验密码与验证码。"""
    password = request.form.get("password", "")
    captcha_answer = request.form.get("captcha", "")
    expected_captcha = session.get(_SESSION_CAPTCHA, "")

    # 使用恒定时间比较防止时序攻击
    password_ok = hmac.compare_digest(password, settings.postart_password)
    captcha_ok = hmac.compare_digest(captcha_answer, expected_captcha)

    if not password_ok or not captcha_ok:
        # 校验失败：重新生成验证码后返回登录表单
        question, answer = _new_captcha()
        session[_SESSION_CAPTCHA] = answer
        return (
            render_template(
                "light/postart.html",
                mode="login",
                captcha=question,
                error="密码或验证码错误",
            ),
            401,
        )

    # 登录成功：标记会话并清理验证码
    session[_SESSION_AUTHED] = True
    session.pop(_SESSION_CAPTCHA, None)
    return redirect(url_for("postart.postart"))


def _handle_publish(settings: Settings):
    """处理发布表单提交：校验内容、生成元数据、写入/更新文件。"""
    title = request.form.get("title", "").strip()
    body = request.form.get("body", "").strip()
    edit_slug = request.form.get("edit_slug", "").strip()

    # 标题与正文均不可为空
    if not title or not body:
        return (
            render_template(
                "light/postart.html",
                mode="publish",
                llm_ready=_llm_ready(settings),
                error="标题和正文都不能为空",
                title=title,
                body=body,
            ),
            400,
        )

    posts_dir: Path = settings.content_dir / "posts"

    # 编辑已有文章模式
    if edit_slug:
        update_post_title_and_body(
            posts_dir,
            edit_slug,
            title=title,
            body=body,
        )
        post_path = posts_dir / f"{edit_slug}.md"
        git_committed, git_pushed, git_detail = commit_paths(
            settings.base_dir, [post_path], f"更新文章: {title}"
        )
        return render_template(
            "light/postart.html",
            mode="success",
            slug=edit_slug,
            title=title,
            summary="（已更新）",
            llm_used=False,
            git_committed=git_committed,
            git_pushed=git_pushed,
            git_detail=git_detail,
        )

    # 新文章：必须「生成」后才允许发布
    gen_slug = request.form.get("gen_slug", "").strip()
    gen_summary = request.form.get("gen_summary", "").strip()
    gen_seo_description = request.form.get("gen_seo_description", "").strip()
    gen_seo_keywords = request.form.get("gen_seo_keywords", "").strip()
    if not gen_slug:
        return (
            render_template(
                "light/postart.html",
                mode="publish",
                llm_ready=_llm_ready(settings),
                error="请先点击「生成」按钮生成标题、slug 和简介",
                title=title,
                body=body,
            ),
            400,
        )

    # 直接复用已生成的 slug 与简介，不再调用 AI
    slug = sanitize_slug(gen_slug)
    summary = gen_summary
    llm_used = True

    # 解决文件名冲突
    slug = resolve_unique_slug(slug, posts_dir)

    write_markdown_post(
        posts_dir,
        slug,
        title=title,
        summary=summary,
        authors=_parse_authors(settings.postart_author),
        date_str=today_iso(),
        body=body,
        seo_description=gen_seo_description,
        seo_keywords=gen_seo_keywords,
    )

    # 提交并推送到 git（推送失败不影响发布结果，仅在成功页提示）
    post_path = posts_dir / f"{slug}.md"
    git_committed, git_pushed, git_detail = commit_paths(
        settings.base_dir, [post_path], f"发布文章: {title}"
    )

    return render_template(
        "light/postart.html",
        mode="success",
        slug=slug,
        title=title,
        summary=summary,
        llm_used=llm_used,
        git_committed=git_committed,
        git_pushed=git_pushed,
        git_detail=git_detail,
    )


def _handle_generate(settings: Settings):
    """AI 生成标题/slug/简介（AJAX 接口，返回 JSON）。

    发布页“生成”按钮调用：基于正文（及可选标题）由大模型生成
    标题、slug、简介，供用户选择后再发布。
    """
    body = request.form.get("body", "").strip()
    title = request.form.get("title", "").strip()
    if not body:
        return jsonify({"ok": False, "error": "正文不能为空，请先写正文"}), 400

    try:
        metadata = extract_metadata(
            title,
            body,
            base_url=settings.llm_base_url,
            api_key=settings.llm_api_key,
            model=settings.llm_model,
            # 生成候选时调高温度，多次生成可获得不同标题供选择
            temperature=0.9,
        )
    except LLMError as exc:
        return jsonify({"ok": False, "error": f"生成失败：{exc}"})

    return jsonify(
        {
            "ok": True,
            "title": metadata.title,
            "slug": metadata.slug,
            "summary": metadata.summary,
            "seo_description": metadata.seo_description,
            "seo_keywords": metadata.seo_keywords,
        }
    )


def _handle_import_url(settings: Settings):
    """抓取网页正文并以 SSE 流式输出进度日志，前端实时渲染终端风格日志。"""

    url = request.form.get("url", "").strip()

    def generate():
        q: _sse_queue.Queue = _sse_queue.Queue()
        start_time = _sse_time.time()

        # LLM 未配置时直接返回错误事件
        if not _llm_ready(settings):
            yield (
                "data: "
                + _sse_json.dumps(
                    {
                        "type": "done",
                        "ok": False,
                        "error": "未配置 LLM，无法分析网页正文",
                        "elapsed": 0,
                    },
                    ensure_ascii=False,
                )
                + "\n\n"
            )
            return

        def on_progress(data: dict) -> None:
            elapsed = round(_sse_time.time() - start_time, 1)
            data["elapsed"] = elapsed
            q.put(data)

        def worker():
            try:
                body = fetch_article_markdown(
                    url,
                    base_url=settings.llm_base_url,
                    api_key=settings.llm_api_key,
                    model=settings.llm_model,
                    on_progress=on_progress,
                )
                total_elapsed = round(_sse_time.time() - start_time, 1)
                q.put(
                    {
                        "type": "done",
                        "ok": True,
                        "body": body,
                        "elapsed": total_elapsed,
                    }
                )
            except WebImportError as exc:
                total_elapsed = round(_sse_time.time() - start_time, 1)
                q.put(
                    {
                        "type": "log",
                        "message": f"失败：{exc}",
                        "elapsed": total_elapsed,
                    }
                )
                q.put(
                    {
                        "type": "done",
                        "ok": False,
                        "error": str(exc),
                        "elapsed": total_elapsed,
                    }
                )
            except Exception as exc:
                total_elapsed = round(_sse_time.time() - start_time, 1)
                msg = f"未知错误：{exc}"
                q.put({"type": "log", "message": msg, "elapsed": total_elapsed})
                q.put(
                    {
                        "type": "done",
                        "ok": False,
                        "error": msg,
                        "elapsed": total_elapsed,
                    }
                )

        t = _sse_threading.Thread(target=worker, daemon=True)
        t.start()

        try:
            while True:
                try:
                    item = q.get(timeout=0.5)
                    yield "data: " + _sse_json.dumps(item, ensure_ascii=False) + "\n\n"
                    if item["type"] == "done":
                        break
                except _sse_queue.Empty:
                    # 心跳注释，防止代理/反向代理因长时间无数据而断开
                    yield ": heartbeat\n\n"
        except GeneratorExit:
            pass
        finally:
            t.join(timeout=5)

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )


def _handle_reformat(settings: Settings):
    """调用大模型将编辑器正文整理为结构清晰的 Markdown 文档（AJAX 接口）。"""
    body = request.form.get("body", "").strip()
    if not body:
        return jsonify({"ok": False, "error": "正文不能为空，请先写正文或粘贴内容"}), 400

    try:
        formatted = reformat_markdown(
            body,
            base_url=settings.llm_base_url,
            api_key=settings.llm_api_key,
            model=settings.llm_model,
            temperature=0.3,
        )
    except LLMError as exc:
        return jsonify({"ok": False, "error": f"格式化失败：{exc}"})

    return jsonify({"ok": True, "body": formatted})


def _handle_manage(settings: Settings, action: str):
    """文章管理接口：列出/查看/删除/更新已有文章（AJAX，仅返回 JSON）。"""
    from blog.content import ContentRepository

    repository: ContentRepository = current_app.config["CONTENT_REPOSITORY"]
    posts_dir: Path = settings.content_dir / "posts"

    if action == "manage_list":
        posts = repository.list_posts()
        return jsonify(
            {
                "ok": True,
                "posts": [
                    {
                        "slug": p.slug,
                        "title": p.title,
                        "date": p.date.isoformat() if p.date else "",
                        "summary": p.summary,
                    }
                    for p in posts
                ],
            }
        )

    slug = request.form.get("slug", "").strip()
    if not slug:
        return jsonify({"ok": False, "error": "缺少文章 slug"}), 400

    if action == "manage_get":
        raw = repository.get_post_raw(slug)
        if raw is None:
            return jsonify({"ok": False, "error": f"文章不存在：{slug}"}), 404
        parsed = frontmatter.loads(raw)
        meta = parsed.metadata
        title = meta.get("title") or meta.get("Title") or slug
        date_str = ""
        d = meta.get("date") or meta.get("Date")
        if d:
            date_str = str(d)
        summary = meta.get("summary") or meta.get("Summary") or ""
        authors = meta.get("authors") or meta.get("Authors") or []
        seo_description = meta.get("seo_description") or meta.get("Seo_Description") or ""
        seo_keywords = meta.get("seo_keywords") or meta.get("Seo_Keywords") or ""
        if isinstance(authors, str):
            authors = [authors]
        return jsonify(
            {
                "ok": True,
                "slug": slug,
                "title": str(title),
                "date": date_str,
                "summary": str(summary),
                "authors": [str(a) for a in authors],
                "body": parsed.content.strip(),
                "seo_description": str(seo_description),
                "seo_keywords": str(seo_keywords),
            }
        )

    if action == "manage_delete":
        if not repository.delete_post(slug):
            return jsonify({"ok": False, "error": f"删除失败：{slug}"}), 404
        post_path = posts_dir / f"{slug}.md"
        commit_paths(settings.base_dir, [post_path], f"删除文章: {slug}")
        return jsonify({"ok": True})

    if action == "manage_update":
        title = request.form.get("title", "").strip()
        body = request.form.get("body", "").strip()
        if not title or not body:
            return jsonify({"ok": False, "error": "标题和正文都不能为空"}), 400
        if repository.get_post_raw(slug) is None:
            return jsonify({"ok": False, "error": f"文章不存在：{slug}"}), 404
        update_post_title_and_body(
            posts_dir,
            slug,
            title=title,
            body=body,
        )
        post_path = posts_dir / f"{slug}.md"
        commit_paths(settings.base_dir, [post_path], f"更新文章: {slug}")
        return jsonify({"ok": True})

    abort(400)
