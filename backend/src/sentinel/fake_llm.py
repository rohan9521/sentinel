from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class FakeLLM:
    """Offline LLM stand-in used by tests and local demo mode."""

    model_name: str = "fake-model"
    max_usd: float = 0.25

    def invoke(self, prompt: str, **kwargs: Any) -> str:
        if not prompt:
            raise ValueError("prompt must not be empty")
        return (
            "fake: "
            f"model={self.model_name} "
            f"tokens={len(prompt.split())} "
            f"status=offline"
        )

    def generate_verdict(self, *, case_id: str, prompt: str) -> dict[str, Any]:
        return {
            "case_id": case_id,
            "verdict": "request_more_info",
            "confidence": 0.5,
            "rationale": f"Offline demo verdict for {case_id}.",
            "evidence": [{"source": "model", "detail": prompt[:80]}],
        }

