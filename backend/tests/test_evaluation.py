from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

import sentinel.evaluation as evaluation
from sentinel.baseline import SimpleGBMBaseline
from sentinel.data.synthetic import SyntheticCaseGenerator
from sentinel.evaluation import (
    compute_pr_auc,
    compute_recall_at_precision,
    evaluate_baseline_dataset,
)
from sentinel.metrics import build_demo_metric_summary


def test_baseline_score_does_not_depend_on_target_label() -> None:
    case = SyntheticCaseGenerator(seed=42).generate_cases(1)[0]
    opposite_label = replace(
        case,
        label="legitimate" if case.label == "fraud" else "fraud",
    )
    baseline = SimpleGBMBaseline()

    assert baseline.score_case(case) == baseline.score_case(opposite_label)


def test_synthetic_memos_do_not_encode_target_labels() -> None:
    cases = SyntheticCaseGenerator(seed=42).generate_cases(120)
    labels_by_memo: dict[str, set[str]] = {}
    for case in cases:
        labels_by_memo.setdefault(case.transaction.memo, set()).add(case.label)

    assert len(labels_by_memo) > 1
    assert all(labels == {"fraud", "legitimate"} for labels in labels_by_memo.values())


def test_evaluation_is_valid_and_does_not_claim_model_quality() -> None:
    result = evaluate_baseline_dataset(case_count=120, seed=42)

    assert result.cases_evaluated == 120
    assert result.seed == 42
    assert 0.0 <= result.pr_auc <= 1.0
    assert 0.0 <= result.recall_at_precision_90 <= 1.0
    assert 0.0 <= result.precision_at_threshold <= 1.0
    assert 0.0 <= result.recall_at_threshold <= 1.0
    assert result.evaluation_type == "synthetic_demo"
    assert result.model_quality_claim is False
    assert result.p50_latency_ms is None
    assert result.p95_latency_ms is None
    assert result.usd_per_case is None


def test_evaluation_is_reproducible_for_a_fixed_seed() -> None:
    assert evaluate_baseline_dataset(case_count=60, seed=7) == evaluate_baseline_dataset(
        case_count=60,
        seed=7,
    )


def test_default_result_path_is_repository_root_not_current_directory(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    output = tmp_path / "repository" / "results" / "baseline_demo.json"
    monkeypatch.setattr(evaluation, "EVALUATION_RESULTS_PATH", output)
    monkeypatch.chdir(tmp_path)

    evaluation.write_evaluation_results()

    assert output.is_file()
    assert not (tmp_path / "results" / "baseline_demo.json").exists()


@pytest.mark.parametrize(
    ("labels", "scores"),
    [
        ([], []),
        ([0, 1], [0.4]),
        ([0, 2], [0.2, 0.8]),
        ([0, 1], [0.2, float("nan")]),
        ([0, 1], [0.2, 1.1]),
    ],
)
def test_pr_auc_rejects_invalid_evaluation_inputs(
    labels: list[int],
    scores: list[float],
) -> None:
    with pytest.raises(ValueError):
        compute_pr_auc(labels, scores)


def test_recall_at_precision_rejects_invalid_target() -> None:
    with pytest.raises(ValueError, match="target_precision"):
        compute_recall_at_precision([0, 1], [0.2, 0.8], target_precision=1.1)


@pytest.mark.parametrize("case_count", [0, -1, 1])
def test_evaluation_rejects_invalid_or_single_class_dataset(case_count: int) -> None:
    with pytest.raises(ValueError):
        evaluate_baseline_dataset(case_count=case_count)


def test_demo_metric_summary_marks_unmeasured_metrics_unavailable() -> None:
    summary = build_demo_metric_summary()

    assert summary.pr_auc is None
    assert summary.recall_at_precision_90 is None
    assert summary.p50_latency_ms is None
    assert summary.p95_latency_ms is None
    assert summary.usd_per_case is None
