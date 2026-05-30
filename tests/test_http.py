import pytest

from ai_image_scraper.http import HttpClient, HttpError


class _StubResponse:
    def __init__(self, status, payload=b"data"):
        self.status = status
        self.payload = payload


def _make_client(responses, sleeps):
    """Build an HttpClient whose transport replays ``responses``."""
    client = HttpClient(user_agent="test", rate_limit=0, max_retries=2,
                        sleep=lambda s: sleeps.append(s))
    it = iter(responses)

    def fake_do(method, url, params, headers, stream):
        r = next(it)
        return {"status": r.status, "json": lambda: {"ok": True},
                "content": lambda: r.payload}

    client._do_request = fake_do  # type: ignore[assignment]
    return client


def test_retries_then_succeeds():
    sleeps = []
    client = _make_client([_StubResponse(503), _StubResponse(200)], sleeps)
    assert client.get_json("http://x") == {"ok": True}
    assert sleeps == [1]  # one backoff of 2**0


def test_gives_up_after_retries():
    sleeps = []
    client = _make_client([_StubResponse(500)] * 3, sleeps)
    with pytest.raises(HttpError):
        client.get_json("http://x")
    assert sleeps == [1, 2]  # backoffs 2**0, 2**1


def test_non_retryable_4xx_raises_immediately():
    sleeps = []
    client = _make_client([_StubResponse(404)], sleeps)
    with pytest.raises(HttpError):
        client.get_bytes("http://x")
    assert sleeps == []
