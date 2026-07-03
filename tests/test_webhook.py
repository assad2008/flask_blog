import dataclasses
import hashlib
import hmac
import subprocess


def _sign(body: bytes, secret: str) -> str:
    """按 GitHub 规则计算 X-Hub-Signature-256 签名头。"""
    return "sha256=" + hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()


def _configure(app, *, secret="test-secret", ref=""):
    """基于现有 app fixture 注入指定的 webhook 配置。"""
    settings = app.config["SETTINGS"]
    app.config["SETTINGS"] = dataclasses.replace(settings, webhook_secret=secret, webhook_ref=ref)
    return app


def _post(client, body=b"", secret="test-secret", event="push", signature=None):
    """以 GitHub webhook 形式发起请求。"""
    if signature is None:
        signature = _sign(body, secret)
    headers = {"X-Hub-Signature-256": signature}
    if event is not None:
        headers["X-GitHub-Event"] = event
    return client.post(
        "/webhook/github", data=body, headers=headers, content_type="application/json"
    )


def test_webhook_disabled_when_no_secret(client):
    # 未配置密钥时 webhook 禁用，返回 404
    response = client.post("/webhook/github")

    assert response.status_code == 404


def test_webhook_forbidden_without_signature(app, client):
    _configure(app)

    # 不携带签名头
    response = client.post("/webhook/github")

    assert response.status_code == 403


def test_webhook_forbidden_with_wrong_signature(app, client):
    _configure(app)

    response = _post(client, body=b"{}", signature="sha256=deadbeef")

    assert response.status_code == 403


def test_webhook_ignores_non_push_event(app, client):
    _configure(app)

    body = b"{}"
    response = _post(client, body=body, event="ping")

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["ok"] is True
    assert payload["skipped"] is True


def test_webhook_runs_git_pull_on_push(app, client, monkeypatch):
    _configure(app)

    calls = {}

    def fake_run(args, **kwargs):
        calls["args"] = args
        calls["kwargs"] = kwargs
        return _CompletedProcess(0, "Already up to date.\n", "")

    monkeypatch.setattr("blog.routes.webhook.subprocess.run", fake_run)

    response = _post(client, body=b"{}")

    assert response.status_code == 200
    body = response.get_json()
    assert body["ok"] is True
    assert "Already up to date" in body["stdout"]
    assert calls["args"][:2] == ["git", "pull"]


def test_webhook_filters_by_ref_when_configured(app, client, monkeypatch):
    _configure(app, ref="refs/heads/main")
    monkeypatch.setattr(
        "blog.routes.webhook.subprocess.run",
        lambda *a, **k: _CompletedProcess(0, "ok", ""),
    )

    # 非目标分支：跳过
    other = _post(client, body=b'{"ref": "refs/heads/feature"}')
    assert other.status_code == 200
    assert other.get_json()["skipped"] is True

    # 目标分支：执行拉取
    target = _post(client, body=b'{"ref": "refs/heads/main"}')
    assert target.status_code == 200
    assert target.get_json()["ok"] is True


def test_webhook_reports_failure_on_nonzero_exit(app, client, monkeypatch):
    _configure(app)
    monkeypatch.setattr(
        "blog.routes.webhook.subprocess.run",
        lambda *a, **k: _CompletedProcess(1, "", "merge conflict"),
    )

    response = _post(client, body=b"{}")

    assert response.status_code == 500
    assert response.get_json()["ok"] is False


def test_webhook_returns_504_on_timeout(app, client, monkeypatch):
    _configure(app)

    def raise_timeout(*args, **kwargs):
        raise subprocess.TimeoutExpired(cmd="git", timeout=120)

    monkeypatch.setattr("blog.routes.webhook.subprocess.run", raise_timeout)

    response = _post(client, body=b"{}")

    assert response.status_code == 504


class _CompletedProcess:
    def __init__(self, returncode, stdout, stderr):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
