from __future__ import annotations

from sentinel.evaluation import evaluate_baseline_dataset


def test_pr_auc_is_reasonable() -> None:
    result = evaluate_baseline_dataset(case_count=120, seed=42)

    assert result.cases_evaluated == 120
    assert 0.0 <= result.pr_auc <= 1.0
    assert 0.0 <= result.recall_at_precision_90 <= 1.0
    assert result.p50_latency_ms > 0
    assert result.p95_latency_ms > result.p50_latency_ms
    assert result.usd_per_case > 0


def test_evaluation_uses_seeded_data() -> None:
    first = evaluate_baseline_dataset(case_count=60, seed=7)
    second = evaluate_baseline_dataset(case_count=60, seed=7)

    assert first == second
