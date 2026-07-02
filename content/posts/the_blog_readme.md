---
Title:  本博客使用的技术
Summary: 本博客使用的开发技术细节，以及说明
Authors: Django Wong
Date:    2026-06-30
---

# Flask-Blog

一个基于 Flask 和本地 Markdown 文件的现代化博客系统。无需数据库、OSS 或 Redis —— 内容以 Markdown 文件形式保存在 `content/` 目录中，通过 Git 进行版本管理。

## 技术栈

| 组件 | 版本 |
|------|------|
| Python | 3.12+ |
| Flask | 3.x |
| Jinja2 | 模板引擎 |
| python-frontmatter | Front matter 解析 |
| markdown-it-py | Markdown 渲染 |
| mdit-py-plugins | 锚点链接、脚注等插件 |
| Pygments | 代码语法高亮 |
| Waitress | Windows 生产服务器 |
| Gunicorn | Linux 生产服务器 |
| pytest | 测试框架 |
| ruff | Lint & 格式化 |

## 项目结构

```text
flask_blog/
├── app.py                    # 开发服务器入口
├── pyproject.toml            # 项目配置与依赖
├── blog/
│   ├── __init__.py           # 应用工厂 create_app()
│   ├── config.py             # Settings 数据类 (环境变量加载)
│   ├── content/
│   │   ├── __init__.py
│   │   ├── types.py          # Post、Topic、Heading 数据类
│   │   ├── markdown.py       # Markdown 解析、front matter、Pygments 高亮、锚点
│   │   ├── repository.py     # ContentRepository 文件系统读取
│   │   └── pagination.py     # 纯分页函数
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── index.py          # /、/page/、/archives
│   │   ├── posts.py          # /posts/<slug>
│   │   └── topics.py         # /topic/<slug>
│   └── templates/
│       └── light/            # 默认主题模板
├── content/
│   ├── posts/                # 文章 Markdown 文件
│   └── topics/               # 独立页面 Markdown 文件
├── tests/                    # pytest 测试套件
├── .env.example              # 环境变量示例
└── .env                      # 环境变量（已忽略）
```

## 快速开始

### 环境准备

Python 3.12+ 且虚拟环境在 `.venv`：

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
source .venv/bin/activate # Linux/macOS
```

### 安装

```bash
pip install -e ".[dev,server]"
```

### 启动开发服务器

```bash
# 方式一：Flask CLI
flask --app blog:create_app --debug run

# 方式二：直接运行
python app.py
```

## 生产部署

**Linux (推荐)：**

```bash
gunicorn "blog:create_app()" --bind 0.0.0.0:8080
```

**Windows：**

```bash
waitress-serve --listen=0.0.0.0:8080 --call blog:create_app
```

## 配置

通过 `.env` 文件或环境变量进行配置，所有变量都有默认值：

| 环境变量 | 默认值 | 说明 |
|----------|--------|------|
| `BLOG_CONTENT_DIR` | `./content` | 内容目录路径 |
| `BLOG_POSTS_PER_PAGE` | `20` | 每页文章数 |
| `BLOG_THEME` | `light` | 主题名称 |
| `BLOG_SECRET_KEY` | `dev-secret-key` | Flask Secret Key（生产环境务必修改） |

复制 `.env.example` 为 `.env` 即可开始：

```bash
cp .env.example .env
```

## 内容格式

文章和页面均为带 front matter 的 Markdown 文件：

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

### 二级标题

更多内容...

\`\`\`python
# 代码块会自动语法高亮
def hello():
    print("world")
\`\`\`

[外部链接](https://example.com) 会新窗口打开，[内部锚点](#一级标题) 同页跳转。
```

### 功能特性

- **代码高亮**：代码块根据语言自动高亮（Pygments），支持亮色/暗色主题
- **文章目录**：右侧自动生成目录（TOC），支持滚动高亮和阅读进度条
- **锚点跳转**：标题自动生成锚点 ID，支持中文标题
- **返回顶部**：右下角返回顶部按钮，滚动后自动出现
- **外部链接**：外部链接自动在新窗口打开，内部锚点同页跳转
- **响应式**：移动端目录可收起，桌面端常驻显示

### 字段兼容性

`Title`、`Summary`、`Authors`、`Date`（大写）也支持，小写字段优先。

## URL 路由

| 路径 | 说明 |
|------|------|
| `/` | 首页（文章列表） |
| `/page/<page>.html` | 分页文章列表 |
| `/archives.html` | 文章归档 |
| `/posts/<slug>.html` | 单篇文章 |
| `/topic/<slug>.html` | 独立页面 |

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

## 开发者指南

详细的架构说明、修改注意事项和 CLI 参考见 [CLAUDE.md](CLAUDE.html)。

主要内容编写建议：
- 路由处理函数保持简洁，内容逻辑放在 `blog/content/` 中
- 内容通过本地文件系统读取，无需缓存失效逻辑
- 使用 `pytest` 进行测试，`ruff` 进行 lint 和格式化
- 标题使用 `##` 开始的二级标题，会自动出现在文章目录中
