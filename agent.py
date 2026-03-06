#!/usr/bin/env python3
"""Cafe Finder Agent — scans a map for the newest cafes in an area."""

import argparse
import sys

from config import DEFAULT_LIMIT, DEFAULT_PROVIDER, DEFAULT_RADIUS_KM, MAPS_API_KEY, SUPPORTED_PROVIDERS
from enricher import enrich
from geocoder import geocode
from scanner import scan_cafes


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Find the newest cafes in a given area."
    )
    parser.add_argument(
        "--location",
        required=True,
        help="City, address, or 'lat,lng' coordinates",
    )
    parser.add_argument(
        "--radius",
        type=float,
        default=DEFAULT_RADIUS_KM,
        help=f"Search radius in kilometres (default: {DEFAULT_RADIUS_KM})",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=DEFAULT_LIMIT,
        help=f"Maximum results to return (default: {DEFAULT_LIMIT})",
    )
    parser.add_argument(
        "--provider",
        choices=SUPPORTED_PROVIDERS,
        default=DEFAULT_PROVIDER,
        help=f"Map data provider (default: {DEFAULT_PROVIDER})",
    )
    return parser.parse_args()


def run(location: str, radius: float, limit: int, provider: str) -> None:
    # Validate API key for Google provider
    if provider == "google" and not MAPS_API_KEY:
        print("Error: MAPS_API_KEY environment variable is not set.")
        print("Export it with: export MAPS_API_KEY='your-key-here'")
        sys.exit(1)

    print(f"Searching for newest cafes within {radius} km of {location}...\n")

    # Step 1: Geocode the location
    coords = geocode(location, provider)
    print(f"Resolved coordinates: {coords.lat}, {coords.lng}")

    # Step 2: Scan for cafes
    cafes = scan_cafes(coords, radius, provider)
    if not cafes:
        print("No cafes found in this area.")
        return

    print(f"Found {len(cafes)} cafe(s). Enriching results...\n")

    # Step 3: Enrich and rank
    ranked = enrich(cafes)

    # Step 4: Display results
    for i, cafe in enumerate(ranked[:limit], start=1):
        print(cafe.display(i))


def main() -> None:
    args = parse_args()
    try:
        run(args.location, args.radius, args.limit, args.provider)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
