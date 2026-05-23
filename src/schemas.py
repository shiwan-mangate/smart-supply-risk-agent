from typing import List
from pydantic import BaseModel, Field


class RiskReportSchema(BaseModel):
    executive_summary: str = Field(
        description="High-level executive summary"
    )

    risk_score: float = Field(
        description="Risk score from 1 to 10"
    )

    key_risks: List[str] = Field(
        description="Top identified supply chain risks"
    )

    recommended_actions: List[str] = Field(
        description="Mitigation recommendations"
    )

    confidence_level: str = Field(
        description="Low, Medium, or High confidence"
    )


class CompetitorIntelSchema(BaseModel):
    competitor_exposure: str = Field(
        description="How competitors are affected by the same disruption"
    )

    competitive_opportunity: str = Field(
        description="Strategic opportunity if we move faster"
    )

    differentiation_action: str = Field(
        description="Recommended competitive differentiation move"
    )
    