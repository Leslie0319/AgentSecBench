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
