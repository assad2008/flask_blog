---
Title:  本博客使用的技术
Summary: 本博客使用的开发技术细节，以及说明
Authors: Django Wong
Date:    2026-06-30
---

# Flask-Blog

一个现代化的 Flask 博客应用，内容全部存放在本地 Markdown 文件中。项目不依赖数据库、OSS 或 Redis，文章和页面可以直接通过 Git 管理，也可以通过内置发布入口写入 `content/posts/`。

## 核心特性

- **本地 Markdown 内容管理**：文章位于 `content/posts/`，独立页面位于 `content/topics/`。
- **Front matter 元数据**：使用 `title`、`summary`、`authors`、`date` 描述文章信息，兼容旧版大写字段。
- **博客常用页面**：内置首页、分页列表、文章归档、单篇文章页和独立页面。
- **阅读体验增强**：支持代码高亮、文章目录、标题锚点、阅读进度、返回顶部和响应式布局。
- **文章发布入口**：配置 `BLOG_POSTART_PASSWORD` 后启用 `/postart`，可通过页面发布文章。
- **LLM 辅助生成**：可配置 OpenAI 兼容接口，为发布文章生成标题、URL slug 和简介。
- **GitHub webhook 拉取**：可配置 GitHub webhook，在收到 push 后执行 `git pull --ff-only` 更新内容。

## 技术栈

| 组件 | 用途 |
|------|------|
| Python 3.12+ | 运行环境 |
| Flask 3.x | Web 应用框架 |
| Jinja2 | 模板引擎 |
| python-frontmatter | Markdown front matter 解析与写入 |
| markdown-it-py | Markdown 渲染 |
| mdit-py-plugins | Markdown 扩展插件 |
| Pygments | 代码语法高亮 |
| python-dotenv | 本地环境变量加载 |
| pytest | 测试框架 |
| ruff | Lint 与格式化 |
| Gunicorn / Waitress | Linux / Windows 生产服务器 |

## 项目结构

```text
flask_blog/
├── app.py                    # 开发服务器入口
├── pyproject.toml            # 项目配置与依赖
├── requirements.txt          # 固定版本运行依赖
├── requirements-dev.txt      # 固定版本开发依赖
├── blog/
│   ├── __init__.py           # 应用工厂 create_app()
│   ├── config.py             # Settings 数据类与环境变量加载
│   ├── content/
│   │   ├── types.py          # Post、Topic、Heading、Page 数据类
│   │   ├── markdown.py       # Markdown 解析、front matter、目录和代码高亮
│   │   ├── repository.py     # ContentRepository 文件系统读取
│   │   ├── writer.py         # 发布页文章写入逻辑
│   │   └── pagination.py     # 纯分页函数
│   ├── routes/
│   │   ├── index.py          # /、/page/<page>.html、/archives.html
│   │   ├── posts.py          # /posts/<slug>.html
│   │   ├── topics.py         # /topic/<slug>.html
│   │   ├── postart.py        # /postart 文章发布入口
│   │   └── webhook.py        # /webhook/github GitHub webhook
│   ├── services/
│   │   ├── llm.py            # OpenAI 兼容 LLM 元数据生成服务
│   │   └── git.py            # 发布后 git add / commit / push 服务
│   └── templates/
│       └── light/            # 当前主题模板
├── content/
│   ├── posts/                # 文章 Markdown 文件
│   └── topics/               # 独立页面 Markdown 文件
└── tests/                    # pytest 测试套件
```

## 快速开始

### 1. 创建并激活虚拟环境

```bash
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# Windows CMD
.venv\Scripts\activate.bat

# Linux / macOS
source .venv/bin/activate
```

### 2. 安装依赖

推荐使用 `pyproject.toml` 安装开发与服务端依赖：

```bash
pip install -e ".[dev,server]"
```

也可以使用固定版本依赖文件：

```bash
# 运行依赖
pip install -r requirements.txt

# 运行依赖 + 测试和格式化工具
pip install -r requirements-dev.txt
```

### 3. 启动开发服务器

```bash
# Flask CLI
flask --app blog:create_app --debug run

# 或直接运行入口文件
python app.py
```

默认访问地址通常为：`http://127.0.0.1:5000/`。

## 配置说明

应用会从项目根目录的 `.env` 文件和系统环境变量读取配置。所有配置都有默认值，生产环境建议显式设置 `BLOG_SECRET_KEY`。

| 环境变量 | 默认值 | 说明 |
|----------|--------|------|
| `BLOG_CONTENT_DIR` | `./content` | 内容目录路径 |
| `BLOG_POSTS_PER_PAGE` | `20` | 首页每页文章数 |
| `BLOG_THEME` | `light` | 主题名称 |
| `BLOG_SECRET_KEY` | `dev-secret-key` | Flask Secret Key，生产环境务必修改 |
| `BLOG_WEBHOOK_SECRET` | 空 | GitHub webhook 签名密钥；为空时禁用 webhook |
| `BLOG_WEBHOOK_REPO_DIR` | 项目根目录 | webhook 执行 `git pull --ff-only` 的仓库目录 |
| `BLOG_WEBHOOK_REF` | 空 | 限定 webhook 监听的 ref，例如 `refs/heads/master` |
| `BLOG_LOG_DIR` | `./logs` | webhook 日志目录 |
| `BLOG_POSTART_PASSWORD` | 空 | `/postart` 发布入口密码；为空时禁用发布入口 |
| `BLOG_POSTART_AUTHOR` | 空 | 发布入口写入文章时使用的默认作者，多个作者用英文逗号分隔 |
| `BLOG_LLM_BASE_URL` | 空 | OpenAI 兼容接口基址，例如 `https://api.openai.com/v1` |
| `BLOG_LLM_API_KEY` | 空 | LLM 服务密钥 |
| `BLOG_LLM_MODEL` | 空 | LLM 模型名，例如 `gpt-4o-mini`、`deepseek-chat` |

示例 `.env`：

```dotenv
BLOG_SECRET_KEY=change-me-in-production
BLOG_POSTS_PER_PAGE=20
BLOG_THEME=light

# 可选：启用文章发布入口
BLOG_POSTART_PASSWORD=change-me
BLOG_POSTART_AUTHOR=Author Name

# 可选：启用发布页 LLM 元数据生成
BLOG_LLM_BASE_URL=https://api.openai.com/v1
BLOG_LLM_API_KEY=sk-...
BLOG_LLM_MODEL=gpt-4o-mini

# 可选：启用 GitHub webhook 自动拉取
BLOG_WEBHOOK_SECRET=change-me
BLOG_WEBHOOK_REF=refs/heads/master
```

## 内容编写

### 文章

在 `content/posts/` 下新增 Markdown 文件即可创建文章。文件名会作为 URL slug，例如：

```text
content/posts/hello-flask.md -> /posts/hello-flask.html
```

文章格式：

````markdown
---
title: 文章标题
summary: 文章摘要
authors:
  - 作者名
date: 2026-06-28
---

## 一级标题

正文内容...

### 二级标题

更多内容...

```python
# 代码块会自动语法高亮
def hello():
    print("world")
```

[外部链接](https://example.com) 会新窗口打开，[内部锚点](#一级标题) 会在当前页面跳转。
````

### 独立页面

在 `content/topics/` 下新增 Markdown 文件即可创建独立页面。文件名会作为页面 slug，例如：

```text
content/topics/about.md -> /topic/about.html
```

独立页面使用与文章相同的 front matter 格式。

### 字段兼容性

推荐使用小写字段：`title`、`summary`、`authors`、`date`。

为兼容旧内容，也支持大写字段：`Title`、`Summary`、`Authors`、`Date`。同一字段同时存在时，小写字段优先。

## 文章发布入口

配置 `BLOG_POSTART_PASSWORD` 后，应用会启用 `/postart` 发布入口，并在页面底部显示入口链接。发布流程如下：

1. 输入发布密码并通过简单数学验证码登录。
2. 填写标题和正文。
3. 点击“生成”生成标题、slug 和简介。
4. 确认后发布，系统会写入 `content/posts/<slug>.md`。
5. 发布后会尝试执行 `git add`、`git commit` 和 `git push`。

注意事项：

- 未配置 `BLOG_POSTART_PASSWORD` 时，`/postart` 返回 404。
- LLM 配置不完整时，生成接口不可用；发布页会按当前配置状态提示。
- 发布后的推送是 best-effort：推送失败不会删除已经写入的本地文章文件。
- 生产环境请使用强密码和安全的 `BLOG_SECRET_KEY`。

## GitHub webhook

配置 `BLOG_WEBHOOK_SECRET` 后，应用会启用 `POST /webhook/github`。该接口用于接收 GitHub push 事件，并在校验 `X-Hub-Signature-256` 通过后执行：

```bash
git pull --ff-only
```

建议同时配置 `BLOG_WEBHOOK_REF`，只允许指定分支触发拉取，例如：

```dotenv
BLOG_WEBHOOK_REF=refs/heads/master
```

webhook 日志默认写入 `logs/webhook.log`，按天滚动并保留 30 天。

## URL 路由

| 路径 | 说明 |
|------|------|
| `/` | 首页文章列表 |
| `/page/<page>.html` | 分页文章列表 |
| `/archives.html` | 文章归档 |
| `/posts/<slug>.html` | 单篇文章 |
| `/topic/<slug>.html` | 独立页面 |
| `/postart` | 文章发布入口，需配置 `BLOG_POSTART_PASSWORD` |
| `/webhook/github` | GitHub webhook，需配置 `BLOG_WEBHOOK_SECRET` |

## 测试与代码质量

```bash
# 运行全部测试
pytest

# 运行单个测试文件
pytest tests/test_repository.py

# 运行单个测试
pytest tests/test_repository.py::test_list_posts_reads_markdown_and_sorts_by_date_desc

# 代码检查
ruff check .

# 代码格式化
ruff format .
```

## 生产部署

### Linux：Gunicorn

```bash
gunicorn "blog:create_app()" --bind 0.0.0.0:8080
```

### Windows：Waitress

```bash
waitress-serve --listen=0.0.0.0:8080 --call blog:create_app
```

生产环境建议：

- 设置强随机 `BLOG_SECRET_KEY`。
- 如启用 `/postart`，设置强密码并确保站点运行在 HTTPS 后方。
- 如启用 webhook，设置 `BLOG_WEBHOOK_SECRET` 并限制 `BLOG_WEBHOOK_REF`。
- 确保运行用户对 `content/` 和 `logs/` 有合适的读写权限。

## 开发者指南

详细架构说明、常用命令和修改注意事项见 [CLAUDE.md](CLAUDE.md)。

主要开发约定：

- 路由处理函数保持简洁，内容逻辑放在 `blog/content/` 或 `blog/services/` 中。
- 内容通过本地文件系统读取，无需数据库和缓存失效逻辑。
- 使用 `pytest` 进行测试，使用 `ruff` 进行 lint 和格式化。
- Markdown 正文中的 `##` 到 `######` 标题会自动进入文章目录。