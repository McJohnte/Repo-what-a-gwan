"""End-to-end orchestration: search -> download -> persist."""

from __future__ import annotations

import logging
from dataclasses import dataclass

from ai_image_scraper.config import ScraperConfig
from ai_image_scraper.downloader import Downloader
from ai_image_scraper.http import HttpClient, HttpError
from ai_image_scraper.sources import get_source
from ai_image_scraper.storage import MetadataStore

logger = logging.getLogger(__name__)


@dataclass
class ScrapeResult:
    """Summary statistics for a completed run."""

    found: int = 0
    downloaded: int = 0
    skipped_duplicate: int = 0
    skipped_nsfw: int = 0
    failed: int = 0

    def as_dict(self) -> dict:
        return {
            "found": self.found,
            "downloaded": self.downloaded,
            "skipped_duplicate": self.skipped_duplicate,
            "skipped_nsfw": self.skipped_nsfw,
            "failed": self.failed,
        }


class ScrapePipeline:
    """Wires a source, downloader and metadata store together."""

    def __init__(self, config: ScraperConfig, *, http: HttpClient | None = None) -> None:
        self.config = config
        self.http = http or HttpClient(
            user_agent=config.user_agent,
            rate_limit=config.rate_limit,
            max_retries=config.max_retries,
            timeout=config.timeout,
        )
        self.source = get_source(config.source, self.http)
        self.downloader = Downloader(self.http, config.images_dir)
        self.store = MetadataStore(config.metadata_path)

    def run(self) -> ScrapeResult:
        cfg = self.config
        result = ScrapeResult()
        logger.info("searching %s for %r (limit=%s)", cfg.source, cfg.query, cfg.limit)

        for record in self.source.search(cfg.query, cfg.limit):
            result.found += 1

            if cfg.skip_nsfw and record.nsfw:
                result.skipped_nsfw += 1
                logger.debug("skipping nsfw record %s", record.id)
                continue

            if not cfg.overwrite and record.id and self.store.has_id(record.source, record.id):
                result.skipped_duplicate += 1
                logger.debug("skipping known id %s", record.id)
                continue

            try:
                enriched = self.downloader.download(record)
            except HttpError as exc:
                result.failed += 1
                logger.warning("download failed for %s: %s", record.src_url, exc)
                continue

            if enriched is None:
                result.failed += 1
                continue

            if not cfg.overwrite and self.store.has_hash(enriched.sha256 or ""):
                result.skipped_duplicate += 1
                logger.debug("skipping duplicate content %s", enriched.sha256)
                continue

            self.store.append(enriched)
            result.downloaded += 1
            logger.info("saved %s -> %s", enriched.id, enriched.local_path)

        logger.info("done: %s", result.as_dict())
        return result
