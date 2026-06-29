from __future__ import annotations

from flask import Blueprint, current_app, render_template

from blog.content import ContentRepository, paginate_posts

index_bp = Blueprint("index", __name__)


@index_bp.route("/")
@index_bp.route("/page/<int:page>.html")
def index(page: int = 1):
    repository: ContentRepository = current_app.config["CONTENT_REPOSITORY"]
    posts = repository.list_posts()
    paginated = paginate_posts(
        posts,
        current_page=page,
        per_page=current_app.config["POSTS_PER_PAGE"],
    )
    return render_template("light/index.html", page=paginated)


@index_bp.route("/archives.html")
def archives():
    repository: ContentRepository = current_app.config["CONTENT_REPOSITORY"]
    posts = repository.list_posts()
    return render_template("light/archives.html", posts=posts)
