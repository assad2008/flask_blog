from __future__ import annotations

from flask import Blueprint, abort, current_app, render_template

from blog.content import ContentRepository

topics_bp = Blueprint("topics", __name__)


@topics_bp.route("/topic/<slug>.html")
def detail(slug: str):
    repository: ContentRepository = current_app.config["CONTENT_REPOSITORY"]
    topic = repository.get_topic(slug)
    if topic is None:
        abort(404)
    return render_template("light/topic.html", topic=topic)
