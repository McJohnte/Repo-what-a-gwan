"""Download image bytes to disk with content-hash naming and dedup."""

from __future__ import annotations

import hashlib
import logging
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

from ai_image_scraper.http import HttpClient
from ai_image_scraper.models import ImageRecord

logger = logging.getLogger(__name__)

# Map common content types / extensions to a canonical suffix.
_CONTENT_TYPE_EXT = {
    "image/jpeg": ".jpg",
    "image/jpg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
    "image/gif": ".gif",
}


class Downloader:
    """Fetches image bytes and writes them, named by content hash."""

    def __init__(self, http: HttpClient, images_dir: Path) -> None:
        self.http = http
        self.images_dir = Path(images_dir)

    def _guess_extension(self, url: str) -> str:
        suffix = Path(urlparse(url).path).suffix.lower()
        if suffix in {".jpg", ".jpeg", ".png", ".webp", ".gif"}:
            return ".jpg" if suffix == ".jpeg" else suffix
        return ".jpg"

    def download(self, record: ImageRecord) -> Optional[ImageRecord]:
        """Download ``record.src_url``; return the enriched record.

        Returns ``None`` when the URL is missing or the fetch yields no bytes.
        The record is mutated in place with ``sha256``, ``bytes`` and
        ``local_path`` on success.
        """
        if not record.src_url:
            logger.warning("record %s has no src_url; skipping", record.id)
            return None

        data = self.http.get_bytes(record.src_url)
        if not data:
            logger.warning("empty response for %s", record.src_url)
            return None

        digest = hashlib.sha256(data).hexdigest()
        ext = self._guess_extension(record.src_url)
        self.images_dir.mkdir(parents=True, exist_ok=True)
        dest = self.images_dir / f"{digest}{ext}"

        if not dest.exists():
            dest.write_bytes(data)

        record.sha256 = digest
        record.bytes = len(data)
        record.local_path = str(dest)
        return record
