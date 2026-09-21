from app.schemas.analysis import EnvironmentalImpact, RiskLevel


class EnvironmentalImpactAgent:
    async def analyze(self, waste_type: str) -> EnvironmentalImpact:
        battery_related = "battery" in waste_type.lower()
        return EnvironmentalImpact(risk_level=RiskLevel.high if battery_related else RiskLevel.medium, environmental_impacts=["Improper disposal can release hazardous substances into soil and water.", "Authorized recovery reduces demand for newly mined materials."], health_concerns=["Do not burn, crush, or dismantle electronic waste."], reason="The image cannot establish exact chemical composition; advice is based on the product category.")
