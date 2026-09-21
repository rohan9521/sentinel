from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class Evidence(BaseModel):
    source: Literal["model", "history", "typology"]
    detail: str


class ToolTraceEntry(BaseModel):
    tool: str
    input: dict[str, Any]
    output_summary: str
    latency_ms: int


class Verdict(BaseModel):
    verdict: Literal["escalate", "clear", "request_more_info"]
    confidence: float = Field(ge=0.0, le=1.0)
    evidence: list[Evidence] = Field(default_factory=list)
    rationale: str
    tool_trace: list[ToolTraceEntry] = Field(default_factory=list)
