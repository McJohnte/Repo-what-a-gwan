import requests

from config import GOOGLE_PLACES_URL, MAPS_API_KEY, OSM_OVERPASS_URL
from models import Cafe, Coordinates


def scan_cafes(
    coords: Coordinates, radius_km: float, provider: str = "google"
) -> list[Cafe]:
    """Query a map provider for cafes within the given radius."""
    if provider == "google":
        return _scan_google(coords, radius_km)
    return _scan_osm(coords, radius_km)


def _scan_google(coords: Coordinates, radius_km: float) -> list[Cafe]:
    radius_m = int(radius_km * 1000)
    resp = requests.get(
        GOOGLE_PLACES_URL,
        params={
            "location": f"{coords.lat},{coords.lng}",
            "radius": radius_m,
            "type": "cafe",
            "key": MAPS_API_KEY,
        },
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    if data.get("status") not in ("OK", "ZERO_RESULTS"):
        raise RuntimeError(f"Google Places API error: {data.get('status')}")

    cafes = []
    for place in data.get("results", []):
        loc = place["geometry"]["location"]
        cafes.append(
            Cafe(
                name=place.get("name", "Unknown"),
                address=place.get("vicinity", "N/A"),
                coordinates=Coordinates(lat=loc["lat"], lng=loc["lng"]),
                rating=place.get("rating"),
                place_id=place.get("place_id"),
            )
        )
    return cafes


def _scan_osm(coords: Coordinates, radius_km: float) -> list[Cafe]:
    radius_m = int(radius_km * 1000)
    query = f"""
    [out:json][timeout:25];
    (
      node["amenity"="cafe"](around:{radius_m},{coords.lat},{coords.lng});
      way["amenity"="cafe"](around:{radius_m},{coords.lat},{coords.lng});
    );
    out center;
    """
    resp = requests.post(OSM_OVERPASS_URL, data={"data": query}, timeout=30)
    resp.raise_for_status()
    elements = resp.json().get("elements", [])

    cafes = []
    for el in elements:
        tags = el.get("tags", {})
        lat = el.get("lat") or el.get("center", {}).get("lat", 0)
        lng = el.get("lon") or el.get("center", {}).get("lon", 0)
        cafes.append(
            Cafe(
                name=tags.get("name", "Unknown"),
                address=tags.get("addr:street", "N/A"),
                coordinates=Coordinates(lat=lat, lng=lng),
                tags=tags,
            )
        )
    return cafes
