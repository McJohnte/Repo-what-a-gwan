"""Data models shared across the scraper."""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, Optional


@dataclass
class ImageRecord:
    """A single AI-generated image discovered by a source.

    Sources are responsible for populating at least ``id`` and ``src_url``.
    Everything else is best-effort metadata that downstream consumers may use
    for filtering, naming, or auditing.
    """

    id: str
    src_url: str
    source: str
    prompt: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    model: Optional[str] = None
    seed: Optional[str] = None
    nsfw: Optional[bool] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    # Populated by the downloader once the bytes are on disk.
    local_path: Optional[str] = None
    sha256: Optional[str] = None
    bytes: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ImageRecord":
        known = {f for f in cls.__dataclass_fields__}  # type: ignore[attr-defined]
        kwargs = {k: v for k, v in data.items() if k in known}
        return cls(**kwargs)
