from __future__ import annotations

from flask import Flask, render_template

from blog.config import Settings
from blog.content import ContentRepository


def create_app(settings: Settings | None = None) -> Flask:
    settings = settings or Settings.from_env()
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=settings.secret_key,
        SETTINGS=settings,
        CONTENT_REPOSITORY=ContentRepository(settings.content_dir),
        POSTS_PER_PAGE=settings.posts_per_page,
        THEME=settings.theme,
    )

    # 测试环境下不初始化文件日志，避免占用临时目录文件句柄
    if not app.config.get("TESTING"):
        from blog.routes.webhook import init_webhook_logger

        init_webhook_logger(settings.log_dir)

    from blog.routes.index import index_bp
    from blog.routes.postart import postart_bp
    from blog.routes.posts import posts_bp
    from blog.routes.topics import topics_bp
    from blog.routes.webhook import webhook_bp

    app.register_blueprint(index_bp)
    app.register_blueprint(postart_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(topics_bp)
    app.register_blueprint(webhook_bp)
    register_error_handlers(app)

    # 向所有模板注入发布入口开关：仅当配置了发布密码时才在底部显示入口
    # 读取 app.config（而非闭包变量），便于运行时替换 Settings 生效
    @app.context_processor
    def inject_postart_enabled():
        return {"postart_enabled": bool(app.config["SETTINGS"].postart_password)}

    return app


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("light/404.html"), 404
