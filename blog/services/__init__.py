"""外部服务调用层。

当前包含 LLM（OpenAI 兼容接口）相关能力，用于在发布文章时
自动生成 slug 与简介；以及 Git 提交能力，用于发布后提交到本地仓库。
"""

from blog.services.git import commit_paths
from blog.services.llm import (
    LLMError,
    PostMetadata,
    extract_metadata,
    fallback_metadata,
    reformat_markdown,
)

__all__ = [
    "LLMError",
    "PostMetadata",
    "commit_paths",
    "extract_metadata",
    "fallback_metadata",
    "reformat_markdown",
]
