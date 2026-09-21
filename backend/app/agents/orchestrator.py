import asyncio
from app.agents.category_agent import EWasteCategoryAgent
from app.agents.condition_agent import ConditionAssessmentAgent
from app.agents.image_agent import ImageClassificationAgent
from app.agents.impact_agent import EnvironmentalImpactAgent
from app.agents.recycler_locator_agent import RecyclerLocatorAgent
from app.agents.recycling_agent import RecyclingAdvisorAgent
from app.schemas.analysis import AnalyzeResponse


class EWasteAdvisorOrchestrator:
    def __init__(self) -> None:
        self.image_agent, self.condition_agent, self.category_agent = ImageClassificationAgent(), ConditionAssessmentAgent(), EWasteCategoryAgent()
        self.impact_agent, self.recycling_agent, self.locator = EnvironmentalImpactAgent(), RecyclingAdvisorAgent(), RecyclerLocatorAgent()

    async def analyze(self, image_bytes: bytes, filename: str, latitude: float | None = None, longitude: float | None = None) -> AnalyzeResponse:
        classification, condition = await asyncio.gather(self.image_agent.analyze(image_bytes, filename), self.condition_agent.analyze(image_bytes))
        classification = await self.category_agent.analyze(classification)
        impact, recommendation = await asyncio.gather(self.impact_agent.analyze(classification.object), self.recycling_agent.analyze(condition))
        recyclers = self.locator.search(latitude, longitude, 25, classification.object) if latitude is not None and longitude is not None else []
        warnings = ["Image classification uses a filename-based local fallback until a vision provider is configured.", "Recycler records in this starter dataset are explicitly marked DEMO DATA."]
        return AnalyzeResponse(classification=classification, condition=condition, environmental_impact=impact, recommendation=recommendation, nearby_recyclers=recyclers, warnings=warnings)
