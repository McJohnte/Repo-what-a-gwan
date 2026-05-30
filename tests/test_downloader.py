import hashlib

from tests.fakes import FakeHttpClient
from ai_image_scraper.downloader import Downloader
from ai_image_scraper.models import ImageRecord

PNG = b"\x89PNG\r\n\x1a\n" + b"fake-bytes"


def test_download_writes_file_and_enriches(tmp_path):
    http = FakeHttpClient(byte_routes={"img": PNG})
    dl = Downloader(http, tmp_path / "images")
    rec = ImageRecord(id="1", src_url="https://x/img.png", source="lexica")

    out = dl.download(rec)

    assert out is not None
    assert out.sha256 == hashlib.sha256(PNG).hexdigest()
    assert out.bytes == len(PNG)
    assert out.local_path.endswith(".png")
    assert (tmp_path / "images" / f"{out.sha256}.png").read_bytes() == PNG


def test_download_without_url_returns_none(tmp_path):
    http = FakeHttpClient()
    dl = Downloader(http, tmp_path)
    assert dl.download(ImageRecord(id="1", src_url="", source="s")) is None


def test_extension_defaults_to_jpg(tmp_path):
    http = FakeHttpClient(byte_routes={"img": PNG})
    dl = Downloader(http, tmp_path)
    rec = ImageRecord(id="1", src_url="https://x/img?token=1", source="s")
    out = dl.download(rec)
    assert out.local_path.endswith(".jpg")
