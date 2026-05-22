from pydantic import BaseModel, Field
from typing import List


class RiskReportSchema(BaseModel):
    executive_summary: str = Field(description="High-level executive summary")
    risk_score: int = Field(description="Risk score from 1 to 10")
    key_risks: List[str] = Field(description="Top identified supply chain risks")
    recommended_actions: List[str] = Field(description="Mitigation recommendations")
    confidence_level: str = Field(description="Low, Medium, or High confidence")