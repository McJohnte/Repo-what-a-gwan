"""Source abstraction: anything that can yield AI-generated images."""

from __future__ import annotations

import abc
from typing import Iterator

from ai_image_scraper.http import HttpClient
from ai_image_scraper.models import ImageRecord


class ImageSource(abc.ABC):
    """Base class for image sources.

    A source knows how to turn a text query into a stream of
    :class:`ImageRecord` objects. It must not download image bytes — that is
    the downloader's job — it only resolves URLs and metadata.
    """

    #: Short, unique name used on the CLI and in the registry.
    name: str = ""

    def __init__(self, http: HttpClient) -> None:
        self.http = http

    @abc.abstractmethod
    def search(self, query: str, limit: int) -> Iterator[ImageRecord]:
        """Yield up to ``limit`` records matching ``query``."""
        raise NotImplementedError
