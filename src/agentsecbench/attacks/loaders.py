from __future__ import annotations

import json
from pathlib import Path

from agentsecbench.schema import AttackCase


def load_jsonl(path: str | Path) -> list[AttackCase]:
    cases: list[AttackCase] = []
    with Path(path).open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                cases.append(AttackCase.model_validate(json.loads(stripped)))
            except Exception as exc:
                raise ValueError(f"Invalid JSONL at line {line_no}: {exc}") from exc
    return cases
