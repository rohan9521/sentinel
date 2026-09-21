from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sentinel.data.synthetic import build_demo_dataset
from sentinel.fake_llm import FakeLLM


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

    def compare_case(self, case_id: str, memo: str) -> dict[str, Any]:
        result = self.llm.compare_methods(case_id=case_id, prompt=memo)
        return {"case_id": case_id, "result": result}

    def get_results(self) -> dict[str, Any]:
        return {
            "metrics": {
                "pr_auc": 0.88,
                "recall_at_precision_90": 0.76,
                "latency_ms_p50": 180,
                "latency_ms_p95": 320,
                "usd_per_case": 0.004,
            },
            "generated_at": "offline-demo",
        }
