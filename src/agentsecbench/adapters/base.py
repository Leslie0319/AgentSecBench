from __future__ import annotations

from abc import ABC, abstractmethod

from agentsecbench.schema import ModelRequest, ModelResponse


class ModelAdapter(ABC):
    @abstractmethod
    def generate(self, request: ModelRequest) -> ModelResponse:
        raise NotImplementedError
