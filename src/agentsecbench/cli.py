from __future__ import annotations

from pathlib import Path

import typer
from dotenv import load_dotenv

from agentsecbench.adapters.base import ModelAdapter
from agentsecbench.adapters.mock import MockAdapter
from agentsecbench.adapters.openai_compatible import OpenAICompatibleAdapter
from agentsecbench.adapters.vulnerable_mock import VulnerableMockAdapter
from agentsecbench.attacks.loaders import load_jsonl
from agentsecbench.evaluators.base import Evaluator
from agentsecbench.evaluators.keyword import KeywordLeakageEvaluator
from agentsecbench.evaluators.structured import StructuredSafetyEvaluator
from agentsecbench.io import (
    load_experiment_config,
    read_results,
    write_json,
    write_results,
)
from agentsecbench.metrics import summarize
from agentsecbench.runner import run_cases
from agentsecbench.schema import CaseRunResult

app = typer.Typer(no_args_is_help=True)


@app.callback()
def main() -> None:
    """AgentSecBench command-line interface."""
    load_dotenv()


def build_adapter(config) -> ModelAdapter:
    if config.backend == "mock":
        return MockAdapter(model=config.model)

    if config.backend == "mock_vulnerable":
        return VulnerableMockAdapter(model=config.model)

    if config.backend == "openai_compatible":
        if not config.base_url:
            raise ValueError("model.base_url is required for openai_compatible backend")
        return OpenAICompatibleAdapter(
            model=config.model,
            base_url=config.base_url,
            api_key_env=config.api_key_env,
            timeout_seconds=config.timeout_seconds,
            trust_env=config.trust_env,
            request_options=config.request_options,
        )

    raise ValueError(f"Unsupported backend: {config.backend}")


def build_evaluator(name: str) -> Evaluator:
    if name == "keyword_leakage":
        return KeywordLeakageEvaluator()
    if name == "structured_safety":
        return StructuredSafetyEvaluator()
    raise ValueError(f"Unsupported evaluator: {name}")


@app.command()
def run(config: str = typer.Option(..., "--config", "-c")) -> None:
    """Run one benchmark experiment from a YAML config."""
    exp = load_experiment_config(config)
    cases = load_jsonl(exp.dataset)
    adapter = build_adapter(exp.model)
    evaluator = build_evaluator(exp.evaluator)

    results = run_cases(
        cases=cases,
        adapter=adapter,
        evaluator=evaluator,
        temperature=exp.generation.temperature,
        max_tokens=exp.generation.max_tokens,
    )

    output_dir = Path(exp.output_dir)
    write_results(output_dir / "results.jsonl", results)
    summary = summarize(results)
    write_json(output_dir / "summary.json", summary)

    typer.echo(f"run_id={exp.run_id} n={summary['n']} asr={summary['asr']:.3f}")


@app.command()
def reevaluate(
    input_path: str = typer.Option(..., "--input", "-i"),
    evaluator: str = typer.Option("structured_safety", "--evaluator", "-e"),
    output_dir: str = typer.Option(..., "--output-dir", "-o"),
) -> None:
    """Re-evaluate saved model responses without calling the model again."""
    judge = build_evaluator(evaluator)
    prior_results = read_results(input_path)
    updated: list[CaseRunResult] = []

    for item in prior_results:
        evaluation = judge.evaluate(item.case, item.response)
        updated.append(
            CaseRunResult(
                case=item.case,
                response=item.response,
                evaluation=evaluation,
            )
        )

    target = Path(output_dir)
    write_results(target / "results.jsonl", updated)
    summary = summarize(updated)
    write_json(target / "summary.json", summary)
    typer.echo(
        f"reevaluated={summary['n']} evaluator={evaluator} asr={summary['asr']:.3f}"
    )
