from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from random import Random

from sentinel.domain import Case, Transaction


@dataclass
class SyntheticCaseGenerator:
    seed: int = 42
    drift_schedule: list[tuple[int, float]] | None = None

    def __post_init__(self) -> None:
        if self.drift_schedule is None:
            self.drift_schedule = [(0, 0.0), (50, 0.15), (100, 0.3)]

    def _drift_factor(self, index: int) -> float:
        current = 0.0
        for threshold, factor in self.drift_schedule:
            if index >= threshold:
                current = factor
        return current

    def generate_cases(self, count: int = 100) -> list[Case]:
        rng = Random(self.seed)
        cases: list[Case] = []
        start = datetime(2024, 1, 1, tzinfo=None)

        for index in range(count):
            amount = round(40 + (rng.random() * 1700), 2)
            is_fraud = rng.random() < 0.3 + self._drift_factor(index)
            merchant = f"merchant-{index % 10}"
            transaction = Transaction(
                transaction_id=f"txn-{index}",
                account_id=f"acct-{index % 25}",
                timestamp=start + timedelta(days=index, hours=(index % 12)),
                amount=amount,
                currency="USD",
                memo="wire transfer for recurring subscription" if is_fraud else "coffee purchase from retail partner",
                merchant=merchant,
                channel="online" if index % 2 == 0 else "branch",
            )
            cases.append(
                Case(
                    case_id=f"case-{index}",
                    account_id=transaction.account_id,
                    transaction=transaction,
                    label="fraud" if is_fraud else "legitimate",
                    risk_score=0.9 if is_fraud else 0.1,
                    metadata={"split": "synthetic"},
                )
            )
        return cases

    def split_cases_time_based(self, cases: list[Case], *, train_ratio: float = 0.6, val_ratio: float = 0.2) -> tuple[list[Case], list[Case], list[Case]]:
        if not 0.0 < train_ratio < 1.0 or not 0.0 < val_ratio < 1.0:
            raise ValueError("ratios must be between 0 and 1")

        sorted_cases = sorted(cases, key=lambda case: case.transaction.timestamp)
        train_end = max(1, int(len(sorted_cases) * train_ratio))
        val_end = max(train_end + 1, int(len(sorted_cases) * (train_ratio + val_ratio)))

        train = sorted_cases[:train_end]
        val = sorted_cases[train_end:val_end]
        test = sorted_cases[val_end:]

        if not train or not val or not test:
            raise ValueError("splits are empty; increase the dataset size")

        return train, val, test

