from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from sentinel.config import settings
from sentinel.llm import LLMAnalysisRequest, LLMAnalysisResponse
from sentinel.service import SentinelService

app = FastAPI(title="Sentinel API", version="0.1.0")
service = SentinelService()


class ErrorResponse(BaseModel):
    detail: str


@app.get("/health")
def health() -> dict[str, str | bool | float]:
    return {
        "status": "ok",
        "offline_mode": settings.llm_provider == "fake",
        "provider": settings.llm_provider,
        "max_usd": settings.max_usd,
    }


@app.get("/cases")
def list_cases() -> dict[str, list[dict[str, object]]]:
    return {"cases": [case.__dict__ for case in service.list_cases()]}


@app.get("/cases/{case_id}")
def get_case(case_id: str) -> dict[str, object]:
    case = service.get_case(case_id)
    if case is None:
        raise HTTPException(status_code=404, detail="case not found")
    return case


@app.get("/results")
def get_results() -> dict[str, object]:
    return service.get_results()


@app.post(
    "/compare",
    response_model=LLMAnalysisResponse,
    responses={502: {"model": ErrorResponse}},
)
def compare_case(payload: LLMAnalysisRequest) -> LLMAnalysisResponse:
    try:
        result = service.analyze_case(payload)
    except RuntimeError as error:
        raise HTTPException(status_code=502, detail=str(error)) from error
    if result is None:
        raise HTTPException(status_code=404, detail="case not found")
    return result
