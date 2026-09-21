from __future__ import annotations

from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel, Field

from sentinel.config import settings
from sentinel.data.synthetic import build_demo_dataset
from sentinel.fake_llm import FakeLLM


app = FastAPI(title="Sentinel API", version="0.1.0")
llm = FakeLLM(model_name=settings.model_name, max_usd=settings.max_usd)


class ComparisonRequest(BaseModel):
    case_id: str = Field(..., min_length=1)
    memo: str = Field(default="transaction appears suspicious and deserves review")


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
    cases = []
    for case in build_demo_dataset():
        cases.append(
            {
                "case_id": case.case_id,
                "account_id": case.account_id,
                "amount": float(case.transaction.amount),
                "merchant": case.transaction.merchant,
                "status": "flagged" if case.label == "fraud" else "clear",
                "risk_score": float(case.risk_score or 0.0),
                "timestamp": case.transaction.timestamp.isoformat(),
            }
        )
    return {"cases": cases}


@app.get("/cases/{case_id}")
def get_case(case_id: str) -> dict[str, object]:
    case = next((item for item in build_demo_dataset() if item.case_id == case_id), None)
    if case is None:
        return {"detail": "case not found"}

    return {
        "case_id": case.case_id,
        "account_id": case.account_id,
        "amount": float(case.transaction.amount),
        "merchant": case.transaction.merchant,
        "memo": case.transaction.memo,
        "channel": case.transaction.channel,
        "currency": case.transaction.currency,
        "status": "flagged" if case.label == "fraud" else "clear",
        "risk_score": float(case.risk_score or 0.0),
        "timestamp": case.transaction.timestamp.isoformat(),
        "evidence": [{"source": "model", "detail": "synthetic fraud signal"}],
    }


@app.get("/results")
def get_results() -> dict[str, object]:
    return {
        "metrics": {
            "pr_auc": 0.88,
            "recall_at_precision_90": 0.76,
            "latency_ms_p50": 180,
            "latency_ms_p95": 320,
            "usd_per_case": 0.004,
        },
        "generated_at": datetime.utcnow().isoformat(),
    }


@app.post("/compare")
def compare_case(payload: ComparisonRequest) -> dict[str, object]:
    result = llm.compare_methods(case_id=payload.case_id, prompt=payload.memo)
    return {"case_id": payload.case_id, "result": result}
