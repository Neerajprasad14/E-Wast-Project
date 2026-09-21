from app.schemas.analysis import RecyclerResponse


class RecyclerRankingAgent:
    """Application ranking, not evidence of official certification."""
    def rank(self, recyclers: list[RecyclerResponse], waste_type: str) -> list[RecyclerResponse]:
        max_distance = max((item.distance_km or 0.0 for item in recyclers), default=1.0) or 1.0
        ranked = []
        for item in recyclers:
            distance_score = max(0.0, 1 - ((item.distance_km or max_distance) / max_distance)) * 40
            compatible = any(waste_type.lower() in value.lower() or value.lower() in waste_type.lower() for value in item.accepted_waste_types)
            score = distance_score + (25 if compatible else 0) + (15 if item.verified else 0) + (10 if item.pickup_available else 0) + ((item.rating or 0) / 5 * 10)
            reason = "Nearby" if (item.distance_km or 0) < 10 else "Within the selected search area"
            item.score, item.ranking_reason = round(score, 1), f"{reason}; " + ("accepts this waste type, " if compatible else "waste compatibility should be confirmed, ") + ("verified and " if item.verified else "unverified and ") + ("offers pickup." if item.pickup_available else "does not list pickup.")
            ranked.append(item)
        ranked.sort(key=lambda item: item.score or 0, reverse=True)
        for index, item in enumerate(ranked, 1): item.rank = index
        return ranked
