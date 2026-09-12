# Week 1 Execution Plan

## Definition of done

- [x] `uv sync --extra dev` works.
- [x] `agentsecbench run --config ...` executes end-to-end.
- [x] JSONL attack dataset schema is stable for the starter milestone.
- [x] Model adapter interface is stable for the starter milestone.
- [x] Mock adapter works without external services.
- [x] Safe mock vs intentionally vulnerable mock comparison works.
- [ ] OpenAI-compatible HTTP adapter is validated against an authorized endpoint.
- [ ] Baseline evaluator outputs per-case `success` on a real model response.
- [x] Aggregate ASR is saved to `summary.json`.
- [ ] At least 20 synthetic cases exist across jailbreak + prompt injection.
- [x] Unit tests pass.
- [x] README documents the Week-1 reproduction command.

## Day 1 — Project bootstrap
- [x] Python 3.12 + uv environment.
- [x] Run safe mock experiment and tests.
- [x] Understand `schema.py`, `ModelAdapter`, and `runner.py`.
- [x] Understand `architecture.md` and `threat-model.md`.
- [x] Compare safe mock vs intentionally vulnerable mock.

## Day 2 — Model abstraction
- [ ] Test OpenAI-compatible adapter against a local or authorized endpoint.
- [ ] Record model/config/latency metadata.
- [ ] Never hard-code credentials.

## Day 3 — Dataset
- [ ] Expand to 20–30 synthetic cases:
  - jailbreak;
  - direct prompt injection;
  - indirect prompt injection.
- [ ] Keep assets synthetic and success criteria explicit.
- [ ] Separate attacker-controlled input from protected context.

## Day 4 — Evaluation
- [x] Keep keyword evaluator only as a baseline.
- [ ] Add one structured evaluator rule.
- [x] Report ASR overall and per category.

## Day 5 — Reproducibility
- [ ] Snapshot config and run metadata.
- [ ] Make repeated runs deterministic where possible.
- [ ] Add clear artifact naming.

## Day 6 — Analysis
- [x] Produce first controlled comparison with two mock backends.
- [ ] Compare at least two real model/config settings if available.
- [ ] Write 3–5 observations and limitations.

## Day 7 — Research review
- [ ] Clean README after real-model milestone.
- [ ] Write a Week-1 report.
- [x] Sync learned concepts into Notion.
- [ ] Decide Week-2 scope: Agent / Tool sandbox.
