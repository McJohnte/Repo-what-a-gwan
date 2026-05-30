from tests.fakes import FakeHttpClient
from ai_image_scraper.sources.lexica import LexicaSource

SAMPLE = {
    "images": [
        {
            "id": "abc123",
            "src": "https://image.lexica.art/full/abc123.jpg",
            "prompt": "a serene mountain lake at dawn",
            "width": 512,
            "height": 512,
            "model": "stable-diffusion",
            "seed": 42,
            "nsfw": False,
            "gallery": "g1",
        },
        {
            "id": "def456",
            "src": "https://image.lexica.art/full/def456.jpg",
            "prompt": "neon city",
            "width": 768,
            "height": 512,
            "nsfw": True,
        },
    ]
}


def test_search_maps_fields():
    http = FakeHttpClient(json_routes={"lexica.art": SAMPLE})
    src = LexicaSource(http)
    records = list(src.search("mountains", limit=10))

    assert len(records) == 2
    first = records[0]
    assert first.id == "abc123"
    assert first.source == "lexica"
    assert first.prompt == "a serene mountain lake at dawn"
    assert first.width == 512
    assert first.seed == "42"
    assert first.nsfw is False
    assert first.extra["gallery"] == "g1"


def test_search_respects_limit():
    http = FakeHttpClient(json_routes={"lexica.art": SAMPLE})
    src = LexicaSource(http)
    assert len(list(src.search("x", limit=1))) == 1


def test_search_handles_empty_payload():
    http = FakeHttpClient(json_routes={"lexica.art": {}})
    src = LexicaSource(http)
    assert list(src.search("x", limit=5)) == []
