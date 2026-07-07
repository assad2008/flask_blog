---
Authors: River King / ChatGPT
Date: 2026-06-29
Summary: 一个Python资源列表，内容包括：解释器、包管理、Web框架、API框架、数据科学、机器学习、爬虫、数据库、测试、代码质量、日志、CLI工具、自动化运维、文档、经典学习项目等
Title: Python资源汇总大全
seo_description: Python资源汇总大全，收录社区知名、长期维护的Python项目，涵盖解释器、包管理、Web框架、API、数据科学、机器学习、爬虫、数据库、测试、代码质量、日志、CLI工具、自动化运维、文档及经典学习项目等。适合后端开发、数据处理、AI应用及工程化实践参考，助你高效选择Python工具。
seo_keywords: Python资源, Python项目, Python工具, Python框架, Python学习
---

# Python资源汇总大全

> 说明：本清单优先选取社区知名度高、长期维护、生态影响力大的 Python 项目。适合后端开发、数据处理、自动化脚本、AI 应用、测试工具和工程化实践参考。

![Python Logo](https://www.python.org/static/community_logos/python-logo.png)

## 目录

- [贡献](#贡献)
- [Python核心项目 Core Projects](#python核心项目-core-projects)
- [包管理与环境管理 Package & Environment](#包管理与环境管理-package--environment)
- [Web框架 Web Frameworks](#web框架-web-frameworks)
- [API与数据校验 API & Validation](#api与数据校验-api--validation)
- [异步与网络 Async & Networking](#异步与网络-async--networking)
- [数据库与ORM Database & ORM](#数据库与orm-database--orm)
- [爬虫与网页解析 Crawling & Parsing](#爬虫与网页解析-crawling--parsing)
- [数据科学 Data Science](#数据科学-data-science)
- [机器学习与AI Machine Learning & AI](#机器学习与ai-machine-learning--ai)
- [任务队列与调度 Task Queue & Scheduler](#任务队列与调度-task-queue--scheduler)
- [日志与调试 Logging & Debugging](#日志与调试-logging--debugging)
- [测试 Testing](#测试-testing)
- [代码质量 Code Quality](#代码质量-code-quality)
- [命令行与终端 CLI & TUI](#命令行与终端-cli--tui)
- [自动化与运维 Automation & DevOps](#自动化与运维-automation--devops)
- [安全 Security](#安全-security)
- [文档 Documentation](#文档-documentation)
- [学习与经典项目 Learning Projects](#学习与经典项目-learning-projects)
- [推荐项目组合](#推荐项目组合)
- [示例代码](#示例代码)

## 贡献

如果要继续扩展这个列表，建议按照下面标准添加项目：

1. GitHub Star 数量较高，社区活跃。
2. 最近仍在维护，有稳定版本发布。
3. 有完整文档、示例和测试。
4. 在实际工程中有较多应用场景。
5. 优先选择官方组织、基金会或成熟团队维护的项目。

## Python核心项目 Core Projects

*Python语言、官方工具和核心生态项目*

* [CPython](https://github.com/python/cpython) - Python 官方解释器源码，也是 Python 语言本身的主要实现。
* [PEPs](https://github.com/python/peps) - Python Enhancement Proposals，记录 Python 语言改进提案。
* [typeshed](https://github.com/python/typeshed) - Python 标准库和第三方库的类型标注仓库。
* [mypy](https://github.com/python/mypy) - Python 静态类型检查工具。
* [PyPI](https://pypi.org/) - Python 官方第三方包索引平台。

## 包管理与环境管理 Package & Environment

*依赖管理、虚拟环境、项目构建和发布工具*

* [pip](https://github.com/pypa/pip) - Python 最常用的包安装工具。
* [setuptools](https://github.com/pypa/setuptools) - Python 项目打包、构建和分发工具。
* [wheel](https://github.com/pypa/wheel) - Python wheel 包格式支持工具。
* [Poetry](https://github.com/python-poetry/poetry) - Python 依赖管理和打包工具，适合现代项目。
* [PDM](https://github.com/pdm-project/pdm) - 支持 PEP 582 的现代 Python 包管理器。
* [uv](https://github.com/astral-sh/uv) - 高性能 Python 包管理和环境管理工具。
* [pipx](https://github.com/pypa/pipx) - 用隔离环境安装和运行 Python 命令行工具。
* [virtualenv](https://github.com/pypa/virtualenv) - Python 虚拟环境创建工具。
* [pyenv](https://github.com/pyenv/pyenv) - 多版本 Python 管理工具。
* [conda](https://github.com/conda/conda) - 跨语言环境和包管理工具，常用于数据科学和 AI 环境。

## Web框架 Web Frameworks

*用于开发网站、后台系统、管理系统和服务端应用*

* [Django](https://github.com/django/django) - 大而全的 Web 框架，内置 ORM、Admin、认证、模板和安全机制。
* [Flask](https://github.com/pallets/flask) - 轻量级 Web 框架，适合中小型项目和灵活组合。
* [FastAPI](https://github.com/fastapi/fastapi) - 高性能 API 框架，基于类型标注和自动 OpenAPI 文档。
* [Tornado](https://github.com/tornadoweb/tornado) - Web 框架和异步网络库，适合长连接和实时服务。
* [Sanic](https://github.com/sanic-org/sanic) - 面向异步场景的高性能 Web 框架。
* [Bottle](https://github.com/bottlepy/bottle) - 单文件轻量级 Web 框架。
* [Pyramid](https://github.com/Pylons/pyramid) - 灵活、可扩展的 Web 框架。
* [Starlette](https://github.com/encode/starlette) - 轻量级 ASGI 框架，也是 FastAPI 的底层基础之一。

## API与数据校验 API & Validation

*接口开发、参数校验、序列化和 OpenAPI 文档生成*

* [Django REST framework](https://github.com/encode/django-rest-framework) - Django 生态中最常用的 REST API 框架。
* [Pydantic](https://github.com/pydantic/pydantic) - 基于类型标注的数据校验和配置管理工具。
* [Marshmallow](https://github.com/marshmallow-code/marshmallow) - 对象序列化、反序列化和数据校验库。
* [apispec](https://github.com/marshmallow-code/apispec) - OpenAPI 规范生成工具。
* [Connexion](https://github.com/spec-first/connexion) - 基于 OpenAPI 规范优先的 API 框架。
* [Strawberry GraphQL](https://github.com/strawberry-graphql/strawberry) - 现代 Python GraphQL 框架。
* [Ariadne](https://github.com/mirumee/ariadne) - Schema-first 风格的 GraphQL 服务端库。

## 异步与网络 Async & Networking

*HTTP 客户端、异步网络、WebSocket 和网络服务开发*

* [Requests](https://github.com/psf/requests) - 经典 HTTP 客户端库，接口简单，使用广泛。
* [HTTPX](https://github.com/encode/httpx) - 支持同步和异步的现代 HTTP 客户端。
* [aiohttp](https://github.com/aio-libs/aiohttp) - 异步 HTTP 客户端和服务端框架。
* [websockets](https://github.com/python-websockets/websockets) - WebSocket 客户端和服务端库。
* [Uvicorn](https://github.com/encode/uvicorn) - ASGI 服务器，常用于 FastAPI 和 Starlette。
* [Gunicorn](https://github.com/benoitc/gunicorn) - Python WSGI HTTP Server，常用于生产部署。
* [Celery](https://github.com/celery/celery) - 分布式任务队列，常与 Redis 或 RabbitMQ 搭配。

## 数据库与ORM Database & ORM

*数据库访问、ORM、迁移工具和缓存客户端*

* [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy) - Python 最成熟的 ORM 和 SQL 工具包之一。
* [Alembic](https://github.com/sqlalchemy/alembic) - SQLAlchemy 官方数据库迁移工具。
* [Peewee](https://github.com/coleifer/peewee) - 简洁轻量的 ORM。
* [Tortoise ORM](https://github.com/tortoise/tortoise-orm) - 异步 ORM，适合 FastAPI 等异步项目。
* [Django ORM](https://github.com/django/django) - Django 内置 ORM，适合管理后台和业务系统。
* [psycopg](https://github.com/psycopg/psycopg) - PostgreSQL Python 驱动。
* [PyMySQL](https://github.com/PyMySQL/PyMySQL) - MySQL 纯 Python 驱动。
* [mysqlclient](https://github.com/PyMySQL/mysqlclient) - MySQL C 扩展驱动，性能较好。
* [redis-py](https://github.com/redis/redis-py) - Redis 官方 Python 客户端。
* [Motor](https://github.com/mongodb/motor) - MongoDB 异步 Python 驱动。

## 爬虫与网页解析 Crawling & Parsing

*网页抓取、HTML解析、浏览器自动化和反爬场景基础工具*

* [Scrapy](https://github.com/scrapy/scrapy) - 成熟的 Python 爬虫框架，支持管道、调度、下载器中间件。
* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) - HTML/XML 解析库，适合简单页面解析。
* [lxml](https://github.com/lxml/lxml) - 高性能 XML/HTML 解析库。
* [Playwright for Python](https://github.com/microsoft/playwright-python) - 浏览器自动化工具，适合动态页面采集和自动化测试。
* [Selenium](https://github.com/SeleniumHQ/selenium) - 老牌浏览器自动化测试工具。
* [PyQuery](https://github.com/gawel/pyquery) - 类似 jQuery 语法的 HTML 解析工具。
* [parsel](https://github.com/scrapy/parsel) - Scrapy 使用的选择器解析库。
* [feedparser](https://github.com/kurtmckee/feedparser) - RSS/Atom Feed 解析库。

## 数据科学 Data Science

*数据处理、科学计算、可视化和交互式分析*

* [NumPy](https://github.com/numpy/numpy) - Python 科学计算基础库，提供多维数组和向量化计算能力。
* [pandas](https://github.com/pandas-dev/pandas) - 数据分析和表格数据处理库。
* [Polars](https://github.com/pola-rs/polars) - 高性能 DataFrame 库，适合大数据量分析。
* [SciPy](https://github.com/scipy/scipy) - 科学计算算法库。
* [Matplotlib](https://github.com/matplotlib/matplotlib) - Python 经典绘图库。
* [Seaborn](https://github.com/mwaskom/seaborn) - 基于 Matplotlib 的统计可视化库。
* [Plotly.py](https://github.com/plotly/plotly.py) - 交互式可视化库。
* [Bokeh](https://github.com/bokeh/bokeh) - 面向浏览器的交互式可视化库。
* [Jupyter Notebook](https://github.com/jupyter/notebook) - 交互式 Notebook 环境。
* [JupyterLab](https://github.com/jupyterlab/jupyterlab) - Jupyter 下一代交互式开发环境。
* [DuckDB Python](https://github.com/duckdb/duckdb) - 嵌入式分析型数据库，适合本地数据分析。

## 机器学习与AI Machine Learning & AI

*机器学习、深度学习、大模型应用、训练和推理工具*

* [scikit-learn](https://github.com/scikit-learn/scikit-learn) - 经典机器学习库，提供分类、回归、聚类、降维等算法。
* [PyTorch](https://github.com/pytorch/pytorch) - 深度学习框架，研究和工程应用都很广泛。
* [TensorFlow](https://github.com/tensorflow/tensorflow) - Google 开源的深度学习框架。
* [Keras](https://github.com/keras-team/keras) - 高层神经网络 API。
* [Transformers](https://github.com/huggingface/transformers) - Hugging Face 的大模型生态核心库。
* [Diffusers](https://github.com/huggingface/diffusers) - 文生图、扩散模型相关工具库。
* [Datasets](https://github.com/huggingface/datasets) - 机器学习数据集加载和处理库。
* [LangChain](https://github.com/langchain-ai/langchain) - LLM 应用开发框架，支持工具调用、链式编排和 RAG。
* [LlamaIndex](https://github.com/run-llama/llama_index) - 面向 LLM 的数据索引和 RAG 框架。
* [vLLM](https://github.com/vllm-project/vllm) - 高吞吐大模型推理引擎。
* [Ray](https://github.com/ray-project/ray) - 分布式计算框架，可用于训练、调度和服务化。
* [MLflow](https://github.com/mlflow/mlflow) - 机器学习实验管理、模型注册和部署工具。
* [ONNX Runtime](https://github.com/microsoft/onnxruntime) - 跨平台模型推理引擎。
* [OpenCV Python](https://github.com/opencv/opencv-python) - OpenCV 的 Python 包，适合图像处理和视觉任务。

## 任务队列与调度 Task Queue & Scheduler

*后台任务、定时任务、异步任务和分布式执行*

* [Celery](https://github.com/celery/celery) - Python 最知名的分布式任务队列之一。
* [RQ](https://github.com/rq/rq) - 基于 Redis 的简单任务队列。
* [Dramatiq](https://github.com/Bogdanp/dramatiq) - 简洁可靠的后台任务处理库。
* [APScheduler](https://github.com/agronholm/apscheduler) - Python 定时任务调度库。
* [Huey](https://github.com/coleifer/huey) - 轻量级任务队列。
* [Prefect](https://github.com/PrefectHQ/prefect) - 数据流和任务编排平台。
* [Apache Airflow](https://github.com/apache/airflow) - 工作流调度和数据管道编排平台。

## 日志与调试 Logging & Debugging

*日志记录、异常追踪、调试和终端输出增强*

* [Loguru](https://github.com/Delgan/loguru) - 简洁易用的 Python 日志库。
* [structlog](https://github.com/hynek/structlog) - 结构化日志库，适合服务端和微服务场景。
* [Rich](https://github.com/Textualize/rich) - 终端富文本输出、表格、进度条和 Traceback 美化。
* [icecream](https://github.com/gruns/icecream) - 更好用的 print 调试工具。
* [Sentry Python SDK](https://github.com/getsentry/sentry-python) - 异常监控和错误上报 SDK。
* [debugpy](https://github.com/microsoft/debugpy) - VSCode Python 调试器底层库。
* [PySnooper](https://github.com/cool-RR/PySnooper) - 轻量级代码执行跟踪工具。

## 测试 Testing

*单元测试、接口测试、属性测试、覆盖率和 Mock 工具*

* [pytest](https://github.com/pytest-dev/pytest) - Python 最常用的第三方测试框架。
* [unittest](https://docs.python.org/3/library/unittest.html) - Python 标准库内置测试框架。
* [coverage.py](https://github.com/nedbat/coveragepy) - Python 代码覆盖率统计工具。
* [Hypothesis](https://github.com/HypothesisWorks/hypothesis) - 属性测试工具，可自动生成测试数据。
* [tox](https://github.com/tox-dev/tox) - 多环境测试自动化工具。
* [nox](https://github.com/wntrblm/nox) - Python 自动化测试会话工具。
* [responses](https://github.com/getsentry/responses) - Mock requests 请求。
* [pytest-mock](https://github.com/pytest-dev/pytest-mock) - pytest 的 mock 插件。
* [factory_boy](https://github.com/FactoryBoy/factory_boy) - 测试数据工厂库。

## 代码质量 Code Quality

*格式化、Lint、类型检查、导入排序和提交前检查*

* [Ruff](https://github.com/astral-sh/ruff) - 高性能 Python Linter 和格式化工具。
* [Black](https://github.com/psf/black) - Python 代码格式化工具。
* [isort](https://github.com/PyCQA/isort) - import 排序工具。
* [Flake8](https://github.com/PyCQA/flake8) - Python Lint 工具。
* [Pylint](https://github.com/pylint-dev/pylint) - 功能丰富的静态代码分析工具。
* [mypy](https://github.com/python/mypy) - 静态类型检查工具。
* [pyright](https://github.com/microsoft/pyright) - Microsoft 开源的 Python 类型检查器。
* [pre-commit](https://github.com/pre-commit/pre-commit) - Git 提交前钩子管理工具。
* [Bandit](https://github.com/PyCQA/bandit) - Python 安全问题扫描工具。

## 命令行与终端 CLI & TUI

*命令行工具开发、终端界面和交互式应用*

* [Click](https://github.com/pallets/click) - 成熟的命令行工具开发库。
* [Typer](https://github.com/fastapi/typer) - 基于类型标注的 CLI 框架，体验接近 FastAPI。
* [argparse](https://docs.python.org/3/library/argparse.html) - Python 标准库命令行参数解析工具。
* [Rich](https://github.com/Textualize/rich) - 终端美化输出库。
* [Textual](https://github.com/Textualize/textual) - Python TUI 应用框架。
* [prompt_toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit) - 交互式命令行和 REPL 构建工具。
* [questionary](https://github.com/tmbo/questionary) - 命令行交互式问答库。

## 自动化与运维 Automation & DevOps

*服务器自动化、部署、远程执行和配置管理*

* [Ansible](https://github.com/ansible/ansible) - 自动化运维和配置管理工具。
* [Fabric](https://github.com/fabric/fabric) - Python 远程命令执行和部署工具。
* [Invoke](https://github.com/pyinvoke/invoke) - Python 任务执行工具，可替代 Makefile 的部分场景。
* [Supervisor](https://github.com/Supervisor/supervisor) - 进程管理工具，常用于守护 Python 服务。
* [Docker SDK for Python](https://github.com/docker/docker-py) - Docker API 的 Python SDK。
* [Paramiko](https://github.com/paramiko/paramiko) - SSHv2 协议 Python 实现。
* [psutil](https://github.com/giampaolo/psutil) - 系统进程和资源监控库。

## 安全 Security

*加密、安全扫描、密码处理、JWT 和认证相关工具*

* [cryptography](https://github.com/pyca/cryptography) - Python 加密算法和安全基础库。
* [PyJWT](https://github.com/jpadilla/pyjwt) - JSON Web Token 编码和解码库。
* [Passlib](https://github.com/passlib2-project/passlib2) - 密码哈希和校验库。
* [python-jose](https://github.com/mpdavis/python-jose) - JOSE/JWT/JWS/JWE 工具库。
* [Bandit](https://github.com/PyCQA/bandit) - Python 安全静态分析工具。
* [Safety](https://github.com/pyupio/safety) - Python 依赖漏洞检查工具。
* [pip-audit](https://github.com/pypa/pip-audit) - PyPA 官方生态下的依赖漏洞扫描工具。

## 文档 Documentation

*项目文档、API文档和静态站点生成工具*

* [Sphinx](https://github.com/sphinx-doc/sphinx) - Python 官方文档体系常用的文档生成工具。
* [MkDocs](https://github.com/mkdocs/mkdocs) - Markdown 风格的静态文档站点生成器。
* [Material for MkDocs](https://github.com/squidfunk/mkdocs-material) - 非常流行的 MkDocs 主题。
* [pdoc](https://github.com/mitmproxy/pdoc) - 自动生成 Python API 文档。
* [Read the Docs](https://github.com/readthedocs/readthedocs.org) - 开源项目文档托管平台。
* [Jupyter Book](https://github.com/jupyter-book/jupyter-book) - 用 Jupyter/Markdown 构建电子书和技术文档。

## 学习与经典项目 Learning Projects

*适合学习源码、算法、工程结构和最佳实践的项目*

* [awesome-python](https://github.com/vinta/awesome-python) - Python 资源大全，覆盖框架、库、工具和学习资料。
* [The Algorithms - Python](https://github.com/TheAlgorithms/Python) - Python 实现的算法集合。
* [Real Python Materials](https://github.com/realpython/materials) - Real Python 教程配套代码。
* [Full Stack Python](https://github.com/mattmakai/fullstackpython.com) - Python Web 开发全栈学习资源。
* [python-patterns](https://github.com/faif/python-patterns) - Python 设计模式示例。
* [500 Lines or Less](https://github.com/aosabook/500lines) - 用较少代码实现经典软件组件的学习项目。
* [project-based-learning](https://github.com/practical-tutorials/project-based-learning) - 基于项目的编程学习资源，包含 Python 项目。
* [system-design-primer](https://github.com/donnemartin/system-design-primer) - 系统设计学习项目，虽然不只面向 Python，但对后端工程师很有价值。

## 推荐项目组合

### 1. Python Web 后端组合

适合开发管理系统、API服务、业务后台：

```text
FastAPI / Django
SQLAlchemy / Django ORM
Alembic
Pydantic
Uvicorn + Gunicorn
Redis
Celery / RQ
pytest
Ruff + Black + mypy
```

### 2. 数据分析组合

适合 CSV、Excel、数据库统计分析和图表：

```text
JupyterLab
NumPy
pandas / Polars
DuckDB
Matplotlib
Plotly
openpyxl
pytest
```

### 3. AI / RAG 应用组合

适合知识库问答、大模型接口、向量检索：

```text
FastAPI
Pydantic
LangChain / LlamaIndex
Transformers
sentence-transformers
Chroma / FAISS / Milvus
Redis
Celery
MLflow
```

### 4. 自动化测试与脚本组合

适合接口测试、定时任务、运维脚本、数据采集：

```text
Requests / HTTPX
Playwright
pytest
APScheduler
Loguru
Rich
Typer
Ruff
```

## 示例代码

### 示例1：FastAPI + Pydantic 写一个接口

```python
from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Python Awesome API", version="1.0.0")


class Project(BaseModel):
    name: str = Field(..., description="项目名称")
    category: Literal["web", "data", "ai", "test", "tool"]
    github: str
    description: str


PROJECTS = [
    Project(
        name="FastAPI",
        category="web",
        github="https://github.com/fastapi/fastapi",
        description="高性能 Python API 框架",
    ),
    Project(
        name="pandas",
        category="data",
        github="https://github.com/pandas-dev/pandas",
        description="数据分析与表格数据处理库",
    ),
]


@app.get("/projects", response_model=list[Project])
def list_projects(category: str | None = None):
    if category is None:
        return PROJECTS
    return [item for item in PROJECTS if item.category == category]
```

运行：

```bash
pip install fastapi uvicorn pydantic
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

访问：

```text
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/projects
```

### 示例2：Requests + BeautifulSoup 抓取页面标题

```python
import requests
from bs4 import BeautifulSoup

url = "https://www.python.org/"
headers = {
    "User-Agent": "Mozilla/5.0 PythonResourceBot/1.0"
}

response = requests.get(url, headers=headers, timeout=10)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")
print("网页标题：", soup.title.get_text(strip=True))
```

安装依赖：

```bash
pip install requests beautifulsoup4
```

### 示例3：Loguru + Rich 输出漂亮日志

```python
from loguru import logger
from rich.console import Console
from rich.table import Table

console = Console()

projects = [
    ("Django", "Web框架", "https://github.com/django/django"),
    ("FastAPI", "API框架", "https://github.com/fastapi/fastapi"),
    ("PyTorch", "深度学习", "https://github.com/pytorch/pytorch"),
]

logger.info("开始输出 Python 知名项目列表")

table = Table(title="Python 知名项目")
table.add_column("项目")
table.add_column("分类")
table.add_column("地址")

for name, category, url in projects:
    table.add_row(name, category, url)

console.print(table)
logger.success("输出完成")
```

安装依赖：

```bash
pip install loguru rich
```

## 推荐阅读顺序

初学者建议按这个顺序了解：

1. Python 官方文档、CPython、PyPI、pip。
2. Requests、BeautifulSoup、pytest、Ruff。
3. Flask 或 FastAPI。
4. SQLAlchemy、Alembic、Redis、Celery。
5. pandas、NumPy、JupyterLab。
6. scikit-learn、PyTorch、Transformers。
7. Docker、Ansible、Supervisor、MLflow。

## 小结

Python 生态非常庞大，实际选型时不要只看 Star 数，还要结合项目场景：

* 做管理系统：优先 Django。
* 做 API 服务：优先 FastAPI。
* 做脚本和自动化：Requests、Typer、Rich、APScheduler 很实用。
* 做数据分析：pandas、Polars、DuckDB、JupyterLab 是常用组合。
* 做 AI 应用：PyTorch、Transformers、LangChain、LlamaIndex、vLLM 值得重点关注。
* 做工程质量：pytest、Ruff、Black、mypy、pre-commit 建议尽早引入。