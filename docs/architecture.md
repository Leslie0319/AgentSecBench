# Architecture

## Minimal benchmark loop

```text
ExperimentConfig
      |
      v
 AttackCase loader
      |
      v
  ModelAdapter
      |
      v
 ModelResponse
      |
      v
   Evaluator
      |
      v
 EvaluationResult
      |
      +--> JSONL result log
      |
      +--> aggregate metrics
```

## Why a thin custom core?

The benchmark itself should expose exactly what prompt was sent, what model configuration was used, how success was judged, and which artifacts belong to each run.

Heavy agent frameworks can be integrated later at the boundary, but should not hide security-sensitive control flow during the first milestone.

## Controlled comparison principle

A useful benchmark should let us change one factor while keeping the rest fixed. Week 1 already demonstrates the simplest example:

```text
Same dataset
Same evaluator
Same metrics
      |
      +--> safe mock        -> low ASR
      |
      +--> vulnerable mock  -> high ASR
```

This does not prove anything about real model safety. It verifies that the evaluation pipeline can detect intentionally different model behavior under controlled conditions.

## Separation of responsibilities

- `AttackCase` defines what is tested.
- `ModelAdapter` defines how a model is called.
- `Evaluator` defines how success is judged.
- `metrics.py` defines how case-level judgments are aggregated.
- experiment config defines the controlled variables for one run.

Keeping these responsibilities separate is what later allows fair model, defense, or attack comparisons.
