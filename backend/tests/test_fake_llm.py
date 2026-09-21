from __future__ import annotations

from sentinel.fake_llm import FakeLLM


def test_fake_llm_produces_offline_response() -> None:
    llm = FakeLLM(model_name="demo-model")

    reply = llm.invoke("case summary prompt")

    assert "demo-model" in reply
    assert "offline" in reply

    verdict = llm.generate_verdict(case_id="case-42", prompt="case summary prompt")
    assert verdict["case_id"] == "case-42"
    assert verdict["verdict"] == "request_more_info"

