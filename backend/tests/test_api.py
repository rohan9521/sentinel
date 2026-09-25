from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

import sentinel.service as service_module
from sentinel.api import app

client = TestClient(app)


def test_health_route() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_cases_route() -> None:
    response = client.get("/cases")
    assert response.status_code == 200
    payload = response.json()
    assert "cases" in payload
    assert payload["cases"]


def test_results_route_reads_canonical_artifact_and_marks_unmeasured_fields(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    artifact = tmp_path / "repo" / "results" / "baseline_demo.json"
    artifact.parent.mkdir(parents=True)
    artifact.write_text(
        json.dumps(
            {
                "pr_auc": 0.42,
                "recall_at_precision_90": 0.25,
                "p50_latency_ms": None,
                "p95_latency_ms": None,
                "usd_per_case": None,
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(service_module, "EVALUATION_RESULTS_PATH", artifact)
    monkeypatch.chdir(tmp_path)

    response = client.get("/results")

    assert response.status_code == 200
    payload = response.json()
    assert payload["evaluation_type"] == "synthetic_demo"
    assert payload["model_quality_claim"] is False
    assert payload["metrics"]["pr_auc"] == 0.42
    assert payload["metrics"]["recall_at_precision_90"] == 0.25
    assert payload["metrics"]["latency_ms_p50"] is None
    assert payload["metrics"]["latency_ms_p95"] is None
    assert payload["metrics"]["usd_per_case"] is None


def test_compare_route() -> None:
    response = client.post(
        "/compare",
        json={
            "case_id": "case-0",
            "memo": "wire transfer",
            "provider": "fake",
            "model": "fake-model",
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["case_id"] == "case-0"
    assert payload["provider"] == "fake"
    assert payload["offline"] is True
    assert payload["placeholder"] is True
    assert "response" in payload


def test_anthropic_provider_requires_an_api_key() -> None:
    response = client.post(
        "/compare",
        json={
            "case_id": "case-0",
            "provider": "anthropic",
            "model": "claude-3-5-haiku-latest",
        },
    )
    assert response.status_code == 422


def test_unknown_case_is_rejected_before_calling_provider() -> None:
    response = client.post(
        "/compare",
        json={"case_id": "not-a-case", "provider": "fake", "model": "fake-model"},
    )
    assert response.status_code == 404
