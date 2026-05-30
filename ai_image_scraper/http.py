"""A thin HTTP client wrapper with polite rate limiting and retries.

Kept dependency-light: it uses :mod:`requests` if available and degrades to
``urllib`` so the package can run in minimal environments. Network access is
abstracted behind :class:`HttpClient` so tests can inject a fake.
"""

from __future__ import annotations

import logging
import time
from typing import Dict, Optional

logger = logging.getLogger(__name__)

try:  # pragma: no cover - exercised implicitly depending on env
    import requests

    _HAS_REQUESTS = True
except ImportError:  # pragma: no cover
    requests = None  # type: ignore[assignment]
    _HAS_REQUESTS = False


class HttpError(RuntimeError):
    """Raised when a request ultimately fails after exhausting retries."""


class HttpClient:
    """Minimal HTTP client with throttling and exponential-backoff retries."""

    # Status codes worth retrying — transient server/throttling errors.
    RETRY_STATUS = {429, 500, 502, 503, 504}

    def __init__(
        self,
        *,
        user_agent: str,
        rate_limit: float = 1.0,
        max_retries: int = 3,
        timeout: float = 30.0,
        sleep=time.sleep,
    ) -> None:
        self.user_agent = user_agent
        self.rate_limit = rate_limit
        self.max_retries = max_retries
        self.timeout = timeout
        self._sleep = sleep
        self._last_request_at = 0.0
        self._session = requests.Session() if _HAS_REQUESTS else None

    def _throttle(self) -> None:
        if self.rate_limit <= 0:
            return
        elapsed = time.monotonic() - self._last_request_at
        wait = self.rate_limit - elapsed
        if wait > 0:
            self._sleep(wait)

    def _default_headers(self, extra: Optional[Dict[str, str]]) -> Dict[str, str]:
        headers = {"User-Agent": self.user_agent}
        if extra:
            headers.update(extra)
        return headers

    def get_json(self, url: str, *, params: Optional[Dict] = None,
                 headers: Optional[Dict[str, str]] = None) -> dict:
        resp = self._request("GET", url, params=params, headers=headers)
        return resp["json"]()

    def get_bytes(self, url: str, *,
                  headers: Optional[Dict[str, str]] = None) -> bytes:
        resp = self._request("GET", url, headers=headers, stream=True)
        return resp["content"]()

    def _request(self, method: str, url: str, *, params=None, headers=None,
                 stream: bool = False) -> dict:
        last_exc: Optional[Exception] = None
        for attempt in range(self.max_retries + 1):
            self._throttle()
            try:
                resp = self._do_request(method, url, params, headers, stream)
            except Exception as exc:  # noqa: BLE001 - normalise transport errors
                last_exc = exc
                logger.warning("request error (%s/%s) for %s: %s",
                               attempt + 1, self.max_retries + 1, url, exc)
            else:
                status = resp["status"]
                if status in self.RETRY_STATUS:
                    last_exc = HttpError(f"HTTP {status} for {url}")
                    logger.warning("retryable status %s (%s/%s) for %s",
                                   status, attempt + 1, self.max_retries + 1, url)
                elif status >= 400:
                    raise HttpError(f"HTTP {status} for {url}")
                else:
                    return resp
            finally:
                self._last_request_at = time.monotonic()

            if attempt < self.max_retries:
                backoff = 2 ** attempt
                logger.info("backing off %ss before retrying %s", backoff, url)
                self._sleep(backoff)

        raise HttpError(f"request failed for {url}: {last_exc}")

    def _do_request(self, method, url, params, headers, stream) -> dict:
        """Perform one request, returning a transport-agnostic dict."""
        merged = self._default_headers(headers)
        if _HAS_REQUESTS:
            r = self._session.request(  # type: ignore[union-attr]
                method, url, params=params, headers=merged,
                timeout=self.timeout, stream=stream,
            )
            return {
                "status": r.status_code,
                "json": r.json,
                "content": lambda: r.content,
            }
        # urllib fallback (no streaming, no params encoding niceties).
        import json as _json
        import urllib.parse
        import urllib.request

        full = url
        if params:
            full = f"{url}?{urllib.parse.urlencode(params)}"
        req = urllib.request.Request(full, headers=merged, method=method)
        with urllib.request.urlopen(req, timeout=self.timeout) as fh:  # noqa: S310
            body = fh.read()
            status = fh.getcode()
        return {
            "status": status,
            "json": lambda: _json.loads(body.decode("utf-8")),
            "content": lambda: body,
        }
