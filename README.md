# AI Image Scraper

An end-to-end, source-pluggable scraper for **AI-generated images**. It searches
a public image source for a text query, downloads the matching images, and
records their generation metadata (prompt, model, seed, dimensions) to disk.

The default source is [Lexica.art](https://lexica.art), a public gallery of
Stable-Diffusion–generated images.

## Features

- **End-to-end pipeline**: search → download → persist, in one command.
- **Pluggable sources** via a small registry (`ai_image_scraper/sources/`).
- **Polite networking**: configurable rate limiting, per-request timeouts, and
  exponential-backoff retries on transient (429/5xx) errors.
- **Deduplication** by source ID *and* by SHA-256 content hash, so re-runs don't
  re-download or store duplicates.
- **Metadata** appended as JSONL (one record per line) for easy downstream use.
- **NSFW filtering** on by default (`--include-nsfw` to disable).
- **No hard dependencies**: uses `requests` if installed, otherwise falls back
  to the standard library.

## Install

```bash
pip install -r requirements.txt   # optional; only pulls in `requests`
```

## Usage

```bash
# Download up to 25 images for a prompt into ./downloads
python -m ai_image_scraper "cyberpunk city at night"

# More control
python -m ai_image_scraper "watercolor fox" \
    --source lexica \
    --limit 50 \
    --out-dir ./out \
    --rate-limit 1.5 \
    -v
```

Output layout:

```
downloads/
├── images/
│   ├── <sha256>.jpg
│   └── ...
└── metadata.jsonl
```

Each line of `metadata.jsonl` is one image record:

```json
{"id": "abc123", "src_url": "https://image.lexica.art/...", "source": "lexica",
 "prompt": "a serene mountain lake at dawn", "width": 512, "height": 512,
 "model": "stable-diffusion", "seed": "42", "nsfw": false,
 "local_path": "downloads/images/<sha256>.jpg", "sha256": "<sha256>", "bytes": 12345}
```

## Programmatic use

```python
from ai_image_scraper import ScraperConfig, ScrapePipeline

config = ScraperConfig(query="origami dragon", limit=10, out_dir="out")
result = ScrapePipeline(config).run()
print(result.as_dict())   # {'found': 10, 'downloaded': 10, ...}
```

## Adding a new source

1. Subclass `ImageSource` in `ai_image_scraper/sources/` and implement
   `search(query, limit) -> Iterator[ImageRecord]`.
2. Register it in `ai_image_scraper/sources/__init__.py`'s `_SOURCES` map.

It then becomes available via `--source <name>` automatically.

## Architecture

| Module | Responsibility |
| --- | --- |
| `sources/` | Resolve a query into `ImageRecord`s (URLs + metadata). |
| `http.py` | Throttled HTTP client with retries; abstracts the transport. |
| `downloader.py` | Fetch bytes, hash, and write content-addressed files. |
| `storage.py` | Append-only JSONL metadata store with a dedup index. |
| `pipeline.py` | Orchestrate search → download → persist. |
| `cli.py` | Argument parsing and the `python -m ai_image_scraper` entry point. |

## Tests

```bash
python -m pytest
```

The suite (15 tests) runs fully offline using a fake HTTP client, covering the
source mapping, downloader, dedup store, retry logic, and the full pipeline.

## Responsible use

This tool fetches publicly available content. Respect each source's Terms of
Service and `robots.txt`, keep the rate limit conservative, and only use scraped
images in ways permitted by their licenses.
