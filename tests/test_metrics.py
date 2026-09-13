from agentsecbench.metrics import summarize
from agentsecbench.schema import AttackCase, CaseRunResult, EvaluationResult, ModelResponse


def _result(
    case_id: str,
    category: str,
    success: bool,
    *,
    case_type: str = "attack",
    refusal: bool = False,
    utility_success: bool = False,
) -> CaseRunResult:
    return CaseRunResult(
        case=AttackCase(
            id=case_id,
            category=category,
            prompt="x",
            case_type=case_type,
        ),
        response=ModelResponse(text="x", model="mock"),
        evaluation=EvaluationResult(
            case_id=case_id,
            category=category,
            success=success,
            score=float(success),
            reason="test",
            signals={
                "refusal": refusal,
                "utility_success": utility_success,
                "leakage": success,
            },
        ),
    )


def test_summarize() -> None:
    summary = summarize(
        [
            _result("1", "jailbreak", True),
            _result("2", "jailbreak", False),
            _result("3", "prompt_injection", True),
        ]
    )
    assert summary["n"] == 3
    assert summary["attack_n"] == 3
    assert summary["successes"] == 2
    assert summary["asr"] == 2 / 3
    assert summary["by_category"]["jailbreak"]["asr"] == 0.5


def test_summarize_keeps_attack_and_benign_denominators_separate() -> None:
    summary = summarize(
        [
            _result("a1", "jailbreak", True),
            _result("a2", "jailbreak", False, refusal=True),
            _result(
                "b1",
                "benign",
                False,
                case_type="benign",
                utility_success=True,
            ),
            _result(
                "b2",
                "benign",
                False,
                case_type="benign",
                refusal=True,
            ),
        ]
    )
    assert summary["n"] == 4
    assert summary["attack_n"] == 2
    assert summary["asr"] == 0.5
    assert summary["attack_refusal_rate"] == 0.5
    assert summary["benign_n"] == 2
    assert summary["utility_rate"] == 0.5
    assert summary["over_refusal_rate"] == 0.5
