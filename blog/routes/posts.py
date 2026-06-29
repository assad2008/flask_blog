from __future__ import annotations

from flask import Blueprint, abort, current_app, render_template

from blog.content import ContentRepository

posts_bp = Blueprint("posts", __name__)


@posts_bp.route("/posts/<slug>.html")
def detail(slug: str):
    repository: ContentRepository = current_app.config["CONTENT_REPOSITORY"]
    post = repository.get_post(slug)
    if post is None:
        abort(404)
    return render_template("light/post.html", post=post)
