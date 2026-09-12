# Week 1 Execution Plan

## Definition of done

- [ ] `uv sync --extra dev` works.
- [ ] `agentsecbench run --config ...` executes end-to-end.
- [ ] JSONL attack dataset schema is stable.
- [ ] Model adapter interface is stable.
- [ ] Mock adapter works without external services.
- [ ] OpenAI-compatible HTTP adapter is implemented.
- [ ] Baseline evaluator outputs per-case `success`.
- [ ] Aggregate ASR is saved to `summary.json`.
- [ ] At least 20 synthetic cases exist across jailbreak + prompt injection.
- [ ] Unit tests pass.
- [ ] README documents the threat model and reproduction command.

## Day 1 — Project bootstrap
- Python 3.12 + uv.
- Run mock experiment and tests.
- Read `architecture.md` and `threat-model.md`.
- Understand every data class in `schema.py`.

## Day 2 — Model abstraction
- Test OpenAI-compatible adapter against a local or authorized endpoint.
- Record model/config/latency metadata.
- Never hard-code credentials.

## Day 3 — Dataset
- Expand to 20–30 synthetic cases across jailbreak, direct prompt injection, and indirect prompt injection.

## Day 4 — Evaluation
- Keep keyword evaluator only as a baseline.
- Add one structured evaluator rule.
- Report ASR overall and per category.

## Day 5 — Reproducibility
- Snapshot config and run metadata.
- Make repeated runs deterministic where possible.

## Day 6 — Analysis
- Produce the first experiment table and write 3–5 observations and limitations.

## Day 7 — Research review
- Clean README and repo layout.
- Write a Week-1 report.
- Sync learned concepts into Notion.
- Decide Week-2 scope: Agent / Tool sandbox.
