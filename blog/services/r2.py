"""Cloudflare R2 图片上传服务，用于网页导入时转存远程图片。

R2 提供 S3 兼容接口，使用 AWS Signature V4 签名；本模块与 ``oss.py``
并列、结构镜像，保持互相独立、互不影响。
"""

from __future__ import annotations

import hashlib
import hmac
import mimetypes
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

# Markdown 图片语法：![alt](url "title")
_IMAGE_LINK_RE = r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)"
_MAX_IMAGE_BYTES = 20_000_000
_TIMEOUT_SECONDS = 30
# R2 / S3 Sig V4 固定参数：服务名 s3，区域 auto
_R2_REGION = "auto"
_R2_SERVICE = "s3"


class R2ImageError(Exception):
    """R2 图片转存失败。"""


@dataclass(frozen=True)
class R2ImageConfig:
    """R2 存储配置。

    ``account_id`` 用于拼接 S3 端点 ``<account_id>.r2.cloudflarestorage.com``；
    ``public_base_url`` 是配置好的公开访问基址（自定义域名或 r2.dev 子域），
    上传成功后用它生成可访问的图片 URL。
    """

    account_id: str
    access_key_id: str
    secret_access_key: str
    bucket: str
    public_base_url: str

    @property
    def is_ready(self) -> bool:
        """五项 R2 配置是否齐全。"""
        return bool(
            self.account_id.strip()
            and self.access_key_id.strip()
            and self.secret_access_key.strip()
            and self.bucket.strip()
            and self.public_base_url.strip()
        )

    @property
    def endpoint_host(self) -> str:
        """R2 S3 兼容端点主机名。"""
        return f"{self.account_id.strip()}.r2.cloudflarestorage.com"

    def public_url(self, object_name: str) -> str:
        """基于 public_base_url 生成图片的公开访问地址。"""
        base = self.public_base_url.strip().rstrip("/")
        return f"{base}/{object_name}"


def rewrite_markdown_images_to_r2(
    markdown: str,
    *,
    config: R2ImageConfig,
    temp_dir: Path | None = None,
    today: date | None = None,
    fetch_image: Callable[[str, Path], None] | None = None,
    upload_file: Callable[[Path, str, R2ImageConfig], str] | None = None,
    on_progress: Callable[[dict[str, Any]], None] | None = None,
) -> str:
    """把 Markdown 中的远程图片临时下载到本地，上传 R2 后替换为公开地址。"""
    if not markdown or not config.is_ready:
        return markdown

    fetch = fetch_image or download_image
    upload = upload_file or upload_image_file
    current_day = today or date.today()
    replacements: dict[str, str] = {}

    def _log(message: str) -> None:
        if on_progress:
            on_progress({"type": "log", "message": message})

    def _replace(match) -> str:
        alt = match.group(1)
        image_url = match.group(2)
        if not _is_remote_image_url(image_url):
            return match.group(0)
        if image_url in replacements:
            return f"![{alt}]({replacements[image_url]})"
        try:
            target_dir = temp_dir
            if target_dir is None:
                with tempfile.TemporaryDirectory(prefix="flask-blog-images-") as tmp:
                    r2_url = _transfer_one_image(
                        image_url,
                        Path(tmp),
                        current_day,
                        config,
                        fetch,
                        upload,
                    )
            else:
                r2_url = _transfer_one_image(
                    image_url,
                    target_dir,
                    current_day,
                    config,
                    fetch,
                    upload,
                )
            replacements[image_url] = r2_url
            _log(f"图片上传完成：{image_url} -> {r2_url}")
            return f"![{alt}]({r2_url})"
        except Exception as exc:
            # 单张图片失败不影响整篇文章导入，保留原图地址方便后续人工处理。
            _log(f"图片处理失败，已保留原地址：{image_url}（{exc}）")
            return match.group(0)

    import re

    return re.sub(_IMAGE_LINK_RE, _replace, markdown)


def _transfer_one_image(
    image_url: str,
    temp_dir: Path,
    current_day: date,
    config: R2ImageConfig,
    fetch_image: Callable[[str, Path], None],
    upload_file: Callable[[Path, str, R2ImageConfig], str],
) -> str:
    temp_dir.mkdir(parents=True, exist_ok=True)
    ext = _extension_from_url(image_url)
    digest = hashlib.sha256(image_url.encode("utf-8")).hexdigest()[:24]
    local_path = temp_dir / f"{digest}{ext}"
    fetch_image(image_url, local_path)
    object_name = f"posts/images/{current_day:%Y/%m/%d}/{digest}{ext}"
    return upload_file(local_path, object_name, config)


def download_image(url: str, target_path: Path) -> None:
    """下载远程图片到临时文件，并限制大小和响应类型。"""
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; flask-blog-web-import/1.0)",
            "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=_TIMEOUT_SECONDS) as resp:
            content_type = resp.headers.get("Content-Type", "")
            if content_type and not content_type.lower().startswith("image/"):
                raise R2ImageError("目标地址返回的不是图片")
            data = resp.read(_MAX_IMAGE_BYTES + 1)
    except urllib.error.HTTPError as exc:
        raise R2ImageError(f"图片下载失败：HTTP {exc.code}") from exc
    except urllib.error.URLError as exc:
        raise R2ImageError(f"图片下载失败：{exc.reason}") from exc

    if len(data) > _MAX_IMAGE_BYTES:
        raise R2ImageError(f"图片过大（{len(data)} > 限制 {_MAX_IMAGE_BYTES} 字节）")
    target_path.write_bytes(data)


def upload_image_file(path: Path, object_name: str, config: R2ImageConfig) -> str:
    """使用 R2 (S3 兼容) PutObject API 上传本地图片文件，返回公开访问 URL。

    上传走 S3 端点 ``https://<account_id>.r2.cloudflarestorage.com/<bucket>/<object>``，
    返回的 URL 则使用配置好的 ``public_base_url``（自定义域名或 r2.dev）。
    """
    data = path.read_bytes()
    content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"

    now = datetime.now(UTC)
    # Sig V4 要求 ISO 基本格式时间戳
    amz_date = now.strftime("%Y%m%dT%H%M%SZ")
    date_stamp = now.strftime("%Y%m%d")

    host = config.endpoint_host
    # 对象路径需 URI 编码，但保留 / 作为路径分隔符
    canonical_uri = urllib.parse.quote(f"/{config.bucket}/{object_name}", safe="/")

    # S3 Sig V4 要求把请求体 SHA256 作为 x-amz-content-sha256 头参与签名
    payload_hash = hashlib.sha256(data).hexdigest()

    # 规范头：头名小写字母序，每行 "name:value\n"
    canonical_headers = f"host:{host}\nx-amz-content-sha256:{payload_hash}\nx-amz-date:{amz_date}\n"
    signed_headers = "host;x-amz-content-sha256;x-amz-date"

    # 第 1 步：构造规范请求
    canonical_request = (
        f"PUT\n{canonical_uri}\n\n{canonical_headers}\n{signed_headers}\n{payload_hash}"
    )

    # 第 2 步：构造待签字符串
    credential_scope = f"{date_stamp}/{_R2_REGION}/{_R2_SERVICE}/aws4_request"
    string_to_sign = (
        "AWS4-HMAC-SHA256\n"
        f"{amz_date}\n"
        f"{credential_scope}\n"
        f"{hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()}"
    )

    # 第 3 步：逐层派生签名密钥
    k_date = _hmac_sha256(f"AWS4{config.secret_access_key}".encode(), date_stamp)
    k_region = _hmac_sha256(k_date, _R2_REGION)
    k_service = _hmac_sha256(k_region, _R2_SERVICE)
    k_signing = _hmac_sha256(k_service, "aws4_request")

    # 第 4 步：计算签名并组装 Authorization 头
    signature = _hmac_sha256(k_signing, string_to_sign).hex()
    authorization = (
        "AWS4-HMAC-SHA256 "
        f"Credential={config.access_key_id}/{credential_scope}, "
        f"SignedHeaders={signed_headers}, "
        f"Signature={signature}"
    )

    # 上传走 S3 端点；返回值用 public_base_url 生成对外可访问地址
    upload_url = f"https://{host}{canonical_uri}"
    req = urllib.request.Request(
        upload_url,
        data=data,
        method="PUT",
        headers={
            "Content-Type": content_type,
            "x-amz-content-sha256": payload_hash,
            "x-amz-date": amz_date,
            "Authorization": authorization,
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=_TIMEOUT_SECONDS):
            return config.public_url(object_name)
    except urllib.error.HTTPError as exc:
        raise R2ImageError(f"R2 上传失败：HTTP {exc.code}") from exc
    except urllib.error.URLError as exc:
        raise R2ImageError(f"R2 上传失败：{exc.reason}") from exc


def _hmac_sha256(key: bytes, msg: str) -> bytes:
    """HMAC-SHA256 摘要，返回字节。Sig V4 派生签名密钥使用。"""
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()


def _is_remote_image_url(url: str) -> bool:
    parsed = urllib.parse.urlparse(url)
    return parsed.scheme in {"http", "https"}


def _extension_from_url(url: str) -> str:
    path = urllib.parse.urlparse(url).path
    suffix = Path(path).suffix.lower()
    if suffix in {".jpg", ".jpeg", ".png", ".gif", ".webp", ".avif", ".svg", ".bmp"}:
        return suffix
    return ".jpg"
