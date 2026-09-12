from agentsecbench.metrics import summarize
from agentsecbench.schema import AttackCase, CaseRunResult, EvaluationResult, ModelResponse


def _result(case_id: str, category: str, success: bool) -> CaseRunResult:
    return CaseRunResult(
        case=AttackCase(id=case_id, category=category, prompt="x"),
        response=ModelResponse(text="x", model="mock"),
        evaluation=EvaluationResult(case_id=case_id, category=category, success=success, score=float(success), reason="test"),
    )


def test_summarize() -> None:
    summary = summarize([_result("1", "jailbreak", True), _result("2", "jailbreak", False), _result("3", "prompt_injection", True)])
    assert summary["n"] == 3
    assert summary["successes"] == 2
    assert summary["asr"] == 2 / 3
    assert summary["by_category"]["jailbreak"]["asr"] == 0.5
