from __future__ import annotations

import hashlib
import hmac
import subprocess

from flask import Blueprint, abort, current_app, jsonify, request

webhook_bp = Blueprint("webhook", __name__)


def _secret() -> str:
    """从应用配置读取 GitHub webhook 密钥；为空表示禁用 webhook。"""
    return current_app.config["SETTINGS"].webhook_secret


def _repo_dir() -> str:
    """返回执行 git pull 的仓库目录。"""
    return str(current_app.config["SETTINGS"].webhook_repo_dir)


def _expected_ref() -> str:
    """返回需监听的 ref（如 refs/heads/main）；为空表示不限定分支。"""
    return current_app.config["SETTINGS"].webhook_ref


def _verify_signature(body: bytes, secret: str, signature_header: str | None) -> bool:
    """按 GitHub 规则用 HMAC-SHA256 校验 X-Hub-Signature-256 签名。

    签名格式为 ``sha256=<hex>``，使用恒定时间比较防止时序攻击。
    """
    if not signature_header:
        return False
    expected = "sha256=" + hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature_header)


def _run_git_pull() -> tuple[bool, str, str, int | None]:
    """执行 ``git pull --ff-only``，返回 (ok, stdout, stderr, http_status)。"""
    try:
        result = subprocess.run(
            ["git", "pull", "--ff-only"],
            cwd=_repo_dir(),
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return False, "", "git pull timed out", 504
    except FileNotFoundError:
        return False, "", "git executable not found", 500

    ok = result.returncode == 0
    return ok, result.stdout, result.stderr, 200 if ok else 500


@webhook_bp.post("/webhook/github")
def github_webhook():
    # 未配置密钥时禁用 webhook，避免暴露未授权入口
    secret = _secret()
    if not secret:
        abort(404)

    # GitHub 使用请求体的 HMAC-SHA256 签名进行身份校验
    body = request.get_data()
    if not _verify_signature(body, secret, request.headers.get("X-Hub-Signature-256")):
        abort(403)

    # 仅处理 push 事件，其它事件（如 ping）直接忽略
    event = request.headers.get("X-GitHub-Event", "")
    if event != "push":
        return jsonify({"ok": True, "skipped": True, "reason": f"event {event!r} ignored"})

    # 配置了 webhook_ref 时，只对指定分支的 push 触发拉取
    expected_ref = _expected_ref()
    if expected_ref:
        payload = request.get_json(silent=True) or {}
        ref = payload.get("ref", "")
        if ref != expected_ref:
            return jsonify({"ok": True, "skipped": True, "reason": f"ref {ref!r} ignored"})

    ok, stdout, stderr, status = _run_git_pull()
    return jsonify({"ok": ok, "stdout": stdout, "stderr": stderr}), status
