from __future__ import annotations

import hashlib
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from agentsecbench.schema import ExperimentConfig


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_config_snapshot(source: str | Path, target: str | Path) -> None:
    source_path = Path(source)
    target_path = Path(target)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_bytes(source_path.read_bytes())


def _git_output(args: list[str]) -> str | None:
    try:
        completed = subprocess.run(
            ["git", *args],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return completed.stdout.strip()


def git_state() -> dict[str, Any]:
    commit_sha = _git_output(["rev-parse", "HEAD"])
    status = _git_output(["status", "--porcelain"])
    return {
        "commit_sha": commit_sha,
        "dirty": bool(status) if status is not None else None,
    }


def build_run_metadata(
    *,
    exp: ExperimentConfig,
    config_path: str | Path,
    config_snapshot_path: str | Path,
    results_path: str | Path,
    summary_path: str | Path,
) -> dict[str, Any]:
    dataset_path = Path(exp.dataset)
    return {
        "schema_version": 1,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "run_id": exp.run_id,
        "experiment": {
            "evaluator": exp.evaluator,
            "model": exp.model.model,
            "backend": exp.model.backend,
            "temperature": exp.generation.temperature,
            "max_tokens": exp.generation.max_tokens,
        },
        "git": git_state(),
        "runtime": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
        },
        "inputs": {
            "config": {
                "path": str(config_path),
                "sha256": sha256_file(config_path),
            },
            "dataset": {
                "path": str(dataset_path),
                "sha256": sha256_file(dataset_path),
            },
        },
        "artifacts": {
            "config.snapshot.yaml": {
                "sha256": sha256_file(config_snapshot_path),
            },
            "results.jsonl": {
                "sha256": sha256_file(results_path),
            },
            "summary.json": {
                "sha256": sha256_file(summary_path),
            },
        },
    }
