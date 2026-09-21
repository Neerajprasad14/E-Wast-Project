"""Geospatial helpers independent of the storage provider."""
from math import asin, cos, radians, sin, sqrt


def calculate_distance(user_lat: float, user_lon: float, recycler_lat: float, recycler_lon: float) -> float:
    """Return great-circle distance in kilometres using the Haversine formula."""
    earth_radius_km = 6371.0088
    lat_delta = radians(recycler_lat - user_lat)
    lon_delta = radians(recycler_lon - user_lon)
    a = sin(lat_delta / 2) ** 2 + cos(radians(user_lat)) * cos(radians(recycler_lat)) * sin(lon_delta / 2) ** 2
    return earth_radius_km * 2 * asin(sqrt(a))
