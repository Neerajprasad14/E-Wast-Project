from app.schemas.analysis import Classification


class EWasteCategoryAgent:
    async def analyze(self, classification: Classification) -> Classification:
        return classification
