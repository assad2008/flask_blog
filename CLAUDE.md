# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概览

这是一个旧版 Flask 博客应用，使用阿里云 OSS 存储博客内容，而不是使用数据库。OSS 中 `blogs/` 前缀下的 Markdown 文件会被视为文章；`topics/` 前缀下的 Markdown 文件会被渲染为独立的主题/页面内容。README 中描述该应用的业务逻辑由 Flask 编写，通过 Tornado 对外提供服务，并使用 Redis 做缓存。

代码使用了较老的 Python/Flask 写法，例如 `flask.ext.*`，以及类似 `from settings import THEME_NAME` 的隐式相对导入。因此，除非明确要现代化导入方式和依赖，否则应优先使用 Python 2 / 旧版 Flask 兼容环境。

## 常用命令

在仓库根目录（`flask_blog/`）运行命令。

```bash
# 安装项目列出的依赖
pip install -r requirements.txt

# 启动生产风格的 Tornado WSGI 服务（默认端口为 8080）
python server.py --port=8080

# 启动 Flask 内置开发服务器
python app.py
```

应用要能正常提供真实内容，需要先完成以下配置：

- 在 `blog/settings.py` 中设置 OSS 凭据和 Bucket 信息：`OSS_ENDPOINT`、`OSS_KEY`、`OSS_SECRET`、`OSS_BUCKET`。
- 按照 `README.md` 的说明，确保 OSS Bucket 中包含 `blogs/` 和 `topics/` 目录/前缀。
- 在 `blog/settings.py` 中配置 Redis：`REDIS_HOST` 和 `REDIS_PORT`；`blog/utils/rediscache.py` 会通过 `rc` 包连接 Redis。
- `blog/settings.py` 中的 `WEB_LOG` 会作为 Tornado 的 `log_file_prefix` 使用。

当前仓库中没有测试套件、测试运行器配置或 lint 配置。如果以后添加测试，请同时在这里记录该项目专用的准确测试命令。

## 架构说明

- `server.py` 是部署时的主要入口。它从 `app.py` 导入 Flask app，将其包装到 Tornado 的 `WSGIContainer` 中，并绑定 `--host` / `--port` 选项。
- `app.py` 通过调用 `blog.create_app()` 创建 Flask 应用。
- `blog/__init__.py` 定义应用工厂。它注册来自 `blog.views.index`、`blog.views.post` 和 `blog.views.topic` 的所有蓝图，并通过主题模板辅助函数配置简单的 404/500 错误处理。
- `blog/settings.py` 是集中配置模块，包含主题名、OSS、Redis、语言/时区、分页、静态路径和日志配置。
- `blog/views/` 只包含路由处理：
  - `/` 和 `/page/<int:page>.html` 从 OSS 列出文章。
  - `/archives.html` 列出全部文章。
  - `/posts/<filename>.html` 加载 `blogs/<filename>.md`。
  - `/topic/<filename>.html` 加载 `topics/<filename>.md`。
- `blog/models/` 包含基于 OSS 的内容访问逻辑。`post.py` 从 OSS 列出并加载博客 Markdown，提取 Markdown metadata，按 `Date` 对文章排序，并将完整文章列表缓存到 Redis 的 `allblogs` 键下。`topic.py` 从 OSS 加载主题 Markdown。
- `blog/utils/__init__.py` 包含 Markdown 转换辅助函数，使用 `markdown2` extras，包括 metadata、tables、code highlighting、TOC、footnotes 和 wiki links。
- `blog/helper.py` 通过给模板名加上 `THEME_NAME` 前缀，集中处理主题模板渲染。
- `templates/Light/` 是当前由 `THEME_NAME = 'Light'` 选中的主题。模板期望 Markdown metadata 中包含 `Title`、`Date` 和 `Summary` 等字段。

## 内容格式

文章和主题都是带有 `markdown2` metadata front matter 的 Markdown 文件。示例文件 `awesome-php.md` 使用如下结构：

```markdown
---
Title:  Example title
Summary: Example summary
Authors: Author name
Date:    2015-01-08
---

Markdown content...
```

文章列表依赖 `Date`、`Title` 和 `Summary`；文章/主题详情页会渲染转换后的 Markdown HTML，并在模板中通过 `blog.metadata` 或 `topics.metadata` 访问 metadata。

## 修改注意事项

- 保持路由处理函数简洁；按照现有分层，将 OSS/内容转换逻辑放在 `blog/models/` 或 `blog/utils/` 中。
- 修改 `get_blogs()` 缓存逻辑时要谨慎：主页和归档页都会使用缓存的 `allblogs` 数据，而仓库中没有缓存失效代码。
- 依赖列表未固定版本，并且相对于当前代码看起来不完整（`blog/models/post.py` 导入了 `pypages`，但 `requirements.txt` 没有列出它）。在假设全新安装可用之前，请先在目标运行环境中验证依赖行为。