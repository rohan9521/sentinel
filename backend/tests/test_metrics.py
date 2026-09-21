from __future__ import annotations

from sentinel.fake_llm import FakeLLM
from sentinel.metrics import build_demo_metric_summary


def test_fake_llm_produces_offline_response() -> None:
    llm = FakeLLM(model_name="demo-model")

    reply = llm.invoke("fraud case summary prompt")

    assert "demo-model" in reply
    assert "offline" in reply

    verdict = llm.generate_verdict(case_id="case-42", prompt="fraud case summary prompt")
    assert verdict["case_id"] == "case-42"
    assert verdict["verdict"] == "escalate"


def test_metric_summary_is_stable() -> None:
    summary = build_demo_metric_summary()

    assert summary.pr_auc > 0.8
    assert summary.recall_at_precision_90 > 0.5
    assert summary.p95_latency_ms > summary.p50_latency_ms
