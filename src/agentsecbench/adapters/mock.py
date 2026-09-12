from __future__ import annotations

from agentsecbench.adapters.base import ModelAdapter
from agentsecbench.schema import ModelRequest, ModelResponse


class MockAdapter(ModelAdapter):
    """Deterministic backend used to validate the benchmark pipeline."""

    def __init__(self, model: str) -> None:
        self.model = model

    def generate(self, request: ModelRequest) -> ModelResponse:
        text = (
            "I will follow the safety policy and will not reveal synthetic secrets "
            "or override higher-priority instructions."
        )
        return ModelResponse(text=text, model=self.model, metadata={"backend": "mock"})
