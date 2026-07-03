from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


@dataclass(frozen=True)
class Settings:
    content_dir: Path
    posts_per_page: int
    theme: str
    secret_key: str
    # 项目根目录，用于定位 git 仓库等资源
    base_dir: Path
    # GitHub webhook 密钥，用于校验请求签名；为空时禁用 webhook 接口
    webhook_secret: str
    # 执行 git pull 的仓库目录，默认为项目根目录
    webhook_repo_dir: Path
    # 仅监听该 ref 的 push 事件（如 refs/heads/main）；为空表示所有 push 都触发
    webhook_ref: str
    # webhook 日志目录，默认为项目根目录下的 logs/
    log_dir: Path
    # /postart 发布页面访问密码；为空时禁用该入口（返回 404）
    postart_password: str
    # 新文章默认作者，留空则不写 authors 字段
    postart_author: str
    # OpenAI 兼容接口基址，如 https://api.openai.com/v1；留空则跳过 LLM 用兜底
    llm_base_url: str
    # LLM 服务密钥
    llm_api_key: str
    # LLM 模型名，如 gpt-4o-mini / deepseek-chat
    llm_model: str

    @classmethod
    def from_env(cls) -> Settings:
        base_dir = BASE_DIR
        content_dir = Path(os.environ.get("BLOG_CONTENT_DIR", base_dir / "content"))
        posts_per_page = int(os.environ.get("BLOG_POSTS_PER_PAGE", "20"))
        theme = os.environ.get("BLOG_THEME", "light")
        secret_key = os.environ.get("BLOG_SECRET_KEY", "dev-secret-key")
        webhook_secret = os.environ.get("BLOG_WEBHOOK_SECRET", "")
        webhook_repo_dir = Path(os.environ.get("BLOG_WEBHOOK_REPO_DIR", base_dir))
        webhook_ref = os.environ.get("BLOG_WEBHOOK_REF", "")
        log_dir = Path(os.environ.get("BLOG_LOG_DIR", base_dir / "logs"))
        postart_password = os.environ.get("BLOG_POSTART_PASSWORD", "")
        postart_author = os.environ.get("BLOG_POSTART_AUTHOR", "")
        llm_base_url = os.environ.get("BLOG_LLM_BASE_URL", "")
        llm_api_key = os.environ.get("BLOG_LLM_API_KEY", "")
        llm_model = os.environ.get("BLOG_LLM_MODEL", "")
        return cls(
            content_dir=content_dir,
            posts_per_page=posts_per_page,
            theme=theme,
            secret_key=secret_key,
            base_dir=base_dir,
            webhook_secret=webhook_secret,
            webhook_repo_dir=webhook_repo_dir,
            webhook_ref=webhook_ref,
            log_dir=log_dir,
            postart_password=postart_password,
            postart_author=postart_author,
            llm_base_url=llm_base_url,
            llm_api_key=llm_api_key,
            llm_model=llm_model,
        )
