# Flask Blog 现代化改造设计

日期：2026-06-28

## 背景

当前项目是一个旧版 Flask 博客应用。它使用 Flask 编写业务逻辑，通过 Tornado 包装 WSGI 对外服务，从阿里云 OSS 读取 Markdown 内容，并使用 Redis 缓存文章列表。代码使用了较老的 Python/Flask 写法，例如 `flask.ext.*`、隐式相对导入和未固定版本依赖。

本次改造目标是保留 Flask，但使用现代 Python/Flask 技术栈重构项目，并将内容源从 OSS 改为本地 Markdown 文件，由 Git 管理。

## 已确认目标

- 保留 Flask，不迁移到其他 Web 框架。
- 删除 Tornado，不再使用 Tornado WSGI 包装。
- 删除 OSS 内容依赖。
- 删除 Redis 作为必需依赖。
- 内容改为本地 Markdown 文件，并通过 Git 管理。
- 保留现有博客 URL 结构，避免旧链接失效。
- 建立现代 Python 工具链，包括测试和 lint/format。
- 第一阶段不做前后端分离，不引入复杂前端框架。

## 非目标

第一阶段不包含以下内容：

- 重写为 Next.js、Astro、Nuxt 或其他全栈/静态站点框架。
- 引入数据库。
- 引入 Redis 或其他缓存服务作为必需组件。
- 引入复杂后台管理系统。
- 重做整套视觉设计。
- 增加标签、分类、RSS、sitemap、全文搜索等扩展功能。
- Docker 和 CI 可以后续添加，不作为第一阶段必选项。

## 推荐技术栈

- Python 3.12+
- Flask 3.x
- Jinja2
- 本地 Markdown + Git
- `python-frontmatter`：解析 front matter
- `markdown-it-py`：渲染 Markdown
- `mdit-py-plugins`：补充 Markdown 插件能力
- `pygments`：代码高亮
- `python-dotenv`：本地环境变量加载
- `pytest`：测试
- `ruff`：lint 和 format
- `gunicorn`：Linux 生产 WSGI 服务
- `waitress`：Windows 或简单部署场景

## 目标目录结构

```text
flask_blog/
  pyproject.toml
  README.md
  CLAUDE.md
  app.py
  blog/
    __init__.py
    config.py
    routes/
      __init__.py
      index.py
      posts.py
      topics.py
    content/
      __init__.py
      repository.py
      markdown.py
      pagination.py
    templates/
      light/
        base.html
        index.html
        post.html
        topic.html
        archives.html
        page.html
        404.html
    static/
      ...
  content/
    posts/
      awesome-php.md
    topics/
      about.md
  tests/
    test_markdown.py
    test_pagination.py
    test_repository.py
    test_routes.py
```

## 运行方式

开发环境使用 Flask CLI：

```bash
flask --app blog:create_app --debug run
```

可以保留轻量 `app.py`：

```bash
python app.py
```

生产环境不再使用 Tornado。Linux 推荐：

```bash
gunicorn "blog:create_app()" --bind 0.0.0.0:8080
```

Windows 或简单部署推荐：

```bash
waitress-serve --listen=0.0.0.0:8080 --call blog:create_app
```

## 依赖管理

从 `requirements.txt` 迁移到 `pyproject.toml`。

建议核心依赖：

```toml
[project]
requires-python = ">=3.12"
dependencies = [
  "Flask>=3.0",
  "python-frontmatter",
  "markdown-it-py",
  "mdit-py-plugins",
  "pygments",
  "python-dotenv",
]
```

建议可选依赖：

```toml
[project.optional-dependencies]
server = [
  "gunicorn; platform_system != 'Windows'",
  "waitress",
]
dev = [
  "pytest",
  "ruff",
]
```

应移除的旧依赖：

- `Tornado`
- `Flask-Cache`
- `Flask-Script`
- `Flask-Babel`，除非后续明确需要多语言
- `redis`
- `rc`
- `oss2`
- `pypages`

## 模块设计

### Flask app factory

`blog/__init__.py` 继续作为应用工厂入口，但改为现代 Flask 结构：

- 创建 Flask app。
- 加载配置。
- 注册 routes blueprints。
- 注册错误处理器。

### 配置层

新增 `blog/config.py`。

配置项包括：

- `CONTENT_DIR`
- `POSTS_PER_PAGE`
- `THEME`
- `SECRET_KEY`
- debug 相关配置

第一阶段使用 Flask config 或简单 dataclass 即可，不引入复杂配置框架。

### 路由层

`blog/routes/` 只负责：

1. 读取 URL 参数。
2. 调用内容层。
3. 渲染模板或返回 404。

保留现有 URL：

- `/`
- `/page/<int:page>.html`
- `/archives.html`
- `/posts/<slug>.html`
- `/topic/<slug>.html`

### 内容仓库层

新增 `blog/content/repository.py`。

职责：

- 扫描 `content/posts/*.md`。
- 扫描 `content/topics/*.md`。
- 根据 slug 读取文章。
- 根据 slug 读取 topic 页面。
- 忽略非 Markdown 文件。
- 不依赖 Flask request/response。
- 不负责 HTML 渲染之外的 HTTP 行为。

推荐接口：

```python
list_posts() -> list[Post]
get_post(slug: str) -> Post | None
get_topic(slug: str) -> Topic | None
```

### Markdown 渲染层

新增 `blog/content/markdown.py`。

职责：

- 解析 front matter。
- 渲染 Markdown body 为 HTML。
- 标准化 metadata 字段。
- 提供清晰的数据对象给模板使用。

推荐标准字段：

- `title`
- `summary`
- `authors`
- `date`
- `slug`
- `html`

兼容旧字段：

- `Title`
- `Summary`
- `Authors`
- `Date`

如果新旧字段同时存在，小写字段优先。

### 分页层

新增 `blog/content/pagination.py`。

职责：

- 接收文章列表、当前页和每页数量。
- 返回当前页文章和分页信息。
- 替代旧的 `pypages` 依赖。
- 不依赖 Flask。

## 数据流

文章详情页数据流：

```text
GET /posts/awesome-php.html
        ↓
routes/posts.py
        ↓
ContentRepository.get_post("awesome-php")
        ↓
MarkdownRenderer.render(file_content)
        ↓
templates/light/post.html
        ↓
HTML response
```

首页数据流：

```text
GET /
        ↓
routes/index.py
        ↓
ContentRepository.list_posts()
        ↓
按日期倒序排序
        ↓
paginate(posts, page=1)
        ↓
templates/light/index.html
```

## 内容格式

文章和 topic 使用本地 Markdown 文件。

目录：

```text
content/posts/
content/topics/
```

兼容现有 front matter：

```markdown
---
Title:  Github上的PHP资源汇总大全
Summary: 一个PHP资源列表...
Authors: Django Wong
Date:    2015-01-08
---

正文内容...
```

新文章推荐使用小写字段：

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

slug 默认来自文件名。例如：

```text
content/posts/awesome-php.md
```

对应：

```text
/posts/awesome-php.html
```

## 模板设计

保留 Light 主题的基本视觉，但整理为现代 Jinja 模板结构。

建议从旧路径：

```text
templates/Light/*.htm
```

迁移到：

```text
blog/templates/light/*.html
```

模板变量从旧形式：

```jinja2
{{ blog.metadata.get('Title') }}
```

改为：

```jinja2
{{ post.title }}
{{ post.date }}
{{ post.html|safe }}
```

建议增加 `base.html`，减少 header、footer、nav 和 HTML 骨架重复。

## 错误处理

用户可见错误：

- 文章 slug 不存在时返回 404。
- topic slug 不存在时返回 404。
- 首页没有文章时返回正常页面和空状态。
- 缺少 title 时标题回退为 slug。

开发期错误：

- 内容目录不存在时给出清晰错误提示。
- Markdown 文件解析失败时，debug 模式下显示文件路径和错误。
- 生产环境记录日志并返回 500，避免暴露内部路径。

## 缓存策略

第一阶段不引入 Redis，也不做复杂缓存。

默认策略：每次请求读取本地 Markdown 文件。

理由：

- 本地文件读取成本低。
- 开发时修改 Markdown 后可立即生效。
- 部署复杂度低。
- 不需要设计缓存失效机制。

第二阶段可以选择增加进程内索引缓存，基于文件 mtime 判断是否重建。

## 测试策略

第一阶段应新增以下测试。

### Markdown 解析测试

覆盖：

- 旧大写 metadata。
- 新小写 metadata。
- 小写字段优先。
- 缺少标题时 fallback 到 slug。
- Markdown body 渲染为 HTML。
- 日期解析为 `date` 类型。

### Repository 测试

使用临时目录创建 Markdown 文件，覆盖：

- `list_posts()` 扫描 `content/posts/*.md`。
- 文章按日期倒序排列。
- 非 Markdown 文件被忽略。
- `get_post(slug)` 返回对应文章。
- 不存在 slug 返回 `None`。
- `get_topic(slug)` 读取 `content/topics/*.md`。

### 分页测试

覆盖：

- 首页第一页。
- 中间页。
- 超出范围页。
- 空文章列表。
- 每页数量配置。

### 路由测试

使用 Flask test client 覆盖：

- `/` 返回 200。
- `/archives.html` 返回 200。
- `/posts/existing.html` 返回 200。
- `/posts/missing.html` 返回 404。
- `/topic/existing.html` 返回 200。
- `/topic/missing.html` 返回 404。
- `/page/2.html` 分页行为正确。

## 开发命令

建议第一阶段完成后支持：

```bash
# 安装开发依赖
pip install -e ".[dev,server]"

# 启动开发服务器
flask --app blog:create_app --debug run

# 启动生产 WSGI 服务
gunicorn "blog:create_app()" --bind 0.0.0.0:8080

# Windows/简单部署
waitress-serve --listen=0.0.0.0:8080 --call blog:create_app

# 运行全部测试
pytest

# 运行单个测试文件
pytest tests/test_repository.py

# 运行单个测试
pytest tests/test_repository.py::test_list_posts_sorts_by_date_desc

# 格式化 / lint
ruff format .
ruff check .
```

## 分阶段交付

### 第一阶段：核心现代化迁移

交付内容：

1. Python 3.12+ / Flask 3.x 运行时。
2. 删除 Tornado、OSS、Redis、Flask-Script 等旧依赖。
3. 新增本地 Markdown 内容目录。
4. 新增内容仓库、Markdown 渲染和分页模块。
5. 保留旧 URL。
6. 整理模板到现代 Jinja 结构。
7. 新增 `pyproject.toml`。
8. 新增 pytest 测试。
9. 新增 ruff 配置。
10. 更新 README 和 CLAUDE.md。

### 第二阶段：体验和性能优化

可选内容：

- `flask content validate`
- `flask content build-index`
- RSS
- sitemap
- 标签/分类
- TOC
- 代码高亮样式
- 进程内内容索引缓存
- Dockerfile
- CI

### 第三阶段：主题和前端升级

可选内容：

- 保留 Jinja，重写 CSS。
- 或引入 Tailwind CSS。
- 或使用 HTMX/Alpine.js 增加轻量交互。
- 继续保持服务端渲染，不做前后端分离。

## 推荐实施顺序

1. 建立 `pyproject.toml`、测试和 ruff 基础。
2. 实现 Markdown parser，并用测试锁定兼容行为。
3. 实现 repository 和 pagination，并用测试覆盖。
4. 改造 Flask app factory 和 routes。
5. 迁移内容目录和示例文章。
6. 整理模板变量和模板路径。
7. 删除旧 OSS/Redis/Tornado 代码和依赖。
8. 更新 README 和 CLAUDE.md。
9. 跑通测试、lint 和本地启动。

## 验收标准

第一阶段完成时，应满足：

- `flask --app blog:create_app --debug run` 可以启动开发服务器。
- `/`、`/archives.html`、`/posts/<slug>.html`、`/topic/<slug>.html` 可按预期访问。
- 本地 Markdown 文件能通过 Git 管理并被页面读取。
- OSS、Redis、Tornado 不再是运行必需项。
- 旧 URL 结构保持兼容。
- `pytest` 通过。
- `ruff check .` 通过。
- README 和 CLAUDE.md 包含新的运行、测试和架构说明。
