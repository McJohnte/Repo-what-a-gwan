from datetime import datetime

from models import Cafe

DATE_FORMATS = [
    "%Y-%m-%d",  # 2025-11-15  (ISO, common in OSM)
    "%Y-%m",     # 2025-11
    "%Y",        # 2025
    "%b %Y",     # Nov 2025
    "%B %Y",     # November 2025
]


def enrich(cafes: list[Cafe]) -> list[Cafe]:
    """Enrich cafe entries with additional metadata and sort by newest first."""
    for cafe in cafes:
        _estimate_opened_date(cafe)
    return sorted(cafes, key=_sort_key, reverse=True)


def _estimate_opened_date(cafe: Cafe) -> None:
    """Estimate the opening date from available metadata.

    Google Places doesn't directly expose an opening date, so this uses
    heuristics such as the 'start_date' OSM tag or falls back to 'Unknown'.
    """
    if cafe.opened_date:
        return

    start_date = cafe.tags.get("start_date")
    if start_date:
        cafe.opened_date = start_date
        return

    cafe.opened_date = "Unknown"


def _parse_date(date_str: str) -> datetime | None:
    """Try multiple date formats and return the first successful parse."""
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None


def _sort_key(cafe: Cafe) -> str:
    """Return a sort key so that cafes with known dates come first (newest on
    top) and unknowns sink to the bottom."""
    if cafe.opened_date and cafe.opened_date != "Unknown":
        dt = _parse_date(cafe.opened_date)
        if dt:
            return dt.isoformat()
    return ""
