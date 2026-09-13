from collections import Counter

from agentsecbench.attacks.loaders import load_jsonl


DATASETS = [
    "data/attacks/week1.jsonl",
    "data/attacks/week1_expanded.jsonl",
]


def test_attack_prompts_do_not_contain_protected_markers() -> None:
    for dataset in DATASETS:
        cases = load_jsonl(dataset)
        for case in cases:
            for marker in case.success_markers:
                assert marker not in case.prompt, (
                    f"{case.id}: protected success marker must not appear in attacker-controlled prompt"
                )


def test_expanded_dataset_has_balanced_attack_categories() -> None:
    cases = load_jsonl("data/attacks/week1_expanded.jsonl")
    counts = Counter(case.category for case in cases)

    assert len(cases) == 24
    assert counts == {
        "jailbreak": 8,
        "direct_prompt_injection": 8,
        "indirect_prompt_injection": 8,
    }


def test_benign_controls_have_explicit_utility_ground_truth() -> None:
    cases = load_jsonl("data/attacks/benign_controls.jsonl")
    counts = Counter(case.category for case in cases)

    assert len(cases) == 8
    assert counts == {
        "benign_instruction_following": 4,
        "benign_external_content": 4,
    }
    for case in cases:
        assert case.case_type == "benign"
        assert case.utility_markers
        assert not case.success_markers
        assert case.protected_context is None
