from __future__ import annotations

from sentinel.domain import Case, Verdict


def build_verdict(case: Case) -> Verdict:
    if case.label == "fraud":
        return Verdict(
            verdict="escalate",
            confidence=0.88,
            evidence=[{"source": "model", "detail": f"High risk score for {case.case_id}"}],
            rationale="Synthetic rule-based demo verdict for a fraud case.",
        )

    return Verdict(
        verdict="clear",
        confidence=0.91,
        evidence=[{"source": "history", "detail": f"Customer {case.account_id} has a stable pattern."}],
        rationale="Synthetic rule-based demo verdict for a legitimate case.",
    )

