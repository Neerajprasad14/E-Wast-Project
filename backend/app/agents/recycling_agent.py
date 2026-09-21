from app.schemas.analysis import ConditionAssessment, Recommendation


class RecyclingAdvisorAgent:
    async def analyze(self, condition: ConditionAssessment) -> Recommendation:
        action = "RECYCLE" if condition.condition.value in {"Damaged", "Severely Damaged"} else "INSPECT THEN REPAIR OR RECYCLE"
        return Recommendation(action=action, reason="Use an authorized recycler when reuse or safe repair is not practical.", steps=["Back up and factory-reset personal data if the device still works.", "Keep batteries intact and separate loose batteries where accepted.", "Confirm accepted waste types with the recycler before visiting."], safety_instructions=["Do not place e-waste in general household waste.", "Do not puncture, bend, or expose damaged batteries to heat."])
