from __future__ import annotations

from flask import Blueprint, abort, current_app, render_template, request

from blog.content import ContentRepository

posts_bp = Blueprint("posts", __name__)

# 站点名称，用于 SEO 标签（OG、结构化数据等）
SITE_NAME = "随笔记录"


@posts_bp.route("/posts/<slug>.html")
def detail(slug: str):
    repository: ContentRepository = current_app.config["CONTENT_REPOSITORY"]
    post = repository.get_post(slug)
    if post is None:
        abort(404)
    return render_template(
        "light/post.html",
        post=post,
        canonical_url=request.base_url,
        site_name=SITE_NAME,
    )
