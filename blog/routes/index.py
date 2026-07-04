from __future__ import annotations

from collections import defaultdict

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

    # 按年份分组
    year_groups: dict[int, list] = defaultdict(list)
    for post in posts:
        if post.date:
            year_groups[post.date.year].append(post)

    years = [
        {"year": year, "posts": year_posts, "count": len(year_posts)}
        for year, year_posts in sorted(year_groups.items(), reverse=True)
    ]

    return render_template("light/archives.html", posts=posts, years=years)
