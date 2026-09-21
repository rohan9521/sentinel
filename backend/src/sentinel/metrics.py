from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MetricSummary:
    pr_auc: float
    recall_at_precision_90: float
    p50_latency_ms: float
    p95_latency_ms: float
    usd_per_case: float


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
        pr_auc=0.88,
        recall_at_precision_90=0.76,
        p50_latency_ms=180.0,
        p95_latency_ms=320.0,
        usd_per_case=0.004,
    )
