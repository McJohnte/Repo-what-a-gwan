"""Lexica.art source.

Lexica hosts a large, searchable gallery of Stable-Diffusion–generated images
and exposes a simple public search endpoint::

    GET https://lexica.art/api/v1/search?q=<query>

Each result carries the generation prompt and dimensions, which map cleanly
onto :class:`ImageRecord`.
"""

from __future__ import annotations

import itertools
from typing import Iterator

from ai_image_scraper.models import ImageRecord
from ai_image_scraper.sources.base import ImageSource


class LexicaSource(ImageSource):
    name = "lexica"

    API_URL = "https://lexica.art/api/v1/search"

    def search(self, query: str, limit: int) -> Iterator[ImageRecord]:
        headers = {"Accept": "application/json"}
        payload = self.http.get_json(
            self.API_URL, params={"q": query}, headers=headers
        )
        images = payload.get("images", []) if isinstance(payload, dict) else []
        for item in itertools.islice(images, limit):
            yield self._to_record(item)

    def _to_record(self, item: dict) -> ImageRecord:
        return ImageRecord(
            id=str(item.get("id", "")),
            src_url=item.get("src") or item.get("srcSmall") or "",
            source=self.name,
            prompt=item.get("prompt"),
            width=item.get("width"),
            height=item.get("height"),
            model=item.get("model"),
            seed=str(item["seed"]) if item.get("seed") is not None else None,
            nsfw=item.get("nsfw"),
            extra={
                "gallery": item.get("gallery"),
                "grid": item.get("grid"),
                "promptid": item.get("promptid"),
            },
        )
