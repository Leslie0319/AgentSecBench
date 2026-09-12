from __future__ import annotations

import re

from agentsecbench.adapters.base import ModelAdapter
from agentsecbench.schema import ModelRequest, ModelResponse


class VulnerableMockAdapter(ModelAdapter):
    """Deterministic synthetic backend that intentionally leaks protected markers.

    This exists only to verify that the benchmark can distinguish a safe
    backend from an intentionally vulnerable one. It is not a real model.
    """

    _marker_pattern = re.compile(r"AGENTSECBENCH_SECRET_\d+")

    def __init__(self, model: str) -> None:
        self.model = model

    def generate(self, request: ModelRequest) -> ModelResponse:
        source = request.system_prompt or ""
        match = self._marker_pattern.search(source)
        leaked = match.group(0) if match else "AGENTSECBENCH_SECRET_999"

        return ModelResponse(
            text=f"Sure. The synthetic secret is {leaked}.",
            model=self.model,
            metadata={"backend": "mock_vulnerable", "synthetic_only": True},
        )
