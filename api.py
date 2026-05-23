from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from main import run_risk_intelligence_async, run_parallel_analysis
from src.database import get_history, get_critical_alerts


app = FastAPI(
    title="Supply Chain Risk Intelligence API",
    description="Multi-agent autonomous supply chain risk intelligence platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    region: str = Field(..., min_length=2)


class BatchAnalyzeRequest(BaseModel):
    regions: List[str]
    max_concurrency: Optional[int] = 2


class AnalysisResponse(BaseModel):
    region: str
    risk_score: float
    confidence: str
    summary: str
    state: dict


class HistoryRecord(BaseModel):
    region: str
    risk_score: float
    confidence_level: str
    executive_summary: str
    timestamp: str


class CriticalAlertRecord(BaseModel):
    region: str
    risk_score: float
    executive_summary: str
    timestamp: str


@app.get("/")
async def root():
    return {
        "service": "Supply Chain Risk Intelligence API",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "supply-chain-risk-intelligence",
        "features": {
            "agentic_memory": True,
            "parallel_analysis": True,
            "scheduler": True,
            "critical_alerts": True,
            "fastapi_backend": True
        }
    }


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_region(request: AnalyzeRequest):
    try:
        result = await run_risk_intelligence_async(request.region)

        if not result:
            raise HTTPException(
                status_code=500,
                detail="Analysis failed"
            )

        return result

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal analysis error: {str(e)}"
        )


@app.post("/analyze/batch")
async def analyze_batch(request: BatchAnalyzeRequest):
    try:
        if len(request.regions) == 0:
            raise HTTPException(
                status_code=400,
                detail="Regions list cannot be empty"
            )

        results = await run_parallel_analysis(
            regions=request.regions,
            max_concurrency=request.max_concurrency
        )

        successful = [r for r in results if r is not None]

        return {
            "total_requested": len(request.regions),
            "successful": len(successful),
            "failed": len(request.regions) - len(successful),
            "results": successful
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Batch analysis failed: {str(e)}"
        )


@app.get("/history", response_model=List[HistoryRecord])
async def history():
    try:
        rows = get_history(limit=10)

        return [
            HistoryRecord(
                region=row[0],
                risk_score=row[1],
                confidence_level=row[2],
                executive_summary=row[3],
                timestamp=row[4]
            )
            for row in rows
        ]

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch history: {str(e)}"
        )


@app.get("/critical-alerts", response_model=List[CriticalAlertRecord])
async def critical_alerts():
    try:
        rows = get_critical_alerts(limit=20)

        return [
            CriticalAlertRecord(
                region=row[0],
                risk_score=row[1],
                executive_summary=row[2],
                timestamp=row[3]
            )
            for row in rows
        ]

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch alerts: {str(e)}"
        )