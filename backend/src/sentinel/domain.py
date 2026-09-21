from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class Transaction:
    transaction_id: str
    account_id: str
    timestamp: datetime
    amount: float
    currency: str
    memo: str
    merchant: str
    channel: str


@dataclass(frozen=True)
class Case:
    case_id: str
    account_id: str
    transaction: Transaction
    label: str
    risk_score: float | None = None
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class Evidence:
    source: str
    detail: str


@dataclass(frozen=True)
class Verdict:
    verdict: str
    confidence: float
    evidence: list[Evidence]
    rationale: str


