from __future__ import annotations

from collections import defaultdict

from agentsecbench.schema import CaseRunResult


def summarize(results: list[CaseRunResult]) -> dict[str, object]:
    total = len(results)
    attack_results = [item for item in results if item.case.case_type == "attack"]
    benign_results = [item for item in results if item.case.case_type == "benign"]

    attack_successes = sum(item.evaluation.success for item in attack_results)
    attack_refusals = sum(
        bool(item.evaluation.signals.get("refusal", False)) for item in attack_results
    )
    utility_successes = sum(
        bool(item.evaluation.signals.get("utility_success", False))
        for item in benign_results
    )
    benign_refusals = sum(
        bool(item.evaluation.signals.get("refusal", False)) for item in benign_results
    )

    by_attack_category: dict[str, list[CaseRunResult]] = defaultdict(list)
    by_benign_category: dict[str, list[CaseRunResult]] = defaultdict(list)
    by_outcome: dict[str, int] = defaultdict(int)

    for item in results:
        if item.case.case_type == "attack":
            by_attack_category[item.case.category].append(item)
        else:
            by_benign_category[item.case.category].append(item)
        if item.evaluation.outcome:
            by_outcome[item.evaluation.outcome] += 1

    attack_category_summary = {
        category: {
            "n": len(items),
            "successes": sum(item.evaluation.success for item in items),
            "asr": (
                sum(item.evaluation.success for item in items) / len(items)
                if items
                else 0.0
            ),
        }
        for category, items in sorted(by_attack_category.items())
    }

    benign_category_summary = {
        category: {
            "n": len(items),
            "utility_successes": sum(
                bool(item.evaluation.signals.get("utility_success", False))
                for item in items
            ),
            "utility_rate": (
                sum(
                    bool(item.evaluation.signals.get("utility_success", False))
                    for item in items
                )
                / len(items)
                if items
                else 0.0
            ),
            "refusals": sum(
                bool(item.evaluation.signals.get("refusal", False)) for item in items
            ),
            "over_refusal_rate": (
                sum(
                    bool(item.evaluation.signals.get("refusal", False))
                    for item in items
                )
                / len(items)
                if items
                else 0.0
            ),
        }
        for category, items in sorted(by_benign_category.items())
    }

    summary: dict[str, object] = {
        "n": total,
        "attack_n": len(attack_results),
        "successes": attack_successes,
        "asr": (
            attack_successes / len(attack_results) if attack_results else 0.0
        ),
        "attack_refusals": attack_refusals,
        "attack_refusal_rate": (
            attack_refusals / len(attack_results) if attack_results else 0.0
        ),
        "benign_n": len(benign_results),
        "utility_successes": utility_successes,
        "utility_rate": (
            utility_successes / len(benign_results) if benign_results else 0.0
        ),
        "benign_refusals": benign_refusals,
        "over_refusal_rate": (
            benign_refusals / len(benign_results) if benign_results else 0.0
        ),
        "by_category": attack_category_summary,
        "by_benign_category": benign_category_summary,
    }
    if by_outcome:
        summary["by_outcome"] = dict(sorted(by_outcome.items()))
    return summary
