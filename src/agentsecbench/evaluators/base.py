from __future__ import annotations

from abc import ABC, abstractmethod

from agentsecbench.schema import AttackCase, EvaluationResult, ModelResponse


class Evaluator(ABC):
    @abstractmethod
    def evaluate(self, case: AttackCase, response: ModelResponse) -> EvaluationResult:
        raise NotImplementedError
