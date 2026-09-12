from __future__ import annotations

from collections import defaultdict

from agentsecbench.schema import CaseRunResult


def summarize(results: list[CaseRunResult]) -> dict[str, object]:
    total = len(results)
    successes = sum(item.evaluation.success for item in results)
    by_category: dict[str, list[bool]] = defaultdict(list)
    for item in results:
        by_category[item.case.category].append(item.evaluation.success)
    category_summary = {
        category: {"n": len(values), "successes": sum(values), "asr": (sum(values) / len(values)) if values else 0.0}
        for category, values in sorted(by_category.items())
    }
    return {"n": total, "successes": successes, "asr": (successes / total) if total else 0.0, "by_category": category_summary}
