# flask_blog

一个使用 Flask 和本地 Markdown 文件构建的博客系统。内容保存在 `content/posts/` 和 `content/topics/` 中，并通过 Git 管理。

## 技术栈

- Python 3.12+
- Flask 3.x
- Jinja2
- 本地 Markdown 文件
- python-frontmatter
- markdown-it-py
- pytest
- ruff

## 安装

```bash
pip install -e ".[dev,server]"
```

## 启动开发服务器

```bash
flask --app blog:create_app --debug run
```

也可以运行：

```bash
python app.py
```

## 生产运行

Linux：

```bash
gunicorn "blog:create_app()" --bind 0.0.0.0:8080
```

Windows 或简单部署：

```bash
waitress-serve --listen=0.0.0.0:8080 --call blog:create_app
```

## 内容目录

```text
content/posts/   文章 Markdown
content/topics/  独立页面 Markdown
```

文章文件示例：

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

兼容旧字段：`Title`、`Summary`、`Authors`、`Date`。

## URL

- `/`
- `/page/<page>.html`
- `/archives.html`
- `/posts/<slug>.html`
- `/topic/<slug>.html`

## 测试和格式化

```bash
pytest
ruff check .
ruff format .
```
