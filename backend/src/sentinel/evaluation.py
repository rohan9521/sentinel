from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from math import isfinite
from pathlib import Path

from sentinel.baseline import SimpleGBMBaseline
from sentinel.data.synthetic import SyntheticCaseGenerator

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
EVALUATION_RESULTS_PATH = REPOSITORY_ROOT / "results" / "baseline_demo.json"


@dataclass(frozen=True)
class EvaluationResult:
    pr_auc: float
    recall_at_precision_90: float
    precision_at_threshold: float
    recall_at_threshold: float
    cases_evaluated: int
    seed: int
    evaluation_type: str
    model_quality_claim: bool
    p50_latency_ms: float | None
    p95_latency_ms: float | None
    usd_per_case: float | None


def _safe_divide(numerator: float, denominator: float) -> float:
    if denominator == 0:
        return 0.0
    return numerator / denominator


def _validate_inputs(labels: list[int], scores: list[float]) -> None:
    if not labels or not scores or len(labels) != len(scores):
        raise ValueError("labels and scores must be non-empty and aligned")
    if any(label not in (0, 1) for label in labels):
        raise ValueError("labels must contain only 0 and 1")
    if any(not isfinite(score) or not 0.0 <= score <= 1.0 for score in scores):
        raise ValueError("scores must be finite probabilities between 0 and 1")


def _compute_precision_recall(
    labels: list[int],
    scores: list[float],
) -> tuple[list[float], list[float]]:
    pairs = sorted(zip(scores, labels, strict=True), key=lambda item: item[0], reverse=True)
    positives = sum(labels)
    tp = 0
    fp = 0
    prev_recall = 0.0
    precisions: list[float] = []
    recalls: list[float] = []

    for _, label in pairs:
        if label == 1:
            tp += 1
        else:
            fp += 1

        precision = _safe_divide(tp, tp + fp)
        recall = _safe_divide(tp, positives)
        if recall > prev_recall:
            precisions.append(precision)
            recalls.append(recall)
            prev_recall = recall

    return precisions, recalls


def compute_pr_auc(labels: list[int], scores: list[float]) -> float:
    _validate_inputs(labels, scores)

    positives = sum(labels)
    if positives == 0:
        return 0.0

    pairs = sorted(zip(scores, labels, strict=True), key=lambda item: item[0], reverse=True)
    tp = 0
    fp = 0
    prev_recall = 0.0
    area = 0.0

    for _, label in pairs:
        if label == 1:
            tp += 1
        else:
            fp += 1

        recall = _safe_divide(tp, positives)
        precision = _safe_divide(tp, tp + fp)
        if recall > prev_recall:
            area += precision * (recall - prev_recall)
            prev_recall = recall

    return round(area, 6)


def compute_recall_at_precision(
    labels: list[int],
    scores: list[float],
    target_precision: float = 0.9,
) -> float:
    _validate_inputs(labels, scores)
    if not 0.0 <= target_precision <= 1.0:
        raise ValueError("target_precision must be between 0 and 1")

    thresholds = sorted(set(scores), reverse=True)
    best_recall = 0.0

    for threshold in thresholds:
        tp = 0
        fp = 0
        positives = sum(labels)
        for score, label in zip(scores, labels, strict=True):
            if score >= threshold:
                if label == 1:
                    tp += 1
                else:
                    fp += 1

        precision = _safe_divide(tp, tp + fp)
        recall = _safe_divide(tp, positives)
        if precision >= target_precision:
            best_recall = max(best_recall, recall)

    return round(best_recall, 6)


def evaluate_baseline_dataset(case_count: int = 120, seed: int = 42) -> EvaluationResult:
    if case_count <= 0:
        raise ValueError("case_count must be positive")

    generator = SyntheticCaseGenerator(seed=seed)
    cases = generator.generate_cases(case_count)
    labels = [1 if case.label == "fraud" else 0 for case in cases]
    if len(set(labels)) != 2:
        raise ValueError("evaluation dataset must contain both label classes")

    baseline = SimpleGBMBaseline(threshold=0.5)

    scores: list[float] = []
    for case in cases:
        prediction = baseline.score_case(case)
        scores.append(prediction.score)

    threshold_precision = _safe_divide(
        sum(1 for score, label in zip(scores, labels, strict=True) if score >= 0.5 and label == 1),
        sum(1 for score in scores if score >= 0.5),
    )
    threshold_recall = _safe_divide(
        sum(1 for score, label in zip(scores, labels, strict=True) if score >= 0.5 and label == 1),
        sum(labels),
    )

    return EvaluationResult(
        pr_auc=compute_pr_auc(labels, scores),
        recall_at_precision_90=compute_recall_at_precision(labels, scores, target_precision=0.9),
        precision_at_threshold=round(threshold_precision, 6),
        recall_at_threshold=round(threshold_recall, 6),
        cases_evaluated=len(cases),
        seed=seed,
        evaluation_type="synthetic_demo",
        model_quality_claim=False,
        p50_latency_ms=None,
        p95_latency_ms=None,
        usd_per_case=None,
    )


def write_evaluation_results(path: str | Path | None = None) -> EvaluationResult:
    result = evaluate_baseline_dataset()
    output = Path(path) if path is not None else EVALUATION_RESULTS_PATH
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(f"{json.dumps(asdict(result), indent=2)}\n", encoding="utf-8")
    return result
