"""Source registry.

New sources register themselves here so the CLI and pipeline can resolve them
by name. To add a source, implement :class:`ImageSource` and add it to
``_SOURCES`` below.
"""

from __future__ import annotations

from typing import Dict, List, Type

from ai_image_scraper.http import HttpClient
from ai_image_scraper.sources.base import ImageSource
from ai_image_scraper.sources.lexica import LexicaSource

_SOURCES: Dict[str, Type[ImageSource]] = {
    LexicaSource.name: LexicaSource,
}


def available_sources() -> List[str]:
    """Return the sorted list of registered source names."""
    return sorted(_SOURCES)


def get_source(name: str, http: HttpClient) -> ImageSource:
    """Instantiate a registered source by name."""
    try:
        cls = _SOURCES[name]
    except KeyError:
        raise ValueError(
            f"unknown source {name!r}; available: {', '.join(available_sources())}"
        ) from None
    return cls(http)


__all__ = ["available_sources", "get_source", "ImageSource", "LexicaSource"]
