from __future__ import annotations

from fastapi.testclient import TestClient

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


def test_compare_route() -> None:
    response = client.post("/compare", json={"case_id": "case-0", "memo": "fraud transaction"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["case_id"] == "case-0"
    assert "result" in payload
