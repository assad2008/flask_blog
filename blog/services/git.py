"""Git 服务：将发布的新文章提交并推送到远程仓库。

执行 ``git add`` + ``git commit`` + ``git push``。推送为 best-effort：
失败（无远程、无凭证、非快进等）不影响已完成的本地提交，仅在成功页提示。
设置 ``GIT_TERMINAL_PROMPT=0`` 避免凭证交互导致进程挂起。
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path


def commit_paths(repo_dir: Path, paths: list[Path], message: str) -> tuple[bool, bool, str]:
    """将指定文件 ``git add``、``commit`` 并 ``push``。

    返回 ``(committed, pushed, detail)``：

    - ``committed`` 为 ``True`` 表示本地提交成功（含“无可提交内容”）；
    - ``pushed`` 为 ``True`` 表示推送成功；推送失败时 ``committed`` 仍可能为 ``True``；
    - ``detail`` 为相关输出/错误文本，供调用方提示。
    """
    env = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}

    def run(args: list[str]) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", *args],
            cwd=str(repo_dir),
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=env,
            timeout=60,
            check=False,
        )

    # 解析为绝对路径，确保 git add 定位正确
    resolved = [str(p.resolve()) for p in paths]
    add = run(["add", "--", *resolved])
    if add.returncode != 0:
        return False, False, (add.stderr or add.stdout).strip()

    commit = run(["commit", "-m", message])
    # returncode 0 = 已提交；1 = 无可提交内容（仍视为提交成功）
    if commit.returncode not in (0, 1):
        return False, False, (commit.stderr or commit.stdout).strip()

    # 推送（best-effort）：失败不影响已完成的本地提交
    push = run(["push"])
    if push.returncode == 0:
        return True, True, (push.stdout or "").strip()
    return True, False, (push.stderr or push.stdout or "push failed").strip()
