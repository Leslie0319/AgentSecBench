from pathlib import Path

from agentsecbench.provenance import (
    build_run_metadata,
    sha256_file,
    write_config_snapshot,
)
from agentsecbench.schema import ExperimentConfig


def test_reproducibility_metadata_and_snapshot(tmp_path: Path) -> None:
    dataset = tmp_path / "dataset.jsonl"
    dataset.write_text('{"id":"x"}\n', encoding="utf-8")

    config = tmp_path / "experiment.yaml"
    config.write_text(
        "\n".join(
            [
                "run_id: test-run",
                "model:",
                "  backend: mock",
                "  model: mock-safe-model",
                f"dataset: {dataset.as_posix()}",
                f"output_dir: {(tmp_path / 'run').as_posix()}",
                "evaluator: structured_safety",
                "generation:",
                "  temperature: 0.0",
                "  max_tokens: 64",
                "",
            ]
        ),
        encoding="utf-8",
    )

    exp = ExperimentConfig.model_validate(
        {
            "run_id": "test-run",
            "model": {"backend": "mock", "model": "mock-safe-model"},
            "dataset": str(dataset),
            "output_dir": str(tmp_path / "run"),
            "evaluator": "structured_safety",
            "generation": {"temperature": 0.0, "max_tokens": 64},
        }
    )

    output_dir = tmp_path / "run"
    output_dir.mkdir()
    results = output_dir / "results.jsonl"
    summary = output_dir / "summary.json"
    snapshot = output_dir / "config.snapshot.yaml"
    results.write_text("{}\n", encoding="utf-8")
    summary.write_text("{}\n", encoding="utf-8")

    write_config_snapshot(config, snapshot)
    metadata = build_run_metadata(
        exp=exp,
        config_path=config,
        config_snapshot_path=snapshot,
        results_path=results,
        summary_path=summary,
    )

    assert snapshot.read_bytes() == config.read_bytes()
    assert metadata["schema_version"] == 1
    assert metadata["run_id"] == "test-run"
    assert metadata["inputs"]["dataset"]["sha256"] == sha256_file(dataset)
    assert metadata["artifacts"]["results.jsonl"]["sha256"] == sha256_file(results)
    assert len(metadata["inputs"]["config"]["sha256"]) == 64
    assert "commit_sha" in metadata["git"]
    assert "dirty" in metadata["git"]
