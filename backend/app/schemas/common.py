from typing import Any
from pydantic import BaseModel, Field


class AgentResult(BaseModel):
    """Consistent, serializable outcome used by every agent."""
    success: bool = True
    confidence: float | None = Field(default=None, ge=0, le=1)
    data: dict[str, Any] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)
    error: str | None = None
