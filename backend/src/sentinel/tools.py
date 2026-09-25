from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from sentinel.data.synthetic import SyntheticCaseGenerator
from sentinel.typologies import TypologyIndex


class ScoreTransactionInput(BaseModel):
    case_id: str = Field(min_length=1)


class AccountHistoryInput(BaseModel):
    account_id: str = Field(min_length=1)
    window_days: int = Field(default=30, gt=0, le=365)


class SearchTypologiesInput(BaseModel):
    query: str = Field(min_length=1, max_length=200)


class ScoreTransactionTool:
    def __init__(self, case_store: list[Any] | None = None) -> None:
        self.case_store = case_store or SyntheticCaseGenerator(seed=42).generate_cases(40)

    def __call__(self, case_id: str) -> dict[str, Any]:
        for case in self.case_store:
            if case.case_id == case_id:
                score = max(0.05, min(0.98, float(case.risk_score or 0.2)))
                shap = {
                    "amount": round(float(case.transaction.amount) / 1000.0, 4),
                    "merchant": 0.18 if "merchant" in case.transaction.merchant else 0.04,
                    "memo": 0.27 if "transfer" in case.transaction.memo.lower() else 0.08,
                    "channel": 0.16 if case.transaction.channel == "online" else 0.05,
                }
                return {"case_id": case_id, "score": round(score, 4), "shap_top_5": shap}
        raise ValueError(f"Case {case_id} not found")


class AccountHistoryTool:
    def __init__(self, case_store: list[Any] | None = None) -> None:
        self.case_store = case_store or SyntheticCaseGenerator(seed=42).generate_cases(40)

    def __call__(self, account_id: str, window_days: int = 30) -> dict[str, Any]:
        related = [case for case in self.case_store if case.account_id == account_id]
        if not related:
            return {"account_id": account_id, "window_days": window_days, "summary": "no history"}

        amounts = [float(case.transaction.amount) for case in related]
        avg_amount = sum(amounts) / len(amounts)
        return {
            "account_id": account_id,
            "window_days": window_days,
            "summary": {
                "velocity": round(sum(amounts) / max(1, len(amounts)), 2),
                "avg_amount": round(avg_amount, 2),
                "new_payees": len({case.transaction.merchant for case in related}),
                "geography_change": (
                    "high"
                    if any("merchant" in case.transaction.merchant for case in related)
                    else "low"
                ),
            },
        }


class SearchTypologiesTool:
    def __init__(self, index: TypologyIndex | None = None) -> None:
        self.index = index or TypologyIndex()

    def __call__(self, query: str) -> list[dict[str, str | tuple[str, ...]]]:
        return self.index.search(query, limit=3)
