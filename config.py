import os


MAPS_API_KEY = os.environ.get("MAPS_API_KEY", "")

DEFAULT_RADIUS_KM = 2
DEFAULT_LIMIT = 10
DEFAULT_PROVIDER = "google"

SUPPORTED_PROVIDERS = ("google", "osm")

GOOGLE_PLACES_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
GOOGLE_GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"

OSM_NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
OSM_OVERPASS_URL = "https://overpass-api.de/api/interpreter"
