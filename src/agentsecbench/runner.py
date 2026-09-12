from __future__ import annotations

from agentsecbench.adapters.base import ModelAdapter
from agentsecbench.evaluators.base import Evaluator
from agentsecbench.schema import AttackCase, CaseRunResult, ModelRequest


def run_cases(*, cases: list[AttackCase], adapter: ModelAdapter, evaluator: Evaluator, temperature: float, max_tokens: int) -> list[CaseRunResult]:
    results: list[CaseRunResult] = []
    for case in cases:
        response = adapter.generate(ModelRequest(prompt=case.prompt, temperature=temperature, max_tokens=max_tokens))
        evaluation = evaluator.evaluate(case, response)
        results.append(CaseRunResult(case=case, response=response, evaluation=evaluation))
    return results
