# AgentSecBench

A reproducible benchmark and research sandbox for LLM / Agent security evaluation.

## What does AgentSecBench mean?

**AgentSecBench = Agent Security Benchmark.**

The project is designed to evolve from a minimal LLM security evaluation loop into a reproducible benchmark for Agent / Tool / MCP security research.

## Week-1 goal

Build the smallest complete loop:

`attack cases -> model adapter -> evaluator -> metrics -> JSONL results`

The first milestone intentionally focuses on infrastructure quality and reproducibility. Agent/MCP sandbox, RAG attacks, SFT/LoRA defenses, and automated attack search are later milestones.

## Core design principles

1. **Provider-agnostic**: model access is hidden behind a small adapter interface.
2. **Reproducible**: configs, datasets, outputs, and run metadata are explicit.
3. **Security-first**: every experiment starts from a threat model.
4. **Research-friendly**: baselines, metrics, and ablations are first-class.
5. **Minimal abstraction**: avoid heavy agent frameworks in the core during the first milestone.

## Quick start

```bash
# Python 3.12 recommended
uv sync --extra dev

uv run agentsecbench run \
  --config configs/experiments/week1_mock.yaml
```

The mock backend requires no API key and should produce:

```text
runs/week1-mock/results.jsonl
runs/week1-mock/summary.json
```

Run tests:

```bash
uv run pytest
uv run ruff check .
```

### Windows note

On Windows, some current `uv` editable-install / launcher issues can break imports when the project or virtual environment path contains non-ASCII characters. If `uv sync` succeeds but `import agentsecbench` still raises `ModuleNotFoundError`, clone the repository to an ASCII-only path such as `C:\dev\AgentSecBench` and recreate `.venv` there.

## Repository layout

```text
AgentSecBench/
├── configs/
│   ├── experiments/
│   └── models/
├── data/
│   └── attacks/
├── docs/
├── runs/                  # generated; ignored by git
├── src/agentsecbench/
│   ├── adapters/
│   ├── attacks/
│   ├── evaluators/
│   ├── cli.py
│   ├── io.py
│   ├── metrics.py
│   ├── runner.py
│   └── schema.py
└── tests/
```

## Roadmap

- **M0 / Week 1**: runner + JSONL datasets + mock/OpenAI-compatible adapters + baseline evaluator.
- **M1**: jailbreak + direct/indirect prompt injection benchmark.
- **M2**: Agent / Tool sandbox and permission-boundary evaluation.
- **M3**: RAG injection and data-exfiltration scenarios.
- **M4**: guards + policy engine + LoRA/SFT defense experiments.
- **M5**: automated attack search: generate -> score -> mutate -> verify.

## Safety scope

Use controlled test prompts, synthetic secrets, local sandboxes, and systems you are authorized to test. Do not use this project to target third-party systems without permission.
