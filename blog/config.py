from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class Settings:
    content_dir: Path
    posts_per_page: int
    theme: str
    secret_key: str

    @classmethod
    def from_env(cls) -> Settings:
        content_dir = Path(os.environ.get("BLOG_CONTENT_DIR", BASE_DIR / "content"))
        posts_per_page = int(os.environ.get("BLOG_POSTS_PER_PAGE", "20"))
        theme = os.environ.get("BLOG_THEME", "light")
        secret_key = os.environ.get("BLOG_SECRET_KEY", "dev-secret-key")
        return cls(
            content_dir=content_dir,
            posts_per_page=posts_per_page,
            theme=theme,
            secret_key=secret_key,
        )
