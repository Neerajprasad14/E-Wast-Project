from app.schemas.analysis import Condition, ConditionAssessment


class ConditionAssessmentAgent:
    async def analyze(self, image_bytes: bytes) -> ConditionAssessment:
        return ConditionAssessment(condition=Condition.unknown, repairability="Requires physical inspection", confidence=0.0, observations=["A local fallback cannot assess visible damage from pixels.", "Internal condition cannot be inferred from an image."])
