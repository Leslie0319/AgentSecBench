# Week 1 Execution Plan

## Definition of done

- [x] `uv sync --extra dev` works.
- [x] `agentsecbench run --config ...` executes end-to-end.
- [x] JSONL attack dataset schema is stable for the smoke-test milestone.
- [x] Model adapter interface is stable for mock + OpenAI-compatible backends.
- [x] Mock adapter works without external services.
- [x] OpenAI-compatible HTTP adapter is implemented.
- [x] Baseline evaluator outputs per-case `success`.
- [x] Aggregate ASR is saved to `summary.json`.
- [ ] At least 20 synthetic cases exist across jailbreak + prompt injection.
- [x] Unit tests pass.
- [x] README documents the threat model / reproduction path.

## Day 1 — Project bootstrap
- [x] Python 3.12 + uv environment.
- [x] Run safe mock experiment and tests.
- [x] Run intentionally vulnerable mock comparison.
- [x] Read `architecture.md` and `threat-model.md`.
- [x] Understand `schema.py`, `ModelAdapter`, `runner.py`, Evaluator, and ASR.
- [x] Separate attacker-controlled prompt from protected context.

## Day 2 — First real model
- [x] Prepare Qwen3.7-Flash OpenAI-compatible config.
- [x] Send protected context through a system message.
- [x] Keep API key in `.env` / environment variable only.
- [x] Record latency, finish reason, generation settings, and token usage metadata.
- [x] Explicitly disable thinking mode for the first controlled run.
- [ ] Create a local Beijing-region Model Studio API key.
- [ ] Run the two-case real-model smoke test.
- [ ] Inspect `results.jsonl` and explain the model behavior case by case.

## Day 3 — Dataset
- [ ] Expand to 20–30 synthetic cases across jailbreak, direct prompt injection, and indirect prompt injection.
- [ ] Define explicit asset, attacker capability, and success criterion per case.

## Day 4 — Evaluation
- [x] Keep keyword evaluator as a baseline.
- [ ] Add one structured evaluator rule.
- [x] Report ASR overall and per category.

## Day 5 — Reproducibility
- [ ] Snapshot config and run metadata.
- [ ] Make repeated runs deterministic where possible.

## Day 6 — Analysis
- [x] Produce a controlled safe-vs-vulnerable mock comparison.
- [ ] Compare at least two real model/config settings.
- [ ] Write 3–5 observations and limitations.

## Day 7 — Research review
- [ ] Clean final Week-1 README/report.
- [ ] Write a Week-1 report.
- [x] Sync learned concepts into Notion.
- [ ] Decide Week-2 scope: Agent / Tool sandbox.
