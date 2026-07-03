from __future__ import annotations

import hashlib
import hmac
import logging
import subprocess
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from flask import Blueprint, abort, current_app, jsonify, request

from blog.config import Settings

webhook_bp = Blueprint("webhook", __name__)

# webhook 专用 logger；handler 在应用工厂创建时按天滚动配置
logger = logging.getLogger("blog.webhook")


def init_webhook_logger(log_dir: Path) -> None:
    """配置按天滚动的 webhook 文件日志。

    日志文件为 ``webhook.log``，每天午夜滚动，历史文件保留 30 天。
    多次调用安全（已配置 handler 时跳过）。
    """
    log_dir.mkdir(parents=True, exist_ok=True)
    if logger.handlers:
        return
    handler = TimedRotatingFileHandler(
        log_dir / "webhook.log",
        when="midnight",
        backupCount=30,
        encoding="utf-8",
    )
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    # 不冒泡到 root logger，避免重复输出到控制台
    logger.propagate = False


def _settings() -> Settings:
    return current_app.config["SETTINGS"]


def _secret() -> str:
    """从应用配置读取 GitHub webhook 密钥；为空表示禁用 webhook。"""
    return _settings().webhook_secret


def _repo_dir() -> str:
    """返回执行 git pull 的仓库目录。"""
    return str(_settings().webhook_repo_dir)


def _expected_ref() -> str:
    """返回需监听的 ref（如 refs/heads/main）；为空表示不限定分支。"""
    return _settings().webhook_ref


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
    # GitHub 每次投递的唯一 ID，便于在日志中关联同一请求的各步骤
    delivery = request.headers.get("X-GitHub-Delivery", "-")
    event = request.headers.get("X-GitHub-Event", "")
    tag = f"[delivery={delivery} ip={request.remote_addr} event={event!r}]"

    logger.info("%s received webhook request", tag)

    # 未配置密钥时禁用 webhook，避免暴露未授权入口
    secret = _secret()
    if not secret:
        logger.warning("%s webhook disabled: BLOG_WEBHOOK_SECRET not configured", tag)
        abort(404)

    # GitHub 使用请求体的 HMAC-SHA256 签名进行身份校验
    body = request.get_data()
    signature_header = request.headers.get("X-Hub-Signature-256")
    if not _verify_signature(body, secret, signature_header):
        logger.warning(
            "%s signature verification failed (header=%s)",
            tag,
            "missing" if not signature_header else "invalid",
        )
        abort(403)
    logger.info("%s signature verified", tag)

    # 仅处理 push 事件，其它事件（如 ping）直接忽略
    if event != "push":
        logger.info("%s ignored non-push event", tag)
        return jsonify({"ok": True, "skipped": True, "reason": f"event {event!r} ignored"})

    # 配置了 webhook_ref 时，只对指定分支的 push 触发拉取
    expected_ref = _expected_ref()
    if expected_ref:
        payload = request.get_json(silent=True) or {}
        ref = payload.get("ref", "")
        if ref != expected_ref:
            logger.info("%s skipped: ref=%r does not match expected=%r", tag, ref, expected_ref)
            return jsonify({"ok": True, "skipped": True, "reason": f"ref {ref!r} ignored"})
        logger.info("%s ref=%r matched expected, start git pull", tag, ref)
    else:
        logger.info("%s no ref filter, start git pull", tag)

    logger.info("%s running 'git pull --ff-only' in %s", tag, _repo_dir())
    ok, stdout, stderr, status = _run_git_pull()
    if ok:
        logger.info("%s git pull succeeded: %s", tag, stdout.strip().replace("\n", " | "))
    else:
        logger.error(
            "%s git pull failed (status=%s): stdout=%r stderr=%r",
            tag,
            status,
            stdout.strip(),
            stderr.strip(),
        )
    return jsonify({"ok": ok, "stdout": stdout, "stderr": stderr}), status
