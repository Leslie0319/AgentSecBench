from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

CaseType = Literal["attack", "benign"]
EvaluationOutcome = Literal[
    "leaked",
    "refused",
    "ambiguous",
    "safe_compliance",
    "over_refusal",
    "utility_failure",
]
EvaluatorName = Literal["keyword_leakage", "structured_safety"]


class AttackCase(BaseModel):
    id: str
    category: str
    prompt: str
    case_type: CaseType = "attack"
    protected_context: str | None = None
    synthetic_secret: str | None = None
    success_markers: list[str] = Field(default_factory=list)
    utility_markers: list[str] = Field(default_factory=list)
    notes: str | None = None


class ModelRequest(BaseModel):
    prompt: str
    system_prompt: str | None = None
    temperature: float = 0.0
    max_tokens: int = 128


class ModelResponse(BaseModel):
    text: str
    model: str
    latency_ms: float | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class EvaluationResult(BaseModel):
    case_id: str
    category: str
    success: bool
    score: float
    reason: str
    outcome: EvaluationOutcome | None = None
    signals: dict[str, bool] = Field(default_factory=dict)


class CaseRunResult(BaseModel):
    case: AttackCase
    response: ModelResponse
    evaluation: EvaluationResult


class ModelConfig(BaseModel):
    backend: Literal["mock", "mock_vulnerable", "openai_compatible"]
    model: str
    base_url: str | None = None
    api_key_env: str | None = None
    timeout_seconds: float = 60.0
    trust_env: bool = True
    request_options: dict[str, Any] = Field(default_factory=dict)


class GenerationConfig(BaseModel):
    temperature: float = 0.0
    max_tokens: int = 128


class ExperimentConfig(BaseModel):
    run_id: str
    model: ModelConfig
    dataset: str
    output_dir: str
    evaluator: EvaluatorName = "keyword_leakage"
    generation: GenerationConfig = Field(default_factory=GenerationConfig)
