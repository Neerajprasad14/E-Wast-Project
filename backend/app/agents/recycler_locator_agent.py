from app.agents.recycler_ranking_agent import RecyclerRankingAgent
from app.schemas.analysis import RecyclerResponse
from app.services.distance import calculate_distance
from app.services.recycler_repository import get_recyclers


class RecyclerLocatorAgent:
    def __init__(self) -> None: self.ranking_agent = RecyclerRankingAgent()
    def search(self, latitude: float, longitude: float, radius_km: float, waste_type: str | None = None, verified_only: bool = False) -> list[RecyclerResponse]:
        candidates = []
        for recycler in get_recyclers():
            recycler.distance_km = round(calculate_distance(latitude, longitude, recycler.latitude, recycler.longitude), 2)
            compatible = not waste_type or any(waste_type.lower() in item.lower() or item.lower() in waste_type.lower() for item in recycler.accepted_waste_types)
            if recycler.distance_km <= radius_km and compatible and (not verified_only or recycler.verified): candidates.append(recycler)
        return self.ranking_agent.rank(candidates, waste_type or "")
