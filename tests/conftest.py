import pytest

from blog import create_app
from blog.config import Settings


@pytest.fixture
def app(tmp_path, monkeypatch):
    # 测试中不创建文件日志，避免占用临时目录文件句柄
    monkeypatch.setattr("blog.routes.webhook.init_webhook_logger", lambda *_a, **_k: None)

    posts_dir = tmp_path / "posts"
    topics_dir = tmp_path / "topics"
    posts_dir.mkdir()
    topics_dir.mkdir()

    (posts_dir / "hello.md").write_text(
        """---
title: Hello
date: 2024-01-02
summary: Hello summary
---

Hello **world**.
""",
        encoding="utf-8",
    )
    (topics_dir / "about.md").write_text(
        """---
title: About
summary: About summary
---

About page.
""",
        encoding="utf-8",
    )

    settings = Settings(
        content_dir=tmp_path,
        posts_per_page=1,
        theme="light",
        secret_key="test-secret",
        base_dir=tmp_path,
        webhook_secret="",
        webhook_repo_dir=tmp_path,
        webhook_ref="",
        log_dir=tmp_path / "logs",
    )
    flask_app = create_app(settings=settings)
    flask_app.config.update(TESTING=True)
    return flask_app


@pytest.fixture
def client(app):
    return app.test_client()
