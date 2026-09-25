from __future__ import annotations

from typing import Any, Protocol

from sentinel.baseline import SimpleGBMBaseline
from sentinel.domain import Case
from sentinel.fake_llm import FakeLLM
from sentinel.tools import AccountHistoryTool, ScoreTransactionTool, SearchTypologiesTool


class TriageMethod(Protocol):
    def run(self, case: Case) -> dict[str, Any]:
        """Execute the method for a single case."""


class GBMMethod:
    def __init__(self, threshold: float = 0.5) -> None:
        self.threshold = threshold

    def run(self, case: Case) -> dict[str, Any]:
        prediction = SimpleGBMBaseline(threshold=self.threshold).score_case(case)
        return {
            "method": "gbm",
            "case_id": case.case_id,
            "verdict": "fraud" if prediction.label == "fraud" else "legitimate",
            "score": prediction.score,
            "label": prediction.label,
            "shap": prediction.shap,
        }


class LLMOnlyMethod:
    def __init__(self, llm: FakeLLM | None = None) -> None:
        self.llm = llm or FakeLLM()

    def run(self, case: Case) -> dict[str, Any]:
        prompt = (
            f"Review transaction {case.case_id} for account {case.account_id}. "
            f"Merchant={case.transaction.merchant}; amount={case.transaction.amount}; "
            f"memo={case.transaction.memo}; channel={case.transaction.channel}"
        )
        verdict = self.llm.generate_verdict(case_id=case.case_id, prompt=prompt)
        return {
            "method": "llm_only",
            "case_id": case.case_id,
            "verdict": verdict["verdict"],
            "confidence": verdict["confidence"],
            "rationale": verdict["rationale"],
            "evidence": verdict["evidence"],
        }


class FixedPipelineMethod:
    def __init__(self, score_tool: ScoreTransactionTool | None = None) -> None:
        self.score_tool = score_tool or ScoreTransactionTool()
        self.history_tool = AccountHistoryTool()
        self.typology_tool = SearchTypologiesTool()

    def run(self, case: Case) -> dict[str, Any]:
        score = self.score_tool(case.case_id)
        history = self.history_tool(case.account_id)
        typologies = self.typology_tool(case.transaction.memo)
        verdict = "escalate" if float(score["score"]) >= 0.55 else "clear"
        return {
            "method": "fixed_pipeline",
            "case_id": case.case_id,
            "verdict": verdict,
            "score": score,
            "history": history,
            "typologies": typologies,
        }


class ToolCallingAgentMethod:
    def __init__(self, score_tool: ScoreTransactionTool | None = None) -> None:
        self.score_tool = score_tool or ScoreTransactionTool()
        self.history_tool = AccountHistoryTool()
        self.typology_tool = SearchTypologiesTool()

    def run(self, case: Case) -> dict[str, Any]:
        score = self.score_tool(case.case_id)
        history = self.history_tool(case.account_id)
        typologies = self.typology_tool(case.transaction.memo)
        verdict = "escalate" if float(score["score"]) >= 0.5 else "request_more_info"
        return {
            "method": "tool_calling_agent",
            "case_id": case.case_id,
            "verdict": verdict,
            "confidence": 0.85 if verdict == "escalate" else 0.62,
            "evidence": [
                {"source": "model", "detail": "score_transaction"},
                {"source": "history", "detail": "get_account_history"},
                {
                    "source": "typology",
                    "detail": typologies[0]["title"] if typologies else "none",
                },
            ],
            "tool_trace": [
                {
                    "tool": "score_transaction",
                    "input": case.case_id,
                    "output_summary": score["score"],
                },
                {
                    "tool": "get_account_history",
                    "input": case.account_id,
                    "output_summary": history["summary"],
                },
            ],
        }
