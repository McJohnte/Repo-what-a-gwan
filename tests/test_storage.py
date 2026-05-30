from ai_image_scraper.models import ImageRecord
from ai_image_scraper.storage import MetadataStore


def _rec(**kw):
    base = dict(id="1", src_url="u", source="lexica", sha256="hash1")
    base.update(kw)
    return ImageRecord(**base)


def test_append_and_read_roundtrip(tmp_path):
    path = tmp_path / "metadata.jsonl"
    store = MetadataStore(path)
    store.append(_rec(prompt="hi"))

    records = list(MetadataStore(path).read_all())
    assert len(records) == 1
    assert records[0].prompt == "hi"


def test_dedup_index_persists_across_instances(tmp_path):
    path = tmp_path / "metadata.jsonl"
    MetadataStore(path).append(_rec(id="42", sha256="deadbeef"))

    reloaded = MetadataStore(path)
    assert reloaded.has_id("lexica", "42")
    assert reloaded.has_hash("deadbeef")
    assert not reloaded.has_id("lexica", "999")
    assert len(reloaded) == 1
