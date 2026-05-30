"""Configuration for the scraper pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

DEFAULT_USER_AGENT = (
    "ai-image-scraper/1.0 (+https://github.com/mcjohnte/repo-what-a-gwan)"
)


@dataclass
class ScraperConfig:
    """Tunable knobs for a scraping run.

    Attributes:
        query: Search term sent to the source.
        source: Registered source name (see ``ai_image_scraper.sources``).
        limit: Maximum number of images to download.
        out_dir: Directory where images and metadata are written.
        rate_limit: Minimum seconds to wait between outbound HTTP requests.
        max_retries: Retry attempts for transient HTTP failures.
        timeout: Per-request timeout in seconds.
        user_agent: User-Agent header sent with every request.
        skip_nsfw: Drop records flagged not-safe-for-work by the source.
        overwrite: Re-download images even if already present locally.
    """

    query: str
    source: str = "lexica"
    limit: int = 25
    out_dir: Path = Path("downloads")
    rate_limit: float = 1.0
    max_retries: int = 3
    timeout: float = 30.0
    user_agent: str = DEFAULT_USER_AGENT
    skip_nsfw: bool = True
    overwrite: bool = False

    def __post_init__(self) -> None:
        self.out_dir = Path(self.out_dir)
        if self.limit <= 0:
            raise ValueError("limit must be a positive integer")
        if self.rate_limit < 0:
            raise ValueError("rate_limit must be non-negative")
        if self.max_retries < 0:
            raise ValueError("max_retries must be non-negative")

    @property
    def images_dir(self) -> Path:
        return self.out_dir / "images"

    @property
    def metadata_path(self) -> Path:
        return self.out_dir / "metadata.jsonl"
