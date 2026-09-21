from enum import Enum
from pydantic import BaseModel, Field


class Condition(str, Enum):
    excellent = "Excellent"
    good = "Good"
    fair = "Fair"
    damaged = "Damaged"
    severely_damaged = "Severely Damaged"
    unknown = "Unknown"


class RiskLevel(str, Enum):
    low = "Low"
    medium = "Medium"
    high = "High"


class Classification(BaseModel):
    object: str
    category: str
    confidence: float = Field(ge=0, le=1)


class ConditionAssessment(BaseModel):
    condition: Condition
    repairability: str
    confidence: float = Field(ge=0, le=1)
    observations: list[str]


class EnvironmentalImpact(BaseModel):
    risk_level: RiskLevel
    environmental_impacts: list[str]
    health_concerns: list[str]
    reason: str


class Recommendation(BaseModel):
    action: str
    reason: str
    steps: list[str]
    safety_instructions: list[str]


class AnalyzeResponse(BaseModel):
    classification: Classification
    condition: ConditionAssessment
    environmental_impact: EnvironmentalImpact
    recommendation: Recommendation
    nearby_recyclers: list["RecyclerResponse"]
    warnings: list[str] = []


class RecyclerResponse(BaseModel):
    id: str
    name: str
    address: str
    city: str
    state: str
    latitude: float
    longitude: float
    accepted_waste_types: list[str]
    pickup_available: bool
    verified: bool
    authorization_status: str
    verification_source: str | None = None
    last_verified: str | None = None
    opening_hours: str | None = None
    phone: str | None = None
    email: str | None = None
    website: str | None = None
    rating: float | None = None
    distance_km: float | None = None
    score: float | None = None
    rank: int | None = None
    ranking_reason: str | None = None
