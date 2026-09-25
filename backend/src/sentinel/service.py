from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from sentinel.data.synthetic import build_demo_dataset
from sentinel.evaluation import EVALUATION_RESULTS_PATH
from sentinel.fake_llm import FakeLLM
from sentinel.llm import (
    LLMAnalysisRequest,
    LLMAnalysisResponse,
    analyze_with_llm,
    build_case_prompt,
)


@dataclass(frozen=True)
class CaseSummary:
    case_id: str
    account_id: str
    merchant: str
    amount: float
    status: str
    risk_score: float
    timestamp: str


class SentinelService:
    """Business logic wrapper for the Sentinel demo API."""

    def __init__(self, llm: FakeLLM | None = None) -> None:
        self.llm = llm or FakeLLM()

    def list_cases(self) -> list[CaseSummary]:
        return [
            CaseSummary(
                case_id=case.case_id,
                account_id=case.account_id,
                merchant=case.transaction.merchant,
                amount=float(case.transaction.amount),
                status="flagged" if case.label == "fraud" else "clear",
                risk_score=float(case.risk_score or 0.0),
                timestamp=case.transaction.timestamp.isoformat(),
            )
            for case in build_demo_dataset()
        ]

    def get_case(self, case_id: str) -> dict[str, Any] | None:
        for case in build_demo_dataset():
            if case.case_id == case_id:
                return {
                    "case_id": case.case_id,
                    "account_id": case.account_id,
                    "merchant": case.transaction.merchant,
                    "amount": float(case.transaction.amount),
                    "currency": case.transaction.currency,
                    "channel": case.transaction.channel,
                    "memo": case.transaction.memo,
                    "status": "flagged" if case.label == "fraud" else "clear",
                    "risk_score": float(case.risk_score or 0.0),
                    "timestamp": case.transaction.timestamp.isoformat(),
                    "evidence": [{"source": "model", "detail": "synthetic fraud signal"}],
                }
        return None

    def analyze_case(self, request: LLMAnalysisRequest) -> LLMAnalysisResponse | None:
        case = next(
            (item for item in build_demo_dataset() if item.case_id == request.case_id),
            None,
        )
        if case is None:
            return None
        facts = (
            f"account={case.account_id}; merchant={case.transaction.merchant}; "
            f"amount={case.transaction.amount} {case.transaction.currency}; "
            f"channel={case.transaction.channel}; "
            f"timestamp={case.transaction.timestamp.isoformat()}"
        )
        prompt = build_case_prompt(
            case_id=case.case_id,
            case_facts=facts,
            memo=request.memo or case.transaction.memo,
        )
        return analyze_with_llm(request, prompt=prompt)

    def get_results(self) -> dict[str, Any]:
        path = EVALUATION_RESULTS_PATH
        if path.exists():
            metrics = json.loads(path.read_text(encoding="utf-8"))
            return {
                "evaluation_type": "synthetic_demo",
                "model_quality_claim": False,
                "metrics": {
                    "pr_auc": metrics.get("pr_auc"),
                    "recall_at_precision_90": metrics.get("recall_at_precision_90"),
                    "latency_ms_p50": None,
                    "latency_ms_p95": None,
                    "usd_per_case": None,
                },
                "generated_at": path.stat().st_mtime,
            }
        return {
            "evaluation_type": "synthetic_demo",
            "model_quality_claim": False,
            "metrics": {
                "pr_auc": None,
                "recall_at_precision_90": None,
                "latency_ms_p50": None,
                "latency_ms_p95": None,
                "usd_per_case": None,
            },
            "generated_at": "offline-demo",
        }
