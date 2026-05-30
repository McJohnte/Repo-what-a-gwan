"""Command-line interface for the AI image scraper."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import List, Optional

from ai_image_scraper.config import DEFAULT_USER_AGENT, ScraperConfig
from ai_image_scraper.pipeline import ScrapePipeline
from ai_image_scraper.sources import available_sources


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ai-image-scraper",
        description="Scrape AI-generated images from a public source.",
    )
    parser.add_argument("query", help="search term, e.g. 'cyberpunk city'")
    parser.add_argument(
        "-s", "--source", default="lexica", choices=available_sources(),
        help="image source to scrape (default: lexica)",
    )
    parser.add_argument(
        "-n", "--limit", type=int, default=25,
        help="maximum number of images to download (default: 25)",
    )
    parser.add_argument(
        "-o", "--out-dir", type=Path, default=Path("downloads"),
        help="output directory (default: ./downloads)",
    )
    parser.add_argument(
        "--rate-limit", type=float, default=1.0,
        help="minimum seconds between HTTP requests (default: 1.0)",
    )
    parser.add_argument(
        "--max-retries", type=int, default=3,
        help="retry attempts for transient failures (default: 3)",
    )
    parser.add_argument(
        "--timeout", type=float, default=30.0,
        help="per-request timeout in seconds (default: 30)",
    )
    parser.add_argument(
        "--user-agent", default=DEFAULT_USER_AGENT,
        help="User-Agent header to send",
    )
    parser.add_argument(
        "--include-nsfw", action="store_true",
        help="do not skip records flagged NSFW by the source",
    )
    parser.add_argument(
        "--overwrite", action="store_true",
        help="re-download images even if already seen",
    )
    parser.add_argument(
        "-v", "--verbose", action="count", default=0,
        help="-v for INFO, -vv for DEBUG logging",
    )
    return parser


def _configure_logging(verbosity: int) -> None:
    level = logging.WARNING
    if verbosity == 1:
        level = logging.INFO
    elif verbosity >= 2:
        level = logging.DEBUG
    logging.basicConfig(level=level, format="%(levelname)s %(name)s: %(message)s")


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    _configure_logging(args.verbose)

    config = ScraperConfig(
        query=args.query,
        source=args.source,
        limit=args.limit,
        out_dir=args.out_dir,
        rate_limit=args.rate_limit,
        max_retries=args.max_retries,
        timeout=args.timeout,
        user_agent=args.user_agent,
        skip_nsfw=not args.include_nsfw,
        overwrite=args.overwrite,
    )

    try:
        result = ScrapePipeline(config).run()
    except KeyboardInterrupt:  # pragma: no cover
        print("\ninterrupted", file=sys.stderr)
        return 130
    except Exception as exc:  # noqa: BLE001 - top-level guard
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result.as_dict(), indent=2))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
