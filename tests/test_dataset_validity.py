from agentsecbench.attacks.loaders import load_jsonl


def test_week1_attack_prompts_do_not_contain_protected_markers() -> None:
    cases = load_jsonl("data/attacks/week1.jsonl")

    for case in cases:
        for marker in case.success_markers:
            assert marker not in case.prompt, (
                f"{case.id}: protected success marker must not appear in attacker-controlled prompt"
            )
