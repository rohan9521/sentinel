from __future__ import annotations

from dataclasses import dataclass
from math import exp

from sentinel.domain import Case


@dataclass(frozen=True)
class BaselinePrediction:
    case_id: str
    score: float
    label: str
    shap: dict[str, float]


class SimpleGBMBaseline:
    """Deterministic rule-based heuristic scorer for offline demo use."""

    def __init__(self, threshold: float = 0.5) -> None:
        self.threshold = threshold

    def score_case(self, case: Case) -> BaselinePrediction:
        amount_signal = min(case.transaction.amount / 1000.0, 1.5)
        memo_signal = 0.0
        memo_lower = case.transaction.memo.lower()
        if "wire" in memo_lower or "transfer" in memo_lower:
            memo_signal += 0.45
        if "subscription" in memo_lower or "recurring" in memo_lower:
            memo_signal += 0.35
        if "coffee" in memo_lower or "retail" in memo_lower:
            memo_signal -= 0.15

        channel_signal = 0.18 if case.transaction.channel == "online" else 0.04
        merchant_signal = 0.14 if case.transaction.merchant.startswith("merchant-") else 0.0

        raw_score = 0.2 + amount_signal + memo_signal + channel_signal + merchant_signal
        raw_score = max(-2.0, min(2.0, raw_score))
        probability = 1.0 / (1.0 + exp(-raw_score))

        label = "fraud" if probability >= self.threshold else "legitimate"
        shap = {
            "amount": round(amount_signal / 2.0, 4),
            "memo": round(memo_signal / 2.0, 4),
            "channel": round(channel_signal / 2.0, 4),
            "merchant": round(merchant_signal / 2.0, 4),
        }

        return BaselinePrediction(
            case_id=case.case_id,
            score=round(probability, 6),
            label=label,
            shap=shap,
        )
