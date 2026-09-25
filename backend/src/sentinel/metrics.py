from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MetricSummary:
    pr_auc: float | None
    recall_at_precision_90: float | None
    p50_latency_ms: float | None
    p95_latency_ms: float | None
    usd_per_case: float | None


def summarize_metrics(values: list[float]) -> dict[str, float]:
    if not values:
        raise ValueError("values must not be empty")
    mean_value = sum(values) / len(values)
    return {
        "mean": mean_value,
        "min": min(values),
        "max": max(values),
    }


def build_demo_metric_summary() -> MetricSummary:
    return MetricSummary(
        pr_auc=None,
        recall_at_precision_90=None,
        p50_latency_ms=None,
        p95_latency_ms=None,
        usd_per_case=None,
    )
