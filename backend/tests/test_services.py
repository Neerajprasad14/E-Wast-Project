from app.agents.location_agent import LocationAgent
from app.services.distance import calculate_distance


def test_haversine_distance_is_zero_for_same_point():
    assert calculate_distance(17.385, 78.4867, 17.385, 78.4867) == 0


def test_haversine_distance_hyderabad_to_secunderabad_is_plausible():
    assert 5 < calculate_distance(17.385, 78.4867, 17.4399, 78.4983) < 8


def test_location_agent_requires_coordinates_together():
    try: LocationAgent().resolve(17.3, None, None, None)
    except ValueError as error: assert "together" in str(error)
    else: raise AssertionError("Expected coordinate validation error")
