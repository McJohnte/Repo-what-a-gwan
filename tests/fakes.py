"""Test doubles used across the suite."""

from __future__ import annotations

from typing import Dict, Optional

from ai_image_scraper.http import HttpError


class FakeHttpClient:
    """In-memory stand-in for :class:`ai_image_scraper.http.HttpClient`.

    Routes are matched by substring so tests can register
    ``{"lexica.art": {...}}`` and ``{"image": b"..."}`` without full URLs.
    """

    def __init__(self, json_routes: Optional[Dict[str, dict]] = None,
                 byte_routes: Optional[Dict[str, bytes]] = None) -> None:
        self.json_routes = json_routes or {}
        self.byte_routes = byte_routes or {}
        self.json_calls = []
        self.byte_calls = []

    def get_json(self, url: str, *, params=None, headers=None) -> dict:
        self.json_calls.append((url, params))
        for key, payload in self.json_routes.items():
            if key in url:
                return payload
        raise HttpError(f"no fake json route for {url}")

    def get_bytes(self, url: str, *, headers=None) -> bytes:
        self.byte_calls.append(url)
        for key, payload in self.byte_routes.items():
            if key in url:
                return payload
        raise HttpError(f"no fake byte route for {url}")
