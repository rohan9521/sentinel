from __future__ import annotations

from sentinel.data.synthetic import SyntheticCaseGenerator
from sentinel.methods import FixedPipelineMethod, GBMMethod, LLMOnlyMethod, ToolCallingAgentMethod


def test_agent_tools_score_and_retrieve() -> None:
    generator = SyntheticCaseGenerator(seed=9)
    case = generator.generate_cases(1)[0]

    assert case.case_id
    assert case.account_id
    assert case.transaction.memo

    gbm = GBMMethod().run(case)
    llm = LLMOnlyMethod().run(case)
    fixed = FixedPipelineMethod().run(case)
    agent = ToolCallingAgentMethod().run(case)

    assert gbm["method"] == "gbm"
    assert llm["method"] == "llm_only"
    assert fixed["method"] == "fixed_pipeline"
    assert agent["method"] == "tool_calling_agent"
    assert gbm["verdict"] in {"fraud", "legitimate"}
    assert llm["verdict"] in {"escalate", "clear", "request_more_info"}
