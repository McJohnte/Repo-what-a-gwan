import requests

from config import GOOGLE_GEOCODE_URL, MAPS_API_KEY, OSM_NOMINATIM_URL
from models import Coordinates


def geocode(location: str, provider: str = "google") -> Coordinates:
    """Convert a location string into geographic coordinates."""
    if provider == "google":
        return _geocode_google(location)
    return _geocode_osm(location)


def _geocode_google(location: str) -> Coordinates:
    resp = requests.get(
        GOOGLE_GEOCODE_URL,
        params={"address": location, "key": MAPS_API_KEY},
        timeout=10,
    )
    resp.raise_for_status()
    data = resp.json()
    if data["status"] != "OK" or not data.get("results"):
        raise ValueError(f"Google geocoding failed for '{location}': {data['status']}")
    geo = data["results"][0]["geometry"]["location"]
    return Coordinates(lat=geo["lat"], lng=geo["lng"])


def _geocode_osm(location: str) -> Coordinates:
    resp = requests.get(
        OSM_NOMINATIM_URL,
        params={"q": location, "format": "json", "limit": 1},
        headers={"User-Agent": "CafeFinderAgent/1.0"},
        timeout=10,
    )
    resp.raise_for_status()
    results = resp.json()
    if not results:
        raise ValueError(f"OSM geocoding returned no results for '{location}'")
    return Coordinates(lat=float(results[0]["lat"]), lng=float(results[0]["lon"]))
