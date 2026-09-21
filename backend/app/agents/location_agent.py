"""Location resolution without browser permission assumptions."""
from dataclasses import dataclass


@dataclass(frozen=True)
class ResolvedLocation:
    latitude: float | None
    longitude: float | None
    city: str | None
    state: str | None


class LocationAgent:
    """Validates explicit GPS coordinates or accepts a city/state fallback."""
    def resolve(self, latitude: float | None, longitude: float | None, city: str | None, state: str | None) -> ResolvedLocation:
        if (latitude is None) != (longitude is None):
            raise ValueError("Latitude and longitude must be supplied together.")
        if latitude is not None and not -90 <= latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90.")
        if longitude is not None and not -180 <= longitude <= 180:
            raise ValueError("Longitude must be between -180 and 180.")
        return ResolvedLocation(latitude, longitude, city, state)
