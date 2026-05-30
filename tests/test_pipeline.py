from tests.fakes import FakeHttpClient
from ai_image_scraper.config import ScraperConfig
from ai_image_scraper.pipeline import ScrapePipeline

PAYLOAD = {
    "images": [
        {"id": "a", "src": "https://img/a.jpg", "prompt": "p1", "nsfw": False},
        {"id": "b", "src": "https://img/b.jpg", "prompt": "p2", "nsfw": True},
        {"id": "c", "src": "https://img/c.jpg", "prompt": "p3", "nsfw": False},
    ]
}


def _http():
    return FakeHttpClient(
        json_routes={"lexica.art": PAYLOAD},
        byte_routes={"a.jpg": b"AAAA", "b.jpg": b"BBBB", "c.jpg": b"CCCC"},
    )


def test_pipeline_downloads_and_skips_nsfw(tmp_path):
    cfg = ScraperConfig(query="x", out_dir=tmp_path, limit=10)
    result = ScrapePipeline(cfg, http=_http()).run()

    assert result.found == 3
    assert result.downloaded == 2
    assert result.skipped_nsfw == 1
    assert (tmp_path / "metadata.jsonl").exists()
    assert len(list((tmp_path / "images").iterdir())) == 2


def test_pipeline_dedups_on_second_run(tmp_path):
    cfg = ScraperConfig(query="x", out_dir=tmp_path, limit=10)
    ScrapePipeline(cfg, http=_http()).run()
    second = ScrapePipeline(cfg, http=_http()).run()

    assert second.downloaded == 0
    assert second.skipped_duplicate == 2


def test_pipeline_include_nsfw(tmp_path):
    cfg = ScraperConfig(query="x", out_dir=tmp_path, limit=10, skip_nsfw=False)
    result = ScrapePipeline(cfg, http=_http()).run()
    assert result.downloaded == 3
    assert result.skipped_nsfw == 0


def test_pipeline_dedups_identical_content(tmp_path):
    # All three URLs return identical bytes -> only one unique file kept.
    http = FakeHttpClient(
        json_routes={"lexica.art": PAYLOAD},
        byte_routes={".jpg": b"SAME"},
    )
    cfg = ScraperConfig(query="x", out_dir=tmp_path, limit=10, skip_nsfw=False)
    result = ScrapePipeline(cfg, http=http).run()
    assert result.downloaded == 1
    assert result.skipped_duplicate == 2
