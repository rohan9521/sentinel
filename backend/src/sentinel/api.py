from __future__ import annotations

from fastapi import FastAPI, HTTPException

from sentinel.config import settings
from sentinel.service import SentinelService

app = FastAPI(title="Sentinel API", version="0.1.0")
service = SentinelService()


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


@app.post("/compare")
def compare_case(payload: dict[str, str]) -> dict[str, object]:
    case_id = payload.get("case_id")
    memo = payload.get("memo", "")
    if not case_id:
        raise HTTPException(status_code=400, detail="case_id is required")
    return service.compare_case(case_id, memo)
