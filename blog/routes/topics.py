from __future__ import annotations

from flask import Blueprint, abort, current_app, render_template, request

from blog.content import ContentRepository

topics_bp = Blueprint("topics", __name__)

# 站点名称，用于 SEO 标签（OG、结构化数据等）
SITE_NAME = "随笔记录"


@topics_bp.route("/topic/<slug>.html")
def detail(slug: str):
    repository: ContentRepository = current_app.config["CONTENT_REPOSITORY"]
    topic = repository.get_topic(slug)
    if topic is None:
        abort(404)
    return render_template(
        "light/topic.html",
        topic=topic,
        canonical_url=request.base_url,
        site_name=SITE_NAME,
    )
