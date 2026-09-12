from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class AttackCase(BaseModel):
    id: str
    category: str
    prompt: str
    synthetic_secret: str | None = None
    success_markers: list[str] = Field(default_factory=list)
    notes: str | None = None


class ModelRequest(BaseModel):
    prompt: str
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


class GenerationConfig(BaseModel):
    temperature: float = 0.0
    max_tokens: int = 128


class ExperimentConfig(BaseModel):
    run_id: str
    model: ModelConfig
    dataset: str
    output_dir: str
    generation: GenerationConfig = Field(default_factory=GenerationConfig)
