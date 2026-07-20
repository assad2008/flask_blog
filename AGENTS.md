# AGENTS.md

本文件为 AI 编码助手（如 OpenCode、Claude Code 等）在本仓库中工作提供指导。

## 项目概览

Flask-Blog — 一个现代化的 Flask 博客应用，使用本地 Markdown 文件存储内容。无需数据库、OSS 或 Redis。

- `content/posts/` 下的 `.md` 文件为文章
- `content/topics/` 下的 `.md` 文件为独立页面

技术栈：Python 3.12+ / Flask 3.x / Jinja2 / python-frontmatter / markdown-it-py / pytest / ruff

## 常用命令

当前运行环境为 Windows，Python 环境位于 `.venv`。所有命令在仓库根目录执行，需先激活虚拟环境：

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1

# Windows CMD
.venv\Scripts\activate.bat
```

```bash
# 安装依赖
pip install -e ".[dev,server]"

# 开发服务器
flask --app blog:create_app --debug run
python app.py

# 生产服务器
gunicorn "blog:create_app()" --bind 0.0.0.0:8080          # Linux
waitress-serve --listen=0.0.0.0:8080 --call blog:create_app  # Windows

# 测试
pytest
pytest tests/test_repository.py
pytest tests/test_repository.py::test_list_posts_reads_markdown_and_sorts_by_date_desc

# 代码检查与格式化
ruff check .
ruff format .
```

## 架构

```
flask_blog/
├── app.py                    # 开发服务器入口
├── pyproject.toml            # 项目配置与依赖
├── blog/
│   ├── __init__.py           # create_app() 应用工厂，注册蓝图和错误处理器
│   ├── config.py             # Settings 数据类，通过 Settings.from_env() 从环境变量加载
│   ├── content/
│   │   ├── types.py          # Post、Topic、Heading、Page 数据类
│   │   ├── markdown.py       # Markdown 解析、front matter 提取、目录生成、代码高亮
│   │   ├── repository.py     # ContentRepository 从本地文件系统读取内容
│   │   ├── writer.py         # 发布页文章写入逻辑
│   │   └── pagination.py     # 纯分页函数
│   ├── routes/
│   │   ├── index.py          # /、/page/<int:page>.html、/archives.html
│   │   ├── posts.py          # /posts/<slug>.html
│   │   ├── topics.py         # /topic/<slug>.html
│   │   ├── postart.py        # /postart 文章发布入口（需密码）
│   │   └── webhook.py        # /webhook/github GitHub webhook
│   ├── services/
│   │   ├── llm.py            # OpenAI 兼容 LLM 元数据生成服务与 LLM 请求日志
│   │   ├── web_import.py     # 网页正文抓取与大模型提取
│   │   ├── oss.py            # 阿里云 OSS 图片转存服务（网页导入时转存远程图片）
│   │   ├── r2.py             # Cloudflare R2 图片转存服务（AWS Sig V4，与 OSS 互斥）
│   │   └── git.py            # 发布后 git add/commit/push 服务
│   └── templates/
│       └── light/            # 当前主题模板，Jinja2 继承，base.html 为共享壳
│           └── _toc.html     # 文章目录 partial（post/topic 页面共享）
├── content/
│   ├── posts/                # 文章 Markdown 文件
│   └── topics/               # 独立页面 Markdown 文件
└── tests/                    # pytest 测试套件
```

### URL 路由

| 路径 | 说明 |
|------|------|
| `/` | 首页文章列表 |
| `/page/<int:page>.html` | 分页文章列表 |
| `/archives.html` | 文章归档 |
| `/posts/<slug>.html` | 单篇文章 |
| `/topic/<slug>.html` | 独立页面 |
| `/postart` | 文章发布入口（需配置 `BLOG_POSTART_PASSWORD`） |
| `/webhook/github` | GitHub webhook（需配置 `BLOG_WEBHOOK_SECRET`） |

## 内容格式

文章和主题均为带 front matter 的 Markdown 文件：

```markdown
---
title: 文章标题
summary: 文章摘要
authors:
  - 作者名
date: 2026-06-28
---

## 一级标题

正文内容...

```python
# 代码块会自动语法高亮
def hello():
    print("world")
```
```

- 文件名即为 URL slug（如 `hello-flask.md` → `/posts/hello-flask.html`）
- 推荐使用小写字段 `title`、`summary`、`authors`、`date`
- 兼容旧版大写字段 `Title`、`Summary`、`Authors`、`Date`；同时存在时小写优先
- 文章列表依赖 `date`、`title` 和 `summary` 字段

## 环境配置

应用从项目根目录 `.env` 文件和系统环境变量读取配置，所有配置均有默认值。

| 环境变量 | 默认值 | 说明 |
|----------|--------|------|
| `BLOG_CONTENT_DIR` | `./content` | 内容目录 |
| `BLOG_POSTS_PER_PAGE` | `20` | 首页每页文章数 |
| `BLOG_THEME` | `light` | 主题名称 |
| `BLOG_SECRET_KEY` | `dev-secret-key` | Flask Secret Key |
| `BLOG_WEBHOOK_SECRET` | 空 | webhook 签名密钥；为空则禁用 webhook |
| `BLOG_WEBHOOK_REPO_DIR` | 项目根目录 | webhook git 仓库目录 |
| `BLOG_WEBHOOK_REF` | 空 | 限定监听 ref（如 `refs/heads/master`） |
| `BLOG_LOG_DIR` | `./logs` | 日志目录（webhook、LLM 请求） |
| `BLOG_POSTART_PASSWORD` | 空 | 发布入口密码；为空则禁用 `/postart` |
| `BLOG_POSTART_AUTHOR` | 空 | 默认作者，多个用英文逗号分隔 |
| `BLOG_LLM_BASE_URL` | 空 | OpenAI 兼容接口基址 |
| `BLOG_LLM_API_KEY` | 空 | LLM 服务密钥 |
| `BLOG_LLM_MODEL` | 空 | LLM 模型名 |
| `BLOG_IMAGE_STORAGE` | `oss` | 网页导入图片转存后端：`oss` 或 `r2`，二者互斥 |
| `BLOG_OSS_ACCESS_KEY_ID` | 空 | 阿里云 OSS AccessKey ID；四项齐全时启用 OSS 转存 |
| `BLOG_OSS_ACCESS_KEY_SECRET` | 空 | 阿里云 OSS AccessKey Secret |
| `BLOG_OSS_ENDPOINT` | 空 | OSS 公网 endpoint（如 `oss-cn-hangzhou.aliyuncs.com`） |
| `BLOG_OSS_BUCKET` | 空 | OSS 存储桶名 |
| `BLOG_R2_ACCOUNT_ID` | 空 | Cloudflare R2 账户 ID；五项齐全时启用 R2 转存 |
| `BLOG_R2_ACCESS_KEY_ID` | 空 | R2 Access Key ID |
| `BLOG_R2_SECRET_ACCESS_KEY` | 空 | R2 Secret Access Key |
| `BLOG_R2_BUCKET` | 空 | R2 存储桶名 |
| `BLOG_R2_PUBLIC_BASE_URL` | 空 | R2 公开访问基址（自定义域名或 `*.r2.dev`） |

## 修改注意事项

- **路由函数保持简洁**：内容逻辑放在 `blog/content/` 中，服务逻辑放在 `blog/services/` 中
- **无需缓存**：内容通过本地文件系统读取，不需要缓存失效逻辑
- **依赖管理**：使用 `pyproject.toml`，通过 `pip install -e ".[dev,server]"` 安装
- **测试**：使用 `pytest`；修改代码后必须确保现有测试通过
- **代码质量**：使用 `ruff check .` 和 `ruff format .` 确保代码符合规范
- **注释**：生成代码时务必添加必要的注释
- **遵循现有模式**：编写新代码前先查看同类文件，模仿现有代码风格、命名和结构
- **安全**：绝不引入会暴露或记录敏感密钥的代码

## 其他要求

- 不要执行任何git命令
- 生成的代码必须要有必要的注释