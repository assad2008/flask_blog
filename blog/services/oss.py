"""阿里云 OSS 图片上传服务，用于网页导入时转存远程图片。"""

from __future__ import annotations

import base64
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
from email.utils import format_datetime
from pathlib import Path
from typing import Any

_IMAGE_LINK_RE = r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)"
_MAX_IMAGE_BYTES = 20_000_000
_TIMEOUT_SECONDS = 30


class OssImageError(Exception):
    """OSS 图片转存失败。"""


@dataclass(frozen=True)
class OssImageConfig:
    access_key_id: str
    access_key_secret: str
    endpoint: str
    bucket: str

    @property
    def is_ready(self) -> bool:
        """四项 OSS 配置是否齐全。"""
        return bool(
            self.access_key_id.strip()
            and self.access_key_secret.strip()
            and self.endpoint.strip()
            and self.bucket.strip()
        )

    @property
    def public_endpoint(self) -> str:
        """去掉协议前缀后的公网 endpoint，用于生成公开访问地址。"""
        endpoint = self.endpoint.strip().rstrip("/")
        parsed = urllib.parse.urlparse(endpoint)
        return parsed.netloc or parsed.path

    def public_url(self, object_name: str) -> str:
        """生成 bucket 公网 endpoint 形式的图片 URL。"""
        return f"https://{self.bucket}.{self.public_endpoint}/{object_name}"


def rewrite_markdown_images_to_oss(
    markdown: str,
    *,
    config: OssImageConfig,
    temp_dir: Path | None = None,
    today: date | None = None,
    fetch_image: Callable[[str, Path], None] | None = None,
    upload_file: Callable[[Path, str, OssImageConfig], str] | None = None,
    on_progress: Callable[[dict[str, Any]], None] | None = None,
) -> str:
    """把 Markdown 中的远程图片临时下载到本地，上传 OSS 后替换为 OSS 地址。"""
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
                    oss_url = _transfer_one_image(
                        image_url,
                        Path(tmp),
                        current_day,
                        config,
                        fetch,
                        upload,
                    )
            else:
                oss_url = _transfer_one_image(
                    image_url,
                    target_dir,
                    current_day,
                    config,
                    fetch,
                    upload,
                )
            replacements[image_url] = oss_url
            _log(f"图片上传完成：{image_url} -> {oss_url}")
            return f"![{alt}]({oss_url})"
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
    config: OssImageConfig,
    fetch_image: Callable[[str, Path], None],
    upload_file: Callable[[Path, str, OssImageConfig], str],
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
                raise OssImageError("目标地址返回的不是图片")
            data = resp.read(_MAX_IMAGE_BYTES + 1)
    except urllib.error.HTTPError as exc:
        raise OssImageError(f"图片下载失败：HTTP {exc.code}") from exc
    except urllib.error.URLError as exc:
        raise OssImageError(f"图片下载失败：{exc.reason}") from exc

    if len(data) > _MAX_IMAGE_BYTES:
        raise OssImageError(f"图片过大（{len(data)} > 限制 {_MAX_IMAGE_BYTES} 字节）")
    target_path.write_bytes(data)


def upload_image_file(path: Path, object_name: str, config: OssImageConfig) -> str:
    """使用 OSS PutObject API 上传本地图片文件，返回公网访问 URL。"""
    data = path.read_bytes()
    content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    date_header = format_datetime(datetime.now(UTC), usegmt=True)
    resource = f"/{config.bucket}/{object_name}"
    string_to_sign = f"PUT\n\n{content_type}\n{date_header}\n{resource}"
    signature = base64.b64encode(
        hmac.new(
            config.access_key_secret.encode("utf-8"),
            string_to_sign.encode("utf-8"),
            hashlib.sha1,
        ).digest()
    ).decode("ascii")
    url = config.public_url(object_name)
    req = urllib.request.Request(
        url,
        data=data,
        method="PUT",
        headers={
            "Content-Type": content_type,
            "Date": date_header,
            "Authorization": f"OSS {config.access_key_id}:{signature}",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=_TIMEOUT_SECONDS):
            return url
    except urllib.error.HTTPError as exc:
        raise OssImageError(f"OSS 上传失败：HTTP {exc.code}") from exc
    except urllib.error.URLError as exc:
        raise OssImageError(f"OSS 上传失败：{exc.reason}") from exc


def _is_remote_image_url(url: str) -> bool:
    parsed = urllib.parse.urlparse(url)
    return parsed.scheme in {"http", "https"}


def _extension_from_url(url: str) -> str:
    path = urllib.parse.urlparse(url).path
    suffix = Path(path).suffix.lower()
    if suffix in {".jpg", ".jpeg", ".png", ".gif", ".webp", ".avif", ".svg", ".bmp"}:
        return suffix
    return ".jpg"
