# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概览

这是一个现代化的 Flask 博客应用，使用本地 Markdown 文件存储内容。`content/posts/` 下的 Markdown 文件为文章；`content/topics/` 下的 Markdown 文件为独立页面。无需数据库、OSS 或 Redis。

技术栈：Python 3.12+、Flask 3.x、Jinja2、python-frontmatter、markdown-it-py、pytest、ruff。

## 常用命令

当前 Python 环境在 `.venv`。在仓库根目录（`flask_blog/`）运行命令。

```bash
pip install -e ".[dev,server]"
flask --app blog:create_app --debug run
python app.py
gunicorn "blog:create_app()" --bind 0.0.0.0:8080
waitress-serve --listen=0.0.0.0:8080 --call blog:create_app
pytest
pytest tests/test_repository.py
pytest tests/test_repository.py::test_list_posts_reads_markdown_and_sorts_by_date_desc
ruff check .
ruff format .
```

## 架构说明

- `app.py` 是 Flask 开发服务器入口，通过调用 `blog.create_app()` 创建应用。
- `blog/__init__.py` 定义应用工厂 `create_app(settings=None) -> Flask`，注册蓝图和错误处理器。
- `blog/config.py` 是配置模块，提供 `Settings` 数据类，通过 `Settings.from_env()` 从环境变量加载配置。
- `blog/routes/` 包含路由蓝图：
  - `index.py`：`/`、`/page/<int:page>.html`、`/archives.html`
  - `posts.py`：`/posts/<slug>.html`
  - `topics.py`：`/topic/<slug>.html`
- `blog/content/` 包含内容层：
  - `types.py`：`Post`、`Topic`、`Page` 数据类
  - `markdown.py`：Markdown 解析和 front matter 提取
  - `repository.py`：`ContentRepository` 从本地文件系统读取内容
  - `pagination.py`：纯分页函数
- `blog/templates/light/` 是当前主题模板目录。模板使用 Jinja2 继承，`base.html` 为共享 HTML 壳。
- `content/posts/` 和 `content/topics/` 为本地 Markdown 内容目录。
- `tests/` 包含 pytest 测试套件，覆盖 markdown 解析、分页、内容仓库和路由。

## 内容格式

文章和主题都是带有 front matter 的 Markdown 文件：

```markdown
---
title: Example title
summary: Example summary
authors:
  - Author name
date: 2026-06-28
---

Markdown content...
```

兼容旧字段：`Title`、`Summary`、`Authors`、`Date`（小写优先）。文章列表依赖 `date`、`title` 和 `summary`。

## 修改注意事项

- 保持路由处理函数简洁；内容逻辑放在 `blog/content/` 中。
- 内容通过本地文件系统读取，无需缓存失效逻辑。
- 依赖由 `pyproject.toml` 管理，使用 `pip install -e ".[dev,server]"` 安装。
- 使用 `pytest` 进行测试，`ruff` 进行 lint 和格式化。
