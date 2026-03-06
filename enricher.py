from datetime import datetime

from models import Cafe


def enrich(cafes: list[Cafe]) -> list[Cafe]:
    """Enrich cafe entries with additional metadata and sort by newest first."""
    for cafe in cafes:
        _estimate_opened_date(cafe)
    return sorted(cafes, key=_sort_key, reverse=True)


def _estimate_opened_date(cafe: Cafe) -> None:
    """Estimate the opening date from available metadata.

    Google Places doesn't directly expose an opening date, so this uses
    heuristics such as the 'start_date' OSM tag or falls back to 'Unknown'.
    A production version could cross-reference review timestamps or business
    registration databases for a more accurate date.
    """
    if cafe.opened_date:
        return

    # OSM data sometimes includes a start_date tag
    if "start_date" in cafe.tags:
        cafe.opened_date = cafe.tags[cafe.tags.index("start_date")]
        return

    cafe.opened_date = "Unknown"


def _sort_key(cafe: Cafe) -> str:
    """Return a sort key so that cafes with known dates come first (newest on
    top) and unknowns sink to the bottom."""
    if cafe.opened_date and cafe.opened_date != "Unknown":
        try:
            return datetime.strptime(cafe.opened_date, "%b %Y").isoformat()
        except ValueError:
            pass
    return ""
