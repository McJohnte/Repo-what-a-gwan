"""Persistence for image metadata and a dedup index.

Metadata is appended to a JSONL file (one :class:`ImageRecord` per line). A
companion in-memory set of seen content hashes / source IDs prevents writing
duplicate records across runs.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterator, Set

from ai_image_scraper.models import ImageRecord


class MetadataStore:
    """Append-only JSONL store with dedup awareness."""

    def __init__(self, path: Path) -> None:
        self.path = Path(path)
        self._seen_ids: Set[str] = set()
        self._seen_hashes: Set[str] = set()
        self._load_existing()

    def _load_existing(self) -> None:
        if not self.path.exists():
            return
        for record in self.read_all():
            self._index(record)

    def _index(self, record: ImageRecord) -> None:
        if record.id:
            self._seen_ids.add(f"{record.source}:{record.id}")
        if record.sha256:
            self._seen_hashes.add(record.sha256)

    def has_id(self, source: str, image_id: str) -> bool:
        return f"{source}:{image_id}" in self._seen_ids

    def has_hash(self, sha256: str) -> bool:
        return sha256 in self._seen_hashes

    def append(self, record: ImageRecord) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record.to_dict(), ensure_ascii=False) + "\n")
        self._index(record)

    def read_all(self) -> Iterator[ImageRecord]:
        if not self.path.exists():
            return
        with self.path.open("r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    yield ImageRecord.from_dict(json.loads(line))

    def __len__(self) -> int:
        return len(self._seen_ids)
